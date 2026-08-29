# Cost model

The public demo, GitHub Pages, tests, and fixtures require no Azure spend. A temporary lab would use three exact resource groups, VNet/NSGs, two private endpoints/private DNS zones, Key Vault, Storage, Log Analytics/Sentinel at minimal ingestion, and an internal consumption-style Container Apps workload. Exact regional pricing must be queried immediately before apply because prices and free allowances change; private-endpoint charges make the EUR 20 full-run gate especially important.

Status for this run: `READY_NOT_AUTHENTICATED`. No Azure resource was created, so observed incremental cost is €0 and no live estimate is represented. The placeholder-free machine record in `artifacts/evidence/infracost.json` identifies the missing authentication/tool context rather than inventing a number.

Key Vault purge protection is intentionally enabled with seven-day soft-delete retention. After resource-group deletion, Azure may retain the soft-deleted vault object/name during that protection window even though no billable active resource remains; teardown evidence must report that residual state rather than claiming immediate name reuse.
