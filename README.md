# wwoof-planner

Privates Lern- und Planungsprojekt: KI-freie Python-Skripte, die Hofinformationen für eine WWOOF-Reise lokal erfassen und aufbereiten. Der Hof-Sammler ist für die Länderseiten der Common WWOOF Platform (CWP) gebaut, zuerst Deutschland; die Länderseite wird in der Konfiguration gewählt.

**Dieses Repository enthält keine echten Hofdaten.** Echte Daten liegen außerhalb des Repositorys. Die Testdaten in `tests/fixtures/` sind vollständig erfunden.

## Ordner

| Ordner | Inhalt |
|---|---|
| `src/` | Python-Code |
| `sites/` | eine Datei pro Länderseite, z. B. `de.yaml` (ab Phase 2) |
| `tests/fixtures/` | erfundene Testdaten |
| `out/` | Ausgaben aus Testläufen (nicht in Git) |
| `docs/` | Projektdokumentation: Plan, Regeln, Fortschritt |

## Arbeitsweise

Den Code schreibt Claude Code schrittweise; der Nutzer prüft, lässt sich erklären und pusht selbst.

- `CLAUDE.md`: Regeln für Claude Code (Arbeitsweise, Daten- und Plattformregeln)
- `docs/arbeiten_mit_claude_code.md`: Anleitung für die Zusammenarbeit
- `docs/06_fortschritt.md`: aktueller Stand, Schrittplan und Entscheidungen
- `docs/07_bedienung.md`: Bedienung des Sammlers, Checkliste für eine neue Länderseite

## Ausführen

Im Ordner `wwoof-planner` mit aktivierter virtueller Umgebung:

    python -m src.filter_region                 # filter by region, write to out/
    python -m src.farm_stats                    # guestbook counts, categories, duplicates
    python -m src.farm_pandas                   # same evaluations with pandas, compared
    python -m src.table_roundtrip prepare       # copy test table for the spreadsheet test
    python -m src.table_roundtrip compare       # compare after saving in Excel

Alle Skripte arbeiten mit den erfundenen Testdaten in `tests/fixtures/`.

## Stand

- [x] Phase 0 – Einrichtung
- [x] Phase 1 – Python-Grundlagen, Testdaten, CSV-Format
- [ ] Phase 2 – Konfiguration mit Länderseiten-Datei, robots.txt, pytest
- [ ] Phase 3 – HTML/CSS, Playwright auf Übungsseiten
- [ ] Phase 4 – wwoof.de erkunden (erste Länder-Prüfung)
- [ ] Phase 5 – Hof-Sammler
- [ ] Phase 6 – Stichworte und Bereinigung
- [ ] Phase 7 – Export
