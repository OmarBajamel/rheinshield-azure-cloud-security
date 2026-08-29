# LinkedIn post — English

How do you connect Azure architecture, cloud governance, detection engineering, and German compliance expectations without producing four disconnected documents?

I built **RheinShield** as an end-to-end answer.

It is a public, bilingual portfolio platform for the fictional RheinCommerce GmbH: an Azure Landing Zone reference plus a cost-gated single-subscription lab, built with Terraform and Azure Verified Modules. The design covers Entra ID, Zero Trust, managed identity, private endpoints, Key Vault, Azure Policy, and secretless GitHub Actions OIDC.

For the SOC layer, I created 14 Microsoft Sentinel KQL analytics rules, five hunts, three workbooks, three automation rules, and three disabled dry-run playbooks. A fixed-seed generator produces 738 synthetic events and the complete INC-001 identity incident. All 14 malicious fixtures triggered; all 14 benign fixtures stayed quiet. That is reproducible fixture evidence—not production efficacy.

The assurance layer connects 27 risks and 20 controls to NIS2/BSIG, ISO/IEC 27001:2022, BSI IT-Grundschutz, and MCSB. Applicability remains conditional; no certification or legal-compliance claim is made.

The main lesson: credible cloud security depends on scope, provenance, and honest validation status as much as configuration. The repository records the Terraform, browser, accessibility, and privacy gates, while the public dashboard exposes only synthetic data.

RheinShield supports my applications for Azure Cloud Security, Sentinel/SOC, IAM, DevSecOps, and technical security consulting roles in Germany.

#Azure #CloudSecurity #MicrosoftSentinel #Terraform #CyberSecurity
