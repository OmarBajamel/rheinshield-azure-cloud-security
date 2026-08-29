# Synthetic telemetry

`tools/synthetic-telemetry/generate.py` creates 90 days of deterministic activity with fixed seed `20260829`, eight normal events per day, and an 18-event INC-001 window. User, resource, IP/location, product, and identity values are fictional aliases. Dangerous activity is represented only as data: the generator never authenticates, sprays passwords, executes PowerShell, changes a control, or downloads objects.

The full JSONL stream supports timeline and evidence demonstrations. Each analytics rule also has a compact, table-independent fixture used by the offline evaluator. Those fixture results measure implementation correctness against designed cases, not real-world precision or production efficacy. The manifest records event counts, time span, classification, output path, and SHA-256.
