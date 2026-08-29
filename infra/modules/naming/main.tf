locals {
  base               = lower("${var.project}-${var.environment}-${var.location_short}-${var.suffix}")
  global_name_prefix = substr(replace(lower("${var.project}${var.environment}${var.location_short}"), "-", ""), 0, 14)
  names = {
    resource_group_platform = "rg-${local.base}-platform"
    resource_group_network  = "rg-${local.base}-network"
    resource_group_security = "rg-${local.base}-security"
    resource_group_workload = "rg-${local.base}-workload"
    log_analytics           = "law-${local.base}"
    key_vault               = "kv${local.global_name_prefix}${var.suffix}"
    container_environment   = "cae-${local.base}"
    container_app           = "ca-${local.base}-api"
    managed_identity        = "id-${local.base}-workload"
    storage_account         = "st${local.global_name_prefix}${var.suffix}"
  }
}

output "names" { value = local.names }
