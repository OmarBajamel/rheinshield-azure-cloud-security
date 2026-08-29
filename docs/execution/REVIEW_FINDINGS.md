# Independent review findings

This register is populated during the five independent release reviews. Severity uses Critical, High, Medium, Low, and Note. Release is blocked by unresolved Critical or High findings.

| ID | Review | Severity | Finding | Resolution | Status |
|---|---|---|---|---|---|
| REV-000 | Bootstrap | Medium | Initial Sites dependency graph exhausted local disk | Adapted to lean React/Vite Sites output and removed only project-created caches | RESOLVED |
| REV-A01 | Azure architecture | High | Hosted workflow exported `RHEINSHIELD_CLIENT_ID` while the deploy script checked an unspecified `AZURE_CLIENT_ID` | Bound the plan-only path to explicit `RHEINSHIELD_*` provenance and verified the authenticated tenant | RESOLVED |
| REV-A02 | Azure architecture | High | Reader-only hosted plan could trigger provider registration | Disabled automatic AzureRM resource-provider registration in the lab provider | RESOLVED |
| REV-A03 | Azure architecture | High | Apply did not require a saved destruction plan | Both Bash and PowerShell apply paths now require an exact-scope plan created within 15 minutes | RESOLVED |
| REV-A04 | Azure architecture | High | Bootstrap cleanup did not bind the service-principal object to the recorded application ID | Both cleanup paths verify the service principal `appId` before deletion | RESOLVED |
| REV-A05 | Azure architecture | High | Terraform evidence predated final networking/workload inputs | Re-ran recursive format, all three root initializations/validations, lab native test, TFLint, and the custom IaC gate after the last HCL change | RESOLVED |
| REV-D01 | Detection engineering | High | Hunting queries were honestly marked unauthenticated but the structural validator still required fixture validation | Validator now requires `READY_NOT_AUTHENTICATED` for hunts; analytics fixtures remain separately fixture-validated | RESOLVED |
| REV-S01 | Security/privacy | High | Release builder accepted dirty and untracked source inputs | Builder now refuses any dirty source tree, archives tracked files only, and records commit/tree provenance | RESOLVED |
| REV-S02 | Dependency security | High | `pytest` 8.4.2 was affected by PYSEC-2026-1845 | Raised the development floor to the fixed pytest 9 line; tests and `pip-audit` passed | RESOLVED |
| REV-S03 | Fresh-clone dependency security | High | The clean clone exposed GHSA-fx2h-pf6j-xcff in Vite 8.0.13 | Upgraded to Vite 8.2.2; full npm audit, build, unit, and browser suites passed | RESOLVED |
| REV-C01 | Compliance | High | Four MCSB crosswalks asserted controls that did not directly support the mapped practice | Risk, supplier, and sanitization rows now assert no direct control; secure CI maps to DS-2/DS-3/DS-4 | RESOLVED |
| REV-C02 | Compliance | High | Four evidence modes contradicted the NIS2 gap assessment and dashboard totals | Continuity, supplier, secure CI, and incident-reporting rows now use `PLAN_VALIDATED`; generated totals are 9/7/2/1/1 | RESOLVED |
| REV-F01 | Frontend/recruiter | Note | All eight routes in both languages, responsive behavior, PDFs, and credibility wording were reviewed | No Critical or High finding; representative browser and PDF evidence retained | RESOLVED |
| REV-R01 | Release provenance | High | Pre-release ZIP and manifest were generated before the final source revision | Builder now refuses dirty input and records the clean source commit/tree/archive hash; exact archives are rescanned before the generated-evidence commit | RESOLVED |

Architecture and compliance/frontend re-reviews reported no unresolved Critical or High blocker after the listed remediations. Security release provenance is closed only by the checked-in clean-build record, exact archive scans, hashes, and manifest.
