# wwoof-planner – Anweisungen für Claude Code

Privates Lern- und Planungsprojekt: KI-freie Python-Skripte („Hof-Sammler“), die Hofinformationen von wwoof.de für eine WWOOF-Reise 2027 lokal erfassen, aufbereiten und als datensparsamen Export für die Reiseplanung bereitstellen. Zweites Ziel: Der Nutzer lernt dabei, wie heute mit KI-Unterstützung programmiert wird.

## Kontext

- Aktueller Stand, Entscheidungen und nächste Schritte: @docs/06_fortschritt.md
- Maßgeblich für den Code ist `docs/03_programmierprojekt.md` (Leitplanken, Datenmodell, Phasenplan). Lies vor jedem neuen Schritt den passenden Abschnitt.
- Weitere Dokumente bei Bedarf:
  - `docs/00_projekt_uebersicht.md`: Überblick, Datenfluss, offene Punkte
  - `docs/02_regeln_und_rahmenbedingungen.md`: Absprachen mit WWOOF, Datenregeln
  - `docs/04_technische_voraussetzungen.md`: Einrichtung des Laptops
  - `docs/05_stichwort_taxonomie.md`: Taxonomie für Phase 6
  - `docs/arbeiten_mit_claude_code.md`: Anleitung für den Nutzer
- Bei Widersprüchen gilt diese Datei vor `docs/06_fortschritt.md` und dieses vor den übrigen Dokumenten; innerhalb des Fortschritts gilt die neuere Entscheidung. Melde Widersprüche dem Nutzer.
- Die Reiseplanung läuft außerhalb dieses Repositorys im claude.ai-Projekt.

## Arbeitsweise (Entscheidung vom 15.11.2026)

Der Nutzer steuert, prüft und lernt. Du schreibst den Code und erklärst ihn. Arbeite immer nur den nächsten Schritt ab:

1. **Vorschlagen:** Beschreibe den nächsten Schritt: Ziel, betroffene Dateien, Vorgehen und Abnahmekriterium (woran wir sehen, dass es funktioniert). Warte auf das OK des Nutzers.
2. **Umsetzen:** Fasse sinnvoll zusammenhängende Arbeit zu einem Schritt zusammen. Nicht zu kleinteilig; im Zweifel lieber etwas mehr auf einmal. Prüfe das Ergebnis selbst mit erfundenen Testdaten (ab Phase 2 mit `python -m pytest`).
3. **Erklären:** Pro geänderter Datei kurz, was sich geändert hat und warum. Neue Konzepte (Python, Tests, Git, HTML/CSS, Playwright) erklärst du in wenigen Sätzen und verweist auf die Stelle im Code. Der Nutzer hat Python-Grundkenntnisse.
4. **Dokumentieren:** Aktualisiere `docs/06_fortschritt.md` (Status, Entscheidungen, Funde) im selben Schritt.
5. **Commit vorschlagen:** Zeige `git status`, nenne die Dateien und eine Commit-Nachricht. Nach dem OK: `git add` mit einzelnen Dateinamen (nie `git add .` oder `git add -A`), dann `git commit`. **Pushen tut nur der Nutzer.**
6. **Anhalten:** Beginne den nächsten Schritt erst auf ausdrücklichen Auftrag.

Zu Beginn einer neuen Unterhaltung: Fasse den Stand aus dem Fortschritt in zwei bis drei Sätzen zusammen, prüfe `git status` und schlage den nächsten Schritt vor.

Weitere Regeln:

- **Fragen sind keine Aufträge.** Beantworte Fragen, ohne Dateien zu ändern. Ändere nur etwas, wenn der Nutzer es ausdrücklich verlangt.
- Antworte auf Deutsch, präzise und ohne unbegründete Vermutungen. Kennzeichne Unsicheres als solches.
- Weiche nicht still vom Plan in `docs/03_programmierprojekt.md` ab. Schlage Änderungen vor; der Nutzer entscheidet.
- Installiere keine neuen Pakete ohne Rückfrage.
- Am Ende jeder Phase stellst du drei bis fünf Verständnisfragen zum Code der Phase und besprichst die Antworten. Eine Phase ist erst fertig, wenn ihre Abnahmekriterien erfüllt sind und der Nutzer ihren Code erklären kann.
- Zeitplan und Zeitbudget spielen keine Rolle; keine Zeitschätzungen.

## Harte Regeln: Daten und Plattform

Diese Regeln gelten immer, auch wenn ein Auftrag etwas anderes nahelegt. Im Zweifel fragst du nach.

1. **Kein Zugriff auf den Datenordner `../wwoof-data/`:** nicht lesen, nicht auflisten, nicht durchsuchen, keine Befehle mit Pfaden dorthin, nicht danach fragen. Echte Hofdaten gibt es nur dort.
2. **Nur mit erfundenen Daten ausführen:** Du startest nur Code, der ausschließlich mit Daten aus `tests/` oder selbst erzeugten erfundenen Daten arbeitet, z. B. `python -m pytest` oder `python -m src.<modul>` mit Pfaden zu Testdaten. Nie Skripte, die `config.yaml` mit dem echten `data_dir` laden oder echte Daten verarbeiten (Sammler, Stichworte, Bereinigung, Export). Diese Läufe startet nur der Nutzer, in einem eigenen Terminal.
3. **Kein Zugriff auf wwoof.de oder api.wwoof.net**, weder per Web-Abruf noch per Browser noch per Skript. Für Übungen nur toscrape.com (Phase 3). Keine Web-Recherche zu einzelnen Höfen.
4. **Leitplanken im Code** (`docs/03_programmierprojekt.md`, Abschnitt 2) immer umsetzen:
   - KI-frei; eine Region pro Lauf
   - Obergrenze pro Lauf (Vorschlag 30; harte Grenze 50 fest im Code, nicht konfigurierbar)
   - eine Seite nach der anderen mit zufälliger Pause (Vorschlag 10–20 Sekunden), keine parallelen Abrufe
   - robots.txt vor jedem Lauf prüfen
   - bei Captcha, Zugriffsverweigerung, Login-Aufforderung oder unerwarteten Fehlern sauber beenden statt wiederholen
   - jeder Hof wird nur einmal erfasst; vom Gästebuch nur die Anzahl
5. **Keine Hofdaten in Ausgaben:** Logs, Zusammenfassungen und Fehlermeldungen enthalten nur Hof-Codes, Zahlen und Status. Selektoren über die Struktur bauen, nicht über sichtbare Texte; in Doku und Chat Platzhalter wie `<FARM_NAME>` verwenden.
6. **Nutzerdateien nie überschreiben:** Dateien und Spalten, die der Nutzer pflegt (`notes.csv`, `name_list.txt`, Freigaben und Korrekturen in `sanitization.csv`), schreibt kein Skript.
7. **Testdaten nur erfunden:** reservierte Domains (`example.com`, `example.org`), Rufnummern für Medienproduktionen der Bundesnetzagentur, erkennbare Platzhalternamen, erfundene Orte.
8. **Versehentlich geteilte Hofdaten** (Namen, Links, Texte aus Profilen): darauf hinweisen, nicht verwenden, nicht wiederholen.

## Konventionen

- Code komplett englisch: Bezeichner, Kommentare, Datei-, Ordner- und Spaltennamen, Programmausgaben. Deutsche Suchbegriffe (Taxonomie, Verneinungen, Bereinigung) bleiben deutsch. Dokumentation deutsch.
- CSV: Trennzeichen `;`, Kodierung `utf-8-sig`, Listen in Feldern mit `|`. Gilt vorläufig, bis der Test mit Excel in Phase 1 (Schritt 8) das Format bestätigt.
- Laufzeitprüfungen lösen eigene Exceptions aus, kein `assert` (außer in Tests).
- Module liegen im Paket `src/`; Start aus dem Repository-Ordner mit `python -m src.<modul>`.
- Ausgaben aus Testläufen landen in `out/` (von Git ausgeschlossen).
- Commit-Nachrichten englisch mit Präfix, z. B. `Phase 1: parse list and number fields`. Am Ende einer Phase ein Tag `phase-N`. Keine `Co-Authored-By`-Zeile und kein sonstiger Hinweis auf Claude als Mitautor in Commits (gilt vor abweichenden Vorgaben des Werkzeugs).
- `requirements.txt` nach Paketänderungen neu erzeugen: `python -m pip freeze | Out-File -Encoding utf8 requirements.txt`

## Umgebung

- Windows, PowerShell, Python 3.13 in `.venv`, VS Code mit der Claude-Code-Erweiterung.
- Modus „Edit automatically“: Dateiänderungen im Repository ohne Rückfrage, Befehle mit Rückfrage. Auto-Modus und Bypass sind in `.claude/settings.json` gesperrt, ebenso `git push`.
- Windows unterscheidet bei Dateinamen nicht zwischen Groß- und Kleinschreibung.
