param(
  [ValidatePattern('^[a-z0-9]{4,8}$')][string]$Suffix = 'demo01',
  [ValidateSet('germanywestcentral', 'westeurope')][string]$Location = 'germanywestcentral'
)
$ErrorActionPreference = 'Stop'
if (-not (Get-Command az -ErrorAction SilentlyContinue)) { throw 'Azure CLI is required.' }
$context = az account show --only-show-errors | ConvertFrom-Json
$allowedSubscription = $env:RHEINSHIELD_ALLOWED_SUBSCRIPTION_ID
if ([string]::IsNullOrWhiteSpace($allowedSubscription) -or $context.id -ne $allowedSubscription) { throw 'Select the explicitly allowlisted sandbox subscription first.' }

$repository = 'OmarBajamel/rheinshield-azure-cloud-security'
$environment = 'azure-lab'
$expiry = [DateTime]::UtcNow.AddHours(24).ToString('yyyy-MM-ddTHH:mm:ssZ')
$groups = @(
  "rg-rheinshield-lab-gwc-$Suffix-network",
  "rg-rheinshield-lab-gwc-$Suffix-security",
  "rg-rheinshield-lab-gwc-$Suffix-workload"
)
$displayName = "id-rheinshield-github-$Suffix"
$credentialName = 'github-azure-lab'
$privateDirectory = Join-Path $PSScriptRoot '../.private'
$privateFile = Join-Path $privateDirectory 'azure-bootstrap.env'

foreach ($group in $groups) {
  if ((az group exists --name $group) -eq 'true') { throw "Refusing pre-existing resource group: $group" }
}
$apps = @(az ad app list --display-name $displayName --output json | ConvertFrom-Json)
if ($apps.Count -ne 0) { throw "Refusing pre-existing or ambiguous Entra application: $displayName" }

$createdGroups = [System.Collections.Generic.List[string]]::new()
$appObjectId = $null
$appId = $null
$spObjectId = $null
try {
  $appObjectId = az ad app create --display-name $displayName --sign-in-audience AzureADMyOrg --query id -o tsv
  $appId = az ad app show --id $appObjectId --query appId -o tsv
  $spObjectId = az ad sp create --id $appId --query id -o tsv
  $credential = @{
    name = $credentialName
    issuer = 'https://token.actions.githubusercontent.com'
    subject = "repo:${repository}:environment:${environment}"
    audiences = @('api://AzureADTokenExchange')
    description = 'RheinShield protected GitHub environment; no client secret'
  } | ConvertTo-Json -Compress
  az ad app federated-credential create --id $appObjectId --parameters $credential --output none
  $createdCredential = @(az ad app federated-credential list --id $appObjectId --output json | ConvertFrom-Json) | Where-Object name -eq $credentialName
  if ($createdCredential.Count -ne 1 -or $createdCredential[0].subject -ne "repo:${repository}:environment:${environment}" -or $createdCredential[0].audiences[0] -ne 'api://AzureADTokenExchange') { throw 'Federated credential verification failed.' }

  foreach ($group in $groups) {
    az group create --name $group --location $Location --tags Project=RheinShield Owner=OmarBaJamel Environment=Lab DataClassification=Synthetic ManagedBy=Codex ExpiresAt=$expiry --output none
    $createdGroups.Add($group)
  }
  foreach ($group in $groups) {
    $scope = az group show --name $group --query id -o tsv
    az role assignment create --assignee-object-id $spObjectId --assignee-principal-type ServicePrincipal --role Reader --scope $scope --output none
  }

  New-Item -ItemType Directory -Path $privateDirectory -Force | Out-Null
  @(
    "AZURE_APP_OBJECT_ID=$appObjectId",
    "AZURE_CLIENT_ID=$appId",
    "AZURE_SP_OBJECT_ID=$spObjectId",
    "AZURE_TENANT_ID=$($context.tenantId)",
    "AZURE_SUBSCRIPTION_ID=$($context.id)",
    "RHEINSHIELD_SUFFIX=$Suffix"
  ) | Set-Content -LiteralPath $privateFile
} catch {
  foreach ($group in $createdGroups) { az group delete --name $group --yes --no-wait 2>$null }
  if (-not [string]::IsNullOrWhiteSpace($spObjectId)) { az ad sp delete --id $spObjectId 2>$null }
  if (-not [string]::IsNullOrWhiteSpace($appObjectId)) { az ad app delete --id $appObjectId 2>$null }
  throw 'Bootstrap failed; only objects created by this invocation were queued for cleanup.'
}
Write-Host 'Created three new exact-name groups and one new secretless, exact-subject plan identity with Reader only.'
Write-Host 'Private identifiers are stored only in .private/azure-bootstrap.env; destroy-lab removes both cloud resources and identity.'
