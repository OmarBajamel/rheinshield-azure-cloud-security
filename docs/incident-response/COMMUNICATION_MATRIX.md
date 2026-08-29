# Incident communication matrix

This project prepares decision paths and sends no email, Teams, SMS, ticket or regulatory notification.

| Audience | Trigger | Owner | Content | Channel | Target |
|---|---|---|---|---|---|
| Incident team | validated High incident | SOC Lead | facts, scope, tasks, evidence links | approved internal bridge | immediate |
| Management | critical service/privileged impact | Incident Commander | business impact, decisions, forecast | approved crisis channel | 30 min |
| DPO/legal | personal-data or reportability question | CISO | known facts, uncertainty, clock | confidential channel | immediate |
| BSI authority | legal threshold met | Management/legal | statutory early warning/notification content | official reporting route | deadline per current BSIG assessment |
| Customers/suppliers | material service/data effect and approved wording | Communications | impact, actions, support | authorized external channel | decision-based |
| Insurer/law enforcement | contractual/legal trigger | Legal | minimum necessary evidence | approved route | decision-based |

The current German obligations and dates are referenced in `docs/research/GERMAN_SOURCE_NOTES.md`; legal counsel confirms applicability and deadlines for a real incident.
