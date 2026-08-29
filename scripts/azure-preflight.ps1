$ErrorActionPreference = 'Stop'
if (-not (Get-Command az -ErrorAction SilentlyContinue)) { throw 'Azure CLI unavailable: remain READY_NOT_AUTHENTICATED.' }
if (-not (Get-Command terraform -ErrorAction SilentlyContinue)) { throw 'Terraform unavailable: install an official maintained release.' }
$context = az account show --only-show-errors | ConvertFrom-Json
if (-not $context.id) { throw 'No authenticated Azure subscription context.' }
$allowedSubscription = $env:RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID
if ([string]::IsNullOrWhiteSpace($allowedSubscription)) { throw 'RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID must be set to the approved sandbox subscription.' }
if ($context.id -ne $allowedSubscription) { throw 'Authenticated subscription does not match the approved RheinShield sandbox subscription.' }
$ceilingValue = $env:RHEINSHIELD_MAX_INCREMENTAL_COST_EUR
if ([string]::IsNullOrWhiteSpace($ceilingValue)) { $ceilingValue = '20' }
$ceiling = [decimal]$ceilingValue
if ($ceiling -gt 20) { throw 'Cost ceiling cannot exceed EUR 20 for this project.' }
Write-Host 'Authenticated Azure context found. Identifiers intentionally suppressed.'
Write-Host "Cost ceiling: EUR $ceiling. Continue only after prefix collision and estimate checks."
