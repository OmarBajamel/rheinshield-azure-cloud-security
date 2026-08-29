@description('Existing Log Analytics workspace with Microsoft Sentinel enabled.')
param workspaceName string

@description('Stable automation-rule resource identifier.')
param automationRuleId string = 'e646c906-0868-4398-8af7-2556ccddd201'

@description('Disabled by default until an operator reviews incident taxonomy and permissions.')
param automationEnabled bool = false

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: workspaceName
}

resource highSeverityTriage 'Microsoft.SecurityInsights/automationRules@2025-09-01' = {
  name: automationRuleId
  scope: workspace
  properties: {
    displayName: 'RheinShield - High-severity triage checklist'
    order: 100
    triggeringLogic: {
      isEnabled: automationEnabled
      triggersOn: 'Incidents'
      triggersWhen: 'Created'
      conditions: [
        {
          conditionType: 'Property'
          conditionProperties: {
            propertyName: 'IncidentSeverity'
            operator: 'Equals'
            propertyValues: [
              'High'
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
            { labelName: 'rheinshield-triage-required' }
          ]
        }
      }
      {
        order: 2
        actionType: 'AddIncidentTask'
        actionConfiguration: {
          title: 'Validate high-severity evidence and containment scope'
          description: 'Confirm entities, data freshness, detection rule, business impact, and authorization before containment.'
        }
      }
    ]
  }
}
