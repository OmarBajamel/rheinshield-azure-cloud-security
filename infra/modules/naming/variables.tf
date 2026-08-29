variable "project" {
  type    = string
  default = "rheinshield"
}

variable "environment" {
  type    = string
  default = "lab"
}

variable "location_short" {
  type    = string
  default = "gwc"
}

variable "suffix" {
  type        = string
  description = "Deterministic non-secret resource suffix."
}
