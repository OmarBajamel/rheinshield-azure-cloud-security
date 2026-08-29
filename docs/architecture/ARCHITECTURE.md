# RheinShield architecture

RheinShield deliberately separates a statically/provider-validated enterprise landing-zone reference from a mock-plan-validated single-subscription lab. The fictional RheinCommerce GmbH has development, test, and production workloads, but the public run creates no tenant hierarchy and consumes no private Azure data.

## Enterprise reference

The target architecture contains Platform (Management, Connectivity, Identity) and Landing Zones (Corp, Online, Sandbox). Its documented control plane includes central Azure Policy, Log Analytics/Sentinel, private DNS, and hub-and-spoke networking. The repository's enterprise Terraform root implements the official Azure Landing Zone pattern through pinned `Azure/avm-ptn-alz/azurerm` 0.21.0; the extra target-architecture services are documented recommendations, not resources instantiated by that root. No authenticated management-group plan ran.

## Deployable lab

The lab consumes three exact, bootstrap-created `rg-rheinshield-lab-gwc-<suffix>-*` groups and composes five modules: naming, network, monitoring, security, and workload. The mock-plan-validated code uses an internal Container Apps environment, delegated workload subnet, separate private-endpoint subnet, Key Vault and Blob private endpoints/private DNS, public-network disablement, managed identity, Key Vault RBAC, diagnostic settings, Sentinel enablement, expiry tags, and exact-target deletion. Live DNS, routing, telemetry, and runtime behavior remain `READY_NOT_AUTHENTICATED`. Tenant-wide management groups and enforced Conditional Access are excluded.

## Trust boundaries

1. Public demo: deterministic, synthetic, network-independent data.
2. GitHub CI: read-only tests; Azure OIDC is available only to protected manual environments.
3. Azure project scope: short-lived workload identity constrained to the exact three pre-created project resource groups; no subscription-level Contributor role.
4. Private evidence: ignored locally, sanitized before any public export.

See `THREAT_MODEL.md`, `PLATFORM_LANDING_ZONE.md`, `NETWORK_ARCHITECTURE.md`, and `LAB_VS_ENTERPRISE.md`.
