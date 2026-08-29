import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import '../app/globals.css';

type Language = 'en' | 'de';
type Status = 'LIVE_DEPLOYED' | 'LIVE_VALIDATED' | 'FIXTURE_VALIDATED' | 'PLAN_VALIDATED' | 'READY_NOT_AUTHENTICATED' | 'READY_LICENSE_REQUIRED' | 'SKIPPED_COST_GUARD' | 'UNAVAILABLE' | 'FAILED_WITH_EVIDENCE';

const routes = [
  ['executive', 'Executive overview', 'Lagebild'],
  ['landing-zone', 'Landing zone', 'Landing Zone'],
  ['identity', 'Identity', 'Identität'],
  ['soc', 'SOC & detections', 'SOC & Detektionen'],
  ['incident', 'Incident', 'Vorfall'],
  ['risk', 'Risk & compliance', 'Risiko & Compliance'],
  ['cost', 'Cost & operations', 'Kosten & Betrieb'],
  ['methodology', 'Methodology', 'Methodik'],
] as const;

const detectionRows = [
  ['RS001', 'Password spray', 'Kennwort-Spraying', 'Credential Access', 'Zugriff auf Anmeldedaten', 'Microsoft Entra ID'],
  ['RS002', 'Success after failures', 'Erfolg nach Fehlversuchen', 'Initial Access', 'Initialzugriff', 'Microsoft Entra ID'],
  ['RS003', 'Impossible travel', 'Unmögliche Reise', 'Initial Access', 'Initialzugriff', 'Microsoft Entra ID'],
  ['RS004', 'Privileged role assignment', 'Privilegierte Rollenzuweisung', 'Privilege Escalation', 'Rechteausweitung', 'Audit Logs'],
  ['RS005', 'Service principal credential', 'Anmeldeinformation für Dienstprinzipal', 'Persistence', 'Persistenz', 'Audit Logs'],
  ['RS006', 'Conditional Access change', 'Änderung am bedingten Zugriff', 'Defense Evasion', 'Umgehung von Schutzmaßnahmen', 'Audit Logs'],
  ['RS007', 'Unrestricted inbound rule', 'Uneingeschränkte Eingangsregel', 'Initial Access', 'Initialzugriff', 'Azure Activity'],
  ['RS008', 'Monitoring control deleted', 'Überwachungskontrolle gelöscht', 'Defense Evasion', 'Umgehung von Schutzmaßnahmen', 'Azure Activity'],
  ['RS009', 'Storage public access', 'Öffentlicher Speicherzugriff', 'Exfiltration', 'Datenabfluss', 'Azure Activity'],
  ['RS010', 'Key Vault access spike', 'Zugriffsspitze am Key Vault', 'Credential Access', 'Zugriff auf Anmeldedaten', 'Diagnostics'],
  ['RS011', 'Encoded PowerShell', 'Kodierte PowerShell', 'Execution', 'Ausführung', 'Security Events'],
  ['RS012', 'Mass object download', 'Massenhafter Objektdownload', 'Collection', 'Sammlung', 'Diagnostics'],
  ['RS013', 'Unfamiliar deployment principal', 'Unbekannte Bereitstellungsidentität', 'Persistence', 'Persistenz', 'Azure Activity'],
  ['RS014', 'Repeated denied operations', 'Wiederholt abgelehnte Vorgänge', 'Discovery', 'Erkundung', 'Azure Activity'],
] as const;

const risks = [
  ['Identity compromise', 'Identitätskompromittierung', 20, 10, 'Treat', 'Behandeln'], ['Privileged access misuse', 'Missbrauch privilegierter Zugriffe', 20, 8, 'Treat', 'Behandeln'],
  ['Public storage exposure', 'Öffentliche Speicherfreigabe', 16, 8, 'Treat', 'Behandeln'], ['Logging interruption', 'Unterbrechung der Protokollierung', 16, 6, 'Treat', 'Behandeln'],
  ['Supplier credential abuse', 'Missbrauch von Lieferantenzugängen', 15, 9, 'Treat', 'Behandeln'], ['Regional service outage', 'Regionaler Dienstausfall', 12, 8, 'Mitigate', 'Mindern'],
  ['Unsupported component', 'Nicht unterstützte Komponente', 12, 6, 'Treat', 'Behandeln'], ['Data retention drift', 'Abweichende Aufbewahrung', 9, 4, 'Monitor', 'Beobachten'],
] as const;

const controls = [
  ['Allowed regions', 'Zulässige Regionen', 'RSP-001', 'ISO A.5.23 · BSIG §30'],
  ['Required project tag', 'Pflichtkennzeichnung Projekt', 'RSP-002', 'ISO A.5.9 · MCSB AM-1'],
  ['Required lifecycle tags', 'Pflichtkennzeichnungen Lebenszyklus', 'RSP-003', 'ISO A.5.9 · BSI ORP.1.A2'],
  ['Storage TLS 1.2', 'Speicher mit TLS 1.2', 'RSP-004', 'ISO A.8.24 · MCSB DP-3'],
  ['Secure transfer required', 'Sichere Übertragung erforderlich', 'RSP-005', 'ISO A.8.24 · MCSB DP-4'],
  ['Public blob access disabled', 'Öffentlicher Blobzugriff deaktiviert', 'RSP-006', 'ISO A.8.3 · MCSB NS-2'],
  ['Storage public network assessed', 'Öffentliches Speichernetz geprüft', 'RSP-007', 'ISO A.8.20 · MCSB NS-2'],
  ['Key Vault RBAC', 'Key Vault mit RBAC', 'RSP-008', 'ISO A.5.15 · MCSB PA-7'],
  ['Key Vault purge protection', 'Löschschutz für Key Vault', 'RSP-009', 'ISO A.8.13 · MCSB DP-6'],
  ['Public IP restricted', 'Öffentliche IP eingeschränkt', 'RSP-010', 'ISO A.8.20 · MCSB NS-2'],
  ['No Internet SSH/RDP', 'Kein SSH/RDP aus dem Internet', 'RSP-011', 'ISO A.8.20 · BSI NET.1.1.A11'],
  ['Managed identity required', 'Verwaltete Identität erforderlich', 'RSP-012', 'ISO A.5.16 · MCSB IM-3'],
  ['Diagnostics required', 'Diagnoseeinstellungen erforderlich', 'RSP-013', 'ISO A.8.15 · MCSB LT-3'],
  ['Shared storage key disabled', 'Gemeinsamer Speicherschlüssel deaktiviert', 'RSP-014', 'ISO A.5.17 · MCSB IM-1'],
] as const;

const incident = [
  ['07:25', 'Baseline deviation begins', 'Abweichung von der Basislinie beginnt', 'Synthetic contractor identity receives repeated failures.', 'Synthetisches Dienstleisterkonto erzeugt wiederholte Fehlversuche.', 'Observe', 'Beobachten'],
  ['07:31', 'RS001 fires', 'RS001 löst aus', 'Password-spray threshold reached; incident INC-001 opened.', 'Schwellenwert für Kennwort-Spraying erreicht; INC-001 eröffnet.', 'MTTD 6m', 'MTTD 6m'],
  ['07:40', 'Analyst acknowledges', 'Analyst übernimmt', 'Identity events correlated with supplier access window.', 'Identitätsereignisse mit Lieferantenzugriffsfenster korreliert.', 'MTTA 9m', 'MTTA 9m'],
  ['07:44', 'RS004 correlates', 'RS004 korreliert', 'Unexpected privileged role assignment raises severity to High.', 'Unerwartete privilegierte Rollenzuweisung erhöht den Schweregrad auf Hoch.', 'Escalate', 'Eskalieren'],
  ['08:02', 'Containment approved', 'Eindämmung freigegeben', 'Dry-run playbook documents revoke-session and disable-account steps.', 'Dry-Run-Playbook dokumentiert Sitzungsentzug und Kontosperrung.', 'Dry run', 'Trockenlauf'],
  ['08:19', 'Recovery complete', 'Wiederherstellung abgeschlossen', 'Synthetic identity isolated; access review and token inventory queued.', 'Synthetische Identität isoliert; Zugriffsprüfung und Tokeninventar eingeplant.', 'MTTR 48m', 'MTTR 48m'],
] as const;

const resourceGroups = [
  ['network', 'VNet, 3 subnets, private DNS links', 'VNet, 3 Subnetze, private DNS-Verknüpfungen'],
  ['security', 'Log Analytics, Key Vault, storage, Sentinel path', 'Log Analytics, Key Vault, Speicher, Sentinel-Pfad'],
  ['workload', 'Internal Container Apps environment and API', 'Interne Container-Apps-Umgebung und API'],
] as const;

const hunts = [
  ['HQ001', 'Identity attack chain', 'Identitätsangriffskette', 'SigninLogs + AuditLogs'],
  ['HQ002', 'Dormant privileged account', 'Inaktives privilegiertes Konto', 'SigninLogs'],
  ['HQ003', 'Resource tampering sequence', 'Abfolge von Ressourcenmanipulationen', 'AzureActivity'],
  ['HQ004', 'Key Vault access anomaly', 'Anomalie beim Key-Vault-Zugriff', 'AzureDiagnostics'],
  ['HQ005', 'Encoded script execution', 'Ausführung kodierter Skripte', 'SecurityEvent'],
] as const;

const text = {
  en: {
    eyebrow: 'RheinCommerce GmbH · fictional German marketplace',
    title: 'Security evidence, made inspectable.',
    lede: 'A portfolio-grade Azure landing zone and security operations platform connecting governance, identity, detection engineering, response, and audit-ready evidence.',
    notice: 'Synthetic portfolio data — no real tenant, identity, incident, or customer information',
    disclaimer: 'Educational portfolio case study — not legal advice, certification, or a claim of regulatory compliance.',
    mode: 'PUBLIC-DEMO', openMenu: 'Open navigation', closeMenu: 'Close navigation', switchLanguage: 'Deutsche Ansicht öffnen',
  },
  de: {
    eyebrow: 'RheinCommerce GmbH · fiktiver deutscher Marktplatz',
    title: 'Sicherheitsnachweise, klar nachvollziehbar.',
    lede: 'Eine portfoliofähige Azure Landing Zone mit Security Operations – von Governance und Identitäten bis zu Detektionen, Reaktion und prüfbaren Nachweisen.',
    notice: 'Synthetische Portfoliodaten — keine realen Mandanten-, Identitäts-, Vorfalls- oder Kundendaten',
    disclaimer: 'Ausbildungs- und Portfolio-Fallstudie — keine Rechtsberatung, Zertifizierung oder Konformitätsaussage.',
    mode: 'PUBLIC-DEMO', openMenu: 'Navigation öffnen', closeMenu: 'Navigation schließen', switchLanguage: 'Open English view',
  },
};

function StatusBadge({ children }: { children: Status | string }) {
  const value = String(children);
  const tone = value.includes('FIXTURE') ? 'good' : value.includes('PLAN') ? 'info' : value.includes('LICENSE') || value.includes('COST') ? 'warn' : 'neutral';
  return <span className={`status ${tone}`}>{children}</span>;
}

function PageHeader({ kicker, title, intro, status = 'FIXTURE_VALIDATED' }: { kicker: string; title: string; intro: string; status?: Status }) {
  return <header className="page-header"><div><p className="eyebrow">{kicker}</p><h1>{title}</h1><p className="lede">{intro}</p></div><StatusBadge>{status}</StatusBadge></header>;
}

function Metric({ label, value, detail, tone = 'mint' }: { label: string; value: string; detail: string; tone?: string }) {
  return <article className={`metric ${tone}`}><span>{label}</span><b>{value}</b><small>{detail}</small></article>;
}

function Panel({ title, kicker, children, className = '' }: React.PropsWithChildren<{ title: string; kicker?: string; className?: string }>) {
  return <article className={`panel ${className}`}><div className="panel-heading">{kicker && <p className="eyebrow">{kicker}</p>}<h2>{title}</h2></div>{children}</article>;
}

function Executive({ lang }: { lang: Language }) {
  const de = lang === 'de';
  return <>
    <PageHeader kicker={text[lang].eyebrow} title={text[lang].title} intro={text[lang].lede} />
    <section className="metric-grid" aria-label={de ? 'Wichtige Kennzahlen' : 'Key security metrics'}>
      <Metric label={de ? 'Erfasste Assets' : 'Governed assets'} value="26" detail={de ? '100 % klassifiziert' : '100% classified'} />
      <Metric label={de ? 'Policy-Kontrollen' : 'Policy controls'} value="14" detail={de ? 'Nachweise verknüpft' : 'evidence linked'} tone="blue" />
      <Metric label={de ? 'Kritische inhärente Risiken' : 'Critical inherent risks'} value="3" detail={de ? '27 offene Risiken insgesamt' : '27 open risks in total'} tone="amber" />
      <Metric label={de ? 'Detektionsabdeckung' : 'Detection coverage'} value="14/14" detail={de ? 'Fixtures bestanden' : 'fixtures passed'} />
    </section>
    <section className="two-col">
      <Panel kicker={de ? 'Nachweisreife' : 'Assurance posture'} title={de ? 'Validierung nach Modus' : 'Validation by mode'}>
        <div className="assurance-score"><strong>20</strong><span>{de ? 'Fähigkeiten mit Modus, Nachweis und Grenze' : 'capabilities with mode, evidence, and limitation'}</span></div>
        <dl className="status-list"><div><dt>{de ? 'Enterprise-Referenz' : 'Enterprise reference'}</dt><dd><StatusBadge>READY_NOT_AUTHENTICATED</StatusBadge></dd></div><div><dt>Azure Lab</dt><dd><StatusBadge>PLAN_VALIDATED</StatusBadge></dd></div><div><dt>Sentinel</dt><dd><StatusBadge>FIXTURE_VALIDATED</StatusBadge></dd></div><div><dt>Defender</dt><dd><StatusBadge>READY_LICENSE_REQUIRED</StatusBadge></dd></div></dl>
      </Panel>
      <Panel kicker="INC-001" title={de ? 'Kompromittiertes Dienstleisterkonto' : 'Compromised contractor identity'}>
        <div className="incident-status"><span>{de ? 'Eingedämmt (Simulation)' : 'Contained (simulation)'}</span><StatusBadge>FIXTURE_VALIDATED</StatusBadge></div>
        <div className="trio"><div><b>6m</b><span>MTTD</span></div><div><b>9m</b><span>MTTA</span></div><div><b>48m</b><span>MTTR</span></div></div>
        <p className="muted">{de ? 'Zeitwerte stammen ausschließlich aus der deterministischen Übung.' : 'Timing values derive only from the deterministic exercise.'}</p>
      </Panel>
    </section>
    <section className="three-col">
      <Panel title={de ? 'Identität' : 'Identity'}><p className="big-label">8</p><p>{de ? 'Rollen- und Gruppentypen mit Funktionstrennung.' : 'role and group types with separation of duties.'}</p></Panel>
      <Panel title={de ? 'Datenaktualität' : 'Data freshness'}><p className="big-label">29 Aug</p><p>{de ? 'Fester Seed 20260829, reproduzierbar.' : 'Fixed seed 20260829, reproducible.'}</p></Panel>
      <Panel title={de ? 'Priorität' : 'Top priority'}><p className="big-label amber-text">P1</p><p>{de ? 'Azure Live-Validierung nach Kosten- und Berechtigungsprüfung.' : 'Azure live validation after cost and permission gate.'}</p></Panel>
    </section>
    <Panel kicker={de ? 'Entscheidungsübersicht' : 'Decision brief'} title={de ? 'Status, Risiko und nächste Entscheidung' : 'Status, risk, and next decision'}><div className="evidence-grid"><div><b>{de ? 'Aktueller Nachweis' : 'Current evidence'}</b><ul className="check-list"><li>{de ? '28/28 deterministische Detektionserwartungen bestanden' : '28/28 deterministic detection expectations passed'}</li><li>{de ? 'Terraform-Laborplan mit Mock-Provider validiert' : 'Terraform lab plan validated with mock provider'}</li><li>{de ? 'INC-001: Hoch, eingedämmt, reine Simulation' : 'INC-001: High, contained, simulation only'}</li></ul></div><div><b>{de ? 'Management-Entscheidung' : 'Management decision'}</b><ul className="node-list"><li>{de ? 'Drei kritische inhärente Risiken zuerst behandeln' : 'Treat three critical inherent risks first'}</li><li>{de ? 'Azure-Live-Test nur nach Authentifizierung und €20-Gate' : 'Run Azure live proof only after authentication and €20 gate'}</li><li>{de ? 'Keine regulatorische Konformität oder Produktionswirksamkeit behauptet' : 'No regulatory compliance or production efficacy claimed'}</li></ul></div></div></Panel>
  </>;
}

function LandingZone({ lang }: { lang: Language }) {
  const de = lang === 'de';
  return <>
    <PageHeader kicker={de ? 'Governance & Plattform' : 'Governance & platform'} title={de ? 'Landing Zone und Governance' : 'Landing zone & governance'} intro={de ? 'Zwei getrennte Wege: eine produktionsnahe Enterprise-Referenz und ein sicherer Ein-Subscription-Labormodus.' : 'Two deliberately separate paths: a production-oriented enterprise reference and a safe single-subscription lab.'} status="PLAN_VALIDATED" />
    <section className="two-col architecture-compare">
      <Panel kicker="ENTERPRISE-REFERENCE" title={de ? 'Zielarchitektur' : 'Target architecture'}><ul className="node-list"><li>{de ? 'Eigene RheinShield-Stammgruppe' : 'Dedicated RheinShield reference root'}</li><li>{de ? 'Plattform: Management · Konnektivität · Identität' : 'Platform: management · connectivity · identity'}</li><li>{de ? 'Landing Zones: Unternehmen · Online · Sandbox' : 'Landing Zones: corp · online · sandbox'}</li><li>{de ? 'Abonnements für Entwicklung · Test · Produktion' : 'Development · test · production subscriptions'}</li><li>{de ? 'Zentrale Richtlinien; Zielbild für Protokollierung, privates DNS und Hub-Netz' : 'Central policy; target design for logging, private DNS, and hub network'}</li></ul><StatusBadge>READY_NOT_AUTHENTICATED</StatusBadge></Panel>
      <Panel kicker="LAB" title={de ? 'Deploybares Labor' : 'Deployable lab'}><ul className="node-list"><li>{de ? 'Drei vorab erstellte, exakt benannte Ressourcengruppen' : 'Three pre-created, exact-name resource groups'}</li><li>{de ? 'Fünf Terraform-Module' : 'Five Terraform modules'}</li><li>{de ? 'Internes Container-Umfeld und private Endpunkte' : 'Internal container environment and private endpoints'}</li><li>{de ? 'Log-Analytics-/Sentinel-Konfigurationspfad' : 'Log Analytics / Sentinel configuration path'}</li><li>{de ? 'Ablaufkennzeichnung und exaktes Lösch-Gate' : 'Expiry tag and exact-target teardown gate'}</li></ul><StatusBadge>PLAN_VALIDATED</StatusBadge></Panel>
    </section>
    <section className="metric-grid"><Metric label={de ? 'Assets' : 'Assets'} value="26" detail={de ? 'mit BIA verknüpft' : 'BIA-linked'} /><Metric label={de ? 'Terraform-Module' : 'Terraform modules'} value="5" detail={de ? 'Namen · Netz · Monitoring · Sicherheit · Workload' : 'naming · network · monitoring · security · workload'} tone="blue" /><Metric label={de ? 'Policy-Kontrollen' : 'Policy controls'} value="14" detail={de ? 'versionierte Baseline' : 'versioned baseline'} /><Metric label="Region" value="Germany W" detail={de ? 'Westeuropa als Ausweichregion' : 'West Europe fallback'} tone="amber" /></section>
    <Panel kicker={de ? 'Kontrollfluss' : 'Control flow'} title={de ? 'Zentraler Nachweispfad' : 'Central evidence path'}><div className="flow" role="img" aria-label={de ? 'Workloads senden Protokolle über Log Analytics und Sentinel zum Nachweismanifest und Dashboard' : 'Workloads send logs through Log Analytics and Sentinel to the evidence manifest and dashboard'}><span>{de ? 'Workloads' : 'Workloads'}</span><i>→</i><span>Log Analytics</span><i>→</i><span>Sentinel</span><i>→</i><span>{de ? 'Nachweismanifest' : 'Evidence manifest'}</span><i>→</i><span>Dashboard</span></div></Panel>
    <section className="two-col"><Panel kicker={de ? 'Ressourceninventar' : 'Resource inventory'} title={de ? 'Exakter Laborscope' : 'Exact lab scope'}><div className="table-wrap"><table><caption>{de ? 'Nur neue, suffixgebundene Gruppen; keine Wiederverwendung' : 'New suffix-bound groups only; no reuse'}</caption><thead><tr><th>{de ? 'Gruppe' : 'Group'}</th><th>{de ? 'Geplanter Inhalt' : 'Planned contents'}</th></tr></thead><tbody>{resourceGroups.map(row=><tr key={row[0]}><td><code>{`…-${row[0]}`}</code></td><td>{de ? row[2] : row[1]}</td></tr>)}</tbody></table></div></Panel><Panel kicker={de ? 'Governance-Metadaten' : 'Governance metadata'} title={de ? 'Kennzeichnung und Protokollierung' : 'Tagging & logging'}><dl className="status-list"><div><dt>{de ? 'Pflichtkennzeichnungen' : 'Required tags'}</dt><dd>6</dd></div><div><dt>{de ? 'Ablaufzeit' : 'Expiry'}</dt><dd>24h</dd></div><div><dt>{de ? 'Log-Aufbewahrung' : 'Log retention'}</dt><dd>30d</dd></div><div><dt>{de ? 'Diagnoseziele' : 'Diagnostic targets'}</dt><dd>Key Vault · Storage · App</dd></div><div><dt>{de ? 'Öffentlicher Datenzugriff' : 'Public data access'}</dt><dd>{de ? 'Deaktiviert' : 'Disabled'}</dd></div></dl><p className="muted">Project · Owner · Environment · DataClassification · ManagedBy · ExpiresAt</p></Panel></section>
    <Panel kicker={de ? 'Richtlinienabdeckung' : 'Policy coverage'} title={de ? '14 versionierte Kontrollen' : '14 versioned controls'}><div className="table-wrap"><table><caption>{de ? 'Policy-Baseline mit Standardwirkung Audit; keine Live-Zuweisung' : 'Policy baseline with Audit default; no live assignment'}</caption><thead><tr><th>ID</th><th>{de ? 'Kontrolle' : 'Control'}</th><th>{de ? 'Zuordnung' : 'Mapping'}</th></tr></thead><tbody>{controls.map(row=><tr key={row[2]}><td><code>{row[2]}</code></td><td>{de ? row[1] : row[0]}</td><td>{row[3]}</td></tr>)}</tbody></table></div></Panel>
  </>;
}

function Identity({ lang }: { lang: Language }) {
  const de = lang === 'de';
  const roles = de
    ? [['Plattformadministration','PIM-berechtigte Projektrolle'],['Security-Analyse','Trennung Sentinel-Mitwirkende/Lesende'],['Workload-Betrieb','Mitwirkende auf Ressourcengruppenebene'],['Entwicklung','Bereitstellung nur über föderierte Identität'],['Audit','Leserechte und Nachweiszugriff'],['Dienstleistende','Befristeter Zugriff und wiederkehrende Prüfung'],['Externe Lieferanten','Gastlebenszyklus und Sponsor'],['Notfallzugriff','Ausgenommen, überwacht, zwei Identitäten']]
    : [['Platform administrators','PIM-eligible project role'],['Security analysts','Sentinel Contributor / Reader split'],['Workload operators','Resource-group Contributor'],['Developers','Deployment-only federated identity'],['Auditors','Reader + evidence access'],['Contractors','Time-bound access, recurring review'],['External suppliers','Guest lifecycle + sponsor'],['Emergency access','Excluded, monitored, two identities']];
  return <>
    <PageHeader kicker="Microsoft Entra ID · Zero Trust" title={de ? 'Identität und Zero Trust' : 'Identity & Zero Trust'} intro={de ? 'Minimale Rechte, Funktionstrennung und zeitlich begrenzter Zugriff – als sichere, nicht erzwungene Entwürfe.' : 'Least privilege, separation of duties, and time-bound access—delivered as safe, non-enforcing designs.'} status="READY_NOT_AUTHENTICATED" />
    <section className="metric-grid"><Metric label={de ? 'Rollenmodelle' : 'Role models'} value="8" detail={de ? 'RBAC- und Entra-Gruppen' : 'RBAC + Entra groups'} /><Metric label="Conditional Access" value="6" detail={de ? 'deaktivierte Entwurfsdatensätze' : 'disabled design records'} tone="blue" /><Metric label={de ? 'Langfristige CI-Geheimnisse' : 'Long-lived CI secrets'} value="0" detail={de ? 'OIDC-Föderationsentwurf' : 'OIDC federation design'} /><Metric label={de ? 'Lizenzabhängig' : 'License dependent'} value="3" detail={de ? 'PIM · Risiko · Zugriffsprüfungen' : 'PIM · risk · access reviews'} tone="amber" /></section>
    <section className="two-col"><Panel title={de ? 'Rollen- und Gruppenmodell' : 'Role & group model'}><div className="table-wrap"><table><caption>{de ? 'Acht menschliche Rollen; Workload- und CI-Identitäten werden separat geführt' : 'Eight human roles; workload and CI identities are tracked separately'}</caption><thead><tr><th>{de ? 'Rolle' : 'Persona'}</th><th>{de ? 'Kontrolle' : 'Control'}</th></tr></thead><tbody>{roles.map(r=><tr key={r[0]}><td>{r[0]}</td><td>{r[1]}</td></tr>)}</tbody></table></div></Panel><Panel title={de ? 'Zugriffslebenszyklus' : 'Access lifecycle'}><ol className="steps"><li><b>{de ? 'Eintritt' : 'Joiner'}</b><span>{de ? 'Personal-Trigger, Sponsor, minimale Gruppe' : 'HR trigger, sponsor, minimum group'}</span></li><li><b>{de ? 'Wechsel' : 'Mover'}</b><span>{de ? 'Altzugriff vor neuer Vergabe entziehen' : 'Remove prior access before grant'}</span></li><li><b>{de ? 'Prüfung' : 'Reviewer'}</b><span>{de ? 'Quartalsweise Zugriffsbestätigung' : 'Quarterly certification'}</span></li><li><b>{de ? 'Austritt' : 'Leaver'}</b><span>{de ? 'Sperren, Token widerrufen, prüfen' : 'Block, revoke tokens, review'}</span></li></ol></Panel></section>
    <section className="three-col"><Panel title={de ? 'Privilegierte Rollen' : 'Privileged roles'}><p className="big-label">4h</p><p>{de ? 'Maximale Aktivierung; Begründung, MFA und Freigabe im PIM-Entwurf.' : 'Maximum activation; justification, MFA, and approval in the PIM design.'}</p><StatusBadge>READY_LICENSE_REQUIRED</StatusBadge></Panel><Panel title="Conditional Access"><p className="big-label">6</p><p>{de ? 'Deaktivierte Vorlagen mit zwei Notfallkonten, gestufter Einführung und Rückfallplan.' : 'Disabled templates with two emergency accounts, staged rollout, and rollback plan.'}</p><StatusBadge>READY_LICENSE_REQUIRED</StatusBadge></Panel><Panel title={de ? 'Zugriffsprüfungen' : 'Access reviews'}><p className="big-label">90d</p><p>{de ? 'Quartalsweise Prüfung für privilegierte, externe und dienstleistende Zugriffe.' : 'Quarterly review for privileged, guest, and contractor access.'}</p><StatusBadge>READY_LICENSE_REQUIRED</StatusBadge></Panel></section>
    <Panel kicker="OIDC" title={de ? 'GitHub Actions ohne langfristiges Geheimnis' : 'Secretless GitHub Actions'}><div className="flow"><span>{de ? 'Geschützte GitHub-Umgebung' : 'Protected GitHub environment'}</span><i>→</i><span>{de ? 'OIDC-Subjekt' : 'OIDC subject'}</span><i>→</i><span>{de ? 'Föderierte Anmeldeinformation' : 'Federated credential'}</span><i>→</i><span>{de ? 'Drei exakte Ressourcengruppen' : 'Three exact resource groups'}</span></div><p className="muted">{de ? 'Das Vertrauen ist auf Repository und geschützte Umgebung begrenzt; es gibt kein Clientgeheimnis und keine Abonnementrolle für Mitwirkende.' : 'Trust is constrained to the repository and protected environment; there is no client secret or subscription-level Contributor role.'}</p></Panel>
  </>;
}

function Soc({ lang }: { lang: Language }) {
  const de = lang === 'de';
  const tacticCoverage = de
    ? [['Initialzugriff',3],['Zugriff auf Anmeldedaten',2],['Persistenz',2],['Umgehung von Schutzmaßnahmen',2],['Rechteausweitung',1],['Ausführung',1],['Sammlung',1],['Datenabfluss',1],['Erkundung',1]] as const
    : [['Initial Access',3],['Credential Access',2],['Persistence',2],['Defense Evasion',2],['Privilege Escalation',1],['Execution',1],['Collection',1],['Exfiltration',1],['Discovery',1]] as const;
  return <>
    <PageHeader kicker="Microsoft Sentinel · KQL · MITRE ATT&CK" title={de ? 'SOC und Detektionsabdeckung' : 'SOC & detection coverage'} intro={de ? 'Detektionen als Code mit bösartigen und gutartigen Fixtures, nachvollziehbaren Datenabhängigkeiten und sicheren Dry-Run-Playbooks.' : 'Detections as code with malicious and benign fixtures, explicit data dependencies, and safe dry-run playbooks.'} />
    <section className="metric-grid"><Metric label={de ? 'Analytics-Regeln' : 'Analytics rules'} value="14" detail={de ? '14/14 Fixtures bestanden' : '14/14 fixtures passed'} /><Metric label={de ? 'Hunting-Abfragen' : 'Hunting queries'} value="5" detail={de ? 'auf Angriffsketten ausgerichtet; nicht live ausgeführt' : 'attack-chain oriented; not live executed'} tone="blue" /><Metric label="Workbooks" value="3" detail={de ? 'validierte JSON-Vorlagen' : 'validated JSON templates'} /><Metric label="SOAR" value="3 + 3" detail={de ? 'Automatisierungen und Playbooks' : 'automation + playbooks'} tone="amber" /></section>
    <section className="two-col wide-left"><Panel title={de ? 'Detektionskatalog' : 'Detection catalog'}><div className="table-wrap"><table><caption>{de ? 'Vierzehn deaktivierte Regeln mit synthetischen Testfällen' : 'Fourteen disabled rules with synthetic test cases'}</caption><thead><tr><th>ID</th><th>{de ? 'Anwendungsfall' : 'Use case'}</th><th>{de ? 'MITRE-Taktik' : 'MITRE tactic'}</th><th>{de ? 'Quelle' : 'Source'}</th></tr></thead><tbody>{detectionRows.map(r=><tr key={r[0]}><td><code>{r[0]}</code></td><td>{de ? r[2] : r[1]}</td><td>{de ? r[4] : r[3]}</td><td>{r[5]}</td></tr>)}</tbody></table></div></Panel><Panel title={de ? 'Fixture-Testmatrix' : 'Fixture test matrix'}><div className="donut" role="img" aria-label={de ? '14 richtig positive und 14 richtig negative Ergebnisse' : '14 true positives and 14 true negatives'}><strong>28/28</strong><span>{de ? 'Erwartungen erfüllt' : 'expectations met'}</span></div><dl className="status-list"><div><dt>{de ? 'Richtig positiv' : 'True positives'}</dt><dd>14</dd></div><div><dt>{de ? 'Richtig negativ' : 'True negatives'}</dt><dd>14</dd></div><div><dt>{de ? 'Falsch positiv' : 'False positives'}</dt><dd>0</dd></div><div><dt>{de ? 'Falsch negativ' : 'False negatives'}</dt><dd>0</dd></div></dl><p className="muted">{de ? 'Fixture-Metriken sind kein Nachweis für Produktionswirksamkeit; die Python-Auswertung ersetzt keine KQL-Ausführung im Dienst.' : 'Fixture metrics do not represent production efficacy; the Python evaluator is not a service-side KQL execution.'}</p></Panel></section>
    <Panel kicker="MITRE ATT&CK" title={de ? 'Abdeckung nach Taktik' : 'Coverage by tactic'}><div className="coverage-grid">{tacticCoverage.map(([label,count])=><div className="coverage-row" key={label}><span>{label}</span><div aria-hidden="true"><i style={{width:`${count/3*100}%`}}/></div><b>{count}</b></div>)}</div></Panel>
    <section className="two-col"><Panel kicker={de ? 'Proaktive Suche' : 'Threat hunting'} title={de ? 'Fünf versionierte Hunting-Abfragen' : 'Five versioned hunting queries'}><div className="table-wrap"><table><caption>{de ? 'Strukturell validiert; keine Live-KQL-Ausführung' : 'Structurally validated; no live KQL execution'}</caption><thead><tr><th>ID</th><th>{de ? 'Hypothese' : 'Hypothesis'}</th><th>{de ? 'Tabelle' : 'Table'}</th></tr></thead><tbody>{hunts.map(row=><tr key={row[0]}><td><code>{row[0]}</code></td><td>{de ? row[2] : row[1]}</td><td>{row[3]}</td></tr>)}</tbody></table></div></Panel><Panel kicker={de ? 'Betriebsregelkreis' : 'Operating loop'} title={de ? 'Tuning und sichere Automation' : 'Tuning & safe automation'}><ol className="steps"><li><b>{de ? 'Täglich' : 'Daily'}</b><span>{de ? 'Fehlalarme, Datenlücken und Entitätszuordnung prüfen' : 'Review false positives, data gaps, and entity mapping'}</span></li><li><b>{de ? 'Wöchentlich' : 'Weekly'}</b><span>{de ? 'Schwellenwerte und Ausnahmen mit Ablaufdatum prüfen' : 'Review thresholds and expiring exceptions'}</span></li><li><b>{de ? 'Monatlich' : 'Monthly'}</b><span>{de ? 'MITRE-, Quellen- und Runbook-Abdeckung abgleichen' : 'Reconcile MITRE, source, and runbook coverage'}</span></li><li><b>SOAR</b><span>{de ? '3 Regeln und 3 Playbooks standardmäßig deaktiviert und im Trockenlauf' : '3 rules and 3 playbooks disabled and dry-run by default'}</span></li></ol></Panel></section>
  </>;
}

function Incident({ lang }: { lang: Language }) {
  const de = lang === 'de';
  return <>
    <PageHeader kicker="INC-001 · tabletop exercise" title={de ? 'Untersuchung eines Identitätsvorfalls' : 'Identity incident investigation'} intro={de ? 'Eine deterministische Angriffskette verbindet Alarmierung, Analyseentscheidungen, Eindämmung und Verbesserungsmaßnahmen.' : 'A deterministic attack chain connects alerts, analyst decisions, containment, and improvement actions.'} />
    <section className="metric-grid"><Metric label="MTTD" value="6m" detail={de ? 'Beginn → Vorfall' : 'onset → incident'} /><Metric label="MTTA" value="9m" detail={de ? 'Vorfall → Übernahme' : 'incident → acknowledgement'} tone="blue" /><Metric label="MTTR" value="48m" detail={de ? 'Übernahme → Wiederherstellung' : 'acknowledgement → recovery'} /><Metric label={de ? 'Schweregrad' : 'Severity'} value={de ? 'Hoch' : 'High'} detail={de ? 'synthetische Übung' : 'synthetic exercise'} tone="amber" /></section>
    <Panel title={de ? 'Zeitachse und Analystenentscheidungen' : 'Timeline & analyst decisions'}><ol className="timeline">{incident.map((e,i)=><li key={e[0]}><time>{e[0]}</time><span className="timeline-dot"/><div><b>{de ? e[2] : e[1]}</b><p>{de ? e[4] : e[3]}</p><small>{de ? e[6] : e[5]}</small></div>{i<incident.length-1&&<span className="timeline-line"/>}</li>)}</ol></Panel>
    <section className="three-col"><Panel title={de ? 'Betroffene Entitäten' : 'Related entities'}><p><code>contractor-017</code><br/><code>supplier-app-03</code><br/><code>role-sec-reader</code></p></Panel><Panel title={de ? 'Ausgelöste Regeln' : 'Triggered rules'}><p><code>RS001</code> {de ? 'Kennwort-Spraying' : 'Password spray'}<br/><code>RS002</code> {de ? 'Erfolg nach Fehlversuchen' : 'Success after failures'}<br/><code>RS004</code> {de ? 'Privilegierte Zuweisung' : 'Privileged assignment'}</p></Panel><Panel title={de ? 'Verbesserungen' : 'Lessons learned'}><p>{de ? 'Lieferantenzugriff enger befristen, Anomalien priorisieren, Tokeninventar automatisieren.' : 'Shorten supplier access, prioritize anomalies, automate token inventory.'}</p></Panel></section>
    <Panel kicker={de ? 'Nachweiskette' : 'Evidence chain'} title={de ? 'Nachweise und Eindämmungsentscheidungen' : 'Evidence and containment decisions'}><div className="evidence-grid"><div><b>{de ? 'Gesicherte Nachweise' : 'Preserved evidence'}</b><ul className="check-list"><li>{de ? 'Anmelde- und Audit-Ereignisse mit Hashmanifest' : 'Sign-in and audit events with hash manifest'}</li><li>{de ? 'Rollenänderung und Dienstprinzipalaktivität' : 'Role change and service-principal activity'}</li><li>{de ? 'Analysezeitachse und Entscheidungspunkte' : 'Analyst timeline and decision points'}</li></ul></div><div><b>{de ? 'Trockenlauf der Eindämmung' : 'Containment dry run'}</b><ul className="check-list"><li>{de ? 'Sitzungen widerrufen und Konto deaktivieren' : 'Revoke sessions and disable account'}</li><li>{de ? 'Unerwartete Rolle und Anmeldeinformation entfernen' : 'Remove unexpected role and credential'}</li><li>{de ? 'Kontrollen wiederherstellen und Zugriffsprüfung starten' : 'Restore controls and launch access review'}</li></ul></div></div></Panel>
  </>;
}

function Risk({ lang }: { lang: Language }) {
  const de = lang === 'de';
  const heatCounts: Record<string, number> = {'2-5':1,'3-4':5,'3-5':14,'4-4':4,'4-5':3};
  return <>
    <PageHeader kicker="NIS2 · ISO/IEC 27001:2022 · BSI · MCSB" title={de ? 'Risiko und Compliance-Nachweise' : 'Risk & compliance evidence'} intro={de ? 'Ein risikobasierter Querverweis ohne Zertifizierungs- oder Rechtskonformitätsbehauptung.' : 'A risk-based crosswalk with no certification or legal-compliance claim.'} status="FIXTURE_VALIDATED" />
    <div className="legal-note"><strong>{de ? 'Anwendbarkeit:' : 'Applicability:'}</strong> {de ? 'Die Einstufung als wichtiger/besonders wichtiger Einrichtung bleibt wegen Marktplatzdefinition, Tätigkeitsumfang und Rechtsauslegung bedingt. B2B allein genügt nicht als Beleg.' : 'Classification as an important/highly important entity remains conditional on marketplace definition, business scope, and legal interpretation. B2B operation alone is not sufficient evidence.'}</div>
    <section className="metric-grid"><Metric label={de ? 'Risiken' : 'Risks'} value="27" detail={de ? 'Owner und Behandlung' : 'owner & treatment'} /><Metric label={de ? 'Kontrollnachweise' : 'Control evidence'} value="20" detail={de ? 'maschinenlesbar' : 'machine-readable'} tone="blue" /><Metric label={de ? 'Frameworks' : 'Frameworks'} value="4" detail="NIS2 · ISO · BSI · MCSB" /><Metric label={de ? 'Zertifizierungen' : 'Certifications claimed'} value="0" detail={de ? 'bewusst keine' : 'explicitly none'} tone="amber" /></section>
    <section className="two-col"><Panel title={de ? 'Risikobehandlung' : 'Risk treatment'}><div className="table-wrap"><table><caption>{de ? 'Auszug aus 27 offenen synthetischen Risiken' : 'Excerpt from 27 open synthetic risks'}</caption><thead><tr><th>{de ? 'Risiko' : 'Risk'}</th><th>{de ? 'Inhärent' : 'Inherent'}</th><th>{de ? 'Residual' : 'Residual'}</th><th>{de ? 'Antwort' : 'Response'}</th></tr></thead><tbody>{risks.map(r=><tr key={String(r[0])}><td>{de ? r[1] : r[0]}</td><td><span className="risk-score high">{r[2]}</span></td><td><span className={`risk-score ${Number(r[3])>8?'high':Number(r[3])>5?'med':'low'}`}>{r[3]}</span></td><td>{de ? r[5] : r[4]}</td></tr>)}</tbody></table></div></Panel><Panel title={de ? 'Risikomatrix' : 'Risk heat map'}><p className="muted">{de ? 'Anzahl nach Eintrittswahrscheinlichkeit (Zeilen 5–1) und Auswirkung (Spalten 1–5).' : 'Counts by likelihood (rows 5–1) and impact (columns 1–5).'}</p><div className="risk-heat" role="img" aria-label={de ? 'Risikomatrix mit 27 inhärenten Risiken: 3 bei Wahrscheinlichkeit 4 und Auswirkung 5; 4 bei 4 und 4; 14 bei 3 und 5; 5 bei 3 und 4; 1 bei 2 und 5.' : 'Risk heat map with 27 inherent risks: 3 at likelihood 4 impact 5; 4 at 4 and 4; 14 at 3 and 5; 5 at 3 and 4; 1 at 2 and 5.'}><span/><>{[1,2,3,4,5].map(impact=><b key={`h-${impact}`}>{impact}</b>)}</>{[5,4,3,2,1].flatMap(likelihood=>[<b key={`l-${likelihood}`}>{likelihood}</b>,...[1,2,3,4,5].map(impact=>{const count=heatCounts[`${likelihood}-${impact}`]||0; const score=likelihood*impact; return <i key={`${likelihood}-${impact}`} className={score>=20?'critical':score>=12?'high':score>=6?'med':'low'}>{count||'·'}</i>})])}</div></Panel></section>
    <Panel title={de ? 'Kontrollzuordnung' : 'Control mapping'}><div className="table-wrap"><table><caption>{de ? 'Vierzehn Policy-Kontrollen mit ausgewählten Framework-Verweisen' : 'Fourteen policy controls with selected framework references'}</caption><thead><tr><th>{de ? 'Kontrolle' : 'Control'}</th><th>ID</th><th>{de ? 'Zuordnung' : 'Mapping'}</th></tr></thead><tbody>{controls.map(r=><tr key={r[2]}><td>{de ? r[1] : r[0]}</td><td><code>{r[2]}</code></td><td>{r[3]}</td></tr>)}</tbody></table></div></Panel>
    <Panel kicker={de ? '20 Nachweiskontrollen' : '20 evidence controls'} title={de ? 'Status nach belastbarem Nachweismodus' : 'Status by defensible evidence mode'}><div className="evidence-status-summary"><article><b>9</b><span>FIXTURE_VALIDATED</span></article><article><b>7</b><span>PLAN_VALIDATED</span></article><article><b>2</b><span>READY_NOT_AUTHENTICATED</span></article><article><b>1</b><span>READY_LICENSE_REQUIRED</span></article><article><b>1</b><span>UNAVAILABLE</span></article></div><p className="muted">{de ? 'Die vollständige Matrix verknüpft jede Kontrolle mit BSIG/NIS2, ISO/IEC 27001:2022, BSI, MCSB und einem konkreten Repository-Nachweis.' : 'The complete matrix links every control to BSIG/NIS2, ISO/IEC 27001:2022, BSI, MCSB, and one concrete repository evidence path.'}</p></Panel>
    <Panel kicker={de ? 'Verbesserungsplan' : 'Remediation roadmap'} title={de ? 'Prioritäten für 90 Tage' : 'Priorities across 90 days'}><div className="roadmap"><article><b>0–30</b><span>{de ? 'Identität und Protokollierung' : 'Identity and logging'}</span><small>{de ? 'Phishing-resistente Anmeldung, Dienstleisterprüfung, Diagnosealarme' : 'Phishing-resistant auth, contractor review, diagnostic alerts'}</small></article><article><b>31–60</b><span>{de ? 'Workload und Lieferkette' : 'Workload and supply chain'}</span><small>{de ? 'Freigabe für Anmeldeinformationen, SBOM-Gate, Lieferantennachweise' : 'Credential approval, SBOM gate, supplier evidence'}</small></article><article><b>61–90</b><span>{de ? 'Resilienz und Betrieb' : 'Resilience and operations'}</span><small>{de ? 'Wiederherstellungsübung, Regionstest, Management-Planspiel' : 'Restore exercise, regional test, management tabletop'}</small></article></div></Panel>
  </>;
}

function Cost({ lang }: { lang: Language }) {
  const de = lang === 'de';
  return <>
    <PageHeader kicker={de ? 'Kostenleitplanke · Lebenszyklus' : 'Cost guard · lifecycle'} title={de ? 'Cloud-Kosten und Betrieb' : 'Cloud cost & operations'} intro={de ? 'Keine Azure-Ressourcen ohne Scope-, Preis- und Löschprüfung. Das öffentliche Portfolio bleibt vollständig offline nutzbar.' : 'No Azure resources without scope, price, and teardown gates. The public portfolio remains fully usable offline.'} status="READY_NOT_AUTHENTICATED" />
    <section className="metric-grid"><Metric label={de ? 'Kostenlimit' : 'Cost ceiling'} value="€20" detail={de ? 'gesamter Lauf' : 'entire project run'} /><Metric label={de ? 'Schätzung' : 'Estimate'} value="N/A" detail={de ? 'kein authentifizierter Azure-Plan' : 'no authenticated Azure plan'} tone="amber" /><Metric label={de ? 'Beobachtete Kosten' : 'Observed cost'} value="€0" detail={de ? 'keine Ressourcen erstellt' : 'no resources created'} tone="blue" /><Metric label={de ? 'Ablauf' : 'Expiry'} value="24h" detail={de ? 'Pflichttag; Logs höchstens 30 Tage' : 'mandatory tag; logs max 30 days'} /></section>
    <section className="two-col"><Panel title={de ? 'Kosten-Gate' : 'Cost gate'}><ol className="steps"><li><b>{de ? '1 · Umfang' : '1 · Scope'}</b><span>{de ? 'Drei exakt benannte Projektressourcengruppen' : 'Three exact-name project resource groups'}</span></li><li><b>{de ? '2 · Schätzung' : '2 · Estimate'}</b><span>{de ? 'Aktuelle maschinenlesbare Kostenschätzung' : 'Current machine-readable cost estimate'}</span></li><li><b>{de ? '3 · Bereitstellung' : '3 · Deploy'}</b><span>{de ? 'Minimale synthetische Datenmenge' : 'Minimal synthetic data volume'}</span></li><li><b>{de ? '4 · Nachweise' : '4 · Evidence'}</b><span>{de ? 'Bereinigen und hashen' : 'Sanitize and hash'}</span></li><li><b>{de ? '5 · Löschen' : '5 · Destroy'}</b><span>{de ? 'Exakte Ziele löschen und Abwesenheit prüfen' : 'Delete exact targets and verify absence'}</span></li></ol></Panel><Panel title={de ? 'Betriebsreife' : 'Operational readiness'}><dl className="status-list"><div><dt>{de ? 'Monitoring-Entwurf' : 'Monitoring design'}</dt><dd><StatusBadge>PLAN_VALIDATED</StatusBadge></dd></div><div><dt>{de ? 'Sicherung und Wiederherstellung' : 'Backup & recovery'}</dt><dd><StatusBadge>PLAN_VALIDATED</StatusBadge></dd></div><div><dt>{de ? 'Kostenpflichtige Defender-Pläne' : 'Defender paid plans'}</dt><dd><StatusBadge>SKIPPED_COST_GUARD</StatusBadge></dd></div><div><dt>{de ? 'Ressourcenlöschung' : 'Resource destruction'}</dt><dd><StatusBadge>UNAVAILABLE</StatusBadge></dd></div></dl><p className="muted">{de ? 'Keine Azure-Ressourcen wurden erstellt; daher war keine Löschung erforderlich. Der Löschpfad ist auf drei exakte Namen und Eigentumskennzeichnungen begrenzt.' : 'No Azure resources were created, so destruction was not required. The teardown path is constrained to three exact names and ownership tags.'}</p></Panel></section>
    <Panel kicker={de ? 'Lebenszyklusbeleg' : 'Lifecycle evidence'} title={de ? 'Anlegen, verlängern, löschen, verifizieren' : 'Create, refresh, destroy, verify'}><div className="roadmap"><article><b>0h</b><span>{de ? 'Kollisionsfreier Bootstrap' : 'Collision-free bootstrap'}</span><small>{de ? 'Neue Gruppen und neue plan-only OIDC-Identität' : 'New groups and new plan-only OIDC identity'}</small></article><article><b>&lt;24h</b><span>{de ? 'Hashgebundener Kostennachweis' : 'Hash-bound cost evidence'}</span><small>{de ? 'Infracost-Rohdaten an den gespeicherten Plan gebunden' : 'Raw Infracost output bound to the saved plan'}</small></article><article><b>+15m</b><span>{de ? 'Zweistufige Löschung' : 'Two-step teardown'}</span><small>{de ? 'Frischer Löschplan, synchrone Löschung, Abwesenheitsprüfung, Identitätsentfernung' : 'Fresh destroy plan, synchronous deletion, absence check, identity removal'}</small></article></div></Panel>
  </>;
}

function Methodology({ lang }: { lang: Language }) {
  const de = lang === 'de';
  return <>
    <PageHeader kicker={de ? 'Transparenz vor Behauptungen' : 'Transparency over claims'} title={de ? 'Methodik und Nachweise' : 'Methodology & evidence'} intro={de ? 'Jede Fähigkeit weist Modus, Provenienz, Limitierung und Zeitstempel aus.' : 'Every capability records its mode, provenance, limitation, and verification timestamp.'} />
    <section className="status-grid">{[
      ['LIVE_DEPLOYED',de?'In Azure bereitgestellt.':'Applied in Azure.'],['LIVE_VALIDATED',de?'Live-Verhalten geprüft.':'Live behavior checked.'],['PLAN_VALIDATED',de?'Ein echter oder nachgebildeter IaC-Plan wurde erfolgreich ausgewertet.':'A real or mocked IaC plan completed successfully.'],['FIXTURE_VALIDATED',de?'Deterministische Offline-Daten bestanden.':'Deterministic offline data passed.'],['READY_NOT_AUTHENTICATED',de?'Statisch vorbereitet; authentifizierter Diensttest fehlt.':'Statically prepared; authenticated service test absent.'],['READY_LICENSE_REQUIRED',de?'Technisch entworfen; Lizenz und Live-Test nötig.':'Technically designed; license and live test required.'],['SKIPPED_COST_GUARD',de?'Wegen Kostenleitplanke ausgelassen.':'Omitted by cost guard.'],['UNAVAILABLE',de?'In diesem Lauf nicht verfügbar oder nicht anwendbar.':'Unavailable or inapplicable in this run.'],['FAILED_WITH_EVIDENCE',de?'Fehler mit Nachweis dokumentiert.':'Failure recorded with evidence.'],
    ].map(s=><article key={s[0]}><StatusBadge>{s[0]}</StatusBadge><p>{s[1]}</p></article>)}</section>
    <section className="two-col"><Panel title={de ? 'Reproduzierbare Daten' : 'Reproducible data'}><p className="big-label">738</p><p>{de ? 'Ereignisse über 90 Tage, davon 18 für INC-001. Seed 20260829; SHA-256 im Manifest.' : 'events across 90 days, including 18 for INC-001. Seed 20260829; SHA-256 recorded in the manifest.'}</p></Panel><Panel title={de ? 'Öffentlichkeits-Gate' : 'Public-release gate'}><ul className="check-list"><li>{de ? 'Private Pfade ignoriert' : 'Private paths ignored'}</li><li>{de ? 'PII-, Token-, IP- und Secret-Muster gescannt' : 'PII, token, IP, and secret patterns scanned'}</li><li>{de ? 'PDF-, ZIP- und Bildmetadaten geprüft' : 'PDF, ZIP, and image metadata inspected'}</li><li>{de ? 'Screenshots visuell geprüft' : 'Screenshots visually reviewed'}</li></ul></Panel></section>
    <section className="two-col"><Panel kicker={de ? 'Nachweis-Pipeline' : 'Evidence pipeline'} title={de ? 'Von der Quelle zur öffentlichen Behauptung' : 'From source to public claim'}><ol className="steps"><li><b>1</b><span>{de ? 'Deterministische Fixture oder statisch validierte Vorlage' : 'Deterministic fixture or statically validated template'}</span></li><li><b>2</b><span>{de ? 'Testbericht mit Status und Einschränkung' : 'Test report with status and limitation'}</span></li><li><b>3</b><span>{de ? 'Sanitizing-Scan und SHA-256-Manifest' : 'Sanitization scan and SHA-256 manifest'}</span></li><li><b>4</b><span>{de ? 'Unabhängiger Architektur-, Sicherheits- und Compliance-Review' : 'Independent architecture, security, and compliance review'}</span></li></ol></Panel><Panel kicker={de ? 'Quellenregister' : 'Source register'} title={de ? 'Entscheidungen mit Primärquellen' : 'Decisions backed by primary sources'}><dl className="status-list"><div><dt>Microsoft Learn / Azure</dt><dd>{de ? 'Architektur · Identität · SOC' : 'Architecture · identity · SOC'}</dd></div><div><dt>GitHub Docs</dt><dd>OIDC · Actions · Pages</dd></div><div><dt>BSI / Bundesrecht</dt><dd>NIS2UmsuCG · BSIG · IT-Grundschutz</dd></div><div><dt>EUR-Lex</dt><dd>NIS2 Directive</dd></div><div><dt>{de ? 'Stichtag' : 'As of'}</dt><dd>2026-08-29</dd></div></dl><p className="muted">{de ? 'Publikations- und Abrufdaten sowie Lizenz-/Preview-Grenzen sind im offiziellen Quellenregister dokumentiert.' : 'Publication/retrieval dates and license/preview boundaries are recorded in the official source register.'}</p></Panel></section>
    <Panel kicker={de ? 'Nachweisvollständigkeit' : 'Evidence completeness'} title={de ? '20 Fähigkeiten nach tatsächlichem Validierungsmodus' : '20 capabilities by actual validation mode'}><div className="evidence-status-summary"><article><b>8</b><span>FIXTURE_VALIDATED</span></article><article><b>4</b><span>PLAN_VALIDATED</span></article><article><b>5</b><span>READY_NOT_AUTHENTICATED</span></article><article><b>3</b><span>READY_LICENSE_REQUIRED</span></article></div><p className="muted">{de ? 'Jeder Eintrag der maschinenlesbaren Matrix enthält Nachweispfad, Kosten-/Lizenzstatus, Einschränkung, Zeitstempel und Release-Commit.' : 'Every machine-readable matrix entry records an evidence path, cost/license status, limitation, timestamp, and release commit.'}</p></Panel>
    <Panel title={de ? 'Wesentliche Einschränkungen' : 'Material limitations'}><p>{de ? 'Keine authentifizierte Azure-Subscription und keine kostenpflichtigen Microsoft-Sicherheitslizenzen wurden für diese öffentliche Ausführung verwendet. Enterprise-, Defender-, Entra- und Sentinel-Livewirkungen sind daher nicht behauptet; die entsprechenden Artefakte sind Plan-, Vorlagen- oder Fixture-validiert.' : 'No authenticated Azure subscription or paid Microsoft security licenses were used for this public run. Enterprise, Defender, Entra, and Sentinel live effects are therefore not claimed; the relevant artifacts are plan-, template-, or fixture-validated.'}</p></Panel>
  </>;
}

function App() {
  const initialHash = window.location.hash.replace('#/', '').split('?')[0];
  const [route, setRoute] = useState(routes.some(r=>r[0]===initialHash) ? initialHash : 'executive');
  const [lang, setLang] = useState<Language>(new URLSearchParams(window.location.hash.split('?')[1]).get('lang') === 'de' ? 'de' : 'en');
  const [menuOpen, setMenuOpen] = useState(false);
  const t = text[lang];
  useEffect(() => {
    const onHash = () => { const [next, query] = window.location.hash.replace('#/', '').split('?'); if (routes.some(r=>r[0]===next)) setRoute(next); setLang(new URLSearchParams(query).get('lang')==='de'?'de':'en'); setMenuOpen(false); window.scrollTo(0,0); window.requestAnimationFrame(()=>document.getElementById('main')?.focus()); };
    window.addEventListener('hashchange', onHash); return () => window.removeEventListener('hashchange', onHash);
  }, []);
  useEffect(() => { document.documentElement.lang = lang; document.title = `RheinShield · ${routes.find(r=>r[0]===route)?.[lang==='en'?1:2]}`; }, [lang,route]);
  const page = useMemo(() => ({ executive:<Executive lang={lang}/>, 'landing-zone':<LandingZone lang={lang}/>, identity:<Identity lang={lang}/>, soc:<Soc lang={lang}/>, incident:<Incident lang={lang}/>, risk:<Risk lang={lang}/>, cost:<Cost lang={lang}/>, methodology:<Methodology lang={lang}/> }[route]), [route,lang]);
  const href = (key: string) => `#/${key}?lang=${lang}`;
  const switchLanguage = () => { const next = lang==='en'?'de':'en'; window.location.hash = `/${route}?lang=${next}`; };
  return <div className="app-shell">
    <a className="skip-link" href="#main">{lang==='de'?'Zum Inhalt springen':'Skip to content'}</a>
    <header className="topbar"><a className="brand" href={href('executive')} aria-label={lang==='de'?'RheinShield Startseite':'RheinShield home'}><span className="brand-mark" aria-hidden="true">RS</span><span><b>RheinShield</b><small>{lang==='de'?'Azure-Sicherheitsnachweise':'Azure security evidence'}</small></span></a><button className="menu-button" aria-expanded={menuOpen} aria-label={menuOpen?t.closeMenu:t.openMenu} onClick={()=>setMenuOpen(!menuOpen)}>☰</button><nav className={menuOpen?'open':''} aria-label={lang==='de'?'Hauptnavigation':'Primary navigation'}>{routes.map(r=><a key={r[0]} className={route===r[0]?'active':''} aria-current={route===r[0]?'page':undefined} href={href(r[0])}>{lang==='en'?r[1]:r[2]}</a>)}</nav><button className="language" type="button" onClick={switchLanguage} aria-label={t.switchLanguage}><span className={lang==='en'?'selected':''}>EN</span><i>/</i><span className={lang==='de'?'selected':''}>DE</span></button></header>
    <div className="notice" role="note"><span className="pulse" aria-hidden="true"/><span>{t.notice}</span><b>{t.mode}</b></div>
    <main id="main" tabIndex={-1}>{page}</main>
    <footer><span>{t.disclaimer}</span><span>Omar Ba Jamel · v1.0.0</span></footer>
  </div>;
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
