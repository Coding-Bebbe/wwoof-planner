# Fortschritt

**Stand:** 18.11.2026 · Wird in jeder Sitzung geladen und bleibt deshalb kurz: Stand, Schrittplan der aktuellen Phase, Vormerkungen, offene Fragen. Entscheidungen und Verlauf stehen in `08_entscheidungsprotokoll.md`, Phaseninhalte in `03_programmierprojekt.md`, Abschnitt 8.

---

## 1. Stand

- Phasen 0 und 1 abgeschlossen (Tag `phase-1`).
- 17.11.2026: Hof-Sammler für alle Länderseiten der CWP (Commit `Docs: support CWP country sites`). Danach Neuausrichtung: Erkundung der Länderseite vorgezogen, Steckbrief statt Bereinigung und Freigabe, Doku verschlankt (`08_entscheidungsprotokoll.md`, letzter Eintrag).
- 18.11.2026: Schritt 2.1 erledigt: pytest mit Netzsperre, GitHub Actions, `src/config.py` (Länderseiten-Dateien), `src/robots_check.py`, `sites/de.yaml` (`base_url` `https://wwoof.de`).
- Länderseiten: Deutschland (`de`) Mitgliedschaft aktiv, Länderseiten-Datei angelegt, Länder-Prüfung in Phase 2; Norwegen nächster Kandidat (`07_bedienung.md`, Teil C); Irland außerhalb des Umfangs.
- **Beim Nutzer offen (aus 2.1):** `python -m src.config de` (prüft `sites/de.yaml`); nach dem Push den Workflow „tests“ im Reiter „Actions“ prüfen; optional `python -m src.robots_check de` im eigenen Fenster (07, A.3), Ergebnis nur als Status und Zahlen melden.
- **Nächster Schritt:** Phase 2, Schritt 2.2.

---

## 2. Phasen

| Phase | Inhalt | Status |
|---|---|---|
| 0 | Einrichtung | erledigt (06.11.2026) |
| 1 | Python-Grundlagen, erfundene Testdaten, CSV-Format | erledigt (17.11.2026) |
| 2 | Länderseite erkunden (erste Länder-Prüfung: Deutschland) | offen |
| 3 | Hof-Sammler, erste Region erfassen | offen |
| 4 | Erster Export (schlank) | offen |
| 5 | Stichworte und Steckbrief | offen |
| 6 | Vollständiger Export | offen |

---

## 3. Schrittplan Phase 2

| Nr. | Schritt | Wer | Status |
|---|---|---|---|
| 2.1 | pytest und GitHub Actions; `robots_check.py` mit Tests an erfundenem robots.txt-Text; `config.load_site()` mit den Prüfungen aus 03, Abschnitt 5.4; `sites/de.yaml` (Regionen nur mit Schlüssel und Kürzel); Tests mit erfundenen Länderseiten (`zz`, `site: no`) | Claude Code | erledigt (18.11.2026); Workflow auf GitHub prüft der Nutzer nach dem Push |
| 2.2 | `page_skeleton.py` mit Tests an erfundenem HTML; `explore_site.py`; Testlauf auf quotes.toscrape.com; `07_bedienung.md`, Teil A.0 | Claude Code | offen |
| 2.3 | Vorab-Sichtung von Hand; Lauf auf wwoof.de (Suchseite je Region, 2–3 Profile, ggf. Reiter); Skelette prüfen und teilen | Nutzer | offen |
| 2.4 | Auswertung: Aufbau in 03 dokumentieren; Selektoren-Entwurf; erfundene Testseiten in `tests/fixtures/pages/`; offene Punkte 10–12 entscheiden | beide | offen |
| 2.5 | Attrappe: erfundener Export in `out/`; Test im claude.ai-Projekt; Export-Spalten und Steckbrief-Anforderungen festhalten | beide | offen |
| 2.6 | Abschluss: Verständnisfragen, README, Tag `phase-2` | beide | offen |

---

## 4. Vormerkungen

Nur Punkte, die nicht schon als Aufgabe in 03, Abschnitt 8, stehen.

| Phase | Punkt | Herkunft |
|---|---|---|
| 2.2 | `crawl delay` aus der robots.txt als Mindestpause der Erkundung verwenden (`RobotsRules.crawl_delay`) | 18.11.2026 |
| 2.2 | Netzsperre in `tests/conftest.py` mit Playwright unter Windows prüfen (Loopback ist erlaubt) | 18.11.2026 |
| 3 | Regionswert exakt vergleichen; Warnung bei 0 Treffern erwägen (teilweise durch die Prüfung in `config.py` abgedeckt) | 08.11.2026 |
| Teil C | Bei jeder weiteren Länderseite: Normalisierung für die Sprache (z. B. æ, ø, å); Sprachcode für Norwegisch (`no` oder `nb`); Regel für erfundene Rufnummern des Landes in Testdaten | 17.11.2026 |
| alle | Dateinamen nicht aus Werten ableiten, die sich nur in der Schreibung unterscheiden (Windows) | 08.11.2026 |

---

## 5. Offene Fragen an den Nutzer

Keine. (Frage 1, `base_url` für Deutschland, am 18.11.2026 beantwortet: `https://wwoof.de`.)

Die offenen Punkte zur Reise und zum Sammler stehen in `00_projekt_uebersicht.md`.
