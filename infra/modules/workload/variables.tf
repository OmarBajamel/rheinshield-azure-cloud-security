variable "name_prefix" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "log_analytics_workspace_id" { type = string }
variable "managed_identity_id" { type = string }
variable "key_vault_uri" { type = string }
variable "infrastructure_subnet_id" { type = string }
variable "container_image" {
  type        = string
  description = "Owner-approved OCI image pinned by sha256 digest. No mutable default is permitted."
  validation {
    condition     = can(regex("^[a-z0-9._/-]+/[a-z0-9._/-]+@sha256:[a-f0-9]{64}$", lower(var.container_image)))
    error_message = "container_image must be an owner-approved registry reference pinned with @sha256:<64 lowercase hex>."
  }
}
variable "tags" { type = map(string) }
