# NIS2/BSIG gap assessment

| Area | Evidence now | Status | Gap / treatment |
|---|---|---|---|
| Risk analysis and security policy | risk register, security policies | FIXTURE_VALIDATED | management approval is scenario-only |
| Incident handling | 14 detections, IR plan, INC-001 | FIXTURE_VALIDATED | no production/on-call measurement |
| Business continuity and crisis | BIA, backup/recovery, Notfallhandbuch | PLAN_VALIDATED | live restore and crisis exercise needed |
| Supply-chain security | supplier policy and risk | PLAN_VALIDATED | contractual/technical supplier evidence absent |
| Acquisition/development/vulnerability | CI design, secure workload, scan workflows | PLAN_VALIDATED | shipped container scan requires build runner |
| Control effectiveness | fixtures, evidence matrix, reviews | FIXTURE_VALIDATED | no live control sampling |
| Cyber hygiene/training | policy requirement | UNAVAILABLE | training delivery/evidence outside portfolio |
| Cryptography | TLS/Key Vault design | PLAN_VALIDATED | key lifecycle not live-validated |
| Personnel/access/assets | inventory, JML, RBAC/PIM | PLAN_VALIDATED | Entra licensing and tenant evidence absent |
| MFA/secure communication | CA templates | READY_LICENSE_REQUIRED | report-only/live validation required |
| Incident reporting | decision/communication matrix | PLAN_VALIDATED | legal applicability and organizational contacts required |
| Management governance | executive dashboard and risk owners | PLAN_VALIDATED | real approval/training not represented |

No row claims legal compliance. The practical effect of non-live evidence is that configuration quality can be reviewed, but operating effectiveness cannot be concluded.
