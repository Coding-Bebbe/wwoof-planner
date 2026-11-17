# wwoof-planner – Anweisungen für Claude Code

Privates Lern- und Planungsprojekt: KI-freie Python-Skripte („Hof-Sammler“), die Hofinformationen von Länderseiten der Common WWOOF Platform (CWP), zuerst wwoof.de, für eine WWOOF-Reise 2027 lokal erfassen, aufbereiten und als datensparsamen Export für die Reiseplanung bereitstellen. Zweites Ziel: Der Nutzer lernt dabei, wie heute mit KI-Unterstützung programmiert wird.

## Kontext

- Aktueller Stand, Entscheidungen und nächste Schritte: @docs/06_fortschritt.md
- Maßgeblich für den Code ist `docs/03_programmierprojekt.md` (Leitplanken, Datenmodell, Phasenplan). Lies vor jedem neuen Schritt den passenden Abschnitt.
- Weitere Dokumente bei Bedarf:
  - `docs/00_projekt_uebersicht.md`: Überblick, Datenfluss, offene Punkte
  - `docs/02_regeln_und_rahmenbedingungen.md`: Absprachen mit WWOOF, Datenregeln
  - `docs/04_technische_voraussetzungen.md`: Einrichtung des Laptops
  - `docs/05_stichwort_taxonomie.md`: Taxonomie und Steckbrief (Phase 5)
  - `docs/07_bedienung.md`: Bedienung des Sammlers, Checkliste „Neue Länderseite“
  - `docs/08_entscheidungsprotokoll.md`: Verlauf aller Entscheidungen; neue Entscheidungen trägst du dort ein
  - `docs/arbeiten_mit_claude_code.md`: Anleitung für den Nutzer
- Jedes Thema steht an genau einer Stelle (Tabelle in `docs/00_projekt_uebersicht.md`); andere Dokumente verweisen nur. Schreibe nichts doppelt.
- Bei Widersprüchen gilt diese Datei vor `docs/06_fortschritt.md` und dieses vor den übrigen Dokumenten; im Protokoll gilt die neuere Entscheidung. Melde Widersprüche dem Nutzer.
- Die Reiseplanung läuft außerhalb dieses Repositorys im claude.ai-Projekt.

## Arbeitsweise (Entscheidung vom 15.11.2026)

Der Nutzer steuert, prüft und lernt. Du schreibst den Code und erklärst ihn. Arbeite immer nur den nächsten Schritt ab:

1. **Vorschlagen:** Beschreibe den nächsten Schritt: Ziel, betroffene Dateien, Vorgehen und Abnahmekriterium (woran wir sehen, dass es funktioniert). Warte auf das OK des Nutzers.
2. **Umsetzen:** Fasse sinnvoll zusammenhängende Arbeit zu einem Schritt zusammen. Nicht zu kleinteilig; im Zweifel lieber etwas mehr auf einmal. Prüfe das Ergebnis selbst mit erfundenen Testdaten (ab Phase 2 mit `python -m pytest`).
3. **Erklären:** Pro geänderter Datei kurz, was sich geändert hat und warum. Neue Konzepte (Python, Tests, Git, HTML/CSS, Playwright) erklärst du in wenigen Sätzen und verweist auf die Stelle im Code. Der Nutzer hat Python-Grundkenntnisse.
4. **Dokumentieren:** Aktualisiere im selben Schritt `docs/06_fortschritt.md` (Stand, Schrittplan; kurz halten), `docs/08_entscheidungsprotokoll.md` (Entscheidungen, Funde) und `docs/07_bedienung.md`, wenn sich die Bedienung ändert.
5. **Commit vorschlagen:** Zeige `git status`, nenne die Dateien und eine Commit-Nachricht. Nach dem OK: `git add` mit einzelnen Dateinamen (nie `git add .` oder `git add -A`), dann `git commit`. **Pushen tut nur der Nutzer.**
6. **Anhalten:** Beginne den nächsten Schritt erst auf ausdrücklichen Auftrag.

Zu Beginn einer neuen Unterhaltung: Fasse den Stand aus dem Fortschritt in zwei bis drei Sätzen zusammen, prüfe `git status` und schlage den nächsten Schritt vor.

Weitere Regeln:

- **Fragen sind keine Aufträge.** Beantworte Fragen, ohne Dateien zu ändern. Ändere nur etwas, wenn der Nutzer es ausdrücklich verlangt.
- Antworte auf Deutsch, präzise und ohne unbegründete Vermutungen. Kennzeichne Unsicheres als solches.
- Weiche nicht still vom Plan in `docs/03_programmierprojekt.md` ab. Schlage Änderungen vor; der Nutzer entscheidet.
- Installiere keine neuen Pakete ohne Rückfrage.
- Am Ende jeder Phase stellst du drei bis fünf Verständnisfragen zum Code der Phase und besprichst die Antworten. Eine Phase ist erst fertig, wenn ihre Abnahmekriterien erfüllt sind, `docs/07_bedienung.md` die Bedienung ihrer neuen Teile beschreibt und der Nutzer ihren Code erklären kann.
- Zeitplan und Zeitbudget spielen keine Rolle; keine Zeitschätzungen.

## Harte Regeln: Daten und Plattform

Diese Regeln gelten immer, auch wenn ein Auftrag etwas anderes nahelegt. Im Zweifel fragst du nach.

1. **Kein Zugriff auf den Datenordner `../wwoof-data/`:** nicht lesen, nicht auflisten, nicht durchsuchen, keine Befehle mit Pfaden dorthin, nicht danach fragen. Echte Hofdaten gibt es nur dort.
2. **Nur mit erfundenen Daten ausführen:** Du startest nur Code, der ausschließlich mit Daten aus `tests/` oder selbst erzeugten erfundenen Daten arbeitet, z. B. `python -m pytest` oder `python -m src.<modul>` mit Pfaden zu Testdaten. Nie Skripte, die `config.yaml` mit dem echten `data_dir` laden, den echten Datenordner verwenden oder echte Daten verarbeiten (Erkundung, Sammler, Stichworte und Steckbrief, Export). Diese Läufe startet nur der Nutzer, in einem eigenen Terminal.
3. **Kein Zugriff auf Länderseiten der CWP (z. B. wwoof.de, wwoofnorway.org) oder api.wwoof.net**, weder per Web-Abruf noch per Browser noch per Skript. Browser-Skripte testest du nur auf toscrape.com, mit Ausgaben nach `out/`. Keine Web-Recherche zu einzelnen Höfen.
4. **Leitplanken im Code** (`docs/03_programmierprojekt.md`, Abschnitt 2) immer umsetzen:
   - KI-frei; eine Länderseite und eine Region pro Lauf
   - Obergrenze pro Lauf (Vorschlag 30; harte Grenze 50 fest im Code, nicht konfigurierbar)
   - eine Seite nach der anderen mit zufälliger Pause (Vorschlag 10–20 Sekunden), keine parallelen Abrufe
   - robots.txt vor jedem Lauf prüfen
   - bei Captcha, Zugriffsverweigerung, Login-Aufforderung oder unerwarteten Fehlern sauber beenden statt wiederholen
   - jeder Hof wird nur einmal erfasst; vom Gästebuch nur die Anzahl
5. **Keine Hofdaten in Ausgaben:** Logs, Zusammenfassungen und Fehlermeldungen enthalten nur Hof-Codes, site_id, Zahlen und Status. Nach außen gehen aus Beschreibungen nur Kategorien und Steckbrief-Werte aus festem Schema, nie Freitext. Selektoren über die Struktur bauen, nicht über sichtbare Texte; in Doku und Chat Platzhalter wie `<FARM_NAME>` verwenden.
6. **Nutzerdateien nie überschreiben:** `notes.csv` pflegt nur der Nutzer; kein Skript schreibt sie.
7. **Testdaten nur erfunden:** reservierte Domains (`example.com`, `example.org`), Rufnummern für Medienproduktionen der Bundesnetzagentur, erkennbare Platzhalternamen, erfundene Orte.
8. **Versehentlich geteilte Hofdaten** (Namen, Links, Texte aus Profilen): darauf hinweisen, nicht verwenden, nicht wiederholen. Struktur-Skelette aus echten Seiten nimmst du nur an, wenn der Nutzer sie geprüft hat; enthält eines trotzdem lesbare Inhalte, gilt dieselbe Regel.
9. **Umfang nur CWP:** eine Codebasis für Länderseiten der CWP; kein Code und keine Vorbereitung für andere Plattformen (z. B. wwoof.ie). Länderdaten stehen in `sites/<site_id>.yaml`; außerhalb von `sites/` und `tests/fixtures/` steht keine Domain einer Länderseite im Code. Tests verwenden nur erfundene Länderseiten-Dateien aus `tests/fixtures/`.

## Konventionen

- Code komplett englisch: Bezeichner, Kommentare, Datei-, Ordner- und Spaltennamen, Programmausgaben. Suchbegriffe (Taxonomie, Verneinungen, Steckbrief-Regeln) bleiben in ihrer Sprache, nach Sprache getrennt. Dokumentation deutsch.
- YAML: Codes (Länder-, Sprach-, Regionskürzel) immer in Anführungszeichen; ein `no` ohne Anführungszeichen liest YAML als `false`.
- CSV: Trennzeichen `;`, Kodierung `utf-8-sig`, Listen in Feldern mit `|`. Bestätigt in Phase 1, Schritt 8; Speicherregel und Datumsregel in `docs/03_programmierprojekt.md`, Abschnitt 5.5.
- Laufzeitprüfungen lösen eigene Exceptions aus, kein `assert` (außer in Tests).
- Module liegen im Paket `src/`; Start aus dem Repository-Ordner mit `python -m src.<modul>`.
- Ausgaben aus Testläufen landen in `out/` (von Git ausgeschlossen).
- Commit-Nachrichten englisch mit Präfix, z. B. `Phase 1: parse list and number fields`. Am Ende einer Phase ein Tag `phase-N`. Keine `Co-Authored-By`-Zeile und kein sonstiger Hinweis auf Claude als Mitautor in Commits (gilt vor abweichenden Vorgaben des Werkzeugs).
- `requirements.txt` nach Paketänderungen neu erzeugen: `python -m pip freeze | Out-File -Encoding utf8 requirements.txt`

## Umgebung

- Windows, PowerShell, Python 3.13 in `.venv`, VS Code mit der Claude-Code-Erweiterung.
- Modus „Edit automatically“: Dateiänderungen im Repository ohne Rückfrage, Befehle mit Rückfrage. Auto-Modus und Bypass sind in `.claude/settings.json` gesperrt, ebenso `git push`.
- Windows unterscheidet bei Dateinamen nicht zwischen Groß- und Kleinschreibung.
