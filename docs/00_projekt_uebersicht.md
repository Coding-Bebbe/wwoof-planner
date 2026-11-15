# WWOOF-Reise – Projektübersicht

**Zweck dieses Projekts:** zwei Ziele.

1. **Reise:** eine optimale 3–4-monatige WWOOF-Reise 2027 planen, mit Aufenthalten auf verschiedenen, möglichst guten Höfen, auf denen der Nutzer arbeitet und lernt.
2. **Programmierprojekt („Hof-Sammler“):** ein Projekt, das Ziel 1 so gut wie möglich unterstützt und bei dem der Nutzer Programmieren lernt. Der Sammler erfasst Hofinformationen KI-frei und lokal.

**Stand:** 15.11.2026

---

## Dateien

Seit dem 15.11.2026 ist das Repository `wwoof-planner` die gültige Quelle für Code, Regeln und Fortschritt. Die Kopien dieser Dokumente im claude.ai-Projekt werden nicht mehr gepflegt; dort bleibt nur der Reiseplan maßgeblich.

| Datei | Ort | Inhalt |
|---|---|---|
| `CLAUDE.md` | Repository | Arbeitsweise und harte Regeln für Claude Code |
| `00_projekt_uebersicht.md` | `docs/` | Überblick, Status, Datenfluss, offene Punkte, Arbeitsregeln für Claude |
| `01_reiseplan.md` | nur im claude.ai-Projekt | Ziele, Zeitraum, Auswahlkriterien, Kontaktstrategie, Ablauf, Tracker, Länderinfos |
| `02_regeln_und_rahmenbedingungen.md` | `docs/` | Absprachen mit WWOOF, Datenregeln, Nutzungsbedingungen, Rechtsrahmen, Entscheidungen |
| `03_programmierprojekt.md` | `docs/` | Leitplanken, Architektur, Datenmodell und Lernplan des Hof-Sammlers |
| `04_technische_voraussetzungen.md` | `docs/` | Einrichtung des Windows-Laptops, Git und GitHub, Claude Code |
| `05_stichwort_taxonomie.md` | `docs/` | Stichwort-Kategorien für die Beschreibungen |
| `06_fortschritt.md` | `docs/` | Aktueller Stand, Phasenstatus, Entscheidungsprotokoll, nächste Schritte (pflegt Claude Code) |
| `arbeiten_mit_claude_code.md` | `docs/` | Anleitung für den Nutzer: zielführend mit Claude Code arbeiten |

Verweise in den Dateien nutzen die Kurznamen.

---

## Status (15.11.2026)

- **Reiseplanung:** Das Konzept steht (Arbeitsteilung siehe `01_reiseplan.md` im claude.ai-Projekt). Planungsgrundlage für den Reisebeginn ist **Juni 2027** (frühestens März). Vorrang hat, dass der Hof-Sammler vor der Kontaktphase fertig ist; notfalls beginnt die Reise später.
- **WWOOF:**
  - Die Organisationen haben auf die Anfrage zur KI-Nutzung geantwortet (siehe `02_regeln_und_rahmenbedingungen.md`, Abschnitt 1).
  - Laut Nutzer ist zusätzlich abgeklärt, dass der Hof-Sammler und die geplante Vorgehensweise in Ordnung sind. Ausgeschlossen bleiben Massenabrufe und direktes KI-Browsing.
  - Die Mitgliedschaft bei WWOOF Deutschland ist aktiv.
- **Datenfluss (festgelegt am 31.10. und 01.11.2026):**
  - Hofnamen bleiben lokal; Claude arbeitet ausschließlich mit Hof-Codes.
  - Das Skript erfasst die Anzahl der Gästebucheinträge (nur die Zahl) und, falls technisch gut möglich, die freien Zeitfenster aus dem Kalender.
  - Jeder Hof wird nur einmal erfasst und steht genau einmal in der Tabelle.
  - Code und Hofdaten liegen in getrennten Ordnern. Claude hat keinen Zugriff auf den Datenordner und startet keine Läufe gegen wwoof.de. Zusammengearbeitet wird mit Claude Code lokal auf dem Laptop.
  - Bereinigte Beschreibungen gehen nach Freigabe durch den Nutzer an Claude; laut Nutzer umfasst die Abklärung mit WWOOF das. Sie sind ein wichtiger Teil der Bewertung und Priorisierung.
- **Programmierprojekt:** Phase 0 ist seit 06.11.2026 abgeschlossen, Phase 1 ist in Arbeit (siehe `06_fortschritt.md`). Seit dem 15.11.2026 schreibt Claude Code den Code schrittweise; der Nutzer prüft, lässt sich erklären und pusht selbst (siehe `CLAUDE.md`).

---

## Datenfluss auf einen Blick

```
wwoof.de (Landesseite auf der Common WWOOF Platform, Login des Nutzers)
   │  Hof-Sammler: KI-frei, vom Nutzer gestartet, eine Region pro Lauf,
   │  Pausen, Obergrenze, jeder Hof nur einmal
   ▼
Datenordner wwoof-data/ (nur auf dem Laptop, außerhalb des Code-Repositorys,
kein Zugriff für Claude)
   farms.csv: Hof-Code, Hofname, Ort, Originalbeschreibung, Lernmöglichkeiten,
              Anzahl Gästebucheinträge, freie Zeitfenster, angezeigte Namen
   notes.csv: eigene Notizen des Nutzers (ohne Personenbezug)
   │  Stichwort-Kategorien (automatisch)
   │  Bereinigung der Beschreibung (automatisch) + Freigabe durch den Nutzer
   ▼
Export für Claude (Whitelist, mit Selbsttest; lädt der Nutzer selbst hoch)
   Hof-Code, Ort, Region, Lernmöglichkeiten, Stichwort-Kategorien,
   Anzahl Gästebucheinträge, freie Zeitfenster, Notizen,
   bereinigte Beschreibung (nur vom Nutzer freigegebene)
   ▼
Claude: Bewertung, Route, Nachrichtenentwürfe (mit Hof-Codes und Platzhaltern)
```

---

## Offene Punkte

Die Nummern bleiben stabil, weil andere Dateien auf sie verweisen. Erledigte Punkte stehen in der zweiten Tabelle.

| Nr. | Punkt | Stand | Benötigt für |
|---|---|---|---|
| 1 | Reisezeitraum (Start, Ende) | Teilweise: Beginn frühestens März, eher Juni 2027; Planungsgrundlage Juni. Genaue Daten offen. | Grobroute, Kontaktkalender, Zeitraum für die Kalender-Erfassung im Sammler |
| 2 | Länder und Reihenfolge (genannt: z. B. Irland, Norwegen, Deutschland) | offen | Grobroute |
| 3 | Gewichtung der Kriterien (Lage, Bewertungen, Vielfalt der Tätigkeiten, …) | offen | Bewertungsraster |
| 4 | Fortbewegung: ÖPNV oder Auto | offen | Routenplanung |
| 7 | robots.txt von wwoof.de prüfen | wird im Skript umgesetzt | Phase 2 und vor jedem Lauf |
| 10 | Abgrenzung der Region „bayerisches Voralpenland“ (Landkreise, Umkreis um einen Ort oder Filter der Plattform) | offen | Phase 4 |
| 11 | Gesamtumfang (Anzahl der Regionen) und Tagesgrenze für Läufe | offen | vor Phase 5 |
| 12 | Kalender: Zeigt wwoof.de freie Zeitfenster an, und lassen sie sich zuverlässig auslesen? | offen | Phase 4 |

### Erledigt

| Punkt | Ergebnis |
|---|---|
| Hofname an Claude | Entfällt (31.10.2026): Hofnamen bleiben in der lokalen Tabelle; Claude erhält Hof-Codes. |
| 5: Beschreibungen an Claude | Erledigt laut Nutzer (01.11.2026): Bereinigte, vom Nutzer freigegebene Beschreibungen dürfen an Claude gehen; die Abklärung mit WWOOF umfasst das. Sie sind ein wichtiger Teil der Bewertung und Priorisierung. |
| 6: Nutzungsbeschränkungen der Common WWOOF Platform (Verbot automatisierter Zugriffe?) | Erledigt laut Nutzer (01.11.2026): Mit WWOOF abgeklärt, dass das Skript und die Vorgehensweise in Ordnung sind. Ausgeschlossen sind Massenabrufe und direktes KI-Browsing. Damit ist das Gate vor Phase 4 erfüllt. |
| 8: Mitgliedschaft bei WWOOF Deutschland | Aktiv (01.11.2026). Ob das WWOOFer-Profil vollständig ist, prüft der Nutzer in Phase 4. |
| Gästebuch-Tenor | Gestrichen (01.11.2026): Relevant ist nur die Anzahl der Einträge. Laut Nutzer gibt der Host Einträge zur Veröffentlichung frei, daher sind sie in der Regel positiv. |
| 9: Absicherung der Datentrennung in Claude Code | Erledigt laut Nutzer (06.11.2026): Claude Code lokal; Read-Deny-Regel für `wwoof-data` eingerichtet und getestet (Leseversuch abgelehnt). Seit 15.11.2026 zusätzlich Projekteinstellungen in `.claude/settings.json` (Auto-Modus und Bypass gesperrt, keine Lesezugriffe der Dateiwerkzeuge außerhalb des Repositorys). Die Grenze bleibt: Die Regeln greifen nicht bei Skripten, die Dateien selbst öffnen; deshalb startet Claude keine Skripte mit echten Daten (Regeln 7 und 8). Einzelheiten in `04_technische_voraussetzungen.md`, Abschnitt 8. |

---

## Arbeitsregeln für Claude in diesem Projekt

1. **Sprache und Stil:** Antworte auf Deutsch, präzise und ohne unbegründete Vermutungen. Kennzeichne Unsicheres als solches.
2. **Keine personenbezogenen Daten von Gastgeber:innen** annehmen oder verarbeiten: keine Hofnamen, Personennamen, Kontaktdaten, Adressen, Koordinaten, Fotos, Screenshots, unbereinigten Profiltexte, Gästebuch- oder Bewertungstexte, Nachrichten im Wortlaut, Profil-Links, Benutzernamen oder Profil-IDs.
3. **Erlaubt an Claude:** Hof-Code, Ort (Gemeinde bzw. nächster Ort, ohne Adresse), Region, Land, Lernkategorien, Stichwort-Kategorien, Anzahl der Gästebucheinträge, freie Zeitfenster sowie eigene Notizen des Nutzers ohne Personenbezug. **Bereinigte Beschreibungen**, sofern der Nutzer sie freigegeben hat.
4. **Hof-Codes:** Claude bezeichnet Höfe ausschließlich mit Hof-Codes (z. B. `DE-VA-003`). Nachrichtenentwürfe enthalten Platzhalter `[HOFNAME]` und `[NAME]`, die der Nutzer selbst einsetzt.
5. **Versehentlich geschickte Personendaten**, auch Reste in bereinigten Beschreibungen (z. B. ein Vorname): darauf hinweisen, nicht verwenden und nicht wiederholen.
6. **Keine Web-Recherche zu einzelnen Höfen**, weil dabei mit hoher Wahrscheinlichkeit Personendaten auftauchen.
7. **Kein Zugriff auf die WWOOF-Plattform durch Claude:** kein Lesen von Profilseiten, kein KI-Browsing, kein Versand über den Account, kein Zugriff auf das Postfach. Claude startet auch keine Skripte, die wwoof.de aufrufen. Jeden Lauf gegen wwoof.de startet der Nutzer selbst.
8. **Datenordner:** Claude erhält keinen Zugriff auf den Datenordner `wwoof-data/` (Hoftabelle, Notizen, Namensliste, Berichte, Logs, Browser-Profil) und fragt in Claude Code auch nicht danach. Claude führt Code nur mit erfundenen Testdaten aus. Code, Konfiguration und Fehlermeldungen ohne Hofdaten können geteilt werden; HTML-Quelltext von Hofseiten nie (Details in `03_programmierprojekt.md`, Abschnitt 10).
9. **Der Hof-Sammler bleibt KI-frei:** Die Skripte rufen keine KI-Dienste auf.
10. **Code auf Englisch:** Bezeichner, Kommentare, Datei- und Ordnernamen, Spaltennamen, Konfigurationsschlüssel und Programmausgaben sind englisch. Ausnahme sind deutsche Begriffe, nach denen der Code sucht (Taxonomie, Verneinungen, Formulierungen bei der Bereinigung). Die Dokumentation bleibt deutsch.
11. **Arbeitsweise (seit 15.11.2026):** Claude Code schreibt den Code schrittweise und erklärt jede Änderung; der Nutzer prüft, fragt nach und pusht selbst. Am Ende jeder Phase stellt Claude Code Verständnisfragen. Einzelheiten in `CLAUDE.md`.
12. **Fortschritt:** Claude Code pflegt `docs/06_fortschritt.md` nach jedem Schritt.
