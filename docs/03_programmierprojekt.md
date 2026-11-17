# Programmierprojekt: Hof-Sammler (Länderseiten der CWP, zuerst Deutschland)

**Stand:** 17.11.2026 · Maßgeblich für den Code: Ziel, Leitplanken, Aufbau, Datenmodell, Phasen. Regeln zu Daten und Teilen: `02_regeln_und_rahmenbedingungen.md`; Verlauf: `08_entscheidungsprotokoll.md`.

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
- freie Zeitfenster aus dem Kalender, falls technisch gut möglich (Klärung in Phase 2)

**Von dir gepflegt:** eigene Notizen ohne Personenbezug (Abschnitt 6, Punkt 7).

**Weiterverarbeitung, ebenfalls lokal und KI-frei:**
- Stichwort-Kategorien aus der Beschreibung (Abschnitt 6)
- ein Hof-Steckbrief aus der Beschreibung: nur Schlüssel und Werte eines festen Schemas, kein Freitext, deshalb ohne Personendaten und ohne Prüfung durch dich (Abschnitt 7)

**Export für Claude (Whitelist), in zwei Stufen:** zuerst Hof-Code, Ort, Region, Lernmöglichkeiten, Anzahl der Gästebucheinträge, freie Zeitfenster, Notizen (Phase 4); dann zusätzlich Stichwort-Kategorien, Abdeckung und Steckbrief (Phase 6). **Hofnamen und Freitexte aus Profilen gehen nie an Claude.**

**Nebenziel:** Programmieren lernen (Ziel 2 des Projekts): Python vom eigenen Skript bis zur Browser-Automatisierung, dazu HTML- und CSS-Grundlagen, Tests mit pytest und Versionsverwaltung mit Git und GitHub. Seit dem 15.11.2026 mit Schwerpunkt auf der Entwicklung mit KI-Unterstützung: Aufgaben formulieren, Code von Claude Code prüfen und verstehen (Abschnitt 8).

---

## 2. Leitplanken (gelten immer)

1. **KI-frei:** Die Skripte rufen keine KI-Dienste auf.
2. **Nur einzelne Regionen:** eine Länderseite und eine Region pro Lauf, nie die gesamte Hostliste einer Länderseite.
3. **Obergrenze pro Lauf:** Vorschlag 30 Profile. Eine harte Grenze von 50 ist fest im Code verankert und lässt sich nicht per Konfiguration überschreiben. Grenzen, Pausen und Abbruchregeln gelten unverändert für jede Länderseite. Gesamtumfang und Tagesgrenze legen wir vor Phase 3 fest, auch ob sie je Länderseite oder insgesamt gelten (offener Punkt 11 in `00_projekt_uebersicht.md`).
4. **Normales Tempo, kein Massenabruf:** eine Seite nach der anderen, keine parallelen Abrufe, zufällige Pause zwischen zwei Seitenaufrufen (Vorschlag 10–20 Sekunden). Ein Lauf mit 30 Profilen dauert damit grob 6–13 Minuten (Pausen plus Ladezeiten). Jeder zusätzliche Aufruf pro Profil (z. B. für Gästebuch oder Kalender) verlängert den Lauf entsprechend, bei zwei Zusatzaufrufen auf etwa das Dreifache.
5. **Echter Browser, eigene Sitzung:** Playwright steuert einen echten Browser. Du loggst dich darin einmal je Länderseite **manuell** ein; jede Länderseite hat ein eigenes Browser-Profil. Dein Passwort steht nie im Code. Keine direkten Aufrufe der Plattform-Schnittstelle (api.wwoof.net), kein Umgehen von Schutzmaßnahmen.
6. **Läufe startest nur du:** Jeden Lauf gegen eine Länderseite startest du selbst in deinem Terminal. Claude startet weder den Sammler noch andere Skripte, die eine Länderseite oder api.wwoof.net aufrufen (Absprache mit WWOOF: kein direktes KI-Browsing).
7. **robots.txt:** Die robots.txt der gewählten Länderseite wird vor jedem Lauf geprüft. Bei einem Verbot bricht das Skript ab.
8. **Abbruch statt Hartnäckigkeit:** Bei Captcha, Zugriffsverweigerung, Login-Aufforderung oder unerwarteten Fehlern beendet sich das Skript sauber, statt es erneut zu versuchen.
9. **Daten bleiben lokal und getrennt:** Alles, was ein Lauf erzeugt oder liest (Hoftabelle, Notizen, Berichte, gesicherte Seiten und Skelette der Erkundung, Logs, Browser-Profile), liegt im Datenordner `wwoof-data/` außerhalb des Code-Repositorys (Abschnitt 5.1). Claude hat darauf keinen Zugriff. An Claude gehen nur der Export mit den Whitelist-Feldern und von dir geprüfte Struktur-Skelette (Phase 2); beides gibst du selbst weiter.
10. **Einmalige Erfassung, keine Redundanzen:** Jeder Hof wird nur einmal abgerufen und steht genau einmal in `farms.csv`, mit genau einem Hof-Code. Erneute Abrufe zur Aktualisierung gibt es nicht. Andere Dateien verweisen nur über den Hof-Code auf einen Hof und wiederholen keine Felder aus `farms.csv`.
11. **Gästebuch nur als Zahl:** Das Skript liest nur die Anzahl der Einträge. Gästebuchtexte werden weder gespeichert noch exportiert.
12. **Löschung nach der Reise:** Alle Hofdaten werden nach der Reise gelöscht. Darum kümmerst du dich, auch um die Exporte, die du in das Claude-Projekt hochgeladen hast.
13. **Gates:**
    - Abklärung mit WWOOF: erledigt (offener Punkt 6, laut Nutzer am 01.11.2026). Sie gilt laut Nutzer für alle Länderseiten der CWP (`02_regeln_und_rahmenbedingungen.md`, Abschnitt 1).
    - Vor dem ersten Lauf gegen eine Länderseite ist die Checkliste in `07_bedienung.md`, Teil C, erledigt: Mitgliedschaft → Regionsschlüssel und -kürzel → robots.txt-Prüfung → Länder-Prüfung → Suchdefinition je Region → Testlauf mit einem Profil. Für Deutschland ist Phase 2 die Länder-Prüfung.
    - Im Code stehen davon nur zwei Prüfungen: die robots.txt-Prüfung vor jedem Lauf (offener Punkt 7, Phase 2) und der Abbruch des Sammlers, wenn die gewählte Region keine Suchdefinition hat (Phase 3). Den Rest sichert die Checkliste.
    - Vor jedem Export: Der Selbsttest lässt nur Whitelist-Spalten und, beim Steckbrief, nur Schlüssel und Werte aus dem Schema durch (Abschnitt 7, Phasen 4 und 6).
14. **Länderdaten an einer Stelle:** Was eine Länderseite ausmacht, steht in `sites/<site_id>.yaml` (Abschnitt 5.4). Außerhalb von `sites/` und `tests/fixtures/` steht keine Domain einer Länderseite im Code. Tests verwenden nur erfundene Länderseiten-Dateien.

---

## 3. Warum Playwright?

Der Seitenquelltext von wwoof.de enthält die Konfiguration einer JavaScript-Anwendung (Ember), die ihre Inhalte von einer Schnittstelle (api.wwoof.net) nachlädt (geprüft am 25.10.2026). Ein einfacher HTTP-Abruf, etwa mit `requests`, sieht diese Inhalte deshalb nicht zuverlässig. Playwright öffnet die Seiten wie ein normaler Browser, und das Skript liest, was auch du auf dem Bildschirm sehen würdest. Wie die Seiten genau aufgebaut sind, klärt die Erkundung in Phase 2. Ob andere Länderseiten der CWP gleich aufgebaut sind, ist nicht belegt; das klärt die Länder-Prüfung (`07_bedienung.md`, Teil C).

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
   - Hofname, Ort, Beschreibung, Lernmöglichkeiten, Anzahl der Gästebucheinträge und, falls aktiviert, die freien Zeitfenster lesen. Muss dafür ein eigener Reiter oder eine eigene Seite geöffnet werden, zählt das als eigener Seitenaufruf mit Pause.
   - Eine Zeile in `farms.csv` schreiben.
   - Zufällige Pause.
8. Bei etwas Ungewöhnlichem (Captcha, Zugriffsverweigerung, Login-Aufforderung) sofort sauber beenden und einen Log-Eintrag schreiben. Log-Einträge nennen die site_id, aber keine Hofdaten.
9. Zusammenfassung ausgeben (Länderseite, Region, neu erfasst, übersprungen, Fehler), **ohne Hofdaten**.

Selektoren, URL-Normalisierung, Ablauf und das Auslesen eines Profils gelten für die ganze CWP und stehen an genau einer Stelle im Code; welche, legen wir in Phase 2 fest. Was je Länderseite verschieden ist, steht in der Länderseiten-Datei.

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
│   ├── docs\                  Projektdokumente (00, 02–08, Anleitung)
│   ├── sites\                 eine Datei pro Länderseite, z. B. de.yaml (Abschnitt 5.4)
│   ├── src\
│   │   ├── config.py          Konfiguration und Länderseiten-Datei laden und prüfen
│   │   ├── robots_check.py    robots.txt prüfen
│   │   ├── explore_site.py    Erkundung: Seiten lokal sichern, Struktur-Skelett schreiben
│   │   ├── page_skeleton.py   HTML in ein Skelett ohne Inhalte umwandeln
│   │   ├── session.py         Browser mit persistentem Profil starten
│   │   ├── region_list.py     Suchergebnisse einer Region lesen
│   │   ├── profile_reader.py  ein Profil lesen, Felder extrahieren
│   │   ├── collector.py       Steuerung: Grenzen, Pausen, Hof-Codes, Abgleich, Fortsetzen, Logging
│   │   ├── tagging.py         Taxonomie und Steckbrief anwenden, Bericht
│   │   └── export.py          Whitelist-Export für Claude mit Selbsttest
│   └── tests\                 pytest-Tests, nur mit erfundenen Höfen
│       └── fixtures\          erfundene Testdaten, Länderseiten-Dateien und Testseiten
│
└── wwoof-data\                Datenordner (kein Git, kein Zugriff für Claude)
    ├── browser_profile\
    │   └── <site_id>\         Login-Sitzung je Länderseite, z. B. de\
    ├── local\                 Hoftabelle (alle Länder), Berichte, Notizen, Profil-Link-Listen,
    │                          samples\ und structure\ der Erkundung (Phase 2)
    ├── export\                Export für Claude (lädst du selbst hoch)
    └── logs\                  Protokolle ohne Hofdaten
```

- Den Pfad zum Datenordner liest der Code aus `config.yaml` (`data_dir`); im Code steht kein Pfad zu echten Daten. Die Unterordner legt das Skript bei Bedarf selbst an.
- **Zusammenarbeit mit Claude Code (Entscheidung vom 01.11.2026):** Claude Code läuft lokal und wird immer im Ordner `wwoof-planner\` gestartet, nie in `wwoof-data\` oder im gemeinsamen Oberordner `Projekte\`.
- **Absicherung:** Read-Deny-Regel für `wwoof-data\`, Projekteinstellungen in `.claude/settings.json` und deren Grenzen beschreibt `04_technische_voraussetzungen.md`, Abschnitt 8. Wegen dieser Grenzen startet Claude keine Skripte, die eine Länderseite aufrufen oder echte Daten verarbeiten (Leitplanke 6).
- **Logs** enthalten keine Hofdaten, liegen aber trotzdem im Datenordner: Schreibt ein Fehler doch Hofdaten ins Log, gelangen sie so nicht zu Claude. Log-Auszüge teilst du nach eigener Prüfung.
- **Browser-Profile:** je Länderseite ein eigener Unterordner `browser_profile/<site_id>/` mit eigenem Login; für jede Länderseite ist eine eigene Mitgliedschaft nötig. Jedes Profil enthält eine Login-Sitzung und ist damit so schutzbedürftig wie ein Passwort.
- **Dateinamen**, die aus site_id oder Regionsschlüssel entstehen (z. B. Link-Listen), sind nur klein geschrieben, weil Windows bei Dateinamen nicht zwischen Groß- und Kleinschreibung unterscheidet.

### 5.2 Hof-Code

- **Format:** `LAND-REGION-NNN`, z. B. `DE-VA-001` für das Voralpenland und `DE-SN-001` für Sachsen.
  - `LAND` ist die site_id der Länderseite in Großbuchstaben (Ländercode nach ISO 3166-1 Alpha-2, z. B. `de` → `DE`, `no` → `NO`).
  - `REGION` ist das Regionskürzel aus der Länderseiten-Datei (Abschnitt 5.4). Das Präfix wird aus diesen beiden Werten gebildet; es gibt dafür keine eigene Einstellung (eine Quelle).
- Das Skript vergibt den Code beim ersten Erfassen fortlaufend. Er bleibt dem Hof dauerhaft zugeordnet.
- **Eindeutigkeit:** Ein Hof bekommt genau einen Code. Die Zuordnung erfolgt über die **normalisierte Profil-URL** (`profile_url`), die nur lokal gespeichert wird. „Normalisiert“ heißt: ohne Zusätze wie Abfrageparameter, sodass derselbe Hof immer dieselbe URL hat. Die normalisierte URL **behält die Domain**, damit der Abgleich auch über Länderseiten hinweg eindeutig bleibt. Wie die URLs aufgebaut sind (z. B. mit einer Profil-ID), klärt die Erkundung in Phase 2.
- **Überschneidung zweier Regionen (Entscheidung vom 01.11.2026):** Taucht ein Hof in einer weiteren Region auf, behält er den Code und die Region aus der ersten Erfassung und wird nicht erneut abgerufen.
- **Kein Bezug zum Namen:** keine Initialen, keine Abkürzungen des Hofnamens.
- Die Zuordnung Hof-Code ↔ Hofname steht nur in `local/farms.csv`. Dort schlägst du nach, welchen Hof du anschreiben musst.
- **Land:** Das Land eines Hofs steckt im Länderteil des Hof-Codes. `farms.csv` bleibt eine Tabelle für alle Länder, ohne zusätzliche Spalte.

### 5.3 Dateien

Alle Daten liegen als CSV-Dateien vor. Sie lassen sich in Excel oder LibreOffice öffnen, und es ist eine **Liste**, keine Datenbank (passend zur Absprache „private Liste“).

**Grundsatz:** Dateien, die du von Hand bearbeitest (`notes.csv`), überschreibt das Skript nie.

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
| `available_windows` | freie Zeitfenster im Format `JJJJ-MM-TT/JJJJ-MM-TT`, mehrere getrennt durch `\|`; leer, wenn nicht erfasst. Was gespeichert wird, wenn der Kalender keine freien Fenster zeigt, legen wir in Phase 2 fest. |
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
| `facts` | Steckbrief: `key=value`-Paare aus dem Schema, getrennt durch `\|` (Abschnitt 7) |
| `coverage_percent` | Anteil der Sätze mit mindestens einer relevanten Kategorie |
| `uncovered_sentences` | zur Stichprobe durch dich |
| `review_flags` | z. B. mögliche Verneinung, siehe Abschnitt 6 |

**Profil-Link-Listen** (nur lokal; schreibt der Sammler): eine Datei je Länderseite und Region; der Name enthält site_id und Regionsschlüssel in Kleinbuchstaben, z. B. `links_de_voralpenland.csv`. Den genauen Namen legen wir in Phase 3 fest.

**`local/samples/<site_id>/`** und **`local/structure/<site_id>/`** (nur lokal; schreibt das Erkundungsskript in Phase 2): gesicherte Seiten und ihre Struktur-Skelette. Die Skelette darfst du nach Prüfung mit Claude teilen, die gesicherten Seiten nie.

**`export/export_for_claude.csv`** (geht an Claude; lädst du selbst hoch)

| Spalte | Inhalt | Stufe |
|---|---|---|
| `farm_code` | | Phase 4 |
| `location`, `region` | | Phase 4 |
| `learning_categories` | | Phase 4 |
| `guestbook_count` | | Phase 4 |
| `available_windows` | | Phase 4 |
| `notes` | aus `notes.csv` | Phase 4 |
| `categories` | | Phase 6 |
| `coverage_percent` | | Phase 6 |
| `facts` | Steckbrief | Phase 6 |

Die Spalten der ersten Stufe überprüfen wir nach der Rückmeldung zur Attrappe (Phase 2).

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
  enabled: true                     # keep only if the calendar is readable (phase 2)
  date_from: "2027-03-01"           # earliest possible travel start
  date_to: "2027-10-31"             # adjust once the travel period is fixed
```

```yaml
# sites/de.yaml - draft; phase 2 fixes the format and explores the site, phase 3 adds search definitions and categories
base_url: "https://wwoof.de"        # exact form is checked by the user in phase 2
languages: ["de", "en"]             # language codes of the descriptions
regions:
  voralpenland:                     # region key: lower case, unique across all sites
    code: "VA"                      # region code in the farm code, unique within this site
    # search: defined after the country check (phase 2)
  sachsen:
    code: "SN"
learning_categories: []             # list from the country check (phase 2)
```

**Was `config.py` prüft** (Phase 2):
- Codes und Schlüssel sind Strings. Ein `no` ohne Anführungszeichen (Norwegen: site_id `"no"`) liest YAML als `false`; das wird mit klarer Meldung abgelehnt. Codes stehen deshalb immer in Anführungszeichen.
- `site` besteht aus genau zwei Kleinbuchstaben, und `sites/<site>.yaml` existiert (Vorschlag von Claude Code, Einspruch möglich: Unter Windows würde `"DE"` sonst `de.yaml` laden, unter Linux in GitHub Actions nicht).
- Nur bekannte Schlüssel, in beiden Dateien; doppelte Schlüssel werden abgelehnt (Vorschlag von Claude Code: PyYAML übernimmt nach bisherigem Kenntnisstand stillschweigend den letzten Wert; in Phase 2 per Test zu belegen).
- Die gewählte Region ist in der Länderseiten-Datei vorhanden.
- Regionsschlüssel sind klein und über alle Länderseiten eindeutig; dazu liest `config.py` die Regionsschlüssel aller Dateien in `sites/`. Regionskürzel sind innerhalb einer Länderseite eindeutig (Vorschlag von Claude Code).
- `base_url` beginnt mit `https://`.
- **Fehlende Suchdefinition ist zulässig:** Eine Region mit Schlüssel und Kürzel, aber ohne Suchdefinition ist gültig. Das ist der Zustand zwischen dem Festlegen der Regionen und der Länder-Prüfung (`07_bedienung.md`, Teil C). Erst der Sammler verlangt eine Suchdefinition (Phase 3).
- `learning_categories` darf bis zur Länder-Prüfung leer sein; verlangt wird die Liste erst vom Export-Selbsttest (Phase 4) (Vorschlag von Claude Code, Einspruch möglich).

### 5.5 Konventionen

- **Sprache:** Der Code ist komplett englisch: Bezeichner, Kommentare, Datei- und Ordnernamen, Spaltennamen, Konfigurationsschlüssel und Programmausgaben. Ausnahme sind Suchbegriffe in den Sprachen der Länderseiten (Taxonomie, Verneinungen, Regeln für den Steckbrief); sie werden nach Sprache getrennt (Abschnitte 6 und 7). Die `label`-Texte in `taxonomy.yaml` bleiben deutsch, weil sie nur Anzeigetexte für dich sind. Die Dokumentation bleibt deutsch.
- **YAML:** Codes (site_id, Sprachcodes, Regionskürzel) stehen immer in Anführungszeichen.
- **Dateinamen** aus site_id und Regionsschlüssel nur in Kleinbuchstaben.
- **CSV-Format (festgelegt am 17.11.2026 nach dem Test in Phase 1, Schritt 8):** Trennzeichen `;` und Kodierung UTF-8 mit BOM (`utf-8-sig`). Mit diesen Einstellungen öffnet ein deutsches Excel die Dateien per Doppelklick mit richtigen Spalten und Umlauten. Listen innerhalb eines Feldes werden mit `|` getrennt. Zeilenenden CRLF.
  - **Speichern in Excel nur als „CSV UTF-8 (durch Trennzeichen getrennt)“.** Damit blieben im Test BOM, Kodierung, Trennzeichen, Umlaute, mehrzeilige Felder und `|`-Listen erhalten.
  - **Excel wandelt Datumswerte um:** Aus `2026-11-08` wird beim Speichern `08.11.2026`. Deshalb:
    - Dateien, die nur Skripte schreiben (`farms.csv`, `keyword_report.csv`, Export), in Excel nur ansehen, nie speichern.
    - Bekommt eine Datei, die du bearbeitest, später eine Datumsspalte, liest das Skript sie in beiden Formaten (`JJJJ-MM-TT` und `TT.MM.JJJJ`).
  - Prüfwerkzeug: `python -m src.table_roundtrip prepare` und `compare` (nur mit der erfundenen Testdatei).
- **Tests:** pytest ab Phase 2, im Ordner `tests/`, nur mit erfundenen Höfen und erfundenen Länderseiten-Dateien unter `tests/fixtures/` (z. B. `base_url: "https://example.org"`), nie mit echten Dateien aus `sites/`. Erfundene Länderseiten bekommen Ländercodes, die ISO 3166-1 für Benutzerzwecke reserviert und nie einem Land zuteilt, z. B. `zz` oder `xa` (Vorschlag von Claude Code). Tests greifen nicht auf das Netz zu; robots.txt-Tests arbeiten mit erfundenem Text. Prüfungen, die zur Laufzeit abbrechen sollen (Grenzwerte, Export-Selbsttest), lösen eigene Fehler (Exceptions) aus statt `assert`, weil Python `assert`-Anweisungen mit der Option `-O` abschaltet.
- **Git:** Jede abgeschlossene Aufgabe wird ein Commit. Vor jedem Commit zeigt `git status`, was hineinkommt. Der Datenordner liegt außerhalb des Repositorys und ist zusätzlich per `.gitignore` ausgeschlossen.

---

## 6. Stichwort-Umwandlung ohne Informationsverlust

Die Stichwort-Kategorien strukturieren die Bewertung. Zusammen mit dem Steckbrief (Abschnitt 7) sind sie die einzige Information aus dem Beschreibungstext, die Claude erhält. Stichworte sind immer eine Verdichtung. „Nichts geht verloren“ wird deshalb so sichergestellt:

1. **Der Originaltext bleibt vollständig erhalten**, lokal und unverändert in `farms.csv`. Er ist die maßgebliche Quelle und wird nie gelöscht oder überschrieben (bis zur Löschung nach der Reise).
2. **Regelbasiert und KI-frei:** Eine Taxonomie (`taxonomy.yaml`) ordnet Begriffe und Synonyme Kategorien zu.
   - **Nach Sprache getrennt (Entscheidung vom 17.11.2026):** Suchbegriffe, Verneinungen und Ignorierliste stehen je Sprache. Angewendet werden nur die Sprachen der Länderseite, zu der ein Hof gehört (`languages` in `sites/<site_id>.yaml`, erkennbar am Länderteil des Hof-Codes); für Deutschland Deutsch und Englisch, da Profile teils englisch sind.
   - Grund: Begriffe kollidieren zwischen Sprachen (norwegisch „sau“ = Schaf, deutsch „Sau“ = Schwein).
   - Die Kategorienschlüssel bleiben sprachunabhängig.
   - Fehlen die Sprachdaten für eine Sprache der Länderseite, bricht die Stichwort-Erkennung für die betroffenen Höfe mit klarer Meldung ab (nur Hof-Code, site_id, Sprachcode).
   - Einzelheiten in `05_stichwort_taxonomie.md`, Abschnitt 5; die Umstellung des YAML-Entwurfs erfolgt in Phase 5.
3. **Whitelist-Prinzip:** Die Spalte `categories` enthält nur Kategorieschlüssel aus der Taxonomie, nie Freitext.
4. **Abdeckungsprüfung:** Die Beschreibung wird in Sätze zerlegt. Jeder Satz ohne relevanten Treffer wird lokal markiert. Der Bericht `keyword_report.csv` zeigt pro Hof den Anteil abgedeckter Sätze und listet die nicht abgedeckten Sätze, nur lokal.
5. **Nachschärfen per Stichprobe (seit 17.11.2026):** Du liest lokal eine Stichprobe der nicht abgedeckten Sätze, nicht alle. Steckt darin eine relevante Information, ergänzt du Taxonomie oder Steckbrief-Regeln und lässt das Skript erneut laufen. Das wiederholst du, bis sich zwei Runden kaum noch unterscheiden. Wiederkehrende irrelevante Sätze (Begrüßung, Familie und Ähnliches) markierst du über die Ignorierliste als „gesichtet, irrelevant“. Lies in jeder Runde außerdem einige **abgedeckte** Sätze stichprobenartig: Ein Satz mit einem Treffer kann weitere Informationen enthalten, die noch keiner Kategorie zugeordnet sind (z. B. „Der Bahnhof ist nah, wir holen dich ab“).
6. **Fehlerquellen im Deutschen** (für weitere Sprachen entsprechend bei der Länder-Prüfung):
   - **Verneinung:** „Wir haben keine Tiere“ enthält „Tiere“. Steht ein Verneinungswort der jeweiligen Sprache (kein, keine, nicht, ohne; no, not, without) kurz vor dem Treffer, setzt das Skript einen Prüfhinweis.
   - **Zusammengesetzte Wörter:** Teilwortsuche findet „Ziege“ in „Ziegenkäse“, aber auch „Rind“ in „Rinde“. Dagegen helfen Ausschlusslisten pro Kategorie.
   - **Umlaute und Groß-/Kleinschreibung:** Der Text wird vor dem Abgleich vereinheitlicht.
7. **Notizen für Feinheiten:** Umfang oder Qualität („großer Gemüsegarten“, „Käserei als Hauptbetrieb“) lassen sich nicht in Kategorien fassen. Dafür gibt es `notes.csv` (Abschnitt 5.3): Notizen in deinen eigenen Worten, ohne Personenbezug. Sie gehen mit dem Export an Claude.
8. **Taxonomie mit Claude besprechen:** Neue Begriffe und Kategorien kannst du mit Claude abstimmen, ohne Satzkontext aus Profilen. Beispiel: „Gehört ‚Mob Grazing‘ zu Tierhaltung oder zu Weidemanagement?“

---

## 7. Hof-Steckbrief statt Bereinigung (Entscheidung vom 17.11.2026)

**Ziel:** Claude erhält aus der Beschreibung möglichst viel verwertbare Information, ohne dass Personendaten enthalten sein können und ohne dass du jede Beschreibung prüfen musst.

**Prinzip Positivliste:** Ein KI-freies Skript formt jede Beschreibung in einen **Steckbrief** um. Er besteht nur aus Schlüsseln und Werten eines festen Schemas, z. B. `accommodation=caravan`, `pickup=yes`, `work_hours_per_day=5`, `station_walk_minutes=10`. Die Werte sind feste Begriffe aus dem Schema, Zahlen oder Wahrheitswerte, nie Text aus der Beschreibung. Namen, Kontakt- und Adressdaten sind damit durch den Aufbau ausgeschlossen; Bereinigung und Freigabe entfallen.

- **Auslesen:** regelbasiert je Sprache, wie die Taxonomie (Abschnitt 6), z. B. „10 Minuten zu Fuß vom Bahnhof“ → `station_walk_minutes=10`. Angewendet werden nur die Sprachen der Länderseite des Hofs; fehlen Regeln für eine dieser Sprachen, bricht das Skript für die betroffenen Höfe mit klarer Meldung ab.
- **Schema:** legen wir in Phase 5 fest, abgeleitet aus deinen Auswahlkriterien (offener Punkt 3 in `00_projekt_uebersicht.md`) und der Rückmeldung zur Attrappe aus Phase 2. Es steht in `taxonomy.yaml` neben den Kategorien.
- **Bericht:** `keyword_report.csv` zeigt je Hof Kategorien und Steckbrief. Du prüfst per Stichprobe, ob die Regeln richtig greifen, nicht jeden Hof.
- **Selbsttest** (Phase 6): Jeder Schlüssel und jeder Wert muss im Schema stehen, sonst bricht der Export ab.
- **Grenze:** Nuancen aus dem Freitext gehen verloren. Ausgleich: Stichwort-Kategorien, deine Notizen und das Lesen der Profile der engeren Auswahl, das du vor einer Anfrage ohnehin auf der Länderseite machst.
- **Verworfen:** die Bereinigung des Freitexts mit Prüfung jeder Beschreibung (geplant bis 17.11.2026) und das Umformulieren mit einem lokalen Sprachmodell (nicht KI-frei; frei formulierter Text wäre nicht sicher frei von Namen).

---

## 8. Lernplan

**Arbeitsweise:** siehe `CLAUDE.md`. Claude Code schreibt den Code schrittweise; du steuerst, prüfst, lernst und pushst. Jede Phase ist erst fertig, wenn ihre Abnahmekriterien erfüllt sind, `07_bedienung.md` ihre neuen Teile beschreibt und du ihren Code erklären kannst.

**Neuausrichtung vom 17.11.2026:** Die Erkundung der Länderseite kommt direkt nach den Grundlagen, damit alle weiteren Schritte auf dem tatsächlichen Aufbau der Seite beruhen. Die Übungen auf toscrape.com sind in das Erkundungsskript integriert, und ein schlanker Export folgt direkt auf den Sammler. Die Zuordnung zur alten Nummerierung steht in `08_entscheidungsprotokoll.md`.

### Phase 0 – Einrichtung (erledigt 06.11.2026)

- **Ergebnis:** Laptop eingerichtet, Code- und Datenordner getrennt, privates GitHub-Repository, Claude Code mit Sperre des Datenordners.
- **Fertig:** Checkliste in `04_technische_voraussetzungen.md`, Abschnitt 9.

### Phase 1 – Python-Grundlagen am eigenen Projekt (erledigt 17.11.2026)

- **Gelernt:** Listen, Dictionaries, Funktionen, CSV lesen und schreiben, Fehlerbehandlung, erste Schritte mit pandas.
- **Ergebnis:** erfundene Testtabelle `tests/fixtures/farms_sample.csv`; `src/farm_table.py`, `filter_region.py`, `farm_stats.py`, `farm_pandas.py`, `table_roundtrip.py`; CSV-Format festgelegt (Abschnitt 5.5).

### Phase 2 – Länderseite erkunden (erste Länder-Prüfung: Deutschland)

- **Ziel:** den tatsächlichen Aufbau der Länderseite kennen, bevor der Sammler entsteht, und daraus erfundene Testseiten bauen, auf denen alle weiteren Schritte aufbauen. Zugleich die Länder-Prüfung für Deutschland nach `07_bedienung.md`, Teil C, Schritt 6.
- **Gate für deinen Lauf auf wwoof.de:** Abklärung erledigt (gilt für alle CWP-Länderseiten), Mitgliedschaft aktiv, robots.txt-Prüfung umgesetzt (Aufgabe 1), Skript auf toscrape.com getestet (Aufgabe 2).
- **Du lernst:** pytest, GitHub Actions, YAML und seine Fallen, eigene Exceptions, `urllib.robotparser`, HTML, CSS und DOM (am Skelett), Playwright (persistentes Profil, Warten auf JavaScript-Inhalte, Login), Entwicklerwerkzeuge des Browsers.
- **Aufgaben:**
  1. **Grundlagen:** pytest und ein GitHub-Actions-Workflow (Tests bei jedem Push); `robots_check.py` mit Tests an erfundenem robots.txt-Text; `config.load_site()` lädt und prüft `sites/<site>.yaml` (Prüfungen in Abschnitt 5.4); `sites/de.yaml` mit `base_url`, `languages` und den Regionen `voralpenland` (`VA`) und `sachsen` (`SN`) nur mit Schlüssel und Kürzel; Tests mit erfundenen Länderseiten, darunter `site: no` ohne Anführungszeichen und eine Region ohne Suchdefinition.
  2. **Erkundungsskript** `src/explore_site.py` mit `src/page_skeleton.py` (siehe unten), Tests an erfundenem HTML; Claude Code testet das Skript auf quotes.toscrape.com (Login, JavaScript-Seite `/js/`), ohne Fenster, Ausgaben nach `out/`.
  3. **Dein Lauf:** Vorab-Sichtung von Hand (Regionsfilter, ungefähre Hofzahlen je Region, Gästebuch-Anzahl, Kalender, Lernkategorien, URL-Muster); dann Lauf auf wwoof.de (Suchseite je Region, 2–3 Profile, bei Bedarf Reiter wie Gästebuch oder Kalender); Skelette prüfen und teilen.
  4. **Auswertung:** Aufbau dokumentieren (Abschnitt 4: was plattformweit und was länderspezifisch ist, und an welcher Stelle im Code das Plattformweite steht); Entwurf der Selektoren; Regel für die Normalisierung von `profile_url` (mit Domain); prüfen, ob eine Lernkategorie das Zeichen `|` enthält; offene Punkte 10 (Voralpenland), 11 (Umfang) und 12 (Kalender) entscheiden; erfundene Testseiten mit demselben Aufbau in `tests/fixtures/pages/`.
  5. **Attrappe:** Claude Code erzeugt einen erfundenen Export im geplanten Format in `out/`; du testest im claude.ai-Projekt, ob Bewertung und Routenplanung damit gelingen; Export-Spalten und Anforderungen an den Steckbrief festhalten.
- **Erkundungsskript:**
  - Aufruf durch dich: `python -m src.explore_site --site de --data-dir <Datenordner> <URL> [<URL> …]`. Die URLs gibst du an; jede muss mit der `base_url` der Länderseite beginnen. So steht keine Domain im Code.
  - Ablauf: robots.txt prüfen; Browser mit dem Profil `browser_profile/<site>/`, bei Bedarf Login von Hand und Bestätigen mit Enter; je URL Seite öffnen und warten, bei Status ab 400 Abbruch; gerenderte Seite **nur lokal** in `local/samples/<site>/` sichern, Skelett in `local/structure/<site>/` schreiben; Pause 10–20 Sekunden; **harte Grenze 5 Seiten pro Lauf**; im Terminal nur Zähler, Dateinamen und Status.
  - Skelett: `script`, `style`, `svg`, Kommentare und `meta` entfernt; Text wird zu `⟨TEXT:n⟩` bzw. `⟨NUM:n⟩` (n = Länge); alle Attributwerte außer `class`, `role` und `type` werden zu `⟨VAL:n⟩`, Links zu `⟨URL⟩`; gleichartige Geschwister werden zusammengefasst (die ersten zwei und „× N“); die Größe ist begrenzt.
  - Das Skelett darfst du nach deiner Prüfung (Checkliste in `07_bedienung.md`, Teil A.0) mit Claude teilen (`02_regeln_und_rahmenbedingungen.md`, Abschnitt 2). Die gesicherten Seiten bleiben lokal; mit ihnen prüfst du in Phase 3 den Leser offline, ohne erneute Seitenaufrufe.
  - Seitenaufrufe der Erkundung sind keine Erfassung: In `farms.csv` kommt ein Hof erst durch den Sammler.
- **Fertig, wenn:**
  - `python -m pytest` ohne Fehler durchläuft und der Workflow auf GitHub grün ist,
  - Konfigurationsfehler (z. B. `site: no` ohne Anführungszeichen, unbekannter Schlüssel) mit klarer Meldung abgelehnt werden und eine Region ohne Suchdefinition angenommen wird,
  - das Erkundungsskript auf toscrape.com getestet ist,
  - die Skelette von Suchseite und Profilseite geprüft und geteilt sind,
  - der Aufbau dokumentiert ist (Regionsfilter, URL-Aufbau und Normalisierung, Login-Sitzung, Gästebuch-Anzahl, Kalender, Lernkategorien) und die erfundenen Testseiten stehen,
  - die Rückmeldung zur Attrappe festgehalten ist,
  - `07_bedienung.md` die Erkundung (Teil A.0) und die robots.txt-Prüfung beschreibt.

### Phase 3 – Hof-Sammler

- **Vorher:** Gesamtumfang und Tagesgrenze festlegen, auch ob sie je Länderseite oder insgesamt gelten (offener Punkt 11).
- **Du lernst:** Programmstruktur über mehrere Dateien, Logging, robuste Fehlerbehandlung, Fortsetzbarkeit, Abgleich von Datensätzen.
- **Aufgaben:**
  - `config.py` lädt zusätzlich `config.yaml` (Abschnitt 5.4; harte Grenze 50 fest im Code).
  - `sites/de.yaml`: Suchdefinitionen und `learning_categories` aus Phase 2.
  - `region_list.py`, `profile_reader.py` und `collector.py` nach dem Ablauf in Abschnitt 4, entwickelt und getestet an den erfundenen Testseiten aus Phase 2. Vor dem ersten echten Lauf prüfst du `profile_reader` offline an den lokal gesicherten Seiten.
  - Hat die gewählte Region keine Suchdefinition, bricht der Sammler vor dem ersten Seitenaufruf ab (mit Test).
  - Hof-Codes, Abgleich über die normalisierte Profil-URL (auch in `find_duplicate_profile_urls`), Link-Listen und Log-Einträge mit site_id; Fehler, wenn ein Listenwert das Trennzeichen `|` enthält.
  - Spalte `displayed_names` aus `FARM_COLUMNS` und der Fixture entfernen.
  - `07_bedienung.md`, Teil A, vollständig.
- **Fertig, wenn:** eine Region (z. B. das Voralpenland) erfasst ist, alle Grenzen eingehalten wurden, jeder Hof genau einmal mit genau einem Hof-Code in `farms.csv` steht (geprüft mit einem pytest-Test an erfundenen Daten und einer Prüffunktion für die echte Tabelle), das Log keine Hofdaten enthält und `07_bedienung.md`, Teil A, den Sammellauf beschreibt.

### Phase 4 – Erster Export (schlank)

- **Ziel:** so früh wie möglich eine Grundlage für die Reiseplanung, noch ohne Stichworte und Steckbrief.
- **Du lernst:** Prüfungen zur Laufzeit mit eigenen Exceptions, pytest-Tests dafür, Datenschutz als Code.
- **Aufgaben:** `export.py` schreibt `export/export_for_claude.csv` mit den Spalten der ersten Stufe (Abschnitt 5.3, angepasst nach der Rückmeldung zur Attrappe). Selbsttest vor dem Schreiben:
  - nur Whitelist-Spalten;
  - `farm_code` hat das Format `LAND-REGION-NNN`, ist eindeutig, und sein Länderteil gehört zu einer bekannten Länderseite;
  - kein Hofname erscheint in irgendeinem Feld;
  - `learning_categories` enthält nur Kategorien aus der Liste der Länderseite des Hofs; ist diese Liste leer, bricht der Export ab;
  - `guestbook_count` ist eine ganze Zahl ab 0;
  - `location` ist kurz und enthält keine Ziffern;
  - `available_windows` hat das festgelegte Format und liegt im konfigurierten Zeitraum;
  - `notes` enthält keinen Hofnamen und keine Kontaktmuster (E-Mail, Web-Adresse, @-Namen, längere Ziffernfolgen).
- **Fertig, wenn:** der Export den Selbsttest besteht, du ihn in das claude.ai-Projekt hochladen kannst und `07_bedienung.md`, Teil B, Export und Hochladen beschreibt.

### Phase 5 – Stichworte und Steckbrief

- **Du lernst:** Textverarbeitung (Normalisierung, Zerlegen in Sätze, Wortsuche), reguläre Ausdrücke, Auswertungsberichte.
- **Aufgaben:**
  - `taxonomy.yaml` aus `05_stichwort_taxonomie.md` übernehmen und nach Sprache umstellen.
  - Steckbrief-Schema festlegen und Regeln zum Auslesen je Sprache schreiben (Abschnitt 7).
  - `tagging.py` schreibt `keyword_report.csv` (Kategorien, Steckbrief, Abdeckung, nicht abgedeckte Sätze).
  - pytest-Tests an erfundenen Texten, darunter die Beschreibungen der Fixture mit erfundenen Namen und Kontaktdaten: Diese dürfen nie im Steckbrief erscheinen.
  - Fehlen Sprachdaten für die Länderseite eines Hofs, bricht das Skript für die betroffenen Höfe mit klarer Meldung ab (mit Test).
- **Fertig, wenn:** die Tests bestehen, Taxonomie und Regeln per Stichprobe nachgeschärft sind, bis sich zwei Runden kaum noch unterscheiden, und `07_bedienung.md`, Teil B, Stichworte und Steckbrief beschreibt.

### Phase 6 – Vollständiger Export

- **Aufgaben:** Export um `categories`, `coverage_percent` und `facts` erweitern. Selbsttest zusätzlich: `categories` enthält nur Schlüssel aus der Taxonomie; jeder Schlüssel und jeder Wert in `facts` steht im Schema; für jeden Hof sind die Sprachdaten seiner Länderseite vorhanden.
- **Fertig, wenn:** der Export den Selbsttest besteht, du ihn hochladen kannst und `07_bedienung.md` aktualisiert ist. Claude bewertet dann und plant die Route.

---

## 9. Ausbaustufen (später, optional)

- **Weitere Felder:**
  - Durchschnittsbewertung, falls die Plattform eine als Zahl anzeigt.
  - Freie Zeitfenster aus dem Kalender, falls sie sich in Phase 2 als nicht gut machbar für die erste Version erweisen (bis dahin pflegst du sie von Hand).
- **Planungsskripte**, die mit deiner eigenen Tabelle arbeiten, nicht mit der Plattform:
  - Bewertungsskript mit gewichteten Punkten und Rangliste.
  - Routenplaner: Orte in Koordinaten umwandeln, Reihenfolge mit Zeitfenstern optimieren, z. B. mit Google OR-Tools.
  - Kartendarstellung, z. B. mit folium.
  - Kontaktplaner: Anfragetermine berechnen, Nachrichtenentwürfe aus Vorlagen erzeugen.
  - Für Dienste zur Ortsbestimmung oder für Fahrpläne vorher deren Nutzungsbedingungen prüfen.
- **Weitere Länder (Entscheidung vom 17.11.2026):**
  - Weitere Länderseiten der CWP kommen nur über die Checkliste in `07_bedienung.md`, Teil C, dazu, ohne Codeänderung, solange die Länder-Prüfung keine Abweichung zeigt.
  - **Norwegen** (wwoofnorway.org, site_id `"no"`) ist der nächste Kandidat: eigene Mitgliedschaft, robots.txt-Prüfung, Länder-Prüfung mit dem Erkundungsskript, norwegische Sprachdaten für Taxonomie und Steckbrief.
  - **Irland** (wwoof.ie) hat eine eigene Plattform und gehört nicht zum Umfang: kein Code und keine Vorbereitung dafür.

---

## 10. Datenschutz im Code

Was du mit Claude teilen darfst und was nicht, regelt `02_regeln_und_rahmenbedingungen.md`, Abschnitt 2. Für den Code gilt zusätzlich:

- Logs, Zusammenfassungen und Fehlermeldungen enthalten nur Hof-Codes, site_id, Zahlen und Status.
- Selektoren entstehen über die Struktur (CSS-Klassen, Attribute, Position), nicht über sichtbare Texte. `playwright codegen` erzeugt oft textbasierte Selektoren; diese werden ersetzt.
- Der Datenordner liegt außerhalb des Repositorys und ist zusätzlich per `.gitignore` ausgeschlossen (siehe Datei im Repository).

---

## Quellen

- Übungsseiten: https://toscrape.com
- Playwright für Python, Dokumentation: https://playwright.dev/python/docs/intro
- WWOOF-bezogene Quellen: siehe `02_regeln_und_rahmenbedingungen.md`
