@description('Existing Log Analytics workspace with Microsoft Sentinel enabled.')
param workspaceName string

@description('Stable automation-rule resource identifier.')
param automationRuleId string = 'e646c906-0868-4398-8af7-2556ccddd202'

@description('Disabled by default until an operator reviews incident taxonomy and permissions.')
param automationEnabled bool = false

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: workspaceName
}

resource identityIncident 'Microsoft.SecurityInsights/automationRules@2025-09-01' = {
  name: automationRuleId
  scope: workspace
  properties: {
    displayName: 'RheinShield - Identity incident enrichment task'
    order: 110
    triggeringLogic: {
      isEnabled: automationEnabled
      triggersOn: 'Incidents'
      triggersWhen: 'Created'
      conditions: [
        {
          conditionType: 'Property'
          conditionProperties: {
            propertyName: 'IncidentTactics'
            operator: 'Contains'
            propertyValues: [
              'CredentialAccess'
              'PrivilegeEscalation'
            ]
          }
        }
      ]
    }
    actions: [
      {
        order: 1
        actionType: 'ModifyProperties'
        actionConfiguration: {
          labels: [
            { labelName: 'rheinshield-identity' }
          ]
        }
      }
      {
        order: 2
        actionType: 'AddIncidentTask'
        actionConfiguration: {
          title: 'Collect identity context'
          description: 'Review sign-in, MFA, device, role, workload-credential, and session context before changing the identity.'
        }
      }
    ]
  }
}
