# RheinShield Sentinel content as code

This directory contains 14 scheduled analytics-rule YAML/KQL definitions, five
hunting queries, three ARM workbook templates, three Sentinel automation-rule
Bicep templates, three disabled dry-run Logic App playbooks, deterministic
normalized fixtures, a synthetic deployment-principal watchlist, and executable
offline validation.

Capability status: `FIXTURE_VALIDATED`. No Azure deployment or live query is
claimed. Rules and automation are disabled by default. See
`docs/sentinel/DETECTION_TESTING.md` for the validation command and limitations,
and `docs/sentinel/SOAR_SAFETY.md` before promoting any automation.

`tools/detection-test-harness/render_arm.py` converts the analytics-rule YAML
source into a workspace-scoped ARM template using the supported
`Microsoft.SecurityInsights/alertRules@2025-09-01` contract. The generated
template preserves `enabled: false`; connector and target-schema checks remain
mandatory before deployment.
