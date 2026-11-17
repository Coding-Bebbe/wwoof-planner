# Arbeiten mit Claude Code in diesem Projekt

**Stand:** 15.11.2026, ergänzt am 17.11.2026 (Länderseiten der CWP, `docs/07_bedienung.md`) · Anleitung für dich. Die Regeln für Claude Code selbst stehen in `CLAUDE.md`.

---

## 1. Rollen

| Du | Claude Code |
|---|---|
| legst fest, was als Nächstes gebaut wird | schlägt den nächsten Schritt vor und setzt ihn nach deinem OK um |
| prüfst Vorschläge, Befehle und Änderungen | testet mit erfundenen Daten und erklärt jede Änderung |
| fragst nach, bis du den Code verstehst | beantwortet Fragen, ohne Code zu ändern |
| gibst Commits frei und pushst | committet nach deinem OK, pusht nie |
| startest alle Läufe mit echten Daten | startet nur Code mit erfundenen Daten |

Was du dabei lernst: Aufgaben so beschreiben, dass das Ergebnis passt; Code lesen und beurteilen; Änderungen prüfen, bevor sie ins Repository gehen; Tests als Absicherung nutzen; erkennen, wann ein Vorschlag falsch, zu groß oder unsauber ist.

---

## 2. Wie Claude Code den Projektkontext bekommt

- **`CLAUDE.md`** lädt Claude Code zu Beginn jeder Unterhaltung automatisch. Über einen Import darin wird auch **`docs/06_fortschritt.md`** jedes Mal mitgeladen.
- Die übrigen Dokumente in `docs/` liest Claude Code bei Bedarf.
- Eine neue Unterhaltung weiß nur, was in diesen Dateien steht. Deshalb aktualisiert Claude Code den Fortschritt in jedem Schritt.
- Das automatische Gedächtnis von Claude Code ist ausgeschaltet. Alles Wichtige steht im Repository und ist auf GitHub nachvollziehbar.
- Willst du eine dauerhafte Regel ändern, bitte Claude Code, `CLAUDE.md` anzupassen. Die Änderung ist dann im Commit sichtbar.

---

## 3. Ablauf eines Schritts

1. **Neue Unterhaltung starten** und den Stand abfragen (Prompt in Abschnitt 13).
2. **Vorschlag prüfen:** Ist das Ziel klar? Passen die Dateien? Gibt es ein Abnahmekriterium, also eine Prüfung, an der man sieht, dass es funktioniert? Ist der Schritt zu groß oder zu klein? Dann „Ok, umsetzen“ oder anpassen lassen.
3. **Umsetzung:** Claude Code ändert Dateien ohne Rückfrage. Vor jedem Befehl fragt es; den Befehl prüfst du (Abschnitt 6).
4. **Erklärung lesen** und nachfragen, bis du jede Änderung verstehst.
5. **Review** der Änderungen (Abschnitt 5).
6. **Commit:** Claude Code zeigt `git status`, die Dateien und eine Nachricht. Nach deinem OK committet es.
7. **Push:** Du führst im Terminal `git push` aus.
8. **Nächster Schritt in einer neuen Unterhaltung** (z. B. mit `/clear`). So bleibt der Kontext übersichtlich, und Claude Code arbeitet mit dem aktuellen Fortschritt.

---

## 4. Gute Aufträge formulieren

Ein guter Auftrag enthält **Ziel**, **Kontext**, **Abnahmekriterium** und **Grenzen**.

| Schwach | Besser |
|---|---|
| „Mach Schritt 6.“ | „Setz Schritt 6 um: Doppelungen über `profile_url` erkennen und mit Hof-Codes melden. Mit der Testdatei muss DE-VA-001/DE-VA-003 gemeldet werden. Nur `src/` und `docs/06_fortschritt.md` ändern.“ |
| „Das funktioniert nicht.“ | „`python -m src.farm_stats` bricht mit dieser Meldung ab: … Erklär mir die Ursache, bevor du etwas änderst.“ |
| „Mach den Code besser.“ | „Schau dir @src/farm_table.py an. Was würdest du verbessern und warum? Noch nichts ändern.“ |

Weitere Hilfen:

- **Dateien einbinden:** `@` und den Dateinamen tippen, z. B. `@src/farm_table.py`. Markierter Code im Editor geht automatisch mit; `Alt+K` fügt einen Verweis mit Zeilennummern ein.
- **Wenn du selbst noch unsicher bist:** „Stell mir Fragen, bis du den Schritt genau beschreiben kannst. Dann schlag ihn vor.“
- **Schrittgröße steuern:** „Fass die Schritte 6 und 7 zusammen.“ oder „Das ist mir zu viel auf einmal, teil es auf.“

---

## 5. Änderungen prüfen (Review)

**Wo du die Änderungen siehst:**
- In VS Code in der **Quellcodeverwaltung** (`Strg+Umschalt+G`): Liste der geänderten Dateien; ein Klick zeigt alt und neu nebeneinander.
- Im Terminal: `git status` (welche Dateien) und `git diff` (was genau).

**Checkliste vor jedem Commit:**
- Sind nur die erwarteten Dateien geändert oder neu?
- Verstehe ich jede Änderung? Wenn nicht: nachfragen.
- Ist das Abnahmekriterium erfüllt? Hast du die Ausgabe gesehen? Selbst einmal ausführen lohnt sich.
- Keine echten Daten, keine Pfade zu `wwoof-data`, keine Domain einer Länderseite außerhalb von `sites/`? Tests nur mit erfundenen Länderseiten-Dateien aus `tests/fixtures/`?
- Ausgaben und Logs nur mit Hof-Codes, site_id und Zahlen?
- Beim Sammler: Sind Pausen, Obergrenze, robots.txt-Prüfung und sauberer Abbruch eingebaut?
- Ist `docs/06_fortschritt.md` aktualisiert? Und `docs/07_bedienung.md`, wenn sich die Bedienung geändert hat?

**Rückgängig machen:** Claude Code bitten („Nimm die Änderung an X zurück“), zurückspulen (Abschnitt 9) oder selbst `git restore <datei>`.

---

## 6. Befehle freigeben

Claude Code fragt vor jedem Befehl. Einige rein lesende Befehle wie `ls`, `cat`, `git status` und `git diff` laufen ohne Rückfrage.

**Freigeben, wenn der Befehl nur erfundene Daten berührt:**
- `python -m pytest` (ab Phase 2)
- `python -m src.<modul>` mit Testdaten aus `tests/` oder Ausgaben nach `out/`
- `git add <einzelne Dateien>` und `git commit` nach deinem OK
- `python -m pip install …`, wenn das Paket vorher besprochen wurde

**Ablehnen:**
- alles, was `wwoof-data` enthält
- Skripte mit echter Konfiguration oder echten Daten (Sammler, Stichworte, Bereinigung, Export ohne Testpfad)
- alles mit einer Länderseite der CWP (z. B. wwoof.de, wwoofnorway.org) oder api.wwoof.net
- `git add .` oder `git add -A`
- Löschbefehle außerhalb von `out/`
- jeden Befehl, den du nicht verstehst. Lehne ab und frag: „Was macht dieser Befehl?“

**„Ja, nicht erneut fragen“:** Diese Option speichert eine dauerhafte Freigabe. Nutze sie in diesem Projekt nicht. Vor allem nicht für `python` oder `pytest`: Tests und Skripte schreibt Claude Code selbst, eine dauerhafte Freigabe würde also beliebigen Code ohne deinen Blick laufen lassen.

---

## 7. Modi

Die Modusanzeige unten im Eingabefeld zeigt den aktuellen Modus; ein Klick wechselt ihn.

| Modus | Was passiert | Wann nutzen |
|---|---|---|
| **Edit automatically** (Standard) | Dateien im Repository ändert Claude Code ohne Rückfrage, vor Befehlen fragt es | normale Schritte |
| **Plan** | Claude Code liest und plant, ändert aber nichts. Der Plan öffnet sich als Dokument, das du kommentieren kannst, bevor du ihn freigibst. Auch mit `/plan` | größere Schritte; reine Fragen |
| **Manual** | Jede Dateiänderung erscheint als Vergleich zum Annehmen oder Ablehnen, auch einzeln pro Änderung | heikle Stellen, z. B. Grenzen im Sammler oder der Export-Selbsttest |
| Auto, Bypass | gesperrt in `.claude/settings.json` | nie |

---

## 8. Fragen stellen, ohne dass sich etwas ändert

- **Einfach fragen.** `CLAUDE.md` legt fest: Fragen sind keine Aufträge. Claude Code beantwortet sie, ohne Dateien zu ändern.
- **Ganz sicher:** in den **Plan**-Modus wechseln. Dort kann Claude Code nichts ändern.
- **Kurze Nebenfrage:** `/btw` und deine Frage. Die Antwort erscheint in einem eigenen Bereich und belastet die Unterhaltung nicht.

Fragen, die beim Lernen helfen:
- „Erklär mir @src/farm_table.py Zeile für Zeile.“
- „Warum hast du das so gelöst und nicht mit …?“
- „Was passiert, wenn die Datei leer ist / eine Spalte fehlt / ein Wert keine Zahl ist?“
- „Zeig mir die Stelle, die die Obergrenze von 50 durchsetzt.“
- „Welcher Test prüft das, und wie würde er scheitern, wenn der Code falsch wäre?“
- „Was ist ein Dictionary / eine Exception / ein Fixture? Kurz, mit Beispiel aus unserem Code.“

---

## 9. Wenn etwas schiefläuft

- **Stoppen:** **Stop** klicken oder `Esc` drücken. Der laufende Durchgang endet; was Claude Code bis dahin geändert hat, bleibt erhalten.
- **Zurückspulen:** Maus über eine frühere Nachricht, dann die Schaltfläche zum Zurückspulen. „Rewind code to here“ setzt den Code auf diesen Stand zurück, die Unterhaltung bleibt. Das gilt nur für Dateien, die Claude Code mit seinen Dateiwerkzeugen geändert hat, nicht für Änderungen durch Befehle.
- **Git:** `git status` zeigt, was geändert ist; `git restore <datei>` stellt den letzten Commit-Stand her.
- **Nach zwei erfolglosen Korrekturen:** neue Unterhaltung mit einem besseren Auftrag, der das Gelernte enthält. Das klappt meist besser als eine dritte Korrektur.
- **Fehlermeldungen:** aus Testläufen komplett an Claude Code geben. Aus echten Läufen nur nach deiner Prüfung, ohne Hofdaten.

---

## 10. Datenschutz im Alltag

- **Echte Läufe (ab Phase 5) startest nur du**, in einem eigenen PowerShell-Fenster außerhalb von VS Code. Wie, beschreibt `docs/07_bedienung.md`, Teil A (Länderseite und Region in `config.yaml` wählen, starten, einloggen).
- Öffne **keine Dateien aus `wwoof-data` in VS Code**, solange das Claude-Panel offen ist. Echte Tabellen öffnest du in Excel oder LibreOffice.
- Keine Screenshots, Links oder Textauszüge echter Hofseiten in den Chat; stattdessen Platzhalter wie `<FARM_NAME>`.
- Fragt Claude Code nach `wwoof-data` oder will es einen echten Lauf starten: ablehnen und darauf hinweisen. Das ist ein Fehler, den wir beheben.
- GitHub Copilot ist für diesen Arbeitsbereich abgeschaltet. Lass es so, solange nicht geprüft ist, welche Dateien es an seinen Dienst sendet.

---

## 11. GitHub und Fortschritt

- **Pro Schritt ein Commit** (Claude Code nach deinem OK), danach **`git push`** (du).
- **Ende einer Phase:** Claude Code aktualisiert den Status in `README.md` und setzt nach deinem OK einen Tag `phase-N`. Du pushst ihn mit `git push origin phase-N`.
- **Ab Phase 2: GitHub Actions.** Nach jedem Push laufen die Tests auf GitHub. Das Ergebnis siehst du im Reiter „Actions“ des Repositorys und als Häkchen oder Kreuz am Commit.
- **`docs/06_fortschritt.md`** ist das Logbuch des Projekts: Stand, Schrittplan, Entscheidungen, Funde. Auf GitHub jederzeit lesbar.
- **`docs/07_bedienung.md`** ist die Bedienungsanleitung des Sammlers. Sie wächst mit den Phasen; eine Phase ist erst fertig, wenn dort ihre neuen Teile beschrieben sind.
- **claude.ai-Projekt:** nur noch für die Reiseplanung. Den Export (Phase 7) lädst du dort hoch.

---

## 12. Einmalige Einrichtung (15.11.2026)

- [ ] Dateien aus dem Paket in den Ordner `wwoof-planner` kopieren: `CLAUDE.md`, `.claude/settings.json`, `docs/`
- [ ] Claude-Code-Erweiterung in VS Code aktualisieren (Erweiterungen-Ansicht)
- [ ] VS-Code-Benutzereinstellung `claudeCode.initialPermissionMode` auf `acceptEdits`
- [ ] VS-Code-Arbeitsbereichseinstellung `chat.disableAIFeatures` aktivieren (Copilot aus)
- [ ] Neue Unterhaltung in Claude Code: Modusanzeige zeigt „Edit automatically“; unter „Permissions“ stehen die Deny-Regeln (`git push`, `wwoof-data`)
- [ ] Erster Schritt mit Claude Code: Schritt 0 aus `docs/06_fortschritt.md` (Umstellung prüfen und committen), danach `git push`

---

## 13. Spickzettel: Prompts

**Start einer Unterhaltung**
```
Fass kurz zusammen, wo wir stehen, prüf git status und schlag den nächsten Schritt vor. Noch nichts ändern.
```

**Umsetzen**
```
Ok, setz den Schritt um und erklär mir danach jede geänderte Datei.
```

**Nur fragen**
```
Nur eine Frage, nichts ändern: Warum …?
```

**Code erklären lassen**
```
Erklär mir @src/<datei>.py so, dass ich jede Zeile nachvollziehen kann. Neue Konzepte bitte mit einem Beispiel aus unserem Code.
```

**Fehler untersuchen**
```
Dieser Befehl schlägt fehl: <Befehl und vollständige Meldung>. Erklär mir zuerst die Ursache, dann schlag eine Lösung vor.
```

**Commit**
```
Zeig mir git status und schlag einen Commit vor.
```

**Phase abschließen**
```
Prüf die Abnahmekriterien der Phase und stell mir die Verständnisfragen.
```

---

## Quellen

- Claude Code in VS Code: https://code.claude.com/docs/en/vs-code
- Berechtigungsmodi: https://code.claude.com/docs/en/permission-modes
- Berechtigungen und Regeln: https://code.claude.com/docs/en/permissions
- CLAUDE.md und Gedächtnis: https://code.claude.com/docs/en/memory
- Best Practices: https://code.claude.com/docs/en/best-practices
- VS Code, KI-Funktionen abschalten: https://code.visualstudio.com/docs/setup/copilot
