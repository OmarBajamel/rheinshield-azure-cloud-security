variable "location" {
  type        = string
  description = "Azure region allowlisted for the cost-bounded lab."
  default     = "germanywestcentral"
  validation {
    condition     = contains(["germanywestcentral", "westeurope"], var.location)
    error_message = "Lab location must be Germany West Central or West Europe."
  }
}

variable "suffix" {
  type        = string
  description = "Unique lowercase suffix shared by the exact project resource-group names."
  default     = "demo01"
  validation {
    condition     = can(regex("^[a-z0-9]{4,8}$", var.suffix))
    error_message = "Suffix must be 4-8 lowercase alphanumeric characters."
  }
}

variable "expires_at" {
  type        = string
  description = "ISO-8601 expiration timestamp for lab lifecycle enforcement."
  validation {
    condition     = can(formatdate("YYYY-MM-DD'T'hh:mm:ssZ", var.expires_at))
    error_message = "expires_at must be an RFC 3339 timestamp."
  }
}

variable "container_image" {
  type        = string
  description = "Owner-approved OCI image pinned by sha256 digest; supplied only for an authenticated plan/apply."
  validation {
    condition     = can(regex("^[a-z0-9._/-]+/[a-z0-9._/-]+@sha256:[a-f0-9]{64}$", lower(var.container_image)))
    error_message = "container_image must be an owner-approved registry reference pinned with @sha256:<64 lowercase hex>."
  }
}
