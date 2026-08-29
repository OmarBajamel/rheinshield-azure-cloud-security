#!/usr/bin/env bash
set -euo pipefail

command -v az >/dev/null || { echo 'Azure CLI is required.' >&2; exit 1; }
suffix="${1:?Usage: scripts/cleanup-bootstrap-identity.sh <4-8-character-suffix>}"
[[ "$suffix" =~ ^[a-z0-9]{4,8}$ ]] || { echo 'Unsafe suffix.' >&2; exit 1; }
private_file='.private/azure-bootstrap.env'
[[ -f "$private_file" ]] || { echo 'Private bootstrap provenance file is required; refusing identity lookup by display name.' >&2; exit 1; }

app_object_id=''; app_id=''; sp_object_id=''; recorded_subscription=''; recorded_suffix=''
while IFS='=' read -r key value; do
  case "$key" in
    AZURE_APP_OBJECT_ID) app_object_id="$value" ;;
    AZURE_CLIENT_ID) app_id="$value" ;;
    AZURE_SP_OBJECT_ID) sp_object_id="$value" ;;
    AZURE_SUBSCRIPTION_ID) recorded_subscription="$value" ;;
    RHEINSHIELD_SUFFIX) recorded_suffix="$value" ;;
  esac
done < "$private_file"
[[ -n "$app_object_id" && -n "$app_id" && -n "$sp_object_id" && "$recorded_suffix" == "$suffix" ]] || { echo 'Bootstrap provenance is incomplete or belongs to another suffix.' >&2; exit 1; }
subscription="$(az account show --query id -o tsv)"
[[ -n "${RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID:-}" && "$subscription" == "$RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID" && "$subscription" == "$recorded_subscription" ]] || { echo 'Subscription/provenance mismatch.' >&2; exit 1; }
display_name="$(az ad app show --id "$app_object_id" --query displayName -o tsv)"
verified_app_id="$(az ad app show --id "$app_object_id" --query appId -o tsv)"
[[ "$display_name" == "id-rheinshield-github-${suffix}" && "$verified_app_id" == "$app_id" ]] || { echo 'Application provenance mismatch.' >&2; exit 1; }
verified_sp_app_id="$(az ad sp show --id "$sp_object_id" --query appId -o tsv)"
[[ "$verified_sp_app_id" == "$app_id" ]] || { echo 'Service-principal provenance mismatch.' >&2; exit 1; }
subject="$(az ad app federated-credential list --id "$app_object_id" --query "[?name=='github-azure-lab'].subject | [0]" -o tsv)"
[[ "$subject" == 'repo:OmarBajamel/rheinshield-azure-cloud-security:environment:azure-lab' ]] || { echo 'Federated credential subject mismatch.' >&2; exit 1; }

az ad sp delete --id "$sp_object_id"
az ad app delete --id "$app_object_id"
[[ "$(az ad app list --app-id "$app_id" --query 'length(@)' -o tsv)" == 0 ]] || { echo 'Application deletion verification failed.' >&2; exit 1; }
rm -- "$private_file"
echo "Verified absent: RheinShield bootstrap identity for suffix $suffix."
