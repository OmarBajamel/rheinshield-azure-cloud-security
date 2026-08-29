# MITRE ATT&CK coverage

This matrix uses Enterprise ATT&CK technique identifiers as analytical labels.
It describes intended detection coverage, not complete prevention or full ATT&CK
coverage. Mappings are maintained in each rule YAML and checked by the harness.

| Technique | Technique intent | Tactics represented | RheinShield rules | Evidence boundary |
|---|---|---|---|---|
| T1110 / T1110.003 | Brute force / password spraying | Credential Access | RS001, RS002 | Entra failures and success correlation |
| T1078.004 | Cloud account abuse | Initial Access, Privilege Escalation | RS002, RS003, RS004, RS013 | Sign-ins, role events, deployment identity |
| T1098 | Additional cloud account/role access | Persistence, Privilege Escalation | RS004 | Directory role audit events |
| T1098.001 | Additional cloud credentials | Persistence, Privilege Escalation | RS005 | Service-principal/application credentials |
| T1562.007 | Cloud firewall or identity control weakening | Defense Evasion | RS006, RS007, RS009 | Policy, network, and storage control changes |
| T1190 | Exploit public-facing application (exposure precursor) | Initial Access | RS007 | Wildcard inbound rule only; exploitation is not asserted |
| T1562.001 | Impair defenses | Defense Evasion | RS008 | Monitoring and security configuration deletion |
| T1537 | Transfer data to cloud account (exposure precursor) | Exfiltration | RS009 | Public/storage network posture change only |
| T1555 | Credentials from password stores | Credential Access | RS010 | Secret access spike; secret theft is not asserted |
| T1530 | Data from cloud storage | Collection | RS010, RS012 | Vault enumeration and blob reads |
| T1059.001 | PowerShell | Execution | RS011 | Process command-line evidence |
| T1027 | Obfuscated/compressed files and information | Defense Evasion | RS011 | Encoded/obfuscation markers only |
| T1567 | Exfiltration over web service | Exfiltration | RS012 | Mass read precursor; destination is not proven |
| T1588.006 | Obtain capabilities: vulnerabilities (deployment anomaly context) | Resource Development | RS013 | Mapping is secondary; unfamiliar deployment remains the primary signal |
| T1087.004 | Cloud account discovery | Discovery | RS014 | Repeated denied control-plane activity |
| T1069.003 | Cloud role discovery | Discovery | RS014 | Multiple denied operations, not direct proof of enumeration |

## Tactic distribution

| Tactic | Rules |
|---|---|
| Credential Access | RS001, RS002, RS010 |
| Initial Access | RS002, RS003, RS007, RS013 |
| Persistence | RS004, RS005, RS006, RS013 |
| Privilege Escalation | RS004, RS005, RS014 |
| Defense Evasion | RS006, RS007, RS008, RS009, RS011 |
| Execution | RS011 |
| Discovery | RS014 |
| Collection | RS010, RS012 |
| Exfiltration | RS009, RS012 |

Coverage should be reviewed when ATT&CK releases change and when a rule's logic
or evidence boundary changes. A mapping alone is not evidence that a technique
is prevented, nor that all variants of that technique are detected.
