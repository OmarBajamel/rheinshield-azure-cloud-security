resource "azurerm_virtual_network" "hub" {
  name                = "vnet-${var.name_prefix}-hub"
  address_space       = ["10.20.0.0/20"]
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_virtual_network" "workload" {
  name                = "vnet-${var.name_prefix}-workload"
  address_space       = ["10.21.0.0/20"]
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_network_security_group" "workload" {
  name                = "nsg-${var.name_prefix}-workload"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags

  security_rule {
    name                       = "Deny-Internet-Administrative-Ports"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["22", "3389"]
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet" "workload" {
  name                 = "snet-workload"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.workload.name
  address_prefixes     = ["10.21.0.0/23"]

  delegation {
    name = "container-apps-environment"
    service_delegation {
      name    = "Microsoft.App/environments"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    }
  }
}

resource "azurerm_subnet" "private_endpoints" {
  name                              = "snet-private-endpoints"
  resource_group_name               = var.resource_group_name
  virtual_network_name              = azurerm_virtual_network.workload.name
  address_prefixes                  = ["10.21.4.0/24"]
  private_endpoint_network_policies = "Disabled"
}

resource "azurerm_subnet_network_security_group_association" "workload" {
  subnet_id                 = azurerm_subnet.workload.id
  network_security_group_id = azurerm_network_security_group.workload.id
}

resource "azurerm_virtual_network_peering" "hub_to_workload" {
  name                      = "peer-hub-to-workload"
  resource_group_name       = var.resource_group_name
  virtual_network_name      = azurerm_virtual_network.hub.name
  remote_virtual_network_id = azurerm_virtual_network.workload.id
}

resource "azurerm_virtual_network_peering" "workload_to_hub" {
  name                      = "peer-workload-to-hub"
  resource_group_name       = var.resource_group_name
  virtual_network_name      = azurerm_virtual_network.workload.name
  remote_virtual_network_id = azurerm_virtual_network.hub.id
}

output "workload_subnet_id" { value = azurerm_subnet.workload.id }
output "private_endpoint_subnet_id" { value = azurerm_subnet.private_endpoints.id }
output "workload_virtual_network_id" { value = azurerm_virtual_network.workload.id }
output "virtual_network_ids" { value = [azurerm_virtual_network.hub.id, azurerm_virtual_network.workload.id] }
