param(
  [Parameter(Mandatory)][ValidatePattern('^[a-z0-9]{4,8}$')][string]$Suffix,
  [switch]$Execute
)
$ErrorActionPreference = 'Stop'
& "$PSScriptRoot/azure-preflight.ps1"
$privateFile = Join-Path $PSScriptRoot '../.private/azure-bootstrap.env'
if (-not (Test-Path -LiteralPath $privateFile)) { throw 'Bootstrap provenance is required so resource and identity cleanup remain atomic.' }
$context = az account show --only-show-errors | ConvertFrom-Json
$groups = @(
  "rg-rheinshield-lab-gwc-$Suffix-network",
  "rg-rheinshield-lab-gwc-$Suffix-security",
  "rg-rheinshield-lab-gwc-$Suffix-workload"
)
$existing = @()
foreach ($group in $groups) {
  if ((az group exists --name $group) -ne 'true') { continue }
  $tag = az group show --name $group --query tags.Project -o tsv
  $owner = az group show --name $group --query tags.Owner -o tsv
  $environment = az group show --name $group --query tags.Environment -o tsv
  if ($tag -ne 'RheinShield' -or $owner -ne 'OmarBaJamel' -or $environment -ne 'Lab') { throw "Refusing target with unexpected ownership tags: $group" }
  $existing += $group
}

$planFile = Join-Path $PSScriptRoot "../.private/destroy-plan-$Suffix.json"
if (-not $Execute) {
  @{
    schemaVersion = '1.0.0'
    createdAt = [DateTime]::UtcNow.ToString('o')
    subscriptionId = $context.id
    groups = $groups
    includesBootstrapIdentity = $true
  } | ConvertTo-Json | Set-Content -LiteralPath $planFile
  Write-Host "Saved a 15-minute destruction plan: $planFile"
  Write-Host "Review it, then run: ./scripts/destroy-lab.ps1 -Suffix $Suffix -Execute"
  exit 0
}

if (-not (Test-Path -LiteralPath $planFile)) { throw 'A saved destruction plan is required.' }
$plan = Get-Content -LiteralPath $planFile -Raw | ConvertFrom-Json
$age = [DateTime]::UtcNow - [DateTime]::Parse($plan.createdAt).ToUniversalTime()
if ($age.TotalSeconds -lt 0 -or $age.TotalMinutes -gt 15 -or $plan.subscriptionId -ne $context.id -or (Compare-Object @($plan.groups) $groups)) { throw 'Destruction plan is stale or does not match the current exact scope.' }
foreach ($group in $existing) { az group delete --name $group --yes }
foreach ($group in $groups) { if ((az group exists --name $group) -eq 'true') { throw "Deletion verification failed: $group still exists." } }
& "$PSScriptRoot/cleanup-bootstrap-identity.ps1" -Suffix $Suffix
Remove-Item -LiteralPath $planFile
Write-Host "Verified absent: exact RheinShield lab groups and bootstrap identity for suffix $Suffix."
