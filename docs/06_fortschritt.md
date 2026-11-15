# Fortschritt

**Stand:** 15.11.2026 · gepflegt von Claude Code nach jedem Schritt (bis 15.11.2026 von Claude im claude.ai-Projekt)

---

## 1. Aktueller Stand

- **Phase 0 abgeschlossen (06.11.2026).**
- **Phase 1 in Arbeit.** Die Schritte 1–4 sind erledigt und gepusht: Projektstruktur und README, erfundene Testdaten, CSV lesen (`src/farm_table.py`), nach Region filtern und Ergebnis schreiben (`src/filter_region.py`). Schritt 5 wurde am 08.11.2026 als Anleitung ausgegeben, aber nicht umgesetzt; `src/farm_stats.py` gibt es noch nicht.
- **Umstellung am 15.11.2026:** Claude Code schreibt den Code schrittweise, der Nutzer prüft, lässt sich erklären und pusht selbst. Regeln in `CLAUDE.md`, Entscheidungen in Abschnitt 6 (15.11.2026), Anleitung in `docs/arbeiten_mit_claude_code.md`.
- **Schritt 0 (Umstellung) umgesetzt am 15.11.2026**; Commit `Set up Claude Code workflow`, Push durch den Nutzer.
- **Außerhalb des Schrittplans:** Die lokale Änderung an `src/filter_region.py` vom 11.11.2026 (Kommentare) hat der Nutzer behalten; eigener Commit `Phase 1: tidy comments in filter_region`.
- **Nächster Schritt:** Phase 1, Schritt 5.

---

## 2. Planungsgrundlagen

| Thema | Stand |
|---|---|
| Gerät | privater Windows-Laptop (Surface Pro 8) |
| Werkzeug | Claude Code in VS Code, Modus „Edit automatically“, Befehle mit Rückfrage |
| Vorkenntnisse | Python-Grundlagen, Terminal; HTML/CSS neu |
| Zeitplan | keiner; der Nutzer arbeitet nach eigenem Tempo (15.11.2026) |
| Reiseplanung | im claude.ai-Projekt (`01_reiseplan.md`); Planungsgrundlage für den Reisebeginn ist Juni 2027 |

---

## 3. Phasenstatus

| Phase | Inhalt | Status |
|---|---|---|
| 0 | Einrichtung, Git und GitHub, Ordnertrennung, Claude Code mit Sperre des Datenordners | erledigt (06.11.2026) |
| 1 | Python-Grundlagen, erfundene Testdaten, CSV-Format | in Arbeit (seit 08.11.2026) |
| 2 | Konfiguration, robots.txt, pytest, GitHub Actions | offen |
| 3 | HTML/CSS-Grundlagen, Playwright auf Übungsseiten | offen |
| 4 | wwoof.de erkunden (Gate erfüllt) | offen |
| 5 | Hof-Sammler bauen, erste Region erfassen | offen |
| 6 | Stichworte (Teil A), Bereinigung und Freigabe der Beschreibungen (Teil B) | offen |
| 7 | Export mit freigegebenen Beschreibungen | offen |

---

## 4. Nächste Schritte

### 4.1 Schritt 0: Umstellung auf Claude Code

| Aufgabe | Status |
|---|---|
| Neue Dateien prüfen: `CLAUDE.md`, `.claude/settings.json`, `.vscode/settings.json`, `docs/` | erledigt (15.11.2026) |
| `.gitignore` ergänzen um `.claude/settings.local.json` und `CLAUDE.local.md` (persönliche Einstellungen gehören nicht ins Repository) | erledigt (15.11.2026) |
| `README.md`: Ordnertabelle um `docs/` ergänzen; Verweis auf `CLAUDE.md` und `docs/arbeiten_mit_claude_code.md`; fehlendes „außerhalb“ in der Einleitung ergänzt | erledigt (15.11.2026) |
| Commit `Set up Claude Code workflow`; der Nutzer pusht | Commit nach OK des Nutzers |

### 4.2 Schrittplan Phase 1

Seit 15.11.2026 schreibt Claude Code den Code; der Nutzer prüft. Den Test mit Excel in Schritt 8 macht der Nutzer.

| Nr. | Schritt | Commit-Nachricht | Status |
|---|---|---|---|
| 1 | Repository vorbereiten: `src/`, `tests/fixtures/`, `src/__init__.py`, `.gitignore`, `README.md` | `Phase 1: add project structure and README` | erledigt |
| 2 | Erfundene Testdaten `tests/fixtures/farms_sample.csv` (5 Zeilen, 4 Höfe; DE-VA-003 doppelt zu DE-VA-001) | `Phase 1: add invented test farms` | erledigt |
| 3 | CSV lesen: `src/farm_table.py` (`read_farms` mit Spaltenprüfung), `src/filter_region.py` | `Phase 1: read farm table` | erledigt |
| 4 | Nach Region filtern (`filter_by_region`) und Ergebnis nach `out/` schreiben (`write_farms`) | `Phase 1: filter farms by region and write result` | erledigt |
| 5 | Felder umwandeln (Einzelheiten unten) | `Phase 1: parse list and number fields` | offen |
| 6 | Doppelungen über `profile_url` erkennen und mit Hof-Codes melden | `Phase 1: detect duplicate profile URLs` | offen |
| 7 | pandas: dieselbe Auswertung wie in den Schritten 4–6, Ergebnisse vergleichen | `Phase 1: explore farm table with pandas` | offen |
| 8 | CSV-Format-Test: Vergleichsskript (Claude Code); der Nutzer öffnet eine Kopie in `out/` mit Excel oder LibreOffice, ändert, speichert; das Skript vergleicht. Format festlegen und in `docs/03_programmierprojekt.md`, Abschnitt 5.5, eintragen | `Phase 1: compare tables after spreadsheet round trip` | offen |
| 9 | Abschluss: Verständnisfragen, README-Status, Tag `phase-1` | `Phase 1: complete` | offen |

**Einzelheiten zu Schritt 5** (Entwurf vom 08.11.2026, von Claude mit den Testdaten geprüft):

- In `src/farm_table.py`:
  - `split_list(value)`: teilt ein Listenfeld am Trennzeichen `LIST_SEPARATOR`; ein leeres Feld ergibt eine leere Liste (Falle: `"".split("|")` ergibt `['']`).
  - `parse_guestbook_count(farm)`: liefert `guestbook_count` als ganze Zahl ab 0; sonst `ValueError` mit Hof-Code im Text, z. B. `DE-VA-001: guestbook_count is not a whole number >= 0: 'zwölf'`.
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

### 4.3 Vormerkungen für spätere Phasen

| Phase | Punkt | Herkunft |
|---|---|---|
| 2 | Regionswerte aus `config.yaml` und Tabelle müssen exakt übereinstimmen (Groß- und Kleinschreibung); Warnung bei 0 Treffern erwägen | Schritt 4, 08.11.2026 |
| 2 | Tests laufen bei jedem Push automatisch auf GitHub (GitHub Actions) | Entscheidung vom 15.11.2026 |
| 4 | Prüfen, ob eine Lernkategorie der Plattform das Zeichen `\|` enthält; sonst würde `split_list` sie zerlegen | 15.11.2026 |
| 5 | Der Sammler löst einen Fehler aus, wenn ein Listenwert das Trennzeichen enthält, statt ihn falsch zu speichern | Vorschlag von Claude, 15.11.2026 (Einspruch möglich) |
| alle | Dateinamen nicht aus Werten ableiten, die sich nur in der Schreibung unterscheiden (Windows) | Schritt 4, 08.11.2026 |

---

## 5. Offene Fragen an den Nutzer

Derzeit keine. Die offenen Punkte zur Reise und zum Sammler stehen in `docs/00_projekt_uebersicht.md`.

---

## 6. Entscheidungsprotokoll

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
