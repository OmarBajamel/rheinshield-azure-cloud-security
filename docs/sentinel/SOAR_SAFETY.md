# SOAR design and safety controls

The pack contains three Microsoft Sentinel automation-rule templates and three
Logic App Consumption workflow templates. All automation rules default to
`automationEnabled = false`. All workflows are deployed with `state: 'Disabled'`,
set `dryRun: true`, return `externalSideEffects: false`, and contain only Compose
and Response actions. They include no API connection, outbound HTTP action,
role assignment, email, Teams, ticketing, identity mutation, or Azure resource
mutation. This is `PLAN_VALIDATED` plus repository static validation, not a live run.

## Automation rules

| Template | Trigger and condition | Safe action |
|---|---|---|
| `high-severity-triage.bicep` | New High incident | Add label and evidence/containment checklist task |
| `identity-incident-enrichment.bicep` | New Credential Access or Privilege Escalation incident | Add identity label and context-collection task |
| `cloud-control-change-triage.bicep` | New RheinShield cloud-control incident title | Add cloud-control label and rollback-review task |

Automation rules use `Microsoft.SecurityInsights/automationRules@2025-09-01`.
They never invoke a playbook automatically in this pack. An incident label/task
is reversible and workspace-scoped, but still requires deployment review.

## Dry-run playbooks

| Template | Input | Output only |
|---|---|---|
| `identity-containment-dry-run.bicep` | Incident ID, account, proposed action | Session/identity containment plan |
| `network-rollback-dry-run.bicep` | Incident ID, resource ID, observed rule | IaC comparison and rollback plan |
| `storage-protection-dry-run.bicep` | Incident ID, storage resource ID, classification | Access-restriction and token-review plan |

The workflows use `Microsoft.Logic/workflows@2019-05-01`, the current stable
deployment API shown by Microsoft Learn. A system-assigned identity is created
for future least-privilege use, but this repository assigns it no role.

## Controlled promotion to live response

1. Deploy only to a dedicated project resource group after cost and scope gates.
2. Keep workflows disabled and run a template validation plus security review.
3. Define one exact disposable lab target and a separate approval identity.
4. Add the minimum connector and RBAC action; avoid subscription-wide roles.
5. Test with a synthetic incident and capture sanitized evidence.
6. Add explicit approval, idempotency, retry, timeout, and failure paths.
7. Enable one automation rule, observe it, and retain a manual kill switch.
8. Remove test RBAC and connections during cleanup.

Production containment of real identities or resources is deliberately outside
the authorization and evidence provided by this content pack.
