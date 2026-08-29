# INC-001 - Compromised Privileged Contractor Account and Cloud Control Changes

**Classification:** Synthetic tabletop/detection exercise  
**Status:** Contained (simulated)  
**Validation:** `FIXTURE_VALIDATED`  
**Scope:** fictional RheinCommerce GmbH; no real account or Azure resource was touched

## Executive technical summary

A password-spray pattern was followed by a suspicious successful contractor sign-in, unusual travel, privileged elevation, service-principal credential creation, identity-policy change, weakened network/storage controls, logging deletion, Key Vault enumeration, safe encoded-process telemetry, mass synthetic object access, unfamiliar deployment and privilege discovery. Fourteen deterministic rule fixtures detected the designed anomalies; paired benign fixtures remained quiet. The sequence demonstrates correlation and response engineering, not production efficacy.

## Exercise metrics

First malicious activity begins at 07:25 UTC. The first alert/incident is created at 07:31 (simulated MTTD 6 minutes). An analyst acknowledges at 07:40 (simulated MTTA 9 minutes). Containment is completed at 08:28 (simulated MTTR 48 minutes from acknowledgement). These are exercise calculations, not operational service metrics.

## Timeline and detection-to-evidence map

| UTC | Event | Detection | Evidence | Decision |
|---:|---|---|---|---|
| 07:25 | 12 failures across 6 accounts | RS001 | `rs001-password-spray.json` | preserve sign-in context |
| 07:31 | successful contractor sign-in; incident opened | RS002 | `rs002-success-after-failures.json` | High severity; start triage |
| 07:37 | synthetic impossible travel | RS003 | `rs003-impossible-travel.json` | validate location fixture |
| 07:40 | analyst acknowledgement | workflow evidence | public timeline | scope account/session impact |
| 07:44 | privileged role activation | RS004 | role-assignment fixture | recommend revoke elevation |
| 07:48 | workload credential added | RS005 | service-principal fixture | recommend remove new credential |
| 07:51 | Conditional Access changed | RS006 | policy-change fixture | compare approved baseline |
| 07:55 | NSG allows unrestricted inbound | RS007 | network-change fixture | produce rollback plan |
| 07:58 | diagnostic setting deleted | RS008 | activity fixture | restore logging first |
| 08:01 | storage network weakened | RS009 | storage-change fixture | restore deny/default network |
| 08:04 | 34 Key Vault operations / 14 aliases | RS010 | vault fixture | review secrets; rotation plan |
| 08:07 | encoded PowerShell pattern (not executed) | RS011 | process fixture | isolate only in safe lab |
| 08:10 | 126 synthetic objects downloaded | RS012 | storage fixture | scope data affected |
| 08:14 | unfamiliar deployment principal/location | RS013 | activity fixture | deny pending verification |
| 08:18 | 11 denied operations across 4 actions | RS014 | activity fixture | treat as privilege discovery |
| 08:28 | exercise containment complete | all | decision log + plan | move to recovery |

## Investigation method

1. Confirm synthetic mode, incident clock, rule versions, hashes, and ingestion window.
2. Pivot from the account to IP/location, authentication result, role assignment, workload identity, resource changes, Key Vault/storage access and process entity.
3. Order events by time and correlate stable public aliases; do not infer causality from one event.
4. Compare changed controls with Terraform/policy baselines and approved-change records.
5. Record what is known, inferred and unverified. Preserve raw evidence privately; publish only sanitized aggregates.

## Root cause and contributing factors

Exercise root cause: a fictional contractor credential was compromised after repeated authentication attempts. Contributing design gaps were standing/activatable privilege without a sufficiently strong device boundary, weak workload-credential change controls, delayed logging-integrity alerting, and supplier-access review gaps. These are scenario findings, not facts about a real company.

## Containment, eradication and recovery

- Dry-run recommendations: revoke sessions, disable only the disposable lab identity, remove the new workload credential, end role activation, restore CA/NSG/storage/diagnostic baselines, block identified fixture indicators, and rotate affected synthetic secrets.
- Validate audit completeness, check for additional credentials/assignments, redeploy trusted configuration from IaC, and confirm rule/connector health.
- Restore service in risk order: identity/logging, control-plane baseline, secrets, storage/network, workload.
- Monitor for 72 simulated hours; document owner acceptance before closure.

No playbook sends messages or actively disables a real user. Default automation creates tags/tasks/comments and a containment change plan only.

## 30/60/90-day roadmap

- 30 days: require phishing-resistant admin authentication, remove standing contractor privilege, protect diagnostic settings, tune correlated identity alerts.
- 60 days: implement workload-identity change approval, quarterly supplier access review, restore-test evidence, and policy remediation.
- 90 days: test cross-region recovery, measure production false positives after an authorized pilot, and exercise management notification/reporting decision paths.
