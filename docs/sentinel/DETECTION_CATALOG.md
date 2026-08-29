# RheinShield Microsoft Sentinel detection catalog

Status: `FIXTURE_VALIDATED`. All rules are disabled by default and use synthetic,
deterministic fixtures. No rule in this catalog has been queried against a live
Log Analytics workspace. Production enablement requires connector, schema,
retention, ingestion-delay, and false-positive validation.

| ID | Detection | Severity | Data source | Frequency / lookback | Primary entities | Fixture |
|---|---|---:|---|---|---|---|
| RS001 | Password spray across accounts | High | `SigninLogs` | 5m / 15m | IP | `rs001-password-spray.json` |
| RS002 | Success after repeated failures | High | `SigninLogs` | 5m / 30m | Account, IP | `rs002-success-after-failures.json` |
| RS003 | Improbable travel | Medium | `SigninLogs.LocationDetails` | 15m / 2h | Account, IP | `rs003-impossible-travel.json` |
| RS004 | Privileged role assignment/elevation | High | `AuditLogs` | 5m / 10m | Account | `rs004-privileged-role-assignment.json` |
| RS005 | Workload-identity credential added | High | `AuditLogs` | 5m / 10m | Account | `rs005-service-principal-credential.json` |
| RS006 | Conditional Access/risk policy change | High | `AuditLogs` | 5m / 10m | Account | `rs006-conditional-access-change.json` |
| RS007 | Unrestricted inbound network rule | High | `AzureActivity` request properties | 5m / 15m | Account, Azure resource | `rs007-unrestricted-inbound-rule.json` |
| RS008 | Monitoring/security control deleted | High | `AzureActivity` | 5m / 15m | Account, Azure resource | `rs008-monitoring-control-deleted.json` |
| RS009 | Storage exposure weakened | High | `AzureActivity` request properties | 5m / 15m | Account, Azure resource | `rs009-storage-public-access.json` |
| RS010 | Key Vault enumeration/access spike | High | `AzureDiagnostics` | 5m / 10m | IP, Azure resource | `rs010-key-vault-access-spike.json` |
| RS011 | Encoded/obfuscated PowerShell | Medium | `SecurityEvent` 4688 | 5m / 10m | Host, account, process | `rs011-encoded-powershell.json` |
| RS012 | Mass object download | High | `StorageBlobLogs` | 5m / 15m | IP, Azure resource | `rs012-mass-object-download.json` |
| RS013 | Unfamiliar deployment principal/location | Medium | `AzureActivity`, watchlist | 15m / 30m | Account, Azure resource | `rs013-unfamiliar-deployment-principal.json` |
| RS014 | Repeated denied Azure operations | Medium | `AzureActivity` | 5m / 15m | Account, IP | `rs014-repeated-denied-operations.json` |

Every YAML definition is the source of truth and contains a stable UUID, full
KQL, data-source requirements, ISO-8601 scheduling values, threshold, entity
mappings, ATT&CK tactics and techniques, expected false positives, tuning and
response guidance, fixture path, evaluator, and expected result. The content
test harness checks that contract and executes one benign and one malicious
normalized scenario per rule.

## Deployment gates

Before enabling a rule in any workspace:

1. Confirm the named table and referenced columns exist in the target tenant.
2. Replay a representative historical window and review every result with a data owner.
3. Measure ingestion latency and make `queryPeriod` long enough to cover it without duplicate floods.
4. Configure named-location, automation-window, CI-principal, and lifecycle watchlists with owners and expiry.
5. Validate entity mappings and incident grouping in a non-production workspace.
6. Enable progressively, record the production baseline, and update the tuning register through review.

The fixture metrics are regression evidence for the committed synthetic cases;
they do not estimate real-world precision, recall, attack prevention, or compliance.
