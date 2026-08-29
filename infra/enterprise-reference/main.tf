# PLAN-ONLY reference. The empty for_each is an intentional mechanical apply
# block: this checked-in root can initialize and validate, but creates nothing.
module "alz" {
  for_each = tomap({})
  source   = "Azure/avm-ptn-alz/azurerm"
  version  = "0.21.0"

  architecture_name  = "alz"
  location           = var.location
  parent_resource_id = var.dedicated_parent_management_group_resource_id
}

output "reference_apply_blocked" {
  description = "Confirms that the checked-in enterprise reference has no module instances."
  value       = length(module.alz) == 0
}
