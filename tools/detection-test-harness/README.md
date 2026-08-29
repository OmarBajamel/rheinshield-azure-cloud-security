# Detection test harness

This harness validates all RheinShield analytics-rule metadata and KQL surfaces,
then executes each rule's threshold logic against deterministic normalized
baseline and malicious fixtures. It also validates the workbook JSON envelopes,
embedded workbook JSON, hunting queries, automation templates, playbook safety
invariants, and required operational documentation.

Run from the repository root:

```powershell
python -m pip install -r tools/detection-test-harness/requirements.txt
python tools/detection-test-harness/validate.py --write-results
python tools/detection-test-harness/render_arm.py --output artifacts/generated/sentinel-analytics-rules.json
python -m unittest discover -s tools/detection-test-harness -p "test_*.py" -v
```

The evaluator does not run KQL against Azure. A passing result means
`FIXTURE_VALIDATED`, not `LIVE_VALIDATED`; the reported precision and recall
apply only to the committed compact fixtures and are not production efficacy
metrics. The evidence JSON is written only after every validation succeeds.
The ARM renderer converts the reviewed YAML source of truth into a deployable,
disabled-by-default template; generated output is intentionally not the source.
