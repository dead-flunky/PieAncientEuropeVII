# PAE – Prüfbericht Civilopedia-Konzepte (Stand 7.19b, Commit d23836c)

Geprüft: alle 65 Texte in `Assets/XML/Text/PAEGameText_Concepts_Pedia.xml` (deutsch), abgeglichen mit Python, DLL und XML.
Zeilenangaben „Z.“ beziehen sich auf den Beginn des Konzepts in `PAEGameText_Concepts_Pedia.xml`.

**Formales, gut:** Die Datei ist reines ASCII. Es gibt keine verbotenen Zeichen, und Englisch ist überall vorhanden und eigenständig übersetzt.
**Formales, Fehler:** In RELIGION ist `[LINK=BUILDING_REL_STEUER]…[/LINK]` falsch geschlossen. Richtig ist `[\LINK]`. Das betrifft alle 5 Sprachen: Z. 11718, 11843, 11970, 12097, 12225.
**Doppelte Datei:** `Assets/XML/GameInfo/CIV4BasicInfos.xml` ist eine veraltete Kopie. Civ4 lädt nur `BasicInfos/CIV4BasicInfos.xml`. Die Kopie bitte löschen.

---

## A. Code-Fehler (hier Code ändern, nicht Text)

| # | Datei:Zeile | Fehler | Fix |
|---|---|---|---|
| 1 | `PAE/PAE_Christen.py:265` | `myRandom(iChance) < iChance` ist immer wahr, Bekehrung zu Judentum/Islam also immer 100 % | `if CvUtil.myRandom(100, "convertCity") < iChance:` |
| 2 | `PAE/PAE_Unit.py:2964` | Elite nach Sieg: Bedingung `< 70`, gesetzt wird aber `30`. Ein Elite mit 30–69 Schaden wird dadurch sogar **geheilt** | `pWinner.setDamage(70, -1)` |
| 3 | `PAE/PAE_City.py:1117` | KI „zahlt“ bei der Revolte, bekommt aber Gold (`changeGold(iBetrag)`) | `pPlayer.changeGold(-iBetrag)` |
| 4 | `PAE/PAE_City.py:1191` | Nachbarstadt-Revolte wählt nur Städte mit **mehr** Verteidigern als Einwohnern, also gerade die gut bewachten. Vermutlich vertauscht | `if pLoopCity.getPopulation() > pLoopCity.plot().getNumDefenders(iOwner):` (bitte bestätigen, ob so gemeint) |
| 5 | `PAE/PAE_Christen.py` ca. 482–500 | Pagane Einrichtungen: Off-by-one `iRand > iChance`, Chancen je 10 Punkte höher als gedacht | Text oder Code angleichen |

---

## B. Fehlende Konzepte (Mechaniken, die in keinem Konzept beschrieben sind)

Nach Wichtigkeit sortiert:
1. **Handel**: Handelskarren und Karawanen, Kauf/Verkauf/Diebstahl von Boni, automatische Handelsrouten (Popup 744–748), Händlerraub, Begleitschutz (762), Handelsstraßen, Städte mit Sonderbedarf, Forschungsschub, Höchstzahl an Handelseinheiten, Projekt Seidenstraße. Ein Konzept TRADE gibt es zwar, Teile davon stecken aber in MOVEMENT (siehe C). Prüfen, ob TRADE alles abdeckt, und den Raub nur dort beschreiben.
2. **Jagd**: Jäger, Jagdradius (8 Felder im Szenario, sonst Standard), erlegte Tiere bringen Nahrung, Held durch Großwild, Lager/Turm/Schürflager bauen (771, 4 Gold), Tiere einfangen und domestizieren.
3. **Eroberungsfolgen**: Partisanen, Große Persönlichkeiten fangen (50/40/10 %), Tech durch Eroberung (ab Pop 3), Reliquien, Siegesstele, Deportation, Flüchtlinge, abtrünnige Stadt (706: behalten, versklaven, zerstören), Beutegold, Goldkarren (677).
4. **Moral und Segen**: Hagia Sophia, Zeus, Rhetorik, Sklavenopfer (752/759/760) und wie sie im Kampf verbraucht werden.
5. **Einheiten umrüsten und kaufen**: Auf-/Absitzen (666/667), Elefanten (776), Katapult-Munition (775), Edle Rüstung (699), Wellen-Öl (701), Magnetkompass (767), Schiffsreparatur/Crew (768), Einheit verkaufen (695), Trojanisches Pferd (697).
6. **Stadtbrand und Feuerwehr**: Brandchance, Schutz durch Brunnen/Zisterne/Feuerwehr, Brandeinheiten, neues Event „Trümmer oder Wiederaufbau“ (7.19). Waldbrand.
7. **Emigranten und Stadt auflösen** (672/673/753): Auswanderung bei Unzufriedenheit, Emigrant → Latifundium/Dorf, Stadt auflösen.
8. **Inquisition und Religionsaustreibung** (665/704), Missionare (731), Großer Prophet bestimmt die Heilige Stadt bzw. terraformt (769/774). Teilweise in RELIGION, dort prüfen.
9. **Thing** (germanische Versammlung, ab Demokratie) als Gegenstück zu den Panhellenischen Spielen.
10. **Spieloptionen**: Pandora, Seth, Armageddon, Apokalypse, kein PAE-Kampf, keine Rodung, keine Katastrophen. Ein kurzes Konzept oder ein Abschnitt in „Wichtige Fakten“.
11. **Bewegungsregeln aus der DLL**:
    - Flussüberquerung ohne Straße oder Brücke kostet alle Bewegungspunkte.
    - Furten.
    - Wagen und Streitwagen dürfen Wald nur auf Straßen betreten.
    - Verletzte Einheiten und Schiffe sind langsamer.
    - Römer- und Perserstraßen sind nicht plünderbar.
    - Straßenbau auf fremdem Gebiet gibt einen Diplomatie-Bonus.
    - Türme, Forts, Limes und Kastell geben +1 Sicht.
12. **Kleineres**:
    - Karten zeichnen (728: 7 Kategorien mit Kosten und Chancen).
    - Limes (733).
    - Strandgut und Treibgut.
    - Höhlen und Barbarenfestungen (2 Goldkarren).
    - Stadtruinen.
    - Verfall unbewirtschafteter Verbesserungen.
    - Nahrungskosten beim Einheitenbau.
    - Gebäude ohne Ressource oder ohne passende Staatsform werden entfernt.
    - Stadtstaaten bauen keine Siedler.
    - Sümpfe verschwinden durch Kanalisation oder Deich.
    - Warft erzeugt einen Hügel.
    - Wunder-Sondereffekte (Babel, Göbekli Tepe, 10 Gebote).
    - Umbenennung der Völker in der Spätantike.

---

## C. Korrekturen je Konzept

### Tabellen, die neu aus dem XML erzeugt werden sollten (fast komplett veraltet)
- **IMPROVEMENTS (Z. 6527)**: Kosten und Techs stimmen nicht mehr. Beispiele:
  - Fischerboote 5/5, Lager 4, Holzfäller 6 (Bronzeverarbeitung), Hütte 10/10 (Staatenbildung)
  - Weide 10/10 (Abgrenzungen), Weingut 15/20, Brunnen 12 (Bewässerungskanäle), Plantage 20/20
  - Steinbruch 15/20, Mine 25/20, Straße 8, Via Romana 20, Persische Straße 15
  - Spähturm 5, Wachturm 10, Forts 20/30, Handelsposten 0 (Konservierung)

  Die Wassermühle gibt es nicht mehr. Es fehlen Ölpresse, Torf, Latifundium, Kastell, Limes und Salzmine.
- **COMBAT_PEDIA / Fernangriff (Z. 3734)**: Die Werte sind veraltet. Beispiele:
  - Jäger 3/40 %/1, Plänkler 7, Peltast 8, Beritt./Kamelbogen 12, Feuerkatapult 6/70 %
  - Balliste 7/1, ohne Kollateralschaden

  „Nubischer Bogenschütze“ heißt jetzt „Medjau“, Decareme heißt „Deceris“. Es fehlen Speerwerfer, Arquites, Faris, Scorpio, Katapeltes und Dreimannstreitwagen.
- **FORMATIONS (Z. 4944)**: Fast alle Werte sind veraltet. Beispiele:
  - Schildwall ±20/+10 % Gelände; Keil +20 gegen Speer, +20 im Wald; Gasse +20
  - Flanke und Zange ±20; Parther nur +50 % Rückzug; Fourage +5 Heilung

  Es fehlen Kohorte, Phalanx II und Festung. Flucht: ab 70 % Schaden, nur Fußtruppen mit 1 Bewegungspunkt.

### Zahlen und Chancen (Spieler planen danach)
- **NATURAL_DISASTERS (Z. 8799)**:
  - Seesturm, Tornado, Heuschrecken: Ohne Armageddon wird alle 60 Runden **eine** davon ausgewürfelt (50/25/25 %). Halbiert wird das Intervall ab **400 v. Chr.**
  - Sandsturm: ab 400 v. Chr. 45 statt 90.
  - Meteoriten: 2 bis 20, Bonus 33 %.
  - Komet: 25 % Bonus, zusätzlich 25 % auf einen See.
  - Erdbeben: neue Ressourcen nur auf Hügeln.
  - Globale Katastrophe:
    - Hütten werden zu 50 % zerstört.
    - Ebene wird zu Savanne, Grasland zu Wald.
    - Dörfer werden zu Weilern, Straßen zu Pfaden.
    - Nahrungsspeicher werden geleert.
    - Mit Apokalypse fallen alle Städte auf Pop 2.
- **PIRACY (Z. 10834)**:
  - Plündern auf Stufe 0–I: 1 % statt 10 %.
  - Massakrieren und Versklaven: 10 %.
  - Abwanderung nur, wenn das Dorf schrumpft, und nur in eigene Städte im Umkreis von 3.
  - Jede Plünderung gibt 20 % Chance auf die nächste Stufe.
- **SLAVE (Z. 13233)**:
  - Prüfung mit 20 % pro Runde, nicht „jede 4. Runde“.
  - Sterberaten sinken durch Techs: Haus 4→2→1, Feld 6→3→2, Bergwerk 8→4→3 %.
  - Ein stehender Sklave ersetzt einen gestorbenen.
  - Christwerden 1:20.
  - Christenaufstand ca. 0,5 % pro Runde, 30 Schaden.
- **RESERVISTS (Z. 12309)**: Prüfung mit 20 % pro Runde, dann 2 % Tod, nur wenn im selben Durchgang kein Sklave starb.
- **CHRISTEN (Z. 1387)**:
  - Chancen: Stadt und Sklavenmarkt 80, Stadt 70, Sklavenmarkt 60 %, +20 % mit Sklavenquartieren, keine Bekehrung hinduistischer oder buddhistischer Städte.
  - „44 Runden später“ heißt richtig „im Jahr 44 n. Chr.“.
  - Judentum/Islam: 75 % gilt nur für die Hauptstadt (siehe Code-Fehler A1).
  - Judenaufstand 2 %, bei Unzufriedenheit 6 %; Israel kann entstehen.
  - Christenverfolgung ist komplett anders als beschrieben: ab 44 n. Chr., 20 % der Runden × 2/75, jede Stadt, 2 Runden Revolte, +30 Schaden.
- **CITIES (Z. 1804)**:
  - Anarchie: Mensch 10 %, KI 5 %.
  - Fremde Religion: gemeint ist die fehlende Staatsreligion. Nur Städte mit Stadtstatus, nicht unter Henotheismus, nicht mit Großem Pantheon; 2 % (KI 1,3 %), 4 Runden.
  - Schrumpfen während einer Revolte: 25 %.
  - Überlaufen:
    - Nicht bei Beschützend-Trait, mindestens 2 Verteidiger, nicht mit „Keine Städtezerstörung“.
    - „+1/+2 % pro Revoltedauer“ gibt es nicht.
    - Rechenbeispiel richtig: 14.
    - „5. +4 %“ steht doppelt.
  - Grippe „ab 2“ widerspricht LEPRA_PLAGUE („ab 6“).
- **CIVIL_WAR (Z. 2523)**:
  - Schaden 20–39 pro Runde (max. 90); Tod ab mehr als 74 %.
  - Ende: KI 1:5. „Keine Auswirkung“: Mensch 50 %, KI 75 %.
  - Beim Ausbruch Stadtmauer halbiert, 50 % auf −1 Pop.
  - Den Auslöser „Verschmutzung“ gibt es nicht. Richtig: Religionskonflikt, Sehnsucht nach der Heimat, fremde Religion.
- **COMBAT2 (Z. 2768)**:
  - Tech-Bonus 10–20 %.
  - Verbrannte Erde: Nur Forts und Hütten werden zu Ruinen.
  - Flucht:
    - Nur Verteidiger können fliehen; Standard max. 5 %.
    - Dorf 20 %, Gemeinde 30/15 %.
    - Tiere 40/20, 60/30, 80/40 %.
    - Schiffe 80 % (Sieger ≥ 50 % Schaden), Generalsformation 100 %.
  - Pferdeverlust: Einheiten mit Absteige-Variante werden zu 50 % zu Fußtruppen und hinterlassen kein Pferd; 30 % Pferd nur bei Streitwagen ohne Absteige-Variante. Die Goten fehlen in der Liste.
- **COMBAT3 (Z. 3406)**:
  - „Unzuverlässig verlieren“ hat zwei Mechanismen: Angriffssieg 20/50 %; Rang 25/50 %, KI 33 %. In einem Konzept zusammenführen.
  - Salär: Stärke·3 + 3 je Beförderung, Erfolg 80 %.
  - Legendär → General: ohne Kriegsmüdigkeit-Bedingung, nur im eigenen Gebiet, Rückfall auf „Trainiert“, verliert Held und die Hälfte der XP.
- **DECIMATION (Z. 3943)**: Salär 80 %, Desertieren 20 %, Rangverlust erst ab Routiniert.
- **LOYAL (Z. 7354)**:
  - Beispiel 2 ergibt 60 %.
  - Gefangennahme 25 % Einheit / 75 % Sklave.
  - Führerschaft schützt; Belagerungs- und Handelseinheiten laufen nicht über; Corvus I/II/III 30/50/75 %.
- **BARBARIANS (Z. 726)**:
  - Seevölker: 1 + Kartengröße + Schwierigkeitsgrad Spawnversuche (halbiert auf Landkarten); 2 Schiffe nur mit Aggressiven Barbaren ab 1000 v. Chr.
  - Hunnen: „alle 10 Jahre“, geteilt durch die Startära; Tribut nur über 100 Gold.
  - Wikinger: ab 600 n. Chr., bis 4 Schiffe.
  - Alle Schwierigkeitsgrade haben 400 Runden (skaliert mit dem Tempo).
- **ANIMALS (Z. 215)**:
  - Gelände: Wölfe auch in Tundra, Leoparden im Dschungel, Esel im Wald, Pferde auch in Tundra, Hyänen nur in der Wüste.
  - Bergziegen streichen (Einheit existiert nicht).
  - Ergänzen: Elefant, Löwe auf Löwen-Bonus, Spawn erst ab Runde 150 auf unbesetzten, unsichtbaren Feldern.
  - Pferde und Kamele meiden jedes Feature, Wildschweine bleiben im Wald.
- **BONUSVERBREITUNG (Z. 871)**:
  - 80 % nur für Getreide und Plantagen, die man schon besitzt; sonst 100 %.
  - Es gibt **fünf** Prioritäten.
  - Abschnitte Pferd/Kamel-Prioritäten streichen (veraltet).
  - Preis regional ×1, national ×2, international ×3.
  - Fischerboot vs. Handelsschiff klären: richtig sind Arbeitsboot und Handelseinheiten, Tech Aquakultur.
- **DESERTIFICATION (Z. 4069)**:
  - Chancen je Ära: Wald 4/5/6,7 %, Savanne bzw. modernisiert 6,7/10/20 %, Dichter Wald 2/2,5/3,3 %.
  - Lager schützen; Minen im Wald haben Priorität 1.
  - Hunde und Brennende Schweine verursachen Rodung. Ausgenommen sind Pferd, Kamel, Elefant und Aufklärer.
- **FOG_OF_WAR (Z. 4780)**:
  - Hauptstädte und Wunderstädte bleiben **immer** sichtbar; ab Kartographie auch das Meer.
  - 50 % Chance pro Feld; die KI ist nur alle 20 Runden betroffen.
- **FAQ (Z. 4279), IMPORTANT_FACTS (Z. 6471), MOVEMENT (Z. 8597), PAE_SUPPLY (Z. 10231)**:
  - Die Stapelgrenze hängt vom Schwierigkeitsgrad ab (10–20, KI +20), Pflicht erst **über** dem Limit. Nur in PAE_SUPPLY definieren, sonst verweisen.
  - FAQ: Zufriedenheits- und Gesundheitsbonus 2–3.
- **PAE_SUPPLY (Z. 10231)**:
  - Plünderung: Plantage +30; „Stadt +25“ ist die Gemeinde.
  - Nur Versorger auf demselben Feld werden aufgeladen; +1 XP nur auf fremdem Gebiet.
  - Vasallenstadt 33 %.
  - Stadtschaden: Pop-Verlust 20 % erst ab Pop > 3, Nahrung nur bei mehr als 10 im Speicher.
- **REBELLION (Z. 11485)**:
  - 25 % pro Runde, nicht jede 3. Runde.
  - Nur wenn Versorgungstickets **fehlen**.
  - KI +0,5 % pro Einheit.
  - Nachbarstadt-Revolte 3 Runden (siehe A4).
- **RELIGION (Z. 11672)**:
  - Die Tech heißt „Verbot & Verfolgung“; Religionskonflikte erst ab Prinz.
  - Judentum: 2/3 Chance auf +1 tolerierte Religion.
  - Schritt 4a: 3:4 mit Auswanderer. Schritt 4b: ca. 1:20.
  - Kriegsdienstverweigerung bei jeder fremden Staatsreligion, Ende mit Toleranzedikt (außer Exklusivismus).
  - Pagane Einrichtungen: siehe A5.
  - Austreibung: nicht möglich für Religionen heiliger Städte und für die Staatsreligion; Pop-Verlust ab > 1.
  - [LINK]-Fehler, siehe oben.
- **PROMOTIONS (Z. 11031)**:
  - Häuserkampf/Garnison nur in Städten mit Status „Stadt“, nur für Axt, Schwert und Bogen.
  - Geländebeförderung ab 2 passenden Feldern.
  - Schiffe 5 % je Wasserfeld, erst ab 4.
  - Werte: Hinterhalt 20, Rückzugstaktik 20, Tarnung 20, Taktik +10 Rückzug, Gesegnet 25.
  - Wüstenfuchs I–V; doppelte Bewegung kommt von „Wüstenschiff“.
- **STATTHALTER (Z. 14234)**:
  - Tribut: Pop × 6 + bis 1/3 Zufall.
  - Kein Tribut ab Polyarchie.
- **TRADE (Z. 14380)**:
  - Einheiten: Gaulos braucht Handelsschiffe; der Händler fehlt; Handelsposten brauchen Warenhandel und Status Kolonie.
  - Preise: Raritäten 25, Grundmodifikator 125.
  - +25 % gilt für Handelskarren und Karawanen.
  - Fremdkauf 125 % − 5 % je Haltungsstufe.
  - Forschungsbonus Preis/10 × Ära.
  - Straßenwerte (×3/×4) widersprechen „+1“.
- **UNITCOST (Z. 14919)**: Ergänzen: keine Nahrungskosten unter Bauernmiliz, KI zahlt die Hälfte, Reis zählt nicht als Getreide; „10 Prozentpunkte“.
- **USURPATOR (Z. 16619)**:
  - Provinzhauptstädte rebellieren beim Generalstod zu 25 % (Seth 50 %).
  - KI: 1/25 Usurpator, sonst zahlt sie 1/3 ihres Goldes.
- **GENERALDEATH (Z. 6013)**:
  - Seth 50 %.
  - Provinzhauptstädte: Einheiten verletzt, Mauer −2/3, 33 % Bürgerkrieg.
- **VASSALS (Z. 16695)**:
  - Tech Vasallentum nötig.
  - Städtelimit 5 (aggressiv 3).
  - „Wahrscheinlichkeit 2“ ist eine Oder-Alternative.
- **OLYMPIC_GAMES (Z. 9817)**:
  - Teilnahme ab Schaukampf, Ende mit 2. Konzil.
  - Kalender Monate/Jahreszeiten: 48/16 Runden, 3/4 Goldkarren.
  - 25 % Chance auf ein Fuhrwerk.
- **LEPRA_PLAGUE (Z. 7123)**:
  - KI-Chancen reduziert (Lepra ÷3, Pest ÷2).
  - Pest: Modernisierungen zu 1/3, Seuchenfelder, Einheiten auf Nachbarfeldern 15–44 Schaden.
- **MERCENARY_ASSIGN (Z. 7615)**: Folter-Kosten ¾, ½ oder ¼ der Grundkosten; KI alle 17 Runden mit 50/40/30 %.
- **MERCENARY_HIRE (Z. 8100)**: Aufschlag +5 % pro Anheuerung in derselben Runde.
- **7_WONDERS (Z. 3)**: Zeus braucht Elfenbein, die Gärten einen Damm, der Koloss eine Schmiede in einer Küstenstadt. Pyramiden und Zeus verlangen die Religion als Staatsreligion.
- **BUILDING_PROMO (Z. 1379)**: Seekrieg ab Navigation IV.
- **KOLONIE_PROVINZ (Z. 6837)**: Provinzpalast braucht 4 Städte mit Stadtstatus. Die −25 % Kriegsverdruss im XML nicht gefunden (bitte prüfen).
- **KULTE (Z. 6958)**: Dionysos braucht TECH_KUNST, Kybele TECH_SENSE (prüfen). Englisches „and“ im Deutschen.
- **GG_ACTIONS (Z. 6264)**:
  - Die Links „Kampf VI“ und „Arzt III“ zeigen auf „Legende“ bzw. „Sanitäter III“.
  - Revolte endet sofort (nicht nach 1 Runde).
  - „Heroic Epic“ heißt „Heldenepos“.
- **SPIONAGE (Z. 13922)**: „Raumschiffteil sabotieren“ ist ein BTS-Überbleibsel.
- **MOVEMENT (Z. 8597)**: Der Raub-Abschnitt steht doppelt (auch in TRADE). Bedingungen: Ware geladen, allein auf dem Feld; ohne Schutz 3/5 Tod; die KI verliert nur die Ware.

### Tippfehler (Auswahl)
„Menüoberfäche“, „könne gejagt“, „Pferdressourcen“, „Überfalle“, „ausgebilden“ (2×), „Chistentums“, „gückliche“, „letzen“ (2×), „Gedächnissen“, „Vorausetzung“ (2×), „Usurbatoren“, „Triumpfbögen“, „Fruchbarkeitsgötter“, „lebten mussten“, „der der Gegner“, „Sölderntum“, „Minimalste Chance ist auf jedem Fall“, „Bulgarien/Asturien/Dakien“ (Völker → Bulgaren/Asturier/Daker), „Handesweg“, „gibts es“, „aussichtlosen“, „Obisidian“, „Elephant“, „Berechungen“, „Provinzshauptstadt“, „ründlichen“, „Vasalls“, „Infantrie“, „Lieutnant“, „Kriegesbande“, „Betriebssystemem“, „Wie haben“, „daß“, „während dem/einem“ → „während des/eines“.

---

## D. Empfehlungen zur Struktur
1. **Lange Konzepte gliedern** mit Unterüberschriften: NATURAL_DISASTERS (Wetter, Großkatastrophen, global, Intervalltabelle), SLAVE (Erwerb, Einsatz, Ansiedlung, Risiken, Aufstände), RELIGION (Regeln zuerst, Geschichte ans Ende), TRADE, CITIES (Revolten/Überlaufen eigenes Konzept), COMBAT2 (Flucht eigenes Konzept).
2. **Jede Regel nur an einer Stelle**: Stapelgrenze → PAE_SUPPLY; Raub → TRADE; Unzuverlässig → COMBAT3; Salär → DECIMATION. Anderswo nur verlinken.
3. **Versionsgeschichte raus** („komplett überarbeitet“, „ab PAE V“): Spieler brauchen den aktuellen Stand.
4. **Tabellen aus dem XML erzeugen** (Fernangriff, Verbesserungen, Formationen). Das kann ich bei Bedarf als Text vorbereiten, dann veralten sie nicht wieder unbemerkt.
5. **Neue Konzepte aus Abschnitt B**: zuerst Handel (falls TRADE es nicht abdeckt), Jagd, Eroberungsfolgen, Stadtbrand/Feuerwehr, Moral/Segen, Einheiten umrüsten, Spieloptionen.
