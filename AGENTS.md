# RheinShield contributor instructions

## Commands

- `npm run generate:data` produces deterministic public-demo data with seed `20260829`.
- `npm run build:public` builds the recruiter dashboard without Azure credentials.
- `python -m pytest -q` runs workload, telemetry, sanitizer, and content tests.
- `python tools/detection-test-harness/validate.py` validates Sentinel metadata and fixtures.
- `scripts/validate.ps1` or `scripts/validate.sh` runs the complete local quality gate.

## Safety and scope

- The default maximum incremental Azure spend is EUR 20. Stop before apply when the preflight cannot prove the estimate is within this ceiling.
- Live resources must use `rg-rheinshield-` resource groups and all mandatory lifecycle tags. Never modify the Tenant Root Group, unrelated management groups, existing tenant-wide Conditional Access, real users, or unrelated resources.
- Enterprise landing-zone code is plan-only unless an isolated hierarchy is independently proven. Conditional Access definitions remain disabled/report-only and scoped to disposable lab groups.
- Use GitHub OIDC; never create or commit a long-lived Azure client secret.
- `data/private/`, `evidence/private/`, `.private/`, state, plans, IDs, UPNs, IP addresses, tokens, and raw portal exports are private and ignored.
- Public screenshots and release artifacts must show the synthetic-data label and pass the sanitizer/privacy scan.
- Only evidence-backed statuses are allowed: `LIVE_DEPLOYED`, `LIVE_VALIDATED`, `PLAN_VALIDATED`, `FIXTURE_VALIDATED`, `READY_NOT_AUTHENTICATED`, `READY_LICENSE_REQUIRED`, `SKIPPED_COST_GUARD`, `UNAVAILABLE`, or `FAILED_WITH_EVIDENCE`.
- Release only after tests, IaC checks, PII/secret scans, screenshot review, checksums, and fresh-clone verification pass. Never post LinkedIn content.

## Definition of done

The public demo must run without Azure access; enterprise and lab IaC, 14 detection rules, 5 hunts, 3 workbooks, 3 automation rules, 3 dry-run playbooks, 25 risks, framework mappings, bilingual dashboard, evidence, screenshots, CV/social package, release, cleanup proof, and honest limitations must be present and verified.
