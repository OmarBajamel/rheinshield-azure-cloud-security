# INC-001 lessons learned

## What worked in the exercise

- Stable rule IDs, deterministic fixtures and evidence hashes made results repeatable.
- Identity, control-plane and data-access signals formed one inspectable timeline.
- Dry-run playbooks preserved safety while producing analyst tasks and rollback steps.
- The capability matrix prevented fixture outcomes from being presented as live Sentinel efficacy.

## Gaps and owners

| Gap | Owner | Due | Evidence of closure |
|---|---|---:|---|
| Contractor privilege can outlive business need | IAM Lead | 30 days | access-review decision set |
| Workload credential changes need stronger approval | Platform Owner | 60 days | policy/change evidence |
| Diagnostic-setting deletion needs resilient alerting | SOC Lead | 30 days | RS008 canary and runbook |
| Recovery evidence lacks a live restore | Operations | 90 days | authorized restore-test record |
| Production false-positive behavior is unknown | Detection Engineering | pilot + 30 days | controlled live canary results |

The exercise does not claim a risk reduction. It identifies testable improvements and evidence owners.
