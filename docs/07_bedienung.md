# Bedienung des Hof-Sammlers

**Stand:** 18.11.2026 · Anleitung für dich. Sie wächst mit den Phasen: Eine Phase ist erst fertig, wenn hier die Bedienung ihrer neuen Teile beschrieben ist. Teile, die es noch nicht gibt, sind mit **„noch nicht gebaut (Phase X)“** gekennzeichnet. Maßgeblich für den Aufbau ist `03_programmierprojekt.md`.

---

## Begriffe

| Begriff | Bedeutung | Beispiel |
|---|---|---|
| Länderseite | Seite einer WWOOF-Landesorganisation auf der Common WWOOF Platform (CWP) | wwoof.de, wwoofnorway.org |
| site_id | Ländercode nach ISO 3166-1 Alpha-2 in Kleinbuchstaben; zugleich Name der Länderseiten-Datei | `"de"` → `sites/de.yaml` |
| Länderseiten-Datei | `sites/<site_id>.yaml`: nur Länderdaten (`base_url`, `languages`, `regions`, `learning_categories`) | `sites/de.yaml` |
| Regionsschlüssel | Name der Region in `config.yaml` und in der Spalte `region`; klein geschrieben, über alle Länderseiten eindeutig | `voralpenland` |
| Regionskürzel | Teil des Hof-Codes; innerhalb einer Länderseite eindeutig | `VA` |
| Suchdefinition | wie die Suche einer Region auf der Länderseite aufgerufen wird; entsteht in der Länder-Prüfung | (Format ab Phase 2) |
| Hof-Code | `LAND-REGION-NNN`; LAND ist die site_id in Großbuchstaben | `DE-VA-001` |
| Länder-Prüfung | Erkundung einer Länderseite mit dem Erkundungsskript (A.0; Teil C, Schritt 6) | Phase 2 für Deutschland |
| Struktur-Skelett | Aufbau einer Seite ohne Inhalte: Texte und Attributwerte durch Platzhalter ersetzt | `div.card > ⟨TEXT:42⟩` |
| Steckbrief | Angaben aus der Beschreibung als Schlüssel und Werte eines festen Schemas, kein Freitext | `pickup=yes` |

---

## Teil A – Erkundung und Sammellauf

### A.0 Länderseite erkunden

Zweck: den Aufbau einer Länderseite kennenlernen, bevor der Sammler entsteht (Länder-Prüfung, Teil C, Schritt 6). Seitenaufrufe der Erkundung sind keine Erfassung; in `farms.csv` kommt nichts.

1. **Vorab von Hand:** Sieh dir die Länderseite als Mitglied im normalen Browser an und notiere nur Strukturen und Zahlen:
   - Wie filtert die Suche nach Regionen?
   - Wie viele Höfe gibt es ungefähr je Region?
   - Ist die Gästebuch-Anzahl als Zahl sichtbar?
   - Gibt es einen Kalender?
   - Werden Lernkategorien angezeigt?
   - Wie sind Profil-URLs aufgebaut (Muster mit Platzhaltern, z. B. `/<SPRACHE>/hosts/<ZAHL>`)?
   - Wähle die URLs für den Lauf aus: Suchseite je Region, 2–3 Profile, bei Bedarf Reiter wie Gästebuch oder Kalender.
2. **Skript starten** im eigenen PowerShell-Fenster mit aktivierter Umgebung (A.1):
   ```powershell
   python -m src.explore_site --site de --data-dir ..\wwoof-data <URL> [<URL> ...]
   ```
   - URLs in Anführungszeichen setzen, wenn sie `&` enthalten (PowerShell würde sonst abbrechen).
   - Höchstens 5 URLs pro Lauf (harte Grenze im Code), keine doppelt. Jede URL muss zur Länderseite gehören (`https://` und der Host aus `base_url` in `sites/de.yaml`).
   - Vor dem ersten Seitenaufruf prüft das Skript alles und dann die robots.txt. Bei einem Fehler startet es nicht (`Not started: …`, Teil E).
3. **Ablauf:**
   - Ein Browserfenster öffnet sich mit dem Profil `browser_profile/de/` und zeigt die Startseite. Beim ersten Mal (oder wenn die Sitzung abgelaufen ist) loggst du dich dort von Hand ein. Dann im Terminal Enter drücken.
   - Das Skript öffnet die URLs nacheinander, mit 10–20 Sekunden Pause dazwischen (mindestens so lange, wie ein Crawl-delay der robots.txt verlangt). Die Zeit fürs Einloggen zählt als Pause.
   - **Schau dem Fenster zu.** Siehst du ein Captcha, eine Login-Aufforderung oder eine Fehlerseite: **Strg+C** im Terminal. Das Skript endet sauber; bereits gesicherte Seiten bleiben. Diese Fälle erkennt das Skript erst ab Phase 3 selbst.
   - Das Skript bricht selbst ab bei Status ab 400, bei einer Umleitung auf eine andere Seite (z. B. die Login-Seite) und bei Browserfehlern (`Run stopped …`, Teil E).
   - Ein Lauf ruft höchstens 6 Seiten auf: die Startseite (nicht gesichert) und bis zu 5 URLs.
4. **Ausgaben:**
   - Im Terminal nur Zähler, Dateinamen und Status, z. B. `Page 2 of 3: status 200, saved 20261119-153012-2.html, skeleton 412 lines`. Steht dahinter `network busy`, hat die Seite noch nachgeladen; das Skelett kann unvollständig sein.
   - Im Datenordner, je Lauf mit Datum und Uhrzeit im Namen (nie überschrieben):
     - `local/samples/<site>/…-<n>.html`: gesicherte Seiten. Sie bleiben lokal und werden nie geteilt. In Phase 3 prüfst du damit den Leser offline.
     - `local/samples/<site>/index.csv`: welche Datei zu welcher URL gehört (`file;url;status;saved_at`). Enthält URLs, bleibt deshalb ebenfalls lokal.
     - `local/structure/<site>/…-<n>.txt`: Skelette.
5. **Skelett prüfen, bevor du es teilst.** Am Ende jeder Skelett-Datei steht eine Liste aller lesbaren Wörter (`readable tokens`). Prüfe zuerst diese Liste, dann überfliege den Rest:
   - [ ] Die Tokenliste enthält nur Elementnamen (`div`, `a` …), Attributnamen (`href`, `aria-label` …), CSS-Klassen und Werte von `role` und `type`.
   - [ ] Keine CSS-Klasse und kein Wert sieht aus wie ein Name, Ort, Hofname oder eine Profil-ID. Längere Zahlen in Klassen sind bereits ersetzt (`host-⟨NUM:5⟩`).
   - [ ] In der Struktur erscheinen Texte nur als `⟨TEXT:n⟩` oder `⟨NUM:n⟩`, andere Werte nur als `⟨VAL:n⟩` oder `⟨URL⟩`.
   - [ ] Findest du etwas Lesbares: Skelett nicht teilen und Claude Code nur die Art des Fundes melden (z. B. „Klassenname enthält einen Namen“). Nach dem Nachschärfen der Regeln erzeugst du die Skelette neu, ohne die Seiten erneut aufzurufen:
     ```powershell
     python -m src.page_skeleton ..\wwoof-data\local\samples\de ..\wwoof-data\local\structure\de
     ```
6. **Teilen:** Die geprüfte Skelett-Datei nach `out/structure/` im Repository-Ordner kopieren (von Git ausgeschlossen) und Claude Code darauf verweisen, mit einer Zeile, welche Art Seite es ist (z. B. „Suchseite Region 1“, „Profil 2“). Die URL nennst du nicht.

**Generalprobe ohne Länderseite** (empfohlen vor dem ersten Lauf): derselbe Ablauf mit sichtbarem Fenster auf der Übungsseite, mit einem Datenordner unter `out/`:

```powershell
mkdir out\explore_test -Force
python -m src.explore_site --sites-dir tests\fixtures\practice_sites --site xt --data-dir out\explore_test https://quotes.toscrape.com/page/2/ https://quotes.toscrape.com/js/
```

Probiere dabei Login-Pause, Enter und einmal Strg+C aus. Die Übungsseite verlangt keinen Login; Enter genügt.

### A.1 Voraussetzungen

Einmal je Länderseite, vor dem ersten Lauf:
- Abklärung mit WWOOF: erledigt; sie gilt laut dir für alle Länderseiten der CWP (`02_regeln_und_rahmenbedingungen.md`, Abschnitt 1). Kein eigener Schritt.
- Mitgliedschaft bei der Landesorganisation der Länderseite. Deutschland: aktiv.
- Checkliste in Teil C bis Schritt 9 erledigt. Für Deutschland übernehmen das die Phasen 2 und 3; nur die Sprachdaten (Schritt 8) folgen in Phase 5.

Vor jedem Lauf:
- Gesamtumfang und Tagesgrenze beachten (offener Punkt 11 in `00_projekt_uebersicht.md`; wird vor Phase 3 festgelegt).
- Ein eigenes PowerShell-Fenster außerhalb von VS Code verwenden. In VS Code ist keine Datei aus `wwoof-data` geöffnet.
- Im neuen Fenster in den Repository-Ordner wechseln und die virtuelle Umgebung aktivieren; erst dann findet Python die Pakete (PyYAML, Playwright):
  ```powershell
  cd $HOME\Projekte\wwoof-planner
  .\.venv\Scripts\Activate.ps1
  ```
  Aktiv ist sie, wenn die Eingabezeile mit `(.venv)` beginnt. Das Terminal in VS Code aktiviert sie selbst, ein eigenes Fenster nicht.

### A.2 Länderseite und Region wählen – noch nicht gebaut (Phase 3)

In `config.yaml`:

```yaml
site: "de"                 # site_id of the country site
region: "voralpenland"     # region key from sites/de.yaml
```

- Werte **immer in Anführungszeichen.** Ohne Anführungszeichen liest YAML `no` (Norwegen) als `false`; das Skript lehnt das mit einer Meldung ab.
- `site` ist die site_id in Kleinbuchstaben; die Datei `sites/<site>.yaml` muss existieren.
- `region` ist ein Regionsschlüssel aus dieser Datei.
- Grenzwerte und Pausen stehen ebenfalls in `config.yaml`. Die harte Grenze von 50 Profilen pro Lauf steht im Code und lässt sich nicht ändern.

### A.3 robots.txt prüfen

Die Prüfung liest `base_url` aus der Länderseiten-Datei, ruft `<base_url>/robots.txt` **einmal** ab und meldet für die Startseite und für jede angegebene Adresse `allowed` oder `DISALLOWED`. Erkundungsskript (ab Phase 2) und Sammler (ab Phase 3) prüfen die robots.txt vor jedem Lauf selbst.

Im eigenen PowerShell-Fenster mit aktivierter Umgebung (A.1), weil die Prüfung die Länderseite aufruft:

```powershell
python -m src.robots_check de
python -m src.robots_check de <URL> [<URL> ...]
```

- Jede URL muss zur Länderseite gehören: `https://` und genau der Host aus `base_url`. Sonst bricht die Prüfung vor dem Abruf ab.
- Die Ausgabe nennt keine URLs, nur `URL 1`, `URL 2` usw. in der Reihenfolge deiner Eingabe.
- Ausgewertet werden die Regeln für alle Programme (`User-agent: *`) nach RFC 9309.
- `crawl delay`: Verlangt die robots.txt eine Wartezeit zwischen zwei Seitenaufrufen, steht sie hier. Die Skripte warten dann mindestens so lange (ab Schritt 2.2).
- Exit-Code 0, wenn alles erlaubt ist; 1 bei einem Verbot oder Fehler.

Beispiel (erfunden):

```
Site de: robots.txt found
  start page   allowed
  URL 1        allowed
  crawl delay  none
Result: 0 of 2 addresses disallowed
```

| Ergebnis | Bedeutung | Was du tust |
|---|---|---|
| `robots.txt found`, alles `allowed` | Die Regeln erlauben die Abrufe | weiter |
| `no robots.txt (status 404 or 410), no rules apply` | Die Länderseite hat keine robots.txt; nach RFC 9309 gelten dann keine Regeln | weiter |
| `DISALLOWED` | Die Regeln verbieten diese Adresse | nicht abrufen; siehe A.7 |
| Abbruch mit Meldung | Abruf nicht möglich oder Antwort unbrauchbar | siehe Teil E |

### A.4 Starten – noch nicht gebaut (Phase 3)

Im eigenen PowerShell-Fenster mit aktivierter Umgebung (A.1):

```powershell
python -m src.collector
```

Der Modulname folgt dem Plan in `03_programmierprojekt.md`, Abschnitt 5.1; endgültig gilt er, sobald es den Sammler gibt.

### A.5 Login – noch nicht gebaut (Phase 3)

- Jede Länderseite hat ein eigenes Browser-Profil im Datenordner: `browser_profile/<site_id>/`, z. B. `browser_profile/de/`.
- Bist du nicht eingeloggt, meldet das Skript das. Du loggst dich im geöffneten Browser von Hand ein und bestätigst im Terminal mit Enter.
- Dein Passwort steht nie in einer Datei. Das Browser-Profil ist so schutzbedürftig wie ein Passwort.

### A.6 Ablauf – noch nicht gebaut (Phase 3)

Konfiguration und Länderseiten-Datei prüfen → robots.txt prüfen → Browser mit dem Profil der Länderseite öffnen → Suche der Region aufrufen → Link-Liste speichern (Dateiname mit site_id und Regionsschlüssel) → bereits erfasste Höfe überspringen → je neuem Profil: lesen, Hof-Code vergeben, Zeile in `farms.csv`, zufällige Pause (Vorschlag 10–20 Sekunden) → Zusammenfassung. Einzelheiten in `03_programmierprojekt.md`, Abschnitt 4.

### A.7 Abbruchgründe und was du tust – noch nicht gebaut (Phase 3)

Der Sammler beendet sich sauber, statt es erneut zu versuchen.

| Grund | Was du tust |
|---|---|
| Konfiguration unzulässig (z. B. Wert ohne Anführungszeichen, unbekannte Region, Grenzwert über 50) | `config.yaml` oder Länderseiten-Datei korrigieren (Teil E) |
| Region ohne Suchdefinition | Länder-Prüfung abschließen und Suchdefinition eintragen (Teil C, Schritte 6 und 7) |
| robots.txt verbietet den Abruf | Nicht umgehen. Lauf nicht starten; mit Claude Code besprechen (ohne Hofdaten) |
| Login-Aufforderung mitten im Lauf | Neu einloggen; den Lauf später fortsetzen (A.8) |
| Captcha oder Zugriffsverweigerung | Nicht sofort erneut starten. Später fortsetzen; tritt es wieder auf, anhalten und besprechen |
| unerwarteter Fehler | Meldung prüfen und ohne Hofdaten an Claude Code geben |

### A.8 Fortsetzen – noch nicht gebaut (Phase 3)

Denselben Befehl mit derselben Konfiguration erneut starten. Bereits erfasste Höfe werden über die normalisierte Profil-URL erkannt und übersprungen, auch wenn sie in einer anderen Region oder über eine andere Länderseite erfasst wurden. Die Obergrenze gilt je Lauf.

### A.9 Zusammenfassung und Log – noch nicht gebaut (Phase 3)

- Im Terminal: Länderseite, Region, neu erfasst, übersprungen, Fehler. Nur Hof-Codes und Zahlen.
- Das Log liegt in `wwoof-data/logs/`, nennt die site_id und enthält keine Hofdaten. Auszüge gibst du Claude Code nur nach eigener Prüfung.

---

## Teil B – Nach dem Lauf

### B.1 Notizen pflegen

`local/notes.csv`: eigene Notizen je Hof-Code, ohne Personenbezug; sie gehen mit dem Export an Claude. Diese Regeln gelten schon seit Phase 1:
- **Speichern in Excel nur als „CSV UTF-8 (durch Trennzeichen getrennt)“.**
- Dateien, die nur Skripte schreiben (`farms.csv`, `keyword_report.csv`, Export), nur ansehen, nie speichern. Excel wandelt sonst Datumswerte um.

### B.2 Export, erste Stufe – noch nicht gebaut (Phase 4)

Das Skript schreibt `export/export_for_claude.csv` mit Hof-Code, Ort, Region, Lernkategorien, Gästebuch-Anzahl, Zeitfenstern und Notizen. Vorher prüft ein Selbsttest alles (`03_programmierprojekt.md`, Phase 4); scheitert er, entsteht kein Export. Damit kann die Planung im claude.ai-Projekt beginnen.

### B.3 Stichworte und Steckbrief – noch nicht gebaut (Phase 5)

Das Skript ordnet die Beschreibungen Kategorien zu, bildet den Steckbrief und schreibt `local/keyword_report.csv`. Du prüfst **per Stichprobe**, ob Kategorien und Steckbrief stimmen, und schärfst die Regeln nach (`03_programmierprojekt.md`, Abschnitte 6 und 7). Eine Prüfung jeder Beschreibung ist nicht nötig, weil der Steckbrief keinen Freitext enthält. Angewendet werden nur die Sprachen der Länderseite des Hofs; fehlen Sprachdaten, bricht das Skript für die betroffenen Höfe ab (`05_stichwort_taxonomie.md`, Abschnitte 5 und 6).

### B.4 Export, vollständig – noch nicht gebaut (Phase 6)

Wie B.2, zusätzlich mit Kategorien, Abdeckung und Steckbrief. Der Selbsttest lässt nur Schlüssel und Werte aus dem Schema durch.

### B.5 Hochladen

Den Export lädst du selbst in das claude.ai-Projekt hoch. Sieh ihn vorher kurz an: nur Hof-Codes, keine Hofnamen.

---

## Teil C – Neue Länderseite hinzufügen (Checkliste)

Für Deutschland ist die Mitgliedschaft aktiv. Die übrigen Schritte verteilen sich auf die Phasen:
- Phase 2: Schritte 3–6 (Datei, Regionen, robots.txt, Erkundung).
- Phase 3: Schritte 7, 9 und 10.
- Phase 5: Schritt 8. Er folgt für Deutschland also erst nach dem ersten Lauf. Das geht, weil der Sammler die Sprachdaten nicht braucht; erst Stichworte, Steckbrief und der vollständige Export verlangen sie.

Für jede weitere Länderseite gehst du die Liste selbst in dieser Reihenfolge durch. Claude Code hilft beim Anlegen der Dateien und Tests, ruft aber nie eine Länderseite auf. Die Abklärung mit WWOOF gilt für alle Länderseiten der CWP und ist deshalb kein eigener Schritt.

1. **Zugehörigkeit zur CWP prüfen:** Steht die Landesorganisation in der Liste der Organisationen auf der CWP (Quelle in `02_regeln_und_rahmenbedingungen.md`)?
   - Nein → außerhalb des Umfangs, hier aufhören.
   - Deckt die Organisation mehrere Länder ab oder passt kein eindeutiger Ländercode → anhalten und entscheiden.
2. **Mitgliedschaft** bei der Landesorganisation abschließen. Beim Beitritt die Mitgliedsbedingungen lesen; widersprechen sie dem Vorgehen, anhalten und entscheiden (Vorschlag von Claude Code).
3. **Länderseiten-Datei anlegen:** `sites/<site_id>.yaml` mit `base_url` und `languages`, Vorlage `sites/de.yaml`. site_id ist der ISO-Code in Kleinbuchstaben, in YAML immer in Anführungszeichen. `base_url` ist nur `https://` und der Host, wie ihn die Adresszeile des Browsers zeigt (mit oder ohne `www`), ohne `/` am Ende. Nur in dieser Datei steht die Domain der Länderseite.
4. **Regionsschlüssel und Regionskürzel festlegen,** noch ohne Suchdefinition:
   - Schlüssel klein (`a–z`, `0–9`, `_`) und über alle Länderseiten eindeutig.
   - Kürzel zwei oder drei Großbuchstaben, innerhalb der Länderseite eindeutig.
   - `config.py` lässt Regionen ohne Suchdefinition zu; `learning_categories: []` darf noch leer sein.
   - Gesamtumfang beachten (offener Punkt 11).
   - **Prüfen** (ohne Netz): `python -m src.config <site_id>` meldet `ok` oder nennt Datei, Feld und Fehler (Teil E).
5. **robots.txt prüfen** (A.3). Verbietet sie den Abruf, wird die Länderseite nicht erfasst.
6. **Länder-Prüfung** wie Phase 2 für Deutschland: Vorab-Sichtung von Hand und Erkundungsskript (A.0). Claude Code bekommt nur geprüfte Skelette und Strukturbeschreibungen mit Platzhaltern. Zu klären:
   - Gleicher Seitenaufbau wie die bisherigen Länderseiten? Passen die plattformweiten Selektoren?
   - Profil-URLs: gleicher Aufbau (mit eigener Domain)? Passt die Normalisierung?
   - Login-Sitzung: bleibt sie im Browser-Profil `browser_profile/<site_id>/` erhalten?
   - Regionsfilter: wie wird eine Region gesucht?
   - Lernkategorien: welche gibt es, in welcher Sprache, enthält eine das Zeichen `|`?
   - Gästebuch-Anzahl und Kalender: wo und wie?
   - **Zeigt sich eine Abweichung:** anhalten und entscheiden. Nichts auf Vorrat umbauen.
7. **Suchdefinition je Region eintragen** (aus Schritt 6) und `learning_categories` in die Länderseiten-Datei übernehmen.
8. **Sprachdaten ergänzen** – Struktur noch nicht gebaut (Phase 5):
   - Taxonomie-Begriffe, Ausnahmen, Verneinungen, Ignorierliste und Steckbrief-Regeln für jede Sprache der Länderseite, dazu Regeln für die Normalisierung.
   - Dazu pytest-Tests an erfundenen Texten. Für erfundene Rufnummern dieses Landes in Testdaten eine Regel festlegen; die Regel mit den Rufnummern der Bundesnetzagentur gilt nur für Deutschland.
9. **Testlauf mit einem Profil,** von dir gestartet. Wie genau, legt Phase 3 fest.
10. **Erster Lauf** nach Teil A. Fehlt der gewählten Region die Suchdefinition, bricht der Sammler ab.
11. **Dokumente aktualisieren:**
    - `06_fortschritt.md`: Stand der Länderseite; `08_entscheidungsprotokoll.md`: Entscheidungen.
    - dieses Dokument: Erfahrungen, neue Meldungen in Teil E.
    - bei Abweichungen `03_programmierprojekt.md`, bei Bedarf `00_projekt_uebersicht.md`.

---

## Teil D – Löschung nach der Reise

Alle Hofdaten werden nach der Reise gelöscht; darum kümmerst du dich (Zusage gegenüber WWOOF, `02_regeln_und_rahmenbedingungen.md`, Abschnitt 6). Am einfachsten löschst du den ganzen Datenordner `wwoof-data`. Zur Kontrolle:

- [ ] `wwoof-data/local/` (Hoftabelle, Notizen, Berichte, Link-Listen, `samples/` und `structure/` der Erkundung)
- [ ] `wwoof-data/export/`
- [ ] `wwoof-data/logs/`
- [ ] `wwoof-data/browser_profile/` mit den Unterordnern aller Länderseiten (Login-Sitzungen)
- [ ] die ins claude.ai-Projekt hochgeladenen Exporte
- [ ] Kopien außerhalb des Datenordners (z. B. im Download-Ordner), danach den Papierkorb leeren

Das Repository `wwoof-planner` enthält keine Hofdaten. `out/` enthält Ausgaben aus erfundenen Testdaten und die geprüften Skelette in `out/structure/`; diese löschst du ebenfalls. Deine Mitgliedschaften betrifft die Löschung nicht.

---

## Teil E – Häufige Meldungen

| Meldung | Ursache | Was tun | Stand |
|---|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | Skript über den ▷-Knopf oder außerhalb des Ordners `wwoof-planner` gestartet | Im Ordner `wwoof-planner` mit `python -m src.<modul>` starten | gilt |
| `ModuleNotFoundError: No module named 'yaml'` (oder `playwright`, `pandas`) | Virtuelle Umgebung im eigenen Fenster nicht aktiviert; das allgemeine Python von Windows hat die Pakete nicht | Umgebung aktivieren (A.1), dann den Befehl wiederholen | gilt |
| Fehlermeldung, die den Modulnamen mit `.py` nennt (z. B. `src.filter_region.py`) | Bei `python -m` wurde `.py` angehängt | Modulname ohne `.py`: `python -m src.filter_region` | gilt |
| Aktivierung der virtuellen Umgebung blockiert | Ausführungsrichtlinie von PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (`04_technische_voraussetzungen.md`, Abschnitt 3) | gilt |
| `Configuration error: … is false, not text; put codes in quotes …` | Ein Code steht ohne Anführungszeichen, z. B. `no`; YAML liest ihn als `false` | Wert in Anführungszeichen setzen | gilt |
| `Configuration error: site id must look like "de" …` oder `…/<site>.yaml: file not found` | site_id falsch geschrieben, nicht klein oder Datei fehlt | site_id in Kleinbuchstaben; Datei in `sites/` prüfen | gilt |
| `Configuration error: …: unknown key '…'`, `missing key '…'` oder `duplicate key '…' (line n)` | Tippfehler, fehlender Eintrag oder Eintrag, der nicht in die Datei gehört | Schlüssel korrigieren; die Länderseiten-Datei enthält nur Länderdaten | gilt |
| `Configuration error: …: … must look like …`, `base_url must be …`, `invalid YAML: … (line n)` | Wert im falschen Format oder YAML-Syntaxfehler | Wert nach dem genannten Muster korrigieren | gilt |
| `Configuration error: region key … appears in … and …` | Derselbe Regionsschlüssel in zwei Länderseiten-Dateien | einen der Schlüssel umbenennen (die Spalte `region` enthält kein Land) | gilt |
| `URL n does not belong to site …` | Die URL gehört nicht zum Host aus `base_url` (z. B. `www` zu viel oder zu wenig, `http://`) | URL von der gewählten Länderseite verwenden; ggf. `base_url` prüfen | gilt |
| `Not started: at most 5 pages per run (hard limit); n URLs given` | Erkundung: mehr als 5 URLs angegeben | auf mehrere Läufe verteilen | gilt |
| `Not started: URL n repeats URL m` | Erkundung: dieselbe URL zweimal angegeben | doppelte URL weglassen | gilt |
| `Not started: …: data folder not found` oder `… must be outside the repository …` | Erkundung: Datenordner falsch geschrieben oder im Repository | Pfad prüfen, z. B. `..\wwoof-data`; nur Testläufe dürfen `out\` verwenden | gilt |
| `Not started: site …: the start page is disallowed by robots.txt` oder `URL n of m is disallowed by robots.txt` | Erkundung: robots.txt verbietet eine der Adressen | nicht umgehen; diese URL weglassen, siehe A.7 | gilt |
| `Run stopped after k of n pages: page i of n: status …` | Die Seite antwortet mit einem Fehler (ab 400), z. B. nicht gefunden oder Zugriff verweigert | Bei 404: URL prüfen. Bei 401, 403, 429 oder 5xx: nicht sofort erneut, siehe A.7 | gilt |
| `Run stopped after …: redirected to another page (e.g. the login page) …` oder `… to another site …` | Die Seite hat auf eine andere Adresse umgeleitet, meist weil die Sitzung abgelaufen ist | Im Fenster neu einloggen (nächster Lauf zeigt die Startseite); bleibt es dabei, die URL im Browser prüfen | gilt |
| `Run stopped after …: browser error net::ERR_…` oder `page did not load within 30 seconds` | Keine Verbindung oder Seite zu langsam | Internetverbindung prüfen, später erneut | gilt |
| `Run stopped: browser profile is in use …` | Ein anderer Lauf mit demselben Profil ist noch offen | anderes Fenster schließen, dann erneut | gilt |
| `Run stopped by Ctrl+C …` oder `… browser window was closed` | Du hast abgebrochen oder das Browserfenster geschlossen | nichts; gesicherte Seiten bleiben | gilt |
| `network busy (content may be incomplete)` hinter einer Seite | Die Seite lud nach 10 Sekunden noch Inhalte nach | Skelett prüfen; fehlt Inhalt, die Seite in einem späteren Lauf erneut aufnehmen | gilt |
| Unbekannte Region | `region` passt zu keinem Regionsschlüssel der Länderseite | Regionsschlüssel aus der Länderseiten-Datei verwenden | noch nicht gebaut (Phase 3) |
| Region ohne Suchdefinition | Länder-Prüfung noch nicht abgeschlossen | Teil C, Schritte 6 und 7 | noch nicht gebaut (Phase 3) |
| `DISALLOWED`, Exit-Code 1 | robots.txt verbietet den Abruf | nicht umgehen; siehe A.7 | gilt |
| `robots.txt: access denied or too many requests (status …); do not retry now` | Die Länderseite verweigert den Abruf (401, 403) oder bremst (429) | nicht sofort erneut; später ein Versuch; tritt es wieder auf, anhalten und besprechen (A.7) | gilt |
| `robots.txt: unexpected status …` oder `robots.txt could not be fetched (…)` | Serverfehler, keine Verbindung, Zeitüberschreitung | Internetverbindung prüfen, später erneut | gilt |
| `robots.txt is an HTML page, not a robots.txt file; check it by hand` | Die Länderseite liefert statt robots.txt eine Webseite | `<base_url>/robots.txt` im Browser ansehen; keinen Lauf starten; Claude Code nur die Art des Fundes melden | gilt |
| `robots.txt was redirected to another address; check base_url …` | `base_url` stimmt nicht, z. B. mit oder ohne `www` | Adresszeile im Browser prüfen, `base_url` korrigieren, mit `python -m src.config <site_id>` prüfen | gilt |
| `this Python version evaluates robots.txt rules the old way …` | Ältere Python-Version, die robots.txt-Regeln anders auswertet | Python aktualisieren (getestet mit 3.13.15) | gilt |
| Login-Aufforderung oder Captcha im Seiteninhalt | Sitzung abgelaufen oder Schutzmaßnahme der Seite | Erkundung: Strg+C (A.0); Sammler: siehe A.7 | Erkennung durch das Skript noch nicht gebaut (Phase 3) |
| Sprachdaten fehlen | Für eine Sprache der Länderseite fehlen Begriffe oder Steckbrief-Regeln | Teil C, Schritt 8 | noch nicht gebaut (Phase 5) |

Die genauen Meldungstexte ergänzen die jeweiligen Phasen.
