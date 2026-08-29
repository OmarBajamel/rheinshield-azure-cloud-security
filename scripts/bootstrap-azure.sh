#!/usr/bin/env bash
set -euo pipefail

command -v az >/dev/null || { echo 'Azure CLI is required.' >&2; exit 1; }
suffix="${1:-demo01}"
[[ "$suffix" =~ ^[a-z0-9]{4,8}$ ]] || { echo 'Unsafe suffix.' >&2; exit 1; }
location="${RHEINSHIELD_LOCATION:-germanywestcentral}"
[[ "$location" == germanywestcentral || "$location" == westeurope ]] || { echo 'Location is not allowlisted.' >&2; exit 1; }
repository='OmarBajamel/rheinshield-azure-cloud-security'
environment='azure-lab'
subscription="$(az account show --query id -o tsv)"
[[ -n "${RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID:-}" && "$subscription" == "$RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID" ]] || { echo 'Select the explicitly allowlisted sandbox subscription.' >&2; exit 1; }
tenant="$(az account show --query tenantId -o tsv)"
expiry="$(date -u -d '+24 hours' +'%Y-%m-%dT%H:%M:%SZ')"
groups=("rg-rheinshield-lab-gwc-${suffix}-network" "rg-rheinshield-lab-gwc-${suffix}-security" "rg-rheinshield-lab-gwc-${suffix}-workload")
display_name="id-rheinshield-github-${suffix}"
credential_name='github-azure-lab'
private_file='.private/azure-bootstrap.env'

for group in "${groups[@]}"; do
  [[ "$(az group exists -n "$group")" == false ]] || { echo "Refusing pre-existing resource group: $group" >&2; exit 1; }
done
app_count="$(az ad app list --display-name "$display_name" --query 'length(@)' -o tsv)"
[[ "$app_count" == 0 ]] || { echo "Refusing pre-existing or ambiguous Entra application: $display_name" >&2; exit 1; }

created_groups=()
app_object_id=''
app_id=''
sp_object_id=''
cleanup_failed_bootstrap() {
  set +e
  for group in "${created_groups[@]}"; do az group delete -n "$group" --yes --no-wait >/dev/null 2>&1; done
  [[ -z "$sp_object_id" ]] || az ad sp delete --id "$sp_object_id" >/dev/null 2>&1
  [[ -z "$app_object_id" ]] || az ad app delete --id "$app_object_id" >/dev/null 2>&1
  echo 'Bootstrap failed; only objects created by this invocation were queued for cleanup.' >&2
}
trap cleanup_failed_bootstrap ERR

app_object_id="$(az ad app create --display-name "$display_name" --sign-in-audience AzureADMyOrg --query id -o tsv)"
app_id="$(az ad app show --id "$app_object_id" --query appId -o tsv)"
sp_object_id="$(az ad sp create --id "$app_id" --query id -o tsv)"
parameters="{\"name\":\"$credential_name\",\"issuer\":\"https://token.actions.githubusercontent.com\",\"subject\":\"repo:$repository:environment:$environment\",\"audiences\":[\"api://AzureADTokenExchange\"],\"description\":\"RheinShield protected environment; no client secret\"}"
az ad app federated-credential create --id "$app_object_id" --parameters "$parameters" -o none
subject="$(az ad app federated-credential list --id "$app_object_id" --query "[?name=='$credential_name'].subject | [0]" -o tsv)"
audience="$(az ad app federated-credential list --id "$app_object_id" --query "[?name=='$credential_name'].audiences[0] | [0]" -o tsv)"
[[ "$subject" == "repo:$repository:environment:$environment" && "$audience" == 'api://AzureADTokenExchange' ]] || { echo 'Federated credential verification failed.' >&2; exit 1; }

for group in "${groups[@]}"; do
  az group create -n "$group" -l "$location" --tags Project=RheinShield Owner=OmarBaJamel Environment=Lab DataClassification=Synthetic ManagedBy=Codex ExpiresAt="$expiry" -o none
  created_groups+=("$group")
done
for group in "${groups[@]}"; do
  scope="$(az group show -n "$group" --query id -o tsv)"
  az role assignment create --assignee-object-id "$sp_object_id" --assignee-principal-type ServicePrincipal --role Reader --scope "$scope" -o none
done

mkdir -p .private
umask 077
printf 'AZURE_APP_OBJECT_ID=%s\nAZURE_CLIENT_ID=%s\nAZURE_SP_OBJECT_ID=%s\nAZURE_TENANT_ID=%s\nAZURE_SUBSCRIPTION_ID=%s\nRHEINSHIELD_SUFFIX=%s\n' "$app_object_id" "$app_id" "$sp_object_id" "$tenant" "$subscription" "$suffix" > "$private_file"
trap - ERR
echo 'Created three new exact-name groups and one new secretless, exact-subject plan identity with Reader only.'
echo 'Private identifiers are stored only in .private/azure-bootstrap.env; destroy-lab removes both cloud resources and identity.'
