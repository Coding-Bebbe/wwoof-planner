# Technische Voraussetzungen: Laptop einrichten (Windows)

**Stand:** 06.11.2026 (Phase 0 abgeschlossen), ergänzt am 15.11.2026 (Abschnitt 8: Arbeitsweise mit Claude Code) und am 17.11.2026 (Länderseiten der CWP: Abschnitte 1, 3, 8). Die Versionsangaben zu Python wurden am 31.10.2026 geprüft; bei späterer Einrichtung die aktuellen Hinweise auf python.org beachten.

**Gerät des Nutzers:** privater Windows-Laptop (Surface Pro 8). Diese Anleitung beschreibt deshalb nur Windows. Alle Befehle laufen in der **PowerShell**.

---

## 1. Übersicht

| Komponente | Zweck | Hinweis |
|---|---|---|
| Betriebssystem | | Windows. Die Prozessorarchitektur prüfst du in Abschnitt 5 (erwartet: `AMD64`, also 64-Bit-Intel). |
| Rechte | Software installieren | privater Laptop |
| Speicherplatz | Python, Pakete, Browser | ca. 2 GB als großzügiger Puffer; der Chromium-Browser für Playwright braucht einige hundert MB |
| **Python** | Programmiersprache | **Empfehlung 3.13**, 3.14 sollte ebenfalls funktionieren. **Mindestens 3.11**, weil pandas 3.x Python 3.11 oder neuer voraussetzt (Playwright selbst braucht 3.9 oder neuer). |
| **VS Code** mit der Python-Erweiterung von Microsoft | Editor | kostenlos, code.visualstudio.com |
| PowerShell | Befehle ausführen | in Windows enthalten |
| venv | Projektpakete isolieren | in Python enthalten |
| **Playwright** (Python-Paket) und **Chromium** | Browser-Automatisierung | per pip, Browser per `playwright install` |
| **pandas** | Tabellen | per pip |
| **PyYAML** | Konfiguration und Taxonomie lesen | per pip |
| **pytest** | Tests | per pip |
| openpyxl | optional: Excel-Export | per pip |
| **Git** (Git for Windows) | Versionsverwaltung | **Pflicht**; bringt den Git Credential Manager für die Anmeldung bei GitHub mit |
| **GitHub-Konto** | privates Repository | **Pflicht** |
| **Claude Code** (lokal) | schreibt seit dem 15.11.2026 den Code | Einrichtung und Absicherung in Abschnitt 8 |
| WWOOF-Mitgliedschaft je Länderseite | Zugang zu Hofprofilen | Deutschland aktiv (01.11.2026), ab Phase 4 nötig; jede weitere Länderseite braucht eine eigene (`07_bedienung.md`, Teil C) |

---

## 2. Python installieren

python.org empfiehlt unter Windows inzwischen den **Python Install Manager**. Der klassische Installer wird mit Python 3.16 eingestellt.

1. **Python Install Manager** aus der Microsoft-Store-App installieren (von python.org empfohlen) oder unter python.org/downloads herunterladen.
2. PowerShell öffnen. Beim ersten Start läuft ein Konfigurationsprüfer; Standardvorschläge übernehmen. Eine Frage zum PATH mit Ja beantworten.
3. Python 3.13 installieren und prüfen:
   ```powershell
   py install 3.13
   py -V:3.13 --version
   ```
4. Hinweis: Ist von früher noch der alte „Python Launcher“ installiert, empfiehlt python.org, ihn zu deinstallieren, weil beide den Befehl `py` nutzen.

---

## 3. Ordner und virtuelle Umgebung

**Zwei getrennte Ordner** (siehe `03_programmierprojekt.md`, Abschnitt 5.1): `wwoof-planner` für den Code (wird das Git-Repository) und `wwoof-data` für alle Hofdaten. Beide liegen nebeneinander im Ordner `Projekte` in deinem Benutzerordner.

**Wichtig:** Lege die Ordner nicht im Desktop- oder Dokumente-Ordner an, falls dort die OneDrive-Sicherung aktiv ist. Die Hofdaten sollen den Laptop nicht verlassen.

```powershell
mkdir $HOME\Projekte\wwoof-planner
mkdir $HOME\Projekte\wwoof-data
cd $HOME\Projekte\wwoof-planner
```

Virtuelle Umgebung im Code-Ordner erstellen und aktivieren:

```powershell
py -V:3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Blockiert PowerShell die Aktivierung mit einer Meldung zur Ausführungsrichtlinie, einmalig ausführen und danach erneut aktivieren:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Nach der Aktivierung steht `(.venv)` vor der Eingabezeile. Ab jetzt bezieht sich `python` auf die virtuelle Umgebung.

Die Unterordner im Datenordner (`browser_profile` mit einem Unterordner je Länderseite, z. B. `browser_profile\de`, sowie `local`, `export`, `logs`) legt das Skript später selbst an.

---

## 4. Pakete und Browser installieren

Bei aktivierter virtueller Umgebung:

```powershell
python -m pip install --upgrade pip
python -m pip install playwright pandas pyyaml pytest openpyxl
python -m playwright install chromium
```

Installierte Versionen festhalten, damit die Umgebung später reproduzierbar ist:

```powershell
python -m pip freeze | Out-File -Encoding utf8 requirements.txt
```

Grund für `Out-File`: Die in Windows vorinstallierte PowerShell 5.1 schreibt mit `>` umgeleitete Ausgaben als UTF-16. Das stört später beim Anzeigen auf GitHub.

---

## 5. Installation prüfen

**Schritt 1: Versionen, Architektur und Importe**

```powershell
python --version
python -c "import platform; print(platform.machine())"
python -c "import pandas, yaml, playwright, pytest; print('Packages OK')"
```

Erwartet: Python 3.13.x, `AMD64` und `Packages OK`. Zeigt die zweite Zeile etwas anderes (z. B. `ARM64`), schick Claude die Ausgabe.

**Schritt 2: Playwright-Test.** Datei `test_playwright.py` im Code-Ordner anlegen:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")
    print("Page title:", page.title())
    browser.close()
```

Ausführen:

```powershell
python test_playwright.py
```

Erwartet: Ein Browserfenster öffnet sich kurz, und im Terminal steht der Seitentitel der Übungsseite. Die Datei ist nur ein Einrichtungstest; sie kommt nicht ins Repository.

---

## 6. VS Code einrichten

1. VS Code von code.visualstudio.com installieren.
2. Die Erweiterung **Python** (Herausgeber: Microsoft) installieren.
3. Den Ordner `wwoof-planner` öffnen (Datei → Ordner öffnen). Nicht den Oberordner `Projekte` öffnen.
4. Befehlspalette öffnen (Strg+Umschalt+P) und **„Python: Select Interpreter“** wählen. Dort den Interpreter aus `.venv` auswählen.
5. Im integrierten Terminal (Terminal → Neues Terminal) sollte `(.venv)` erscheinen.

---

## 7. Git und GitHub

### 7.1 Git installieren

```powershell
winget install --id Git.Git -e --source winget
```

Alternativ den Installer von git-scm.com nutzen. Danach PowerShell schließen, neu öffnen und prüfen:

```powershell
git --version
```

### 7.2 GitHub-Konto und E-Mail-Schutz

1. Auf github.com ein Konto anlegen, falls noch keins vorhanden ist.
2. In den GitHub-Einstellungen unter „Emails“ die Option **„Keep my email addresses private“** aktivieren. GitHub zeigt dann eine noreply-Adresse an (Form: `ID+BENUTZERNAME@users.noreply.github.com`). Mit dieser Adresse steht deine echte E-Mail-Adresse nicht in den Commits.

### 7.3 Git einrichten

```powershell
git config --global user.name "Dein Name"
git config --global user.email "ID+BENUTZERNAME@users.noreply.github.com"
git config --global init.defaultBranch main
```

### 7.4 Privates Repository anlegen und verbinden

1. Auf GitHub ein neues Repository `wwoof-planner` anlegen: Sichtbarkeit **Private**, **ohne** README, `.gitignore` und Lizenz. So klappt der erste Push ohne Konflikt.
2. Im Code-Ordner die Datei `.gitignore` mit dem Inhalt aus `03_programmierprojekt.md`, Abschnitt 10, anlegen (inklusive `.venv/`).
3. Repository anlegen, prüfen und hochladen:

```powershell
git init
git status
git add .gitignore requirements.txt
git commit -m "Initial commit"
git remote add origin https://github.com/BENUTZERNAME/wwoof-planner.git
git push -u origin main
```

Beim ersten Push öffnet sich ein Anmeldefenster für GitHub (Git Credential Manager).

### 7.5 Täglicher Ablauf

```powershell
git status                       # what has changed?
git add <file>                   # stage specific files
git commit -m "Short message"    # save a snapshot
git push                         # upload to GitHub
```

Vor jedem Commit mit `git status` prüfen, dass nur Code, Konfiguration, Taxonomie und erfundene Testdaten dabei sind. Seit dem 15.11.2026 macht Claude Code `git add` und `git commit` nach deinem OK; `git push` machst nur du.

---

## 8. Claude Code einrichten

**Entscheidung vom 01.11.2026:** Wir arbeiten mit Claude Code lokal auf deinem Laptop. Claude Code arbeitet direkt im Code-Ordner: Es kann dort Dateien anlegen, Tests ausführen und dir Befehle vorschlagen. Bei dir ist die VS-Code-Erweiterung „Claude Code for VS Code“ vorhanden (Panel rechts im Editor). Die Einrichtung ist seit dem 06.11.2026 abgeschlossen (Checkliste, Abschnitt 9). **Seit dem 15.11.2026** schreibt Claude Code den Code; die Arbeitsweise steht in `CLAUDE.md` und `docs/arbeiten_mit_claude_code.md`.

**Datenordner sperren** (siehe `03_programmierprojekt.md`, Abschnitt 5.1):

1. Claude Code immer im Ordner `wwoof-planner` starten, nie in `wwoof-data` oder `Projekte`.
2. Eine Read-Deny-Regel für den Datenordner anlegen. Unter Windows werden Pfade dafür in POSIX-Form geschrieben: Aus `C:\Users\…` wird `//c/Users/…`. Beispiel (Benutzername ersetzen):
   ```json
   {
     "permissions": {
       "deny": ["Read(//c/Users/BENUTZER/Projekte/wwoof-data/**)"]
     }
   }
   ```
   Laut Doku sperrt eine Read-Deny-Regel auch das Bearbeiten und Anlegen von Dateien unter diesem Pfad. Empfohlene Ablage: die Benutzer-Einstellungsdatei `C:\Users\BENUTZER\.claude\settings.json` (`~/.claude/settings.json`). Sie gilt in jedem Start von Claude Code, unabhängig vom Ordner. Bestehende Einträge bleiben erhalten, nur `permissions` kommt dazu (Komma nach dem vorherigen Eintrag, keines nach dem letzten). Ein einzelner `/` am Anfang eines Pfads ist laut Doku keine absolute Angabe; deshalb `//c/…`. Mit `/permissions` (in der Erweiterung auch über „Permissions“ im Bereich „Customize“) prüfst du, dass die Regel samt Quelldatei aufgelistet wird.
3. **Modus (seit 15.11.2026):** „Edit automatically“ (`acceptEdits`). Claude Code ändert Dateien im Code-Ordner ohne Rückfrage und fragt vor Befehlen nach. Den Startmodus legt die VS-Code-Benutzereinstellung `claudeCode.initialPermissionMode` fest; die Erweiterung liest ihn laut Doku nicht aus der Projektdatei. Die Projektdatei `.claude/settings.json` sperrt Auto-Modus und Bypass, verbietet `git push` und lässt Claudes Dateiwerkzeuge nichts außerhalb des Repositorys lesen. Bis zum 15.11.2026 galt der Modus „Manual“.
4. Sperre testen: eine Datei `access_test.txt` in `wwoof-data` anlegen. Als Kontrolle zuerst `requirements.txt` lesen lassen (muss klappen), dann Claude bitten, `access_test.txt` zu lesen. Erwartet: Der Zugriff wird abgelehnt. Danach die Datei löschen. (Erledigt am 06.11.2026.)
5. Editor-Kontext beachten: Das Panel zeigt die gerade geöffnete Datei als Kontext. Öffne keine Dateien aus `wwoof-data` im Editor, solange das Panel offen ist. GitHub Copilot ist seit dem 15.11.2026 für diesen Arbeitsbereich abgeschaltet (Einstellung `chat.disableAIFeatures` in den Arbeitsbereichseinstellungen).

**Grenze:** Die Deny-Regel greift nicht bei Skripten, die Dateien selbst öffnen (z. B. ein Python-Skript), und die Sandbox von Claude Code, die das auf Betriebssystemebene verhindern würde, läuft nicht unter nativem Windows. Deshalb gilt zusätzlich: Claude startet keine Skripte, die eine Länderseite der CWP aufrufen oder echte Daten verarbeiten, und du prüfst jeden Befehl, bevor du ihn freigibst. Echte Läufe startest du selbst in einem eigenen PowerShell-Fenster.

---

## 9. Checkliste „Phase 0 erledigt“

Stand 06.11.2026: alle Punkte laut Nutzer erfüllt.

- [x] Python 3.13 (mindestens 3.11) installiert, Version und Architektur geprüft
- [x] Ordner `wwoof-planner` (Code) und `wwoof-data` (Daten) nebeneinander angelegt, nicht in einem OneDrive-Ordner
- [x] Virtuelle Umgebung `.venv` im Code-Ordner
- [x] Pakete installiert: playwright, pandas, pyyaml, pytest, openpyxl
- [x] Chromium für Playwright installiert
- [x] `test_playwright.py` öffnet die Übungsseite und zeigt den Titel
- [x] VS Code nutzt den Interpreter aus `.venv`
- [x] `requirements.txt` erzeugt
- [x] Git installiert und eingerichtet (Name, noreply-Adresse, Standardzweig `main`)
- [x] Privates GitHub-Repository `wwoof-planner` angelegt, `.gitignore` vorhanden, erster Commit hochgeladen
- [x] Claude Code installiert, Read-Deny-Regel für `wwoof-data` angelegt und getestet: Ein Leseversuch auf eine Testdatei im Datenordner wird abgelehnt (offener Punkt 9)
- [x] WWOOF-Deutschland-Mitgliedschaft aktiv (01.11.2026); Vollständigkeit des Profils prüfst du in Phase 4

---

## 10. Häufige Probleme

| Problem | Lösung |
|---|---|
| `python` oder `py` wird nicht gefunden | PowerShell schließen und neu öffnen; Konfigurationsprüfer erneut ausführen: `py install --configure` |
| Aktivierung der venv blockiert | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (Abschnitt 3) |
| `ModuleNotFoundError` | venv nicht aktiviert oder falscher Interpreter in VS Code |
| Playwright: Browser fehlt | `python -m playwright install chromium` |
| `git` wird nicht gefunden | PowerShell nach der Installation neu öffnen |
| Push wird abgelehnt (`rejected`) | Meist wurde das Repository auf GitHub mit README angelegt. Fehlermeldung an Claude schicken. |
| `requirements.txt` sieht auf GitHub seltsam aus | Mit `>` erzeugt (UTF-16); mit dem Befehl aus Abschnitt 4 neu erzeugen |
| Download scheitert (Proxy, Firewall) | anderes Netz nutzen |

Fehlermeldungen kannst du Claude komplett schicken, solange sie keine Hofdaten enthalten.

---

## Quellen

- Python unter Windows (Python Install Manager): https://docs.python.org/using/windows.html
- Python Install Manager, Downloadseite: https://www.python.org/downloads/latest/pymanager
- pandas-Releases (pandas 3.x setzt Python 3.11+ voraus): https://github.com/pandas-dev/pandas/releases
- Playwright für Python: https://playwright.dev/python/docs/intro
- Git for Windows: https://git-scm.com
- GitHub, Commit-E-Mail-Adresse festlegen (noreply-Adresse): https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address
- Claude Code, Berechtigungen (Deny-Regeln, Windows-Pfade): https://code.claude.com/docs/en/permissions
- Claude Code, Berechtigungsmodi (Startmodus, Auto-Modus sperren): https://code.claude.com/docs/en/permission-modes
- Claude Code in VS Code: https://code.claude.com/docs/en/vs-code
- Claude Code, Sandbox (nicht unter nativem Windows): https://code.claude.com/docs/en/sandboxing
- VS Code, KI-Funktionen abschalten: https://code.visualstudio.com/docs/setup/copilot
- Übungsseite: https://toscrape.com
