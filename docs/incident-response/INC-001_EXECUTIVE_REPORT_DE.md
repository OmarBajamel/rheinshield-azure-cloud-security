# Managementbericht DE - INC-001

## Einordnung

INC-001 ist eine vollständig synthetische Sicherheitsübung für die fiktive RheinCommerce GmbH. Es wurden keine realen Konten angegriffen, keine Azure-Ressourcen verändert und keine Kundendaten verarbeitet. Der Bericht ist kein Nachweis einer Zertifizierung oder Rechtskonformität.

## Lagebild

Die Übung verknüpft einen Passwort-Spray-Indikator mit einer erfolgreichen Anmeldung eines Auftragnehmerkontos, einer Rechteerhöhung, einer neuen Anwendungsberechtigung sowie Änderungen an Netzwerk-, Speicher- und Protokollierungskontrollen. Vierzehn regelbasierte Erkennungen wurden mit deterministischen Testdaten geprüft. Die Kontrollkette zeigt, wie technische Signale in eine nachvollziehbare Managemententscheidung überführt werden.

## Übungskennzahlen

- Simulierte MTTD: 6 Minuten
- Simulierte MTTA: 9 Minuten
- Simulierte MTTR: 48 Minuten ab Analystenübernahme
- Datenmodus: synthetisch
- Validierungsmodus: `FIXTURE_VALIDATED`, keine Live-Sentinel-Messung

## Entscheidung und Maßnahmen

Der Analyst empfiehlt das Widerrufen von Sitzungen und Berechtigungen, das Entfernen der neu angelegten Anwendungsberechtigung, die Wiederherstellung der Protokollierungs-, Netzwerk- und Speicherkontrollen sowie eine gezielte Rotation betroffener synthetischer Geheimnisse. Alle Eingriffe bleiben im Standardbetrieb Dry-Run; reale Konten werden nicht deaktiviert.

Prioritäten sind eine phishing-resistente Anmeldung für privilegierte Rollen, zeitlich begrenzte Auftragnehmerrechte, genehmigungspflichtige Änderungen an Workload-Identitäten, der Schutz zentraler Protokollierung und regelmäßige Lieferantenzugriffsprüfungen.

## Meldebewertung

Die gesetzliche Meldepflicht wäre von Rechts-/Compliance-Verantwortlichen anhand der tatsächlichen Betroffenheit und Erheblichkeit zu bewerten. Der Zeitplan für Frühwarnung, Meldung und Abschlussbericht wird im Kommunikationsplan abgebildet; die Übung sendet keine Meldung an Behörden oder Dritte.
