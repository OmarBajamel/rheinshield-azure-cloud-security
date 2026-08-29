@description('Existing Log Analytics workspace with Microsoft Sentinel enabled.')
param workspaceName string

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: workspaceName
}

resource knownDeploymentPrincipals 'Microsoft.SecurityInsights/watchlists@2025-09-01' = {
  name: 'KnownDeploymentPrincipals'
  scope: workspace
  properties: {
    displayName: 'RheinShield Known Deployment Principals'
    description: 'Synthetic approved-principal and location pairs for RS013 fixture and lab validation.'
    watchlistAlias: 'KnownDeploymentPrincipals'
    provider: 'RheinShield'
    sourceType: 'Local'
    source: 'known-deployment-principals.csv'
    contentType: 'text/csv'
    numberOfLinesToSkip: 0
    itemsSearchKey: 'Principal'
    labels: [
      'RheinShield'
      'Synthetic'
    ]
    rawContent: loadTextContent('known-deployment-principals.csv')
  }
}
