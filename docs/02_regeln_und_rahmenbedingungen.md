# Regeln und Rahmenbedingungen

**Stand:** 01.11.2026, ergänzt am 15.11.2026 (Abschnitt 6) und am 17.11.2026 (alle Länderseiten der CWP: Abschnitte 1–6). Dies ist keine Rechtsberatung; die rechtlichen Punkte sind eine Einordnung.

---

## 1. Absprachen mit WWOOF (Oktober und November 2026)

Der Nutzer hat bei den WWOOF-Organisationen jeweils nachgefragt. Die Antworten liegen hier nur als **Zusammenfassung des Nutzers** vor, nicht im Originalwortlaut.

**Nicht erlaubt:**
- Massenzugriffe
- persönliche Daten oder Kontaktdaten von Gastgeber:innen an KI-Dienste weitergeben

**Erlaubt:**
- KI zur Planung der Reiseroute nutzen
- KI zum Verfassen eigener Nachrichten an Gastgeber:innen nutzen
- eine eigene Liste von Höfen zur privaten, nicht-kommerziellen Planung führen

**Laut Nutzer zusätzlich:** Der Ort (ohne genaue Adresse) darf an Claude gehen.

**Abklärung zum Hof-Sammler (vom Nutzer berichtet am 01.11.2026):** Laut Nutzer ist mit WWOOF abgeklärt, dass das geplante Skript und die Vorgehensweise in Ordnung sind. Ausgeschlossen sind:
- **Massenabrufe.** Laut Nutzer gibt es kein Verbot automatischer Zugriffe, solange kein Massenabruf in Sekunden stattfindet. Das Skript arbeitet deshalb mit Pausen und Obergrenzen (`03_programmierprojekt.md`, Abschnitt 2).
- **Direktes KI-Browsing,** also eine KI, die die Plattform selbst liest oder bedient. Daraus folgt auch: Claude startet keine Skripte, die eine Länderseite der CWP oder api.wwoof.net aufrufen (Abschnitt 6).

**Geltungsbereich der Abklärung (vom Nutzer bestätigt am 17.11.2026):** Abgeklärt hat der Nutzer mit WWOOF Deutschland und mit dem Plattformbetreiber (Federation of WWOOF Organisations, FoWO, Betreiber der CWP). Laut Nutzer gilt die Abklärung für **alle Länderseiten der Common WWOOF Platform**, nicht nur für wwoof.de. Sie wird hier einmal festgehalten und nicht je Länderseite wiederholt. Für jede weitere Länderseite bleiben trotzdem eine eigene Mitgliedschaft und die Checkliste in `07_bedienung.md`, Teil C, nötig. Länderseiten außerhalb der CWP (z. B. wwoof.ie) gehören nicht zum Umfang (Abschnitt 3.2).

Laut Nutzer umfasst die Abklärung auch die Weitergabe **bereinigter, vom Nutzer freigegebener Beschreibungen** an Claude (bestätigt am 01.11.2026).

**Entscheidung des Nutzers (31.10.2026):** Hofnamen gehen nicht an Claude. Sie stehen nur in der lokalen Tabelle des KI-freien Skripts; Claude arbeitet mit Hof-Codes.

**Empfehlung:** Die Originalantworten von WWOOF aufbewahren, auch die Abklärung zum Hof-Sammler.

**Hinweis zur Vorgeschichte:** In der ursprünglichen Anfrage an WWOOF stand, dass keine Hofdaten gespeichert und keine eigene Datenbank angelegt werden (damals bezogen auf KI-gestütztes Lesen im Account). Laut Nutzer hat WWOOF anschließend eine private Hofliste für die Planung erlaubt. Der Hof-Sammler stützt sich auf diese spätere Aussage und speichert deshalb eine **Liste** (CSV-Dateien), keine Datenbank.

---

## 2. Datenregeln (verbindlich für dieses Projekt)

| Darf an Claude | Bleibt beim Nutzer (lokal) |
|---|---|
| Hof-Code (z. B. `DE-VA-003`, ohne Bezug zum Namen) | Hofname und Zuordnung Hof-Code ↔ Hofname |
| Ort (Gemeinde bzw. nächster Ort, ohne Adresse), Region, Land | Personennamen (Hosts, Familie, Gäste) |
| Lernkategorien der Plattform | Adressen, Koordinaten |
| Stichwort-Kategorien aus der Taxonomie | Kontaktdaten (Telefon, E-Mail, Website, Social Media) |
| Anzahl der Gästebucheinträge (nur die Zahl) | Profil-Links, Benutzernamen, Profil-IDs |
| Freie Zeitfenster (aus dem Kalender) | Fotos, Screenshots von Hofseiten |
| Unterkunft, Arbeitszeiten, Sprache, Abholung (als Kategorie) | Originalbeschreibung (unbereinigt) |
| Eigene Notizen und Einschätzungen ohne Personenbezug (z. B. „großer Gemüsegarten“) | Gästebuchtexte (das Skript speichert sie gar nicht) |
| **Bereinigte Beschreibung:** nur mit Freigabe des Nutzers | Nachrichten der Hosts im Wortlaut, HTML-Quelltext von Hofseiten |
| | Browser-Profil mit Login-Sitzung |

**„Bereinigt“ heißt:** Hofname, Personennamen, Kontakt- und Adressdaten sind entfernt, und der Nutzer hat den Text gelesen und freigegeben. Das Verfahren beschreibt `03_programmierprojekt.md`, Abschnitt 7.

**Antworten der Hosts** gehen nur zusammengefasst an Claude, z. B. „DE-VA-003: Zusage 14.–28.4., Abholung am Bahnhof möglich“.

**Technische Trennung (Entscheidung vom 01.11.2026):** Alle Hofdaten liegen im Datenordner `wwoof-data/` außerhalb des Code-Repositorys. Claude erhält darauf keinen Zugriff und fragt in Claude Code auch nicht danach; eine Read-Deny-Regel sperrt den Ordner zusätzlich (Einrichtung in Phase 0). Claude startet keine Skripte, die eine Länderseite der CWP oder api.wwoof.net aufrufen oder echte Hofdaten verarbeiten. Den Export lädt der Nutzer selbst hoch. Details: `03_programmierprojekt.md`, Abschnitt 5.1.

---

## 3. Nutzungsbedingungen: relevante Punkte

### 3.1 Common WWOOF Platform (u. a. Deutschland und Norwegen)

- Die Länderseiten wwoof.de und wwoofnorway.org laufen auf der Common WWOOF Platform (CWP). Die Hofsuche erfolgt über die Länderseite; es gelten die Bedingungen der CWP.
- **Umfang des Hof-Sammlers (Entscheidung vom 17.11.2026):** Der Sammler ist für alle Länderseiten der CWP gebaut; die Länderseite wird in der Konfiguration gewählt. Nicht belegt ist, dass alle Länderseiten technisch gleich aufgebaut sind; das klärt die Länder-Prüfung je Länderseite (`07_bedienung.md`, Teil C). Für jede Länderseite ist eine eigene Mitgliedschaft bei der jeweiligen Landesorganisation nötig.
- Die Plattform gehört der Federation of WWOOF Organisations (FoWO), einer britischen Gesellschaft. Die Allgemeinen Nutzungsbedingungen haben den Stand 22.12.2024.
- **Verboten ist unter anderem:**
  - personenbezogene Daten zum eigenen Profit sammeln, durch Data-Mining auswerten oder abgreifen
  - Robot-Exclusion-Header oder technische Schutzmaßnahmen umgehen oder stören
  - Spam, definiert als dieselbe Nachricht an 10 oder mehr Mitglieder
- **Automatisierte Zugriffe:** Den Volltext konnte Claude nicht lesen, weil das Hilfecenter den Abruf per Bot-Erkennung blockiert hat (das wurde nicht umgangen). Die Frage, ob automatisierte Zugriffe verboten sind, ist laut Nutzer durch die Abklärung mit WWOOF erledigt (Abschnitt 1): Das Skript und die Vorgehensweise sind in Ordnung, Massenabrufe und direktes KI-Browsing sind ausgeschlossen. Das **Gate vor Phase 4** ist damit erfüllt; die Abklärung gilt für alle Länderseiten der CWP (Abschnitt 1).
- **Datenschutzerklärung der CWP:** Zu den Angaben über die landwirtschaftliche Tätigkeit, die einen Host identifizieren können, zählt sie ausdrücklich den **Hofnamen** sowie weitere Profilangaben wie die **Beschreibung** und Angaben zu den Mitbewohnern. Daraus folgen die Entscheidungen zu Hof-Codes und zur Bereinigung der Beschreibungen.

### 3.2 WWOOF Ireland (eigene Plattform, Bedingungen vollständig gelesen)

- **Kein ausdrückliches Bot-Verbot.**
- **Abschnitt 9, Nutzungsbeschränkungen:**
  - (b) kein Sammeln, Data-Mining oder Abgreifen personenbezogener Daten zum eigenen Profit
  - (e) keine Bearbeitungen, Übersetzungen oder abgeleiteten Werke von Inhalten
  - (f) kein Umgehen von Robot-Exclusion-Headern oder technischen Maßnahmen
  - (g), (k) keine unverhältnismäßige Belastung der Infrastruktur
  - (l) Spam: dieselbe Nachricht an 10 oder mehr Mitglieder
  - (n) Informationen über andere Nutzer nur so erheben oder speichern, wie es die Plattform erlaubt
  - (o) personenbezogene Daten anderer Nutzer nicht ohne Erlaubnis veröffentlichen
  - (s) Dritten nicht bei solchen Verstößen helfen
- **Abschnitt 8:** Das Mitglied ist für jede Nutzung seiner Informationen bzw. seines Accounts verantwortlich, auch durch andere.
- **Abschnitte 7 und 15:** Nutzung geschützter Inhalte nur mit vorheriger schriftlicher Genehmigung; ein Verzicht auf Bestimmungen ist nur schriftlich bindend.
- **Recht:** irisches Recht, Streitigkeiten per Schiedsverfahren.
- **Außerhalb des Umfangs (Entscheidung vom 17.11.2026):** wwoof.ie läuft nicht auf der CWP. Für Irland gibt es keinen Code und keine Vorbereitung. Diese Zusammenfassung der Bedingungen bleibt als Information für die Reiseplanung.

### 3.3 WWOOF-Charta (alle Länder)

- Artikel 10: Mitglieder vervielfältigen die Hostliste nicht, geben sie nicht weiter und nutzen sie nur fürs WWOOFing. Die private Planungsliste ist laut Nutzer durch die Zusage von WWOOF abgedeckt.

### 3.4 WWOOF Belgien (Richtwert für Anfragen)

- WWOOFer sollen nicht viele Hosts gleichzeitig kontaktieren, idealerweise weniger als 3.

---

## 4. Klärungsbedarf

1. **robots.txt der gewählten Länderseite:** Das Skript prüft sie vor jedem Lauf und bricht bei einem Verbot ab.
2. **Weitere Länderseiten:** Vor dem ersten Lauf gegen eine neue Länderseite die Checkliste in `07_bedienung.md`, Teil C (Mitgliedschaft, Regionsschlüssel und -kürzel, robots.txt-Prüfung, Länder-Prüfung, Suchdefinition je Region, Testlauf mit einem Profil).

**Erledigt:**
- Hofname an Claude: entfällt, weil Hofnamen lokal bleiben (Entscheidung vom 31.10.2026).
- Nutzungsbeschränkungen der CWP (Verbot automatisierter Zugriffe?): laut Nutzer durch die Abklärung mit WWOOF erledigt (01.11.2026).
- Beschreibungen an Claude: Bereinigte, vom Nutzer freigegebene Beschreibungen dürfen laut Nutzer an Claude gehen; die Abklärung mit WWOOF umfasst das (01.11.2026).

---

## 5. Gesetzlicher Rahmen (Einordnung, keine Rechtsberatung)

- **Datenschutz, Haushaltsausnahme (Art. 2 Abs. 2 lit. c DSGVO):** Die DSGVO gilt nicht für Verarbeitungen durch natürliche Personen zur Ausübung ausschließlich persönlicher oder familiärer Tätigkeiten. Private Reiseplanung fällt sehr wahrscheinlich darunter. Die genauen Grenzen sind aber offen: Der BGH hat dem EuGH im September 2026 Fragen dazu vorgelegt (I ZR 256/25, I ZR 289/25). Daraus folgt: so wenige Personendaten wie möglich.
- **Datenbankrecht (§ 87b UrhG):** Dem Datenbankhersteller steht das Recht zu, die Datenbank insgesamt oder wesentliche Teile davon zu vervielfältigen. Dem gleichgestellt ist die wiederholte und systematische Vervielfältigung unwesentlicher Teile, wenn sie der normalen Auswertung zuwiderläuft oder berechtigte Interessen unzumutbar beeinträchtigt. Daraus folgt: nur einzelne Regionen, keine Gesamtliste, auf jeder Länderseite. Gesamtumfang und Tagesgrenze werden vor Phase 5 festgelegt, auch ob sie je Länderseite oder insgesamt gelten (`00_projekt_uebersicht.md`, offener Punkt 11).
- **Realistisches Hauptrisiko:** vertraglich, also eine Sperrung des Accounts. Bei privater Nutzung ohne Weitergabe ist kein Strafrisiko erkennbar.

---

## 6. Entscheidungen (Verlauf)

| Entscheidung | Begründung |
|---|---|
| Kein KI-Lesen im WWOOF-Account | Regel „keine Personendaten an KI-Dienste“; Profilseiten enthalten praktisch immer Personendaten |
| Kein automatischer Versand von Nachrichten | Nachrichten gehen nur mit Freigabe raus; der Nutzer versendet selbst |
| Kein Scraper für die gesamte Hostliste, kein Verschleiern automatisierter Zugriffe | Massenzugriffe verboten; Datenbankrecht; Verschleierung grenzt an das Umgehen technischer Maßnahmen |
| Hof-Sammler erlaubt unter Auflagen | KI-frei, nur einzelne Regionen, normales Tempo mit Obergrenzen, lokale Speicherung, Export an Claude nur über eine Whitelist (Details in `03_programmierprojekt.md`) |
| Hof-Sammler mit WWOOF abgeklärt (laut Nutzer, berichtet am 01.11.2026) | Skript und Vorgehensweise in Ordnung; ausgeschlossen sind Massenabrufe und direktes KI-Browsing |
| Läufe gegen eine Länderseite startet nur der Nutzer; Claude startet keine Skripte, die eine Länderseite der CWP oder api.wwoof.net aufrufen oder echte Hofdaten verarbeiten (01.11.2026, seit 17.11.2026 für alle Länderseiten) | Kein KI-Browsing, auch nicht indirekt; Hofdaten gelangen nicht in Claudes Kontext |
| Hof-Sammler für alle Länderseiten der CWP; Auswahl über die Konfiguration; andere Plattformen (z. B. wwoof.ie) außerhalb des Umfangs (17.11.2026) | Entscheidung des Nutzers; eine Plattform, eine Codebasis, einfacher Aufbau |
| Abklärung mit WWOOF Deutschland und dem Plattformbetreiber gilt für alle Länderseiten der CWP (bestätigt am 17.11.2026) | Angabe des Nutzers; einmal hier festgehalten (Abschnitt 1), nicht je Länderseite |
| Vor dem ersten Lauf gegen eine Länderseite: Mitgliedschaft, Regionsschlüssel und -kürzel, robots.txt-Prüfung, Länder-Prüfung, Suchdefinition je Region, Testlauf mit einem Profil (17.11.2026) | Checkliste in `07_bedienung.md`, Teil C; im Code bleiben die robots.txt-Prüfung vor jedem Lauf und der Abbruch des Sammlers bei fehlender Suchdefinition |
| Code und Hofdaten in getrennten Ordnern; Datenordner für Claude nicht zugänglich (01.11.2026) | Wunsch des Nutzers; technische statt nur organisatorischer Trennung |
| Zusammenarbeit über Claude Code lokal auf dem Laptop (01.11.2026): Start nur im Code-Ordner, Read-Deny-Regel für den Datenordner, Modus mit Rückfrage, kein Auto-Modus | Entscheidung des Nutzers. Laut Claude-Code-Doku gelten Read-Deny-Regeln nicht für Skripte, die Dateien selbst öffnen, und die Sandbox läuft nicht unter nativem Windows. Deshalb gilt zusätzlich die Regel, dass Claude keine Skripte mit echten Daten startet |
| Claude Code schreibt den Code (15.11.2026): Modus „Edit automatically“ (Dateiänderungen im Code-Ordner ohne Rückfrage, Befehle mit Rückfrage); Auto-Modus und Bypass per `.claude/settings.json` gesperrt; `git push` nur durch den Nutzer | Entscheidung des Nutzers; die Datenregeln gelten unverändert. Die Grenze der Read-Deny-Regel bei Skripten bleibt bestehen; deshalb bleibt die Rückfrage vor jedem Befehl Pflicht, und Claude Code startet weiterhin nur Code mit erfundenen Daten |
| Hofnamen bleiben lokal, Claude arbeitet mit Hof-Codes | Entscheidung des Nutzers (31.10.2026); die CWP-Datenschutzerklärung zählt den Hofnamen zu den identifizierenden Angaben |
| Gästebuch: nur die Anzahl wird erfasst und exportiert, keine Texte | Entscheidung des Nutzers (31.10.2026); Datensparsamkeit |
| Gästebuch-Tenor gestrichen | Entscheidung des Nutzers (01.11.2026): nur die Anzahl ist relevant; laut Nutzer gibt der Host Einträge zur Veröffentlichung frei |
| Jeder Hof wird nur einmal erfasst, keine erneuten Abrufe | Entscheidung des Nutzers (01.11.2026); Datensparsamkeit, weniger Seitenaufrufe |
| Freie Zeitfenster aus dem Kalender werden erfasst, falls technisch gut möglich | Entscheidung des Nutzers (01.11.2026); Zeitfenster sind laut Datenregeln für Claude erlaubt |
| Beschreibungen gehen nur bereinigt und vom Nutzer freigegeben an Claude; laut Nutzer von der Abklärung mit WWOOF umfasst (01.11.2026) | Regel „keine Personendaten an KI-Dienste“; Beschreibungen enthalten oft Namen; die CWP-Datenschutzerklärung nennt die Beschreibung als möglicherweise identifizierend |
| Keine Web-Recherche zu einzelnen Höfen durch Claude | Gefahr, auf Personendaten zu stoßen |
| Löschung aller Hofdaten nach der Reise; darum kümmert sich der Nutzer, auch um hochgeladene Exporte | Zusage aus der Anfrage an WWOOF |
| Stichwort-Umwandlung lokal und regelbasiert | Kategorien strukturieren die Bewertung; für nicht freigegebene Beschreibungen sind sie die einzige Beschreibungsinformation für Claude |

---

## Quellen

- CWP, Allgemeine Nutzungsbedingungen: https://help.wwoof.net/hc/en-us/articles/25138615988509 (deutsch: https://help.wwoof.net/hc/de/articles/25138615988509-Allgemeine-Nutzungsbedingungen)
- CWP, Datenschutzerklärung: https://help.wwoof.net/hc/en-us/articles/25137724404893
- Organisationen auf der CWP: https://help.wwoof.net/hc/en-us/articles/25620416952861-WWOOF-Organizations-on-the-Common-WWOOF-Platform-CWP
- WWOOF Ireland, General Terms of Use (2024): https://wwoof.ie/wp-content/uploads/2024/12/terms-conditions-public-2024.pdf
- WWOOF-Charta: https://docs.wwoof.net/wwoof-charter.pdf
- Charta WWOOF Belgien: https://docs.wwoof.net/BE/membership-terms.pdf
- Art. 2 DSGVO: https://lxgesetze.de/dsgvo/2
- BGH-Vorlage zur Haushaltsausnahme: https://www.datev.de/web/de/berufsgruppenuebergreifend/nachrichten/ndsr/recht/BGH-EuGH-Fragen-Haushaltsausnahme-Datenschutz-Grundverordnung
- § 87b UrhG: https://lxgesetze.de/urhg/87b
- Claude Code, Berechtigungen: https://code.claude.com/docs/en/permissions
- Claude Code, Berechtigungsmodi: https://code.claude.com/docs/en/permission-modes
- Claude Code, Sandbox: https://code.claude.com/docs/en/sandboxing
