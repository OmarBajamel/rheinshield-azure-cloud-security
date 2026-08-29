data "azurerm_client_config" "current" {}

module "naming" {
  source = "../modules/naming"
  suffix = var.suffix
}

locals {
  prefix = "rs-lab-gwc-${var.suffix}"
  tags = {
    Project            = "RheinShield"
    Owner              = "OmarBaJamel"
    Environment        = "Lab"
    DataClassification = "Synthetic"
    ManagedBy          = "Codex"
    ExpiresAt          = var.expires_at
  }
}

data "azurerm_resource_group" "network" {
  name = module.naming.names.resource_group_network
  lifecycle {
    postcondition {
      condition     = try(self.tags.Project, "") == "RheinShield" && try(self.tags.Owner, "") == "OmarBaJamel" && try(self.tags.Environment, "") == "Lab" && try(timecmp(self.tags.ExpiresAt, timestamp()) > 0, false)
      error_message = "The pre-created network resource group must carry the exact RheinShield ownership tags and a future ExpiresAt value."
    }
  }
}

data "azurerm_resource_group" "security" {
  name = module.naming.names.resource_group_security
  lifecycle {
    postcondition {
      condition     = try(self.tags.Project, "") == "RheinShield" && try(self.tags.Owner, "") == "OmarBaJamel" && try(self.tags.Environment, "") == "Lab" && try(timecmp(self.tags.ExpiresAt, timestamp()) > 0, false)
      error_message = "The pre-created security resource group must carry the exact RheinShield ownership tags and a future ExpiresAt value."
    }
  }
}

data "azurerm_resource_group" "workload" {
  name = module.naming.names.resource_group_workload
  lifecycle {
    postcondition {
      condition     = try(self.tags.Project, "") == "RheinShield" && try(self.tags.Owner, "") == "OmarBaJamel" && try(self.tags.Environment, "") == "Lab" && try(timecmp(self.tags.ExpiresAt, timestamp()) > 0, false)
      error_message = "The pre-created workload resource group must carry the exact RheinShield ownership tags and a future ExpiresAt value."
    }
  }
}

module "network" {
  source              = "../modules/network"
  name_prefix         = local.prefix
  location            = var.location
  resource_group_name = data.azurerm_resource_group.network.name
  tags                = local.tags
}

module "monitoring" {
  source              = "../modules/monitoring"
  name                = module.naming.names.log_analytics
  location            = var.location
  resource_group_name = data.azurerm_resource_group.security.name
  tags                = local.tags
}

module "security" {
  source                      = "../modules/security"
  name_prefix                 = local.prefix
  key_vault_name              = module.naming.names.key_vault
  storage_name                = module.naming.names.storage_account
  location                    = var.location
  resource_group_name         = data.azurerm_resource_group.security.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  private_endpoint_subnet_id  = module.network.private_endpoint_subnet_id
  workload_virtual_network_id = module.network.workload_virtual_network_id
  log_analytics_workspace_id  = module.monitoring.workspace_id
  tags                        = local.tags
}

module "workload" {
  source                     = "../modules/workload"
  name_prefix                = local.prefix
  location                   = var.location
  resource_group_name        = data.azurerm_resource_group.workload.name
  log_analytics_workspace_id = module.monitoring.workspace_id
  managed_identity_id        = module.security.identity_id
  key_vault_uri              = module.security.key_vault_uri
  infrastructure_subnet_id   = module.network.workload_subnet_id
  container_image            = var.container_image
  tags                       = local.tags
}

output "resource_group_names" {
  description = "Exact pre-created project resource groups consumed by the lab."
  value       = [data.azurerm_resource_group.network.name, data.azurerm_resource_group.security.name, data.azurerm_resource_group.workload.name]
}

output "workload_fqdn" {
  description = "Internal-only Container App revision FQDN."
  value       = module.workload.fqdn
}
