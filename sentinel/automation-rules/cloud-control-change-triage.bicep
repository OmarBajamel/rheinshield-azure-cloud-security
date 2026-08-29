@description('Existing Log Analytics workspace with Microsoft Sentinel enabled.')
param workspaceName string

@description('Stable automation-rule resource identifier.')
param automationRuleId string = 'e646c906-0868-4398-8af7-2556ccddd203'

@description('Disabled by default until an operator reviews incident taxonomy and permissions.')
param automationEnabled bool = false

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: workspaceName
}

resource cloudControlChange 'Microsoft.SecurityInsights/automationRules@2025-09-01' = {
  name: automationRuleId
  scope: workspace
  properties: {
    displayName: 'RheinShield - Cloud control change triage'
    order: 120
    triggeringLogic: {
      isEnabled: automationEnabled
      triggersOn: 'Incidents'
      triggersWhen: 'Created'
      conditions: [
        {
          conditionType: 'Boolean'
          conditionProperties: {
            operator: 'Or'
            innerConditions: [
              {
                conditionType: 'Property'
                conditionProperties: {
                  propertyName: 'IncidentTitle'
                  operator: 'StartsWith'
                  propertyValues: [
                    'RS007'
                    'RS008'
                    'RS009'
                    'RS013'
                    'RS014'
                  ]
                }
              }
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
            { labelName: 'rheinshield-cloud-control' }
          ]
        }
      }
      {
        order: 2
        actionType: 'AddIncidentTask'
        actionConfiguration: {
          title: 'Validate change and prepare rollback'
          description: 'Compare the event with approved IaC and change records. Prepare a reviewed rollback; do not alter resources automatically.'
        }
      }
    ]
  }
}
