# WWOOF-Reise – Projektübersicht

**Stand:** 17.11.2026

**Zweck des Projekts:** zwei Ziele.

1. **Reise:** eine optimale 3–4-monatige WWOOF-Reise 2027 planen, mit Aufenthalten auf verschiedenen, möglichst guten Höfen, auf denen der Nutzer arbeitet und lernt. Planungsgrundlage für den Reisebeginn ist Juni 2027 (frühestens März).
2. **Programmierprojekt („Hof-Sammler“):** ein Projekt, das Ziel 1 so gut wie möglich unterstützt und bei dem der Nutzer Programmieren lernt. Der Sammler erfasst Hofinformationen von Länderseiten der Common WWOOF Platform (CWP) KI-frei und lokal, zuerst von wwoof.de.

**Vorrang (01.11.2026):** Der Sammler wird fertig, bevor die Kontaktphase beginnt; notfalls beginnt die Reise später.

---

## Dateien und Zuständigkeiten

Das Repository `wwoof-planner` ist die gültige Quelle für Code, Regeln und Fortschritt. Im claude.ai-Projekt ist nur der Reiseplan maßgeblich. **Jedes Thema steht an genau einer Stelle; andere Dateien verweisen darauf.**

| Datei | Ort | Zuständig für |
|---|---|---|
| `CLAUDE.md` | Repository | Arbeitsweise und harte Regeln für Claude Code (immer geladen) |
| `00_projekt_uebersicht.md` | `docs/` | Ziele, Dateien, Datenfluss, offene Punkte |
| `01_reiseplan.md` | nur im claude.ai-Projekt | Reiseziele, Zeitraum, Auswahlkriterien, Kontaktstrategie, Ablauf, Tracker, Länderinfos |
| `02_regeln_und_rahmenbedingungen.md` | `docs/` | Absprachen mit WWOOF, Datenregeln (was an Claude geht, was geteilt werden darf), Nutzungsbedingungen, Rechtsrahmen |
| `03_programmierprojekt.md` | `docs/` | Leitplanken, Ablauf, Datenmodell, Konfiguration, Steckbrief, Phasen |
| `04_technische_voraussetzungen.md` | `docs/` | Einrichtung des Laptops, Git und GitHub, Absicherung von Claude Code |
| `05_stichwort_taxonomie.md` | `docs/` | Stichwort-Kategorien, Sprachen, Steckbrief |
| `06_fortschritt.md` | `docs/` | Stand, Schrittplan der aktuellen Phase, Vormerkungen, offene Fragen (immer geladen, kurz) |
| `07_bedienung.md` | `docs/` | Bedienung: Erkundung, Sammellauf, Arbeitsschritte danach, neue Länderseite, Löschung, Meldungen |
| `08_entscheidungsprotokoll.md` | `docs/` | Verlauf aller Entscheidungen |
| `arbeiten_mit_claude_code.md` | `docs/` | Anleitung für den Nutzer zur Zusammenarbeit mit Claude Code |

Was Claude im claude.ai-Projekt erhalten darf und wie es Höfe bezeichnet, regelt `02_regeln_und_rahmenbedingungen.md`, Abschnitt 2. Die Projektanweisungen im claude.ai-Projekt pflegt der Nutzer dort selbst.

---

## Datenfluss auf einen Blick

```
Länderseite der Common WWOOF Platform (gewählt in config.yaml, zuerst wwoof.de;
Login des Nutzers je Länderseite)
   │  Erkundung (Phase 2): wenige Seiten, lokal gesichert; Struktur-Skelett
   │  ohne Inhalte geht nach Prüfung durch den Nutzer an Claude
   │  Hof-Sammler: KI-frei, vom Nutzer gestartet, eine Länderseite und eine
   │  Region pro Lauf, Pausen, Obergrenze, jeder Hof nur einmal
   ▼
Datenordner wwoof-data/ (nur auf dem Laptop, außerhalb des Code-Repositorys,
kein Zugriff für Claude)
   farms.csv (eine Tabelle für alle Länder; das Land steckt im Hof-Code):
              Hof-Code, Hofname, Ort, Originalbeschreibung, Lernmöglichkeiten,
              Anzahl Gästebucheinträge, freie Zeitfenster
   notes.csv: eigene Notizen des Nutzers (ohne Personenbezug)
   │  Stichwort-Kategorien und Steckbrief (automatisch; nur Werte aus festem
   │  Schema, kein Freitext)
   ▼
Export für Claude (Whitelist, mit Selbsttest; lädt der Nutzer selbst hoch)
   Stufe 1: Hof-Code, Ort, Region, Lernmöglichkeiten, Anzahl Gästebucheinträge,
            freie Zeitfenster, Notizen
   Stufe 2: zusätzlich Stichwort-Kategorien, Abdeckung, Steckbrief
   ▼
Claude: Bewertung, Route, Nachrichtenentwürfe (mit Hof-Codes und Platzhaltern)
```

---

## Offene Punkte

Die Nummern bleiben stabil, weil andere Dateien auf sie verweisen. Erledigte Punkte stehen in der zweiten Tabelle.

| Nr. | Punkt | Stand | Benötigt für |
|---|---|---|---|
| 1 | Reisezeitraum (Start, Ende) | Teilweise: Beginn frühestens März, eher Juni 2027; Planungsgrundlage Juni. Genaue Daten offen. | Grobroute, Kontaktkalender, Zeitraum für die Kalender-Erfassung im Sammler |
| 2 | Länder und Reihenfolge (genannt: z. B. Irland, Norwegen, Deutschland) | offen. Der Sammler deckt nur Länderseiten der CWP ab (17.11.2026); für Irland gibt es keinen Sammler. | Grobroute |
| 3 | Gewichtung der Kriterien (Lage, Bewertungen, Vielfalt der Tätigkeiten, …) | offen | Bewertungsraster, Attrappe des Exports (Phase 2), Steckbrief-Schema (Phase 5) |
| 4 | Fortbewegung: ÖPNV oder Auto | offen | Routenplanung |
| 7 | robots.txt der gewählten Länderseite prüfen | wird im Skript umgesetzt | Phase 2 und vor jedem Lauf |
| 10 | Abgrenzung der Region „bayerisches Voralpenland“ (Landkreise, Umkreis um einen Ort oder Filter der Plattform) | offen | Phase 2 |
| 11 | Gesamtumfang (Anzahl der Regionen) und Tagesgrenze für Läufe; gelten sie je Länderseite oder insgesamt? | offen; Hofzahlen je Region liefert die Erkundung (Phase 2) | vor Phase 3 |
| 12 | Kalender: Zeigt wwoof.de freie Zeitfenster an, und lassen sie sich zuverlässig auslesen? Für weitere Länderseiten Teil der Länder-Prüfung (`07_bedienung.md`, Teil C) | offen | Phase 2 |

### Erledigt

| Punkt | Ergebnis |
|---|---|
| Hofname an Claude | Entfällt (31.10.2026): Hofnamen bleiben in der lokalen Tabelle; Claude erhält Hof-Codes. |
| 5: Beschreibungen an Claude | Erledigt laut Nutzer (01.11.2026): Die Abklärung mit WWOOF umfasst bereinigte Beschreibungen. Seit 17.11.2026 gehen aus Beschreibungen nur noch Stichwort-Kategorien und der Steckbrief (Werte aus festem Schema) an Claude, kein Freitext. |
| 6: Nutzungsbeschränkungen der Common WWOOF Platform (Verbot automatisierter Zugriffe?) | Erledigt laut Nutzer (01.11.2026): Mit WWOOF Deutschland und dem Plattformbetreiber abgeklärt, dass Skript und Vorgehensweise in Ordnung sind; gilt laut Nutzer für alle Länderseiten der CWP (17.11.2026). Ausgeschlossen sind Massenabrufe und direktes KI-Browsing. |
| 8: Mitgliedschaft bei WWOOF Deutschland | Aktiv (01.11.2026). Ob das WWOOFer-Profil vollständig ist, prüft der Nutzer in Phase 2. |
| Gästebuch-Tenor | Gestrichen (01.11.2026): Relevant ist nur die Anzahl der Einträge. |
| 9: Absicherung der Datentrennung in Claude Code | Erledigt laut Nutzer (06.11.2026); Einzelheiten und Grenzen in `04_technische_voraussetzungen.md`, Abschnitt 8. |
