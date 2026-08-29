# Offline detection testing

`tools/detection-test-harness/validate.py` is the executable validation entry
point. It loads every analytics-rule YAML file, validates required metadata and
basic KQL invariants, loads the referenced JSON fixture, and evaluates the rule's
threshold semantics against compact normalized baseline and malicious observations.

The fixture contract uses seed `20260829`, classification `Synthetic`, and case
identifier `INC-001`. Every rule receives one benign and one intentionally
anomalous observation. Normalization is explicit in each fixture—for example a
ten-minute IP bucket, an account/source correlation window, or a deployment
event joined to an approved-principal watchlist. This keeps tests deterministic
and independent of Azure credentials while exercising the security decision,
not merely searching the KQL text for a keyword.

The same harness validates:

- exactly 14 stable, unique analytics rules and their entity/MITRE metadata;
- at least five non-placeholder hunting queries;
- three JSON ARM workbook envelopes and their embedded `Notebook/1.0` JSON;
- three disabled-by-default automation-rule Bicep templates;
- three disabled, connector-free, dry-run-only Logic App Bicep templates; and
- one synthetic watchlist CSV and supported-API Bicep loader for RS013; and
- the required detection, tuning, triage, SOAR, testing, and API decision docs.

Run:

```powershell
python -m pip install -r tools/detection-test-harness/requirements.txt
python tools/detection-test-harness/validate.py --write-results
python -m unittest discover -s tools/detection-test-harness -p "test_*.py" -v
```

`--write-results` writes `artifacts/evidence/detection-test-results.json` and the
fixture manifest only after all checks pass. The evidence records its timestamp,
harness path, per-rule results, fixture hashes, and explicit limitations.

## Interpretation limits

The harness does not parse full KQL grammar, connect to Azure, execute a Sentinel
scheduled rule, test ingestion latency, or establish production precision/recall.
The metrics apply only to committed fixtures. Bicep validation here is structural;
`az bicep build` or a Bicep CLI build remains a separate deployment gate when
that tool is available. Accordingly the capability status is
`FIXTURE_VALIDATED`, never `LIVE_VALIDATED`.

For production promotion, replay every query against a non-production workspace,
verify table schemas and entity output, exercise incident grouping, compile all
Bicep files with the current CLI, and observe a controlled synthetic event end to end.
