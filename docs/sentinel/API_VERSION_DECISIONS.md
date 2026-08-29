# Sentinel content API-version decisions

Verified against official Microsoft Learn resource references on 2026-08-29.
These choices describe template syntax support; they do not claim that any
resource was deployed or that a tenant has the required license and permissions.

| Resource | Version used | Decision |
|---|---:|---|
| `Microsoft.SecurityInsights/alertRules` | `2025-09-01` | Latest stable version listed in the official template reference; used for the analytics-rule content contract/deployment target. |
| `Microsoft.SecurityInsights/automationRules` | `2025-09-01` | Latest stable version listed in the official template reference; supports property/boolean conditions, incident tasks, property changes, and playbook actions. This pack uses only tasks and labels. |
| `Microsoft.SecurityInsights/watchlists` | `2025-09-01` | Latest stable version listed in the official template reference; used to load the synthetic `KnownDeploymentPrincipals` CSV required by RS013. |
| `Microsoft.Insights/workbooks` | `2023-06-01` | Latest stable workbook deployment version in the official reference; `serializedData` contains `Notebook/1.0` JSON. |
| `Microsoft.Logic/workflows` | `2019-05-01` | Current stable Logic App Consumption workflow deployment version listed by Microsoft; used for disabled dry-run workflows. |
| `Microsoft.OperationalInsights/workspaces` | `2023-09-01` | Stable existing-resource reference used only to scope Sentinel extension resources; the templates do not create a workspace. |

Official references:

- [Microsoft.SecurityInsights alertRules](https://learn.microsoft.com/en-us/azure/templates/microsoft.securityinsights/alertrules)
- [Microsoft.SecurityInsights automationRules](https://learn.microsoft.com/en-us/azure/templates/microsoft.securityinsights/automationrules)
- [Microsoft.SecurityInsights watchlists](https://learn.microsoft.com/en-us/azure/templates/microsoft.securityinsights/watchlists)
- [Microsoft.Insights workbooks](https://learn.microsoft.com/en-us/azure/templates/microsoft.insights/workbooks)
- [Microsoft.Logic workflows](https://learn.microsoft.com/en-us/azure/templates/microsoft.logic/workflows)
- [Microsoft.OperationalInsights workspaces](https://learn.microsoft.com/en-us/azure/templates/microsoft.operationalinsights/workspaces)

## Operational decision

The repository is the source of truth for custom content. Rules and automation
remain disabled until target schemas, connectors, cost, licensing, RBAC, and
tuning have been checked. Preview APIs were intentionally avoided. The Microsoft
Defender portal is the operational experience for current Sentinel workflows,
but that portal choice does not change the ARM resource-provider contracts above.
