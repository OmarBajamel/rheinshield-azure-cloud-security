param([Parameter(Mandatory)][ValidatePattern('^[a-z0-9]{4,8}$')][string]$Suffix)
$ErrorActionPreference = 'Stop'
if (-not (Get-Command az -ErrorAction SilentlyContinue)) { throw 'Azure CLI is required.' }
$privateFile = Join-Path $PSScriptRoot '../.private/azure-bootstrap.env'
if (-not (Test-Path -LiteralPath $privateFile)) { throw 'Private bootstrap provenance file is required; refusing identity lookup by display name.' }
$record = @{}
foreach ($line in Get-Content -LiteralPath $privateFile) {
  $key, $value = $line -split '=', 2
  $record[$key] = $value
}
foreach ($required in @('AZURE_APP_OBJECT_ID', 'AZURE_CLIENT_ID', 'AZURE_SP_OBJECT_ID', 'AZURE_SUBSCRIPTION_ID', 'RHEINSHIELD_SUFFIX')) {
  if ([string]::IsNullOrWhiteSpace($record[$required])) { throw "Missing bootstrap provenance field: $required" }
}
if ($record.RHEINSHIELD_SUFFIX -ne $Suffix) { throw 'Bootstrap provenance belongs to another suffix.' }
$context = az account show --only-show-errors | ConvertFrom-Json
if ([string]::IsNullOrWhiteSpace($env:RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID) -or $context.id -ne $env:RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID -or $context.id -ne $record.AZURE_SUBSCRIPTION_ID) { throw 'Subscription/provenance mismatch.' }
$app = az ad app show --id $record.AZURE_APP_OBJECT_ID --output json | ConvertFrom-Json
if ($app.displayName -ne "id-rheinshield-github-$Suffix" -or $app.appId -ne $record.AZURE_CLIENT_ID) { throw 'Application provenance mismatch.' }
$credential = @(az ad app federated-credential list --id $record.AZURE_APP_OBJECT_ID --output json | ConvertFrom-Json) | Where-Object name -eq 'github-azure-lab'
if ($credential.Count -ne 1 -or $credential[0].subject -ne 'repo:OmarBajamel/rheinshield-azure-cloud-security:environment:azure-lab') { throw 'Federated credential provenance mismatch.' }

az ad sp delete --id $record.AZURE_SP_OBJECT_ID
az ad app delete --id $record.AZURE_APP_OBJECT_ID
$remaining = az ad app list --app-id $record.AZURE_CLIENT_ID --query 'length(@)' -o tsv
if ($remaining -ne '0') { throw 'Application deletion verification failed.' }
Remove-Item -LiteralPath $privateFile
Write-Host "Verified absent: RheinShield bootstrap identity for suffix $Suffix."
