# Entscheidungsprotokoll

**Stand:** 17.11.2026 · Verlauf aller Entscheidungen und abgeschlossenen Schrittpläne, chronologisch; neue Einträge kommen ans Ende. Diese Datei wird nicht automatisch geladen. Den aktuellen Stand zeigt `06_fortschritt.md`.

**Hinweise zu älteren Einträgen:**
- Einträge bis zur Neuausrichtung vom 17.11.2026 (letzter Eintrag) verwenden die alte Phasennummerierung. Zuordnung alt → neu: alte Phase 2 → neue Phasen 2 (pytest, GitHub Actions, robots.txt, Länderseiten-Datei) und 3 (`config.yaml`); alte Phase 3 (Übungsseiten) → in Phase 2 integriert; alte Phase 4 → Phase 2; alte Phase 5 → Phase 3; alte Phase 6 → Phase 5 (Teil B, Bereinigung, entfällt); alte Phase 7 → Phasen 4 und 6.
- Verweise wie „Abschnitt 6“ oder „4.3“ in älteren Einträgen beziehen sich auf die frühere Gliederung von `06_fortschritt.md`; dieser Inhalt steht jetzt hier.

---

## Stand vor der Neuausrichtung (aus 06, Abschnitt 1)

- **Phase 0 abgeschlossen (06.11.2026).**
- **Phase 1 abgeschlossen (17.11.2026)**, Tag `phase-1`. Die Schritte 1–4 sind erledigt und gepusht: Projektstruktur und README, erfundene Testdaten, CSV lesen (`src/farm_table.py`), nach Region filtern und Ergebnis schreiben (`src/filter_region.py`). Schritt 5 (Felder umwandeln, `src/farm_stats.py`) Schritt 6 (Doppelungen erkennen) und Schritt 7 (Vergleich mit pandas, `src/farm_pandas.py`) am 15.11.2026 von Claude Code umgesetzt. Schritt 8 (CSV-Format-Test mit Excel, `src/table_roundtrip.py`) am 17.11.2026 erledigt; das CSV-Format steht fest.
- **Umstellung am 15.11.2026:** Claude Code schreibt den Code schrittweise, der Nutzer prüft, lässt sich erklären und pusht selbst. Regeln in `CLAUDE.md`, Entscheidungen in Abschnitt 6 (15.11.2026), Anleitung in `docs/arbeiten_mit_claude_code.md`.
- **Schritt 0 (Umstellung) umgesetzt am 15.11.2026**; Commit `Set up Claude Code workflow`, Push durch den Nutzer.
- **Außerhalb des Schrittplans:** Die lokale Änderung an `src/filter_region.py` vom 11.11.2026 (Kommentare) hat der Nutzer behalten; eigener Commit `Phase 1: tidy comments in filter_region`.
- **Grundsatzentscheidung vom 17.11.2026:** Der Hof-Sammler soll jede Länderseite der Common WWOOF Platform (CWP) erfassen können; die Länderseite wird in der Konfiguration gewählt. In alle Dokumente eingearbeitet (Abschnitt 6, 17.11.2026); neue Bedienungsanleitung `docs/07_bedienung.md`. Code ist nicht betroffen. Commit `Docs: support CWP country sites`.
- **Nächster Schritt:** Phase 2 nach dem angepassten Plan (Konfiguration mit Länderseiten-Datei, robots.txt, pytest, GitHub Actions, `docs/07_bedienung.md` Teil A); Claude Code schlägt den ersten Schritt nach `docs/03_programmierprojekt.md`, Phase 2, vor.

---

## Abgeschlossene Schrittpläne (aus 06, Abschnitte 4.1 und 4.2)

### 4.1 Schritt 0: Umstellung auf Claude Code

| Aufgabe | Status |
|---|---|
| Neue Dateien prüfen: `CLAUDE.md`, `.claude/settings.json`, `.vscode/settings.json`, `docs/` | erledigt (15.11.2026) |
| `.gitignore` ergänzen um `.claude/settings.local.json` und `CLAUDE.local.md` (persönliche Einstellungen gehören nicht ins Repository) | erledigt (15.11.2026) |
| `README.md`: Ordnertabelle um `docs/` ergänzen; Verweis auf `CLAUDE.md` und `docs/arbeiten_mit_claude_code.md`; fehlendes „außerhalb“ in der Einleitung ergänzt | erledigt (15.11.2026) |
| Commit `Set up Claude Code workflow`; der Nutzer pusht | erledigt (15.11.2026) |

### 4.2 Schrittplan Phase 1

Seit 15.11.2026 schreibt Claude Code den Code; der Nutzer prüft. Den Test mit Excel in Schritt 8 macht der Nutzer.

| Nr. | Schritt | Commit-Nachricht | Status |
|---|---|---|---|
| 1 | Repository vorbereiten: `src/`, `tests/fixtures/`, `src/__init__.py`, `.gitignore`, `README.md` | `Phase 1: add project structure and README` | erledigt |
| 2 | Erfundene Testdaten `tests/fixtures/farms_sample.csv` (5 Zeilen, 4 Höfe; DE-VA-003 doppelt zu DE-VA-001) | `Phase 1: add invented test farms` | erledigt |
| 3 | CSV lesen: `src/farm_table.py` (`read_farms` mit Spaltenprüfung), `src/filter_region.py` | `Phase 1: read farm table` | erledigt |
| 4 | Nach Region filtern (`filter_by_region`) und Ergebnis nach `out/` schreiben (`write_farms`) | `Phase 1: filter farms by region and write result` | erledigt |
| 5 | Felder umwandeln (Einzelheiten unten) | `Phase 1: parse list and number fields` | erledigt (15.11.2026) |
| 6 | Doppelungen über `profile_url` erkennen und mit Hof-Codes melden | `Phase 1: detect duplicate profile URLs` | erledigt (15.11.2026) |
| 7 | pandas: dieselbe Auswertung wie in den Schritten 4–6, Ergebnisse vergleichen | `Phase 1: explore farm table with pandas` | erledigt (15.11.2026) |
| 8 | CSV-Format-Test: Vergleichsskript (Claude Code); der Nutzer öffnet eine Kopie in `out/` mit Excel oder LibreOffice, ändert, speichert; das Skript vergleicht. Format festlegen und in `docs/03_programmierprojekt.md`, Abschnitt 5.5, eintragen | `Phase 1: compare tables after spreadsheet round trip` | erledigt (17.11.2026) |
| 9 | Abschluss: Verständnisfragen, README-Status, Tag `phase-1` | `Phase 1: complete` | erledigt (17.11.2026) |

**Einzelheiten zu Schritt 5** (Entwurf vom 08.11.2026, von Claude mit den Testdaten geprüft):

- In `src/farm_table.py`:
  - `split_list(value)`: teilt ein Listenfeld am Trennzeichen `LIST_SEPARATOR`; ein leeres Feld ergibt eine leere Liste (Falle: `"".split("|")` ergibt `['']`).
  - `parse_guestbook_count(farm)`: liefert `guestbook_count` als ganze Zahl ab 0; sonst `ValueError` mit Hof-Code und Länge, aber ohne den fehlerhaften Wert, z. B. `DE-VA-001: guestbook_count is not a whole number >= 0 (length 5)` (geändert am 15.11.2026, siehe Abschnitt 6).
- Neues Skript `src/farm_stats.py`: Höfe nach Gästebucheinträgen absteigend (stabile Sortierung), Anzahl der Höfe pro Lernkategorie; Ausgabe nur Hof-Codes, Zahlen und Kategorienamen.
- Erwartung mit der Testdatei: DE-SN-001 27, DE-VA-001 12, DE-VA-003 12, DE-SN-002 3, DE-VA-002 0; Tierhaltung 3 (wegen der Doppelung), Gemüsebau 3, Käseherstellung 2, übrige Kategorien 1.

**Phase 1 ist fertig, wenn:**
- `python -m src.filter_region` für beide Regionen läuft und die richtigen Zeilen nach `out/` schreibt,
- die Doppelung DE-VA-001/DE-VA-003 gemeldet wird,
- eine fehlende Datei und falsche Spalten zu einer klaren Meldung ohne Traceback führen,
- pandas dieselben Ergebnisse liefert,
- das CSV-Format nach dem Test feststeht und in `docs/03_programmierprojekt.md`, Abschnitt 5.5, eingetragen ist,
- der Nutzer den Code jeder Datei erklären kann,
- alles committet, gepusht und mit `phase-1` getaggt ist.

---

## Entscheidungen (aus 06, Abschnitt 6)

### 01.11.2026 – Q&A-Sitzung (Antworten des Nutzers)

| Frage | Thema | Entscheidung | Eingearbeitet in |
|---|---|---|---|
| 1 | Vorrang bei Zeitknappheit | Sammler zuerst; notfalls beginnt die Reise später | 00 Status, 01 Abschnitt 1, 03 Abschnitt 11 |
| 2 | Reisezeitraum | frühestens März, eher Juni 2027; Planungsgrundlage Juni | 00 Punkt 1, 01 Abschnitte 1 und 3, 03 Abschnitt 11 |
| 3 | Zeitbudget | ca. 4 Stunden pro Woche (aufgehoben am 15.11.2026) | 03 Abschnitt 11 |
| 4 | Automatisierte Zugriffe | laut Nutzer kein Verbot, solange kein Massenabruf in Sekunden stattfindet | 02 Abschnitte 1 und 3.1 |
| 5 | Vorkenntnisse | Python-Grundlagen, Terminal; HTML/CSS nur dem Namen nach, Interesse vorhanden | 03 Abschnitt 8 (Phase 3 um HTML/CSS erweitert) |
| 6 | Lernweise | Mischung; Claude schreibt auch größere Code-Teile; bei Fehlern zuerst Hinweis, Lösung nur auf Nachfrage (ersetzt am 15.11.2026) | 00 Regel 11, 03 Abschnitt 8 |
| 7 | Sprache im Code | komplett Englisch; deutsche Suchbegriffe bleiben deutsch | 00 Regel 10, 03 Abschnitt 5.5, 05 |
| 8 | Tests | pytest wird eingeführt (ab Phase 2) | 03 Abschnitte 5.5 und 8, 04 |
| 9 | Gerät | privater Windows-Laptop (Surface Pro 8) | 04 (auf Windows reduziert) |
| 10 | Zusammenarbeit | Code und Hofdaten so getrennt, dass Claude die Hoftabelle nicht sehen kann | 00 Regeln 7 und 8, 02 Abschnitt 2, 03 Abschnitt 5.1 |
| 11 | Versionsverwaltung | Git mit privatem GitHub-Repository; Anleitung als Teil von Phase 0 | 03 Phase 0, 04 Abschnitt 7 |
| 12 | Projektpflege | Claude pflegt den Fortschritt; Löschung nach der Reise übernimmt der Nutzer | 00, 02 Abschnitt 6, 03 Abschnitt 2 |
| 13 | WWOOF | mit WWOOF abgeklärt: Skript und Vorgehensweise passen; kein Massenabruf, kein direktes KI-Browsing. Mitgliedschaft aktiv. Hofsuche über die Landesseiten | 00 (Punkte 6 und 8 erledigt), 01 Abschnitt 7, 02 Abschnitte 1 und 3.1 |
| 14, 15 | Abgrenzung Voralpenland; Gesamtumfang und Tagesgrenze | noch nicht relevant | 00 Punkte 10 und 11 |
| 16 | Erfassung | nur einmalig, keine Aktualisierung | 03 Abschnitte 2 und 4 |
| 17 | Kalender | in die erste Version, wenn technisch gut möglich; Daten passend in die Tabelle | 01 Abschnitt 2, 03 Abschnitte 1, 5.3 und 8, 00 Punkt 12 |
| 18 | Gästebuch-Tenor, Notizen | Tenor gestrichen; Notizspalte bleibt | 00, 01, 02, 03 Abschnitte 5.3 und 6 |
| 19 | Hof in zwei Regionen | Code der ersten Erfassung; keine Redundanzen | 03 Abschnitte 2 und 5.2 |

### 01.11.2026 – Nachtrag (Antworten auf die offenen Fragen)

| Thema | Entscheidung | Eingearbeitet in |
|---|---|---|
| Bereinigte Beschreibungen an Claude | Dürfen an Claude gehen (von der Abklärung mit WWOOF umfasst) und sind ein wichtiger Teil der Bewertung und Priorisierung. Offener Punkt 5 erledigt; `include_description: true`, exportiert werden nur freigegebene Beschreibungen. Bereinigung (Phase 6 Teil B) gehört damit zum ersten Export. | 00, 02 Abschnitte 1, 2, 4 und 6, 03 Abschnitte 1, 2, 5.4, 6, 7, 8 und 11, 05 |
| Notizen im Export | Gehen an Claude | 03 Abschnitte 5.3 und 6 |
| Werkzeug | Claude Code lokal auf dem Laptop; Absicherung: Start nur im Code-Ordner, Read-Deny-Regel für `wwoof-data`, Modus mit Rückfrage, Test der Sperre | 00 Punkt 9 und Regel 8, 02 Abschnitte 2 und 6, 03 Abschnitte 5.1, 8 und 10, 04 Abschnitt 8 |

### 01.11.2026 – von Claude ergänzt (Einspruch jederzeit möglich)

| Ergänzung | Grund |
|---|---|
| Datenordner `wwoof-data` neben dem Repository `wwoof-planner`; Logs und Browser-Profil liegen ebenfalls im Datenordner | Umsetzung von Antwort 10; ein fehlerhaftes Log oder die Login-Sitzung gelangen so nicht zu Claude |
| Claude startet keine Skripte, die wwoof.de aufrufen oder echte Hofdaten verarbeiten; Läufe startet nur der Nutzer | Folgt aus „kein direktes KI-Browsing“; außerdem greift die Read-Deny-Regel laut Doku nicht bei Skripten, die Dateien selbst öffnen, und die Sandbox läuft nicht unter nativem Windows |
| Kein Auto-Modus in Claude Code | Im Auto-Modus gibt ein Klassifikator statt des Nutzers Befehle frei; jeder Befehl soll sichtbar bleiben |
| Ordner nicht in einem von OneDrive synchronisierten Ordner | Hofdaten sollen den Laptop nicht verlassen |
| Dateien und Spalten, die der Nutzer bearbeitet (`notes.csv`, Namensliste, Freigaben), überschreibt das Skript nie | Notizen und Freigaben gehen sonst bei erneuten Läufen verloren |
| Notizen liegen in einer eigenen Datei `notes.csv` | Trennung von Skript- und Nutzerdaten |
| Abgleich der Höfe über die normalisierte Profil-URL | Umsetzung von Antwort 19 (keine Redundanzen) |
| Zeitfenster im Format `JJJJ-MM-TT/JJJJ-MM-TT`, mit Abrufdatum; vor einer Anfrage aktuellen Kalender prüfen | Umsetzung von Antwort 17; wegen einmaliger Erfassung ist das eine Momentaufnahme |
| CSV mit `;` und UTF-8 mit BOM, Listen mit `\|` (in Phase 1 bestätigen) | Deutsches Excel öffnet die Dateien damit direkt korrekt |
| Taxonomie: englische Schlüssel, deutsche `label`-Texte; Repository-Name `wwoof-planner` | Umsetzung von Antwort 7; Labels sind nur Anzeigetexte |
| Laufzeitprüfungen mit eigenen Exceptions statt `assert` | `assert` lässt sich mit `python -O` abschalten |
| Ausweichlösung bei Zeitdruck: erster Export ohne Beschreibungen | Die Bereinigung liegt auf dem kritischen Pfad |
| E-Mail-Schutz bei GitHub (noreply-Adresse) | Die echte E-Mail-Adresse steht sonst in jedem Commit |

### 06.11.2026 – Abschluss Phase 0

| Thema | Ergebnis | Beleg und Hinweise |
|---|---|---|
| Phase 0 | Abgeschlossen; alle Checklistenpunkte laut Nutzer erfüllt | Der Nutzer hat die Punkte ausdrücklich bestätigt. Claude hat im Gespräch gesehen: Paketliste und `requirements.txt`, Chromium-Download, Git-Version, `git status`, Commit und Push (Repository `wwoof-planner`, Zweig `main`). Ohne Ausgabe bestätigt, also von Claude nicht gesehen: Prüfbefehle zu Python und Architektur, Interpreter in VS Code, noreply-Adresse im Commit, Sichtbarkeit „Private“, Regel in `/permissions` und Ergebnis des Sperrtests. |
| Sperre für `wwoof-data` | Read-Deny-Regel laut Nutzer eingerichtet und getestet (Leseversuch abgelehnt) | Empfohlene Ablage: Benutzer-Datei `~/.claude/settings.json`. Die tatsächliche Quelldatei zeigt `/permissions`. Siehe 04 Abschnitt 8. |
| Modus | „Manual“; kein Auto-Modus (geändert am 15.11.2026) | 04 Abschnitt 8 |
| Editor-Kontext | Das Panel zeigt die gerade geöffnete Datei als Kontext. Regel: Keine Datei aus `wwoof-data` im Editor öffnen, solange das Panel offen ist. GitHub Copilot ist ebenfalls vorhanden; sein Kontext wurde nicht geprüft (abgeschaltet seit 15.11.2026). | 04 Abschnitt 8 |

### 08.11.2026 – Start Phase 1

**Vorgaben des Nutzers**

| Thema | Entscheidung |
|---|---|
| Arbeitsweise | Der Nutzer kopiert den Code aus dem Chat, fügt ihn selbst in VS Code ein und will ihn verstehen (ersetzt am 15.11.2026) |
| Dokumentation | Fortschritte werden stets auf GitHub dokumentiert |

**Von Claude vorgeschlagen (Einspruch jederzeit möglich)**

| Vorschlag | Grund |
|---|---|
| Ein Commit pro Schritt (englische Nachricht mit Präfix „Phase 1: …“), danach `git push`. `README.md` (deutsch) mit Phasenstatus, aktualisiert am Ende jeder Phase. Git-Tag `phase-1` zum Abschluss | Fortschritt ist auf GitHub sichtbar; Einzelheiten stehen in dieser Datei |
| `src/` ist ein Paket (leere `src/__init__.py`); Start mit `python -m src.<modul>` aus dem Code-Ordner, nicht über den ▷-Knopf in VS Code | Absolute Importe `from src.… import …`. Der ▷-Knopf startet die Datei direkt und scheitert mit `ModuleNotFoundError: No module named 'src'` |
| Ausgaben aus Testläufen in `out/` im Code-Ordner; `.gitignore` ergänzt um `out/` und `~$*` (Excel-Sperrdateien) | Erfundene Daten gehören nicht in `wwoof-data`; Ausgaben sollen nicht ins Repository |
| Testdaten: Kontaktdaten nur aus reservierten Bereichen (`example.com`/`example.org`; Rufnummern für Medienproduktionen der Bundesnetzagentur), Personennamen als erkennbare Platzhalter (Mustermann, Doe), erfundene Orte; Fixture als UTF-8 mit BOM gespeichert | Keine Verwechslung mit echten Personen oder Höfen; einheitliches CSV-Format |
| Excel-/LibreOffice-Test nur an Kopien in `out/`, nie an der Fixture | Tabellenprogramme können Werte beim Speichern verändern |
| Programmausgaben in Phase 1 nur Hof-Codes und Zahlen | Gewöhnung an die Regel „Zusammenfassungen und Logs ohne Hofdaten“ (03 Abschnitt 4) |
| `test_playwright.py` löschen (oder per `.gitignore` ausschließen) | Einrichtungstest; gehört laut 04 Abschnitt 5 nicht ins Repository |

**Funde und Ergebnisse aus Schritt 3 und 4**

| Thema | Ergebnis | Folge |
|---|---|---|
| Groß- und Kleinschreibung bei Dateinamen | Ein Lauf mit `REGION = "Sachsen"` schrieb unter Windows nach `out\farms_Sachsen.csv`; im Explorer erschien nur `farms_sachsen.csv`. Windows unterscheidet Dateinamen nicht nach Groß- und Kleinschreibung; die Datei `farms_sachsen.csv` wurde dadurch überschrieben. Claude hatte Schritt 4 nur unter Linux getestet, wo beide Dateien getrennt bleiben. | Regionsschlüssel durchgehend klein schreiben; Dateinamen nicht aus Werten ableiten, die sich nur in der Schreibung unterscheiden (Vorschlag von Claude, Einspruch möglich) |
| Vergleich der Region | `farm["region"] == region` unterscheidet Groß- und Kleinschreibung; „Sachsen“ liefert 0 Höfe ohne Warnung | Vorgemerkt für Phase 2 (Abschnitt 4.3) |
| Aufruf `python -m src.filter_region.py` | Fehler, weil bei `-m` der Modulname ohne `.py` angegeben wird | Erklärt |
| `filter_by_region` | Die Funktion lieferte richtige Ergebnisse, benutzte aber die globale Konstante `REGION` statt des Parameters `region`. Mit anderem Argument hätte sie das falsche Ergebnis geliefert. | Vom Nutzer korrigiert, committet und gepusht |
| Verständnisfragen zu `farm_table.py` | Die Antworten auf Frage 1 (welche Zeile vertauschte Spalten bemerkt) und Frage 2 (zweizeilige Beschreibung) trafen nicht zu; Frage 3 blieb offen. Erklärung im Chat am 08.11.2026. | Wiederholung in Schritt 9 |

### 15.11.2026 – Umstellung auf Claude Code als Entwickler

**Vorgaben des Nutzers**

| Thema | Entscheidung |
|---|---|
| Arbeitsweise | Claude Code schreibt den Code. Der Nutzer schreibt nicht mehr selbst, sondern steuert, prüft und lässt sich erklären. Ziel: realistische Entwicklungsarbeit mit KI lernen und schneller vorankommen, ohne Claude Code „einfach alles machen“ zu lassen |
| Schrittgröße | immer nur der nächste Schritt; sinnvoll zusammenhängende Arbeit zusammen, nicht zu kleinteilig, im Zweifel etwas mehr auf einmal |
| Fragen | Fragen an Claude Code sind möglich, ohne dass sich etwas am Code ändert |
| Verständnis | Claude Code erklärt jede Änderung kurz, der Nutzer fragt nach; am Ende jeder Phase Verständnisfragen. Die Regel „bei Fehlern zuerst Hinweis“ entfällt |
| Rückfragen | Modus „Edit automatically“: Dateiänderungen im Code-Ordner ohne Rückfrage, Befehle mit Rückfrage |
| Git | Commits auf `main`; Claude Code schlägt die Nachricht vor und committet nach OK. Der Nutzer pflegt GitHub weiter und pusht selbst. Ab Phase 2 laufen die Tests auf GitHub (GitHub Actions) |
| Phasen | Alles wie geplant, auch der Rest von Phase 1 und Phase 3, nur von Claude Code geschrieben |
| Zeitplan | entfällt; der Nutzer arbeitet nach eigenem Tempo |
| Gültige Quelle | Das Repository ist die einzige gültige Quelle für Code, Regeln und Fortschritt. Das claude.ai-Projekt dient nur noch der Reiseplanung und später der Bewertung der Exporte |
| Dokumente im Repository | 00, 02–05 und der Fortschritt liegen in `docs/`; der Reiseplan (01) bleibt im claude.ai-Projekt |
| Copilot | wird für diesen Arbeitsbereich abgeschaltet |
| Grundsätze | Alle Daten- und Plattformregeln gelten unverändert |

**Von Claude ergänzt (Einspruch jederzeit möglich)**

| Ergänzung | Grund |
|---|---|
| `CLAUDE.md` mit Arbeitsweise und harten Regeln; dieser Fortschritt wird per Import immer mitgeladen | Claude Code liest `CLAUDE.md` zu Beginn jeder Sitzung |
| `.claude/settings.json`: Auto-Modus und Bypass gesperrt | Laut Doku startet die VS-Code-Erweiterung ab Claude Code v2.1.283 ohne eigene Einstellung im Auto-Modus. Dort gibt ein Klassifikator statt des Nutzers Befehle frei; das widerspricht „Befehle mit Rückfrage“ |
| `.claude/settings.json`: `git push` verboten (für Bash und PowerShell) | Der Nutzer pusht selbst. Unter Windows mit Git Bash würde eine reine Bash-Regel laut Doku das PowerShell-Werkzeug stillschweigend abschalten |
| `.claude/settings.json`: Dateiwerkzeuge lesen nichts außerhalb des Repositorys (`blockReadsOutsideWorkingDirectories`) | Zweite Sperre neben der Read-Deny-Regel für `wwoof-data` |
| `.claude/settings.json`: automatisches Gedächtnis aus (`autoMemoryEnabled: false`) | Der Stand soll nur im Repository stehen, sichtbar und auf GitHub nachvollziehbar |
| VS-Code-Benutzereinstellung `claudeCode.initialPermissionMode = acceptEdits` | Die Erweiterung liest den Startmodus laut Doku nicht aus der Projektdatei |
| `git add` nur mit Dateinamen, nie `git add .` | Verhindert, dass versehentlich Dateien ins Repository gelangen |
| Echte Läufe in einem eigenen PowerShell-Fenster außerhalb von VS Code | Ausgaben echter Läufe bleiben räumlich getrennt von der Sitzung mit Claude Code; ob die Erweiterung Terminalinhalte lesen kann, wurde nicht geprüft |

### 15.11.2026 – Schritt 0: Umstellung umgesetzt (Claude Code)

| Thema | Ergebnis | Hinweise |
|---|---|---|
| `.vscode/settings.json` | Kommt ins Repository (Vorschlag von Claude Code, vom Nutzer freigegeben). Inhalt nur `"chat.disableAIFeatures": true` | Setzt die Entscheidung „Copilot wird für diesen Arbeitsbereich abgeschaltet“ um und gilt auch bei einem neuen Klon. Persönliche VS-Code-Einstellungen gehören in die Benutzereinstellungen, nicht in diese Datei. Ob die Einstellung auch Inline-Vorschläge von Copilot vollständig abschaltet, wurde nicht geprüft. |
| `.gitignore` | Ergänzt um `.claude/settings.local.json` und `CLAUDE.local.md` | Persönliche Einstellungen von Claude Code bleiben lokal |
| Prüfung der neuen Dateien | `CLAUDE.md`, `.claude/settings.json`, `docs/arbeiten_mit_claude_code.md` gelesen; keine Widersprüche zum Fortschritt gefunden | Nicht geprüft: ob die Deny-Regel `git push *` auch ein `git push` ohne Argumente erfasst. Die Checkliste in `docs/arbeiten_mit_claude_code.md`, Abschnitt 12, hakt der Nutzer selbst ab. |
| `src/filter_region.py` | Lokale Änderung vom 11.11.2026 (Docstring zu Kommentar, Hinweis auf `config.yaml` entfernt) gehört nicht zu Schritt 0; der Nutzer hat sie behalten, eigener Commit `Phase 1: tidy comments in filter_region` | Empfehlung von Claude Code war: Docstring behalten (Python-Konvention, `help()` zeigt ihn an). Kann in Schritt 5 wieder aufgegriffen werden. |
| Commits ohne Mitautor | Vorgabe des Nutzers: Commits enthalten keine `Co-Authored-By`-Zeile und keinen Hinweis auf Claude als Mitautor. Eingetragen in `CLAUDE.md`, Abschnitt „Konventionen“ | Gilt auch, wenn das Werkzeug selbst eine solche Zeile vorschlägt |
| `.claude/settings.json`: Freigaben | Vom Nutzer ergänzt: `PowerShell(git status *)` und `PowerShell(git log *)` (nur lesende Befehle); Einrückung von Claude Code korrigiert | Nicht geprüft: ob die Muster auch die Befehle ohne Argumente erfassen |

### 15.11.2026 – Phase 1, Schritt 5: Felder umwandeln (Claude Code)

| Thema | Ergebnis | Hinweise |
|---|---|---|
| Fehlertext von `parse_guestbook_count` | Entscheidung des Nutzers: Die Meldung nennt Hof-Code und Länge des Werts, aber nicht den Wert selbst (abweichend vom Entwurf vom 08.11.2026) | Harte Regel 5 in `CLAUDE.md`: Fehlermeldungen nur mit Hof-Codes, Zahlen und Status. Schreibt der Sammler versehentlich Profiltext in das Feld, gelangt er so nicht in Ausgaben |
| Prüfung von `guestbook_count` | Nur ASCII-Ziffern zulässig (`isascii()` und `isdigit()`), dann `int()` (Vorschlag von Claude Code, Einspruch möglich) | `int()` allein nimmt auch `" 12"`, `"+12"`, `"1_000"`; `isdigit()` allein nimmt auch `"²"`. Mit erfundenen Werten geprüft |
| `src/farm_stats.py` | Ausgabe mit der Testdatei wie erwartet: DE-SN-001 27, DE-VA-001 12, DE-VA-003 12, DE-SN-002 3, DE-VA-002 0; Tierhaltung 3, Gemüsebau 3, Käseherstellung 2, übrige 1 | Gleich viele Einträge behalten die Reihenfolge aus der Datei (stabile Sortierung, auch mit `reverse=True`) |
| Prüfbefehle unter PowerShell 5.1 | `python -c` mit Anführungszeichen im Code scheitert, weil PowerShell 5.1 innere Anführungszeichen beim Weitergeben an Programme entfernt | Für Ad-hoc-Prüfungen ein kleines Skript verwenden; ab Phase 2 pytest |

### 15.11.2026 – Phase 1, Schritt 6: Doppelungen erkennen (Claude Code)

| Thema | Ergebnis | Hinweise |
|---|---|---|
| `find_duplicate_profile_urls` in `src/farm_table.py` | Gibt Gruppen von Hof-Codes mit gleicher `profile_url` zurück, in Dateireihenfolge; die URLs selbst nicht (Vorschlag von Claude Code, Einspruch möglich) | Harte Regel 5: Ausgaben ohne Hofdaten. Liegt in `farm_table.py`, damit der Sammler in Phase 5 die Prüfung wiederverwenden kann |
| Vergleich | Exakt, Zeichen für Zeichen | Die Normalisierung legen wir in Phase 4 fest (Vormerkung in 4.3) |
| `src/farm_stats.py` | Meldet `Duplicate profile URLs: 1 group` mit `DE-VA-001, DE-VA-003`; kein Abbruch | Abnahmekriterium der Phase („Doppelung wird gemeldet“) erfüllt. Mit erfundenen Listen geprüft: keine Doppelung, drei gleiche URLs, zwei getrennte Gruppen |

### 15.11.2026 – Phase 1, Schritt 7: Vergleich mit pandas (Claude Code)

| Thema | Ergebnis | Hinweise |
|---|---|---|
| `src/farm_pandas.py` | Berechnet Regionsfilter (für jede Region der Tabelle, mit Schreiben und Wiedereinlesen), Sortierung, Kategorien und Doppelungen mit csv und mit pandas und meldet je Auswertung `same` oder `DIFFERENT`; bei Abweichung Exit-Code 1. Mit der Testdatei: alles `same` | Abnahmekriterium der Phase („pandas liefert dieselben Ergebnisse“) erfüllt. Keine neuen Pakete (pandas 3.1.0 war installiert) |
| Falle: fehlende Werte | Ohne `keep_default_na=False` macht pandas aus leeren Feldern und Texten wie `NA` oder `null` einen fehlenden Wert (NaN); mit erfundenem Hofnamen `NA` nachgewiesen | Deshalb `dtype=str` und `keep_default_na=False` beim Einlesen |
| Falle: Sortierung | `sort_values` sortiert standardmäßig mit `quicksort`, nicht stabil. Bei 7 Zeilen blieb die Reihenfolge zufällig erhalten, bei 500 erfundenen Zeilen nicht | Deshalb `kind="stable"` |
| Falle: Zahlprüfung | `pd.to_numeric` wäre lockerer als `parse_guestbook_count`; stattdessen Prüfung mit regulärem Ausdruck `[0-9]+`. Mit `" 12"`, `"+12"`, `"²"`, `"-1"` und leerem Feld geprüft: beide Wege lehnen ab, Meldung nur mit Hof-Code | – |
| Kategorien | Vergleich ohne Reihenfolge, weil gleich häufige Kategorien in `most_common()` und `value_counts()` unterschiedlich geordnet sein können (für pandas 3.1 nicht geprüft) | – |
| Dateinamen | Unterscheiden sich Regionsnamen nur in der Schreibung, bricht das Skript mit klarer Meldung ab, statt Dateien zu überschreiben | Umsetzung der Vormerkung aus Schritt 4 (Windows) |
| Weitere Prüfung | Erfundene Tabelle mit leerem Kategorienfeld, `NA`/`null` in Textfeldern, mehrzeiliger Beschreibung mit `;` und Anführungszeichen, gleichen Gästebuchzahlen und drei Höfen mit gleicher URL: alles `same` | Prüfskript lag nur im Scratchpad; ab Phase 2 als pytest-Test |

### 17.11.2026 – Phase 1, Schritt 8: CSV-Format-Test mit Excel (Claude Code und Nutzer)

| Thema | Ergebnis | Hinweise |
|---|---|---|
| `src/table_roundtrip.py` | `prepare` kopiert die Fixture nach `out/roundtrip/`; `compare` prüft BOM, Kodierung, Trennzeichen und Zeilenenden auf Byte-Ebene und vergleicht dann jedes Feld mit `read_farms`. Erwartet ist genau eine Änderung (DE-SN-002, `guestbook_count` 3 → 4). Ausgabe nur Hof-Codes, Spalten, Längen und Status | Vorher mit simulierten Varianten geprüft: unverändert, erwartet, ANSI ohne BOM, Komma, umgewandeltes Datum, LF im mehrzeiligen Feld, fehlende Datei |
| Test des Nutzers | Excel, gespeichert als „CSV UTF-8 (durch Trennzeichen getrennt)“: BOM, UTF-8, `;`, Umlaute, mehrzeilige Beschreibung, `\|`-Listen und `available_windows` unverändert; erwartete Änderung erkannt | Der Gegentest mit „CSV (Trennzeichen-getrennt)“ entfällt, weil nur „CSV UTF-8“ zugelassen ist; ob jene Option ANSI ohne BOM speichert, ist daher nicht geprüft |
| Datum | Excel speichert `retrieved_on` als `TT.MM.JJJJ` statt `JJJJ-MM-TT` (alle 5 Zeilen) | Entscheidung des Nutzers: Dateien, die nur Skripte schreiben, in Excel nur ansehen, nie speichern; Datumsspalten in Nutzerdateien in beiden Formaten lesen (Vormerkung Phase 6 in 4.3). Eingetragen in 03, Abschnitt 5.5 |
| Zeilenumbruch am Dateiende | Die Fixture endet ohne Zeilenumbruch; Excel hängt einen an. `compare` zählt einen Zeilenumbruch am Dateiende deshalb nicht mehr als Abweichung | `csv.writer` schreibt ihn ebenfalls immer |
| CSV-Format | Festgelegt: `;`, UTF-8 mit BOM, Listen mit `\|`, CRLF; Speichern in Excel nur als „CSV UTF-8“ | Abnahmekriterium der Phase erfüllt; `CLAUDE.md` angepasst |

### 17.11.2026 – Phase 1, Schritt 9: Abschluss der Phase (Claude Code und Nutzer)

| Thema | Ergebnis | Belege und Hinweise |
|---|---|---|
| Abnahme | Alle technischen Kriterien aus 4.2 erfüllt | Von Claude Code mit der Fixture geprüft: `filter_region` voralpenland 3 Höfe; sachsen per Hilfsskript (Region ist Konstante im Modul) DE-SN-001, DE-SN-002; `farm_stats` meldet DE-VA-001/DE-VA-003; fehlende Datei und vertauschte Spalten mit klarer Meldung, Exit-Code 1, ohne Traceback; `farm_pandas` 7 × `same` |
| Verständnisfragen | Fünf Fragen gestellt (Spaltenprüfung und `None` in `read_farms`, mehrzeilige Felder und `newline=""`, Fehlermeldungen ohne Werte, `keep_default_na`/`kind="stable"` in pandas, Byte-Prüfung in `table_roundtrip`). Laut Nutzer beantwortet | Die Antworten hat Claude Code nicht gesehen; besprochen wurden sie nicht. Damit ist auch die Wiederholung der Fragen vom 08.11.2026 nur vom Nutzer bestätigt. Der Nutzer hat den Abschluss ausdrücklich beauftragt. Nachbesprechung jederzeit möglich |
| README | Phase 1 abgehakt; Startbefehle aller Skripte ergänzt | – |
| Beobachtung | Ein Skript außerhalb des Repository-Ordners findet `src` nur mit `PYTHONPATH` auf das Repository | Gleiche Ursache wie beim ▷-Knopf (08.11.2026) |

### 17.11.2026 – Grundsatzentscheidung: alle Länderseiten der CWP (Claude Code und Nutzer)

**Vorgaben des Nutzers**

| Thema | Entscheidung |
|---|---|
| Umfang | Der Hof-Sammler soll jede Länderseite der Common WWOOF Platform (CWP) erfassen können, z. B. Deutschland (wwoof.de) und Norwegen (wwoofnorway.org). Die Länderseite wird über die Konfiguration gewählt, nicht durch Codeänderungen. Eine gemeinsame Codebasis, keine Abstraktionsschicht für mehrere Plattformen. Länderseiten außerhalb der CWP (z. B. Irland, wwoof.ie): kein Code, keine Vorbereitung. Aufbau einfach und nachvollziehbar |
| Reihenfolge | Zuerst Deutschland. Weitere Länder nur über die Checkliste „Neue Länderseite“ (`docs/07_bedienung.md`, Teil C). Norwegen ist der nächste Kandidat |
| Gleicher Aufbau | Nicht belegt, dass alle CWP-Länderseiten technisch gleich aufgebaut sind; der Nutzer prüft das bei jeder neuen Länderseite. Bei Abweichung wird dann entschieden; kein Mechanismus auf Vorrat |
| Länderseiten-Datei | Eine Datei pro Länderseite: `sites/<site_id>.yaml`. site_id ist der Ländercode nach ISO 3166-1 Alpha-2 in Kleinbuchstaben, in Großbuchstaben zugleich der Länderteil des Hof-Codes. Inhalt (Entwurf; Phase 2 legt ihn fest): `base_url`, `languages`, `regions` (Schlüssel → Kürzel, Suchdefinition aus Phase 4), `learning_categories`. Nur Länderdaten; `config.py` lehnt unbekannte Schlüssel ab |
| `config.yaml` | Wählt nur `site` und `region`. `farm_code_prefix` entfällt; das Präfix wird aus site_id und Regionskürzel gebildet (eine Quelle) |
| Regionen | Regionsschlüssel klein und über alle Länderseiten eindeutig, weil die Spalte `region` in `farms.csv` kein Land enthält. Regionsschlüssel und -kürzel werden vor der robots-Prüfung festgelegt, die Suchdefinition erst nach der Länder-Prüfung (wie in Phase 4 für Deutschland). `config.py` lässt eine Region ohne Suchdefinition zu; der Sammler verlangt sie |
| YAML-Falle | `no` ohne Anführungszeichen wird als `false` gelesen (Norwegen: site_id `"no"`). Codes stehen immer in Anführungszeichen; `config.py` lehnt Werte, die keine Strings sind, mit klarer Meldung ab; ein Test deckt `site: no` ab |
| Plattformweit | Selektoren, URL-Normalisierung, Ablauf und Auslesen eines Profils gelten für die ganze CWP und stehen an genau einer Stelle im Code (festgelegt in Phase 4). Die normalisierte `profile_url` behält die Domain. Harte Grenzen, Pausen und Abbruchregeln gelten unverändert für jede Länderseite |
| Sprach- und Länderdaten | Suchbegriffe der Taxonomie, Verneinungen, Ignorierliste und Formulierungen der Bereinigung nach Sprache getrennt; angewendet nur die Sprachen der Länderseite des Hofs (Länderteil des Hof-Codes). Grund: „sau“ (norwegisch Schaf, deutsch Schwein). Muster für Postleitzahlen und Telefonnummern je Land. Fehlen Daten, brechen Stichworte, Bereinigung und Export für die betroffenen Höfe mit klarer Meldung ab. Umstellung der Taxonomie in Phase 6, Teil A; Kategorienschlüssel bleiben sprachunabhängig |
| Datenordner | `browser_profile/<site_id>/` je Länderseite (eigener Login, eigene Mitgliedschaft). `farms.csv` bleibt eine Tabelle für alle Länder, ohne Länderspalte. Erzeugte Dateinamen enthalten site_id und Regionsschlüssel in Kleinbuchstaben. Log-Einträge nennen die site_id, ohne Hofdaten |
| Regeln | Alle Regeln, die wwoof.de nennen, gelten für jede CWP-Länderseite und für api.wwoof.net; nichts wird gelockert. Tests nur mit erfundenen Länderseiten-Dateien unter `tests/fixtures/`. Außerhalb von `sites/` und `tests/fixtures/` keine Domain einer Länderseite im Code |
| Abklärung (Rückfrage vom 17.11.2026) | Die Abklärung vom 01.11.2026 war mit WWOOF Deutschland und mit dem Plattformbetreiber (FoWO/CWP). Sie gilt laut Nutzer für alle Länderseiten der CWP und wird einmal in `docs/02_regeln_und_rahmenbedingungen.md`, Abschnitt 1, festgehalten. Der im ersten Entwurf vorgesehene Schalter `agreement_confirmed` je Länderseiten-Datei **entfällt** |
| Vor dem ersten Lauf (Rückfrage vom 17.11.2026) | Checkliste je Länderseite: Mitgliedschaft → Regionsschlüssel und -kürzel → robots-Prüfung → Länder-Prüfung → Suchdefinition → Testlauf mit einem Profil → erster Lauf. Im Code bleibt die robots-Prüfung vor jedem Lauf (dazu der Abbruch ohne Suchdefinition); Mitgliedschaft, Länder-Prüfung und Testlauf sichert die Checkliste ab |
| Dokumentation | Neue Datei `docs/07_bedienung.md` (Teile A–E), wächst mit den Phasen; noch nicht gebaute Teile gekennzeichnet. Eine Phase ist erst fertig, wenn `docs/07` die Bedienung ihrer neuen Teile beschreibt (in `docs/03` und `CLAUDE.md`). README verweist auf `docs/07` |
| Phasen | Phase 1 ohne Codeänderung. Phase 2: `config.py` mit Länderseiten-Datei, robots-Prüfung mit `base_url`, `sites/de.yaml`, Tests mit erfundenen Länderseiten, `docs/07` Teil A. Phase 4 = erste Länder-Prüfung (Deutschland). Phase 5: Sammler mit `site` und `region`, Browser-Profil je Länderseite. Phase 6: Sprachdaten nach Sprache, Muster je Land. Phase 7: Selbsttest prüft Länderteil und Vorhandensein der Sprach- und Länderdaten. Offener Punkt 11 ergänzt um „je Länderseite oder insgesamt?“ |
| Unverändert | Datenregeln, Whitelist-Export, Hof-Code-Format `LAND-REGION-NNN`, harte Grenzen, Arbeitsweise aus `CLAUDE.md`, Code auf Englisch, Dokumentation auf Deutsch. Verweise auf `01_reiseplan.md` bleiben unverändert |

**Von Claude Code ergänzt (Einspruch möglich)**

| Ergänzung | Grund |
|---|---|
| `site` muss aus genau zwei Kleinbuchstaben bestehen | Unter Windows würde `site: "DE"` sonst `sites/de.yaml` laden, unter Linux (GitHub Actions) nicht |
| Regionskürzel innerhalb einer Länderseite eindeutig; Format legt Phase 2 fest | Sonst bekämen zwei Regionen dasselbe Präfix im Hof-Code |
| Doppelte YAML-Schlüssel ablehnen | PyYAML übernimmt nach bisherigem Kenntnisstand stillschweigend den letzten Wert; in Phase 2 per Test zu belegen |
| Eindeutigkeit der Regionsschlüssel: `config.py` liest die Regionsschlüssel aller Dateien in `sites/`; Tests zeigen auf einen Ordner unter `tests/fixtures/` | Nur so lässt sich die Eindeutigkeit über alle Länderseiten prüfen, ohne dass Tests echte Länderseiten-Dateien lesen |
| Erfundene Länderseiten in Tests mit Ländercodes, die ISO 3166-1 für Benutzerzwecke reserviert (z. B. `zz`, `xa`); robots-Tests ohne Netz | Keine Verwechslung mit echten Ländern; kein Zugriff auf echte Seiten |
| `learning_categories` darf bis zur Länder-Prüfung leer sein; verlangt wird die Liste erst vom Export-Selbsttest (Phase 7) | Die Liste entsteht wie die Suchdefinition erst in der Länder-Prüfung; der Sammler braucht sie nicht |
| Auch `exceptions` und `regex` der Taxonomie je Sprache; Normalisierung (ä→ae) für andere Sprachen eigens festlegen | Ausnahmen und Regeln wie „wir holen dich … ab“ sind sprachgebunden; Norwegisch hat æ, ø, å |
| Teil C, Schritt 2: beim Beitritt die Mitgliedsbedingungen der Landesorganisation lesen; bei Widerspruch anhalten und entscheiden | Bedingungen der Landesorganisationen können sich unterscheiden; kein zusätzliches Gate im Code |
| Regel für erfundene Rufnummern bei jeder weiteren Länderseite festlegen | Die Rufnummern der Bundesnetzagentur in harter Regel 7 gelten nur für Deutschland |
| Für Deutschland folgen die Sprach- und Länderdaten (Teil C, Schritt 8) erst in Phase 6, nach dem ersten Lauf | Der Sammler braucht sie nicht; erst Stichworte, Bereinigung und Export |
| Begriff „Landesseite“ in den Dokumenten durch „Länderseite“ ersetzt | Einheitliche Begriffe |
| Keine Änderung an `.claude/settings.json`, `.gitignore`, Code und Tests | Dort steht nichts wwoof.de-Spezifisches; `browser_profile/` in `.gitignore` deckt die Unterordner je Länderseite ab |

**Funde**

| Thema | Ergebnis |
|---|---|
| `docs/00_projekt_uebersicht.md` | Meldete noch „Phase 1 ist in Arbeit“; korrigiert |
| Ablage von Mustern und Formulierungen | Wo Muster für Postleitzahlen und Telefonnummern sowie Formulierungen der Bereinigung liegen, ist offen; Entscheidung in Phase 6 |
| Unverändert bewusst | `help.wwoof.net` und `docs.wwoof.net` (Hilfe- und Dokumentseiten, keine Länderseiten) bleiben wie bisher außerhalb der harten Regel 3. Historische Tabellen in diesem Dokument und die Checkliste von Phase 0 in `docs/04` bleiben unverändert |

### 17.11.2026 – Neuausrichtung: früh erkunden, Steckbrief statt Freigabe, schlanke Doku (Claude Code und Nutzer)

**Anlass:** Der Nutzer hat gefragt, ob das Vorgehen das Ziel erreicht: KI-frei und automatisiert Hofdaten erfassen und so verarbeiten, dass sie die Reiseplanung unterstützen. Claude Code hat sieben Schwächen benannt:
- a) Die Machbarkeit auf der Seite wird spät geklärt.
- b) Die Export-Spalten sind nie am Bedarf geprüft.
- c) Nutzen entsteht erst am Ende.
- d) Jede Beschreibung muss von Hand freigegeben werden.
- e) Die Doku ist doppelt geführt und kostet viele Tokens.
- f) Die Hofzahlen sind unbekannt.
- g) Der Rahmen der Abklärung muss gewahrt bleiben.

**Vorgaben des Nutzers**

| Thema | Entscheidung |
|---|---|
| Ziel | Die Schwächen a–g werden adressiert |
| Beschreibungen | Die Prüfung jeder Beschreibung von Hand ist kein Zielzustand. Stattdessen formt ein Skript jede Beschreibung **regelbasiert in einen Steckbrief** um: nur Schlüssel und Werte eines festen Schemas, kein Freitext. Die Skripte bleiben KI-frei |
| Doku | Informationen nicht doppelt über die Dokumente hinweg führen; unnötigen Aufwand und Token-Verbrauch vermeiden |
| Erkundung zuerst | Zuerst ein Testskript für den Abruf einer Länderseite, damit die Schritte ab Phase 2 auf echten Erkenntnissen aufbauen |
| Struktur-Skelett (Rückfrage) | Ein Erkundungsskript darf aus echten Seiten ein Struktur-Skelett erzeugen (alle Texte und Attributwerte durch Platzhalter ersetzt). Der Nutzer prüft es und teilt es danach mit Claude. Die gesicherten Seiten bleiben lokal |
| Übungsphase (Rückfrage) | Die bisherige Phase 3 (toscrape.com) wird ins Erkundungsskript integriert: Claude Code testet es dort, bevor der Nutzer es auf wwoof.de startet |
| Steckbrief (Rückfrage) | Nur Steckbrief, keine zusätzliche Bereinigung |

**Neuer Phasenplan** (Einzelheiten in `03_programmierprojekt.md`, Abschnitt 8):

| Phase | Inhalt |
|---|---|
| 2 | Länderseite erkunden: pytest und GitHub Actions, robots.txt, Länderseiten-Datei, Erkundungsskript mit Skelett, Lauf des Nutzers, erfundene Testseiten, Attrappe des Exports |
| 3 | Hof-Sammler |
| 4 | Erster Export (schlank) |
| 5 | Stichworte und Steckbrief |
| 6 | Vollständiger Export |

**Von Claude Code ergänzt (Einspruch möglich)**

| Ergänzung | Grund |
|---|---|
| Erkundungsskript: URLs gibt der Nutzer an und sie müssen mit der `base_url` beginnen; robots.txt-Prüfung; höchstens 5 Seiten pro Lauf, Pause 10–20 s; Abbruch bei Status ab 400; Ausgabe nur Zähler, Dateinamen, Status | Rahmen der Abklärung (normales Tempo, kein Massenabruf); keine Domain im Code |
| Gesicherte Seiten (`local/samples/`) bleiben lokal; mit ihnen prüft der Nutzer den Leser in Phase 3 offline | Weniger Seitenaufrufe auf der Länderseite |
| Seitenaufrufe der Erkundung sind keine Erfassung | Die Regel „jeder Hof nur einmal“ betrifft `farms.csv`; die frühere Phase 4 sah ebenfalls Erkundung auf Profilen vor |
| Attrappe: erfundener Export im claude.ai-Projekt testen (Phase 2) | Schwäche b: Export-Spalten und Steckbrief-Schema am Bedarf prüfen |
| Export in zwei Stufen: schlank direkt nach dem Sammler, vollständig nach Stichworten und Steckbrief | Schwäche c: Planung kann früher beginnen |
| Entfallen: `sanitize.py`, `sanitization.csv`, `name_list.txt`, Freigabe (`approved`, `reviewed_on`), Spalte `displayed_names`, Export-Spalte `description_sanitized`, Option `include_description`; neu: Spalte `facts` | Folge des Steckbriefs; weniger erfasste Personendaten. `displayed_names` wird in Phase 3 aus `FARM_COLUMNS` und der Fixture entfernt |
| Muster für Postleitzahlen und Telefonnummern je Land (Entscheidung vom 17.11.2026, CWP) entfallen. Für die Prüfung der Notizen genügen länderunabhängige Kontaktmuster (E-Mail, Web-Adresse, @-Namen, längere Ziffernfolgen) | Ohne exportierten Freitext werden sie nicht mehr gebraucht |
| Vormerkung „Datumsspalten in `sanitization.csv` in beiden Formaten lesen“ (Phase 1, Schritt 8) entfällt mit der Datei; die allgemeine Regel bleibt in 03, Abschnitt 5.5 | Folge des Steckbriefs |
| Nachschärfen von Taxonomie und Steckbrief per Stichprobe, nicht durch Lesen aller nicht abgedeckten Sätze | Schwäche d gilt auch hier |
| Doku: jedes Thema an einer Stelle (Tabelle in `00_projekt_uebersicht.md`); Verlauf aus 06 in diese Datei verschoben (06: 346 → ca. 60 Zeilen); „Arbeitsregeln für Claude“ und Status aus 00 entfernt; Teilen-Tabelle aus 03 nach 02; Kopfzeilen nur noch mit Datum | Schwäche e: 06 wird in jeder Sitzung geladen |
| Ein lokales Sprachmodell zum Umformulieren der Beschreibungen verworfen | Nicht KI-frei; frei formulierter Text wäre nicht sicher frei von Namen |
