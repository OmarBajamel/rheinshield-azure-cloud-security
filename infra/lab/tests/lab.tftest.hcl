mock_provider "azurerm" {
  mock_data "azurerm_client_config" {
    defaults = {
      tenant_id = "00000000-0000-4000-8000-000000000000"
    }
  }
  mock_data "azurerm_resource_group" {
    defaults = {
      tags = {
        Project     = "RheinShield"
        Owner       = "OmarBaJamel"
        Environment = "Lab"
        ExpiresAt   = "2999-12-31T23:59:59Z"
      }
    }
  }
}

run "lab_plan_uses_safe_scope" {
  command = plan
  variables {
    expires_at      = "2026-08-31T18:00:00Z"
    container_image = "ghcr.io/omarbajamel/rheinshield-secure-workload@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  }
  assert {
    condition     = alltrue([for name in output.resource_group_names : startswith(name, "rg-rheinshield-")])
    error_message = "Every lab resource group must use the project prefix."
  }
  assert {
    condition     = length(output.resource_group_names) == 3
    error_message = "The lab consumes exactly three pre-created scoped resource groups."
  }
}
