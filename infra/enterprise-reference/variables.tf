variable "location" {
  type    = string
  default = "germanywestcentral"
}

variable "dedicated_parent_management_group_resource_id" {
  type        = string
  description = "Resource ID of an explicitly dedicated RheinShield sandbox parent. Never use Tenant Root Group or an unrelated management group."
  validation {
    condition     = can(regex("^/providers/microsoft.management/managementgroups/rheinshield-[a-z0-9-]+$", lower(var.dedicated_parent_management_group_resource_id)))
    error_message = "An explicitly dedicated management-group ID named rheinshield-* is required; Tenant Root Group and unrelated groups are forbidden."
  }
}
