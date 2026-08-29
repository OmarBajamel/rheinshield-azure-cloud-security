param(
  [switch]$PlanOnly,
  [ValidatePattern('^[a-z0-9]{4,8}$')][string]$Suffix = 'demo01'
)
$ErrorActionPreference = 'Stop'
& "$PSScriptRoot/azure-preflight.ps1"
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python is required for the cost attestation gate.' }
$env:TF_VAR_suffix = $Suffix
if ([string]::IsNullOrWhiteSpace($env:TF_VAR_expires_at)) { $env:TF_VAR_expires_at = [DateTime]::UtcNow.AddHours(24).ToString('yyyy-MM-ddTHH:mm:ssZ') }
if ([string]::IsNullOrWhiteSpace($env:TF_VAR_container_image) -or $env:TF_VAR_container_image -notmatch '@sha256:[a-f0-9]{64}$') { throw 'TF_VAR_container_image must be an owner-approved digest-pinned OCI reference.' }
$expiry = [DateTime]::Parse($env:TF_VAR_expires_at).ToUniversalTime()
if ($expiry -le [DateTime]::UtcNow -or $expiry -gt [DateTime]::UtcNow.AddHours(24).AddMinutes(5)) { throw 'Lab expiry must be in the future and no more than 24 hours from deployment.' }
$groups = @(
  "rg-rheinshield-lab-gwc-$Suffix-network",
  "rg-rheinshield-lab-gwc-$Suffix-security",
  "rg-rheinshield-lab-gwc-$Suffix-workload"
)
$privateFile = Join-Path $PSScriptRoot '../.private/azure-bootstrap.env'
if (-not (Test-Path -LiteralPath $privateFile)) { throw 'Bootstrap provenance is required; refusing tag-only ownership inference.' }
$record = @{}
foreach ($line in Get-Content -LiteralPath $privateFile) {
  $key, $value = $line -split '=', 2
  $record[$key] = $value
}
$context = az account show --only-show-errors | ConvertFrom-Json
if ($record.RHEINSHIELD_SUFFIX -ne $Suffix -or $record.AZURE_SUBSCRIPTION_ID -ne $context.id -or [string]::IsNullOrWhiteSpace($record.AZURE_APP_OBJECT_ID) -or [string]::IsNullOrWhiteSpace($record.AZURE_CLIENT_ID)) { throw 'Bootstrap provenance does not match the current scope.' }
$app = az ad app show --id $record.AZURE_APP_OBJECT_ID --output json | ConvertFrom-Json
if ($app.appId -ne $record.AZURE_CLIENT_ID -or $app.displayName -ne "id-rheinshield-github-$Suffix") { throw 'Bootstrap application provenance mismatch.' }
$credential = @(az ad app federated-credential list --id $record.AZURE_APP_OBJECT_ID --output json | ConvertFrom-Json) | Where-Object name -eq 'github-azure-lab'
if ($credential.Count -ne 1 -or $credential[0].subject -ne 'repo:OmarBajamel/rheinshield-azure-cloud-security:environment:azure-lab') { throw 'Federated credential provenance mismatch.' }
foreach ($group in $groups) {
  if ((az group exists --name $group) -ne 'true') { throw "Bootstrap-created group is missing: $group" }
  $metadata = az group show --name $group --output json | ConvertFrom-Json
  if ($metadata.tags.Project -ne 'RheinShield' -or $metadata.tags.Owner -ne 'OmarBaJamel' -or $metadata.tags.Environment -ne 'Lab') { throw "Ownership tag mismatch: $group" }
  if ([string]::IsNullOrWhiteSpace($metadata.tags.ExpiresAt) -or [DateTime]::Parse($metadata.tags.ExpiresAt).ToUniversalTime() -le [DateTime]::UtcNow) { throw "Bootstrap scope is expired: $group; destroy and bootstrap a new suffix." }
}

$labDirectory = Join-Path $PSScriptRoot '../infra/lab'
$privateDirectory = Join-Path $PSScriptRoot '../.private'
$plan = Join-Path $labDirectory 'rheinshield.tfplan'
Push-Location $labDirectory
try {
  terraform init -backend=false
  terraform validate
  terraform plan -out=rheinshield.tfplan
} finally { Pop-Location }
if ($PlanOnly) {
  Write-Host 'Plan created. No apply requested.'
  exit 0
}
if (-not (Get-Command infracost -ErrorAction SilentlyContinue)) { throw 'Infracost is required for deploy.' }
New-Item -ItemType Directory -Path $privateDirectory -Force | Out-Null
$planJson = Join-Path $privateDirectory 'rheinshield-plan.json'
$rawCost = Join-Path $privateDirectory 'infracost-raw.json'
$attestation = Join-Path $privateDirectory 'cost-estimate.json'
terraform -chdir=$labDirectory show -json rheinshield.tfplan | Set-Content -LiteralPath $planJson -Encoding utf8
infracost breakdown --path $planJson --currency EUR --format json --out-file $rawCost
python "$PSScriptRoot/../tools/cost-gate/attest.py" --raw-infracost $rawCost --plan $plan --output $attestation
python "$PSScriptRoot/../tools/cost-gate/verify.py" --attestation $attestation --raw-infracost $rawCost --plan $plan --max-eur 20
$destroyPlan = Join-Path $privateDirectory "destroy-plan-$Suffix.json"
if (-not (Test-Path -LiteralPath $destroyPlan)) { throw 'A reviewed, saved destruction plan is required before apply.' }
$destroy = Get-Content -LiteralPath $destroyPlan -Raw | ConvertFrom-Json
$destroyAge = [DateTime]::UtcNow - [DateTime]::Parse($destroy.createdAt).ToUniversalTime()
if ($destroyAge.TotalSeconds -lt 0 -or $destroyAge.TotalMinutes -gt 15 -or $destroy.subscriptionId -ne $context.id -or (Compare-Object @($destroy.groups) $groups) -or $destroy.includesBootstrapIdentity -ne $true) { throw 'Destruction plan is stale or does not match the exact apply scope.' }
foreach ($group in $groups) { az group update --name $group --set "tags.ExpiresAt=$($env:TF_VAR_expires_at)" --output none }
terraform -chdir=$labDirectory apply rheinshield.tfplan
