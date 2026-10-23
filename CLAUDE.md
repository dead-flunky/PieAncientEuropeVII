# PAE – Übergabe an Claude Code (Stand 7.19.1n) => wird als öffentlicher Patch dann zu 7.19.1

Repo: github.com/dead-flunky/PieAncientEuropeVII
Ziel: Bestes Spielerlebnis, verbesserte KI, optimierte Codes.

## Arbeitsweise
- Civ IV BTS: Python 2.4 (Ganzzahl-Division!), C++ DLL, XML.
- Einrückung mit Tabs.
- Code inline im bestehenden Stil, möglichst wenige neue `def`-Funktionen.
- Antworten auf Deutsch, mit genauer Datei- und Zeilenangabe.
- Änderungen nicht selbst einbauen, nicht committen, nicht pushen. Dateien im Repo nur lesen.
- Jede Änderung im Chat so angeben: Datei, Zeile, Funktion, darunter „Alt:“ und „Neu:“ als Codeblock.
  Mehrere Stellen in einer Datei von unten nach oben (höchste Zeilennummer zuerst).
- Multiplayer: Spielzustand nur in `onModNetMessage` ändern (über `sendModNetMessage`), kein `getActivePlayer` in Spiellogik, kein Python-Zustand außerhalb des Spielstands, globale Listen/Dicts aus `PAE_Lists` vor Änderung kopieren.
- Multiplayer, `onModNetMessage`: Der Handler läuft auf allen Rechnern. Nur Popups (`addPopup`) und Töne an `getActivePlayer()` koppeln, nie die Zustandsänderung. Falsch: `if iPlayer != getActivePlayer(): return` vor dem ganzen Handler oder `if isHuman() and iPlayer == getActivePlayer(): ... else: KI-Zweig` (andere Rechner laufen dann in den KI-Zweig). Richtig: Menschen-Zweig zuerst über `isHuman()` trennen, darin nur das Popup an den aktiven Spieler koppeln. Ein Python-Fehler, der nur auf manchen Rechnern auftritt (z. B. `gc.getPlayer(-1)` in einem `elif` nach `getActivePlayer`), ist ebenfalls OOS.
- Popups mit dynamischen Buttons: Die Button-Nummer im Callback muss mit derselben Liste und denselben Bedingungen ausgewertet werden, mit der das Popup gebaut wurde (sonst verrutschen die Buttons, z. B. Söldner 708, Inquisition 704). Daten für die Netzwerknachricht im Sender prüfen: `iData2` des Buttons weitergeben, nicht versehentlich `pPlot.getX()` (Kompass 767).
- KI (`AI_unitUpdate`): Jeder Zweig mit `return True` muss die Züge verbrauchen (finishMoves, Mission, kill, Upgrade), sonst läuft die DLL-Schleife 40–120 Mal.
- Pitboss: `getActivePlayer()` ist auf dem Host -1, `gc.getPlayer(-1)` liefert `None`. Nie ohne Prüfung auf -1 verwenden.
- Zufall nur für Anzeige (Popup-Texte): `gc.getASyncRand().get(n, "...")`, nie `myRandom` in Blöcken mit `getActivePlayer`.
- Text-XML: nur Zeichen aus Latin-1 (bis U+00FF), Sonderzeichen als `&#228;` usw. Nicht erlaubt: Gedankenstrich (–), Minuszeichen (−), Auslassungspunkte (…), Aufzählungspunkt (•), Œ, Längezeichen (ā ē ĭ ḥ), schmales Leerzeichen (U+202F) – auch nicht als `&#…;`-Code. Civ IV kann sie im Spiel nicht darstellen.
- Python: DLL-Funktionen, die eine Stadt liefern (`getPlotCity`, `getCity`, `getCapitalCity`, `getWorkingCity`, `getHolyCity` usw.), liefern nie `None`, sondern ein leeres Objekt. Immer `pPlot.isCity()` oder `pCity.isNone()` prüfen, `pCity is not None` ist dort immer wahr. `is None` nur bei eigenen Funktionen/Parametern, die wirklich `None` zurückgeben (z. B. `PAE_Unit.getNearestCity`).
- DLL, KI: `AI_chooseBuilding/AI_chooseUnit/AI_chooseProcess` geben bei Erfolg sofort einen Bauauftrag (`pushOrder`). Zum reinen Prüfen `AI_bestBuildingThreshold` bzw. `AI_bestUnitAI` verwenden.
- DLL, Sicht: `CvPlot::seeFromLevel()` hängt bei PAE vom Ausbau ab (Turm, Fort, Limes, Kastell). Wer Sichthöhe oder Sichtweite ändert, muss vorher `updateSeeFromSight(false, true)` und nachher `(true, true)` aufrufen, sonst bleiben Felder dauerhaft schwarz.
- DLL, Spieloptionen: Reihenfolge in `CvEnums.h` (GameOptionTypes) und `CIV4GameOptionInfos.xml` muss identisch sein, Name in `CyEnumsInterface.cpp` exakt gleich.
- Alte Spielstände werden nie berücksichtigt: keine Sonderfälle in `read`/`write` (kein Umbau von `CvInitCore::read` bei neuen Spieloptionen, keine neuen `uiFlag`-Stufen für einzelne Updates). Neue Member-Variablen einfach in `read`/`write` aufnehmen. Nach solchen Änderungen sind alte Spielstände inkompatibel, das ist so gewollt.
- DLL: `GET_PLAYER(x)` nie mit einem Wert, der `NO_PLAYER` sein kann (z. B. `plot()->getOwner()`). Index -1 schreibt in fremden Speicher -> CtD ohne Meldung, oft viel später.
- DLL: Nach Python-Ereignissen (`CvEventReporter`) kann das Objekt geloescht sein (Stadt per `acquireCity`, Einheit per `kill`). Vorher Besitzer/ID merken und danach pruefen.
- Debuggen: VC++ 2010 Express -> Projekt-Eigenschaften der aktiven Konfiguration, Debugging: Befehl `Civ4BeyondSword.exe`, Argument `mod=\Pie'sAncientEurope`. HEAP-Meldungen „Invalid address specified to RtlValidateHeap“ sind bei der Debug-DLL Rauschen (verschiedene C-Laufzeiten).
- Python: Gebaeude zerstoeren/auswaehlen nur ueber `getNumRealBuilding(i) > 0`, nicht `isHasBuilding(i)` (das ist auch bei freien Gebaeuden durch Wunder/Konzern/Staatsform wahr, `setNumRealBuilding(i, 0)` entfernt diese nicht).
- Zeilenangaben bei mehreren Änderungen in einer Datei immer von unten nach oben (höchste Zeilennummer zuerst), damit sich die übrigen Zeilen nicht verschieben.
- Python: Ressourcen auf Feldern fuer Spieleraktionen mit `pPlot.getBonusType(iTeam)` abfragen, nicht `getBonusType(-1)` (das zeigt auch noch nicht erforschte Ressourcen).
- Python, ScriptData von Einheiten/Städten: nie roh vergleichen (`pUnit.getScriptData() == "X"`), sondern `CvUtil.getScriptData(pUnit, ["t"]) == "X"`. PAE schreibt weitere Schlüssel dazu (z. B. "P", "ifp"), danach ist der Rohtext JSON. In WBSave-Dateien: `ScriptData={"t": "Name"}`.
- `PAE_Unit.doUpgradeVeteran` übernimmt keine ScriptData der alten Einheit (Szenario-Helden verlieren ihre Kennung beim Rang-Upgrade).
- Events (`CvRandomEventInterface.py`): `PythonCanDo` und `PythonHelp` laufen auch nur lokal beim Popup-Aufbau → kein Zufall, keine Zustandsänderung, sonst OOS. Zufall nur in `PythonCanTrigger*` und `PythonCallback`. Jede im Event-XML genannte Python-Funktion muss existieren (fehlende `PythonCanDo` → uninitialisierter Wert in der DLL).
- Event-XML kann viel ohne Python: `UnitCombatPromotions`/`UnitClassPromotions` (alle + künftige Einheiten), `iImprovementChange`, `iBonusChange`, `iRouteChange` (-1 = entfernen) auf dem Trigger-Feld.
- Texte kommen zeitversetzt: Neue oder geänderte TXT_KEYs werden ins Online-Text-Tool übernommen und erst später als Text-XML ins Repo exportiert. Fehlen sie nach einem Commit im Repo, ist das kein Fehler. Bei Kontrollen nur kurz als "Texte noch offen" erwähnen und mit der Liste unter "Offen" abgleichen. Neue Keys dort eintragen, sobald sie geliefert sind; nach dem Export prüfen (auch auf das Leerzeichen im Tag) und streichen.
- TXT_KEYs: Manche Einträge bekamen ein Leerzeichen im Tag (`<Tag> TXT_KEY…`) → Key wird nicht gefunden. Nach Text-Änderungen oder ab und zu mal bei allen prüfen.
- AudioDefines im Repo können `/DE/-Pfade` oder auch `/EN/`-Pfade. Die Audiofiles (Gesprochene Tech-Zitate) dafür sind nicht im Repo.
- Texte für Text-XMLs (Konzepte, Pedia, Meldungen) als XML liefern (`<TEXT>` mit `<Tag>` und allen fünf Sprachen English, French, German, Italian, Spanish), in UTF-8 und ohne `&#…;`-Codes. Das Online-Text-Tool kann auch die XML-Struktur der neuen TXT_KEYs importieren. Bei Änderungen an einem bestehenden Text ohne den `<TEXT>`-Block und TXT_KEY und Stelle (von-bis) mit Vorschautext nennen. Überall gerade Anführungszeichen ("), keine typografischen („ “ « »). Die Zeichenregel oben (nur Latin-1, keine Gedankenstriche usw.) gilt trotzdem.
- Denkweise: extrem praktisch und der Situation entsprechend. Lieber eine kleine, nachvollziehbare Lösung an Ort und Stelle (z. B. eigener kleiner Wert in Python) als eine saubere, aber aufwendige Umbaulösung (DLL-Refactoring, neue Schnittstellen, ScriptData). Erst die einfache Variante vorschlagen, die große nur, wenn es nicht anders geht. Es sei denn irgendwas kann woanders auch verwendet werden (oder ähnliches wird verwendet), dann eine eigene Funktion dafür schreiben und die andere Stelle optimieren.


## Offen
1. „Pirat werden“ (722): bleibt vermutlich bewusst nur für Menschen (bestätigen).
2. DLL-Check: Stellen ohne PAE-Markierung durchsehen.

Optional:
- P1: Latifundium-/Dorfsuche pro Sklave über die ganze Karte → Kandidaten einmal pro Spieler und Runde cachen.
- Beobachten/feinjustieren: KI-Lagerbonus `iValue += 150` (`CvCityAI::AI_bestPlotBuild`), Armee-Richtwert vor Forschung (`CvCityAI::AI_chooseProduction`, PAE-Block Research), Mindestverteidiger über `iBarbarianDefenders` (`AI_minDefenders`).
- Beobachten/feinjustieren: KI-Stadtangriff ab 80 % Stapelstaerke (`CvUnitAI::AI_stackAttackCity`, Untergrenze `iPowerThreshold`, BTS 110). Bei hohen Verlusten auf 90 erhoehen.
- Beobachten: Feuerkatapult-Schwelle (kleiner Raze-Wert ab 50, `CvGameUtils.AI_unitUpdate`), Terraforming-KI ab 3 Feldern.


## Patch 7.18.3.10–14 (Claude Code)

**Bugfixes**
- **Sicht/schwarze Felder** (`CvPlot::setImprovementType`): Bau oder Verlust von Turm/Fort/Limes/Kastell änderte `seeFromLevel` ohne Neuberechnung → Sichtzähler negativ, Felder blieben schwarz. Jetzt `updateSeeFromSight` vor/nach der Änderung.
- **Eigenschaften nach Laden weg** (`CvPlayer::read/write`): `m_dynTraits` wurde nie gespeichert → `hasTrait()` nach dem Laden immer False (z. B. TRAIT_IMPERIALIST in `canDoCivic`). Jetzt gespeichert (`uiFlag` 2).
- **KI baute Massen an Kriegern/Flachbögen** (`CvCityAI::AI_chooseProduction`, PAE-Block Research): Die Prüfung mit `AI_chooseBuilding/AI_chooseUnit` gab jedes Mal Aufträge. Jetzt `AI_bestBuildingThreshold` + Armee-Richtwert. Folge vorher: Überfüllung → Ungesundheit → Pest.
- **Esel aufladen auf dem Feld ×3 Preis** (`PAE_Cultivation._calculateBonusBuyingPrice4Cultivation`): `pCity is None` → `not pPlot.isCity()`.
- **Erdbeben zerstörte Palast** (`PAE_Disasters.doDestroyCityBuildings`): Gebäude mit `isCapital()` werden verschont.
- **Ausladen an Flussufern per Go-To** (`CvSelectionGroup::isAmphibPlot`): `isCoastalLand()` ignoriert seit PAE Süßwasser → zusätzlich jedes angrenzende Wasserfeld.
- **Auswanderungsanzeige** (`CvMainInterface.py`, PAE_EmigrationText): zeigte den Aufstandstext. Jetzt gleiche Bedingungen wie `PAE_City.doEmigrantSpawn`, neue Texte `TXT_KEY_MAIN_EMIGRATE_DANGER_4–6` (Anarchie, ohne Staatsreligion, Steuern) in `PAEVII.xml`.
- **Waldbrand** (`CvPlot::doFeature`): breitet sich nur noch auf Wald in Ebenen aus, `iDisappearance` 2000.

**Neu**
- Spieloption `GAMEOPTION_NO_DEFORESTATION` (nach NO_ESPIONAGE): keine Waldrodung beim Einheitenbau (`CvEventManager.onUnitBuilt` → `PAE_City.doDesertification`).
- Zweiter Siedler auf Large/Huge für Mensch und KI (`CvEventManager.onUnitBuilt`), XML-Limit bleibt 1.
- KI verlässt brennende Felder (`CvSelectionGroup::doTurn` weckt auf, `CvUnitAI::AI_update` zieht weg).
- KI baut Lager/Holzfällerlager im Wald ohne Ressource (`CvCityAI::AI_bestPlotBuild`, +150).
- KI-Mindestverteidiger je Stadt = `iBarbarianDefenders` des Schwierigkeitsgrads (`CvCityAI::AI_minDefenders`).
- Indra-Kult braucht Hinduismus in der Stadt (`BUILDING_CORPORATION_9` PrereqReligion).
- `BUILD_HUNTING_CAMP` ohne PrereqTech (von keiner Einheit genutzt, Jäger baut Lager für 4 Gold ohne zu sterben).
---

## Patch 7.18.3.15–16 (Claude Code)

**Bugfixes**
- **CtD durch Speicherfehler beim Straßenbau** (`CvUnit::build`): Straße auf herrenlosem Feld -> `GET_PLAYER(NO_PLAYER).AI_changeMemoryCount` schrieb vor das Spieler-Array -> Heap kaputt, Absturz später an zufälliger Stelle (z. B. Siedler-KI). Jetzt nur bei fremdem Team, ohne Barbaren und MinorCivs.
- **Debug-DLL-Absturz nach Stadtwechsel** (`CvCity::doTurn`): `onCityDoTurn` kann die Stadt per `acquireCity` abgeben (Aufstand, Buergerkrieg, Tribut). Danach kein Zugriff mehr auf `this`.
- **Handelsschiff-Schleife** (`CvGameUtils.AI_unitUpdate`, Handelsroute aktiv): ohne Mission jetzt `finishMoves`.

**Neu**
- Taubenschlag: `iAIWeight` 200, `FLAVOR_GROWTH` 30, Empfehlung im Bau-Popup (`getRecommendedBuilding`).


## PAE KI-Review (Python) – Stand 7.18.3.2

Geprüft: Commit `6f6b903`. Fokus: Nutzt die KI die PAE-Mechaniken, die der Mensch per Knopf auslösen kann (`onModNetMessage` 665–775)?

### Ergebnis

Die Abdeckung ist breit, viele Mechaniken sind für die KI bewusst vereinfacht (z. B. Inquisitor wirkt ohne Anreise, Sklaven werten Latifundien kartenweit auf, Rang-Upgrades kostenlos).

**Schleifensicherheit:** In `CvSelectionGroupAI::AI_update` läuft die Schleife weiter, solange die Einheit `readyToMove()` ist. Alle Zweige in `AI_unitUpdate`, die `True` melden, verbrauchen die Züge (finishMoves, Mission, kill oder Upgrade). Einzige Ausnahme: K1.

#### Abgedeckt (Auswahl)
Inquisitor, Pferd auf-/absitzen, alle Sklaven-Zuweisungen (Schule, Bibliothek, Brot-/Manufaktur, Bordell, Theater, Palast, Tempel, Feuerwehr, Feld/Bergwerk, Latifundium), Gladiatoren/Gladiatorenschule, Auswanderer, Goldkarren, Trojanisches Pferd, Rang-Promotion/Prätorianer/Kastell, Edle Rüstung, Schiffe (Öl, Kompass, Reparatur, Mannschaft), Legende → General, Reservisten, Getreide abliefern, Söldner (anheuern/beauftragen), Handel/Handelsrouten, Kultivierung, Moral/Segnen, Druide, Kamel-/Pferdezucht, Prophet → Heilige Stadt, Piraten-Plünderung, Waldbrand, Eskorte, Turm (Jäger), Formationen, Fernangriff, Limes (über normale Bauaufträge).

### Fehler

**K1 – KI verkauft nie Sklaven** (`CvGameUtils.py` ~Z. 2124)
`MISSION_TRADE` scheitert in eigenen Städten immer (`CvUnit::canTrade`: `pCity->getTeam() == getTeam()` → false). Danach `return True` ohne verbrauchte Züge → DLL ruft `AI_update` für denselben Sklaven erneut auf, bis der Zufall den Zweig überspringt.
Fix: wie `PAE_Sklaven.doSell`, aber mit `kill`:
```python
												if bSlaveMarket:
														if CvUtil.myRandom(4, "ai_sell_slave") == 1:
																iGold = CvUtil.myRandom(31, "sell_slave") + 10
																pOwner.changeGold(iGold)
																gc.getPlayer(gc.getBARBARIAN_PLAYER()).changeGold(iGold)
																pUnit.kill(True, -1)
																return True
```

**K2 – Katapult-Umrüstung erzeugt OOS im Multiplayer** (`CvEventManager.py`, Aktion 775)
`gc.getGame().getActiveCivilizationType()` ist auf jedem Rechner ein anderes Volk → jeder Client erzeugt eine andere Einheit.
Fix: `gc.getCivilizationInfo(pPlayer.getCivilizationType())`.

**K3 – KI-Upgrades kostenlos** (`CvGameUtils.getUpgradePriceOverride`, ~Z. 3708)
`iPrice *= getAIUnitUpgradePercent() / 100` ist in Python 2 eine Ganzzahl-Division (80/100 = 0) → KI-Upgrades ab „Häuptling“ gratis, ab „Prinz“ zusätzlich über den Ära-Faktor. Fix: erst multiplizieren, dann teilen.

**Elefanten (Entscheidung 17.10.2026):** Elfenbein-Verbreitung bleibt bewusst abgeschaltet (historisch nicht verbreitet). Gezähmte Elefanten: Mensch kann Bau beschleunigen (iBaseHurry 40) oder per Upgrade zum Kriegs-/Arbeitselefanten machen (Stadt mit Elefantenstall). DLL-KI nutzt nur Beschleunigen/Arbeitselefant, nie Kriegselefant (UNITAI_ENGINEER) → eigener KI-Zweig.
**Neu (Aktion 776, 7.18.4, Entscheidung 17.10.2026):** Wilder Elefant → Arbeits- oder Kriegselefant nur in eigener Stadt mit `TECH_ELEFANTENZUCHT`, 50 Gold (gleicher Preis), kein Metall, kein Stall/Elfenbein. Arbeits- ↔ Kriegselefant überall, kostenlos, verbraucht den Zug. Knöpfe ausgegraut statt versteckt (Tooltip erklärt Bedingungen). Inline umgesetzt (CvMainInterface, CvEventManager 776, getWidgetHelp, AI_unitUpdate) mit `PAE_Unit.doUpgradeVeteran`. `UnitClassUpgrades` von `UNIT_ELEFANT` in der XML entfernen; `iCost` Arbeits-/Kriegselefant angleichen. KI: wild → Krieg (im Krieg) bzw. Arbeit (Frieden); Arbeits- → Kriegselefant im Krieg (1:4, eigenes Land); nie zurück.
✅ **Umgesetzt und geprüft in 7.18.3.5 (Commit `96e43fd`):** Python, Texte (`TXT_KEY_BUTTON_ELEFANT_TRAIN/_SWITCH`, `TXT_KEY_UNIT_ELEFANT_SWAP_HELP`), XML (`UnitClassUpgrades` von `UNIT_ELEFANT` leer, `iCost` Arbeits-/Kriegselefant beide 120). Alle Text-XMLs wohlgeformt, keine neuen doppelten Tags. Handler 776 prüft seit 7.19.1k auch den Ausgangstyp.

### Performance

**P1 – Latifundium-/Dorfsuche über die ganze Karte pro Sklave** (`CvGameUtils.py` ~Z. 2156)
Jeder Sklave außerhalb einer passenden Stadt scannt alle Kartenfelder – bei jedem `AI_update`-Aufruf, auch wenn kein Feld mehr aufwertbar ist. Vorschlag: Kandidatenfelder einmal pro Spieler und Runde sammeln (Cache in `self`).

### Nur für Menschen (keine KI-Logik)

| Aktion | Code | Einschätzung |
|---|---|---|
| Handelsposten errichten | 736 | relevant: Kultur/Gebietsanspruch |
| Statthalter ernennen | 757 | relevant: `doStatthalterTurn_AI` ist auskommentiert |
| Elefantenstall/-zucht | 721 | relevant für Elefanten-Völker: KI-Zweig auskommentiert |
| Heldendenkmal | 758 | gering |
| Duell mit Sklave (XP) | 761 | gering |
| Kamelwechsel | 766 | gering |
| Terraforming | 774 | mittel (Wüste/Tundra) |
| Feuerkatapult umrüsten | 775 | mittel im Belagerungskrieg |
| Pirat werden | 722 | vermutlich bewusst nur HI |
| Karte zeichnen | 728 | KI über Kartenhandel abgedeckt |

### Nicht geprüft
Strategische Entscheidungen der DLL-KI (Kriegsplanung, Armeegröße vs. Stack-Limit/Versorgung, Bauprioritäten). Das lässt sich nur am beobachteten Verhalten beurteilen.


---

## PAE OOS-Audit (Python) – Stand 7.18.3.2

Geprüft: Commit `6f6b903`, alle Python-Dateien außer WorldBuilder (läuft nur lokal). Die bereits behobenen Punkte Sklavenverkauf und Katapult (775) sind ausgeklammert.

### Geprüfte Fallen-Kategorien

| Kategorie | Ergebnis |
|---|---|
| Lokaler Zufall (`random`, Uhrzeit) in Spiellogik | sauber (`random` nur Anzeige im Historiker-Bildschirm) |
| Spiellogik abhängig von `getActivePlayer/Team/CivilizationType` | Katapult (behoben), toter Code (L1); im Nachtrag 7.18.3.5 zusätzlich **O8–O10** gefunden und behoben |
| Popup-Callbacks ändern Zustand ohne Netzwerknachricht | **O4** (Peloponnes-Szenario), sonst sauber |
| Lokale Events (Tastatur, Maus, Auswahl, onUpdate, onGameUpdate) | sauber (nur Cheat-Modus) |
| UI-Callbacks der DLL (`cannot*`, Kosten, `getWidgetHelp`, `updateColoredPlots`, Pfad-Callbacks) ziehen Zufall oder ändern Zustand | sauber (Aufrufgraph geprüft) |
| Bildschirme rufen zustandsändernde PAE-Funktionen auf | sauber (L2 harmlos) |
| Ereignis-Hilfetexte (`getHelp…`) ziehen Zufall | sauber (58 Funktionen) |
| `sendModNetMessage` aus synchronem Code | **O1** |
| Dict/Set mit Objekt-Schlüsseln (adressabhängige Reihenfolge) | sauber |
| Python-Zustand außerhalb des Spielstands steuert Spiellogik | **O2, O3, O5** |
| Speichern/Laden | sauber |

### OOS-Fehler

**Status:** O1, O2, O3, O5 sowie Sklavenverkauf und Katapult (775) umgesetzt und geprüft in 7.18.3.4 (Commit `bb464a1`). O4 bewusst nicht umgesetzt.

**O1 – Vasallen-Verhandlung 686 („nochmal entscheiden“ → Sieger)** ✅ `PAE_Vassal.py`, `onModNetMessage`, Zweig `iData1 == 686`, `else`
`CyMessageControl().sendModNetMessage(682, iData1, iData2, -1, 0)` wird von **jedem** Rechner gesendet (läuft in `onModNetMessage`), und die Argumente sind verschoben (`iData1` = 686 landet als Sieger in `do682` → `gc.getPlayer(686)` = None → Python-Fehler). Der Zweig funktioniert daher nie; nur Argumente zu korrigieren würde das Popup N-fach zeigen.
Fix:
```python
				else:
						do682(iData2, iData3, -1)
```

**O2 – Feldherren-Namen** ✅ `PAE_Unit.getGGName`, Modulliste `GG_UsedNames`
Liste lebt nur im Arbeitsspeicher (nach Laden leer, über geladene Spiele einer Sitzung hinweg gefüllt). Davon hängt ab, ob der Zweig mit `myRandom` erreicht wird → unterschiedliche Anzahl Zufallszahlen pro Rechner → OOS (Pitboss-Beitritt, oder MP nach vorherigem Spiel in derselben Sitzung). Außerdem wiederholen sich Namen nach dem Laden.
Fix: Liste im Spielstand halten (`CyGame`-ScriptData ist bisher ungenutzt; alle Namen sind ASCII):
```python
	lUsed = CvUtil.getScriptData(gc.getGame(), ["gg"], [])
	# … in beiden Schleifen: "iName not in lUsed" statt "not in GG_UsedNames"
	if GG_Name != "" and GG_Name not in lUsed:
		lUsed.append(GG_Name)
		CvUtil.addScriptData(gc.getGame(), "gg", lUsed)
```

**O3 – KI-Zwischenspeicher über Runden hinweg** ✅ `CvGameUtils.py`
- `doSpreadStrategicBonus_AI` (Kamel/Pferd/Esel): `PAE_AI_ID`/`PAE_AI_ID2` werden nie zurückgesetzt. Server und frisch beigetretener Client entscheiden unterschiedlich, ob gescannt bzw. kultiviert wird (inkl. `myRandom`).
- `AI_unitUpdate`: `PAE_AI_Slaves_Owner` (aus A3) bleibt bei nur einem KI-Spieler mit Sklaven über die Runde bestehen.
Fix: Schlüssel mit Runde, Ziel der Einheit im Spielstand der Einheit:
```python
						tKey = (iOwner, gc.getGame().getGameTurn())
						if self.PAE_AI_Slaves_Owner != tKey:
								self.PAE_AI_Slaves_Owner = tKey
```
```python
						# kultivieren, wenn die Einheit ihr Ziel erreicht hat
						if CvUtil.getScriptData(pUnit, ["aiC"], 0):
								CvUtil.removeScriptData(pUnit, "aiC")
								if PAE_Cultivation._isBonusCultivationChance(iOwner, pUnit.plot(), eBonus, False, None):
										PAE_Cultivation.doCultivateBonus(pUnit.plot(), pUnit, eBonus, False)
										pUnit.kill(True, -1)
										return True

						tKey = (iOwner, gc.getGame().getGameTurn())
						if self.PAE_AI_ID != tKey:
								self.PAE_AI_ID = tKey
								# … beim pushMoveToMission zusätzlich:
								#     CvUtil.addScriptData(pUnit, "aiC", 1)
```
`PAE_AI_ID2` entfällt.

**O4 – Szenario „Peloponnesischer Krieg (Keinpferd)“** `CvScreensInterface.py`
7 Popup-Callbacks (`…_Poteidaia1–3`, `…_Megara1–2`, `…_Plataiai1`, `…_Syra1`) ändern Gold, Krieg, Kultur, Einheiten direkt und ziehen `myRandom` – nur auf dem klickenden Rechner. Nur relevant, wenn das Szenario im MP gespielt wird; dann Logik nach `onModNetMessage` verlegen.
**Entscheidung (17.10.2026):** wird nicht umgesetzt – Szenario wird nicht im MP gespielt.

**O5 – Handels-Spezialbonus-Zähler** ✅ `PAE_Trade.init`
`iCitiesSpecialBonus` wird nicht auf 0 gesetzt, und `bInitialized` verhindert jede Neuberechnung nach dem ersten geladenen Spiel einer Sitzung. Ein Rechner, auf dem vorher ein anderes Spiel lief, rechnet mit falschem Zähler → `addCityWithSpecialBonus` verhält sich anders → OOS.
Fix: `bInitialized` entfernen, Zähler bei jedem `init()` auf 0 setzen.

**O6 – Fernangriffskosten** `CvEventManager.py` ~Z. 4216: `DFern = L.DFernangriffCosts` ohne Kopie, danach Schreibzugriff → globales Dict dauerhaft verändert (Gold, sitzungsabhängig). Fix: `DFern = dict(L.DFernangriffCosts)`.

**O7 – Veteranen-Upgrade** `PAE_Unit.py` Z. 816: `forbiddenPromos = L.LVeteranForbiddenPromos` ohne Kopie, danach `.extend()` → globale Liste wächst mit jedem Upgrade, Beförderungen gehen dauerhaft verloren (sitzungsabhängig). Fix: `forbiddenPromos = list(L.LVeteranForbiddenPromos)`.

### Nachtrag 7.18.3.5 (Prüfung in Claude Code) – umgesetzt in 7.18.3.6

Jetzt sind alle `if`-Blöcke mit `getActivePlayer`/`getActiveTeam` per Skript auf Zufall und Zustandsänderungen geprüft, ebenso alle Aufrufe von `gc.getPlayer(getActivePlayer())`.

**O8 – `myRandom` nur beim aktiven Spieler** ✅ `PAE_City.py` Z. 2458, 2481 (Provinztribut), `PAE_Unit.py` Z. 3502 (Usurpator)
Der synchronisierte Zufall lief nur auf einem Rechner weiter → OOS beim nächsten Wurf.
Fix: `gc.getASyncRand().get(n, "...")` (nur Textauswahl).

**O9 – Usurpator-Chance hing am Namen des lokalen Spielers** ✅ `PAE_Unit.py` Z. 3256
`"Apocalypto"` → Chance 2 statt 4 nur auf diesem Rechner → OOS.
Fix: an die Spieloption `GAMEOPTION_PAE_SETH` gekoppelt (Spieloptionen sind auf allen Rechnern gleich).

**O10 – Pitboss-Host: `gc.getPlayer(getActivePlayer())` = None** ✅ `PAE_Disasters.py` Z. 665, 746, 953, 1399, `PAE_Trade.py` Z. 1838, 1901
Python-Fehler nur auf dem Server, der Rest der Funktion (Erdbeben-/Tsunami-Schäden, Handelsaufträge) fehlte dort → OOS.
Fix: `gc.getGame().getActivePlayer() != -1` bzw. `iActivePlayer != -1 and …`.

**O11 – `iCitiesSpecialBonus` driftete** ✅ `CvEventManager.py` nach Z. 2756
Wurde eine Stadt mit Auftrag zerstört, sank der Zähler nicht. Ein Rechner, der neu verbindet, zählte beim Laden richtig, die anderen nicht → OOS.
Fix: `PAE_Trade.init()` jede Runde im Seidenstraßen-Block.

**Nebenbei behoben (7.18.3.6–7.18.3.8):**
- `CvMainInterface.py` Z. 4432, 7319: letzte C3-Schleifen (`getCity(i)`) → `CvUtil.getCities()` (nur Anzeige).
- `PAE_Trade.py` Z. 1944: `UNIT_CAMEL_ARCHER` gab es nicht → `UNIT_ARABIA_CAMELARCHER`.
- `CvWBKeys.py`: Tippfehler `BELGER_ADJECTIV` korrigiert, Duplikat entfernt.
- O4 bleibt offen (nur Einzelspieler). Das Plataiai-Popup (`PeloponnesianWarKeinpferd.py` Z. 135–139) hat aber eigene Texte `TXT_KEY_EVENT_PLATAIAI_THEBEN_DESC/_OPTION_1–3` in `SC_PeloWarKeinpferd.xml` bekommen (7.18.3.7).
- Gedankenstriche und andere Zeichen außerhalb von Latin-1 aus den Text-XMLs entfernt (7.18.3.8/9).


### Schlafende Fallen / Kleinigkeiten

- **L1** `PAE_Trade.doAutomateMerchant`: Zweig `elif iDistance2 == -1` (mit `getActivePlayer()` und `not pushMission(...)`) ist toter Code (Distanzen sind nie -1). `pushMission` liefert `None`, die Bedingung wäre immer wahr. Aufräumen. ✅ (behoben in 7.18.3.10)
- **L2** `PAE_Unit.getSupply` schreibt ScriptData, auch wenn die Oberfläche liest. Deterministisch, aber Lese-Funktionen sollten nicht schreiben. war auch eine kleine OOS-Falle, weil die Oberfläche getSupply aufruft ✅ (behoben in 7.18.3.10)
- **L3** `WegDerGoten.py` Z. 331, 467, 1584: `getUnit(i)` mit Index statt ID (wie C3 bei Städten) → Einheiten werden übersehen. Kein OOS, aber Logikfehler. ✅ (behoben in 7.18.3.10)


---

## PAE Performance-Audit (Python) – Stand Patch 7.18.3

Geprüft: Repository `dead-flunky/PieAncientEuropeVII`, Commit `3ff0199` (11.10.2026).
Fokus: Rundenzeiten, also alles, was pro Runde, pro Stadt, pro Einheit oder pro Feldschritt läuft.
Zeilenangaben beziehen sich auf diesen Commit.

### Prioritäten auf einen Blick

| # | Fundstelle | Häufigkeit | Hebel | Risiko der Änderung |
|---|---|---|---|---|
| A1 | `CvUtil.getScriptData` – leere Daten lösen JSON-Parse + 3 Exceptions aus | 223 Aufrufstellen, teils pro Feld/Einheit | **sehr hoch** | sehr gering |
| A2 | `PAE_Turn_Features.doFogOfWar` – ganze Karte, jede Runde für jeden Menschen | pro Spielerrunde × alle Felder | **hoch** | gering |
| A3 | `CvGameUtils.AI_unitUpdate` – baut bei jedem Aufruf die komplette Städteliste | pro KI-Einheitengruppe, mehrmals je Runde | **hoch** | gering |
| A4 | `cannotConstruct` / `cannotTrain` / Cost-Mods – String-Lookups bei jedem Aufruf | pro Stadt × Gebäude/Einheit, bei jeder KI-Bauentscheidung | **hoch** | gering |
| B1 | `onUnitMove` – bis zu 5 String-Lookups pro Schritt | pro Feldschritt jeder Einheit | mittel | sehr gering |
| B2 | `PAE_Unit.stackDoTurn` – quadratische Teile | pro Spielerrunde × alle Einheiten | mittel | gering |
| B3 | Szenarioname wird ständig neu aus Plot (0,0) geparst | mehrfach pro Spielerrunde, pro Civic-Prüfung | gering–mittel | sehr gering |

Dazu kommen **6 echte Bugs**, die mir dabei aufgefallen sind (Abschnitt C).

**Status (17.10.2026):** Alle Punkte A1–A4, B1–B3 und C1–C6 umgesetzt (C6: Auswahl jetzt aus den ersten 5 Techs, kommentiert). Gemessen: 40 s → 29 s pro Runde auf „Weg der Goten“. Review von 7.18.3.1 in Abschnitt E.

---

### A. Große Hebel

#### A1 – `getScriptData`: Schnellpfad für leere Daten (CvUtil.py:645) ✅

`decode_script_data` ruft das reine Python-`simplejson` (regex-basiert, ohne C-Speedups) auf. Bei leeren Daten – also bei den allermeisten Feldern und vielen Einheiten – passiert Folgendes:

1. `"".replace("\\", "")`
2. `simplejson.loads("")` → wirft `ValueError` → wird abgefangen → `{}`
3. Für jeden Schlüssel in `keylist` (meist 2, z. B. `["H", "t"]`) → `KeyError` → abgefangen

Das sind **drei Exceptions pro Aufruf**, bei dem nichts zu holen ist. Das trifft u. a. `doFogOfWar` (jedes unsichtbare Feld), `stackDoTurn` (jede Einheit), `onUnitMove` (Handelskarren), `doPlotFeatures` (Forts), `cannotDoCivic` und mehrere Stellen in jeder Spielerrunde.

**Fix (verhaltensgleich):** ✅ umgesetzt

```python
def getScriptData(pOwner, keylist=None, default=""):
		sData = pOwner.getScriptData()
		# Schnellpfad: leere ScriptData -> kein JSON-Parse, keine Exceptions
		if not sData:
				if keylist is None:
						return {}
				return default
		if keylist is None:
				return decode_script_data(sData)
		data = decode_script_data(sData)
		for k in keylist:
				if k in data:          # statt try/except KeyError
						return data[k]
		return default
```

`addScriptData`/`removeScriptData` rufen `getScriptData(pOwner, None, {})` auf und bekommen weiterhin ein neues leeres Dict. Die Semantik bleibt identisch.

#### A2 – `doFogOfWar` (PAE_Turn_Features.py:780) ✅

Für **menschliche Spieler jede Runde** über die ganze Karte. Die teuren Prüfungen (ScriptData-Parse, Zufallszahl, Stadtprüfung) kommen **vor** der billigen Frage, ob das Feld überhaupt aufgedeckt ist. Unaufgedeckte Felder durchlaufen also alles für nichts. Außerdem wird `CyMap()` pro Feld neu erzeugt.

**Fix: billigste Ausschlüsse zuerst** ✅ umgesetzt

```python
		if not bDontGoBlackAnymore:
				pMap = CyMap()
				for iI in range(pMap.numPlots()):
						pPlot = pMap.plotByIndex(iI)
						# 1. Nicht aufgedeckt oder sichtbar -> nichts zu tun
						if not pPlot.isRevealed(iTeam, 0) or pPlot.isVisible(iTeam, 0):
								continue
						# 2. Kartenwissen (reine Plot-Abfragen)
						if bShowCoasts:
								if bShowOcean and pPlot.isWater():
										continue
								if pPlot.isCoastalLand() or pPlot.isAdjacentToLand() and pPlot.isWater():
										continue
						if bShowPeaksAndRivers:
								if pPlot.isRiverSide() or pPlot.isPeak():
										continue
						# 3. 50 % Chance
						if CvUtil.myRandom(2, "bGoBlack") == 0:
								continue
						# 4. Hauptstädte / Weltwunder-Städte bleiben sichtbar
						if pPlot.isCity():
								pCity = pPlot.getPlotCity()
								if pCity.isCapital() or pCity.getNumWorldWonders() > 0:
										continue
						# 5. Heiliger Berg (ScriptData) ganz zuletzt
						if CvUtil.getScriptData(pPlot, ["H", "t"]) == "X":
								continue
						pPlot.setRevealed(iTeam, 0, 0, -1)
```

Ergebnis und Wahrscheinlichkeiten bleiben gleich. Es werden nur weniger Zufallszahlen gezogen. Das ist MP-sicher (alle Clients rechnen identisch), ändert aber die Zufallsfolge gegenüber alten Spielständen. Das ist unkritisch, sollte aber bekannt sein.

#### A3 – `AI_unitUpdate` (CvGameUtils.py:1617)

Die DLL ruft diese Funktion **ungefiltert für jede KI-Einheitengruppe** auf (CvUnitAI.cpp:86), auch für Barbaren, Tiere und Treibgut, und oft mehrfach pro Runde.

- **Z. 1628:** `lCities = PyPlayer(iOwner).getCityList()` erzeugt bei *jedem* Aufruf für *jede* Stadt ein `PyCity`-Objekt (je 2 DLL-Aufrufe). Gebraucht wird die Liste nur in zwei Sklaven-Zweigen (Z. ~2028 und ~2248).
  **Fix:** `lCities = None` setzen und erst dort laden, wo sie gebraucht wird (`if lCities is None: lCities = PyPlayer(iOwner).getCityList()`). ✅ umgesetzt
- **Z. 1631–1634:** Der „Instanz-Cache für bessere Rundenzeit“ ist wirkungslos, weil `self.PAE_AI_ID = iOwner` auskommentiert ist. Gleichzeitig **setzt `doSpreadStrategicBonus_AI` (Z. 3751) dieselbe Variable**. Dadurch werden die Sklaven-Caches mal zurückgesetzt und mal nicht, je nachdem, ob vorher ein Stall-Bauer aktiv war. Empfehlung: eigene Variable verwenden (z. B. `self.PAE_AI_SlaveCacheOwner`) und bewusst entscheiden, ob gecacht wird. ✅ umgesetzt
- **129 `getInfoTypeForString`-Aufrufe** im Funktionskörper. Eine gewöhnliche Militäreinheit durchläuft die `if/elif`-Kette und löst dabei Dutzende davon aus, bevor sie bei `return False` ankommt. Siehe A4 für die Lösung.

#### A4 – Konstanten statt String-Lookups in den heißen Callbacks ✅

Aktive Callbacks laut `PythonCallbackDefines.xml`: `cannotTrain`, `cannotConstruct`, `cannotResearch`, `cannotDoCivic`, `getUnitCostMod`, `getBuildingCostMod`. Die DLL ruft sie bei jeder Bau-, Forschungs- und Civic-Bewertung der KI sowie bei jedem Neuzeichnen der Bauliste auf, also pro Stadt × 376 Gebäude bzw. 346 Einheiten.

`cannotConstruct` (Z. 936) löst für ein **beliebiges, nicht betroffenes Gebäude rund 26 `getInfoTypeForString`-Aufrufe** aus: 3 für die Stall-Liste, 12 für die `elif`-Kette, 8 + 3 für die Bonus-Listen. Jeder Aufruf geht über die Python/C++-Grenze und macht einen String-Hash-Lookup. Dazu werden bei jedem Aufruf 3 Listen neu gebaut.

**Fix:** Die IDs einmalig in `PAE_Lists.init()` berechnen. Das ist wichtig, weil `init()` erst nach dem Laden der XML aufgerufen wird (CvEventManager Z. 2363/2460). Auf Modulebene beim Import wären die Werte noch `-1`.

```python
# PAE_Lists.py, in init():
global dCannotConstruct, LStableBuildings, LBonusBuildingsCity, LBonusBuildings3x3
LStableBuildings = [gc.getInfoTypeForString(s) for s in
		("BUILDING_STABLE", "BUILDING_CAMEL_STABLE", "BUILDING_ELEPHANT_STABLE")]
LBonusBuildingsCity = [gc.getInfoTypeForString(s) for s in
		("BUILDING_WINERY", "BUILDING_PAPYRUSPOST", "BUILDING_MUREX", "BUILDING_WINDOFEN_NATIONAL",
		 "BUILDING_GUSS_BLEI", "BUILDING_GUSS_COPPER", "BUILDING_GUSS_ZINN", "BUILDING_GUSS_ZINK")]
# ... analog für 3x3 und die Einzel-IDs (Akropolis, Palast, Kaserne, ...)
```

In `cannotConstruct` kann dann als erstes ein Mengen-Test stehen: `if eBuilding not in L.SSpecialBuildings: return False`. Das ist **ein einziger Python-Vergleich** für die rund 350 Gebäude ohne Sonderregel. Dasselbe gilt für `cannotTrain` (`UNIT_EMIGRANT`, `UNIT_SETTLER`, `TECH_CITY_STATE`), `getUnitCostMod` (`TRAIT_AGGRESSIVE`), `getBuildingCostMod` (`TRAIT_INDUSTRIOUS`) und `cannotResearch`.

✅ umgesetzt über `PAE_Lists.initConstants()` (aufgerufen am Ende von `init()`, IDs als `L.<XML-Tag>`) plus Frühausstieg mit `L.SSpecialBuildings` in `cannotConstruct` und `L.SSpecialUnits` in `cannotTrain`.

---

### B. Mittlere Hebel

#### B1 – `onUnitMove` (CvEventManager.py:4256) ✅
Läuft bei **jedem Feldschritt jeder Einheit**. Pro Schritt: `PROMOTION_FORM_FLIGHT`, außerhalb von Städten zusätzlich `IMPROVEMENT_CAVE`, `IMPROVEMENT_BARBARENFORT`, `PROMOTION_LEADER`, in Städten `BUILDING_CIVIL_WAR`. Diese IDs sollten einmal in `L.init()` berechnet werden.
Kleinigkeit: `pPlot.getImprovementType()` wird zweimal hintereinander abgefragt (Z. 4442/4447). Einmal in eine Variable lesen genügt.

#### B2 – `PAE_Unit.stackDoTurn` (PAE_Unit.py:217) ✅
Pro Spielerrunde über alle Einheiten:
- Pro Einheit `getScriptData(sUnit, ["ifp"])`. Mit A1 wird das bei leeren Daten fast gratis.
- `tmpPlot.getNumDefenders(iPlayer)` wird **pro Einheit** statt pro Feld berechnet. Bei einem 40er-Stapel sind das 40 × 40 Einheiten-Iterationen in der DLL. **Fix:** ein Dict `dPlotChecked[(x, y)] = True` und jedes Feld nur einmal auswerten.
- `tmpA not in PlotArraySupply` / `lHealerPlots` / `lFormationPlots` sind lineare Suchen in Listen. **Fix:** Tupel `(x, y)` als Dict-Schlüssel verwenden. Python 2.4 kennt `set()` bereits, ein Dict funktioniert genauso.

#### B3 – Szenarioname cachen ✅
`CvUtil.getScriptData(CyMap().plot(0, 0), ["S", "t"])` wird in `onBeginPlayerTurn`, `onEndPlayerTurn`, `onEndGameTurn` und in **jedem** `cannotDoCivic`-Aufruf neu geparst. In normalen Spielen ist das mit A1 billig. In Szenarien parst es jedes Mal echtes JSON.
**Fix:** einmal in `onLoadGame`/`onGameStart` in eine Modulvariable lesen (z. B. `PAE_Lists.sScenarioName`).

#### B4 – Was ich mir angesehen habe und für **in Ordnung** halte
- `doPlotFeatures`: Lookups stehen vor der Schleife und die Prüfreihenfolge ist sinnvoll. Das ist das Vorbild für den Rest.
- Fog of War für KI nur alle 20 Runden und versetzt pro Spieler: gute Idee.
- `doSpreadReligion`, `doRevoltAnarchy`, `doStrandgut`: einmal pro Runde, Kosten vertretbar.
- Der KI-Fernangriff steht noch in Python (`onEndPlayerTurn`). Die C++-Version in `CvPlayerAI::AI_doTurnUnitsPre` ist auskommentiert, es wird also nichts doppelt ausgeführt. Langfristig wäre sie in C++ schneller und für die KI auch zum besseren Zeitpunkt (vor statt nach den Zügen). Das gehört aber eher zum KI-Thema.

---

### C. Bugs, die mir nebenbei aufgefallen sind

#### C1 – Nationaler Windofen wird nie auf Ressourcen geprüft ✅
`CvGameUtils.py:1098` und `PAE_City.py:2779`: In den Gebäudelisten steht `BUILDINGCLASS_WINDOFEN_NATIONAL` statt `BUILDING_WINDOFEN_NATIONAL`. Verglichen wird mit einer **Gebäude**-ID. Die Klassen-ID ist 24, und Gebäude Nr. 24 ist `BUILDING_WARFT`. Die Folge:
- Der Nationale Windofen (braucht Kupfer, Silber oder Gold im Stadtradius) wird **nie** geprüft, weder beim Bauen noch beim Abriss.
- Stattdessen wird die Warft geprüft, die keine Ressource braucht. Das läuft folgenlos ins Leere.

**Fix:** an beiden Stellen `BUILDINGCLASS_WINDOFEN_NATIONAL` → `BUILDING_WINDOFEN_NATIONAL`.
⚠️ Danach greift die Regel tatsächlich: Bestehende Windöfen ohne passende Ressource im Radius können abgerissen werden.

#### C2 – Python-Fehler beim Abriss der Bronzeschmiede bricht den Stadt-Rundenablauf ab ✅
`PAE_City.py:2671` in `removeNoBonusNoBuilding`: Fehlen bei der Bronzeschmiede die Oder-Güter (Kohle/Zinn), liefert `bonusMissing()` den Wert `-2`. Der Text wird richtig auf `..._NOBONUSNOBUILDING_4` gesetzt, danach wird aber trotzdem `gc.getBonusInfo(-2).getDescription()` aufgerufen. Das ist `None.getDescription()` und erzeugt einen Python-Fehler.
Das Gebäude ist zu diesem Zeitpunkt schon abgerissen, aber **der Rest von `onCityDoTurn` für diese Stadt fällt aus** (Pest, Lepra, Sklaven, Revolten, Tribut …). Betrifft nur den aktiven menschlichen Spieler. Die Stellen in Z. 2751 und 2806 behandeln `-2` bereits korrekt.
**Fix:** wie dort `"", ` statt `gc.getBonusInfo(bonus).getDescription()` übergeben, wenn `bonus == -2`. ✅ umgesetzt

#### C3 – Städte-Schleifen per Index übersehen Städte ✅
Rund 14 aktive Stellen nutzen `for j in range(pPlayer.getNumCities()): pPlayer.getCity(j)`, z. B. `PAE_Christen.doSpreadReligion` (Z. 144), `PAE_City.py` 1187/4599/4870/4886, `PAE_Trade.py` 556, `PAE_Mercenaries.py` 657, `PAE_Turn_Features.py` 1000/1157 `PAE_Vassal.py` 1058, `CvScreensInterface.py` 2251 und `CvEventManager.py` 1587/5393.
`getCity()` erwartet eine City-**ID**. Ein Slot-Index funktioniert zwar dank einer Sonderregel in `FFreeListTrashArray::getAt`. Sobald aber eine Stadt erobert oder zerstört wurde, entstehen Lücken in den Slots, und die Städte in den hohen Slots werden **nie** erreicht. Im Spätspiel trifft das gerade die eroberten Städte.
**Fix:** `(loopCity, pIter) = pPlayer.firstCity(False)` / `nextCity(pIter, False)`, wie an den meisten anderen Stellen bereits üblich.

#### C4 – Seevolk-Einheit wird getötet und danach weiter benutzt ✅
`CvGameUtils.py:1711`: `if not pUnit.hasCargo(): pUnit.kill(True, -1)` steht ohne `return True`. Die Funktion läuft mit der toten Einheit weiter in den Barbaren-Block (`pUnit.getUnitAIType()` usw.) und liefert dann `False`. Damit setzt die DLL `AI_update` an einer Einheit fort, die zum Löschen markiert ist. Das ist ein potenzieller Absturz- oder OOS-Kandidat.
**Fix:** `return True` direkt nach `kill`. ✅ umgesetzt

#### C5 – Debug-Ausgabe stürzt nach Stadtrevolte ab ✅
`CvEventManager.py:5788`: Mit `bPAETimeCheck = True` greift `pCity.getName()` auf `pCity = None` zu (Z. 5755, Judenaufstand). Das betrifft nur den Debug-Modus, verfälscht dann aber genau die Messung.

#### C6 – „Forschungsbug“-Workaround wählt nicht die billigste Tech ✅
`CvEventManager.py:2866–2875`: Die Schleife bricht nach 3 gefundenen Techs ab (`if len(techs) > 2: break`) und sortiert erst danach. Gewählt wird also die billigste der **ersten drei nach XML-Reihenfolge**, nicht die billigste insgesamt. Falls das Absicht ist (Tempo), sollte der Kommentar das sagen.

---

### D. Messen vorher/nachher

Die vorhandene Infrastruktur reicht dafür aus:
1. `CvEventManager.py:152`: `bPAETimeCheck = True`, in der `Civilization.ini` `LoggingEnable=1` → `PythonDbg.log`.
2. Einen festen Spielstand (spätes Spiel, viele KI-Einheiten) mit `AIAutoPlay` 5–10 Runden laufen lassen, vorher und nachher.
3. `bPAEDebugMark1..10` eignen sich, um einzelne Hooks gezielt abzuschalten und deren Anteil zu bestimmen.

Die Callbacks `cannotConstruct`, `cannotTrain` und `AI_unitUpdate` erfasst `bPAETimeCheck` nicht. Für die wäre ein kleiner Zähl-Decorator sinnvoll (Aufrufe + Gesamtzeit pro Runde ins Log), damit man ihren Anteil sieht.

#### Ergebnis (17.10.2026)
- Karte „Weg der Goten“ (groß): ca. **40 s → 29 s pro Runde** (≈ −28 %)
- Kleinere, fortgeschrittene Karten: ca. 20 s pro Runde (Vergleichswert vorher nicht erfasst)
- Die Änderungen wurden direkt in Patch 7.18.3 übernommen.

### Vorschlag zur Reihenfolge
1. **A1** (5 Zeilen, risikolos, wirkt überall) + **C1, C2, C4** (je 1–2 Zeilen)
2. **A4 + B1** (Konstanten in `PAE_Lists.init()`)
3. **A2, A3, B2, B3**
4. **C3** (14 Stellen, mechanisch)

---

### E. Review 7.18.3.1 (Commit `c8bfa5c`)

**Geprüft:** alle 14 geänderten Python-Dateien gegen 7.18.3 (`3ff0199`). DLL- und XML-Änderungen waren nicht Teil des Audits.

**Ergebnis Audit-Punkte:** A1–A4, B1–B3, C1–C6 korrekt umgesetzt. Keine Tokenizer- oder Einrückungsfehler, alle `L.XYZ`-Verweise vorhanden.

**Offene Hinweise:**
1. **Fehlende Text-Keys:** `TXT_KEY_MESSAGE_CITY_GROWTH_FIRE1`, `..._FIRE2`, `..._NO_UNITS` (neu in `onCityGrowth`) fehlen im Repo → im Spiel erscheint der rohe Key.
2. **Stadtbrand-Balance** (`canTriggerCityFire` und `PAE_City.doStadtbrand`): Durch die neue Basis `iChance = 5` hat eine Stadt *ohne* Brunnen/Zisterne 50 % Schutz – mehr als eine Stadt *mit* Brunnen ab Pop 4 oder mit Zisterne ab Pop 7. Vorschlag: Basis wieder 0, Zisterne `iChance = 11 - iCityPop`, Brunnen `iChance = 8 - iCityPop` (gleiche Werte für die Gebäude, ohne Gebäude kein Schutz wie in 7.18.3).
3. **Klein:** `cannotConstruct`/Palisade baut die Waldliste weiter bei jedem Aufruf – `L.LPalisadeFeatures` existiert dafür. `canTriggerCityFire` liest `getPopulation()` vor der `isNone()`-Prüfung. `setHolyCity` prüft `isNone()` doppelt.
4. **Bitte bestätigen (Spielmechanik):** KI bekommt jetzt auf *allen* Schwierigkeitsgraden zu 50 % einen zweiten Siedler; globale Katastrophen hängen an `gc.getPlayer(0).getCurrentEra()` – `gc.getGame().getCurrentEra()` wäre unabhängig davon, ob Spieler 0 noch lebt.

**Nachprüfung 7.18.3.2 (Commit `6f6b903`):** Punkte 2, 3 (Palisade, isNone-Reihenfolge) und 4.2 korrekt umgesetzt, Einrückungen geprüft. Punkt 1 (Text-Keys in `PAEGameText_Misc.xml`) und 4.1 (KI-Siedler, 7.19.1i) inzwischen erledigt.

## Patch 7.18.3.18 (Claude Code)
- KI-Schleifen: `CvSelectionGroupAI::AI_update` beendet den Zug bei Stillstand (3x gleiches Feld/gleiche Bewegungspunkte) oder Hin-und-her (A->B->A), statt bis zum Limit 40-120.
- KI-Stadtangriff: `CvUnitAI::AI_targetCity` - steht der Stapel schon neben der Zielstadt, greift er ab 80 % an oder wartet, statt zurueckzuweichen.
- Handelsschiffe: nur Routen zwischen Kuestenstaedten (`PAE_Trade.doAssignTradeRoute_AI`, `_getBestCity4Trade`). Route mit Inlandsstadt oder 3 Runden ohne Bewegung (`autS`) wird in `doAutomateMerchant` geloescht.

## Patch 7.19.1 (Claude Code)
- DLL, Furt (`TERRAIN_RIVER_FORD`, ab 7.19.1): Wasser-Plot (`bWater=1`, wird auf Flusshöhe gezeichnet), zählt für Gebiete aber als Land (`areaValid`, `CvMap::calculateAreas`, `CvPlot::setPlotType`, `setTerrainType` → `recalculateAreas`). Landeinheiten dürfen darauf (`isValidDomainForAction`, `CvUnitAI::AI_update`). Kampf von der Furt aufs Ufer bewusst nach BTS-Regeln wie vom Wasser aus (Amphibien-Abzug, keine Belagerungswaffen, kein Rückzug). Neue `isWater()`-Abfragen für Landeinheiten immer auf die Furt prüfen.

## Patch 7.19.1d
Erledigt (10/2026): PAE-Stellen aller wichtigen cpp-Dateien und CvGameTextMgr.cpp (Anzeige/Hilfetexte, OOS-sauber).

## Patch 7.19.1e–g (Claude Code)
- Abwehrschuss (eigene Spieloption `GAMEOPTION_NO_DEFENSIVE_STRIKE` ab 7.19.1h, mit PAE- und BTS-Kampf): Vor einem Nahkampfangriff einer Landeinheit schiesst
- Ablauf: `CvUnit::attack` -> `doDefensiveRangedStrike` -> bei sichtbarem Kampf Pause ueber den Kampf-Timer (8 Takte), Schuss-Animation in Takt 6 (4 Takte, in `updateCombat`), danach Nahkampf. Schuetze wird waehrend der Pause angezeigt (`CvPlot::setPAEShowUnit`, reine Anzeige). Zahlen fest im Code.
- Kampfchance (`getCombatOdds` mit `iAttackerExtraDamage`), Kampfvorschau und KI (`CvUnitAI::AI_attackOdds`) rechnen den Abwehrschuss mit ein.
- KI mit PAE-Kampfrunden (`AI_attackOdds`): ab 80 % Kampfchance immer Angriff; einzige starke Einheit im Stapel verteidigt lieber; ueberlebt sie die Kampfrunden sicher und steht im Stapel, greift sie immer an.
- Brachland: unbewirtschaftete Modernisierung im Stadtradius verfaellt (1:20 pro Runde, erst nach 10 Runden), Bedingungen in `CvPlot::isFallowDecayPossible`, Hinweis in der Feld-Info.

## Erledigt
Performance-Audit bei einem Test im Szenario: WegDerGoten (Huge Map): (anfangs 1min 25s -> 1min 05s -> aktuell 42s (ab 2. Runde sogar nur 32s)), KI-Review K1–K3, OOS-Audit O1–O3, O5–O11 (O4 bewusst nicht), Elefanten-System Aktion 776 (Details in PAE_KI_Review_7.18.3.2.md), Plataiai-Popup-Texte (7.18.3.7), Sonderzeichen in Text-XMLs bereinigt (7.18.3.8/9), L1–L3 (7.18.3.10), Sichtfehler Turm/Fort (7.18.3.11), Bugfix-Paket 7.18.3.12–14 (siehe Abschnitt „Patch 7.18.3.10–14“).
CtD Straßenbau, Handelsschiff-Schleife, Taubenschlag (7.18.3.15–17)
7.18.3.19–7.19b: getCulture(-1)-Fix (Handelsposten, checkLateEra), getCities-Nachbesserungen (PAE_City Revolte, PAE_Vassal), Weg der Goten durchgesehen (onChangeWar war durch __LOG_WARPEACE blockiert, ScriptData-Abfragen, 15.2-Logik, 27.2 jede Runde), Event-OOS (Hurrikan/Zyklon/Monsun/Stadtbrand jetzt Wahl Trümmer oder Wiederaufbau für Gold, ohne Zufall), fehlende Event-Funktionen ersetzt (Ketzerei 2, Thorgal-Hilfe, Plünderer 3) bzw. durch XML gelöst, Bordell 1:4, tote Funktionen entfernt.
Erledigt (7.19.1i–j): Statthalter (757), Handelsposten (736, KI baut auch Händler dafür), Feuerkatapult (775, eigener kleiner Raze-Wert, Torsion 3), changeUnit nur Katapulte, Zweiter Siedler (Limit über cannotTrain, KI ab Kaiser 50 %).
Erledigt (7.19.1k–l): Terraforming (774, `PAE_Unit.doTerraforming` für Mensch und KI, ohne Schwemmland/Oase, KI nur in Wüsten-/Tundrastadt ab 3 Feldern), Handler 776 prüft Ausgangs- und Zieltyp, Heldendenkmal (758, nur echte Gebäude per `getNumRealBuilding`, sonst Verdopplung freier Denkmäler; keine KI), Duell (761, nur mit Sklave auf dem Feld; keine KI), Pferde-/Kamelwechsel (766, `setMoves(0)` statt `finishMoves`, danach `setMadeAttack(True)`: einmal pro Runde, kein Angriff mehr; keine KI).
Erledigt (7.19.1l–n): onModNetMessage-Prüfung 665–776 (Sender, Popup-Callbacks, Handler, aufgerufene Funktionen). OOS: Statthalter Gebäude verkaufen (770, Verkauf lief nur beim aktiven Spieler), Usurpator-Check (`doUsurpatorCheck`, andere Rechner liefen in den KI-Zweig). Fehler: Kompass (767, Kosten = X-Koordinate), Pirat versklaven (726, `iData5` statt `iData4`; Dorf ohne Besitzer -> Python-Fehler nur auf fremden Rechnern), Söldner anheuern (708, Typ-Buttons verrutscht bei fehlenden Typen), `doUsurpatorGeneral` (`pCity` undefiniert, Index-Schleife über wegspringende Einheiten), Inquisition (665/704, Buttons verrutscht bei Missionars-Religion; in Vasallenstädten jetzt Besitzer der Einheit), Gebäude verkaufen nur echte Gebäude (`getNumRealBuilding`). Kleinigkeiten: Trojanisches Pferd nur eine Stadt (stärkste Verteidigung), Dezimierung-Meldung nennt verlorene Moral, Stehlen (739) kostet Spionage nur bei Erfolg, Folter-Chancen wie im Text (50/25/10 %), Töne nicht auf allen Rechnern, `is not None` bei DLL-Städten durch `isNone()` ersetzt. 771 (Lager/Turm) ist toter Code, alle Buttons auskommentiert.