# Decisions

## DEC-001 - Two-track Azure design

The multi-subscription Azure Landing Zone is architecture-as-code only. A separate single-subscription lab limits blast radius, lifetime, and cost. This prevents a portfolio exercise from altering unrelated tenant hierarchy.

## DEC-002 - Offline public evidence first

Every dashboard path consumes deterministic, sanitized JSON. Live collectors are optional adapters. This makes CI, Pages, interviews, and fresh-clone verification credential-free and prevents accidental tenant disclosure.

## DEC-003 - Consumption workload

Azure Container Apps consumption is the reference workload runtime because it supports managed identity, revisions, structured container logs, and scale-to-zero. It remains plan-validated when no safe live preflight exists.

## DEC-004 - Cost-sensitive private connectivity

Private endpoints, Firewall, Bastion, DDoS Network Protection, and NAT Gateway remain enterprise recommendations. The lab uses secure public endpoints with network restrictions unless a price preflight proves private connectivity fits within EUR 20.

## DEC-005 - Lean React build

The original Vinext scaffold required a dependency graph that exceeded the host's available disk. The recruiter interface therefore uses React 19 + TypeScript + Vite with the required Sites plugin, retaining static GitHub Pages portability and Cloudflare-compatible ESM output.
