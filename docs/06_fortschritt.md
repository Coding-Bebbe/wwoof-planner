# Fortschritt

**Stand:** 18.11.2026 · Wird in jeder Sitzung geladen und bleibt deshalb kurz: Stand, Schrittplan der aktuellen Phase, Vormerkungen, offene Fragen. Entscheidungen und Verlauf stehen in `08_entscheidungsprotokoll.md`, Phaseninhalte in `03_programmierprojekt.md`, Abschnitt 8.

---

## 1. Stand

- Phasen 0 und 1 abgeschlossen (Tag `phase-1`).
- 17.11.2026: Hof-Sammler für alle Länderseiten der CWP (Commit `Docs: support CWP country sites`). Danach Neuausrichtung: Erkundung der Länderseite vorgezogen, Steckbrief statt Bereinigung und Freigabe, Doku verschlankt (`08_entscheidungsprotokoll.md`, letzter Eintrag).
- 18.11.2026: Schritt 2.1 erledigt: pytest mit Netzsperre, GitHub Actions (Workflow grün), `src/config.py` (Länderseiten-Dateien), `src/robots_check.py`, `sites/de.yaml` (`base_url` `https://wwoof.de`, vom Nutzer mit `python -m src.config de` geprüft).
- Länderseiten: Deutschland (`de`) Mitgliedschaft aktiv; Teil C, Schritte 3–5 erledigt (robots.txt vorhanden, Startseite erlaubt, kein Crawl-delay; Prüfung des Nutzers am 18.11.2026); Länder-Prüfung in Phase 2. Norwegen nächster Kandidat (`07_bedienung.md`, Teil C); Irland außerhalb des Umfangs.
- 18.11.2026: Schritt 2.2 erledigt: `src/page_skeleton.py`, `src/session.py`, `src/explore_site.py`; auf quotes.toscrape.com getestet (headless). Das Gate für deinen Lauf auf wwoof.de ist damit erfüllt (03, Phase 2).
- **Nächster Schritt:** Phase 2, Schritt 2.3 (du): Generalprobe auf toscrape mit Fenster, Vorab-Sichtung, Lauf auf wwoof.de (`07_bedienung.md`, A.0).

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
| 2.1 | pytest und GitHub Actions; `robots_check.py` mit Tests an erfundenem robots.txt-Text; `config.load_site()` mit den Prüfungen aus 03, Abschnitt 5.4; `sites/de.yaml` (Regionen nur mit Schlüssel und Kürzel); Tests mit erfundenen Länderseiten (`zz`, `site: no`) | Claude Code | erledigt (18.11.2026) |
| 2.2 | `page_skeleton.py` mit Tests an erfundenem HTML; `explore_site.py`; Testlauf auf quotes.toscrape.com; `07_bedienung.md`, Teil A.0 | Claude Code | erledigt (18.11.2026) |
| 2.3 | Generalprobe auf toscrape mit sichtbarem Fenster; Vorab-Sichtung von Hand; Lauf auf wwoof.de (Suchseite je Region, 2–3 Profile, ggf. Reiter; höchstens 5 Seiten je Lauf); Skelette prüfen und teilen | Nutzer | offen |
| 2.4 | Auswertung: Aufbau in 03 dokumentieren; Selektoren-Entwurf; erfundene Testseiten in `tests/fixtures/pages/`; offene Punkte 10–12 entscheiden | beide | offen |
| 2.5 | Attrappe: erfundener Export in `out/`; Test im claude.ai-Projekt; Export-Spalten und Steckbrief-Anforderungen festhalten | beide | offen |
| 2.6 | Abschluss: Verständnisfragen, README, Tag `phase-2` | beide | offen |

---

## 4. Vormerkungen

Nur Punkte, die nicht schon als Aufgabe in 03, Abschnitt 8, stehen.

| Phase | Punkt | Herkunft |
|---|---|---|
| 3 | Captcha und Login-Aufforderung im Seiteninhalt erkennen (Selektoren aus 2.4); bis dahin bricht der Nutzer die Erkundung mit Strg+C ab | 18.11.2026 |
| 3 | Skelett: Karten mit unterschiedlich langen Listen (1–2 statt ab 3 Einträgen) werden nicht zusammengefasst; bei Bedarf nachschärfen, wenn echte Skelette zu lang werden | 18.11.2026 |
| 3 | Regionswert exakt vergleichen; Warnung bei 0 Treffern erwägen (teilweise durch die Prüfung in `config.py` abgedeckt) | 08.11.2026 |
| Teil C | Bei jeder weiteren Länderseite: Normalisierung für die Sprache (z. B. æ, ø, å); Sprachcode für Norwegisch (`no` oder `nb`); Regel für erfundene Rufnummern des Landes in Testdaten | 17.11.2026 |
| alle | Dateinamen nicht aus Werten ableiten, die sich nur in der Schreibung unterscheiden (Windows) | 08.11.2026 |

---

## 5. Offene Fragen an den Nutzer

Keine. (Frage 1, `base_url` für Deutschland, am 18.11.2026 beantwortet: `https://wwoof.de`.)

Die offenen Punkte zur Reise und zum Sammler stehen in `00_projekt_uebersicht.md`.
