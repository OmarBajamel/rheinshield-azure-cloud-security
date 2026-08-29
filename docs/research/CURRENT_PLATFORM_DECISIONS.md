# RheinShield Current Platform Decisions

Decision date: **2026-08-29**  
Evidence basis: [OFFICIAL_SOURCE_REGISTER.md](./OFFICIAL_SOURCE_REGISTER.md)

These decisions freeze a reproducible baseline for the portfolio release. They distinguish supported implementation choices from preview features and license-dependent live proof.

## 1. Azure Landing Zones implementation path

**Decision:** Use the Azure Landing Zones IaC Accelerator and Azure Verified Modules for Terraform as the enterprise-reference path.

- Model management groups, policy, centralized management, connectivity, and subscription vending with the AVM-based modular architecture.
- Keep the enterprise-reference deployment plan-only unless a dedicated sandbox hierarchy exists; never target the Tenant Root Group.
- Implement the low-cost, single-subscription lab as a separate composition. It can reuse suitable AVM resource modules but must not pretend to be a full enterprise landing zone.
- The portal accelerator is reference material only. It is not the source of truth because it weakens versioning, repeatability, review, and CI evidence.

**Status:** `PLAN_VALIDATED` until Terraform validation exists; live status can change only with deployment evidence.  
**Sources:** ALZ-01, ALZ-02, AVM-01.

## 2. Terraform and AVM version baseline

Use explicit constraints and commit `.terraform.lock.hcl` after initialization and validation.

| Component | Baseline on 2026-08-29 | Required decision |
|---|---:|---|
| ALZ core pattern module | `Azure/avm-ptn-alz/azurerm` `0.21.0` | Pin exact module version. |
| AzAPI provider | `Azure/azapi` `~> 2.12` | Primary Azure control-plane provider for new AVM-style modules. |
| AzureRM provider | `hashicorp/azurerm` `~> 5.3` | Use for project-owned resources only where selected; test the 5.x major explicitly. |
| Microsoft Entra provider | `hashicorp/azuread` `~> 3.9` | Use only in the safe tenant-template track; enforcement remains disabled. |

Additional rules:

- Do not use an unbounded `latest` constraint.
- Dependency/module constraints take precedence over the root preference. A conflict is resolved by selecting a compatible tested version or changing the module, not by bypassing Terraform's solver.
- The AVM authoring specification now requires AzAPI `>= 2.12, < 3.0` as the foundation for new AVM modules and permits AzureRM only for the documented no-AzAPI exception. RheinShield is a solution repository rather than an AVM publisher, but adopts the same direction where practical.
- Provider upgrades after this decision require `terraform init -upgrade`, format/validate/test, a reviewed plan, static security scans, and a refreshed source-register entry.

**Status:** version decision `LIVE_VALIDATED` against official registries; infrastructure behavior remains `PLAN_VALIDATED` until tests pass.  
**Sources:** AVM-01, AVM-02, TF-01, TF-02, TF-03.

## 3. Microsoft Sentinel portal target

**Decision:** Make the Microsoft Defender portal the documented operational experience.

- The Azure portal remains supported at this snapshot, but Microsoft ends Sentinel support there after **2027-03-31** and will redirect customers to the Defender portal.
- Screenshots, runbooks, and navigation instructions should be Defender-portal-first. Azure-portal paths may appear only as transitional notes.
- Onboarding to the Defender portal changes some incident fields, correlation behavior, connector visibility, privacy behavior, and unified RBAC. Queries and automation must be tested against the selected experience rather than assumed equivalent.
- For unified incidents and alerts, prefer Microsoft Graph where Microsoft recommends it; keep the SecurityInsights API for Sentinel resources such as analytics and automation rules.

**Status:** `TRANSITION_REQUIRED` for an existing Azure-portal workspace; documentation itself is current.  
**Sources:** SEN-01 and the transition guidance referenced from it.

## 4. Sentinel content lifecycle and API baseline

**Decision:** Treat Git as the source of truth for RheinShield custom content.

- Native Sentinel Repositories supports analytics rules, automation rules, hunting queries, parsers, playbooks, and workbooks from GitHub or Azure DevOps.
- Author deployable repository-sync artifacts as Bicep or ARM templates. Keep human-reviewable KQL and metadata beside those artifacts and validate deterministic generation when conversion is used.
- Use **SecurityInsights API `2025-09-01`** for GA resources. Do not use a preview API unless the feature is isolated, clearly labeled, and has fixture fallback.
- Avoid the preview custom-detection-rule dependency. RheinShield's required scheduled analytics rules should use GA Sentinel analytics-rule resources.
- Use Content hub for out-of-box Microsoft/partner/community packages, record each item's support model and version, and never edit the upstream package in place. Custom content remains repository-managed.
- A native repository connection requires resource-group Owner plus repository authorization. Until those are proved, report `READY_NOT_AUTHENTICATED`, not deployed.

**Status:** artifact development can be `FIXTURE_VALIDATED` or `PLAN_VALIDATED`; native synchronization is `READY_NOT_AUTHENTICATED` until connected.  
**Sources:** SEN-02, SEN-03, SEN-04.

## 5. Sentinel automation and playbooks

**Decision:** Trigger playbooks through automation rules and implement playbooks as Azure Logic Apps.

- Do not attach playbooks directly to analytics rules; that legacy method was deprecated in March 2026.
- Prefer managed identity authentication for Logic Apps connections when the connector supports it.
- Use Consumption Logic Apps for the temporary cost-controlled lab unless a Standard-only networking requirement is demonstrated. Standard can be selected for private endpoints or single-tenant networking, with its fixed cost recorded before deployment.
- Grant only the documented roles: Sentinel Automation Contributor to the Sentinel service account on the playbook resource group, plus the minimum Logic Apps and Sentinel operator/contributor roles for people or deployment identities.
- Default remediation is dry-run or analyst-approved. Any action that disables identities, isolates systems, or changes access must remain limited to disposable project resources.
- Cap automated test executions and record Logic Apps cost separately from Sentinel ingestion.

**Status:** templates can be `PLAN_VALIDATED` / `FIXTURE_VALIDATED`; executions require live evidence.  
**Sources:** SEN-01, SEN-05.

## 6. GitHub Actions to Azure authentication

**Decision:** Use OIDC workload identity federation only; no client secret or publish profile.

Required controls:

- Pin Azure Login v3.0.2 to commit `7ddb5af1ef8758cf1353cf3b42f940aee27ba21c`.
- Set job-scoped `permissions: { id-token: write, contents: read }`; add no unrelated write permission.
- Use audience `api://AzureADTokenExchange` for Azure public cloud.
- Store client, tenant, and subscription identifiers as protected GitHub environment variables or secrets so they are masked in logs, even though they are not authentication secrets.
- Scope the Entra federated credential to the protected deployment environment or exact ref and the one repository.
- Because the public repository will be created after **2026-07-15**, configure the Entra subject in GitHub's immutable form: `repo:OWNER@OWNER-ID/REPO@REPO-ID:<context>`. Resolve the actual numeric IDs after repository creation; never guess or use only the legacy name-based subject.
- Use protected GitHub environments for apply/deploy jobs, keep pull-request jobs read-only, restrict Azure RBAC to project resource groups, and remove the credential after the temporary lab proof if no ongoing deployment is needed.
- Set `AZURE_CORE_OUTPUT=none` by default and request narrow command output explicitly to reduce accidental identifier leakage.

**Status:** workflow code can be `PLAN_VALIDATED`; Azure login is `READY_NOT_AUTHENTICATED` until the federated credential and RBAC assignment are verified.  
**Sources:** GHA-01, GHA-02, GHA-03.

## 7. Defender for Cloud and regulatory-compliance behavior

**Decision:** Use Foundational CSPM as the no-cost default; do not silently activate paid plans.

- Foundational CSPM supplies continuous assessments, recommendations, Secure Score, and MCSB without a paid Defender CSPM plan.
- The paid Defender CSPM plan adds advanced posture capabilities such as regulatory compliance, attack paths, cloud security explorer, governance, and agentless scanning. Workload protection plans are separate.
- Adding non-default standards in the regulatory-compliance dashboard requires at least one paid Defender plan. Therefore a live NIS2/ISO dashboard view is `READY_LICENSE_REQUIRED` unless the current subscription proves an eligible plan.
- Defender dashboard results are assessment signals. They are not a certification and cannot prove NIS2 or ISO 27001 compliance.
- Do not start a paid plan or rely on a trial without the cost gate. A trial can roll into charges.
- Microsoft has announced that Foundational CSPM becomes opt-in for new Azure subscriptions on **2026-10-27**. Make enablement/checking explicit in future lab logic instead of assuming it is on by default.

**Status:** Foundational CSPM may be `LIVE_VALIDATED` when observed; advanced CSPM and non-default standards default to `READY_LICENSE_REQUIRED` or `SKIPPED_COST_GUARD`.  
**Sources:** DFC-01, DFC-02.

## 8. Microsoft Cloud Security Benchmark baseline

**Decision:** Use MCSB v1 as the normative stable release baseline. Maintain a non-normative v2 preview crosswalk.

Rationale:

- Microsoft describes MCSB v2 as superseding v1 but still labels v2 **Preview**.
- Microsoft also states that v2 baselines are not yet available, while v1 baseline material remains available.
- A public portfolio claiming stable control coverage should not silently make preview identifiers its audit baseline.

Implementation:

- Policy/control evidence uses MCSB v1 identifiers.
- A separate appendix may map to v2 preview controls and ISO 27001:2022 mappings, labeled `PREVIEW_REFERENCE_ONLY` with a verification date.
- Re-baseline only after Microsoft declares v2 GA and publishes the needed service baselines/migration guidance.

**Status:** v1 `STABLE_BASELINE`; v2 `PREVIEW_REFERENCE_ONLY`.  
**Sources:** MCSB-01, MCSB-02.

## 9. Microsoft Entra capability and licensing matrix

Tenant-wide controls remain report-only or template-only unless a dedicated tenant, the required licenses, break-glass exclusions, and a safe rollout scope are proven.

| Capability | Minimum decision baseline | RheinShield live default | Status when license is not proved |
|---|---|---|---|
| Security defaults | Entra Free | Document only; do not modify the user's tenant defaults | `READY_NOT_AUTHENTICATED` |
| Conditional Access | Entra ID P1 (also included in some Microsoft 365 plans) | Report-only template; never enforce against existing users | `READY_LICENSE_REQUIRED` |
| Sign-in/user risk policies and full Identity Protection | Entra ID P2 / Entra Suite | Template and synthetic evidence only | `READY_LICENSE_REQUIRED` |
| PIM for Entra/Azure roles | Entra ID P2 or Entra ID Governance | Design and configuration template; no privilege assignment to real users | `READY_LICENSE_REQUIRED` |
| Basic access-review capabilities retained from P2 | Entra ID P2 or ID Governance, depending on exact capability | Template and fixture evidence | `READY_LICENSE_REQUIRED` |
| New/advanced access reviews, lifecycle workflows, advanced entitlement management | Entra ID Governance / Entra Suite | Architecture and workflow artifacts only | `READY_LICENSE_REQUIRED` |
| Guest governance | ID Governance plus the guest MAU billing model where applicable | Out of live-lab scope | `READY_LICENSE_REQUIRED` |
| Built-in Entra roles | Free | Use only least-privilege existing roles; no new privileged assignment to real users | capability can be free, but authorization still required |
| Custom Entra roles | Entra ID P1 for assigned users | Not required for the default lab | `READY_LICENSE_REQUIRED` |

License counts must cover the users in scope as described by Microsoft, including eligible assignees, approvers, reviewers, or reviewed users where applicable. Tenant possession of a SKU must be verified rather than inferred from portal visibility.

**Sources:** ENT-01, ENT-02.

## 10. Release-status rules driven by these decisions

- A valid Terraform plan with mock/fixture tests is `PLAN_VALIDATED`, not `LIVE_DEPLOYED`.
- Content parsed and exercised against deterministic synthetic telemetry is `FIXTURE_VALIDATED`, not live Sentinel proof.
- Missing Azure/GitHub authentication is `READY_NOT_AUTHENTICATED`.
- Missing Entra/Defender entitlement is `READY_LICENSE_REQUIRED`.
- A paid capability rejected by the EUR 20 project cost guard is `SKIPPED_COST_GUARD`.
- Preview content must retain an explicit Preview label in code, evidence, dashboard, and documentation.
- Product dashboards and framework mappings are evidence inputs, not compliance or certification claims.

## 11. Recheck triggers

Refresh this decision record before a release or live deployment when any of the following occurs:

1. MCSB v2 becomes GA or v2 service baselines are published.
2. The date reaches 2026-10-27 and a new subscription is used for Foundational CSPM.
3. A Sentinel workflow still points to the Azure portal near the 2027-03-31 retirement.
4. Terraform lock-file upgrades introduce a new major provider version or a new ALZ module minor version.
5. GitHub repository ownership, name, transfer state, deployment environment, or OIDC subject customization changes.
6. The tenant's Entra or Defender subscriptions change.
7. Sentinel repository synchronization needs a preview-only content type or API.
