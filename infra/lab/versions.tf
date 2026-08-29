terraform {
  required_version = ">= 1.16.0, < 2.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 5.3"
    }
  }
}

provider "azurerm" {
  features {}
  resource_provider_registrations = "none"
}
