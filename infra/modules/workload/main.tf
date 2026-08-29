resource "azurerm_container_app_environment" "this" {
  name                           = "cae-${var.name_prefix}"
  location                       = var.location
  resource_group_name            = var.resource_group_name
  log_analytics_workspace_id     = var.log_analytics_workspace_id
  infrastructure_subnet_id       = var.infrastructure_subnet_id
  internal_load_balancer_enabled = true
  tags                           = var.tags
}

resource "azurerm_container_app" "api" {
  name                         = "ca-${var.name_prefix}-api"
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"
  tags                         = var.tags

  identity {
    type         = "UserAssigned"
    identity_ids = [var.managed_identity_id]
  }

  ingress {
    external_enabled = false
    target_port      = 8000
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 1
    container {
      name   = "rheincommerce-api"
      image  = var.container_image
      cpu    = 0.25
      memory = "0.5Gi"
      env {
        name  = "RHEINSHIELD_MODE"
        value = "lab-live"
      }
      env {
        name  = "KEY_VAULT_URI"
        value = var.key_vault_uri
      }
    }
  }
}

resource "azurerm_monitor_diagnostic_setting" "container_environment" {
  name                       = "diag-container-apps"
  target_resource_id         = azurerm_container_app_environment.this.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  enabled_log {
    category = "ContainerAppConsoleLogs"
  }

  enabled_log {
    category = "ContainerAppSystemLogs"
  }
}

output "fqdn" {
  value = azurerm_container_app.api.latest_revision_fqdn
}
