# RBAC matrix

The machine source is `identity/rbac/role-matrix.json`. Human access is group-based; direct assignments are exceptional. Routine deployment rights stop at the dedicated `rg-rheinshield-*` resource groups. Role-assignment creation and federation bootstrap are separate, time-bound operator tasks.

| Persona | Routine permission | Elevated permission | Separation rule |
|---|---|---|---|
| Platform admin | Reader | project-scope Contributor | cannot approve own activation |
| Security admin | Security Reader | Security Admin | cannot modify workload code |
| SOC Tier 1 | Sentinel Reader | none | cannot contain or close |
| SOC Tier 2 | Sentinel Responder | approved playbook operator | no Azure Owner |
| Developer | workload Reader | constrained deployment via CI | cannot read secrets |
| Auditor | time-bound Reader | none | read-only evidence |
| GitHub deployment | none interactively | Contributor on three exact pre-created RGs; Key Vault Data Access Administrator on security RG | immutable repo/environment subject; no RG creation |
| Workload identity | no interactive login | Key Vault Secrets User at one vault | no control-plane contributor |
