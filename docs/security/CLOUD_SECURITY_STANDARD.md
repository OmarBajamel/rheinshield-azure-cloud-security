# Cloud security standard

All Azure workloads use approved regions, mandatory owner/classification/expiry tags, managed identities, minimum TLS, private access where feasible, central diagnostics, and least-privilege RBAC. Production and lab enforcement levels differ as recorded in `infra/policies/controls.json`. Public administrative ingress is prohibited. Evidence: Terraform modules, policy summary, and capability matrix.
