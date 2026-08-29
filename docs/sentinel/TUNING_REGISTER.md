# Detection tuning and false-positive register

Owner for unresolved entries: SOC Detection Engineering. Each exclusion must
have a business owner, reason, expiry, and regression fixture. Global suppression
of a privileged identity, wildcard source, or production subscription is prohibited.

| Rule | Likely benign source | Initial tuning control | Validation before merge | State |
|---|---|---|---|---|
| RS001 | Shared proxy or broken application | Named proxy list plus account-diversity threshold | Replay 14 days; retain privileged-account coverage | Candidate |
| RS002 | User corrects password | Trusted-location threshold, risk/device correlation | Sample successful sessions and verify sequence | Candidate |
| RS003 | VPN/mobile geolocation | Named VPN exits; require device/risk context | Compare connector coordinates and VPN inventory | Candidate |
| RS004 | Approved PIM activation | Ticket and activation-duration enrichment | Verify permanent assignments still alert | Candidate |
| RS005 | Scheduled key rotation | Automation identity and change-window watchlist | Ensure unexpected issuer/lifetime remains visible | Candidate |
| RS006 | Approved report-only change | Change-window enrichment, not actor exclusion | Test delete, exclusion, and grant weakening | Candidate |
| RS007 | Temporary lab exposure | Resource-ID exception with expiry | Verify wildcard admin ports cannot be suppressed broadly | Candidate |
| RS008 | Resource retirement | Lifecycle tag and decommission ticket | Ensure monitoring deletion precedes resource deletion only when approved | Candidate |
| RS009 | Public static-content account | Governed account watchlist | Keep anonymous blob enablement visible | Candidate |
| RS010 | Secret inventory/rotation | Managed-identity baseline per vault | Test burst and distinct-secret dimensions separately | Candidate |
| RS011 | Signed deployment script | Script hash, signer, parent, and window | Decode safely and retain unknown parent coverage | Candidate |
| RS012 | Backup/analytics job | Identity, schedule, account, and volume baseline | Test object-count and byte thresholds independently | Candidate |
| RS013 | Newly onboarded CI identity | Approved principal/location watchlist with expiry | Validate OIDC subject and unexpected region case | Candidate |
| RS014 | Tool with incomplete RBAC | Deployment-window annotation and identity threshold | Retain high-sensitivity interactive principal coverage | Candidate |

## Change procedure

1. Attach representative sanitized results and the proposed business rationale.
2. Add or update both benign and malicious regression fixtures.
3. Run the offline harness and, where available, a non-production Log Analytics replay.
4. Obtain SOC and data-owner approval for an exclusion that can hide activity.
5. Record review date, reviewer, measurable effect, and expiry in the change record.
6. Re-evaluate after 30 days, a source-schema change, a threshold breach, or an incident miss.

The current register is design-time material. It contains no measured production
false-positive rate because no live tenant data was used.
