---
name: portfolio-evidence-release
description: Prepare a public RheinShield evidence or release package with deterministic generation, privacy scanning, provenance, and claim verification.
---

# RheinShield public evidence release

Read `docs/evidence/SANITIZATION_STANDARD.md` before packaging. Generate from tracked public-demo inputs; never copy from ignored private-evidence paths.

Run the sanitizer and release checks, inspect the dashboard bundle, screenshots, PDFs, and archives for tenant IDs, subscription IDs, user principal names, email addresses, external IPs, tokens, signatures, or query strings. Record SHA-256, source, validation mode, timestamp, and privacy result in the evidence manifest. Reject placeholder URLs and unsupported claims. Only `LIVE_DEPLOYED` or `LIVE_VALIDATED` may describe real cloud state.
