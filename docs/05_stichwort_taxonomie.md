# Stichwort-Taxonomie (Entwurf, Version 1)

**Stand:** 01.11.2026

Diese Taxonomie ordnet Begriffe aus Hofbeschreibungen Kategorien zu. Das Skript `tagging.py` wendet sie **lokal und KI-frei** an (siehe `03_programmierprojekt.md`, Abschnitt 6). Die **Kategorieschlüssel** (z. B. `vegetables`) gehen in den Export für Claude. Den Text selbst bekommt Claude nur als bereinigte, von dir freigegebene Fassung (siehe `03_programmierprojekt.md`, Abschnitt 7). Für Beschreibungen, die du nicht freigegeben hast, sind die Kategorien die einzige Information aus dem Text, die Claude erhält.

Der Entwurf ist ein Startpunkt. In Phase 6 schärfst du ihn anhand der nicht abgedeckten Sätze nach.

**Sprache (Entscheidung vom 01.11.2026):** Schlüssel und Strukturbegriffe der YAML-Datei sind englisch, weil sie Teil des Codes sind. Die Suchbegriffe bleiben deutsch und englisch, so wie sie in Profilen vorkommen. Die `label`-Texte bleiben deutsch, weil sie nur Anzeigetexte für dich sind.

---

## 1. Wie der Abgleich funktioniert

1. **Normalisierung:** Text und Begriffe werden gleich behandelt: Kleinschreibung, ä→ae, ö→oe, ü→ue, ß→ss. In der YAML-Datei schreibst du Begriffe deshalb ganz normal, auch mit Umlauten.
2. **Drei Arten von Begriffen:**
   - `substring` (Teilwort): Der Begriff darf irgendwo im Wort stehen. Das ist nötig für deutsche zusammengesetzte Wörter („Milchziegen“, „Gemüsegarten“).
   - `whole_word` (ganzes Wort): Der Begriff muss ein ganzes Wort sein. Das ist für kurze und englische Begriffe nötig; sonst findet „hen“ auch „then“ und „when“.
   - `regex`: reguläre Ausdrücke für schwierige Fälle (fortgeschritten).
3. **`exceptions` (Ausnahmen):** Enthält ein Wort eine Ausnahme, zählt der Teilwort-Treffer in diesem Wort nicht. Beispiel: „schaf“ steckt auch in „Landwirtschaft“ und „schaffen“, daher die Ausnahmen „schaft“ und „schaff“.
4. **Verneinung (`settings.negations`):** Steht ein Verneinungswort bis zu 3 Wörter vor einem Treffer (`negation_window_words`), setzt das Skript einen Prüfhinweis (z. B. „keine Tiere“). Die Kategorie wird trotzdem vergeben und muss von dir geprüft werden.
5. **Ignorieren (`ignore`):** Sätze **ohne** relevanten Treffer, die einen Begriff aus `ignore` enthalten, gelten als „gesichtet, irrelevant“ (Begrüßungen und Ähnliches). Hat ein Satz einen relevanten Treffer, spielt `ignore` keine Rolle.
6. **Abdeckung:** Anteil der Sätze mit mindestens einem relevanten Treffer. Sätze ohne relevanten Treffer und ohne Ignorier-Treffer landen auf deiner lokalen Prüfliste.

**YAML-Falle:** In YAML werden `no`, `yes`, `on` und `off` ohne Anführungszeichen als Wahrheitswerte gelesen. Deshalb stehen solche Begriffe unten in Anführungszeichen.

---

## 2. Gruppen im Überblick

Im Export erscheinen die Kategorieschlüssel (in Klammern).

| Gruppe (Schlüssel) | Kategorien (Schlüssel) |
|---|---|
| Anbau (`cultivation`) | Gemüsebau (`vegetables`), Obstbau (`fruit`), Kräuter und Heilpflanzen (`herbs`), Getreide und Ackerbau (`grain`), Gewächshaus und Folientunnel (`greenhouse`) |
| Saat und Ernte (`sowing_harvest`) | Saatgut, Aussaat, Anzucht (`seeds_propagation`), Ernte (`harvest`) |
| Boden und Permakultur (`soil_permaculture`) | Boden und Kompost (`soil_compost`), Permakultur (`permaculture`), Agroforst und Hecken (`agroforestry_hedges`), Wald und Holz (`woodland_timber`) |
| Tierhaltung (`livestock`) | Ziegen (`goats`), Schafe (`sheep`), Rinder (`cattle`), Schweine (`pigs`), Geflügel (`poultry`), Pferde und Esel (`horses_donkeys`), Bienen und Imkerei (`bees`), Kameliden und Kleintiere (`camelids_small_animals`), Weide und Weidemanagement (`pasture`), Melken und Milch (`milking`) |
| Verarbeitung (`processing`) | Käse (`cheese`), Brot und Backen (`bread`), Haltbarmachen (`preserving`), Saft, Most und Wein (`juice_cider_wine`) |
| Vermarktung (`marketing`) | Hofladen und Markt (`farm_shop_market`), Solawi und Abokiste (`csa`) |
| Handwerk und Bau (`crafts_building`) | Bau und Reparatur (`building_repair`), Flechten (`weaving`) |
| Selbstversorgung und Technik (`self_sufficiency_tech`) | Selbstversorgung (`self_sufficiency`), Wasser und Energie (`water_energy`) |
| Lernen (`learning`) | Workshops und Kurse (`workshops_courses`) |
| Lage und Landschaft (`landscape`) | Berge (`mountains`), Gewässer (`water_bodies`), Wald und Wiese (`forest_meadow`), Schutzgebiet (`protected_area`) |
| Anbindung (`transport`) | ÖPNV (`public_transport`), Abholung (`pickup`) |
| Unterkunft (`accommodation`) | Unterkunftsart (`accommodation_type`) |
| Sprache (`language`) | Englisch (`english`) |
| Hinweise (`flags`) | Hausarbeit oder Kinderbetreuung (`housework`), Tourismus oder Gastronomie (`tourism_hospitality`) |

Die Hinweis-Kategorien dienen später der Bewertung: Laut der Charta von WWOOF Belgien gehören Haushalt, Tourismus und Gastronomie nicht zu den WWOOF-Tätigkeiten.

---

## 3. Taxonomie (YAML)

Diesen Block übernimmst du in Phase 6 als `taxonomy.yaml`.

```yaml
version: 1

settings:
  negations: [kein, keine, keinen, keinem, keiner, keines, nicht, ohne, "no", "not", without, never]
  negation_window_words: 3

ignore:
  substring: [willkommen, herzlich, "wir freuen uns", "liebe grüße", welcome, "looking forward", "hello"]

groups:

  cultivation:
    label: "Anbau"
    categories:
      vegetables:
        label: "Gemüsebau"
        substring: [gemüse, marktgarten, salat, tomate, kartoffel, kürbis, zucchini, möhre, karotte, kohl, vegetable, veggie, "market garden"]
        exceptions: [kohle]
      fruit:
        label: "Obstbau"
        substring: [obst, apfel, äpfel, kirsch, pflaume, zwetsch, beeren, orchard, fruit, apple, berries]
        whole_word: [berry]
        exceptions: [obstacl]
      herbs:
        label: "Kräuter und Heilpflanzen"
        substring: [kräuter, heilpflanz, "medicinal plant"]
        whole_word: [herb, herbs, herbal]
      grain:
        label: "Getreide und Ackerbau"
        substring: [getreide, ackerbau, weizen, roggen, dinkel, hafer, grain, cereal, wheat, arable]
      greenhouse:
        label: "Gewächshaus und Folientunnel"
        substring: [gewächshaus, folientunnel, polytunnel, greenhouse, glasshouse]

  sowing_harvest:
    label: "Saat und Ernte"
    categories:
      seeds_propagation:
        label: "Saatgut, Aussaat, Anzucht"
        substring: [saatgut, aussaat, anzucht, jungpflanz, pikier, setzling, sowing, seedling, propagat]
        whole_word: [säen, seed, seeds]
      harvest:
        label: "Ernte"
        substring: [ernte, harvest]
        exceptions: [lernte, fernte]

  soil_permaculture:
    label: "Boden und Permakultur"
    categories:
      soil_compost:
        label: "Boden und Kompost"
        substring: [kompost, mulch, gründüngung, humus, bodenaufbau, bodenpflege, bodenleben, compost, "cover crop", "no-dig", "no dig"]
        whole_word: [soil]
      permaculture:
        label: "Permakultur"
        substring: [permakultur, permaculture, waldgarten, "food forest", "forest garden", hügelbeet, hugelkultur, keyline, swale, mischkultur, polykultur, "companion planting"]
      agroforestry_hedges:
        label: "Agroforst und Hecken"
        substring: [agroforst, hecke, baumpflanz, baumschnitt, agroforestry, hedgerow, coppic, "tree planting"]
        exceptions: [check]
      woodland_timber:
        label: "Wald und Holz"
        substring: [forst, brennholz, holzarbeit, woodland, firewood, timber]

  livestock:
    label: "Tierhaltung"
    categories:
      goats:
        label: "Ziegen"
        substring: [ziege, zicklein, goat]
        exceptions: [ziegel]
      sheep:
        label: "Schafe"
        substring: [schaf, schäfer, lämmer, sheep]
        whole_word: [lamm, lamb, lambs, lambing]
        exceptions: [schaft, schaff]
      cattle:
        label: "Rinder"
        substring: [kuh, kühe, kälber, kalb, cattle]
        whole_word: [cow, cows, calf, calves]
        regex: ['rind(?!e\b|en)']
      pigs:
        label: "Schweine"
        substring: [schwein, ferkel]
        whole_word: [pig, pigs, piglet, piglets, swine]
      poultry:
        label: "Geflügel"
        substring: [huhn, hühner, henne, geflügel, gänse, laufente, entenhaltung, wachtel, chicken, poultry, duck]
        whole_word: [gans, ente, enten, hen, hens, goose, geese]
      horses_donkeys:
        label: "Pferde und Esel"
        substring: [pferd, esel, pony, ponies, horse, donkey]
        exceptions: [gesell]
      bees:
        label: "Bienen und Imkerei"
        substring: [biene, imker, honig, beekeep, beehive, apiar, honey]
        whole_word: [bee, bees]
      camelids_small_animals:
        label: "Kameliden und Kleintiere"
        substring: [alpaka, kaninchen, alpaca, rabbit, llama]
        whole_word: [lama, lamas]
      pasture:
        label: "Weide und Weidemanagement"
        substring: [weide, beweidung, weidegang, pasture, grazing]
        exceptions: [weidenflecht, weidenkorb, weidenkätzchen]
      milking:
        label: "Melken und Milch"
        substring: [melken, milch, milking, dairy]

  processing:
    label: "Verarbeitung"
    categories:
      cheese:
        label: "Käse"
        substring: [käse, cheese]
      bread:
        label: "Brot und Backen"
        substring: [brot, backen, backhaus, sauerteig, bread, baking, sourdough]
      preserving:
        label: "Haltbarmachen (Einkochen, Fermentieren)"
        substring: [einkochen, einmachen, fermentier, marmelade, dörren, ferment, pickl, canning, bottling, "food preserv", "preserving food"]
        whole_word: [jam]
      juice_cider_wine:
        label: "Saft, Most und Wein"
        substring: [saft, mosterei, apfelmost, süßmost, mostobst, wein, cider, juice, wine, vineyard]
        whole_word: [mosten]
        exceptions: [schwein, weinen, swine]

  marketing:
    label: "Vermarktung"
    categories:
      farm_shop_market:
        label: "Hofladen und Markt"
        substring: [hofladen, wochenmarkt, bauernmarkt, marktstand, "farm shop", "farmers market", "market stall"]
      csa:
        label: "Solawi und Abokiste"
        substring: [solawi, "solidarische landwirtschaft", abokiste, gemüsekiste, "box scheme"]
        whole_word: [csa]

  crafts_building:
    label: "Handwerk und Bau"
    categories:
      building_repair:
        label: "Bau und Reparatur"
        substring: [lehmbau, strohballen, zaun, zäune, reparatur, renovier, tischler, schreiner, zimmerei, holzbau, construction, carpentry, fencing, "straw bale", repair, woodwork]
        whole_word: [cob]
      weaving:
        label: "Flechten"
        substring: [weidenflecht, korbflecht, weaving, basket]

  self_sufficiency_tech:
    label: "Selbstversorgung und Technik"
    categories:
      self_sufficiency:
        label: "Selbstversorgung"
        substring: [selbstversorg, autark, subsistenz, homestead, self-sufficien, "self sufficien"]
      water_energy:
        label: "Wasser und Energie"
        substring: [solar, photovoltaik, regenwasser, bewässerung, komposttoilette, trockentoilette, irrigation, rainwater, "off-grid", "off grid", "compost toilet"]

  learning:
    label: "Lernen"
    categories:
      workshops_courses:
        label: "Workshops und Kurse"
        substring: [workshop, seminar, kurs, mentor]
        whole_word: [courses, teaching]
        exceptions: [diskurs, konkurs]

  landscape:
    label: "Lage und Landschaft"
    categories:
      mountains:
        label: "Berge"
        substring: [alpen, gebirge, bergblick, mountain]
        whole_word: [berg, berge, bergen]
      water_bodies:
        label: "Gewässer"
        substring: [fluss, seeblick, seeufer, badesee, "am see", küste, coast]
        whole_word: [lake, lakes, river, sea]
        exceptions: [einfluss, überfluss, abfluss]
      forest_meadow:
        label: "Wald und Wiese"
        substring: [wald, wiese, woods, meadow]
        whole_word: [forest]
        exceptions: [waldorf]
      protected_area:
        label: "Schutzgebiet"
        substring: [naturschutz, nationalpark, biosphär, naturpark, "nature reserve", "national park"]

  transport:
    label: "Anbindung"
    categories:
      public_transport:
        label: "ÖPNV"
        substring: [bahnhof, bushaltestelle, buslinie, öpnv, "train station", railway, "bus stop", "public transport"]
        whole_word: [zug, bus, busse, train]
      pickup:
        label: "Abholung"
        substring: [abholen, abholung, abgeholt, "pick up", "pick-up", pickup]
        regex: ['\bhol(?:e|en|t)\b[^.!?]{0,40}\bab\b']   # separable verb: "wir holen dich ... ab"

  accommodation:
    label: "Unterkunft"
    categories:
      accommodation_type:
        label: "Unterkunftsart"
        substring: [zimmer, wohnwagen, bauwagen, zelt, "tiny house", jurte, gästehaus, caravan, yurt, cabin]
        whole_word: [room, tent, tents]
        exceptions: [zimmermann, zimmerei]

  language:
    label: "Sprache"
    categories:
      english:
        label: "Englisch"
        substring: [englisch]
        whole_word: [english]

  flags:
    label: "Hinweise (für die Bewertung)"
    categories:
      housework:
        label: "Hausarbeit oder Kinderbetreuung"
        substring: [haushalt, kinderbetreuung, babysitt, putzen, housework, childcare, cleaning]
      tourism_hospitality:
        label: "Tourismus oder Gastronomie"
        substring: [ferienwohnung, gastronomie, gästezimmer, "bed and breakfast", hospitality]
        whole_word: [café, cafe]
```

---

## 4. Bekannte Grenzen dieses Entwurfs

- **Mehrdeutige Wörter:** „Weide“ kann Grasland oder Baum bedeuten, „Wald“ ist Landschaft und Tätigkeit zugleich. Mehrfachzuordnungen sind gewollt, Fehlzuordnungen zeigt der Abdeckungsbericht nicht. Deshalb gelegentlich die Treffer selbst stichprobenartig prüfen.
- **Ein Treffer pro Satz heißt nicht, dass der ganze Satz erfasst ist:** Die Abdeckungsprüfung markiert nur Sätze ganz ohne Treffer. Ein Satz mit einem Treffer kann weitere, nicht erfasste Informationen enthalten. Deshalb in jeder Runde auch einige abgedeckte Sätze stichprobenartig lesen.
- **Trennbare Verben:** Im Deutschen stehen Verbteile oft weit auseinander („wir holen dich am Bahnhof ab“). Für „abholen“ gibt es dafür eine Regex-Regel; bei anderen Verben fallen solche Fälle erst bei Stichproben auf und werden dann ergänzt.
- **Ortsnamen:** Begriffe wie „berg“ können in Ortsnamen stecken. „berg“ steht deshalb nur unter `whole_word`; Ortsnamen wie „Bamberg“ treffen dann nicht.
- **Andere Sprachen:** Englisch ist abgedeckt; für Norwegen kämen später norwegische Begriffe hinzu.
- **Lernkategorien der Plattform** stehen nicht in dieser Taxonomie. Sie werden in Phase 4 als feste Liste gesammelt und separat gespeichert.
