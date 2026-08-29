#!/usr/bin/env bash
set -euo pipefail

command -v az >/dev/null || { echo 'Azure CLI unavailable: READY_NOT_AUTHENTICATED' >&2; exit 1; }
command -v terraform >/dev/null || { echo 'Terraform is required.' >&2; exit 1; }
command -v python >/dev/null || { echo 'Python is required for the cost attestation gate.' >&2; exit 1; }
subscription="$(az account show --query id -o tsv)"
[[ -n "${RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID:-}" && "$subscription" == "$RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID" ]] || { echo 'Select the explicitly allowlisted sandbox subscription.' >&2; exit 1; }
suffix="${1:-demo01}"
operation="${2:-plan}"
[[ "$suffix" =~ ^[a-z0-9]{4,8}$ ]] || { echo 'Suffix must be 4-8 lowercase alphanumeric characters.' >&2; exit 1; }
[[ "$operation" == plan || "$operation" == deploy ]] || { echo 'Operation must be plan or deploy.' >&2; exit 1; }
app_object_id=''; app_id=''; recorded_subscription=''; recorded_suffix=''
if [[ "${GITHUB_ACTIONS:-}" == true ]]; then
  [[ "$operation" == plan ]] || { echo 'GitHub Actions is plan-only; apply is local-operator only.' >&2; exit 1; }
  [[ "${GITHUB_REPOSITORY:-}" == 'OmarBajamel/rheinshield-azure-cloud-security' \
     && "${GITHUB_REF:-}" == 'refs/heads/main' \
     && "${GITHUB_EVENT_NAME:-}" == 'workflow_dispatch' \
     && "${GITHUB_WORKFLOW_REF:-}" == 'OmarBajamel/rheinshield-azure-cloud-security/.github/workflows/azure-lab.yml@refs/heads/main' \
     && -n "${RHEINSHIELD_CLIENT_ID:-}" \
     && -n "${RHEINSHIELD_APP_OBJECT_ID:-}" \
     && -n "${RHEINSHIELD_SP_OBJECT_ID:-}" \
     && -n "${RHEINSHIELD_TENANT_ID:-}" ]] || { echo 'GitHub workflow provenance mismatch.' >&2; exit 1; }
  [[ "$(az account show --query tenantId -o tsv)" == "$RHEINSHIELD_TENANT_ID" ]] || { echo 'Authenticated tenant does not match workflow provenance.' >&2; exit 1; }
else
  [[ -f .private/azure-bootstrap.env ]] || { echo 'Bootstrap provenance is required; refusing tag-only ownership inference.' >&2; exit 1; }
  while IFS='=' read -r key value; do
    case "$key" in
      AZURE_APP_OBJECT_ID) app_object_id="$value" ;;
      AZURE_CLIENT_ID) app_id="$value" ;;
      AZURE_SUBSCRIPTION_ID) recorded_subscription="$value" ;;
      RHEINSHIELD_SUFFIX) recorded_suffix="$value" ;;
    esac
  done < .private/azure-bootstrap.env
  [[ -n "$app_object_id" && -n "$app_id" && "$recorded_subscription" == "$subscription" && "$recorded_suffix" == "$suffix" ]] || { echo 'Bootstrap provenance does not match the current scope.' >&2; exit 1; }
  [[ "$(az ad app show --id "$app_object_id" --query appId -o tsv)" == "$app_id" && "$(az ad app show --id "$app_object_id" --query displayName -o tsv)" == "id-rheinshield-github-${suffix}" ]] || { echo 'Bootstrap application provenance mismatch.' >&2; exit 1; }
  subject="$(az ad app federated-credential list --id "$app_object_id" --query "[?name=='github-azure-lab'].subject | [0]" -o tsv)"
  [[ "$subject" == 'repo:OmarBajamel/rheinshield-azure-cloud-security:environment:azure-lab' ]] || { echo 'Federated credential provenance mismatch.' >&2; exit 1; }
fi
export TF_VAR_suffix="$suffix"
export TF_VAR_expires_at="${TF_VAR_expires_at:-$(date -u -d '+24 hours' +'%Y-%m-%dT%H:%M:%SZ')}"
[[ "${TF_VAR_container_image:-}" =~ @sha256:[a-f0-9]{64}$ ]] || { echo 'TF_VAR_container_image must be an owner-approved digest-pinned OCI reference.' >&2; exit 1; }
expiry_epoch="$(date -u -d "$TF_VAR_expires_at" +%s)"
now_epoch="$(date -u +%s)"
(( expiry_epoch > now_epoch && expiry_epoch <= now_epoch + 86700 )) || { echo 'Expiry must be in the future and no more than 24 hours away.' >&2; exit 1; }
groups=("rg-rheinshield-lab-gwc-${suffix}-network" "rg-rheinshield-lab-gwc-${suffix}-security" "rg-rheinshield-lab-gwc-${suffix}-workload")
for group in "${groups[@]}"; do
  [[ "$(az group exists -n "$group")" == true ]] || { echo "Bootstrap-created group is missing: $group" >&2; exit 1; }
  [[ "$(az group show -n "$group" --query tags.Project -o tsv)" == RheinShield && "$(az group show -n "$group" --query tags.Owner -o tsv)" == OmarBaJamel && "$(az group show -n "$group" --query tags.Environment -o tsv)" == Lab ]] || { echo "Ownership tag mismatch: $group" >&2; exit 1; }
  group_expiry="$(az group show -n "$group" --query tags.ExpiresAt -o tsv)"
  [[ -n "$group_expiry" && "$(date -u -d "$group_expiry" +%s)" -gt "$now_epoch" ]] || { echo "Bootstrap scope is expired: $group; destroy and bootstrap a new suffix." >&2; exit 1; }
done

terraform -chdir=infra/lab init -backend=false
terraform -chdir=infra/lab validate
terraform -chdir=infra/lab plan -out=rheinshield.tfplan
if [[ "$operation" == deploy ]]; then
  command -v infracost >/dev/null || { echo 'Infracost is required for deploy.' >&2; exit 1; }
  mkdir -p .private
  terraform -chdir=infra/lab show -json rheinshield.tfplan > .private/rheinshield-plan.json
  infracost breakdown --path .private/rheinshield-plan.json --currency EUR --format json --out-file .private/infracost-raw.json
  python tools/cost-gate/attest.py --raw-infracost .private/infracost-raw.json --plan infra/lab/rheinshield.tfplan --output .private/cost-estimate.json
  python tools/cost-gate/verify.py --attestation .private/cost-estimate.json --raw-infracost .private/infracost-raw.json --plan infra/lab/rheinshield.tfplan --max-eur 20
  destroy_plan=".private/destroy-plan-${suffix}.txt"
  [[ -f "$destroy_plan" ]] || { echo 'A reviewed, saved destruction plan is required before apply.' >&2; exit 1; }
  expected_groups="$(IFS=,; echo "${groups[*]}")"
  IFS='|' read -r planned_at planned_subscription planned_groups < "$destroy_plan"
  gate_epoch="$(date -u +%s)"
  [[ "$planned_at" =~ ^[0-9]+$ && "$planned_subscription" == "$subscription" && "$planned_groups" == "$expected_groups" && "$gate_epoch" -ge "$planned_at" && "$gate_epoch" -le $((planned_at + 900)) ]] || { echo 'Destruction plan is stale or does not match the exact apply scope.' >&2; exit 1; }
  for group in "${groups[@]}"; do az group update -n "$group" --set "tags.ExpiresAt=$TF_VAR_expires_at" -o none; done
  terraform -chdir=infra/lab apply rheinshield.tfplan
else
  echo 'Plan created. No apply requested.'
fi
