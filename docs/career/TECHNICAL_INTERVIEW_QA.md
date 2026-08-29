# Technical interview questions and evidence-backed answers

## Why split enterprise and lab architectures?

A portfolio lab must be disposable and must not imply that one subscription is an enterprise landing zone. The reference shows management hierarchy, subscription vending, central connectivity, policy, and SOC ownership; the lab proves safe Terraform composition only within project groups.

## How does CI authenticate to Azure?

The optional manual workflow uses an Entra federated credential and GitHub OIDC. The trust subject is restricted to repository/branch/environment and the role is scoped to project resource groups. Untrusted pull requests receive no Azure token; no client secret is stored.

## What do the detection results prove?

They prove deterministic rule behavior against a small contract: fourteen malicious fixtures trigger and fourteen benign fixtures remain quiet. They do not measure real detection efficacy, production data quality, recall across attack variants, or analyst outcome.

## How was NIS2 handled?

Official German sources were checked after the December 2025 implementation. Size and turnover support scope analysis, but the online-marketplace category remains conditional because a B2B marketplace alone does not prove the relevant consumer-facing legal definition. The assessment separates facts, assumptions, uncertainty, and legal advice.

## Why no paid Defender or live Sentinel?

Authentication, licensing, and cost are first-class gates. The project documents and validates code/templates offline, labels paid capabilities `READY_LICENSE_REQUIRED` or `SKIPPED_COST_GUARD`, and refuses to fabricate secure scores or screenshots.

## What would you change for production?

Use a dedicated hierarchy/subscriptions, remote encrypted Terraform state, private endpoints and egress governance, tested backup/DR, protected policy remediation identities, production telemetry baselines, detection tuning SLAs, licensed identity governance, and formal legal/control ownership.
