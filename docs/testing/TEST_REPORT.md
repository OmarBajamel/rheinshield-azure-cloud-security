# Test report

Release candidate: **v1.0.0**  
Verification date: **2026-08-29**  
Default mode: **public-demo** with deterministic synthetic data

## Results

| Area | Result | Evidence boundary |
|---|---|---|
| Terraform | Format check passed; lab, enterprise-reference and policy roots initialized and validated; lab native mock test 1/1 passed | Lab is `PLAN_VALIDATED`; enterprise and policy roots remain `READY_NOT_AUTHENTICATED`; enterprise apply is mechanically blocked |
| TFLint / IaC security | 0 TFLint issues; 14/14 custom IaC checks passed | Static and repository-local analysis |
| Bicep | 7/7 Sentinel templates compiled with Bicep 0.46.1 | Compilation only; no Azure deployment |
| Python | 10/10 pytest tests passed; Ruff passed; strict MyPy passed on 10 release-critical files | One dependency deprecation warning is recorded and non-failing |
| Sentinel | 14 malicious fixtures triggered; 14 benign fixtures stayed quiet; 5 hunts, 3 workbooks, 3 automation rules, 3 playbooks, and 1 watchlist validated | Python fixture evaluator is not service-side KQL execution or production efficacy proof |
| Dashboard unit/build | 4/4 unit tests passed; TypeScript and ESLint passed; Vite production build succeeded | Public static application; no private endpoint calls |
| Browser | 16/16 route-language views passed, language switch passed, mobile navigation passed, no overflow in the tested 390 px view, and 0 console errors | Chrome/Playwright test against the production build |
| Accessibility | 0 axe A/AA violations across 3 representative route/language scans | Not a full manual WCAG audit and not all 16 views were axe-scanned |
| Lighthouse | 100 Performance, 100 Accessibility, 100 Best Practices, 100 SEO | Local production build in Chrome |
| Dependencies | npm production audit: 0 known vulnerabilities; pip-audit: 0 known vulnerabilities | Locked direct/transitive dependency set at the verification timestamp |
| Privacy | Exact source candidate and exact `dist/` scanners passed; 8 screenshots passed visual privacy review | Pattern and metadata scanning supplements, but cannot replace, human review |

## Known non-failing warning

The FastAPI test client emitted one upstream Starlette deprecation warning about the current `httpx` integration. Tests pass, no shipped vulnerability is associated with the warning, and the dependency is monitored rather than suppressed.

## Reproduction

Run `npm ci`, install `.[dev]`, then execute `npm run release:check`, `python -m pytest -q`, `python tools/detection-test-harness/validate.py`, and the Terraform/Bicep checks described in the root README. The GitHub CI workflow performs the same release-critical gates on a clean runner.
