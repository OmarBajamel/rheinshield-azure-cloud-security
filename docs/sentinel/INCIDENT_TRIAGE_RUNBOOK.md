# Microsoft Sentinel incident triage runbook

This runbook is for the fictional RheinCommerce GmbH portfolio scenario. It uses
synthetic data unless a separately controlled lab is explicitly marked live.
Default containment is advisory and dry-run; never disable a real identity or
change a real resource solely because a playbook proposed an action.

## 1. Intake and safety

1. Record incident ID, creation time, analytics-rule ID, severity, workspace,
   evidence status, and analyst. Confirm whether the data is synthetic or live.
2. Check connector freshness and query ingestion delay. If a required table is
   stale, label the incident `data-quality` and avoid negative conclusions.
3. Validate scope: tenant, subscription, resource group, environment, identities,
   and data classification. Stop if the target is outside the authorized project.
4. Preserve the original alert, query time window, correlation IDs, and entity
   values. Store any raw live export only in the ignored private-evidence path.

## 2. Technical validation

1. Open the source rule in `sentinel/analytics-rules/` and confirm its query,
   threshold, lookback, false positives, and schema assumptions.
2. Rerun the KQL with a narrow immutable time range; do not silently change the
   query. Compare raw rows with summarized output and note ingestion latency.
3. Enrich accounts with role, MFA, device, sign-in, PIM, and recent audit context.
   Enrich IPs with approved corporate/VPN ranges; do not treat geolocation as proof.
4. Enrich Azure resources with owner, deployment history, IaC baseline, policy
   state, diagnostic coverage, criticality, and expiration tag.
5. Build a UTC timeline. Correlate RS001–RS006 as an identity chain and
   RS007–RS014 as control-change, execution, discovery, and collection evidence.

## 3. Classification and decision

Classify only after documenting evidence for and against the hypothesis:

- `TruePositive`: evidence supports unauthorized or malicious activity.
- `BenignPositive`: logic is correct but activity is approved/expected.
- `FalsePositive`: evidence shows the rule logic or source data is inaccurate.
- `Undetermined`: evidence is insufficient; preserve the reason and next action.

Severity considers identity privilege, environment, asset criticality, data
classification, exposure, persistence, blast radius, and confidence. A High
rule does not force a High incident when the event is proven benign, and a
Medium rule can become High when several corroborating signals exist.

## 4. Containment and recovery

1. Run the relevant playbook only in dry-run mode and attach its proposed plan.
2. Obtain the designated identity, cloud, or data owner's authorization for a
   real containment action. Use the narrowest reversible step first.
3. For identity cases, consider session revocation, credential rotation, role
   removal, and Conditional Access restoration through approved procedures.
4. For cloud changes, compare IaC, prepare a reviewed rollback, restore logging,
   and restrict public/network access without deleting evidence.
5. For suspected data access, restrict the scoped identity or token, preserve
   storage/vault logs, and determine object and classification scope.
6. Validate recovery with fresh telemetry and a control-plane read. Record every
   command, approver, time, and observed result.

## 5. Closure and lessons learned

Close only when evidence is preserved, containment/recovery is verified, owners
are informed through the authorized channel, and follow-up actions have owners
and deadlines. Update the tuning register and add a regression fixture for any
logic defect. Link the incident to risk/control evidence, but do not claim that
an alert or closed ticket establishes legal compliance.

Escalate immediately when a privileged identity, production public exposure,
monitoring deletion, secret access, or material data access cannot be bounded.
Use the organization's legal and regulatory reporting process; this portfolio
runbook does not determine statutory notification obligations.
