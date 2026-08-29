#!/usr/bin/env bash
set -euo pipefail

command -v az >/dev/null || { echo 'Azure CLI unavailable.' >&2; exit 1; }
suffix="${1:?Usage: scripts/destroy-lab.sh <4-8-character-suffix> [execute]}"
mode="${2:-plan}"
[[ "$suffix" =~ ^[a-z0-9]{4,8}$ ]] || { echo 'Unsafe suffix.' >&2; exit 1; }
[[ "$mode" == plan || "$mode" == execute ]] || { echo 'Mode must be plan or execute.' >&2; exit 1; }
subscription="$(az account show --query id -o tsv)"
[[ -n "${RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID:-}" && "$subscription" == "$RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID" ]] || { echo 'Select the explicitly allowlisted sandbox subscription.' >&2; exit 1; }
[[ -f .private/azure-bootstrap.env ]] || { echo 'Bootstrap provenance is required so resource and identity cleanup remain atomic.' >&2; exit 1; }
groups=("rg-rheinshield-lab-gwc-${suffix}-network" "rg-rheinshield-lab-gwc-${suffix}-security" "rg-rheinshield-lab-gwc-${suffix}-workload")
existing=()
for group in "${groups[@]}"; do
  [[ "$(az group exists -n "$group")" == true ]] || continue
  [[ "$(az group show -n "$group" --query tags.Project -o tsv)" == RheinShield ]] || { echo "Unexpected project tag: $group" >&2; exit 1; }
  [[ "$(az group show -n "$group" --query tags.Owner -o tsv)" == OmarBaJamel ]] || { echo "Unexpected owner tag: $group" >&2; exit 1; }
  [[ "$(az group show -n "$group" --query tags.Environment -o tsv)" == Lab ]] || { echo "Unexpected environment tag: $group" >&2; exit 1; }
  existing+=("$group")
done

plan_file=".private/destroy-plan-${suffix}.txt"
expected_groups="$(IFS=,; echo "${groups[*]}")"
if [[ "$mode" == plan ]]; then
  printf '%s|%s|%s\n' "$(date -u +%s)" "$subscription" "$expected_groups" > "$plan_file"
  chmod 600 "$plan_file"
  echo "Saved a 15-minute destruction plan for the exact groups and bootstrap identity: $plan_file"
  echo "Review it, then run: scripts/destroy-lab.sh $suffix execute"
  exit 0
fi

[[ -f "$plan_file" ]] || { echo 'A saved destruction plan is required.' >&2; exit 1; }
IFS='|' read -r planned_at planned_subscription planned_groups < "$plan_file"
now_epoch="$(date -u +%s)"
[[ "$planned_at" =~ ^[0-9]+$ && "$planned_subscription" == "$subscription" && "$planned_groups" == "$expected_groups" && "$now_epoch" -ge "$planned_at" && "$now_epoch" -le $((planned_at + 900)) ]] || { echo 'Destruction plan is stale or does not match the current exact scope.' >&2; exit 1; }
for group in "${existing[@]}"; do az group delete -n "$group" --yes; done
for group in "${groups[@]}"; do [[ "$(az group exists -n "$group")" == false ]] || { echo "Deletion verification failed: $group" >&2; exit 1; }; done
bash scripts/cleanup-bootstrap-identity.sh "$suffix"
rm -- "$plan_file"
echo "Verified absent: exact RheinShield lab groups and bootstrap identity for suffix $suffix."
