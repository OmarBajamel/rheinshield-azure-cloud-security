# Network architecture

The enterprise reference uses hub-and-spoke segmentation: ingress, application, data, management, and private endpoint subnets have separate trust boundaries. Azure Firewall, DDoS Network Protection, Bastion, and NAT Gateway are reference options only because they exceed the portfolio cost profile.

The lab code uses a delegated `/23` Container Apps infrastructure subnet and a separate `/24` private-endpoint subnet. The Container Apps environment has an internal load balancer; Key Vault and Blob endpoints attach to dedicated private DNS zones linked to the workload VNet; both data services disable public network access. Network security groups deny Internet-originated SSH/RDP, while the policy model audits or denies public IP and broad management ingress. Live egress, name resolution, endpoint approval, and routing remain `READY_NOT_AUTHENTICATED`.

Terraform defines Key Vault, Storage metric, and Container Apps environment diagnostic settings targeting the central workspace. Category availability and ingestion remain unverified until an authenticated plan/apply. NSG flow logs and advanced traffic analytics are cost-dependent and remain `SKIPPED_COST_GUARD` in public-demo mode.
