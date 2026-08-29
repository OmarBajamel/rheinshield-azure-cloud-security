variable "name_prefix" { type = string }
variable "key_vault_name" { type = string }
variable "storage_name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "tenant_id" {
  type      = string
  sensitive = true
}
variable "private_endpoint_subnet_id" { type = string }
variable "workload_virtual_network_id" { type = string }
variable "log_analytics_workspace_id" { type = string }
variable "tags" { type = map(string) }
