# Backup and recovery

The production recommendation uses service-native backups, Key Vault soft delete/purge protection, versioned deployment artifacts, protected recovery credentials, and periodic restore tests. Commerce and order services target the RTO/RPO in the BIA; telemetry and rebuildable caches use lower-cost recovery.

The public lab deploys no paid backup vault. Recovery is validated through deterministic data regeneration, Terraform rebuild capability, container rebuild, and documented restore sequencing: identity access → network/DNS → data services → workload → monitoring/detections → functional checks. Live restore remains `READY_NOT_AUTHENTICATED`.
