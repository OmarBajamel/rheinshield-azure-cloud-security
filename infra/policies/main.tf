terraform {
  required_version = ">= 1.16.0, < 2.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 5.3"
    }
  }
}

variable "resource_group_id" {
  type        = string
  description = "Dedicated RheinShield lab resource-group scope."
  validation {
    condition     = can(regex("^/subscriptions/[0-9a-f-]{36}/resourcegroups/rg-rheinshield-lab-gwc-[a-z0-9]{4,8}-(network|security|workload)$", lower(var.resource_group_id)))
    error_message = "Policy scope must be one exact RheinShield lab resource-group ID."
  }
}

variable "initiative_effect" {
  type    = string
  default = "Audit"
  validation {
    condition     = contains(["Audit", "Deny", "Disabled"], var.initiative_effect)
    error_message = "Use Audit, Deny, or Disabled."
  }
}

locals {
  baseline = jsondecode(file("${path.module}/controls.json"))
}

resource "azurerm_policy_definition" "baseline" {
  for_each     = local.baseline.controls
  name         = "rheinshield-${lower(each.value.name)}"
  policy_type  = "Custom"
  mode         = each.value.mode
  display_name = each.value.displayName
  description  = "${each.key}; mapped to ${join(", ", each.value.frameworks)}. Lab default is Audit."
  policy_rule  = jsonencode(each.value.policyRule)
  parameters   = jsonencode(each.value.parameters)
  metadata     = jsonencode({ category = "RheinShield", version = local.baseline.version, controlId = each.key })
}

resource "azurerm_policy_set_definition" "baseline" {
  name         = "rheinshield-security-baseline"
  policy_type  = "Custom"
  display_name = local.baseline.initiative
  description  = "Versioned security baseline for the dedicated RheinShield project scope."
  metadata     = jsonencode({ category = "RheinShield", version = local.baseline.version })
  dynamic "policy_definition_reference" {
    for_each = azurerm_policy_definition.baseline
    content {
      policy_definition_id = policy_definition_reference.value.id
      reference_id         = policy_definition_reference.key
      parameter_values     = length(local.baseline.controls[policy_definition_reference.key].parameters) > 0 ? jsonencode({ effect = { value = var.initiative_effect } }) : null
    }
  }
}

resource "azurerm_resource_group_policy_assignment" "baseline" {
  name                 = "rheinshield-security-baseline"
  resource_group_id    = var.resource_group_id
  policy_definition_id = azurerm_policy_set_definition.baseline.id
  display_name         = "RheinShield Security Baseline"
  enforce              = false
}
