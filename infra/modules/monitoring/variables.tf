variable "name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "tags" { type = map(string) }

variable "retention_days" {
  type    = number
  default = 30
  validation {
    condition     = var.retention_days >= 30 && var.retention_days <= 730
    error_message = "Retention must be 30-730 days."
  }
}
