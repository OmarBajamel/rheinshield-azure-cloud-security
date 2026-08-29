# Sanitization standard

Public evidence must contain no tenant or subscription identifier, user principal name, account email, external IP address, access token, client secret, signed URL, private resource name, or unrelated resource. `tools/sanitization/sanitize.py` removes direct identifiers and emits rule counts plus a hash. `scan_public.py` scans the repository before release.

Sanitization preserves timestamps, severity, status, counts, control IDs, synthetic entity aliases, and other audit meaning. Images require human visual review and metadata removal. Any ambiguity is resolved by excluding the field or asset. Output is classified Public/Synthetic and traced in the evidence manifest.
