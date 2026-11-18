# wwoof-planner

Privates Lern- und Planungsprojekt: KI-freie Python-Skripte, die Hofinformationen für eine WWOOF-Reise lokal erfassen und aufbereiten. Der Hof-Sammler ist für die Länderseiten der Common WWOOF Platform (CWP) gebaut, zuerst Deutschland; die Länderseite wird in der Konfiguration gewählt.

**Dieses Repository enthält keine echten Hofdaten.** Echte Daten liegen außerhalb des Repositorys. Die Testdaten in `tests/fixtures/` sind vollständig erfunden.

## Ordner

| Ordner | Inhalt |
|---|---|
| `src/` | Python-Code |
| `sites/` | eine Datei pro Länderseite, z. B. `de.yaml` |
| `tests/` | pytest-Tests; `tests/fixtures/`: erfundene Testdaten und Länderseiten |
| `.github/workflows/` | GitHub Actions: Tests nach jedem Push |
| `out/` | Ausgaben aus Testläufen (nicht in Git) |
| `docs/` | Projektdokumentation: Plan, Regeln, Fortschritt |

## Arbeitsweise

Den Code schreibt Claude Code schrittweise; der Nutzer prüft, lässt sich erklären und pusht selbst.

- `CLAUDE.md`: Regeln für Claude Code (Arbeitsweise, Daten- und Plattformregeln)
- `docs/arbeiten_mit_claude_code.md`: Anleitung für die Zusammenarbeit
- `docs/06_fortschritt.md`: aktueller Stand und Schrittplan
- `docs/07_bedienung.md`: Bedienung des Sammlers, Checkliste für eine neue Länderseite
- `docs/08_entscheidungsprotokoll.md`: Verlauf aller Entscheidungen

## Ausführen

Im Ordner `wwoof-planner` mit aktivierter virtueller Umgebung:

    python -m src.filter_region                 # filter by region, write to out/
    python -m src.farm_stats                    # guestbook counts, categories, duplicates
    python -m src.farm_pandas                   # same evaluations with pandas, compared
    python -m src.table_roundtrip prepare       # copy test table for the spreadsheet test
    python -m src.table_roundtrip compare       # compare after saving in Excel
    python -m pytest                            # run all tests
    python -m src.config de                     # check the country site file sites/de.yaml

Diese Befehle arbeiten nur mit erfundenen Testdaten aus `tests/` oder prüfen Dateien im Repository, ohne Netz. Skripte, die eine Länderseite aufrufen (z. B. die robots.txt-Prüfung), beschreibt `docs/07_bedienung.md`; sie startest nur du, im eigenen PowerShell-Fenster.

## Stand

- [x] Phase 0 – Einrichtung
- [x] Phase 1 – Python-Grundlagen, Testdaten, CSV-Format
- [ ] Phase 2 – Länderseite erkunden (pytest, robots.txt, Erkundungsskript, erste Länder-Prüfung)
- [ ] Phase 3 – Hof-Sammler
- [ ] Phase 4 – Erster Export (schlank)
- [ ] Phase 5 – Stichworte und Steckbrief
- [ ] Phase 6 – Vollständiger Export
