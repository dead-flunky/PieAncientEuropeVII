# Scenario Weg der Goten by brettschmitt
# Spieler-IDs:
# Goten (Spieler): 0
# Germanen: [1,2,3,4]
# GerVandalen: [0,1,2,3,4,9]
# Rom: 14
# Byzanz: 12

# ----------------------------------------------------
# ############# Hinweise von mir (Pie): ##############
# ----------------------------------------------------

# 19.10.2026
# Schreibe in deine PAE_WegDerGoten.CivBeyondSwordWBSave-Datei folgendes (kannst du auch im WB machen (ohne "ScriptData=")):
# Bei der Unit Alarich statt: ScriptData=Alarich ersetze mit ScriptData={"t": "Alarich"}
# Beim TheElder-Stammesfürst statt ScriptData=TheElder ersetze mit ScriptData={"t": "TheElder"}
# Und bei der Stadt Rom ScriptData={"t": "Rome"}


# ----------------------------------------------------
# ################# Hinweise Ende ####################
# ----------------------------------------------------


# Imports
from CvPythonExtensions import (CyGlobalContext, UnitAITypes, CyMap, CyPopupInfo, ButtonPopupTypes, DirectionTypes,
		plotDirection, CyTranslator, CyInterface, ColorTypes, CyCamera, plotXY, CyGInterfaceScreen, EventContextTypes, CyGame)
# import CvEventInterface
import CvUtil
import PyHelpers
# import CvCameraControls
import PAE_Unit
import PAE_City
import PAE_Christen
import PAE_Lists as L
# for popups with dds:
import CvScreenEnums
import Popup as PyPopup

# Defines
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

# Internes (Chancen in %)
iChanceSettlerOnCityAcquired = 10	# 10
iChanceGreatSpyOnConquer = 33			# 33
iChanceSetChristentum = 3				# 5
iChanceSpreadChristentum = 2			# 2
bTheElderUnitAITypeAttack = False	# Event 1.3

#[EVENT-1.2] Jagdgebiet wird erweitert:
#8 Plots um eigene Städte kann Nahrung erjagt werden
# => befindet sich in PAE_Unit getHuntingDistance()

def onGameStart():
#[EVENT-1.1] Vor Spielstart, Auswürfeln der Heiligen Städte.
	# Nordische Mythen: Cherusker (50%), Markomanne (25%), Hermundure (25%)
	# Keltische Mythen: Britonen (50%), Gallier (25%) Aquitanier (25%)
	# Die gewürfelte heilige Stadt bekommt ihr Wunder eingebaut: Donareiche bzw. Heiliger Hain
	lPlayerRelNordic = [1,1,3,4]
	lPlayerRelCeltic = [5,5,6,8]

	# Nordic Gods
	iRand = CvUtil.myRandom(len(lPlayerRelNordic), "WDG_RelNordic")
	iPlayer = lPlayerRelNordic[iRand]
	pPlayer = gc.getPlayer(iPlayer)
	lCities = []
	(loopCity, pIter) = pPlayer.firstCity(False)
	while loopCity:
		if not loopCity.isNone() and loopCity.getOwner() == iPlayer:
			lCities.append(loopCity)
		(loopCity, pIter) = pPlayer.nextCity(pIter, False)
	iRand = CvUtil.myRandom(len(lCities), "WDG_CitiesRelNordic")
	pCity = lCities[iRand]
	gc.getGame().setHolyCity(gc.getInfoTypeForString("RELIGION_NORDIC"), pCity, True)
	pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_NORDIC_SHRINE"), 1)

	# Celtic Gods
	iRand = CvUtil.myRandom(len(lPlayerRelCeltic), "WDG_RelCeltic")
	iPlayer = lPlayerRelCeltic[iRand]
	pPlayer = gc.getPlayer(iPlayer)
	lCities = []
	(loopCity, pIter) = pPlayer.firstCity(False)
	while loopCity:
		if not loopCity.isNone() and loopCity.getOwner() == iPlayer:
			lCities.append(loopCity)
		(loopCity, pIter) = pPlayer.nextCity(pIter, False)
	iRand = CvUtil.myRandom(len(lCities), "WDG_CitiesRelCeltic")
	pCity = lCities[iRand]
	gc.getGame().setHolyCity(gc.getInfoTypeForString("RELIGION_CELTIC"), pCity, True)
	pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_CELTIC_SHRINE"), 1)


#[EVENT-1.5] - onGameStart; Spielstart: Einige KI-Spieler erhalten zufällig 1 Siedler:
	#Alle Siedler, die evtl. auf der Karte sind, löschen
	iRange = gc.getMAX_PLAYERS()
	for iPlayer in range(iRange):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer is not None and not loopPlayer.isNone() and loopPlayer.isAlive():
			lUnits = PyPlayer(loopPlayer.getID()).getUnitList()
			for pUnit in lUnits:
				if pUnit is not None and not pUnit.isNone():
					eUnitType = pUnit.getUnitType()
					if (eUnitType == gc.getInfoTypeForString("UNIT_SETTLER")):
						pUnit.kill(True, -1)
	#Player 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 15, 16, 17 erhalten mit 33% Wahrscheinlichkeit 1 Siedler in ihrer Hauptstadt
	lPlayers = [1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 15, 16, 17]
	for iPlayer in lPlayers:
		iRand = CvUtil.myRandom(3, "WDG_SettlerOnGameStart")
		if iRand == 1:
			pCity = gc.getPlayer(iPlayer).getCapitalCity()
			if not pCity.isNone():
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString("UNIT_SETTLER"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_SETTLE, DirectionTypes.DIRECTION_SOUTH)


#[EVENT-10.0] - onGameStart; Spielstart: Je nach Schwierigkeitsgrad erhält der Spieler unterschiedliche Truppen auf Plot (99/79):
	#Alle Einheiten, die auf dem Feld 99/79 stehen, löschen -> DANN
	#Alles über Kaiser: (A)
	#Kaiser: (B)
	#König: (C)
	#Bis einschl. Prinz: (D)
	"""
	(A)
	1x UNIT_SWORDSMAN_LATENE,
	2x UNIT_AXEMAN2,
	2x UNIT_GERMANNE,
	1x UNIT_SEHER,
	1x UNIT_WORKER,

	(B)
	Alles aus A, plus:
	1x UNIT_GERMANNE,
	1x UNIT_EMIGRANT

	(C)
	Alles aus A, B, plus:
	1x UNIT_BERSERKER_GERMAN,
	1x UNIT_EMIGRANT

	(D)
	Alles aus A, B, C, plus:
	1x UNIT_GERMANNE,
	1x UNIT_EMIGRANT
	"""
	iPlayer = 0
	pPlayer = gc.getPlayer(iPlayer)
	iX = 99 #für Testzwecke auf der kleineren 70x90 Karte (iX=50). Ist auf der echten Karte 99
	iY = 79
	# Handicap: 0 (Settler) - 8 (Deity) ; 5 = King
	iHandicap = gc.getGame().getHandicapType()
	pPlot = gc.getMap().plot(iX, iY)
	iRange = pPlot.getNumUnits()
	for iUnit in range(iRange):
		pLoopUnit = pPlot.getUnit(iUnit)
		if not pLoopUnit.isNone():
			pLoopUnit.kill(True, -1)
	# (A)
	pPlayer.initUnit(gc.getInfoTypeForString("UNIT_SWORDSMAN_LATENE"), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
	pPlayer.initUnit(gc.getInfoTypeForString("UNIT_AXEMAN2"), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
	pPlayer.initUnit(gc.getInfoTypeForString("UNIT_AXEMAN2"), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
	pPlayer.initUnit(gc.getInfoTypeForString("UNIT_GERMANNE"), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
	pPlayer.initUnit(gc.getInfoTypeForString("UNIT_GERMANNE"), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
	pPlayer.initUnit(gc.getInfoTypeForString("UNIT_SEHER"), iX, iY, UnitAITypes.UNITAI_RESERVE, DirectionTypes.DIRECTION_SOUTH)
	pPlayer.initUnit(gc.getInfoTypeForString("UNIT_WORKER"), iX, iY, UnitAITypes.UNITAI_WORKER, DirectionTypes.DIRECTION_SOUTH)
	# (B)
	if iHandicap <= 6:
		pPlayer.initUnit(gc.getInfoTypeForString("UNIT_GERMANNE"), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		pPlayer.initUnit(gc.getInfoTypeForString("UNIT_EMIGRANT"), iX, iY, UnitAITypes.UNITAI_RESERVE, DirectionTypes.DIRECTION_SOUTH)
	# (C)
	if iHandicap <= 5:
		pPlayer.initUnit(gc.getInfoTypeForString("UNIT_BERSERKER_GERMAN"), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		pPlayer.initUnit(gc.getInfoTypeForString("UNIT_EMIGRANT"), iX, iY, UnitAITypes.UNITAI_RESERVE, DirectionTypes.DIRECTION_SOUTH)
	# (D)
	if iHandicap <= 4:
		pPlayer.initUnit(gc.getInfoTypeForString("UNIT_GERMANNE"), iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		pPlayer.initUnit(gc.getInfoTypeForString("UNIT_EMIGRANT"), iX, iY, UnitAITypes.UNITAI_RESERVE, DirectionTypes.DIRECTION_SOUTH)



# [EVENT-2.1] Rom (Player 14) und Byzanz (Player 12) haben ein permanentes Verteidigungsbündnis bis zur Reichsteilung
	#gc.getTeam(gc.getPlayer(14).getTeam()).signDefensivePact(12)



def DawnOfMan():
#[EVENT-10.1] - onDawnOfMan;
	# Bild PopUp bei Spielstart
	#Ihr seid Alarich der Gote!
	#Gestern noch ein angesehener Clanfürst im Gotenreich, heute ein Verbannter. Die alte Heimat ist zum Feind geworden, ihr müsst sie als Barbaren betrachten! Aber die Gemeinschaft ist schwach, wir sollten nicht zögern und zurückschlagen! Einer eurer Gefolgsleute ist dortgeblieben, um die Lage für euch auszukundschaften.
	#Wir sollten sofort nach Hagelsberg marschieren. Dem Ältesten persönlich die Tür eintreten, durch die er uns grade erst hinausgeworfen hat. Und dort ist auch der zentrale Rüstungsschneider, von wo aus das ganze Reich versorgt wird.
	#Oder wir beginnen unseren Feldzug weiter südlich die Weichsel rauf, wo mit weniger Widerstand zu rechnen ist. Interessant sind vor allem die Pferde in Gotonen. Die Reiterei ist eine für uns noch recht neue Angelegenheit, könnte aber ein wichtiger Pfeiler der Armee werden.
	#Die Entscheidung trefft Ihr, und das Schicksal der wahren Goten liegt in Eurer Hand.
	#<EROBERT EINE STADT>
	szTextHead = ""
	szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GAME_START", ("", ))
	PopUpDDS("Art/Scenarios/WegDerGoten/WDG08.dds",szTextHead,szTextBody,"RIGHT")



def onBeginPlayerTurn(iGameTurn, iPlayer):
	global bTheElderUnitAITypeAttack
	pPlayer = gc.getPlayer(iPlayer)

	if iPlayer == 0:

		#[EVENT-10.6] Wenn der Spieler zwei verschiedene Fleischressourcen im Handelsnetz hat -> DANN
		#Plot (0,1): pPlot.setScriptData() für EVENT-10.6
		#Ein Fruchtbarkeitskultist wird in der Hauptstadt [get.Capitalname] erstellt
		#Ihr habt unterschiedliche Fleischressourcen im Handelsnetz. Ein Anhänger des Fruchtbarkeitskultes will sich bei euch ansiedeln.
		iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["10_6"], "")
		if iCheck == "":
			pCity = pPlayer.getCapitalCity()
			iBoni = 0
			for iBonus in L.LBonusLivestock:
				#if pPlayer.hasBonus(iBonus):
				if pCity.hasBonus(iBonus):
					iBoni += 1
			if iBoni > 1:
				pPlayer.initUnit(gc.getInfoTypeForString("UNIT_EXECUTIVE_2"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_UNKNOWN, DirectionTypes.DIRECTION_SOUTH)
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "10_6", "x")

				if pPlayer.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FRUCHTBARKEITSKULTIST", ("", )))
					popupInfo.addPopup(iPlayer)

		#[EVENT-10.7] Wenn der Spieler zwei verschiedene Getreideressourcen im Handelsnetz hat -> DANN
		#Plot (0,1): pPlot.setScriptData() für EVENT-10.7
		#Ein Kybelekultist wird in der [get.Capitalname] erstellt
		#Ihr habt unterschiedliche Getreidesorten im Handelsnetz. Ein Anhänger des Kybelekultes will sich bei euch ansiedeln.
		iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["10_7"], "")
		if iCheck == "":
			pCity = pPlayer.getCapitalCity()
			iBoni = 0
			for iBonus in L.LBonusGetreide:
				#if pPlayer.hasBonus(iBonus):
				if pCity.hasBonus(iBonus):
					iBoni += 1
			if iBoni > 1:
				pPlayer.initUnit(gc.getInfoTypeForString("UNIT_EXECUTIVE_3"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_UNKNOWN, DirectionTypes.DIRECTION_SOUTH)
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "10_7", "x")

				if pPlayer.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_KYBELEKULTIST", ("", )))
					popupInfo.addPopup(iPlayer)

		#[EVENT-10.8] - onBeginPlayerTurn; Wenn der Spieler zwei verschiedene Heroenkult-Ressourcen im Handelsnetz hat -> DANN
		#Plot (0,1): pPlot.addScriptData() für EVENT-10.8
		#Ein Heroenkultist wird in der Hauptstadt erstellt
		#Ihr habt interessante Ressourcen im Handelsnetz. Ein Anhänger des Heroenkultes will sich bei euch ansiedeln.
		iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["10_8"], "")
		if iCheck == "":
			pCity = pPlayer.getCapitalCity()
			iBoni = 0
			LBonus = [
				gc.getInfoTypeForString("BONUS_IRON2"),
				gc.getInfoTypeForString("BONUS_BRONZE"),
				gc.getInfoTypeForString("BONUS_HORSE")
			]
			for iBonus in LBonus:
				#if pPlayer.hasBonus(iBonus):
				if pCity.hasBonus(iBonus):
					iBoni += 1
			if iBoni > 1:
				pPlayer.initUnit(gc.getInfoTypeForString("UNIT_EXECUTIVE_5"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_UNKNOWN, DirectionTypes.DIRECTION_SOUTH)
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "10_8", "x")

				if pPlayer.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_HEROENKULTIST", ("", )))
					popupInfo.addPopup(iPlayer)

		#[EVENT-27.2] Verteidigungsbuendnis unter GerVandanen (Civ4 hat dafuer kein Ereignis, daher Pruefung jede Runde)
		lGV = [1,2,3,4,9]
		pTeam0 = gc.getTeam(pPlayer.getTeam())
		for i in range(len(lGV)):
			for j in range(i + 1, len(lGV)):
				iA = lGV[i]
				iB = lGV[j]
				sKey = "27_2_" + str(iA) + "_" + str(iB)
				if gc.getPlayer(iA).isAlive() and gc.getPlayer(iB).isAlive() and gc.getTeam(iA).isDefensivePact(iB):
					if CvUtil.getScriptData(gc.getMap().plot(0, 1), [sKey], "") == "":
						CvUtil.addScriptData(gc.getMap().plot(0, 1), sKey, "x")
						if pPlayer.isHuman() and not pTeam0.isAtWar(iA) and not pTeam0.isAtWar(iB):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GERVANDALS_DEFENSIVEPACT", (gc.getPlayer(iA).getName(), gc.getPlayer(iB).getName())))
							popupInfo.addPopup(iPlayer)


	elif iPlayer == 20:
		#[EVENT-1.3] – global in py; AI für den Ältesten:
		#Der Älteste "ScriptData=TheElder" ist Stammesfürst mit General der Alten Goten (Player 20) in Hagelsberg. Er hat zu Beginn des Spiels AI=CityDefence. DANN ->
		#5% Chance jede Runde, dass er zu AI=Attack wechselt
		if not bTheElderUnitAITypeAttack:
			for pLoopUnit in PyPlayer(iPlayer).getUnitList():
				if not pLoopUnit.isNone():
					if CvUtil.getScriptData(pLoopUnit, ["t"]) == "TheElder":
						if pLoopUnit.getUnitAIType() == UnitAITypes.UNITAI_ATTACK:
							bTheElderUnitAITypeAttack = True
						else:
							if CvUtil.myRandom(20, "WDG_Event_1.3_TheElder") == 1:
								pLoopUnit.setUnitAIType(UnitAITypes.UNITAI_ATTACK)
								bTheElderUnitAITypeAttack = True


def onCityAcquired(iPreviousOwner, iNewOwner, pCity):
	global iChanceSettlerOnCityAcquired
	global iChanceGreatSpyOnConquer

	lGermanen = [1,2,3,4]
	lGerVandalen = [0,1,2,3,4,9]
	pNewOwner = gc.getPlayer(iNewOwner)
	iNumCities = pNewOwner.getNumCities()
	iActivePlayer = gc.getGame().getActivePlayer()

	# Germanen
	iAnzVassals = 0
	iAlive = 0
	if iPreviousOwner in lGermanen:
		for iGermane in lGermanen:
			if gc.getPlayer(iGermane).isAlive() and gc.getPlayer(iGermane).getNumCities() > 0:
				# Vasall von Goten (Spieler 0)
				if gc.getTeam(iGermane).isVassal(gc.getPlayer(0).getTeam()):
					iAnzVassals += 1
				else:
					iAlive += 1


#[EVENT-3.1] Es gibt Siedler: Ab der 2. eroberten Stadt gibt es bei jeder Eroberung eine 10% Chance
	if iNumCities > 1:
		if CvUtil.myRandom(100, "WDG_SettlerOnCityAcquired") < iChanceSettlerOnCityAcquired:
			pNewOwner.initUnit(gc.getInfoTypeForString("UNIT_SETTLER"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_SETTLE, DirectionTypes.DIRECTION_SOUTH)

			# Kultur setzen
			#iCulture = pCity.getCulture(iPreviousOwner) / 2
			#pCity.setCulture(iPreviousOwner, iCulture, 1)
			#pCity.setCulture(iNewOwner, iCulture, 1)

			#Ihr habt durch eure Eroberungen viele Leute um euch gesammelt, die nach einer Heimat verlangen. Weist ihnen einen Platz zu, an dem sie ihre eigene Siedlung aufbauen sollen. Sie haben genug gekämpft und verdienen einen Ort, den sie ihr zu Hause nennen.
			#<IHR ERHALTET 1 SIEDLER>
			if pNewOwner.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_SETTLER", ("", )))
				popupInfo.addPopup(iNewOwner)


#[EVENT-10.3] Wenn der Gote die erste Stadt erobert (vom Alten Goten)
	#Der Palast, Monolith und Heldendenkmal wird gesetzt.
	# Die heilige Stadt der Nordischen Mythen wird 1x aufgedeckt
	if iNewOwner == 0 and iPreviousOwner == 20:
		iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["10_3"], "")
		if iCheck == "":

			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_PALACE"), 1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MONOLITH"), 1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MONUMENT"), 1)

			# Die Gotenhauptstadt bekommt 80% Kultur.
			iPreviousCulture = pCity.getCulture(iPreviousOwner) / 10
			pCity.setCulture(iPreviousOwner, iPreviousCulture * 2, 1)
			pCity.setCulture(iNewOwner, iPreviousCulture * 8, 1)

			# Die Heilige Stadt der Nordischen Mythen wird 1x aufgedeckt (aus [Event-1.1])
			pHolyCity = gc.getGame().getHolyCity(gc.getInfoTypeForString("RELIGION_NORDIC"))
			if not pHolyCity.isNone():
				doRevealPlot(0, pHolyCity.plot(), False)

			# Der erste Schritt ist getan. Ihr habt [get.cityname] erobert!
			# Dies wird die Hauptstadt eines neuen, geeinten Gotenreiches sein. Es soll das größte Reich aller Zeiten in Germanien werden, das sich am Ende mit dem der Römer messen kann.
			#Ihr lasst die Leute alle Schäden reparieren und hier unsere Heimat aufbauen. Wir sollten auch bald einen Tempel errichten, um den Göttern zu huldigen. Der Älteste und seine Sippe haben scheinbar geschlafen die letzten Jahre, viele Gebäude sind noch nichtmal geplant.
			#Die heilige Donareiche steht schon seit den Ahnen unter Kontrolle von [get.Leadername], das Zentrum der Götter in [get.cityname] sollten wir irgendwann unter gotische Kontrolle bringen..
			#Das Überraschungsmoment ist jetzt auf unserer Seite. Es empfielt sich, schnell weiter zu ziehen und die umliegenden Dörfer zu erobern.
			#<EROBERT WEITERE STÄDTE>
			#<EROBERT DIE HEILIGE STADT>
			# ohne Heilige Stadt kein PopUp (der Text nennt sie und ihren Besitzer)
			if gc.getPlayer(iNewOwner).isHuman() and not pHolyCity.isNone():
				szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CITY_HEAD", (pCity.getName(), ))
				szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CITY_BODY", (pHolyCity.getName(), gc.getPlayer(pHolyCity.getOwner()).getName(), pHolyCity.getName()))
				PopUpDDS("Art/Scenarios/WegDerGoten/WDG02.dds",szTextHead,szTextBody,"RIGHT")

			# setScriptData
			CvUtil.addScriptData(gc.getMap().plot(0, 1), "10_3", "x")

			# Zoom zur neuen Hauptstadt
			CyCamera().JustLookAtPlot(pCity.plot())
			CyCamera().ZoomIn(0.5)

#[EVENT-10.4] - onCityAcquired; Wenn der Spieler die drei Städte der Alten Goten (Hagelsberg, Gnesen und Gotonen) im Besitz hat:
		#Plot (0,1): pPlot.setScriptData() für EVENT-10.4
		iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["10_4"], "")
		if iCheck == "":
			#Ausgezeichnet! Ihr habt die alte Heimat unter Kontrolle gebracht.
			#Nun lasst uns Vorbereitungen treffen, um die umliegenden Stämme zu unterwerfen. Wir sollten Spione ausbilden, um alle Windrichtungen zu erkunden. Und wir werden weitere Soldaten trainieren müssen, um zu gegebener Zeit mit einer großen Armee vor den Göttern nach Westen zu marschieren.
			#Die vier großen Germanenstämme sollen hinter euch versammelt sein, euch als Vasallen die Treue schwören!

			#Denkt daran, schon früh Straßen in die weiten Wälder zu schlagen. Auch das wurde vom Ältesten immer vernachlässigt!

			#<VEREINT DIE GERMANENSTÄMME IM WESTEN UNTER EUREM BANNER>
			#Hagelsberg: x=95,y=83
			#Gnesen: x=91,y=77
			#Gotonen: x=102,y=71
			if (gc.getMap().plot(95, 83).getOwner() == 0 and
				 gc.getMap().plot(91, 77).getOwner() == 0 and
				 gc.getMap().plot(102,71).getOwner() == 0
				):
				if gc.getPlayer(iNewOwner).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_OLD_GOTHS", ("", )))
					popupInfo.addPopup(iNewOwner)
				# setScriptData
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "10_4", "x")


#[EVENT-10.5] - onCityAcquired;
	#Wenn jemand anders als der Spieler eine der drei Städte des Alten Goten (Hagelsberg, Gnesen und Gotonen) erobert -> DANN
	if iPreviousOwner == 20 and iNewOwner != 0:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_OLD_GOTHS_OTHERS", (gc.getPlayer(iNewOwner).getCivilizationDescriptionKey(),pCity.getName())))
		popupInfo.addPopup(0)


#[EVENT-10.9] - onCityAcquired; Wenn die Alten Goten (Player 20) eine Stadt erobern
	#[ABFRAGE] Ist es NICHT Hagelsberg, Gnesen oder Gotonen -> DANN
	#Die Stadt wird 1x aufgedeckt (fuer den Spieler, Team 0)
	#Plot (0,1): pPlot.addScriptData() fuer EVENT-10.9 (Meldung nur beim ersten Mal)
	#Hagelsberg: x=95,y=83 / Gnesen: x=91,y=77 / Gotonen: x=102,y=71
	if iNewOwner == 20 and (pCity.getX(), pCity.getY()) not in [(95, 83), (91, 77), (102, 71)]:
		doRevealPlot(0, pCity.plot(), False)
		#iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["10_9"], "")
		#if iCheck == "":
		#[get.Leadername] hat [get.Cityname] erobert. Scheinbar hat er erkannt, dass er sein Reich erweitern sollte. Etwas spät!
		#Zu gegebener Zeit werden wir ihn auch dort besuchen.
		if gc.getPlayer(0).isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_OLD_GOTHS_EXPAND", (gc.getPlayer(20).getName(), pCity.getName())))
			popupInfo.addPopup(0)
		#	# setScriptData
		#	CvUtil.addScriptData(gc.getMap().plot(0, 1), "10_9", "x")


#[EVENT-13.1] - onCityAcquired; Wenn der Spieler (zum ersten Mal) eine Stadt eines Germanen (Player 1, 2, 3, 4) erobert:
	#[ABFRAGE] Lebt Alarich noch? -> DANN
	#Plot (0,1): pPlot.setScriptData() für EVENT-13.1
	if iNewOwner == 0 and pNewOwner.isHuman() and iPreviousOwner in lGermanen:
		iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["13_1"], "")
		if iCheck == "":
			for pLoopUnit in PyPlayer(iNewOwner).getUnitList():
				if not pLoopUnit.isNone():
					if CvUtil.getScriptData(pLoopUnit, ["t"]) == "Alarich":

						#Mit der Einnahme von [get.cityname] habt ihr wahrlich ein Zeichen gesetzt.
						#Die Welt soll erfahren, dass die große Vereinigung aller Germanenvölker begonnen hat! Diese Kunde wird von den Barden in alle Himmelsrichtungen getragen. Euer Name wird schon bald in aller Munde sein!
						#
						#Eine Ballade dieser Zeit:
						#"Auf dass ihr es alle seht - Alarich der Gote - wer auf der falsche Seite steht - verzeichnet Tote"

						#Denkt daran, dass die Stämme euch als Vasallen dienen sollen. Vereinigung der Völker bedeutet nicht ihre Auslöschung!
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_GERMAN_CITY", (pCity.getName(), )))
						popupInfo.addPopup(iNewOwner)

						# setScriptData
						CvUtil.addScriptData(gc.getMap().plot(0, 1), "13_1", "x")


#[EVENT-14.1] - onCityAcquired; Wenn der Spieler die Heilige Stadt (Donareiche aus Event-1.1) erobert
	#[ABFRAGE] Hat der Spieler Nordische Mythen als Staatsreli? -> DANN (A)
	#[ABFRAGE] Hat der Spieler eine andere Staatsreli? -> DANN (B)
	#(A)
	#Den Göttern sei Dank! Wir haben die Heilige Stadt unter Kontrolle gebracht! Der Hüter der Donareiche steht zu eurer Verfügung.
	#Auf dass dieser heilige Ort zu wahrer Größe gelangen möge, wie es dem Thing der Götter würdig ist.
	#<IHR ERHALTET 1 GROSSER PROPHET>
	#Plot (0,1): pPlot.setScriptData() für EVENT-14.1
	#Großer Prophet „Der Hüter“ wird in der Heiligen Stadt gesetzt
	#(B)
	#Plot (0,1): pPlot.setScriptData() für EVENT-14.1
	#Die Donareiche, das Zentrum der alten Götter steht unter eurer Kontrolle. Wenn auch ohne Bedeutung für uns, doch eine schöne Erinnerung an die Zeiten der Ahnen.
	if iNewOwner == 0 and pNewOwner.isHuman():
		iReligion = gc.getInfoTypeForString("RELIGION_NORDIC")
		if pCity.isHolyCityByType(iReligion):
			iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["14_1"], "")
			if iCheck == "":
				iCheck = CvUtil.addScriptData(gc.getMap().plot(0, 1), "14_1", "x")
				if pNewOwner.getStateReligion() == iReligion:

					pNewUnit = gc.getPlayer(iNewOwner).initUnit(gc.getInfoTypeForString("UNIT_PROPHET"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_PROPHET, DirectionTypes.DIRECTION_SOUTH)
					txtName = CyTranslator().getText("TXT_KEY_WDG_NORDIC_GUARDIAN", ())
					pNewUnit.setName(txtName)

					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CAPTURED_NORDIC_HOLY_CITY_1", ()))
					popupInfo.addPopup(iNewOwner)

				else:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CAPTURED_NORDIC_HOLY_CITY_2", ()))
					popupInfo.addPopup(iNewOwner)


#[EVENT-14.2]; Wenn jemand anders die Heilige Stadt (Donareiche aus Event-1.1) erobert -> DANN
	#[ABFRAGE] Hat der Spieler Nordische Mythen als Staatsreli? -> DANN
	#Die Heilige Stadt [get.Cityname] wurde von [get.Leadername] erobert! Das ist gegen den Willen der Götter, wir sollten sie befreien!
	else:
		iHumanPlayer = gc.getGame().getActivePlayer()
		if iHumanPlayer == 0 and gc.getPlayer(iHumanPlayer).isHuman():
			iReligion = gc.getInfoTypeForString("RELIGION_NORDIC")
			if pCity.isHolyCityByType(iReligion):
				if gc.getPlayer(iHumanPlayer).getStateReligion() == iReligion:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CAPTURED_NORDIC_HOLY_CITY_3", (pCity.getName(), gc.getPlayer(iNewOwner).getName())))
					popupInfo.addPopup(iHumanPlayer)


#[EVENT-15.1] - onCityAcquired & onVassalState; Wenn der Spieler einen KI-Gegner (nicht MinorCiv) vasallisiert oder vernichtet:
	#Immer, wenn der Spieler eine KI-Gegner vasallisiert oder vernichtet, gibt es eine 33% Chance auf dieses Ereignis -> DANN
	#Plot (0,1): pPlot.setScriptData() für EVENT-15.1
	#1 Großer Spion "Speculatore" wird in der Hauptstadt des neuen Vasallen erstellt. Bei Vernichtung in der letzten eroberten Stadt
	#1 Spion wird in der römischen Hauptstadt erstellt
	if iNewOwner == 0:
		if not gc.getPlayer(iPreviousOwner).isMinorCiv() and not gc.getPlayer(iPreviousOwner).isBarbarian():
			if gc.getPlayer(iPreviousOwner).getNumCities() == 0:
				iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["15_1"], "")
				if iCheck == "":
					if CvUtil.myRandom(100, "WDG Great Spy onVassalState") < iChanceGreatSpyOnConquer:
						CvUtil.addScriptData(gc.getMap().plot(0, 1), "15_1", "x")

						pNewUnit = pNewOwner.initUnit(gc.getInfoTypeForString("UNIT_GREAT_SPY"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MERCHANT, DirectionTypes.DIRECTION_SOUTH)
						pNewUnit.setName("Speculatore")

						#1 Spion wird in der römischen Hauptstadt erstellt (Rom: 14)
						pCityRome = gc.getPlayer(14).getCapitalCity()
						pNewOwner.initUnit(gc.getInfoTypeForString("UNIT_SPY"), pCityRome.getX(), pCityRome.getY(), UnitAITypes.UNITAI_SPY, DirectionTypes.DIRECTION_SOUTH)

						#Ihr habt euch als erfolgreicher Feldherr erwiesen und schon so einige Stämme unterworfen! Ein eher unscheinbarer Kerl, der uns schon länger folgt, offenbart sich als Kundschafter aus Rom und bietet seine Dienste an.
						#Er nennt sich selbst Speculatore, hat mit [get.LeadernameRömer] noch eine Rechnung offen und will dabei helfen, eine Macht aufzubauen, die den römischen Legionen gewachsen ist!
						#Ein Komplize des Speculatore ist in [get.CapitalnameRömer] geblieben, um über die Lage vor Ort zu berichten.
						#<IHR ERHALTET 1 GROSSER SPION>
						#<IHR ERHALTET 1 SPION IN [get.CapitalnameRömer]>

						if pNewOwner.isHuman():
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_SPECULATORE", (gc.getPlayer(14).getName(), pCityRome.getName(), pCityRome.getName())))
							popupInfo.addPopup(iNewOwner)


#____________________(GEÄNDERT) 15.2 und 15.3 zusammengefasst
#[EVENT-15.2.2] – onPlayerVasall & onCityAcquired; Vereinigung der Germanen (Player 1, 2, 3, 4)
#A) bei onVassalState
#B) Wenn ein Germane vernichtet wird
#[ABFRAGE 1] Gibt es damit weniger als zwei Germanen? (<2) -> DANN
#-> Quest gescheitert
#[ABFRAGE 2] Hat der Spieler alle restlichen Germanen als Vasall > DANN
#Plot (0,1): ScriptData() für EVENT-15.2
#-> Trostpreis

#iAnzVassals
#iAlive
	if iPreviousOwner in lGermanen:
		if gc.getPlayer(iPreviousOwner).getNumCities() == 0:
			if CvUtil.getScriptData(gc.getMap().plot(0, 1), ["15_2"], "") == "":
				if iAnzVassals + iAlive < 2:
					CvUtil.addScriptData(gc.getMap().plot(0, 1), "15_2", "x")
					if gc.getPlayer(0).isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_15_4", ("",)))
						popupInfo.addPopup(0)
				elif iAlive == 0:
					pCity = gc.getPlayer(0).getCapitalCity()
					if not pCity.isNone():
						CvUtil.addScriptData(gc.getMap().plot(0, 1), "15_2", "x")
						gc.getPlayer(0).initUnit(gc.getInfoTypeForString("UNIT_BERSERKER_GERMAN"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						if gc.getPlayer(0).isHuman():
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_15_3", ("",)))
							popupInfo.addPopup(0)


#[EVENT-16.1] - onCityAcquired; Wenn der Spieler die Hauptstadt [get.Capitalname] vom Römer (Player 14) einnimmt
#Der Spieler bekommt 500 Punkte
#[EVENT-17.1] - onPlayerKilled; Wenn der Spieler den Römer (Player 14) vasallisiert ODER vernichtet hat
#Der Spieler bekommt 1.000 Punkte
#DIESE MELDUNG SOLL IN DER MITTE DES BILDSCHIRMS KOMMEN, quasi ein Siegbildschirm
	if iPreviousOwner == 14 and iNewOwner == iActivePlayer:
		if gc.getPlayer(iPreviousOwner).getNumCities() == 0:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_ROME", ("", )))
			popupInfo.addPopup(0)
		else:
			if CvUtil.getScriptData(pCity, ["t"]) == "Rome":
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_ROME_CAPITAL", ("", )))
				popupInfo.addPopup(0)


#[EVENT-20.5.1] - onCityAcquired; Wenn die Vandalen (Player 9) vernichtet werden:
	#[ABFRAGE] Hat der Spieler ihn besiegt? -> DANN (A) + SciptData 20.5
	#[ABFRAGE] Hat jemand anders ihn besiegt? -> DANN (B) + SciptData 20.5
	if iPreviousOwner == 9:
		if gc.getPlayer(iPreviousOwner).getNumCities() == 0:
			CvUtil.addScriptData(gc.getMap().plot(0, 1), "20_5", "x")
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			if iNewOwner == 0:
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_VANDALS3", (gc.getPlayer(iPreviousOwner).getName(), )))
			else:
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_VANDALS4", (gc.getPlayer(iNewOwner).getName(), )))
			popupInfo.addPopup(0)

#[EVENT-21.5.1] - onCityAcquired; Wenn die Warnen (Player 2) vernichtet werden:
	#[ABFRAGE] Hat der Spieler ihn besiegt? -> DANN (A)
	#[ABFRAGE] Hat jemand anders ihn besiegt? -> DANN (B)
	#(A) Plot (0,1): pPlot.addScriptData() für EVENT-21.5
	#(B) [ABFRAGE] Ist es NICHT der Römer (Player 14)? -> DANN pPlot.addScriptData() für EVENT-21.5
	if iPreviousOwner == 2:
		if gc.getPlayer(iPreviousOwner).getNumCities() == 0:
			if iNewOwner == 0:
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "21_5", "x")
				if gc.getPlayer(0).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_WARNEN4", (gc.getPlayer(iPreviousOwner).getName(), )))
					popupInfo.addPopup(0)
			elif iNewOwner != 14:
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "21_5", "x")
				if gc.getPlayer(0).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_WARNEN5", (gc.getPlayer(iNewOwner).getName(), gc.getPlayer(iPreviousOwner).getName())))
					popupInfo.addPopup(0)

#[EVENT-22.5.1] - onCityAcquired; Wenn die Hermunduren (Player 4) vernichtet werden:
	#[ABFRAGE] Hat der Spieler ihn besiegt? -> DANN (A)
	#[ABFRAGE] Hat jemand anders ihn besiegt? -> DANN (B)
	#(A) Plot (0,1): pPlot.addScriptData() für EVENT-22.5
	#(B) [ABFRAGE] Ist es NICHT der Römer (Player 14)? -> DANN addScriptData() für EVENT-22.5
	if iPreviousOwner == 4:
		if gc.getPlayer(iPreviousOwner).getNumCities() == 0:
			if iNewOwner == 0:
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "22_5", "x")
				if gc.getPlayer(0).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_HERMUN4", (gc.getPlayer(iPreviousOwner).getName(), )))
					popupInfo.addPopup(0)
			elif iNewOwner != 14:
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "22_5", "x")
				if gc.getPlayer(0).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_HERMUN5", (gc.getPlayer(iNewOwner).getName(), gc.getPlayer(iPreviousOwner).getName())))
					popupInfo.addPopup(0)

#[EVENT-23.5.1] - onCityAcquired; Wenn die Cherusker (Player 1) vernichtet werden:
	#[ABFRAGE] Hat der Spieler ihn besiegt? -> DANN (A)
	#[ABFRAGE] Hat jemand anders ihn besiegt? -> DANN (B)
	#(A) Plot (0,1): pPlot.addScriptData() für EVENT-23.5
	#(B) [ABFRAGE] Ist es NICHT der Römer (Player 14)? -> DANN ScriptData 23.5
	if iPreviousOwner == 1:
		if gc.getPlayer(iPreviousOwner).getNumCities() == 0:
			if iNewOwner == 0:
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "23_5", "x")
				if gc.getPlayer(0).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_CHERUSK4", (gc.getPlayer(iPreviousOwner).getName(), )))
					popupInfo.addPopup(0)
			elif iNewOwner != 14:
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "23_5", "x")
				if gc.getPlayer(0).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_CHERUSK5", (gc.getPlayer(iNewOwner).getName(), gc.getPlayer(iPreviousOwner).getName())))
					popupInfo.addPopup(0)

#[EVENT-24.5] - onCityAcquired; Wenn die Markomannen (Player 3) vernichtet werden:
	#[ABFRAGE] Hat der Spieler ihn besiegt? -> DANN (A)
	#[ABFRAGE] Hat jemand anders ihn besiegt? -> DANN (B)
	#(A) Plot (0,1): pPlot.addScriptData() für EVENT-24.5
	#(B) [ABFRAGE] Ist es NICHT der Römer (Player 14)? -> DANN pPlot.addScriptData() für EVENT-24.5
	if iPreviousOwner == 3:
		if gc.getPlayer(iPreviousOwner).getNumCities() == 0:
			if iNewOwner == 0:
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "24_5", "x")
				if gc.getPlayer(0).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_MARKO4", (gc.getPlayer(iPreviousOwner).getName(), )))
					popupInfo.addPopup(0)
			elif iNewOwner != 14:
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "24_5", "x")
				if gc.getPlayer(0).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_MARKO5", (gc.getPlayer(iNewOwner).getName(), gc.getPlayer(iPreviousOwner).getName())))
					popupInfo.addPopup(0)

#[EVENT-27.3] – onCityAcquired; Wenn ein vernichteter GerVandane (Player 1, 2, 3, 4, 9) wieder eine Stadt erobert (Oder anderweitig geschenkt bekommt)
#[check.ScriptData() für EVENT-20, 21, 22, 23, und 24.5] ->
#ZOOM auf die Stadt
#Ihr Volk galt als ausgelöscht, und doch haben sie sich wieder ehoben. In [getCityname] hat [getLeadername] wieder einige Krieger um sich versammelt.
#Vandalen (Player 9) vernichtet: 20_5
#Warnen (Player 2) vernichtet: 21_5
#Hermunduren (Player 4) vernichtet: 22_5
#Cherusker (Player 1) vernichtet: 23_5
#Markomannen (Player 3) vernichtet: 24_5
	if iNewOwner in lGerVandalen:
		bMeldung = False
		if iNewOwner == 9 and CvUtil.getScriptData(gc.getMap().plot(0, 1), ["20_5"], "") == "x":
			CvUtil.addScriptData(gc.getMap().plot(0, 1), "20_5", "")
			bMeldung = True
		elif iNewOwner == 2 and CvUtil.getScriptData(gc.getMap().plot(0, 1), ["21_5"], "") == "x":
			CvUtil.addScriptData(gc.getMap().plot(0, 1), "21_5", "")
			bMeldung = True
		elif iNewOwner == 4 and CvUtil.getScriptData(gc.getMap().plot(0, 1), ["22_5"], "") == "x":
			CvUtil.addScriptData(gc.getMap().plot(0, 1), "22_5", "")
			bMeldung = True
		elif iNewOwner == 1 and CvUtil.getScriptData(gc.getMap().plot(0, 1), ["23_5"], "") == "x":
			CvUtil.addScriptData(gc.getMap().plot(0, 1), "23_5", "")
			bMeldung = True
		elif iNewOwner == 3 and CvUtil.getScriptData(gc.getMap().plot(0, 1), ["24_5"], "") == "x":
			CvUtil.addScriptData(gc.getMap().plot(0, 1), "24_5", "")
			bMeldung = True

		if bMeldung:
			if gc.getPlayer(0).isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_EVENT_27_3", (pCity.getName(), gc.getPlayer(iNewOwner).getName())))
				popupInfo.addPopup(0)
			CyCamera().JustLookAtPlot(pCity.plot())


def onFirstContact(argsList):
	iTeamX, iHasMetTeamY = argsList

	# onFirstContact-Events gelten nur für den Goten
	if iTeamX != 0: return
	if not gc.getPlayer(0).isHuman(): return

	lGerVandalen = [1,2,3,4,9]

#[EVENT-20.1] Wenn Kontakt zum Vandalen (Player 9) entsteht:
#[EVENT-21.1] Wenn Kontakt zum Warnen (Player 2) entsteht:
#[EVENT-22.1] Wenn Kontakt zum Hermunduren (Player4) entsteht:
#[EVENT-23.1] Wenn Kontakt zum Cherusker (Player1) entsteht:
#[EVENT-24.1] Wenn Kontakt zum Markomannen (Player3) entsteht:
	#Erstellen einer aktuellen Punktliste der GerVandanen.
	#[ABFRAGE] Ist iHasMetTeamY Erster? -> DANN (A)
	#[ABFRAGE] Steht iHasMetTeamY im Mittelfeld? -> DANN (B)
	#[ABFRAGE] Ist iHasMetTeamY Letzter? -> DANN (C)
	# Die Hauptstadt [get.Capitalplot] wird aufgedeckt
	if iHasMetTeamY in lGerVandalen:
		iScoreLast = 0
		iScoreBest = 0
		for iPlayer in lGerVandalen:
			if gc.getPlayer(iPlayer).isAlive():
				if iScoreLast == 0 or CyGame().getPlayerScore(iPlayer) < iScoreLast:
					iScoreLast = CyGame().getPlayerScore(iPlayer)
				if CyGame().getPlayerScore(iPlayer) > iScoreBest:
					iScoreBest = CyGame().getPlayerScore(iPlayer)

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Punkte Team",CyGame().getPlayerScore(iHasMetTeamY))), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Punkte Bester",iScoreBest)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Punkte Letzter",iScoreLast)), None, 2, None, ColorTypes(10), 0, 0, False, False)

		if iHasMetTeamY == 9:
			if iScoreBest == CyGame().getPlayerScore(iHasMetTeamY):
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_VANDALEN_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
			elif iScoreLast == CyGame().getPlayerScore(iHasMetTeamY):
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_VANDALEN_3", (gc.getPlayer(iHasMetTeamY).getName(), ))
			else:
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_VANDALEN_2", (gc.getPlayer(iHasMetTeamY).getName(), ))
		elif iHasMetTeamY == 2:
			if iScoreBest == CyGame().getPlayerScore(iHasMetTeamY):
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_WARNEN_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
			elif iScoreLast == CyGame().getPlayerScore(iHasMetTeamY):
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_WARNEN_3", (gc.getPlayer(iHasMetTeamY).getName(), ))
			else:
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_WARNEN_2", (gc.getPlayer(iHasMetTeamY).getName(), ))
		elif iHasMetTeamY == 4:
			if iScoreBest == CyGame().getPlayerScore(iHasMetTeamY):
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_HERMUN_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
			elif iScoreLast == CyGame().getPlayerScore(iHasMetTeamY):
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_HERMUN_3", (gc.getPlayer(iHasMetTeamY).getName(), ))
			else:
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_HERMUN_2", (gc.getPlayer(iHasMetTeamY).getName(), ))
		elif iHasMetTeamY == 1:
			if iScoreBest == CyGame().getPlayerScore(iHasMetTeamY):
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_CHERUSK_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
			elif iScoreLast == CyGame().getPlayerScore(iHasMetTeamY):
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_CHERUSK_3", (gc.getPlayer(iHasMetTeamY).getName(), ))
			else:
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_CHERUSK_2", (gc.getPlayer(iHasMetTeamY).getName(), ))
		elif iHasMetTeamY == 3:
			if iScoreBest == CyGame().getPlayerScore(iHasMetTeamY):
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_MARKO_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
			elif iScoreLast == CyGame().getPlayerScore(iHasMetTeamY):
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_MARKO_3", (gc.getPlayer(iHasMetTeamY).getName(), ))
			else:
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_MARKO_2", (gc.getPlayer(iHasMetTeamY).getName(), ))

		# PopUp
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(szText)
		popupInfo.addPopup(0)

		# Show Capital
		pCity = gc.getPlayer(iHasMetTeamY).getCapitalCity()
		if not pCity.isNone():
			doRevealPlot(0, pCity.plot(), True)

#[EVENT-25.1] - onFirstContact; Wenn Kontakt zum Friesen (Player21) entsteht:
	elif iHasMetTeamY == 21:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_FRIESEN", (gc.getPlayer(iHasMetTeamY).getName(), )))
		popupInfo.addPopup(0)

#[EVENT-26.1] - onFirstContact; Wenn Kontakt zum Raeter (Player22) entsteht:
	elif iHasMetTeamY == 22:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_RAETER", (gc.getPlayer(iHasMetTeamY).getName(), )))
		popupInfo.addPopup(0)

#[EVENT-30.1] - onFirstContact; Wenn Kontakt zum Arverner (Player 6) entsteht:
#[ABFRAGE] Hat der Arverner Frieden mit Rom (Player 14)? -> DANN (A)
#[ABFRAGE] Hat der Arverner Krieg mit Rom (Player 14)? -> DANN (B)
	elif iHasMetTeamY == 6:
		if not gc.getTeam(gc.getPlayer(6).getTeam()).isAtWar(gc.getPlayer(14).getTeam()):
			szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_ARVERNER1", (gc.getPlayer(iHasMetTeamY).getName(), ))
		else:
			szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_ARVERNER2", (gc.getPlayer(iHasMetTeamY).getName(), gc.getPlayer(14).getName()))
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(szText)
		popupInfo.addPopup(0)

#[EVENT-31.1] - onFirstContact; Wenn Kontakt zum Daker (Player 10) entsteht:
	elif iHasMetTeamY == 10:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_DAKER", (gc.getPlayer(iHasMetTeamY).getCivilizationDescriptionKey(), )))
		popupInfo.addPopup(0)

#[EVENT-40.2] - onFirstContact; Wenn Kontakt zum Römer (Player 14) entsteht:
#Die Hauptstadt der Römer [get.Capitalplot] wird 1x aufgedeckt
	elif iHasMetTeamY == 14:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_ROME", (gc.getPlayer(iHasMetTeamY).getName(), )))
		popupInfo.addPopup(0)

		pCity = gc.getPlayer(iHasMetTeamY).getCapitalCity()
		if not pCity.isNone():
			doRevealPlot(0, pCity.plot(), True)




def onCombatResult(pWinner, pLoser):
	iWinner = pWinner.getOwner()
	iLoser = pLoser.getOwner()

	if pLoser.getScriptData():
		#[EVENT-10.2] Wenn der Älteste stirbt:
		#"The Elder" ist Stammesfürst mit General der Alten Goten (Player 20) in Hagelsberg. Wenn der besiegt ist:
		#[ABFRAGE] Hat der Spieler ihn besiegt? -> DANN (A)
		#[ABFRAGE] Ist er irgendwo anders gestorben? -> DANN (B)
		#(A)
		#Der Älteste ist besiegt! Damit hat [get.LeadernamePlayer20] seine besten Kämpfer verloren.
		#Und wir konnten seinen engsten Vertrauten festnehmen. Oswald ist ein viel gereister Mann, der sich in den Wäldern bestens auskennt. Und er ist weise genug, die richtige Entscheidung zu treffen. Bevor er am Galgenbaum endet, kniet er nieder und schwört euch die ewige Treue.
		#Ihr nehmt ihn gerne auf, von seinem Wissen und seinen Fähigkeiten können wir nur profitieren.
		#<IHR ERHALTET 1 GROSSER SPION> "Oswald"
		#KAMERA ZOOM AUF DEN ORT DES KAMPFES
		#Großer Spion "Oswald" wird erstellt. Er bekommt die Beförderung Wald III (doppelte Fortbewegung im Wald)
		#(B)
		#Der Älteste ist gefallen! Wo auch immer er sich versteckt hatte, sein Schicksal hat ihn eingeholt!
		if iLoser == 20 and CvUtil.getScriptData(pLoser, ["t"]) == "TheElder":
			#[ABFRAGE] Hat der Spieler ihn besiegt? -> DANN (A)
			if iWinner == 0:
				pNewUnit = gc.getPlayer(iWinner).initUnit(gc.getInfoTypeForString("UNIT_GREAT_SPY"), pWinner.getX(), pWinner.getY(), UnitAITypes.UNITAI_SPY, DirectionTypes.DIRECTION_SOUTH)
				pNewUnit.setName("Oswald")
				pNewUnit.setScriptData("Oswald")
				pNewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMMANDO"), True)
				#CyCamera().LookAtUnit(pNewUnit)

				if gc.getPlayer(iWinner).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_THE_ELDER", (gc.getPlayer(iLoser).getName(), )))
					popupInfo.addPopup(iWinner)

			#[ABFRAGE] Ist er irgendwo anders gestorben? -> DANN (B)
			else:
				if gc.getPlayer(0).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_THE_ELDER_2", (gc.getPlayer(iLoser).getName(), )))
					popupInfo.addPopup(0)

			# keine weiteren PAE features nach dem Kampf (zB Flucht)
			return True

		#[EVENT-11.1] - onCombatResult; Wenn Alarich stirbt:
		#Die Startarmee des Spielers wird von Stammesfürst mit General "Alarich" angeführt. Nach dessen Tod gibt es einen neuen Leader der Goten (Athaulf)
		#[ABFRAGE] Ist pPlot.setScriptData() für EVENT-12.2 gesetzt? -> DANN -1 Zufriedenheit im Palast
		#[ABFRAGE] Gibt es schon eine Hauptstadt? -> DANN
		#In [get.Capitalname] wird ein Obelisk gesetzt
		if iLoser == 0 and CvUtil.getScriptData(pLoser, ["t"]) == "Alarich":
			#Die Startarmee des Spielers wird von Stammesfürst mit General "Alarich" angeführt.
			#Nach dessen Tod gibt es einen neuen Leader der Goten (X oder Y)
			#<[get.Leadername] ÜBERNIMMT DIE FÜHRUNG DER GOTEN>

			#Der Nachfolger von Alarich I. als König der Westgoten war sein Schwager Ataulf.
			iLeader = gc.getInfoTypeForString("LEADER_TEUTOBOD")
			gc.getPlayer(iLoser).changeLeader(iLeader) # change to XML leader
			gc.getPlayer(iLoser).setName("Ataulf") # Leader's name


			#[ABFRAGE] Gibt es schon eine Hauptstadt? -> DANN
			#<DIE STELE DES ALARICH WIRD IN [get.Capitalname] ERRICHTET> (Obelisk)
			pCity = gc.getPlayer(iLoser).getCapitalCity()
			if pCity.isNone():
				szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ALARICH_HEAD", ("", ))
				szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ALARICH_BODY_2", ())
				PopUpDDS("Art/Scenarios/WegDerGoten/WDG07.dds",szTextHead,szTextBody,"RIGHT")
			else:

				#[ABFRAGE] Ist pPlot.setScriptData() für EVENT-12.2 gesetzt? -> DANN -1 Zufriedenheit im Palast
				iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["12_2"], "")
				if iCheck == "x":
					iBuildingClass = gc.getInfoTypeForString("BUILDINGCLASS_PALACE")
					iBuildingHappiness = pCity.getBuildingHappyChange(iBuildingClass) - 1
					pCity.setBuildingHappyChange(iBuildingClass, iBuildingHappiness)

				#Der Herr über das Gotenreich ist gefallen! Ihr seid tot!
				#Zeit für Trauer bleibt jedoch nicht viel, das Leben muss weitergehen. Zu euren Ehren wird in [get.capitalname] ein Monument errichtet, wie es noch keins zuvor gab. Ein riesiger gehauener Stein, der mit einer Inschrift an Alarich den Goten erinnert.
				pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_OBELISK"), 1)
				szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ALARICH_HEAD", ("", ))
				szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ALARICH_BODY", (pCity.getName(), ))
				PopUpDDS("Art/Scenarios/WegDerGoten/WDG07.dds",szTextHead,szTextBody,"RIGHT")

			return True

		#[EVENT-23.6] - onCombatResult; Wenn General "Arminius" stirbt:
		#"Arminius" ist Stammesfürst mit General aus EVENT-23.3, der für den Spieler kämpft. Wenn der stirbt -> DANN
		#Der Cherusker bekommt einen neuen Leader. Es bleibt Arminius, nur der Name ändert sich zu "Segestes der Cherusker". "Statthalter von x" ist zu sperrig
		#[ABFRAGE] Ist der Cherusker (Player 1) noch Vasall des Spielers? -> DANN
		#[ZUFALLSEVENT]
		#10% - Der Cherusker sagt sich als Vasall los -> DANN (A)
		#30% - Ein Aufstand in der Hauptstadt des Cheruskers über 5-10 Runden -> DANN (B)
		#60% - Keine Auswirkung -> DANN (C)
		if iLoser == 0 and CvUtil.getScriptData(pLoser, ["t"]) == "Arminius":
			if CvUtil.getScriptData(gc.getMap().plot(0, 1), ["23_3"], "") == "x":
				pCity = gc.getPlayer(1).getCapitalCity()
				#szLeader = CyTranslator().getText("TXT_KEY_LEADER_PRINCE_OF", (pCity.getName(), ))
				szLeader = CyTranslator().getText("TXT_KEY_LIMES_PERSON12", ("",))
				gc.getPlayer(1).setName(szLeader)

				if gc.getTeam(1).isVassal(gc.getPlayer(0).getTeam()):
					iRand = CvUtil.myRandom(10, "ArminiusDies")
					if iRand == 0:
						szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ARMINIUS_TOT1", (szLeader, szLeader))
						gc.getTeam(1).setVassal(gc.getPlayer(0).getTeam(), False, False)

					elif iRand < 4:
						szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ARMINIUS_TOT2", (pCity.getName(), szLeader))
						iRand = CvUtil.myRandom(6, "ArminiusDiesCityRevolt")
						PAE_City.doCityRevolt(pCity, 5 + iRand)

					else:
						szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ARMINIUS_TOT3", ("", ))

					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(szText)
					popupInfo.addPopup(0)

				return True

	# bUnitDone (weitere PAE onCombatResult features erlaubt)
	return False

def onCityBuilt(pCity):
	iPlayer = pCity.getOwner()
	pPlayer = gc.getPlayer(iPlayer)

#[EVENT-12.1] - onCityBuilt; Wenn der Spieler eine (erste) Stadt mit einem Siedler gründet -> DANN
	#Plot (0,1): pPlot.setScriptData() für EVENT-12.1
	#ZOOM AUF DIE SIEDLUNG
	#Die Siedler bedanken sich.
	#Sie wollen ihre neue Heimat schnell zu einem Dorf erweitern, auf dass es bald zum Glanze des Gotenreiches beitragen möge.
	#Wir könnten Fuhrwerke schicken, die hier Ressourcen verbreiten...
	if iPlayer == 0 and pPlayer.isHuman():
		iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["12_1"], "")
		if iCheck == "":
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_OWN_CITY", ("", )))
			popupInfo.addPopup(iPlayer)
			CvUtil.addScriptData(gc.getMap().plot(0, 1), "12_1", "x")
			#ZOOM AUF DIE SIEDLUNG
			CyCamera().JustLookAtPlot(pCity.plot())
			CyCamera().ZoomIn(0.5)



# wenn man einen Spieler erobert oder vasallisiert: (3x vorhanden: onCityAcquired, onPlayerKilled, onVassalState)
def onVassalState(argsList):
	iMaster, iVassal, bVassal = argsList
	global iChanceGreatSpyOnConquer

	lGerVandalen = [0,1,2,3,4,9]
	lGermanen = [1,2,3,4]

	pMaster = gc.getPlayer(iMaster)
	pVassal = gc.getPlayer(iVassal)

	if iMaster == 0 and bVassal:

		iAnzVassals = 0
		iAlive = 0
		if iVassal in lGermanen:
			for iGermane in lGermanen:
				if gc.getPlayer(iGermane).isAlive():
					if gc.getTeam(iGermane).isVassal(pMaster.getTeam()):
						iAnzVassals += 1
					else:
						iAlive += 1

#____________________(GEÄNDERT) 15.2 und 15.3 zusammengefasst
#[EVENT-15.2.2] – onPlayerVasall & onCityAcquired; Vereinigung der Germanen (Player 1, 2, 3, 4)
#A) Wenn der Spieler einen Germanen als Vasall bekommt
#[ABFRAGE 1] Hat der Spieler damit zwei oder drei Germanen als Vasall? (>1 und <4)
#[ABFRAGE 'UND'] Sind die restlichen Germanen vernichtet? [check.ScriptData() für EVENT-21, 22, 23, und 24.5] -> DANN
#Plot (0,1): ScriptData() für EVENT-15.2
#-> Trostpreis
#[ABFRAGE 2] Hat der Spieler damit alle vier Germanen als Vasall? (=4) -> DANN
#Plot (0,1): ScriptData() für EVENT-15.2
#-> Hauptpreis

#B) Wenn ein Germane vernichtet wird
#[ABFRAGE 1] Gibt es damit weniger als zwei Germanen? (<2) -> DANN
#-> Quest gescheitert
#[ABFRAGE 2] Hat der Spieler alle restlichen Germanen als Vasall > DANN
#Plot (0,1): ScriptData() für EVENT-15.2
#-> Trostpreis

# Trostpreis: 2 Berserker (Stärke 14) werden in der Hauptstadt des Spielers erstellt.
# Hauptpreis: 2 Gefolge (Stärke 16) werden in der Hauptstadt des Spielers erstellt
# Gescheitert: (Platzhalter) Die Verinigung aller Germanen ist gescheitert. Es sind nicht genug Völker übrig, um eine Gemeinschaft zu bilden.

		if iAnzVassals == 4:
			if CvUtil.getScriptData(gc.getMap().plot(0, 1), ["15_2"], "") == "":
				pCity = pMaster.getCapitalCity()
				if not pCity.isNone():
					CvUtil.addScriptData(gc.getMap().plot(0, 1), "15_2", "x")
					pMaster.initUnit(gc.getInfoTypeForString("UNIT_WARBAND"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pMaster.initUnit(gc.getInfoTypeForString("UNIT_WARBAND"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

					szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_15_2_HEAD", ("", ))
					szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_15_2", (pCity.getName(), ))
					PopUpDDS("Art/Scenarios/WegDerGoten/WDG09.dds",szTextHead,szTextBody,"RIGHT")

				#KAMERA ZOOM AUF DIE STADT
				CyCamera().JustLookAtPlot(pCity.plot())

		elif iAnzVassals > 1 and iAlive == 0 and CvUtil.getScriptData(gc.getMap().plot(0, 1), ["15_2"], "") == "":
			pCity = pMaster.getCapitalCity()
			if not pCity.isNone():
				CvUtil.addScriptData(gc.getMap().plot(0, 1), "15_2", "x")
				pMaster.initUnit(gc.getInfoTypeForString("UNIT_BERSERKER_GERMAN"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

				if pMaster.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_15_3", ("",)))
					popupInfo.addPopup(iMaster)

				#KAMERA ZOOM AUF DIE STADT
				CyCamera().JustLookAtPlot(pCity.plot())


#[EVENT-15.1] - onCityAcquired & onVassalState; Wenn der Spieler einen KI-Gegner (nicht MinorCiv) vasallisiert oder vernichtet:
		#Immer, wenn der Spieler eine KI-Gegner vasallisiert oder vernichtet, gibt es eine 33% Chance auf dieses Ereignis -> DANN
		#Plot (0,1): pPlot.setScriptData() für EVENT-15.1
		#1 Großer Spion "Speculatore" wird in der Hauptstadt des neuen Vasallen erstellt. Bei Vernichtung in der letzten eroberten Stadt
		#1 Spion wird in der römischen Hauptstadt erstellt
		if not pVassal.isMinorCiv():
			if CvUtil.getScriptData(gc.getMap().plot(0, 1), ["15_1"], "") == "":
				if CvUtil.myRandom(100, "WDG Great Spy onVassalState") < iChanceGreatSpyOnConquer:

					pCity = pVassal.getCapitalCity()
					if pCity.isNone():
						pCity = pMaster.getCapitalCity()

					if not pCity.isNone():
						CvUtil.addScriptData(gc.getMap().plot(0, 1), "15_1", "x")

						pNewUnit = pMaster.initUnit(gc.getInfoTypeForString("UNIT_GREAT_SPY"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MERCHANT, DirectionTypes.DIRECTION_SOUTH)
						pNewUnit.setName("Speculatore")

						#1 Spion wird in der römischen Hauptstadt erstellt (Rom: 14)
						pCityRome = gc.getPlayer(14).getCapitalCity()
						pMaster.initUnit(gc.getInfoTypeForString("UNIT_SPY"), pCityRome.getX(), pCityRome.getY(), UnitAITypes.UNITAI_SPY, DirectionTypes.DIRECTION_SOUTH)

						#Ihr habt euch als erfolgreicher Feldherr erwiesen und schon so einige Stämme unterworfen! Ein eher unscheinbarer Kerl, der uns schon länger folgt, offenbart sich als Kundschafter aus Rom und bietet seine Dienste an.
						#Er nennt sich selbst Speculatore, hat mit [get.LeadernameRömer] noch eine Rechnung offen und will dabei helfen, eine Macht aufzubauen, die den römischen Legionen gewachsen ist!
						#Ein Komplize des Speculatore ist in [get.CapitalnameRömer] geblieben, um über die Lage vor Ort zu berichten.
						#<IHR ERHALTET 1 GROSSER SPION>
						#<IHR ERHALTET 1 SPION IN [get.CapitalnameRömer]>
						if pMaster.isHuman():
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_SPECULATORE", (gc.getPlayer(14).getName(), pCityRome.getName(), pCityRome.getName())))
							popupInfo.addPopup(iMaster)

	# ---------------------------------------------------------------------------------------

	if bVassal:
		# Vandalen
		if iVassal == 9:
			#[EVENT-20.3] - onPlayerVasall; Wenn der Spieler (Player 0) den Vandalen (Player 9) vasalliert:
			if iMaster == 0:
				if CvUtil.getScriptData(gc.getMap().plot(0, 1), ["20_3"], "") == "":
					CvUtil.addScriptData(gc.getMap().plot(0, 1), "20_3", "x")
					if gc.getPlayer(0).isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_VANDALS", (pVassal.getName(), )))
						popupInfo.addPopup(0)
			#[EVENT-20.4] - onPlayerVasall; Wenn jemand anders als der Spieler den Vandalen (Player 9) vasallisiert:
			#[ABFRAGE] Ist es NICHT der Römer (Player 14)? (Rom wird am Ende [EVENT-40] gesondert behandelt) -> DANN
			elif iMaster != 14 and gc.getPlayer(0).isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_VANDALS2", (pMaster.getName(), )))
				popupInfo.addPopup(0)

		# Warnen
		elif iVassal == 2:
			#[EVENT-21.3] - onPlayerVasall; Wenn der Spieler den Warnen (Player 2) vasallisiert:
			#Plot (0,1): pPlot.addScriptData() für EVENT-21.3
			#NEBEN (nicht in) der Hauptstadt der Warnen werden 2 Teutonen erstellt
			if iMaster == 0:
				if CvUtil.getScriptData(gc.getMap().plot(0, 1), ["21_3"], "") == "":

					pCity = gc.getPlayer(iVassal).getCapitalCity()
					if not pCity.isNone():
						iX = pCity.getX()
						iY = pCity.getY()
						for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
							loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
							if loopPlot and not loopPlot.isNone():
								if not loopPlot.isWater() and not loopPlot.isImpassable() and not loopPlot.isUnit():
									pNewUnit = gc.getPlayer(0).initUnit(gc.getInfoTypeForString("UNIT_TEUTONEN"), loopPlot.getX(), loopPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
									pNewUnit = gc.getPlayer(0).initUnit(gc.getInfoTypeForString("UNIT_TEUTONEN"), loopPlot.getX(), loopPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
									break

						CvUtil.addScriptData(gc.getMap().plot(0, 1), "21_3", "x")

						if gc.getPlayer(0).isHuman():
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_WARNEN", (pVassal.getName(), )))
							popupInfo.addPopup(0)

			#[EVENT-21.4] - onPlayerVasall; Wenn jemand anders als der Spieler den Warnen (Player 2) vasallisiert:
			#[ABFRAGE] Ist es NICHT der Römer (Player 14)? -> DANN
			#[ABFRAGE] Ist es einer der GerVandanen? -> DANN (A)
			#[ABFRAGE] Ist es jemand anders? -> DANN (B)
			elif iMaster != 14 and gc.getPlayer(0).isHuman():
				if iMaster in lGerVandalen:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_WARNEN2", (pMaster.getName(), )))
					popupInfo.addPopup(0)
				else:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_WARNEN3", (pMaster.getName(), )))
					popupInfo.addPopup(0)


		# Hermunduren
		elif iVassal == 4:
			#[EVENT-22.3] - onPlayerVasall; Wenn der Spieler den Hermunduren (Player 4) vasallisiert:
			#Plot (0,1): pPlot.addScriptData() für EVENT-22.3
			#Der Spieler erhält 1000 Geld
			if iMaster == 0:
				if CvUtil.getScriptData(gc.getMap().plot(0, 1), ["22_3"], "") == "":
					CvUtil.addScriptData(gc.getMap().plot(0, 1), "22_3", "x")
					gc.getPlayer(0).changeGold(1000)
					if gc.getPlayer(0).isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_HERMUN", (pVassal.getName(), )))
						popupInfo.addPopup(0)

			#[EVENT-22.4] - onPlayerVasall; Wenn jemand anders als der Spieler den Hermunduren (Player 4) vasallisiert:
			#[ABFRAGE] Ist es NICHT der Römer (Player 14)? -> DANN
			#[ABFRAGE] Ist es einer der GerVandanen? -> DANN (A)
			#[ABFRAGE] Ist es jemand anders? -> DANN (B)
			elif iMaster != 14 and gc.getPlayer(0).isHuman():
				if iMaster in lGerVandalen:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_HERMUN2", (pMaster.getName(), )))
					popupInfo.addPopup(0)
				else:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_HERMUN3", (pMaster.getName(), )))
					popupInfo.addPopup(0)

		# Cherusker
		elif iVassal == 1:
			#[EVENT-23.3] - onPlayerVasall; Wenn der Spieler den Cherusker (Player 1) vasallisiert:
			#Plot (0,1): pPlot.addScriptData() für EVENT-23.3
			#NEBEN (nicht in) der Hauptstadt des Cherusker wird ein Stammesfürst (Stärke 12) mit General "Arminius" erstellt, Arminius bekommt Rhetorik und 1 Stern (Trainiert?)
			if iMaster == 0:
				if CvUtil.getScriptData(gc.getMap().plot(0, 1), ["23_3"], "") == "":

					pCity = gc.getPlayer(iVassal).getCapitalCity()
					if not pCity.isNone():
						iX = pCity.getX()
						iY = pCity.getY()
						for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
							loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
							if loopPlot and not loopPlot.isNone():
								if not loopPlot.isWater() and not loopPlot.isImpassable() and not loopPlot.isUnit():

									pNewUnit = gc.getPlayer(0).initUnit(gc.getInfoTypeForString("UNIT_STAMMESFUERST"), loopPlot.getX(), loopPlot.getY(), UnitAITypes.UNITAI_GENERAL, DirectionTypes.DIRECTION_SOUTH)
									pNewUnit.setName("Arminius")
									pNewUnit.setScriptData("Arminius")
									pNewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER"), True)
									pNewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_RHETORIK"), True)
									pNewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
									break

						CvUtil.addScriptData(gc.getMap().plot(0, 1), "23_3", "x")

						if gc.getPlayer(0).isHuman():
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_CHERUSK", (pVassal.getName(), pCity.getName())))
							popupInfo.addPopup(0)

			#[EVENT-23.4] - onPlayerVasall; Wenn jemand anders als der Spieler den Cherusker (Player 1) vasallisiert:
			#[ABFRAGE] Ist es NICHT der Römer (Player 14)? -> DANN
			#[ABFRAGE] Ist es einer der GerVandanen? -> DANN (A)
			#[ABFRAGE] Ist es jemand anders? -> DANN (B)
			elif iMaster != 14 and gc.getPlayer(0).isHuman():
				if iMaster in lGerVandalen:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_CHERUSK2", (pMaster.getName(), )))
					popupInfo.addPopup(0)
				else:
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_CHERUSK3", (pMaster.getName(), )))
					popupInfo.addPopup(0)

		# Markomannen
		elif iVassal == 3:
			#[EVENT-24.3] - onPlayerVasall; Wenn der Spieler den Markomannen (Player 3) vasallisiert:
			#Plot (0,1): pPlot.addScriptData() für EVENT-24.3
			#NEBEN (nicht in) der Hauptstadt des Markomannen wird ein Legionär erstellt
			#Wenn er ohne Eroberung Vasall wurde, wird der Legionär NEBEN der Hauptstadt des Markomannen erstellt
			if iMaster == 0:
				if CvUtil.getScriptData(gc.getMap().plot(0, 1), ["24_3"], "") == "":

					pCity = gc.getPlayer(iVassal).getCapitalCity()
					if not pCity.isNone():
						iX = pCity.getX()
						iY = pCity.getY()
						for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
							loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
							if loopPlot and not loopPlot.isNone():
								if not loopPlot.isWater() and not loopPlot.isImpassable() and not loopPlot.isUnit():
									pNewUnit = gc.getPlayer(0).initUnit(gc.getInfoTypeForString("UNIT_LEGION2"), loopPlot.getX(), loopPlot.getY(), UnitAITypes.UNITAI_GENERAL, DirectionTypes.DIRECTION_SOUTH)
									pNewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
									pNewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT2"), True)
									break

						CvUtil.addScriptData(gc.getMap().plot(0, 1), "24_3", "x")

						if gc.getPlayer(0).isHuman():
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_MARKO", (pVassal.getName(), pCity.getName())))
							popupInfo.addPopup(0)

			#[EVENT-24.4] - onPlayerVasall; Wenn jemand anders als der Spieler den Markomannen (Player 3) vasallisiert:
			#[ABFRAGE] Ist der Hegemon NICHT der Römer (Player 14)? -> DANN
			elif iMaster != 14 and gc.getPlayer(0).isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_MARKO2", (pMaster.getName(), )))
					popupInfo.addPopup(0)



def onChangeWar(argsList):
	# iTeam declared war on iRivalTeam
	bIsWar, iTeam, iRivalTeam = argsList
	lGerVandalen = [0,1,2,3,4,9]
	lGermanen = [0,1,2,3,4]
	iActivePlayer = gc.getGame().getActivePlayer()

	# wenn Krieg erklärt wird -----
	if bIsWar:
	# -----------------------------

		# Wenn dem Spieler Krieg erklärt wird
		if iRivalTeam == 0 and gc.getPlayer(0).isHuman():
			#[EVENT-20.2] - onChangeWar; Wenn der Vandale (Player 9) dem Spieler Krieg erklärt:
			# Diese hinterhältige Kriegserklärung von [get.Leadername] stellt einen unverzeihlichen Vertrauensbruch dar.
			if iTeam == 9:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_20_2", (gc.getPlayer(iTeam).getName(), )))
				popupInfo.addPopup(0)

			#[EVENT-21.2] - onChangeWar; Wenn der Warne (Player 2) dem Spieler Krieg erklärt:
			#[EVENT-22.2] - onChangeWar; Wenn der Hermundure (Player 4) dem Spieler Krieg erklärt:
			#[EVENT-23.2] - onChangeWar; Wenn der Cherusker (Player 1) dem Spieler Krieg erklärt:
				#Erstellen einer aktuellen Punktliste der GerVandanen.
				#[ABFRAGE] Ist der Warne in der oberen Hälfte (oder in der Mitte)? -> DANN (A)
				#[ABFRAGE] Ist der Warne in der unteren Hälfte? -> DANN (B)
			if iTeam == 2 or iTeam == 4 or iTeam == 1:
				if   iTeam == 2: lGerVandalen = [0,1,3,4,9]
				elif iTeam == 4: lGerVandalen = [0,1,2,3,9]
				elif iTeam == 1: lGerVandalen = [0,2,3,4,9]
				iRang = 1
				iScore = CyGame().getPlayerScore(iTeam)
				for iPlayer in lGerVandalen:
					if gc.getPlayer(iPlayer).isAlive():
						if CyGame().getPlayerScore(iPlayer) > iScore:
							iRang += 1

				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				if iRang <= 3:
					if   iTeam == 2: popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_21_2A", (gc.getPlayer(iTeam).getName(), )))
					elif iTeam == 4: popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_22_2A", (gc.getPlayer(iTeam).getName(), )))
					elif iTeam == 1: popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_23_2A", (gc.getPlayer(iTeam).getName(), )))
				else:
					if   iTeam == 2: popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_21_2B", (gc.getPlayer(iTeam).getName(), )))
					elif iTeam == 4: popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_22_2B", (gc.getPlayer(iTeam).getName(), gc.getPlayer(iTeam).getCapitalCity().getName())))
					elif iTeam == 1: popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_23_2B", (gc.getPlayer(iTeam).getName(), )))
				popupInfo.addPopup(0)

			#[EVENT-24.2] - onChangeWar; Wenn der Markomanne (Player 3) dem Spieler Krieg erklärt:
			if iTeam == 3:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_24_2", (gc.getPlayer(iTeam).getName(), )))
				popupInfo.addPopup(0)


		#[EVENT-27.1] - onChangeWar; Wenn die GerVandanen (P 1, 2, 3, 4, 9) untereinander Krieg erklären:
			#[ABFRAGE] Hat der Spieler Frieden mit beiden Parteien? -> DANN
		if gc.getPlayer(iActivePlayer).isHuman():
			if iTeam != iActivePlayer and iRivalTeam != iActivePlayer:
				if iTeam in lGerVandalen and iRivalTeam in lGerVandalen and not gc.getTeam(gc.getPlayer(iActivePlayer).getTeam()).isAtWar(iTeam) and not gc.getTeam(gc.getPlayer(iActivePlayer).getTeam()).isAtWar(iRivalTeam):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GERVANDALS_DECLARES_WAR_ON_EACH_OTHER", (gc.getPlayer(iTeam).getName(), gc.getPlayer(iRivalTeam).getName())))
					popupInfo.addPopup(iActivePlayer)

		#[EVENT-28.1] Wenn einer der GerVandanen dem Römer (Player 14) Krieg erklärt:
			#[ABFRAGE] Hat der Spieler Frieden mit dem angreifenden GerVandanen [get.Leadername]? -> DANN
			#[get.Leadername] hat Rom den Krieg erklärt! Man muss ihm viel Glück wünschen.
			#Vielleicht können wir ihn unterstützen? Zumindest sollten wir unsere Pläne anpassen.
		if iTeam in lGerVandalen and iTeam != 0 and gc.getPlayer(0).isHuman():
			if iRivalTeam == 14 or gc.getTeam(iRivalTeam).isVassal(gc.getPlayer(14).getTeam()):
				if not gc.getTeam(gc.getPlayer(iActivePlayer).getTeam()).isAtWar(iTeam):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GERVANDALS_DECLARES_WAR_ROME", (gc.getPlayer(iTeam).getName(), )))
					popupInfo.addPopup(iActivePlayer)

		#[EVENT-41.1] - onChangeWar; Wenn der Römer (Player 14) einem der GerVandanen (P 1, 2, 3, 4, 9) Krieg erklärt:
		if iTeam == 14 and iRivalTeam in lGerVandalen and iRivalTeam != 0:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ROME_DECLARES_WAR_GERVANDALS", (gc.getPlayer(iTeam).getName(), gc.getPlayer(iRivalTeam).getName())))
				popupInfo.addPopup(0)


	# wenn Frieden geschlossen wird
	else:
	# -----------------------------
		return


#[EVENT-2.1.1] Christentum Gründung:
#Ab Jahr 5 v.Chr. gibt es eine 5% Chance, dass es entsteht (also innerhalb von 20 Jahren, NICHT Runden!)
#Entstehen soll es dann in Byzanz (80%) oder Rom (20%) -> DANN
#Neu: Der gewürfelte Reliführer erhält 1000 Gold
# check im CvEventManager unter onEndGameTurn
def setChristentum():
		global iChanceSetChristentum

		if CvUtil.myRandom(100, "WDG Christentum") >= iChanceSetChristentum: return

		pCity = None
		iChance = CvUtil.myRandom(10, "WDG Christentum HolyCity")
		if iChance < 2:
			# Rom: x=70,y=11
			pPlot = plotXY(70, 11, 0, 0)
			if pPlot.isCity(): pCity = pPlot.getPlotCity()
		else:
			# Byzanz: x=134,y=7
			pPlot = plotXY(134, 7, 0, 0)
			if pPlot.isCity(): pCity = pPlot.getPlotCity()

		# 1. Heilige Stadt setzen
		if pCity is not None:
				gc.getGame().setHolyCity(gc.getInfoTypeForString("RELIGION_CHRISTIANITY"), pCity, True)
				gc.getPlayer(pCity.getOwner()).changeGold(1000)

				# Es gibt Gerüchte, dass in [get.cityname] ein Kind geboren- und damit eine alte Prophezeiung erfüllt wurde... 
				# Es soll keinen sterblichen Vater haben, sondern von einem Gott gezeugt sein!
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CHRIST_SET", (pCity.getName(), ))
				PopUpDDS("Art/Scenarios/WegDerGoten/WDG03.dds","",szText,"RIGHT")

				# 2. Religion den Barbaren zukommen (sonst kommt Religionswahl bei Theologie)
				pBarbTeam = gc.getTeam(gc.getPlayer(gc.getBARBARIAN_PLAYER()).getTeam())
				pBarbTeam.setHasTech(gc.getInfoTypeForString("TECH_THEOLOGY"), True, gc.getBARBARIAN_PLAYER(), 0, 0)

				# 3. globale Variable bChristentum auf true setzen
				PAE_Christen.init()



#[EVENT-2.2] Christentum verbreitet sich:
#Ab Gründung gibt es eine 2% Chance pro Jahr, dass die Verbreitung beginnt -> DANN
def doSpreadReligion():
		global iChanceSpreadChristentum

		# [EVENT-2.2] Startsignal nur einmal, danach normale PAE-Verbreitung
		if CvUtil.getScriptData(gc.getMap().plot(0, 1), ["2_2"], "") != "":
			PAE_Christen.doSpreadReligion()
			return

		if CvUtil.myRandom(100, "WDG Christentum Verbreitung") < iChanceSpreadChristentum:

			iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")
			iChristentum = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
			iIslam = gc.getInfoTypeForString("RELIGION_ISLAM")
			iReligion = iChristentum

			if gc.getGame().isReligionFounded(iReligion):

				# Stadt suchen, die diese Religion hat
				lCities = []
				pCapitalCity = None
				iNumPlayers = gc.getMAX_PLAYERS()
				for i in range(iNumPlayers):
					loopPlayer = gc.getPlayer(i)
					if loopPlayer.isAlive():
						for loopCity in CvUtil.getCities(loopPlayer):
							if loopCity is not None and not loopCity.isNone():
								if loopCity.isHasReligion(iReligion):
									lCities.append(loopCity)

				if len(lCities):
					pCity = lCities[CvUtil.myRandom(len(lCities), "doSpreadReligion_RandomCity")]
					if pCity is None or pCity.isNone(): return

					iX = pCity.getX()
					iY = pCity.getY()

					lCities = []
					iRange = 20
					iCityCheck = 0
					for i in range(-iRange, iRange+1):
						for j in range(-iRange, iRange+1):
							loopPlot = plotXY(iX, iY, i, j)
							if loopPlot.isCity():
								loopCity = loopPlot.getPlotCity()
								if loopCity.isConnectedTo(pCity) and not loopCity.isHasReligion(iReligion):
									if loopCity.isCapital() or loopCity.isHasBuilding(iBuilding):
										pCapitalCity = loopCity
									elif not loopCity.isHasReligion(iIslam):
										lCities.append(loopCity)

					# Christen auch über Handelswege verbreiten
					# ausser es wurde eine wichtige Stadt gefunden
					if pCapitalCity is None:
							iTradeRoutes = pCity.getTradeRoutes()
							for i in range(iTradeRoutes):
								loopCity = pCity.getTradeCity(i)
								if loopCity.isCapital() or loopCity.isHasBuilding(iBuilding):
									pCapitalCity = loopCity
									break
								elif not loopCity.isHasReligion(iReligion) and not loopCity.isHasReligion(iIslam):
									lCities.append(loopCity)

					# gefundene Hauptstadt immer konvertieren
					if not pCapitalCity is None:
						pCity = pCapitalCity

					elif len(lCities):
						iRand = CvUtil.myRandom(len(lCities), "doSpreadReligionChooseCity")
						pCity = lCities[iRand]
					else:
						return

					pCity.setHasReligion(iReligion, 1, 1, 0)

					# Der neue Glaube, der vor Jahren in [get.cityname] begründet wurde, breitet sich weiter aus. 
					# Die Anhänger nennen sich Christen und sollen keine anderen Götter neben ihrem eigenen dulden...
					# Obwohl ihr Prophet am Kreuz gestorben ist, behaupten sie, er wandle dennoch unter ihnen.
					szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CHRIST_SPREAD", (gc.getGame().getHolyCity(iReligion).getName(), ))
					PopUpDDS("Art/Scenarios/WegDerGoten/WDG04.dds","",szText,"RIGHT")
					CvUtil.addScriptData(gc.getMap().plot(0, 1), "2_2", "x")


def onCityGrowth(pCity,iPlayer):
	pPlayer = gc.getPlayer(iPlayer)

#[EVENT-12.2] - onCityGrowth; Wenn der Spieler mehr als 2 Städte mit Stadtstatus (Größe 6) hat:
	#[ABFRAGE] Lebt Alarich noch? -> DANN
	#Plot (0,1): pPlot.setScriptData() für EVENT-12.2
	#+1 Zufriedenheit im Palast
	iBuilding = gc.getInfoTypeForString("BUILDING_STADT")
	if iPlayer == 0 and pPlayer.countNumBuildings(iBuilding) > 2:

		iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["12_2"], "")
		if iCheck == "":

			#[ABFRAGE] Lebt Alarich noch? -> DANN
			#iPromoLeader = gc.getInfoTypeForString("PROMOTION_LEADER")
			for pLoopUnit in PyPlayer(iPlayer).getUnitList():
				if not pLoopUnit.isNone():
					if CvUtil.getScriptData(pLoopUnit, ["t"]) == "Alarich":

						#+1 Zufriedenheit im Palast
						pCity = pPlayer.getCapitalCity()
						if not pCity.isNone():
							iBuildingClass = gc.getInfoTypeForString("BUILDINGCLASS_PALACE")
							iBuildingHappiness = pCity.getBuildingHappyChange(iBuildingClass) + 1
							pCity.setBuildingHappyChange(iBuildingClass, iBuildingHappiness)

							if pPlayer.isHuman():
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GOTEN_3POP6", ("", )))
								popupInfo.addPopup(iPlayer)
						CvUtil.addScriptData(gc.getMap().plot(0, 1), "12_2", "x")
						break



#[EVENT-12.3] in Event 12.4 integriert



def onBuildingBuilt(pCity, iPlayer, iBuildingType):
	pPlayer = gc.getPlayer(iPlayer)

#[EVENT-12.4] - onBuildingBuilt; Wenn der Spieler einen ersten Provinzpalast gebaut hat -> DANN
	#Plot (0,1): pPlot.setScriptData() für EVENT-12.4
	#KAMERA ZOOM AUF DIE STADT
	#1 Gaufürst wird in der Stadt erstellt (Auch wenn man schon einen hat). Der Gaufürst bekommt 1 Stern (Trainiert?)
	if iPlayer == 0 and pPlayer.isHuman() and iBuildingType == gc.getInfoTypeForString("BUILDING_PROVINZPALAST"):
		iCheck = CvUtil.getScriptData(gc.getMap().plot(0, 1), ["12_4"], "")
		if iCheck == "":

			pNewUnit = pPlayer.initUnit(gc.getInfoTypeForString("UNIT_STATTHALTER_NORTH"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			pNewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)

			CvUtil.addScriptData(gc.getMap().plot(0, 1), "12_4", "x")

			#KAMERA ZOOM AUF DIE STADT
			CyCamera().JustLookAtPlot(pCity.plot())

			#In [get.cityname] wurde ein Provinzpalast fertiggestellt...
			#<IHR ERHALTET 1 GAUFÜRST>
			pCapital = pPlayer.getCapitalCity()
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GOTEN_ERSTERPROVINZPALAST", (pCity.getName(),pCapital.getName())))
			popupInfo.addPopup(iPlayer)


def doRevealPlot(iTeam, pPlot, bZoom):
	iX = pPlot.getX()
	iY = pPlot.getY()
	for x in range(-1, 2):
		for y in range(-1, 2):
			loopPlot = plotXY(iX, iY, x, y)
			if loopPlot and not loopPlot.isNone():
				loopPlot.setRevealed(iTeam, True, False, -1)
	if bZoom:
		CyCamera().JustLookAtPlot(pPlot)
		#CyCamera().ZoomIn(0.5)


# PopUps mit dds-Bild
def PopUpDDS(ddsPIC, txtHEADER, txtBODY, alignment):
	screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
	if alignment == "CENTER":
		iX = screen.getXResolution() / 2 - 200
		iY = 40
	elif alignment == "LEFT":
		iX = 90
		iY = 90
	else: # (RIGHT)
		iX = screen.getXResolution() - 456
		iY = 90
	popupDDS = PyPopup.PyPopup(4000, EventContextTypes.EVENTCONTEXT_ALL) # 4000 = PopUpID
	#popupDDS.setSize(400,400) # (INT iXS, INT iYS) geht net
	popupDDS.setPosition(iX,iY)
	popupDDS.setHeaderString(txtHEADER)
	popupDDS.addDDS(ddsPIC, 0, 0, 256, 256) # (dds, x, y, width: 360 max, height)
	popupDDS.setBodyString(txtBODY)
	popupDDS.launch()
