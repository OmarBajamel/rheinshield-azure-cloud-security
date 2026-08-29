# Architecture decision records

## ADR-001 — Two infrastructure tracks

Accepted. Keep the enterprise management-group architecture plan-only and the lab resource-group scoped. This prevents a portfolio exercise from changing unrelated tenant governance.

## ADR-002 — Terraform plus Bicep

Accepted. Terraform is the primary platform language; Bicep is used for Sentinel resources where the current SecurityInsights/Logic Apps resource model is clearer and already validated by the content harness.

## ADR-003 — Offline-first evidence

Accepted. The public dashboard is built from deterministic fixtures. Live evidence can enrich it only after automated sanitization and privacy review.

## ADR-004 — Cost-sensitive omissions

Accepted. Azure Firewall, Bastion, paid Defender plans, high-volume Sentinel ingestion, and regional failover deployments remain designed but not activated under the €20 ceiling.

## ADR-005 — Vite instead of Vinext

Accepted. The Sites scaffold's Vinext dependency graph exceeded available workspace capacity. The same Sites Vite plugin and React UI are retained with a materially smaller deterministic dependency set; static GitHub Pages is the required runtime.
