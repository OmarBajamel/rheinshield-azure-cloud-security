# German NIS-2, BSIG and BSI IT-Grundschutz source notes

Research snapshot: **2026-08-29 (Europe/Berlin)**  
Scope: German NIS-2 implementation status, enacted BSIG terminology, the RheinCommerce GmbH scenario, and the current BSI IT-Grundschutz Compendium.  
Status: **research baseline**. This document is an educational portfolio aid, not legal advice and not a compliance opinion.

## Executive conclusions

1. Germany's NIS-2 implementation is no longer a draft. The NIS-2 implementation act was published as **BGBl. 2025 I Nr. 301** and the amended/new-form BSI Act took effect on **2025-12-06**. BSI guidance retrieved for this review describes the duties as applicable from that date.
2. Use the enacted German terms **besonders wichtige Einrichtung** (bwE) and **wichtige Einrichtung** (wE). Do not label an entity a German-law *wesentliche Einrichtung*; that is EU-directive language, not the category name used by § 28 BSIG.
3. A provider of an online marketplace is in **Anlage 2**, so a qualifying provider is a **wichtige Einrichtung**, not automatically a bwE. A separate Anlage-1 activity, KRITIS status, or another special rule could change the result.
4. The fictional facts do not yet prove that RheinCommerce is an “Online-Marktplatz”. Section 2 no. 28 BSIG cross-refers to § 312l BGB; reading § 312l(2)–(3) shows a consumer-facing service/operator concept. The brief currently says **B2B marketplace**. If it is strictly B2B, the online-marketplace route is not established.
5. The official BSI compendium page still identifies **IT-Grundschutz-Kompendium, Edition 2023** as the current German edition. No later edition was listed on the official page at retrieval time.

## 1. German implementation status and terminology

| Topic | Verified fact | Portfolio decision | Confidence |
|---|---|---|---|
| Enactment | The NIS-2 implementation act is recorded in BGBl. 2025 I Nr. 301; BSI says it took effect on 2025-12-06. | Treat NIS-2/BSIG obligations as enacted law, not a bill or expected future requirement. | High |
| Statute name | The current official heading is *Gesetz über das Bundesamt für Sicherheit in der Informationstechnik und über die Sicherheit in der Informationstechnik von Einrichtungen (BSI-Gesetz – BSIG)*. | Use “BSIG” after the full title on first mention. | High |
| Regulated categories | § 28 BSIG uses *besonders wichtige Einrichtungen* and *wichtige Einrichtungen*. | Use bwE/wE in German material; explain the relation to EU “essential/important entities” once. | High |
| Self-assessment | BSI states that organizations must determine for themselves whether they are in scope. | Present the RheinCommerce result as a reasoned scenario assessment, never as an authority determination. | High |
| Registration channel | BSI uses a two-step setup beginning with *Mein Unternehmenskonto* and then the BSI Portal. The BSI announced the second portal step as available on 2026-06-01. | A runbook should point to the current BSI Portal workflow and avoid the obsolete claim that a future portal is pending. | High |
| Portal timing | § 33(1) BSIG requires registration no later than three months after an organization first or again meets the definition; changes are due within two weeks under § 33(5). | Model ownership, a three-month control, and a two-week change-update control. | High |
| Risk measures | § 30 requires suitable, proportionate and effective technical and organizational measures, documented by the entity, covering ten minimum subject areas. | Map technical controls to the ten statutory themes, but do not equate a mapping with legal compliance. | High |
| Incident reporting | § 32 establishes an early warning within 24 hours, an incident notification within 72 hours, requested interim reporting, and a final report within one month. | The incident exercise should generate four timed reporting artifacts and record when the clock starts: knowledge of an *erheblicher Sicherheitsvorfall*. | High |
| Management duty | § 38 requires management to implement and oversee § 30 measures and to participate regularly in training. | Include management approval, oversight metrics and training evidence in the control-evidence model. | High |
| Digital-entity detail | § 30(3) gives priority to the Commission implementing act for listed digital entities, including online marketplaces. Regulation (EU) 2024/2690 is in force. | If the fictional entity is made consumer-facing, add a dedicated 2024/2690 applicability/control crosswalk rather than relying on § 30(2) alone. | High |

### Terminology guardrails

- Preferred: **NIS-2-Richtlinie**, **NIS-2-Umsetzungsgesetz**, **BSI-Gesetz (BSIG)**, **besonders wichtige Einrichtung (bwE)**, **wichtige Einrichtung (wE)**, **erheblicher Sicherheitsvorfall**, **Risikomanagementmaßnahmen**.
- Avoid: calling the enacted German law “still pending”; treating “KRITIS”, “bwE” and “wE” as synonyms; using *wesentliche Einrichtung* as though it were the § 28 category; saying that ISO 27001 or IT-Grundschutz certification is legally required for every wE/bwE.
- The BSI frequently writes “NIS-2”; the formal act abbreviation may appear as **NIS2UmsuCG**. Preserve titles as published by their source.

## 2. RheinCommerce applicability assessment

### Statutory logic

- § 28(1)(4) BSIG assigns an Anlage-1 entity to bwE when it has at least 250 employees **or** both annual revenue above EUR 50 million and balance-sheet total above EUR 43 million.
- § 28(2)(3) BSIG assigns an entity in Anlage 1 or Anlage 2 to wE when it has at least 50 employees **or** both annual revenue and balance-sheet total above EUR 10 million, unless it is already a bwE.
- Anlage 2 no. 6 lists providers of online marketplaces, online search engines and social-networking platforms.
- § 2 no. 28 BSIG cross-refers to § 312l BGB. Section 312l(2) describes a service that enables consumers to conclude distance contracts; § 312l(3) identifies the operator that makes such a marketplace available to consumers.
- § 28(4) imports the Commission SME recommendation for headcount and financial calculations and contains a specific rule about partner/linked undertakings. A real assessment therefore needs entity/group facts, not just a marketing headcount.

### Facts, assumptions and result

| Type | Item | Effect |
|---|---|---|
| Scenario fact | RheinCommerce GmbH is fictional, headquartered in Düsseldorf, has about 280 employees and provides a B2B marketplace and related commerce services. | The headcount would satisfy the numeric thresholds if counted under § 28(4). |
| Scenario fact | The brief does not state that consumers can conclude distance contracts on the platform. | The statutory online-marketplace definition is not yet proven. |
| Scenario assumption | “Annual turnover above the relevant threshold” is intentionally vague and no balance-sheet total is supplied. | The financial limbs cannot be tested. This does not block the employee-count limb, but the missing facts must remain visible. |
| Legal fact | Online-marketplace providers are in Anlage 2. | A qualifying marketplace with this headcount would normally be a **wE**, not a bwE solely because it is large. |
| Unknown | No evidence establishes KRITIS status, an Anlage-1 service, telecom status, group aggregation, an exception, or a special jurisdiction rule. | Do not infer another category or regulator. |

**Conditional conclusion (medium confidence):**

- If RheinCommerce enables consumers to conclude distance contracts and the headcount is attributable under § 28(4), the scenario supports classification as a **wichtige Einrichtung** under § 28(2)(3) in conjunction with Anlage 2 no. 6.1.1.
- If the service is genuinely B2B-only, the supplied facts do **not** establish the online-marketplace category. Ordinary e-commerce activity is not by itself enough to infer BSIG scope.
- The project should keep the ambiguity and implement controls as an “NIS-2-aligned readiness baseline”. A later scenario document may deliberately add a consumer-facing service, but it must label that as a fictional design assumption rather than retroactively presenting it as a researched fact.

## 3. Minimum obligation baseline if the entity is in scope

| BSIG reference | Obligation theme | RheinShield evidence target |
|---|---|---|
| § 30(1) | Proportionate, effective, documented measures protecting availability, integrity and confidentiality | Risk register, control design, validation results, residual-risk record |
| § 30(2) no. 1 | Risk analysis and information-system security policies | Threat model, risk method, policies, Azure baseline |
| § 30(2) no. 2 | Incident handling | Sentinel detections, triage runbooks, INC-001 timeline |
| § 30(2) no. 3 | Business continuity, backup, disaster recovery and crisis management | BIA, backup/restore design and tested exercise evidence |
| § 30(2) no. 4 | Supply-chain security | Supplier register, GitHub dependency controls, cloud shared-responsibility notes |
| § 30(2) no. 5 | Secure acquisition, development and maintenance; vulnerability handling/disclosure | IaC scanning, dependency scanning, secure SDLC, vulnerability workflow |
| § 30(2) no. 6 | Effectiveness assessment | Automated tests, control metrics, internal-review evidence |
| § 30(2) no. 7 | Basic cyber-hygiene and awareness | Role-based training and exercise record |
| § 30(2) no. 8 | Cryptography concepts and processes | Key Vault/managed identity design, TLS and key-management standards |
| § 30(2) no. 9 | Personnel security, access control and asset management | Entra ID/RBAC/PIM/JML design and asset inventory |
| § 30(2) no. 10 | MFA/continuous authentication and secure communications | Conditional Access templates, MFA evidence model, emergency communications design |
| § 32 | Significant-incident reporting workflow | Synthetic 24-hour, 72-hour, interim and one-month report package |
| § 33 | Registration and change notifications | Applicability owner, deadline calculator and registration checklist |
| § 38 | Management oversight and training | Management dashboard, approval record and training register |

This is a traceability baseline, not an exhaustive legal requirements register. Sector rules, implementing acts, regulator instructions and facts about the real entity can change the required controls.

## 4. Current BSI IT-Grundschutz baseline

### Verified edition

The official German BSI page retrieved on 2026-08-29 labels **Edition 2023**, available since 2023-02-01, as the IT-Grundschutz Compendium and provides the PDF, modules, cross-reference tables, XML, change documents, checklists and errata for that edition. The page metadata had been updated later, but no later compendium edition was offered. Therefore:

- RheinShield should pin its mapping metadata to `edition: 2023` and `retrieved: 2026-08-29`.
- The German edition is the authoritative working baseline; the BSI warns that English versions can differ and are not the certification basis.
- IT-Grundschutz is a methodology/control source, not a declaration that RheinShield or the fictional company is certified.

### Relevant module shortlist

This shortlist is intentionally selective. The final model must document why each module applies to the defined information domain and must not claim that a module title alone proves implementation.

| Area | Relevant Edition-2023 modules | RheinShield use |
|---|---|---|
| ISMS and organization | ISMS.1, ORP.1, ORP.2, ORP.3, ORP.4, ORP.5 | Security governance, personnel, awareness, IAM and compliance management |
| Concepts | CON.1, CON.2, CON.3, CON.8 | Cryptography, privacy, backup and secure software development |
| Operations | OPS.1.1.2, OPS.1.1.3, OPS.1.1.5, OPS.1.1.6, OPS.2.2 | Administration, patch/change control, logging, testing/release and cloud use |
| Detection and response | DER.1, DER.2.1, DER.2.2, DER.2.3, DER.3.1, DER.4 | Detection, incident handling, forensics readiness, major incidents, audit and emergency management |
| Applications/systems | APP.3.1, SYS.1.1, SYS.1.6 | Web workload, general server controls and containerization |
| Networks | NET.1.1, NET.1.2, NET.3.2 | Network architecture, network management and firewalling |

### Mapping rules

1. Record module and requirement identifiers at the requirement level in the compliance dataset, not just the module name.
2. Distinguish `designed`, `implemented`, `tested`, `live-validated` and `not-applicable-with-rationale`.
3. Store public evidence only after sanitization; tenant IDs, subscription IDs, identities and raw portal exports stay private/untracked.
4. A Terraform plan or fixture test can support design/plan evidence, but cannot be reported as a live control test.
5. Review the official compendium page and errata again immediately before a public release.

## 5. Primary sources

All links were retrieved successfully on 2026-08-29 unless noted.

| Source | Publisher | Date/status | Decision supported |
|---|---|---|---|
| [NIS-2-Umsetzungsgesetz ab morgen in Kraft](https://www.bsi.bund.de/DE/Service-Navi/Presse/Pressemitteilungen/Presse2025/251205_NIS-2-Umsetzungsgesetz_in_Kraft.html) | BSI | 2025-12-05 | Effective date and expanded scope |
| [NIS-2-regulierte Unternehmen](https://www.bsi.bund.de/DE/Themen/Regulierte-Wirtschaft/NIS-2-regulierte-Unternehmen/nis-2-regulierte-unternehmen_node.html) | BSI | Current page | Self-assessment and BSI guidance hub |
| [NIS-2-Pflichten](https://www.bsi.bund.de/DE/Themen/Regulierte-Wirtschaft/NIS-2-regulierte-Unternehmen/NIS-2-Pflichten/nis-2-pflichten_node.html) | BSI | Current page | Registration and incident-reporting overview |
| [Second registration step available](https://www.bsi.bund.de/DE/Service-Navi/Presse/Pressemitteilungen/Presse2026/260601_NIS2_BSI-Portal.html) | BSI | 2026-06-01 | Current portal status |
| [Official BSIG](https://www.gesetze-im-internet.de/bsig_2025/) | Federal Ministry of Justice / Federal Office of Justice | Current consolidated text | Statutory source |
| [§ 2 BSIG](https://www.gesetze-im-internet.de/bsig_2025/__2.html) | Federal Ministry of Justice / Federal Office of Justice | Current | Definitions, including online marketplace |
| [§ 28 BSIG](https://www.gesetze-im-internet.de/bsig_2025/__28.html) | Federal Ministry of Justice / Federal Office of Justice | Current | Entity categories and size thresholds |
| [§ 30 BSIG](https://www.gesetze-im-internet.de/bsig_2025/__30.html) | Federal Ministry of Justice / Federal Office of Justice | Current | Risk-management measures and implementing-act priority |
| [§ 32 BSIG](https://www.gesetze-im-internet.de/bsig_2025/__32.html) | Federal Ministry of Justice / Federal Office of Justice | Current | Reporting sequence and deadlines |
| [§ 33 BSIG](https://www.gesetze-im-internet.de/bsig_2025/__33.html) | Federal Ministry of Justice / Federal Office of Justice | Current | Registration and update deadlines |
| [§ 38 BSIG](https://www.gesetze-im-internet.de/bsig_2025/__38.html) | Federal Ministry of Justice / Federal Office of Justice | Current | Management oversight, liability context and training |
| [Anlage 1 BSIG](https://www.gesetze-im-internet.de/bsig_2025/anlage_1.html) | Federal Ministry of Justice / Federal Office of Justice | BGBl. 2025 I Nr. 301 pp. 43–46 | Higher-criticality sectors |
| [Anlage 2 BSIG](https://www.gesetze-im-internet.de/bsig_2025/anlage_2.html) | Federal Ministry of Justice / Federal Office of Justice | BGBl. 2025 I Nr. 301 pp. 47–48 | Online marketplaces listed as digital-service providers |
| [§ 312l BGB](https://www.gesetze-im-internet.de/bgb/__312l.html) | Federal Ministry of Justice / Federal Office of Justice | Current | Consumer-facing marketplace definition |
| [Commission Implementing Regulation (EU) 2024/2690](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32024R2690) | EUR-Lex / European Union | In force; 2024-10-17 | Detailed technical/methodological requirements for listed digital entities |
| [IT-Grundschutz-Kompendium](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/IT-Grundschutz/IT-Grundschutz-Kompendium/it-grundschutz-kompendium_node.html) | BSI | Edition 2023, available 2023-02-01 | Current compendium edition and official download set |

## 6. Uncertainty and revalidation triggers

- Vacancy and compliance sources are time-sensitive. Revalidate this note before release or after any BSIG amendment, BSI portal notice, new implementing act, or new IT-Grundschutz edition/errata.
- The official Federal Gazette page returned an automated-access restriction during this run. The publication number is corroborated by the consolidated statute and BSI source; the public link remains `https://www.recht.bund.de/bgbl/1/2025/301/VO.html` for manual verification.
- A legal applicability decision for a real company requires exact service design, customer type, group structure, employee calculation, revenue, balance-sheet total, establishment/jurisdiction, sector overlays and exceptions.
- ISO/IEC 27001:2022 text is copyrighted and is not reproduced here. Any later mapping should use control identifiers and licensed/authorized summaries only.
