# Synthetic secure workload

This FastAPI service demonstrates validated inputs, correlation IDs, structured JSON logs, secure response headers, a single-process lab rate limiter, health/readiness endpoints, and synthetic order operations. It contains no user authentication or real data and is not an intentionally vulnerable target.

The Terraform design attaches a user-assigned identity and grants only `Key Vault Secrets User` at the project vault. The current sample app does not call Key Vault: `KEY_VAULT_URI` exposes a configuration boundary only, so managed-identity authentication remains `READY_NOT_AUTHENTICATED`. Platform/container logs are routed through the Container Apps environment and diagnostic setting; no OpenTelemetry SDK integration is claimed. Public-demo mode runs locally without Azure.
