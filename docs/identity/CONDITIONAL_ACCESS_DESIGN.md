# Conditional Access design

Six vendor-neutral design records live at `identity/conditional-access/policies.json`. They are not Microsoft Graph import payloads and require an authenticated schema-aware converter plus validation before deployment. Every record is disabled in source. A safe lab deployment may translate them to `enabledForReportingButNotEnforced`, only for dedicated lab groups/service principals, and only after the What If tool, emergency-access exclusions, licensing, and impact evidence are reviewed.

CA-001 protects administrators with phishing-resistant authentication; CA-002 blocks legacy clients; CA-003 applies privileged device/session constraints; CA-004 covers risky users/sign-ins (P2); CA-005 covers workload-identity risk (premium); CA-006 limits unmanaged-device sessions. The design records and tenant behavior are `READY_LICENSE_REQUIRED`; no Graph-schema or live enforcement claim is made.
