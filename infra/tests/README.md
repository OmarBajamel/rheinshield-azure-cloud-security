# Terraform native tests

Executable tests live below `infra/lab/tests/` so `terraform -chdir=infra/lab test` discovers them. They use mock providers and prove the resource-group prefix and exact project scope without Azure credentials.
