# Christian features and events

# Imports
from CvPythonExtensions import (CyGlobalContext, CyInterface, plotXY, CyPopupInfo, ButtonPopupTypes,
											CyTranslator, ColorTypes, isWorldWonderClass,
											isTeamWonderClass, isNationalWonderClass)
# import CvEventInterface
import CvUtil
import PAE_Lists as L
import PAE_Unit

# Defines
gc = CyGlobalContext()

# Globals
bChristentum = False


def init():
		global bChristentum
		bChristentum = gc.getGame().isReligionFounded(gc.getInfoTypeForString("RELIGION_CHRISTIANITY"))


def setHolyCity():
		global bChristentum
		# Stadt finden
		pCity = None
		iJudentum = gc.getInfoTypeForString("RELIGION_JUDAISM")
		# Prio1: Heilige Stadt des Judentums
		if gc.getGame().isReligionFounded(iJudentum):
				pCity = gc.getGame().getHolyCity(iJudentum)

		# Prio 2: Juedische Stadt
		if pCity is None:
				lCities = []
				iNumPlayers = gc.getMAX_PLAYERS()
				for i in range(iNumPlayers):
						loopPlayer = gc.getPlayer(i)
						if loopPlayer.isAlive():
								iNumCities = loopPlayer.getNumCities()
								for j in range(iNumCities):
										loopCity = loopPlayer.getCity(j)
										if loopCity is not None and not loopCity.isNone():
												if loopCity.isHasReligion(iJudentum):
														lCities.append(loopCity)

				if lCities:
						pCity = lCities[CvUtil.myRandom(len(lCities), "holy_jew")]

		# Prio3: Hauptstadt mit den meisten Sklaven (ink. Gladiatoren)
		# oder Prio 4: biggest capital city
		if pCity is None:
				# falls es nur Staedte ohne Sklaven gibt
				lCities = []
				# fuer den Vergleich mit Staedten mit Sklaven
				iSumSlaves = 0
				# biggest capital
				iPop = 0

				iNumPlayers = gc.getMAX_PLAYERS()
				for i in range(iNumPlayers):
						loopPlayer = gc.getPlayer(i)
						if loopPlayer.isAlive():
								loopCity = loopPlayer.getCapitalCity()
								if loopCity is not None and not loopCity.isNone():
										iSlaves = (loopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GLADIATOR"))
															 + loopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"))
															 + loopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD"))
															 + loopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD")))

										iCityPop = loopCity.getPopulation()
										if iSlaves == 0:
												if iCityPop > iPop:
														iPop = iCityPop
														lCities = []
														lCities.append(loopCity)
												elif iCityPop == iPop:
														lCities.append(loopCity)
										elif iSumSlaves < iSlaves:
												iSumSlaves = iSlaves
												pCity = loopCity

				if pCity is None:
						if lCities:
								pCity = lCities[CvUtil.myRandom(len(lCities), "holy")]

		# 1. Religion den Barbaren zukommen (sonst kommt Religionswahl bei Theologie)
		pBarbTeam = gc.getTeam(gc.getPlayer(gc.getBARBARIAN_PLAYER()).getTeam())
		pBarbTeam.setHasTech(gc.getInfoTypeForString("TECH_THEOLOGY"), True, gc.getBARBARIAN_PLAYER(), True, False)

		# 2. Heilige Stadt setzen
		if pCity is not None:
				gc.getGame().setHolyCity(gc.getInfoTypeForString("RELIGION_CHRISTIANITY"), pCity, True)
				bChristentum = True

				# Meldung an die Spieler
				for i in range(iNumPlayers):
					loopPlayer = gc.getPlayer(i)
					if loopPlayer.isAlive() and loopPlayer.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						# Ein Kind namens Jesus wurde in %s1 geboren!
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_RELIGION_CHRISTIANITY", (pCity.getName(),"")))
						popupInfo.addPopup(i)

# Eventmanager in onEndGameTurn
def doSpreadReligion():

		iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")
		iChristentum = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
		iIslam = gc.getInfoTypeForString("RELIGION_ISLAM")
		iJudentum = gc.getInfoTypeForString("RELIGION_JUDAISM")
		LReligions = [iChristentum, iIslam, iJudentum]

		for iReligion in LReligions:
			if gc.getGame().isReligionFounded(iReligion):
				#gc.getGame().calculateReligionPercent(iReligion):

				# Chance to spread
				iRand = CvUtil.myRandom(100, "doSpreadReligion")
				# 33 % und später 50%
				if iReligion == iChristentum:
					if canSpreadChristentumOverall() and iRand > 50:
						continue
					elif iRand > 33:
						continue
				# 20%
				elif iReligion == iIslam and iRand > 20:
					continue
				# 10%
				elif iReligion == iJudentum and iRand > 10:
					continue

				# Stadt suchen
				lCities = []
				pCapitalCity = None
				iNumPlayers = gc.getMAX_PLAYERS()
				for i in range(iNumPlayers):
					loopPlayer = gc.getPlayer(i)
					if loopPlayer.isAlive():
						iNumCities = loopPlayer.getNumCities()
						for j in range(iNumCities):
							loopCity = loopPlayer.getCity(j)
							if loopCity is not None and not loopCity.isNone():
								if loopCity.isHasReligion(iReligion):
									lCities.append(loopCity)

				if len(lCities):
					pCity = lCities[CvUtil.myRandom(len(lCities), "doSpreadReligion_RandomCity")]
					if pCity is None or pCity.isNone(): return

					iX = pCity.getX()
					iY = pCity.getY()

					# TEST
					#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",(gc.getReligionInfo(iReligion).getDescription(),iRand)), None, 2, None, ColorTypes(10), 0, 0, False, False)
					#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",(pCity.getName(),iRand)), None, 2, None, ColorTypes(10), 0, 0, False, False)

					lCities = []
					iRange = 8
					iCityCheck = 0
					for i in range(-iRange, iRange+1):
						for j in range(-iRange, iRange+1):
							loopPlot = plotXY(iX, iY, i, j)
							if loopPlot.isCity():
								loopCity = loopPlot.getPlotCity()
								if loopCity.isConnectedTo(pCity) and not loopCity.isHasReligion(iReligion):
									if loopCity.isCapital() or loopCity.isHasBuilding(iBuilding):
										pCapitalCity = loopCity
									elif iReligion == iChristentum and not loopCity.isHasReligion(iIslam) or iReligion == iIslam and not loopCity.isHasReligion(iChristentum) or iReligion == iJudentum:
										lCities.append(loopCity)

					# Christen später auch über Handelswege verbreiten
					# ausser es wurde eine Hauptstadt gefunden
					if iReligion == iChristentum and not pCapitalCity is None:
						if canSpreadChristentumOverall():
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
						convertCity(pCapitalCity, iReligion)

					elif len(lCities):
						iRand = CvUtil.myRandom(len(lCities), "doSpreadReligionChooseCity")
						convertCity(lCities[iRand], iReligion)

						# Christianisiere eine 2. Stadt ab Apostelwanderung 1:3
						if iReligion == iChristentum and canSpreadChristentumOverall() and CvUtil.myRandom(3, "doSpreadReligion") == 1:
							iRand = CvUtil.myRandom(len(lCities), "doSpreadReligionChooseCity")
							convertCity(lCities[iRand], iReligion)

					# TEST
					#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Nachbar-Cities",len(lCities))), None, 2, None, ColorTypes(10), 0, 0, False, False)


def convertCity(pCity, iReligion):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		if pCity.isHasReligion(iReligion): return

		if iReligion == gc.getInfoTypeForString("RELIGION_CHRISTIANITY"):
				# nicht bei Hindu, Buddh
				if not pCity.isHasReligion(gc.getInfoTypeForString("RELIGION_HINDUISM")) and not pCity.isHasReligion(gc.getInfoTypeForString("RELIGION_BUDDHISM")):

						if pCity.isCapital() or pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZPALAST")):
								iChance = 100 # 100%
						elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STADT")):
								if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")):
										iChance = 90
								else:
										iChance = 80
						elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")):
								iChance = 70
						else:
								iChance = 50

						# bei folgenden Civics Chance verringern
						if pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_THEOCRACY")):
								iChance -= 30
						if pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_AMPHIKTIONIE")):
								iChance -= 20

						if CvUtil.myRandom(100, "convertCity") < iChance:
								pCity.setHasReligion(iReligion, 1, 1, 0)
								if pPlayer.isHuman():
										iRand = 1 + CvUtil.myRandom(10, "TXT_KEY_MESSAGE_HERESY_2CHRIST_")
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_HERESY_2CHRIST_"+str(iRand), (pCity.getName(), 0)),
																						 None, 2, "Art/Interface/Buttons/Actions/button_kreuz.dds", ColorTypes(11), pCity.getX(), pCity.getY(), True, True)
								# TEST
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_HERESY_2CHRIST_1", (pCity.getName(), 0)),
								#														 None, 2, "Art/Interface/Buttons/Actions/button_kreuz.dds", ColorTypes(11), pCity.getX(), pCity.getY(), True, True)
								return True

		elif iReligion == gc.getInfoTypeForString("RELIGION_ISLAM") or iReligion == gc.getInfoTypeForString("RELIGION_JUDAISM"):

						if pCity.isCapital():
								iChance = 75 # 75%
						elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STADT")):
								iChance = 50
						else:
								iChance = 25

						# bei folgenden Civics Chance verringern
						if pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_THEOCRACY")):
								iChance -= 25
						if pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_AMPHIKTIONIE")):
								iChance -= 15

						if CvUtil.myRandom(iChance, "convertCity") < iChance:
								pCity.setHasReligion(iReligion, 1, 1, 0)
								if pPlayer.isHuman():
										if iReligion == gc.getInfoTypeForString("RELIGION_ISLAM"):
												szText = "TXT_KEY_MESSAGE_HERESY_2ISLAM"
										elif iReligion == gc.getInfoTypeForString("RELIGION_JUDAISM"):
												szText = "TXT_KEY_MESSAGE_HERESY_2JUDENTUM"
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText(szText, (pCity.getName(), 0)),
																						 None, 2, gc.getReligionInfo(iReligion).getButton(), ColorTypes(11), pCity.getX(), pCity.getY(), True, True)
								return True

		return False


# CvEventManager: onCityDoTurn
def removePagans(pCity):
		if pCity is None or pCity.isNone() or pCity.getName() == "":
			return False

		# 1. Check: 1:30
		if CvUtil.myRandom(30, "removePagans") > 0:
			return False

		# Dogmatische Religionen
		iJudentum = gc.getInfoTypeForString("RELIGION_JUDAISM")
		iChristentum = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
		iIslam = gc.getInfoTypeForString("RELIGION_ISLAM")
		LReligions = [iIslam, iChristentum, iJudentum]
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		lCorp = []
		lReli = []

		for iReligion in LReligions:
			if gc.getGame().isReligionFounded(iReligion):
				if pCity.isHasReligion(iReligion):

					# 2. Check: Chance to abort
					iChance = 0
					iRand = CvUtil.myRandom(10, "removePagans")
					# 20% bzw 40%
					if iReligion == iIslam:
						iChance = 2
						if pPlayer.getStateReligion() == iReligion:
							iChance = 4
					# 10% bzw 40%
					elif iReligion == iChristentum:
						iChance = 1
						if pPlayer.getStateReligion() == iReligion:
							iChance = 4
					# 0% bzw 10%
					elif iReligion == iJudentum:
						iChance = 0
						if pPlayer.getStateReligion() == iReligion:
							iChance = 1

					if iRand > iChance:
						continue

					# Kult
					lCorp = []
					iRange = gc.getNumCorporationInfos()
					for i in range(iRange):
						if pCity.isHasCorporation(i):
							lCorp.append(i)

					# Religion
					lReli = []
					iRange = gc.getNumReligionInfos()
					for i in range(iRange):
						if pCity.isHasReligion(i) and i != iReligion:
							lReli.append(i)

					# Kult oder Religion entfernen
					txtReligionOrKult = ""
					bUndoCorp = False
					if lCorp and lReli:
						if CvUtil.myRandom(2, "undoCorp") == 1:
							bUndoCorp = True

					# Kult
					if lCorp or bUndoCorp:
						iRand = CvUtil.myRandom(len(lCorp), "removePaganCult")
						iRange = gc.getNumBuildingInfos()
						for iBuildingLoop in range(iRange):
							if pCity.isHasBuilding(iBuildingLoop):
								pBuilding = gc.getBuildingInfo(iBuildingLoop)
								if pBuilding.getPrereqCorporation() == lCorp[iRand]:
									# Akademien (Corp7)
									if pBuilding.getType() not in [
										gc.getInfoTypeForString("BUILDING_ACADEMY_2"),
										gc.getInfoTypeForString("BUILDING_ACADEMY_3"),
										gc.getInfoTypeForString("BUILDING_ACADEMY_4")
									]:
										# Wunder sollen nicht betroffen werden
										iBuildingClass = pBuilding.getBuildingClassType()
										if not isWorldWonderClass(iBuildingClass) and not isTeamWonderClass(iBuildingClass) and not isNationalWonderClass(iBuildingClass):
											pCity.setNumRealBuilding(iBuildingLoop, 0)
						pCity.setHasCorporation(lCorp[iRand], 0, 0, 0)
						txtReligionOrKult = gc.getCorporationInfo(lCorp[iRand]).getText()

					# Religion
					elif lReli:
						iRand = CvUtil.myRandom(len(lReli), "removePaganReli")

						# PAE 6.14: Reli der Heiligen Stadt erst zuletzt austreiben
						iReli = lReli[iRand]
						bHolyCity = pCity.isHolyCityByType(iReli)
						bLastCityOfReligion = False
						if bHolyCity:
							bLastCityOfReligion = True
							(loopCity, pIter) = pPlayer.firstCity(False)
							while loopCity:
								if not loopCity.isNone() and loopCity.getID() != pCity.getID() and loopCity.isHasReligion(iReli):
									bLastCityOfReligion = False
									break
								(loopCity, pIter) = pPlayer.nextCity(pIter, False)

						if not bLastCityOfReligion or (bHolyCity and bLastCityOfReligion):
							iRange = gc.getNumBuildingInfos()
							for iBuildingLoop in range(iRange):
								if pCity.isHasBuilding(iBuildingLoop):
									pBuilding = gc.getBuildingInfo(iBuildingLoop)
									if pBuilding.getPrereqReligion() == iReli:
										# Holy City
										if pBuilding.getHolyCity() == -1:
											# Wunder sollen nicht betroffen werden
											iBuildingClass = pBuilding.getBuildingClassType()
											if not isWorldWonderClass(iBuildingClass) and not isTeamWonderClass(iBuildingClass) and not isNationalWonderClass(iBuildingClass):
												pCity.setNumRealBuilding(iBuildingLoop, 0)

							pCity.setHasReligion(iReli, 0, 0, 0)
							txtReligionOrKult = gc.getReligionInfo(iReli).getText()

					# Meldung
					if txtReligionOrKult != "":
						if pPlayer.isHuman():
							iRand = 1 + CvUtil.myRandom(3, "TXT_KEY_MESSAGE_HERESY_CULTS_")
							if iReligion == iJudentum:
								text = "TXT_KEY_MESSAGE_HERESY_CULTS2_"
							elif iReligion == iChristentum:
								text = "TXT_KEY_MESSAGE_HERESY_CULTS_"
							else:
								text = "TXT_KEY_MESSAGE_HERESY_CULTS3_"
							CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText(text+str(iRand), (txtReligionOrKult, pCity.getName())),
							None, 2, gc.getReligionInfo(iReligion).getButton(), ColorTypes(11), pCity.getX(), pCity.getY(), True, True)
							# "Art/Interface/Buttons/Actions/button_kreuz.dds"
						return True

					# danach pagane Gebäude zerstören (wenn Relis und Kulte weg sind)
					LBuildings = [
						gc.getInfoTypeForString("BUILDING_ANCIENT_OBSERVATORY"),
						gc.getInfoTypeForString("BUILDING_NUBIAN_PYRAMID"),
						gc.getInfoTypeForString("BUILDING_STEINKREIS"),
						gc.getInfoTypeForString("BUILDING_LIBRARY"),
						gc.getInfoTypeForString("BUILDING_SCHULE"),
						gc.getInfoTypeForString("BUILDING_GYMNASION"),
						gc.getInfoTypeForString("BUILDING_ORACLE2"),
						gc.getInfoTypeForString("BUILDING_HOSPITAL_ROME"),
						gc.getInfoTypeForString("BUILDING_GLADIATORENSCHULE"),
						gc.getInfoTypeForString("BUILDING_CORPORATION_1"),
						gc.getInfoTypeForString("BUILDING_CORPORATION_2"),
						gc.getInfoTypeForString("BUILDING_CORPORATION_3"),
						gc.getInfoTypeForString("BUILDING_CORPORATION_4"),
						gc.getInfoTypeForString("BUILDING_CORPORATION_5"),
						gc.getInfoTypeForString("BUILDING_CORPORATION_6"),
						gc.getInfoTypeForString("BUILDING_CORPORATION_7"),
						gc.getInfoTypeForString("BUILDING_CORPORATION_8"),
						gc.getInfoTypeForString("BUILDING_CORPORATION_9"),
						gc.getInfoTypeForString("BUILDING_CORP1"),
						gc.getInfoTypeForString("BUILDING_CORP3"),
						gc.getInfoTypeForString("BUILDING_CORP5"),
						gc.getInfoTypeForString("BUILDING_CORP6"),
						gc.getInfoTypeForString("BUILDING_CORP7"),
						gc.getInfoTypeForString("BUILDING_THEATER"),
						gc.getInfoTypeForString("BUILDING_GREEK_ODEON"),
						gc.getInfoTypeForString("BUILDING_ACADEMY_1"),
						gc.getInfoTypeForString("BUILDING_ACADEMY_2"),
						gc.getInfoTypeForString("BUILDING_ACADEMY_3"),
						gc.getInfoTypeForString("BUILDING_ACADEMY_4"),
						gc.getInfoTypeForString("BUILDING_ACADEMY_5"),
						gc.getInfoTypeForString("BUILDING_ACADEMY_6"),
						gc.getInfoTypeForString("BUILDING_BADEHAUS"),
						gc.getInfoTypeForString("BUILDING_THERME"),
						gc.getInfoTypeForString("BUILDING_ASKLEPIEION"),
						gc.getInfoTypeForString("BUILDING_DAMPFBAD"),
						gc.getInfoTypeForString("BUILDING_SAUNA"),
						gc.getInfoTypeForString("BUILDING_NUBIAN_DEFFUFA"),
						gc.getInfoTypeForString("BUILDING_NYMPHAEUM"),
						gc.getInfoTypeForString("BUILDING_GARDEN"),
						gc.getInfoTypeForString("BUILDING_HERBARY")
					]
					for iBuilding in LBuildings:
						if gc.getBuildingInfo(iBuilding) is not None:
							if pCity.isHasBuilding(iBuilding):

								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Pagan Building",iBuilding)), None, 2, None, ColorTypes(10), 0, 0, False, False)
								CvUtil.pyPrint ("Pagan building removed: " + gc.getBuildingInfo(iBuilding).getDescription() + " (ID:" + str(iBuilding) +  ") " + pCity.getName() + " X"+str(pCity.getX())+" Y"+str(pCity.getY()))

								pCity.setNumRealBuilding(iBuilding, 0)

								if pPlayer.isHuman():
									# Religiöse Fanatiker haben in %s1 ein Gebäude zerstört: %s2
									# gc.getReligionInfo(iReligion).getButton()
									iRand = 1 + CvUtil.myRandom(7, "TXT_KEY_MESSAGE_HERESY_BUILDINGS_")
									CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_HERESY_BUILDINGS_" + str(iRand), (pCity.getName(),gc.getBuildingInfo(iBuilding).getDescription())),
									None, 2, gc.getBuildingInfo(iBuilding).getButton(), ColorTypes(11), pCity.getX(), pCity.getY(), True, True)
								return True

		return False


# CvEventManager: onCityDoTurn
def doReligionsKonflikt(pCity):

		# Erst ab Schwierigkeitsgrad > 3
		if gc.getGame().getHandicapType() <= 3:
			return False

		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())

		if pTeam.isHasTech(gc.getInfoTypeForString("TECH_HERESY")): iChance = 6
		else: iChance = 2

		# Chance to abort
		if CvUtil.myRandom(100, "ReligionsKonflikt") >= iChance:
			return False

		# 2%: Poly Reli als Staatsreli, aber kein aktiver Krieg
		# BTS Event System: EVENTTRIGGER_NO_WAR (aktiv)


		# Stadt hat mindestens 2 verschiedene Relis (Staatsreligion ausgenommen)
		iStateReligion = pPlayer.getStateReligion()
		# Konflikt gibt es nicht, wenn in einer Stadt nur eine Religion existiert (Staatsreligion ist egal)
		# Konflikt gibt es ab 2 verschiedenen Religionen
		iKonflikt = 2
		LOtherReligions = []
		for i in range(gc.getNumReligionInfos()):
			if pCity.isHasReligion(i):
				# wenn die Staatsreligion in der Stadt ist, dann besteht der Konflikt schon bei 1 fremden Religion
				# die Staatsreligion soll nicht in der LOtherReligions gelistet sein, denn das sind die Opfer
				# (vor der Spätantike werden dies monotheistische Religionen sein)
				if i == iStateReligion:
					iKonflikt = 1
				else:
					LOtherReligions.append(i)

		# größere Städte dürfen 2 Religionen gleichzeitig haben
		if pCity.getPopulation() > 5: iKonflikt += 1

		if len(LOtherReligions) >= iKonflikt:

			# Religion auswählen
			i = CvUtil.myRandom(len(LOtherReligions), "ReligionsKonflikt4: LOtherReligions")
			iReligion = LOtherReligions[i]

			#pCity.changeOccupationTimer(1)

			# Einheiten verletzen und immobile setzen
			pPlot = pCity.plot()
			iRange = pPlot.getNumUnits()
			for iUnit in range(iRange):
				pLoopUnit = pPlot.getUnit(iUnit)
				if pLoopUnit:
					if pLoopUnit.getDamage() < 30:
						pLoopUnit.setDamage(15 + CvUtil.myRandom(25, "removePaganReli"), -1)
					pLoopUnit.setImmobileTimer(1)

			if pPlayer.isHuman():
				CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIONSKONFLIKT_1", (pCity.getName(),)),
				None, 2, "Art/Interface/Buttons/General/button_icon_angry.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

			# 1:3 Der Tempel wird zerstört
			bTempel = False
			if CvUtil.myRandom(3, "ReligionsKonflikt1") == 1:
				iRange = gc.getNumBuildingInfos()
				for iBuildingLoop in range(iRange):
					if pCity.isHasBuilding(iBuildingLoop):
						pBuilding = gc.getBuildingInfo(iBuildingLoop)
						if pBuilding.getPrereqReligion() == iReligion:
							# Holy City
							if pBuilding.getHolyCity() == -1:
								# Wunder sollen nicht betroffen werden
								iBuildingClass = pBuilding.getBuildingClassType()
								if not isWorldWonderClass(iBuildingClass) and not isTeamWonderClass(iBuildingClass) and not isNationalWonderClass(iBuildingClass):
									pCity.setNumRealBuilding(iBuildingLoop, 0)
									bTempel = True
									if pPlayer.isHuman():
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIONSKONFLIKT_2", (pCity.getName(),gc.getReligionInfo(iReligion).getText())),
										None, 2, gc.getBuildingInfo(iBuildingLoop).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

			# 1:3 Die Stadt wird in Brand gesteckt
			if CvUtil.myRandom(3, "ReligionsKonflikt1") == 1:
					iEvent = gc.getInfoTypeForString("EVENTTRIGGER_CITY_FIRE_CRISIS")
					pPlayer.trigger(iEvent)
					pPlayer.resetEventOccured(iEvent)

			# 1:4 Stadt verliert Pop und ggf Religion
			if CvUtil.myRandom(4, "ReligionsKonflikt3") == 1:
				iPop = int(pCity.getPopulation() / 5)
				pCity.changePopulation(-iPop)

				# Auswanderer erstellen
				pNewUnit = pPlayer.initUnit(gc.getInfoTypeForString("UNIT_EMIGRANT"), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				PAE_Unit.setUnitCulture(pNewUnit)
				CvUtil.addScriptData(pNewUnit, "rel", iReligion)
				pNewUnit.finishMoves()

				if pPlayer.isHuman():
					CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIONSKONFLIKT_3", (pCity.getName(),-iPop)),
					None, 2, "", ColorTypes(7), -1, -1, False, False)

				# 1:4 die andere Religion fliegt raus
				if bTempel and CvUtil.myRandom(4, "ReligionsKonflikt4") == 1:
					pCity.setHasReligion(iReligion, 0, 0, 0)
					if pPlayer.isHuman():
						CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_RELIGIONSKONFLIKT_4", (pCity.getName(),gc.getReligionInfo(iReligion).getText())),
						None, 2, gc.getReligionInfo(iReligion).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
			return True

		return False


# Christen nach 44 Runden überall verbreiten
def canSpreadChristentumOverall():
		iReligion = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
		if gc.getGame().isReligionFounded(iReligion) and gc.getGame().getReligionGameTurnFounded(iReligion) > gc.getGame().getGameTurn() + 44:
				return True
		return False


# Eventmanager onUnitBuilt
# Wenn eine monotheistische Religionen in der Stadt ist, aber diese nicht als Staatsreligion deklariert ist, verweigert die Einheit den Kriegsdienst
# Feature wird mit Toleranzedikt beendet (ausser bei Staatsform Exklusivismus)
def doRefuseUnitBuilt(pCity, pUnit):
		if not pUnit.isMilitaryHappiness():
				return

		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		if not pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_EXCLUSIVE")) and gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_TOLERANZ")):
				return

		LText = []
		bRefuse = False
		for i in L.LMonoReligions:
				if pCity.isHasReligion(i) and pPlayer.getStateReligion() != i:
					bRefuse = True
					if i == gc.getInfoTypeForString("RELIGION_JUDAISM"):
						LText.append("TXT_RELIGION_UNIT_BUILT_INFO_1")
						LText.append("TXT_RELIGION_UNIT_BUILT_INFO_2")
						LText.append("TXT_RELIGION_UNIT_BUILT_INFO_3")
					elif i == gc.getInfoTypeForString("RELIGION_CHRISTIANITY"):
						LText.append("TXT_RELIGION_UNIT_BUILT_INFO_4")
						LText.append("TXT_RELIGION_UNIT_BUILT_INFO_5")
						LText.append("TXT_RELIGION_UNIT_BUILT_INFO_6")
					elif i == gc.getInfoTypeForString("RELIGION_ISLAM"):
						LText.append("TXT_RELIGION_UNIT_BUILT_INFO_7")

		if bRefuse and CvUtil.myRandom(4, "iRandReligionUnitBuiltRefuse") == 1:
				iRandText = CvUtil.myRandom(len(LText), "iRandReligionUnitBuiltRefuseText")
				pUnit.kill(True, -1)
				if pPlayer.isHuman():
						szText = u"%s: " % (pCity.getName()) + CyTranslator().getText(LText[iRandText], ())
						CyInterface().addMessage(iPlayer, True, 10, szText, None, 2, pUnit.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
