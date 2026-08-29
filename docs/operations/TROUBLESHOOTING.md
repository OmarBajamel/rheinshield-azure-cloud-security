# Troubleshooting

| Symptom | Check | Safe response |
|---|---|---|
| Dashboard blank | Node version and `npm run build` | Reinstall from lock file; inspect console |
| Fixture mismatch | Generator seed and fixture manifest | Regenerate public data; do not relax expectations |
| Azure preflight fails | Authentication, subscription, prefix collision | Stop mutation; keep `READY_NOT_AUTHENTICATED` |
| Policy blocks teardown | Lab effect and lock state | Remove only project-scoped lock/assignment, then retry |
| Sentinel API error | API decision register and Bicep build | Update template and revalidate offline first |
| Release scan fails | Exact finding path | Sanitize or remove the asset; never suppress a real secret |
