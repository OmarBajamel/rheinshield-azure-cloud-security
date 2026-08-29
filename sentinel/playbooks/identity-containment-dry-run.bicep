@description('Name of the disabled, dry-run-only Logic App.')
param workflowName string = 'la-rheinshield-identity-dry-run'

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
                'account'
              ]
              properties: {
                incidentId: { type: 'string' }
                account: { type: 'string' }
                requestedAction: { type: 'string' }
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
            playbook: 'identity-containment'
            incidentId: '@triggerBody()?[\'incidentId\']'
            target: '@triggerBody()?[\'account\']'
            proposedActions: [
              'Revoke sessions after analyst authorization'
              'Disable dedicated disposable lab identity only'
              'Require credential reset through approved process'
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
