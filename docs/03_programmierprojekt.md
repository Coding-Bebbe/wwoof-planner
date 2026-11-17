# Programmierprojekt: Hof-Sammler (Länderseiten der CWP, zuerst Deutschland)

**Stand:** 01.11.2026, angepasst am 15.11.2026 (Arbeitsweise mit Claude Code in Abschnitt 5.1 und 8, GitHub Actions in Phase 2, Zeitplanung in Abschnitt 11 entfällt) und am 17.11.2026 (alle Länderseiten der Common WWOOF Platform: Abschnitte 1, 2, 4–10)

---

## 1. Ziel

**Hauptziel:** KI-freie Python-Skripte, die in ausgewählten Regionen einer Länderseite der Common WWOOF Platform (CWP) Hofinformationen **in normalem Tempo** in eine **lokale Tabelle** schreiben. Zuerst Deutschland (wwoof.de; Start: bayerisches Voralpenland, Sachsen). Sie unterstützen die Reiseplanung (Ziel 1 des Projekts).

**Umfang (Entscheidung vom 17.11.2026):**
- Der Sammler kann jede Länderseite der CWP erfassen, z. B. Deutschland (wwoof.de) und Norwegen (wwoofnorway.org). Die Länderseite wird in der Konfiguration gewählt, nicht durch Codeänderungen (Abschnitt 5.4).
- Eine gemeinsame Codebasis, keine Abstraktionsschicht für mehrere Plattformen. Länderseiten außerhalb der CWP (z. B. Irland, wwoof.ie) gehören nicht zum Umfang: kein Code und keine Vorbereitung dafür.
- Weitere Länderseiten kommen nur über die Checkliste „Neue Länderseite hinzufügen“ dazu (`07_bedienung.md`, Teil C).
- Nicht belegt ist, dass alle Länderseiten der CWP technisch gleich aufgebaut sind. Das prüft der Nutzer bei jeder neuen Länderseite (Länder-Prüfung). Zeigt sich eine Abweichung, entscheiden wir dann; es gibt keinen Mechanismus auf Vorrat.
- Aufbau und Bedienung bleiben einfach und nachvollziehbar; die Bedienung beschreibt `07_bedienung.md`.

**Lokal erfasst (nur im Datenordner auf deinem Laptop):**
- Hof-Code (vergibt das Skript, siehe Abschnitt 5.2)
- Hofname
- Ort (ohne Adresse)
- Beschreibung (Originaltext)
- Lernmöglichkeiten (Kategorien auf der Website)
- Anzahl der Gästebucheinträge (nur die Zahl)
- freie Zeitfenster aus dem Kalender, falls technisch gut möglich (Klärung in Phase 4)
- auf dem Profil angezeigte Namen, ausschließlich für die automatische Bereinigung (Abschnitt 7)

**Von dir gepflegt:** eigene Notizen ohne Personenbezug (Abschnitt 6, Punkt 7).

**Weiterverarbeitung, ebenfalls lokal und KI-frei:**
- Stichwort-Kategorien aus der Beschreibung, ohne dass Informationen verloren gehen (Abschnitt 6)
- eine bereinigte Fassung der Beschreibung ohne Hof- und Personennamen, Kontakt- und Adressdaten, die du prüfst und freigibst (Abschnitt 7)

**Export für Claude (Whitelist):** Hof-Code, Ort, Region, Lernmöglichkeiten, Stichwort-Kategorien, Anzahl der Gästebucheinträge, Abdeckung, freie Zeitfenster, Notizen. Dazu kommt die bereinigte Beschreibung, sobald du sie freigegeben hast; sie ist ein wichtiger Teil der Bewertung und Priorisierung (offener Punkt 5 ist seit dem 01.11.2026 erledigt). **Hofnamen gehen nie an Claude.**

**Nebenziel:** Programmieren lernen (Ziel 2 des Projekts): Python vom eigenen Skript bis zur Browser-Automatisierung, dazu HTML- und CSS-Grundlagen, Tests mit pytest und Versionsverwaltung mit Git und GitHub. Seit dem 15.11.2026 mit Schwerpunkt auf der Entwicklung mit KI-Unterstützung: Aufgaben formulieren, Code von Claude Code prüfen und verstehen (Abschnitt 8).

---

## 2. Leitplanken (gelten immer)

1. **KI-frei:** Die Skripte rufen keine KI-Dienste auf.
2. **Nur einzelne Regionen:** eine Länderseite und eine Region pro Lauf, nie die gesamte Hostliste einer Länderseite.
3. **Obergrenze pro Lauf:** Vorschlag 30 Profile. Eine harte Grenze von 50 ist fest im Code verankert und lässt sich nicht per Konfiguration überschreiben. Grenzen, Pausen und Abbruchregeln gelten unverändert für jede Länderseite. Gesamtumfang und Tagesgrenze legen wir vor Phase 5 fest, auch ob sie je Länderseite oder insgesamt gelten (offener Punkt 11 in `00_projekt_uebersicht.md`).
4. **Normales Tempo, kein Massenabruf:** eine Seite nach der anderen, keine parallelen Abrufe, zufällige Pause zwischen zwei Seitenaufrufen (Vorschlag 10–20 Sekunden). Ein Lauf mit 30 Profilen dauert damit grob 6–13 Minuten (Pausen plus Ladezeiten). Jeder zusätzliche Aufruf pro Profil (z. B. für Gästebuch oder Kalender) verlängert den Lauf entsprechend, bei zwei Zusatzaufrufen auf etwa das Dreifache.
5. **Echter Browser, eigene Sitzung:** Playwright steuert einen echten Browser. Du loggst dich darin einmal je Länderseite **manuell** ein; jede Länderseite hat ein eigenes Browser-Profil. Dein Passwort steht nie im Code. Keine direkten Aufrufe der Plattform-Schnittstelle (api.wwoof.net), kein Umgehen von Schutzmaßnahmen.
6. **Läufe startest nur du:** Jeden Lauf gegen eine Länderseite startest du selbst in deinem Terminal. Claude startet weder den Sammler noch andere Skripte, die eine Länderseite oder api.wwoof.net aufrufen (Absprache mit WWOOF: kein direktes KI-Browsing).
7. **robots.txt:** Die robots.txt der gewählten Länderseite wird vor jedem Lauf geprüft. Bei einem Verbot bricht das Skript ab.
8. **Abbruch statt Hartnäckigkeit:** Bei Captcha, Zugriffsverweigerung, Login-Aufforderung oder unerwarteten Fehlern beendet sich das Skript sauber, statt es erneut zu versuchen.
9. **Daten bleiben lokal und getrennt:** Alles, was ein Lauf erzeugt oder liest (Hoftabelle, Notizen, Namensliste, Berichte, Logs, Browser-Profile), liegt im Datenordner `wwoof-data/` außerhalb des Code-Repositorys (Abschnitt 5.1). Claude hat darauf keinen Zugriff. An Claude geht nur der Export mit den freigegebenen Feldern (Whitelist), und den lädst du selbst hoch.
10. **Einmalige Erfassung, keine Redundanzen:** Jeder Hof wird nur einmal abgerufen und steht genau einmal in `farms.csv`, mit genau einem Hof-Code. Erneute Abrufe zur Aktualisierung gibt es nicht. Andere Dateien verweisen nur über den Hof-Code auf einen Hof und wiederholen keine Felder aus `farms.csv`.
11. **Gästebuch nur als Zahl:** Das Skript liest nur die Anzahl der Einträge. Gästebuchtexte werden weder gespeichert noch exportiert.
12. **Löschung nach der Reise:** Alle Hofdaten werden nach der Reise gelöscht. Darum kümmerst du dich, auch um die Exporte, die du in das Claude-Projekt hochgeladen hast.
13. **Gates:**
    - Abklärung mit WWOOF: erledigt (offener Punkt 6, laut Nutzer am 01.11.2026). Sie gilt laut Nutzer für alle Länderseiten der CWP (`02_regeln_und_rahmenbedingungen.md`, Abschnitt 1).
    - Vor dem ersten Lauf gegen eine Länderseite ist die Checkliste in `07_bedienung.md`, Teil C, erledigt: Mitgliedschaft → Regionsschlüssel und -kürzel → robots.txt-Prüfung → Länder-Prüfung → Suchdefinition je Region → Testlauf mit einem Profil. Für Deutschland ist Phase 4 die Länder-Prüfung.
    - Im Code stehen davon nur zwei Prüfungen: die robots.txt-Prüfung vor jedem Lauf (offener Punkt 7, Phase 2) und der Abbruch des Sammlers, wenn die gewählte Region keine Suchdefinition hat (Phase 5). Den Rest sichert die Checkliste.
    - Vor dem Export einer Beschreibung: Du hast sie geprüft und freigegeben (Abschnitt 7).
14. **Länderdaten an einer Stelle:** Was eine Länderseite ausmacht, steht in `sites/<site_id>.yaml` (Abschnitt 5.4). Außerhalb von `sites/` und `tests/fixtures/` steht keine Domain einer Länderseite im Code. Tests verwenden nur erfundene Länderseiten-Dateien.

---

## 3. Warum Playwright?

Der Seitenquelltext von wwoof.de enthält die Konfiguration einer JavaScript-Anwendung (Ember), die ihre Inhalte von einer Schnittstelle (api.wwoof.net) nachlädt (geprüft am 25.10.2026). Ein einfacher HTTP-Abruf, etwa mit `requests`, sieht diese Inhalte deshalb nicht zuverlässig. Playwright öffnet die Seiten wie ein normaler Browser, und das Skript liest, was auch du auf dem Bildschirm sehen würdest. Wie die Seiten genau aufgebaut sind, klärst du in Phase 4. Ob andere Länderseiten der CWP gleich aufgebaut sind, ist nicht belegt; das klärt die Länder-Prüfung (`07_bedienung.md`, Teil C).

---

## 4. Ablauf eines Sammellaufs

1. Du startest den Lauf in deinem Terminal. Länderseite und Region stehen in `config.yaml`.
2. Konfiguration und Länderseiten-Datei `sites/<site_id>.yaml` laden und prüfen, Grenzwerte prüfen. Bei unzulässigen Werten bricht das Skript ab. Zusätzlich bricht der Sammler ab, wenn die gewählte Region noch keine Suchdefinition hat (für `config.py` allein ist das zulässig, Abschnitt 5.4).
3. robots.txt der Länderseite prüfen (Adresse aus `base_url`).
4. Browser mit dem persistenten Profil der Länderseite öffnen (`browser_profile/<site_id>/` im Datenordner). Bist du nicht eingeloggt, meldet das Skript das, du loggst dich von Hand ein und bestätigst mit Enter.
5. Suche für die Region aufrufen und die Liste der Profil-Links im Datenordner speichern. Der Dateiname enthält site_id und Regionsschlüssel, nur in Kleinbuchstaben.
6. Bereits erfasste Profile überspringen. Der Abgleich läuft über die normalisierte Profil-URL mit Domain (Abschnitt 5.2) und gilt auch für Höfe, die schon in einer anderen Region oder über eine andere Länderseite erfasst wurden. So wird kein Hof doppelt abgerufen oder gespeichert, und ein abgebrochener Lauf lässt sich später fortsetzen.
7. Für jedes neue Profil, bis zur Obergrenze:
   - Seite öffnen und warten, bis der Inhalt geladen ist.
   - Hof-Code vergeben (aus site_id und Regionskürzel, Abschnitt 5.2).
   - Hofname, Ort, Beschreibung, Lernmöglichkeiten, angezeigte Namen, Anzahl der Gästebucheinträge und, falls aktiviert, die freien Zeitfenster lesen. Muss dafür ein eigener Reiter oder eine eigene Seite geöffnet werden, zählt das als eigener Seitenaufruf mit Pause.
   - Eine Zeile in `farms.csv` schreiben.
   - Zufällige Pause.
8. Bei etwas Ungewöhnlichem (Captcha, Zugriffsverweigerung, Login-Aufforderung) sofort sauber beenden und einen Log-Eintrag schreiben. Log-Einträge nennen die site_id, aber keine Hofdaten.
9. Zusammenfassung ausgeben (Länderseite, Region, neu erfasst, übersprungen, Fehler), **ohne Hofdaten**.

Selektoren, URL-Normalisierung, Ablauf und das Auslesen eines Profils gelten für die ganze CWP und stehen an genau einer Stelle im Code; welche, legen wir in Phase 4 fest. Was je Länderseite verschieden ist, steht in der Länderseiten-Datei.

---

## 5. Projektstruktur und Daten

### 5.1 Ordner

Code und Daten liegen in zwei getrennten Ordnern nebeneinander, z. B. unter `C:\Users\<Benutzer>\Projekte\`. Beide Ordner liegen **nicht** in einem von OneDrive synchronisierten Ordner, damit die Hofdaten den Laptop nicht verlassen.

```
Projekte\
├── wwoof-planner\             Code-Repository (Git, privates GitHub-Repository)
│   ├── .venv\                 virtuelle Umgebung (nicht in Git)
│   ├── .claude\settings.json  Projekteinstellungen für Claude Code
│   ├── .gitignore
│   ├── CLAUDE.md              Arbeitsweise und Regeln für Claude Code
│   ├── config.yaml            Länderseite, Region, Grenzwerte, Pausen, Pfad zum Datenordner, Optionen
│   ├── taxonomy.yaml          Stichwort-Kategorien, Suchbegriffe nach Sprache (aus 05_stichwort_taxonomie.md)
│   ├── requirements.txt       Paketversionen
│   ├── docs\                  Projektdokumente (00, 02–07, Anleitung)
│   ├── sites\                 eine Datei pro Länderseite, z. B. de.yaml (Abschnitt 5.4)
│   ├── src\
│   │   ├── config.py          Konfiguration und Länderseiten-Datei laden und prüfen
│   │   ├── robots_check.py    robots.txt prüfen
│   │   ├── session.py         Browser mit persistentem Profil starten
│   │   ├── region_list.py     Suchergebnisse einer Region lesen
│   │   ├── profile_reader.py  ein Profil lesen, Felder extrahieren
│   │   ├── collector.py       Steuerung: Grenzen, Pausen, Hof-Codes, Abgleich, Fortsetzen, Logging
│   │   ├── tagging.py         Taxonomie anwenden, Abdeckungsbericht
│   │   ├── sanitize.py        Beschreibung bereinigen, Sätze markieren
│   │   └── export.py          Whitelist-Export für Claude mit Selbsttest
│   └── tests\                 pytest-Tests, nur mit erfundenen Höfen
│       └── fixtures\          erfundene Testdaten, auch erfundene Länderseiten-Dateien
│
└── wwoof-data\                Datenordner (kein Git, kein Zugriff für Claude)
    ├── browser_profile\
    │   └── <site_id>\         Login-Sitzung je Länderseite, z. B. de\
    ├── local\                 Hoftabelle (alle Länder), Berichte, Notizen, Namensliste, Profil-Link-Listen
    ├── export\                Export für Claude (lädst du selbst hoch)
    └── logs\                  Protokolle ohne Hofdaten
```

- Den Pfad zum Datenordner liest der Code aus `config.yaml` (`data_dir`); im Code steht kein Pfad zu echten Daten. Die Unterordner legt das Skript bei Bedarf selbst an.
- **Zusammenarbeit mit Claude Code (Entscheidung vom 01.11.2026):** Claude Code läuft lokal und wird immer im Ordner `wwoof-planner\` gestartet, nie in `wwoof-data\` oder im gemeinsamen Oberordner `Projekte\`.
- **Absicherung** (Einrichtung in Phase 0, `04_technische_voraussetzungen.md`, Abschnitt 8):
  - Eine Read-Deny-Regel sperrt `wwoof-data\` für Claudes Dateiwerkzeuge und für Lesebefehle, die Claude Code erkennt (z. B. `cat`).
  - Seit 15.11.2026 zusätzlich: Die Projekteinstellungen `.claude/settings.json` sperren Auto-Modus und Bypass, verbieten `git push` und lassen Claudes Dateiwerkzeuge nichts außerhalb des Repositorys lesen.
  - Claude Code läuft im Modus „Edit automatically“ (seit 15.11.2026): Dateien im Code-Ordner ändert es ohne Rückfrage, vor Befehlen fragt es nach.
  - Grenze laut Doku: Die Deny-Regel greift nicht bei Skripten, die Dateien selbst öffnen (z. B. ein Python-Skript), und die Sandbox, die das auf Betriebssystemebene verhindern würde, läuft nicht unter nativem Windows. Deshalb startet Claude keine Skripte, die eine Länderseite aufrufen oder echte Daten verarbeiten (Leitplanke 6, Abschnitt 10), und du prüfst jeden Befehl, bevor du ihn freigibst.
- **Logs** enthalten keine Hofdaten, liegen aber trotzdem im Datenordner: Schreibt ein Fehler doch Hofdaten ins Log, gelangen sie so nicht zu Claude. Log-Auszüge teilst du nach eigener Prüfung.
- **Browser-Profile:** je Länderseite ein eigener Unterordner `browser_profile/<site_id>/` mit eigenem Login; für jede Länderseite ist eine eigene Mitgliedschaft nötig. Jedes Profil enthält eine Login-Sitzung und ist damit so schutzbedürftig wie ein Passwort.
- **Dateinamen**, die aus site_id oder Regionsschlüssel entstehen (z. B. Link-Listen), sind nur klein geschrieben, weil Windows bei Dateinamen nicht zwischen Groß- und Kleinschreibung unterscheidet.

### 5.2 Hof-Code

- **Format:** `LAND-REGION-NNN`, z. B. `DE-VA-001` für das Voralpenland und `DE-SN-001` für Sachsen.
  - `LAND` ist die site_id der Länderseite in Großbuchstaben (Ländercode nach ISO 3166-1 Alpha-2, z. B. `de` → `DE`, `no` → `NO`).
  - `REGION` ist das Regionskürzel aus der Länderseiten-Datei (Abschnitt 5.4). Das Präfix wird aus diesen beiden Werten gebildet; es gibt dafür keine eigene Einstellung (eine Quelle).
- Das Skript vergibt den Code beim ersten Erfassen fortlaufend. Er bleibt dem Hof dauerhaft zugeordnet.
- **Eindeutigkeit:** Ein Hof bekommt genau einen Code. Die Zuordnung erfolgt über die **normalisierte Profil-URL** (`profile_url`), die nur lokal gespeichert wird. „Normalisiert“ heißt: ohne Zusätze wie Abfrageparameter, sodass derselbe Hof immer dieselbe URL hat. Die normalisierte URL **behält die Domain**, damit der Abgleich auch über Länderseiten hinweg eindeutig bleibt. Wie die URLs aufgebaut sind (z. B. mit einer Profil-ID), klärst du in Phase 4.
- **Überschneidung zweier Regionen (Entscheidung vom 01.11.2026):** Taucht ein Hof in einer weiteren Region auf, behält er den Code und die Region aus der ersten Erfassung und wird nicht erneut abgerufen.
- **Kein Bezug zum Namen:** keine Initialen, keine Abkürzungen des Hofnamens.
- Die Zuordnung Hof-Code ↔ Hofname steht nur in `local/farms.csv`. Dort schlägst du nach, welchen Hof du anschreiben musst.
- **Land:** Das Land eines Hofs steckt im Länderteil des Hof-Codes. `farms.csv` bleibt eine Tabelle für alle Länder, ohne zusätzliche Spalte.

### 5.3 Dateien

Alle Daten liegen als CSV-Dateien vor. Sie lassen sich in Excel oder LibreOffice öffnen, und es ist eine **Liste**, keine Datenbank (passend zur Absprache „private Liste“).

**Grundsatz:** Dateien und Spalten, die du von Hand bearbeitest (`notes.csv`, `name_list.txt`, Freigaben und Korrekturen in `sanitization.csv`), überschreibt das Skript nie.

**`local/farms.csv`** (nur lokal; schreibt nur der Sammler, Zeilen werden nur angehängt; eine Tabelle für alle Länderseiten)

| Spalte | Inhalt |
|---|---|
| `farm_code` | Hof-Code, z. B. DE-VA-001; eindeutig; der Länderteil zeigt die Länderseite |
| `profile_url` | normalisiert, mit Domain; eindeutig; für Abgleich, Fortsetzen und Wiederfinden |
| `farm_name` | Hofname |
| `location` | nur Gemeinde bzw. Ort; zeigt das Profil mehr an, wird nur der Ort gespeichert |
| `region` | Regionsschlüssel der ersten Erfassung, z. B. voralpenland; klein geschrieben und über alle Länderseiten eindeutig, weil die Spalte kein Land enthält |
| `description` | Originaltext |
| `learning_categories` | Lernkategorien der Länderseite, getrennt durch `\|` |
| `guestbook_count` | ganze Zahl ab 0 |
| `available_windows` | freie Zeitfenster im Format `JJJJ-MM-TT/JJJJ-MM-TT`, mehrere getrennt durch `\|`; leer, wenn nicht erfasst. Was gespeichert wird, wenn der Kalender keine freien Fenster zeigt, legen wir nach Phase 4 fest. |
| `displayed_names` | auf dem Profil angezeigte Namen, nur für die Bereinigung |
| `retrieved_on` | Abrufdatum; wichtig, weil die Zeitfenster eine Momentaufnahme sind |

**`local/notes.csv`** (nur lokal; pflegst nur du)

| Spalte | Inhalt |
|---|---|
| `farm_code` | |
| `notes` | eigene Notizen in eigenen Worten, ohne Personenbezug (z. B. „großer Gemüsegarten“, „Käserei als Hauptbetrieb“) |

**`local/keyword_report.csv`** (nur lokal; schreibt das Skript)

| Spalte | Inhalt |
|---|---|
| `farm_code` | |
| `categories` | gefundene Kategorien (Schlüssel aus der Taxonomie) |
| `coverage_percent` | Anteil der Sätze mit mindestens einer relevanten Kategorie |
| `uncovered_sentences` | zur Sichtung durch dich |
| `review_flags` | z. B. mögliche Verneinung, siehe Abschnitt 6 |

**`local/sanitization.csv`** (nur lokal; schreibt das Skript, Freigabe und Korrekturen machst du)

| Spalte | Inhalt |
|---|---|
| `farm_code` | |
| `description_sanitized` | Text mit Platzhaltern `[FARM]`, `[PERSON]`, `[CONTACT]`, `[ADDRESS]` |
| `flagged_sentences` | Sätze mit möglichem Personenbezug, zur Prüfung durch dich |
| `approved` | `yes` oder leer; trägst nur du ein |
| `reviewed_on` | Datum deiner Prüfung |

**`local/name_list.txt`** (nur lokal; pflegst nur du): Namen, die du bei der Prüfung entdeckst und die künftig automatisch ersetzt werden sollen, einer pro Zeile.

**Profil-Link-Listen** (nur lokal; schreibt der Sammler): eine Datei je Länderseite und Region; der Name enthält site_id und Regionsschlüssel in Kleinbuchstaben, z. B. `links_de_voralpenland.csv`. Den genauen Namen legen wir in Phase 5 fest.

**`export/export_for_claude.csv`** (geht an Claude; lädst du selbst hoch)

| Spalte | Inhalt |
|---|---|
| `farm_code` | |
| `location`, `region` | |
| `learning_categories` | |
| `categories` | |
| `guestbook_count` | |
| `coverage_percent` | |
| `available_windows` | |
| `notes` | aus `notes.csv` |
| `description_sanitized` | nur wenn `include_description: true` **und** `approved = yes`, sonst leer |

### 5.4 Konfiguration (Entwurf)

Zwei Arten von Dateien (Entscheidung vom 17.11.2026; Phase 2 legt das Format fest):

- **`config.yaml`** wählt die Länderseite (`site`) und die Region (`region`) und enthält Grenzwerte, Pausen, Pfade und Optionen. Das frühere `farm_code_prefix` entfällt; das Präfix des Hof-Codes wird aus site_id und Regionskürzel gebildet (Abschnitt 5.2).
- **`sites/<site_id>.yaml`**, eine Datei pro Länderseite, z. B. `sites/de.yaml`. Sie enthält **nur Länderdaten**, keine Grenzwerte, Pausen oder Pfade. `config.py` lehnt unbekannte Schlüssel ab.

```yaml
# config.yaml - draft
site: "de"                          # site_id; always in quotes: unquoted no would be read as false
region: "voralpenland"              # region key from sites/<site>.yaml
max_profiles_per_run: 30            # hard limit in code: 50
pause_seconds_min: 10
pause_seconds_max: 20
data_dir: "../wwoof-data"           # data folder outside the repository
availability:
  enabled: true                     # keep only if the calendar is readable (phase 4)
  date_from: "2027-03-01"           # earliest possible travel start
  date_to: "2027-10-31"             # adjust once the travel period is fixed
export:
  include_description: true         # exports only descriptions marked approved = yes
```

```yaml
# sites/de.yaml - draft; phase 2 fixes the format, phase 4 adds search definitions and categories
base_url: "https://wwoof.de"        # exact form is checked by the user in phase 2
languages: ["de", "en"]             # language codes of the descriptions
regions:
  voralpenland:                     # region key: lower case, unique across all sites
    code: "VA"                      # region code in the farm code, unique within this site
    # search: defined after the country check (phase 4)
  sachsen:
    code: "SN"
learning_categories: []             # list from the country check (phase 4)
```

**Was `config.py` prüft** (Phase 2):
- Codes und Schlüssel sind Strings. Ein `no` ohne Anführungszeichen (Norwegen: site_id `"no"`) liest YAML als `false`; das wird mit klarer Meldung abgelehnt. Codes stehen deshalb immer in Anführungszeichen.
- `site` besteht aus genau zwei Kleinbuchstaben, und `sites/<site>.yaml` existiert (Vorschlag von Claude Code, Einspruch möglich: Unter Windows würde `"DE"` sonst `de.yaml` laden, unter Linux in GitHub Actions nicht).
- Nur bekannte Schlüssel, in beiden Dateien; doppelte Schlüssel werden abgelehnt (Vorschlag von Claude Code: PyYAML übernimmt nach bisherigem Kenntnisstand stillschweigend den letzten Wert; in Phase 2 per Test zu belegen).
- Die gewählte Region ist in der Länderseiten-Datei vorhanden.
- Regionsschlüssel sind klein und über alle Länderseiten eindeutig; dazu liest `config.py` die Regionsschlüssel aller Dateien in `sites/`. Regionskürzel sind innerhalb einer Länderseite eindeutig (Vorschlag von Claude Code).
- `base_url` beginnt mit `https://`.
- **Fehlende Suchdefinition ist zulässig:** Eine Region mit Schlüssel und Kürzel, aber ohne Suchdefinition ist gültig. Das ist der Zustand zwischen dem Festlegen der Regionen und der Länder-Prüfung (`07_bedienung.md`, Teil C). Erst der Sammler verlangt eine Suchdefinition (Phase 5).
- `learning_categories` darf bis zur Länder-Prüfung leer sein; verlangt wird die Liste erst vom Export-Selbsttest (Phase 7) (Vorschlag von Claude Code, Einspruch möglich).

### 5.5 Konventionen

- **Sprache:** Der Code ist komplett englisch: Bezeichner, Kommentare, Datei- und Ordnernamen, Spaltennamen, Konfigurationsschlüssel und Programmausgaben. Ausnahme sind Suchbegriffe in den Sprachen der Länderseiten (Taxonomie, Verneinungen, Formulierungen in der Bereinigung); sie werden nach Sprache getrennt (Abschnitte 6 und 7). Die `label`-Texte in `taxonomy.yaml` bleiben deutsch, weil sie nur Anzeigetexte für dich sind. Die Dokumentation bleibt deutsch.
- **YAML:** Codes (site_id, Sprachcodes, Regionskürzel) stehen immer in Anführungszeichen.
- **Dateinamen** aus site_id und Regionsschlüssel nur in Kleinbuchstaben.
- **CSV-Format (festgelegt am 17.11.2026 nach dem Test in Phase 1, Schritt 8):** Trennzeichen `;` und Kodierung UTF-8 mit BOM (`utf-8-sig`). Mit diesen Einstellungen öffnet ein deutsches Excel die Dateien per Doppelklick mit richtigen Spalten und Umlauten. Listen innerhalb eines Feldes werden mit `|` getrennt. Zeilenenden CRLF.
  - **Speichern in Excel nur als „CSV UTF-8 (durch Trennzeichen getrennt)“.** Damit blieben im Test BOM, Kodierung, Trennzeichen, Umlaute, mehrzeilige Felder und `|`-Listen erhalten.
  - **Excel wandelt Datumswerte um:** Aus `2026-11-08` wird beim Speichern `08.11.2026`. Deshalb:
    - Dateien, die nur Skripte schreiben (`farms.csv`, `keyword_report.csv`, Export), in Excel nur ansehen, nie speichern.
    - Datumsspalten in Dateien, die du bearbeitest (z. B. `reviewed_on` in `sanitization.csv`), liest das Skript in beiden Formaten (`JJJJ-MM-TT` und `TT.MM.JJJJ`).
  - Prüfwerkzeug: `python -m src.table_roundtrip prepare` und `compare` (nur mit der erfundenen Testdatei).
- **Tests:** pytest ab Phase 2, im Ordner `tests/`, nur mit erfundenen Höfen und erfundenen Länderseiten-Dateien unter `tests/fixtures/` (z. B. `base_url: "https://example.org"`), nie mit echten Dateien aus `sites/`. Erfundene Länderseiten bekommen Ländercodes, die ISO 3166-1 für Benutzerzwecke reserviert und nie einem Land zuteilt, z. B. `zz` oder `xa` (Vorschlag von Claude Code). Tests greifen nicht auf das Netz zu; robots.txt-Tests arbeiten mit erfundenem Text. Prüfungen, die zur Laufzeit abbrechen sollen (Grenzwerte, Export-Selbsttest), lösen eigene Fehler (Exceptions) aus statt `assert`, weil Python `assert`-Anweisungen mit der Option `-O` abschaltet.
- **Git:** Jede abgeschlossene Aufgabe wird ein Commit. Vor jedem Commit zeigt `git status`, was hineinkommt. Der Datenordner liegt außerhalb des Repositorys und ist zusätzlich per `.gitignore` ausgeschlossen (Abschnitt 10).

---

## 6. Stichwort-Umwandlung ohne Informationsverlust

Die Stichwort-Kategorien strukturieren die Bewertung. Zusammen mit den bereinigten Beschreibungen (Abschnitt 7) sind sie die Grundlage für Claudes Bewertung; für Beschreibungen, die du nicht freigegeben hast, sind sie die einzige Information aus dem Text. Stichworte sind immer eine Verdichtung. „Nichts geht verloren“ wird deshalb so sichergestellt:

1. **Der Originaltext bleibt vollständig erhalten**, lokal und unverändert in `farms.csv`. Er ist die maßgebliche Quelle und wird nie gelöscht oder überschrieben (bis zur Löschung nach der Reise).
2. **Regelbasiert und KI-frei:** Eine Taxonomie (`taxonomy.yaml`) ordnet Begriffe und Synonyme Kategorien zu.
   - **Nach Sprache getrennt (Entscheidung vom 17.11.2026):** Suchbegriffe, Verneinungen und Ignorierliste stehen je Sprache. Angewendet werden nur die Sprachen der Länderseite, zu der ein Hof gehört (`languages` in `sites/<site_id>.yaml`, erkennbar am Länderteil des Hof-Codes); für Deutschland Deutsch und Englisch, da Profile teils englisch sind.
   - Grund: Begriffe kollidieren zwischen Sprachen (norwegisch „sau“ = Schaf, deutsch „Sau“ = Schwein).
   - Die Kategorienschlüssel bleiben sprachunabhängig.
   - Fehlen die Sprachdaten für eine Sprache der Länderseite, bricht die Stichwort-Erkennung für die betroffenen Höfe mit klarer Meldung ab (nur Hof-Code, site_id, Sprachcode).
   - Einzelheiten in `05_stichwort_taxonomie.md`, Abschnitt 5; die Umstellung des YAML-Entwurfs erfolgt in Phase 6, Teil A.
3. **Whitelist-Prinzip:** Die Spalte `categories` enthält nur Kategorieschlüssel aus der Taxonomie, nie Freitext.
4. **Abdeckungsprüfung:** Die Beschreibung wird in Sätze zerlegt. Jeder Satz ohne relevanten Treffer wird lokal markiert. Der Bericht `keyword_report.csv` zeigt pro Hof den Anteil abgedeckter Sätze und listet die nicht abgedeckten Sätze, nur lokal.
5. **Nachschärfen:** Du liest die nicht abgedeckten Sätze lokal. Steckt darin eine relevante Information, ergänzt du die Taxonomie um Begriff und Kategorie und lässt das Skript erneut laufen. Das wiederholst du, bis nur noch irrelevante Sätze übrig sind (Begrüßung, Familie und Ähnliches). Diese kannst du über die Ignorierliste als „gesichtet, irrelevant“ markieren. Lies in jeder Runde außerdem einige **abgedeckte** Sätze stichprobenartig: Ein Satz mit einem Treffer kann weitere Informationen enthalten, die noch keiner Kategorie zugeordnet sind (z. B. „Der Bahnhof ist nah, wir holen dich ab“).
6. **Fehlerquellen im Deutschen** (für weitere Sprachen entsprechend bei der Länder-Prüfung):
   - **Verneinung:** „Wir haben keine Tiere“ enthält „Tiere“. Steht ein Verneinungswort der jeweiligen Sprache (kein, keine, nicht, ohne; no, not, without) kurz vor dem Treffer, setzt das Skript einen Prüfhinweis.
   - **Zusammengesetzte Wörter:** Teilwortsuche findet „Ziege“ in „Ziegenkäse“, aber auch „Rind“ in „Rinde“. Dagegen helfen Ausschlusslisten pro Kategorie.
   - **Umlaute und Groß-/Kleinschreibung:** Der Text wird vor dem Abgleich vereinheitlicht.
7. **Notizen für Feinheiten:** Umfang oder Qualität („großer Gemüsegarten“, „Käserei als Hauptbetrieb“) lassen sich nicht in Kategorien fassen. Dafür gibt es `notes.csv` (Abschnitt 5.3): Notizen in deinen eigenen Worten, ohne Personenbezug. Sie gehen mit dem Export an Claude.
8. **Taxonomie mit Claude besprechen:** Neue Begriffe und Kategorien kannst du mit Claude abstimmen, ohne Satzkontext aus Profilen. Beispiel: „Gehört ‚Mob Grazing‘ zu Tierhaltung oder zu Weidemanagement?“

---

## 7. Bereinigung der Beschreibung (KI-frei)

**Ziel:** Aus der Originalbeschreibung entsteht eine Fassung ohne Hof- und Personennamen, Kontakt- und Adressdaten. Nur diese Fassung darf an Claude, und nur nach deiner Freigabe.

**Schritt 1: Automatisch ersetzen (regelbasiert)**

| Was | Ersetzt durch | Wie erkannt |
|---|---|---|
| Hofname | `[FARM]` | aus der Spalte `farm_name` |
| auf dem Profil angezeigte Namen (z. B. der Gastgeber) | `[PERSON]` | aus der Spalte `displayed_names`; wo diese Namen stehen, klärt Phase 4 |
| Namen aus deiner Namensliste | `[PERSON]` | `local/name_list.txt` |
| E-Mail-Adressen, Web-Adressen, @-Namen aus sozialen Netzwerken | `[CONTACT]` | Muster (reguläre Ausdrücke) |
| Telefonnummern | `[CONTACT]` | Muster, je Land |
| Postleitzahlen, Straßen mit Hausnummer | `[ADDRESS]` | Muster, je Land |

**Schritt 2: Sätze mit möglichem Personenbezug markieren.** Sätze mit typischen Formulierungen über Menschen („wir sind“, „ich bin“, „mein Mann“, „meine Frau“, „unsere Kinder“, „Jahre alt“, „I am“, „my husband“, „our kids“, „years old“) werden für dich markiert, aber nicht automatisch gelöscht. Sie enthalten oft auch Hofinformationen („Wir sind ein kleiner Familienbetrieb mit Ziegen“).

**Sprache und Land (Entscheidung vom 17.11.2026):** Die Formulierungen aus Schritt 2 stehen je Sprache, die Muster für Postleitzahlen und Telefonnummern je Land. Angewendet werden nur die Sprachen und das Land der Länderseite, zu der ein Hof gehört (Länderteil des Hof-Codes). Fehlen diese Daten, brechen Bereinigung und Export für die betroffenen Höfe mit klarer Meldung ab. Wo diese Daten abgelegt werden, legen wir in Phase 6 fest.

**Schritt 3: Deine Prüfung und Freigabe (Pflicht).**
- Du liest jede bereinigte Beschreibung lokal, z. B. in Excel oder LibreOffice.
- Du korrigierst bei Bedarf direkt in `sanitization.csv`. Dabei achtest du auch auf sehr genaue Lagehinweise („neben der Kirche von …“) und persönliche Details (Alter, Beruf, Herkunft).
- Entdeckst du einen Namen, ergänzt du ihn in `name_list.txt`, damit er künftig automatisch ersetzt wird.
- Dann trägst du in der Spalte `approved` „yes“ ein.

**Erneuter Lauf:** Ein erneuter Lauf von `sanitize.py` (z. B. nach einer Ergänzung der Namensliste) überschreibt keine freigegebenen Zeilen, und deine Korrekturen gehen nicht verloren. Wie das genau umgesetzt wird, legen wir in Phase 6 fest.

**Schritt 4: Selbsttest vor dem Export** (Phase 7). Der Export bricht ab, wenn eine bereinigte Beschreibung noch den Hofnamen, einen Namen aus `displayed_names` oder der Namensliste oder ein Kontakt- oder Adressmuster (des Landes des Hofs) enthält, oder wenn sie nicht freigegeben ist.

**Grenze:** Namen, die weder auf dem Profil angezeigt werden noch in deiner Namensliste stehen (z. B. Vornamen von Kindern oder Nachbarn), erkennt das Skript nicht zuverlässig. Im Deutschen werden alle Nomen großgeschrieben, Namen sind also nicht an der Schreibweise erkennbar, und eine KI soll das Skript nicht nutzen. Deshalb ist deine Prüfung in Schritt 3 Pflicht.

---

## 8. Lernplan

**Arbeitsweise (Entscheidung vom 15.11.2026; ersetzt die Fassung vom 01.11.2026):**
- Claude Code schreibt den Code, immer nur den nächsten, sinnvoll zusammenhängenden Schritt. Du steuerst, prüfst die Änderungen, lässt dir erklären, was du nicht verstehst, und pushst selbst.
- Claude Code erklärt jede Änderung kurz und neue Konzepte in wenigen Sätzen. Am Ende jeder Phase stellt es dir Verständnisfragen.
- Fragen an Claude Code sind jederzeit möglich, ohne dass sich etwas am Code ändert.
- Die Lerninhalte der Phasen bleiben; du lernst sie über das Lesen, Prüfen und Hinterfragen des Codes statt über das eigene Schreiben.
- Jede Phase ist erst fertig, wenn du den Code der Phase erklären kannst und `07_bedienung.md` die Bedienung ihrer neuen Teile beschreibt (Entscheidung vom 17.11.2026).
- Die Zeilen „Claude hilft“ in den Phasen beschreiben die Arbeitsweise bis zum 15.11.2026. Seitdem gilt `CLAUDE.md`; Anleitung in `docs/arbeiten_mit_claude_code.md`.

Jede Phase hat ein Ziel, Lerninhalte, konkrete Aufgaben und ein Abnahmekriterium.

### Phase 0 – Einrichtung

- **Ziel:** Arbeitsfähige Umgebung mit Versionsverwaltung und sauberer Trennung von Code und Daten.
- **Du lernst:** Python Install Manager, virtuelle Umgebungen, pip, Git-Grundlagen (Repository, Commit, Push), GitHub, Berechtigungen in Claude Code.
- **Aufgaben:**
  - Laptop einrichten (`04_technische_voraussetzungen.md`).
  - Code-Ordner `wwoof-planner` und Datenordner `wwoof-data` nebeneinander anlegen (Abschnitt 5.1).
  - Git einrichten, privates GitHub-Repository `wwoof-planner` anlegen, erster Commit und Push (`04_technische_voraussetzungen.md`, Abschnitt 7).
  - Claude Code einrichten und den Datenordner sperren (Abschnitt 5.1; `04_technische_voraussetzungen.md`, Abschnitt 8; offener Punkt 9).
- **Fertig, wenn:** die Checkliste in `04_technische_voraussetzungen.md`, Abschnitt 9, abgehakt ist.
- **Claude hilft:** Schritt für Schritt bei der Einrichtung und anhand von Fehlermeldungen.

### Phase 1 – Python-Grundlagen am eigenen Projekt

- **Du lernst:** Variablen, Listen, Dictionaries, Schleifen, Bedingungen, Funktionen, Dateien lesen und schreiben (CSV), Fehlerbehandlung (`try`/`except`), erste Schritte mit pandas.
- **Aufgaben:**
  - Eine Testtabelle mit 3–5 **erfundenen** Höfen in `tests/fixtures/` anlegen, mit allen Spalten aus `farms.csv`. Baue in die erfundenen Beschreibungen erfundene Namen, E-Mail-Adressen und Telefonnummern ein; damit testest du später die Bereinigung. Nimm einen Hof absichtlich doppelt auf (gleiche `profile_url`), um später die Erkennung von Doppelungen zu testen.
  - Ein Skript schreiben, das die Tabelle liest, nach Region filtert und ein Ergebnis schreibt.
  - Das CSV-Format testen (Abschnitt 5.5): Datei in Excel öffnen, ändern, speichern und wieder einlesen.
- **Fertig, wenn:** das Skript läuft, du jede Zeile erklären kannst und das CSV-Format feststeht.
- **Claude hilft:** erklärt Konzepte, gibt Übungen, prüft deinen Code. Die erfundenen Testdaten darfst du mit Claude teilen; Claude kann sie auch erzeugen.

### Phase 2 – Konfiguration, robots.txt und erste Tests

- **Du lernst:** Module und Importe, YAML lesen und seine Fallen (`no` als `false`, doppelte Schlüssel), Werte prüfen (harte Grenzen), eigene Exceptions, `urllib.robotparser` aus der Standardbibliothek, **pytest** (Tests schreiben und ausführen), **GitHub Actions** (Tests laufen automatisch bei jedem Push).
- **Aufgaben:**
  - `config.py` lädt `config.yaml` und die gewählte Länderseiten-Datei `sites/<site>.yaml` und lehnt unzulässige Werte ab (Prüfungen in Abschnitt 5.4: Strings, bekannte Schlüssel, Region vorhanden, Regionsschlüssel eindeutig, `base_url` mit https, harte Grenzen). Eine Region ohne Suchdefinition ist gültig.
  - `robots_check.py` liest `base_url` aus der Länderseiten-Datei und meldet „erlaubt“ oder „verboten“ für eine URL.
  - `sites/de.yaml` mit den bisher bekannten Werten: `base_url`, `languages`, Regionen `voralpenland` (`VA`) und `sachsen` (`SN`) nur mit Schlüssel und Kürzel. Suchdefinitionen und Lernkategorien folgen in Phase 4.
  - pytest-Tests mit erfundenen Länderseiten-Dateien unter `tests/fixtures/` (Abschnitt 5.5), darunter `site: no` ohne Anführungszeichen und eine Region ohne Suchdefinition.
  - Ein GitHub-Actions-Workflow führt die Tests bei jedem Push aus (Entscheidung vom 15.11.2026).
  - `07_bedienung.md`, Teil A: erster Stand (Länderseite und Region wählen, robots-Prüfung); Meldungen der Konfigurationsprüfung in Teil E.
- **Fertig, wenn:**
  - eine Konfiguration mit `max_profiles_per_run: 100` abgelehnt wird,
  - `site: no` ohne Anführungszeichen, ein unbekannter Schlüssel in der Länderseiten-Datei und eine unbekannte Region mit klarer Meldung abgelehnt werden,
  - eine Region ohne Suchdefinition angenommen wird,
  - die robots-Prüfung für Test-URLs korrekt antwortet,
  - `pytest` ohne Fehler durchläuft und der Workflow auf GitHub grün ist,
  - `07_bedienung.md` die neuen Teile beschreibt.

### Phase 3 – HTML/CSS-Grundlagen und Browser-Automatisierung auf Übungsseiten

- **Du lernst:**
  - **HTML und CSS:** Aufbau einer HTML-Seite, Elemente, Attribute, Klassen, der DOM (die Baumstruktur einer Seite im Browser), CSS-Selektoren und die Entwicklerwerkzeuge des Browsers (Elemente untersuchen).
  - **Playwright:** Seiten öffnen, auf Inhalte warten, Selektoren, Texte auslesen, Blättern, Login-Formulare, JavaScript-Inhalte, Pausen und Obergrenzen.
- **Übungsseiten:** books.toscrape.com und quotes.toscrape.com. Beide sind eigens zum Üben gebaut; quotes.toscrape.com hat auch einen Login und eine JavaScript-Variante (`/js/`).
- **Aufgaben:**
  - Die Übungsseiten mit den Entwicklerwerkzeugen untersuchen und Selektoren für einzelne Felder von Hand finden.
  - Einen Mini-Sammler für Zitate über mehrere Seiten bauen, mit Login, Pausen, Obergrenze und CSV-Ausgabe. Als Übung für die Gästebuch-Anzahl zählt er zusätzlich die Zitate pro Seite, ohne ihren Text zu speichern.
- **Fertig, wenn:** der Sammler fortsetzbar ist (bereits erfasste Einträge überspringt, keine Doppelungen erzeugt) und sich bei Fehlern sauber beendet.
- **Warum zuerst üben:** Alle Fehler beim Lernen passieren auf Seiten, die dafür gemacht sind, nicht auf einer Länderseite.

### Phase 4 – wwoof.de erkunden (erste Länder-Prüfung: Deutschland)

- **Gate:** Offener Punkt 6 ist erledigt (01.11.2026; gilt für alle Länderseiten der CWP); Mitgliedschaft bei WWOOF Deutschland aktiv; die robots.txt-Prüfung aus Phase 2 ist umgesetzt.
- **Einordnung:** Phase 4 ist die erste Länder-Prüfung nach `07_bedienung.md`, Teil C, Schritt 6. Sie ist das Muster für weitere Länderseiten.
- **Wer:** Du erkundest die Seite selbst. Claude sieht weder Seiten noch Quelltext, sondern nur Strukturbeschreibungen mit Platzhaltern (Abschnitt 10).
- **Du lernst:** persistente Browserprofile, Entwicklerwerkzeuge auf einer echten Seite, `playwright codegen` zum Finden von Selektoren.
- **Aufgaben:**
  - Persistentes Profil im Datenordner unter `browser_profile/de/` anlegen und dich manuell einloggen. Dabei prüfen, ob dein WWOOFer-Profil vollständig ist.
  - Herausfinden, wie wwoof.de nach Regionen filtert (Bundesland, Karte, Umkreis um einen Ort?). Daraus folgen die Suchdefinitionen der Regionen in `sites/de.yaml` und die Abgrenzung des Voralpenlands (offener Punkt 10).
  - Herausfinden, wie Profil-URLs aufgebaut sind (z. B. Profil-ID, Zusätze). Daraus folgt die Normalisierung für den Abgleich, mit Domain (Abschnitt 5.2).
  - Herausfinden, welche Lageangabe ein Profil zeigt und wie „Lernmöglichkeiten“ dargestellt werden.
  - Herausfinden, **wo die Anzahl der Gästebucheinträge steht**: als Zahl auf dem Profil oder am Reiter, oder nur als Liste, die gezählt werden muss.
  - **Kalender (offener Punkt 12):** Gibt es auf den Hofprofilen einen Kalender? Was zeigt er (freie oder belegte Tage, Monate)? Braucht er einen eigenen Seitenaufruf? Lässt er sich zuverlässig auslesen? Das Ergebnis entscheidet, ob `availability.enabled` auf `true` bleibt.
  - Herausfinden, wo auf dem Profil Namen angezeigt werden (z. B. Gastgebername). Sie werden nur lokal für die Bereinigung gespeichert.
  - Die Liste der vorkommenden Lernkategorien sammeln und in `learning_categories` von `sites/de.yaml` eintragen; sie dient später dem Export-Selbsttest. Dabei prüfen, ob eine Kategorie das Zeichen `|` enthält.
  - Selektoren für alle Felder finden und dokumentieren.
  - Festhalten, was für die ganze CWP gilt (z. B. Selektoren, URL-Aufbau, Ablauf) und was länderspezifisch ist (z. B. Regionsfilter, Lernkategorien), und festlegen, an welcher Stelle im Code das Plattformweite steht (Abschnitt 4).
  - Die Checkliste in `07_bedienung.md`, Teil C, anhand der Erfahrungen schärfen.
- **Fertig, wenn:** die Selektoren dokumentiert sind (mit Platzhaltern statt echter Hofdaten), `sites/de.yaml` Suchdefinitionen und Lernkategorien enthält, die Trennung plattformweit/länderspezifisch dokumentiert ist, Teil C geschärft ist und ein Testlauf mit **einem** Profil funktioniert.
- **Claude hilft:** nur mit Selektoren und Strukturbeschreibungen, die keine Hofdaten enthalten (Abschnitt 10).

### Phase 5 – Hof-Sammler bauen

- **Vorher:** Gesamtumfang und Tagesgrenze festlegen, auch ob sie je Länderseite oder insgesamt gelten (offener Punkt 11).
- **Du lernst:** Programmstruktur über mehrere Dateien, Logging, robuste Fehlerbehandlung, Fortsetzbarkeit, Abgleich von Datensätzen.
- **Aufgaben:**
  - `region_list.py`, `profile_reader.py` und `collector.py` nach dem Ablauf in Abschnitt 4, einschließlich Vergabe der Hof-Codes und Abgleich über die normalisierte Profil-URL (Abschnitt 5.2), Lesen der Gästebuch-Anzahl und, falls aktiviert, der freien Zeitfenster.
  - Der Sammler arbeitet mit `site` und `region` aus `config.yaml`, mit dem Browser-Profil der Länderseite (`browser_profile/<site_id>/`) und prüft vor jedem Lauf die robots.txt.
  - Hat die gewählte Region keine Suchdefinition, bricht der Sammler vor dem ersten Seitenaufruf mit klarer Meldung ab (mit pytest-Test).
  - Link-Listen und Log-Einträge tragen die site_id (Abschnitte 4 und 5.3).
  - `07_bedienung.md`, Teil A, vollständig.
- **Fertig, wenn:** eine Region (z. B. das Voralpenland) erfasst ist, alle Grenzen eingehalten wurden, jeder Hof genau einmal mit genau einem Hof-Code in `farms.csv` steht (geprüft mit einem pytest-Test an erfundenen Daten und einer Prüffunktion für die echte Tabelle), das Log keine Hofdaten enthält und `07_bedienung.md`, Teil A, den Sammellauf beschreibt.

### Phase 6 – Stichworte und Bereinigung

- **Du lernst:** Textverarbeitung (Normalisierung, Zerlegen in Sätze, Wortsuche), reguläre Ausdrücke für Muster (E-Mail, Telefon, Web-Adresse, Postleitzahl), Auswertungsberichte.
- **Teil A (Stichworte):** `taxonomy.yaml` aus `05_stichwort_taxonomie.md` übernehmen und dabei nach Sprache umstellen (`05_stichwort_taxonomie.md`, Abschnitt 5), `tagging.py` nach Abschnitt 6 bauen und die Taxonomie in Runden nachschärfen.
- **Teil B (Bereinigung):** `sanitize.py` nach Abschnitt 7 bauen, mit Formulierungen je Sprache und Mustern für Postleitzahlen und Telefonnummern je Land; Ablage dieser Daten festlegen. Zuerst an den erfundenen Testdaten aus Phase 1 prüfen: Alle eingebauten Namen, E-Mail-Adressen und Telefonnummern müssen ersetzt werden. Danach auf die echten Daten anwenden; du prüfst und gibst frei.
- **Beide Teile:** Fehlen Sprach- oder Länderdaten für die Länderseite eines Hofs, bricht das Skript für die betroffenen Höfe mit klarer Meldung ab (mit pytest-Test). `07_bedienung.md`, Teil B: Stichworte, Bereinigung, Prüfung und Freigabe.
- **Reihenfolge:** Teil B gehört zum ersten Export, weil die bereinigten Beschreibungen ein wichtiger Teil der Bewertung sind. Bei Bedarf kann ein erster Export ohne Beschreibungen erfolgen (`include_description: false`); die Beschreibungen folgen dann mit einem zweiten Export.
- **Fertig, wenn:**
  - alle nicht abgedeckten Sätze gesichtet sind und sich die Taxonomie zwischen zwei Runden nicht mehr ändert, und
  - die Bereinigung alle Testfälle besteht und jede echte Beschreibung von dir geprüft ist (freigegeben oder bewusst nicht).

### Phase 7 – Export und Übergabe an Claude

- **Du lernst:** Prüfungen zur Laufzeit mit eigenen Exceptions, pytest-Tests dafür, Datenschutz als Code.
- **Aufgaben:** `export.py` mit Selbsttest, der vor dem Schreiben prüft:
  - Nur Whitelist-Spalten (Abschnitt 5.3).
  - `farm_code` hat das Format `LAND-REGION-NNN` und ist eindeutig.
  - Der Länderteil jedes Hof-Codes gehört zu einer bekannten Länderseite (`sites/<site_id>.yaml`), und deren Sprach- und Länderdaten sind vorhanden.
  - Kein Hofname erscheint in irgendeinem exportierten Feld.
  - `categories` enthält nur Schlüssel aus der Taxonomie.
  - `learning_categories` enthält nur Kategorien aus der Liste der Länderseite des Hofs (`learning_categories` in der Länderseiten-Datei, aus der Länder-Prüfung); eine leere Liste wird hier abgelehnt.
  - `guestbook_count` ist eine ganze Zahl ab 0.
  - `location` ist kurz und enthält keine Ziffern (also keine Postleitzahl oder Hausnummer).
  - `available_windows` hat das festgelegte Format und liegt im konfigurierten Zeitraum.
  - `notes` enthält keinen Hofnamen, keine Namen aus `displayed_names` oder der Namensliste und keine Kontakt- oder Adressmuster.
  - `description_sanitized` ist nur gefüllt, wenn `include_description: true` gesetzt und der Text freigegeben ist, und enthält keine Namen aus `displayed_names` oder der Namensliste sowie keine Kontakt- oder Adressmuster.
- **Fertig, wenn:** der Export den Selbsttest besteht, du ihn in das Claude-Projekt hochladen kannst und `07_bedienung.md`, Teil B, Export und Hochladen beschreibt. Claude bewertet dann und plant die Route.

---

## 9. Ausbaustufen (später, optional)

- **Weitere Felder:**
  - Durchschnittsbewertung, falls die Plattform eine als Zahl anzeigt.
  - Freie Zeitfenster aus dem Kalender, falls sie sich in Phase 4 als nicht gut machbar für die erste Version erweisen (bis dahin pflegst du sie von Hand).
- **Planungsskripte**, die mit deiner eigenen Tabelle arbeiten, nicht mit der Plattform:
  - Bewertungsskript mit gewichteten Punkten und Rangliste.
  - Routenplaner: Orte in Koordinaten umwandeln, Reihenfolge mit Zeitfenstern optimieren, z. B. mit Google OR-Tools.
  - Kartendarstellung, z. B. mit folium.
  - Kontaktplaner: Anfragetermine berechnen, Nachrichtenentwürfe aus Vorlagen erzeugen.
  - Für Dienste zur Ortsbestimmung oder für Fahrpläne vorher deren Nutzungsbedingungen prüfen.
- **Weitere Länder (Entscheidung vom 17.11.2026):**
  - Weitere Länderseiten der CWP kommen nur über die Checkliste in `07_bedienung.md`, Teil C, dazu, ohne Codeänderung, solange die Länder-Prüfung keine Abweichung zeigt.
  - **Norwegen** (wwoofnorway.org, site_id `"no"`) ist der nächste Kandidat: eigene Mitgliedschaft, robots.txt-Prüfung, Länder-Prüfung, norwegische Sprachdaten und norwegische Muster für Postleitzahlen und Telefonnummern.
  - **Irland** (wwoof.ie) hat eine eigene Plattform und gehört nicht zum Umfang: kein Code und keine Vorbereitung dafür.

---

## 10. Zusammenarbeit und Datenschutz beim Debugging

| Darfst du mit Claude teilen | Bitte nicht teilen |
|---|---|
| Code, Konfiguration | HTML-Quelltext von Hofseiten |
| Fehlermeldungen und Tracebacks ohne Hofdaten | Screenshots von Hofseiten |
| Selektoren mit Platzhaltern (z. B. `<FARM_NAME>`) | Inhalte aus `wwoof-data/` (Hofnamen, Originalbeschreibungen, Namen, Notizen im Rohzustand) |
| Testdaten mit erfundenen Höfen | Log-Zeilen mit Hofnamen, Links oder Texten |
| Strukturbeschreibungen („Die Beschreibung steht in einem Element mit der Klasse X“) | Echte Hofnamen in Selektoren |
| Den Export aus `wwoof-data/export/` (lädst du selbst hoch) | Gästebuchtexte |
| Log-Auszüge, die du geprüft hast | Das Browser-Profil |

**Praktische Regeln:**
- **Claude führt Code nur mit erfundenen Daten aus**, z. B. die pytest-Tests. Läufe gegen eine Länderseite und Läufe mit echten Daten startest du selbst und teilst danach nur Fehlermeldungen oder Zusammenfassungen ohne Hofdaten.
- **Logs ohne Hofdaten bauen:** Logs enthalten nur Hof-Codes, Zeitstempel und Status.
- **Selektoren über die Struktur** (CSS-Klassen, Attribute, Position) statt über sichtbare Texte bauen. Das ist robuster und datenschutzfreundlich. `playwright codegen` erzeugt oft textbasierte Selektoren; diese ersetzt du.
- **Vor dem Teilen** Hofnamen, Links und Textauszüge durch Platzhalter ersetzen.
- **Rückfragen von Claude Code:** Betrifft eine Rückfrage `wwoof-data\`, eine Länderseite oder api.wwoof.net, lehnst du ab. Nach den Regeln sollte das nicht vorkommen; falls doch, ist es ein Fehler, den wir beheben.

**Git:** Das Repository auf GitHub ist privat. Der Datenordner liegt außerhalb des Repositorys. Als zusätzliche Sicherung schließt die `.gitignore` alle Daten-, Profil- und Logordner aus:

```
# virtual environment and caches
.venv/
__pycache__/
.pytest_cache/

# safety net: data must never be inside the repository
wwoof-data/
browser_profile/
local/
export/
logs/
```

---

## 11. Zeitplanung

**Entfällt (Entscheidung vom 15.11.2026):** Es gibt keinen Zeitplan und kein festes Zeitbudget mehr; du arbeitest nach eigenem Tempo. Die Reiseplanung mit Reisebeginn und Kontaktfenster liegt im claude.ai-Projekt (`01_reiseplan.md`). Weiterhin gilt der Vorrang vom 01.11.2026: Der Sammler wird fertig, bevor die Kontaktphase beginnt; notfalls beginnt die Reise später.

---

## Quellen

- Übungsseiten: https://toscrape.com
- Playwright für Python, Dokumentation: https://playwright.dev/python/docs/intro
- WWOOF-bezogene Quellen: siehe `02_regeln_und_rahmenbedingungen.md`
