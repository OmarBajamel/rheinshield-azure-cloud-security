@description('Name of the disabled, dry-run-only Logic App.')
param workflowName string = 'la-rheinshield-storage-dry-run'

@description('Azure region for the Logic App resource.')
param location string = resourceGroup().location

resource workflow 'Microsoft.Logic/workflows@2019-05-01' = {
  name: workflowName
  location: location
  tags: {
    Project: 'RheinShield'
    Owner: 'OmarBaJamel'
    Environment: 'Lab'
    DataClassification: 'Synthetic'
    ManagedBy: 'Codex'
    ExpiresAt: '2026-09-05T00:00:00Z'
    SafetyMode: 'DryRun'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    state: 'Disabled'
    definition: {
      '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#'
      contentVersion: '1.0.0.0'
      parameters: {}
      triggers: {
        manual: {
          type: 'Request'
          kind: 'Http'
          inputs: {
            schema: {
              type: 'object'
              required: [
                'incidentId'
                'storageResourceId'
              ]
              properties: {
                incidentId: { type: 'string' }
                storageResourceId: { type: 'string' }
                dataClassification: { type: 'string' }
              }
            }
          }
        }
      }
      actions: {
        Build_dry_run_plan: {
          type: 'Compose'
          inputs: {
            dryRun: true
            playbook: 'storage-protection'
            incidentId: '@triggerBody()?[\'incidentId\']'
            target: '@triggerBody()?[\'storageResourceId\']'
            proposedActions: [
              'Disable anonymous blob access after approval'
              'Restore network default deny after approval'
              'Review and revoke scoped access tokens after approval'
            ]
            externalSideEffects: false
          }
        }
        Return_dry_run_plan: {
          type: 'Response'
          runAfter: {
            Build_dry_run_plan: [
              'Succeeded'
            ]
          }
          inputs: {
            statusCode: 200
            body: '@outputs(\'Build_dry_run_plan\')'
          }
        }
      }
      outputs: {}
    }
    parameters: {}
  }
}
