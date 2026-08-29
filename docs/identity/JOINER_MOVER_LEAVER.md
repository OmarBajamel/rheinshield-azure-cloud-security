# Joiner-mover-leaver workflow

The authoritative workflow is `identity/joiner-mover-leaver/workflow.json`. Managers request business roles rather than raw Azure roles. Joiners receive a unique identity, MFA registration and minimum groups. Movers lose incompatible access before gaining new access and trigger separation-of-duties review. Leavers are blocked and sessions revoked within one hour for privileged access or eight hours otherwise; groups, application roles, credentials and ownership are reconciled. Contractors require a sponsor and automatic expiry.

Evidence includes request ID, approver, before/after access, timestamps, exceptions and reviewer. No real HR or account operation is performed in this project.
