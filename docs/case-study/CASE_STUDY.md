# RheinShield case study

## Context

The fictional RheinCommerce GmbH is a 280-person Düsseldorf marketplace operator migrating a 24/7 commerce platform to Azure. Its critical dependencies—identity, ordering, supplier integration, customer support, and telemetry—create linked availability, confidentiality, and assurance needs.

## Challenge

A cloud platform can be well-designed while its evidence remains fragmented. The engineering objective was to make every public claim traceable from a business process and risk through a control, implementation, validation mode, and privacy-reviewed artifact.

## Approach

RheinShield separates a production reference from a safe lab. Terraform/AVM describe the platform; Entra definitions model least privilege and lifecycle; Sentinel content detects identity and control-plane threats; deterministic fixtures provide repeatable behavior; the incident exercise tests decisions; compliance mappings index evidence without claiming certification.

## Results

The repository contains five validated Terraform modules, fourteen policy controls, fourteen fixture-tested analytics rules, five hunts, three workbooks, six SOAR resources, 738 deterministic events, twenty-seven risks, twenty evidence controls, and an accessible eight-route English/German dashboard. The validation gate found and corrected HCL syntax/provider issues and two accessibility defects before release.

## Boundaries

No authenticated Azure environment was used, no paid security plan was activated, and no tenant-wide identity control was changed. `PLAN_VALIDATED` and `FIXTURE_VALIDATED` are used instead of live claims. RheinCommerce and INC-001 are fictional; the legal assessment is conditional and not advice.
