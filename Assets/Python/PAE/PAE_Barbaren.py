# Barbarian features and events

# Imports
from CvPythonExtensions import (CyGlobalContext, CyInterface,
																CyTranslator, DirectionTypes,
																ColorTypes, UnitAITypes, CyPopupInfo,
																ButtonPopupTypes, CyAudioGame, plotXY,
																GameOptionTypes)
# import CvEventInterface
import CvUtil
import PyHelpers
import PAE_Lists as L
# Defines
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

bMultiPlayer = False
bGoodyHuts = True
bBarbForts = True
bRageBarbs = False
if gc.getGame().isGameMultiPlayer():
		bMultiPlayer = True
if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_GOODY_HUTS):
		bGoodyHuts = False
if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
		bBarbForts = False
if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_RAGING_BARBARIANS):
		bRageBarbs = True


# leere Festung mit barbarischen Einheiten belegen
def setFortDefence(pPlot):
		# inits
		iBarbPlayer = gc.getBARBARIAN_PLAYER()
		pBarbPlayer = gc.getPlayer(iBarbPlayer)
		# eCiv = gc.getCivilizationInfo(pBarbPlayer.getCivilizationType())

		iPromo = gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS")  # Moves -1
		iPromo2 = gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS2")  # Moves -2

		iAnz = 2
		if bRageBarbs:
				iAnz += 1

		# Einheit herausfinden
		# UNITCLASS_COMPOSITE_ARCHER ist nicht baubar fuer Barbs
		lTempUnit = [
				gc.getInfoTypeForString("UNIT_REFLEX_ARCHER"),
				gc.getInfoTypeForString("UNIT_ARCHER"),
				gc.getInfoTypeForString("UNIT_LIGHT_ARCHER")
		]
		iUnit = -1
		for iUnit in lTempUnit:
				if iUnit != -1 and pBarbPlayer.canTrain(iUnit, 0, 0):
						break
		if iUnit != -1:
				# Einheit setzen / NO_UNITAI vs UNITAI_CITY_DEFENSE
				for _ in range(iAnz):
						pUnit = pBarbPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
						if pUnit.getMoves() > 1:
								pUnit.setHasPromotion(iPromo2, True)
						else:
								pUnit.setHasPromotion(iPromo, True)
						pUnit.finishMoves()

# Barbarische Einheit erzeugen


def createBarbUnit(pPlot):
		if not bBarbForts:
				return

		iBarbPlayer = gc.getBARBARIAN_PLAYER()
		pBarbPlayer = gc.getPlayer(iBarbPlayer)
		iPromo = gc.getInfoTypeForString("PROMOTION_COMBAT1")
		iPromo2 = gc.getInfoTypeForString("PROMOTION_COMBAT2")
		iPromo3 = gc.getInfoTypeForString("PROMOTION_COMBAT3")
		iPromo4 = gc.getInfoTypeForString("PROMOTION_COMBAT4")
		# eCiv = gc.getCivilizationInfo(pBarbPlayer.getCivilizationType())

		iAnz = 1
		if bRageBarbs and CvUtil.myRandom(10, "createBarbUnitWithCombatPromo2") == 1:
				iAnz += 1

		lUnits = []
		# Bogen
		# UNITCLASS_COMPOSITE_ARCHER ist nicht baubar fuer Barbs
		lTempUnit = [
				gc.getInfoTypeForString("UNIT_REFLEX_ARCHER"),
				gc.getInfoTypeForString("UNIT_ARCHER"),
				gc.getInfoTypeForString("UNIT_LIGHT_ARCHER")
		]
		iUnit = -1
		for iUnit in lTempUnit:
				if pBarbPlayer.canTrain(iUnit, 0, 0):
						break
		if iUnit != -1:
				lUnits.append(iUnit)

		# Speer
		lTempUnit = [
				gc.getInfoTypeForString("UNIT_SPEARMAN"),
				gc.getInfoTypeForString("UNIT_LIGHT_SPEARMAN")
		]
		for iUnit in lTempUnit:
				if pBarbPlayer.canTrain(iUnit, 0, 0):
						lUnits.append(iUnit)
						break

		# Axt
		lTempUnit = [
				gc.getInfoTypeForString("UNIT_WURFAXT"),
				gc.getInfoTypeForString("UNIT_AXEMAN2"),
				gc.getInfoTypeForString("UNIT_AXEMAN"),
				gc.getInfoTypeForString("UNIT_AXEWARRIOR")
		]
		for iUnit in lTempUnit:
				if pBarbPlayer.canTrain(iUnit, 0, 0):
						lUnits.append(iUnit)
						break

		# Schwert
		lTempUnit = [
				gc.getInfoTypeForString("UNIT_WARBAND"),
				gc.getInfoTypeForString("UNIT_SWORDSMAN_LATENE"),
				gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"),
				gc.getInfoTypeForString("UNIT_KURZSCHWERT")
		]
		for iUnit in lTempUnit:
				if pBarbPlayer.canTrain(iUnit, 0, 0):
						lUnits.append(iUnit)
						break

		# Reiter
		lTempUnit = [
				gc.getInfoTypeForString("UNIT_CATAPHRACT"),
				gc.getInfoTypeForString("UNIT_HORSEMAN")
		]
		for iUnit in lTempUnit:
				if pBarbPlayer.canTrain(iUnit, 0, 0):
						lUnits.append(iUnit)
						break
		iUnit = gc.getInfoTypeForString("UNIT_HORSE_ARCHER")
		if pBarbPlayer.canTrain(iUnit, 0, 0):
				lUnits.append(iUnit)
		iUnit = gc.getInfoTypeForString("UNIT_CLIBANARII")
		if pBarbPlayer.canTrain(iUnit, 0, 0):
				lUnits.append(iUnit)

		lUnitAIs = [UnitAITypes.UNITAI_ATTACK, UnitAITypes.UNITAI_PILLAGE, UnitAITypes.UNITAI_ATTACK_CITY_LEMMING]

		iAnzUnits = len(lUnits)

		if iAnzUnits == 0:
				if gc.getGame().getCurrentEra() > 3:
						lUnits.append(gc.getInfoTypeForString("UNIT_WARBAND"))
				elif gc.getGame().getCurrentEra() > 2:
						lUnits.append(gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"))
						lUnits.append(gc.getInfoTypeForString("UNIT_SWORDSMAN_LATENE"))
						lUnits.append(gc.getInfoTypeForString("UNIT_SOLDURII"))
				elif gc.getGame().getCurrentEra() > 1:
						lUnits.append(gc.getInfoTypeForString("UNIT_SPEARMAN"))
				elif gc.getGame().getCurrentEra() > 0:
						lUnits.append(gc.getInfoTypeForString("UNIT_LIGHT_SPEARMAN"))

		# Einheit setzen
		bAILemming = False
		if pPlot.getImprovementType() == gc.getInfoTypeForString("IMPROVEMENT_BARBARENFORT"):
				iUnitAI = UnitAITypes.UNITAI_ATTACK_CITY_LEMMING
				bAILemming = True

		for _ in range(iAnz):
				iUnit = lUnits[CvUtil.myRandom(iAnzUnits, "createBarbUnit")]
				if not bAILemming:
					iUnitAI = lUnitAIs[CvUtil.myRandom(len(lUnitAIs), "createBarbUnit_AI")]
				pUnit = pBarbPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), iUnitAI, DirectionTypes.DIRECTION_SOUTH)
				pUnit.setHasPromotion(iPromo, True)
				if bRageBarbs or CvUtil.myRandom(2, "createBarbUnitWithCombatPromo2") == 1:
					pUnit.setHasPromotion(iPromo2, True)
					if bRageBarbs and CvUtil.myRandom(2, "createBarbUnitWithCombatPromo3") == 1:
						pUnit.setHasPromotion(iPromo3, True)
						if CvUtil.myRandom(2, "createBarbUnitWithCombatPromo4") == 1:
							pUnit.setHasPromotion(iPromo4, True)
				pUnit.finishMoves()


# ------ Camp/Kriegslager Einheit setzen (PAE V Patch 4)
def createCampUnit(iPlayer, iGameTurn):
		pPlayer = gc.getPlayer(iPlayer)
		if not pPlayer.isAlive():
				return

		iTeam = pPlayer.getTeam()
		pTeam = gc.getTeam(iTeam)
		# eCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())

		if pPlayer.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_SPECIAL1")) > 0:
				# Terrain
				#eTundra = gc.getInfoTypeForString("TERRAIN_TUNDRA")
				#eGras = gc.getInfoTypeForString("TERRAIN_GRASS")
				#eEbene = gc.getInfoTypeForString("TERRAIN_PLAINS")
				eDesert = gc.getInfoTypeForString("TERRAIN_DESERT")
				# Feature
				#eDichterWald = gc.getInfoTypeForString("FEATURE_DICHTERWALD")

				eCamp = gc.getInfoTypeForString("UNIT_CAMP")

				lCamps = PyPlayer(pPlayer.getID()).getUnitsOfType(eCamp)
				for pUnit in lCamps:
						if pUnit is not None and not pUnit.isNone():
								# pUnit.NotifyEntity(MissionTypes.MISSION_FOUND)
								if pUnit.getFortifyTurns() == 0:
										return

								bCreateUnit = False
								iFortified = CvUtil.getScriptData(pUnit, ["f"], -1)

								if iFortified == -1:
										CvUtil.addScriptData(pUnit, "f", iGameTurn)
								elif (iGameTurn-iFortified) % 5 == 0:
										bCreateUnit = True

								if bCreateUnit:
										pPlot = pUnit.plot()
										lUnits = []

										# Not on hills (for HI)
										if pPlayer.isHuman() and pPlot.isHills():
												CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_HELP_NOCAMPUNIT", ("",)), None, 2,
																								 "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(11), pPlot.getX(), pPlot.getY(), True, True)
												return

										# Desert
										if pPlot.getTerrainType() == eDesert:
												if pPlayer.canTrain(gc.getInfoTypeForString("UNIT_ARABIA_CAMELARCHER"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_ARABIA_CAMELARCHER"))
												if pPlayer.canTrain(gc.getInfoTypeForString("UNIT_CAMEL_CATAPHRACT"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_CAMEL_CATAPHRACT"))

										# Open terrain (primary Mounted only)
										if not lUnits and pPlot.getFeatureType() == -1:
												if pPlayer.canTrain(gc.getInfoTypeForString("UNIT_MONGOL_KESHIK"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_MONGOL_KESHIK"))
												if pPlayer.canTrain(gc.getInfoTypeForString("UNIT_CATAPHRACT"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_CATAPHRACT"))
												if pPlayer.canTrain(gc.getInfoTypeForString("UNIT_HORSE_ARCHER"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_HORSE_ARCHER"))

												if not lUnits and pPlayer.canTrain(gc.getInfoTypeForString("UNIT_HORSEMAN"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_HORSEMAN"))

										# On forests or if no mounted units available/constructable
										if not lUnits:

												if pPlayer.canTrain(gc.getInfoTypeForString("UNIT_REFLEX_ARCHER"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_REFLEX_ARCHER"))
												else:
														lUnits.append(gc.getInfoTypeForString("UNIT_COMPOSITE_ARCHER"))

												if pPlayer.canTrain(gc.getInfoTypeForString("UNIT_SKIRMISHER"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_SKIRMISHER"))

												if pPlayer.canTrain(gc.getInfoTypeForString("UNIT_AXEMAN2"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_AXEMAN2"))

												if pPlayer.canTrain(gc.getInfoTypeForString("UNIT_WARBAND"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_WARBAND"))
												elif pPlayer.canTrain(gc.getInfoTypeForString("UNIT_SWORDSMAN_LATENE"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_SWORDSMAN_LATENE"))
												elif pPlayer.canTrain(gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), 0, 0):
														lUnits.append(gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"))
												else:
														lUnits.append(gc.getInfoTypeForString("UNIT_KURZSCHWERT"))

												# standard unit
												lUnits.append(gc.getInfoTypeForString("UNIT_SPEARMAN"))

												iUnit = -1
												if lUnits:
														iUnit = lUnits[CvUtil.myRandom(len(lUnits), "createCampUnit")]

												# AI: Einheit autom, verkaufen (Soeldnerposten), falls Geldprobleme
												if not pPlayer.isHuman() and (pPlayer.AI_isFinancialTrouble() or pTeam.getAtWarCount(True) == 0):
														pPlayer.changeGold(25)
												elif iUnit != -1:
														# Einheit erstellen
														CvUtil.spawnUnit(iUnit, pPlot, pPlayer)


def doSeevoelker():
		iBarbPlayer = gc.getBARBARIAN_PLAYER()
		pBarbPlayer = gc.getPlayer(iBarbPlayer)

		iUnitTypeShip = gc.getInfoTypeForString("UNIT_SEEVOLK")  # Cargo: 3
		iUnitTypeWarrior1 = gc.getInfoTypeForString("UNIT_SEEVOLK_1")
		iUnitTypeWarrior2 = gc.getInfoTypeForString("UNIT_SEEVOLK_2")
		iUnitTypeWarrior3 = gc.getInfoTypeForString("UNIT_SEEVOLK_3")

		# Handicap: 0 (Settler) - 8 (Deity)
		# Worldsize: 0 (Duell) - 5 (Huge)
		iRange = 1 + gc.getMap().getWorldSize() + gc.getGame().getHandicapType()
		#iRange = max(iRange,8)

		iPlots = gc.getMap().numPlots()
		iLandPlots = gc.getMap().getLandPlots()
		# Wenn es mehr Land als Wasser gibt
		if iLandPlots > iPlots / 2:
				iRange /= 2

		for _ in range(iRange):
				# Wird geaendert zu einem Mittelmeerstreifen: x: 5 bis (X-5), y: 5 bis letztes Drittel von Y
				iMapX = gc.getMap().getGridWidth() - 5
				iMapY = int(gc.getMap().getGridHeight() / 3 * 2)
				iRandX = 5 + CvUtil.myRandom(iMapX, "X")
				iRandY = 5 + CvUtil.myRandom(iMapY, "Y")

				loopPlot = gc.getMap().plot(iRandX, iRandY)
				# Plot soll ein Ozean sein
				terr_ocean = gc.getInfoTypeForString("TERRAIN_OCEAN")
				feat_ice = gc.getInfoTypeForString("FEATURE_ICE")
				iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

				if loopPlot is not None and not loopPlot.isNone():
						if loopPlot.getFeatureType() == iDarkIce:
								continue
						if not loopPlot.isUnit() and not loopPlot.isOwned() and loopPlot.getFeatureType() != feat_ice and loopPlot.getTerrainType() == terr_ocean:
								# Schiffe erstellen
								iAnz = 1
								if bRageBarbs and gc.getGame().getGameTurnYear() > -1000:
										iAnz = 2
								# elif gc.getGame().getGameTurnYear() > -1200:
								#  iAnz = 2

								for _ in range(iAnz):
										CvUtil.spawnUnit(iUnitTypeShip, loopPlot, pBarbPlayer)
										CvUtil.spawnUnit(iUnitTypeWarrior1, loopPlot, pBarbPlayer)
										CvUtil.spawnUnit(iUnitTypeWarrior2, loopPlot, pBarbPlayer)
										CvUtil.spawnUnit(iUnitTypeWarrior3, loopPlot, pBarbPlayer)

		# Meldung PopUp
		if gc.getGame().getGameTurnYear() > -1400 and gc.getGame().getGameTurnYear() < -1380:
				for iPlayer in range(gc.getMAX_PLAYERS()):
						pPlayer = gc.getPlayer(iPlayer)
						if pPlayer.isAlive() and pPlayer.isHuman():
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_SEAPEOPLES", ("", )))
								popupInfo.addPopup(pPlayer.getID())
				CyAudioGame().Play2DSound("AS2D_THEIRDECLAREWAR")


def doHuns():
		iHuns = 0
		iGameTurn = gc.getGame().getGameTurnYear()
		if iGameTurn == 375:
				iHuns = 20
		elif iGameTurn == 380:
				iHuns = 24
		elif iGameTurn == 390:
				iHuns = 26
		elif iGameTurn >= 400 and iGameTurn <= 500 and iGameTurn % 10 == 0:
				iHuns = 18  # Diesen Wert auch unten bei der Meldung angeben!

		if not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START) and gc.getGame().getGameTurnYear() != gc.getDefineINT("START_YEAR"):
				iEra = gc.getGame().getStartEra()
				if iEra > 0:
						iHuns = int(iHuns / iEra)

		if iHuns == 0:
				return

		CivHuns = gc.getInfoTypeForString("CIVILIZATION_HUNNEN")
		bHunsAlive = False

		iMaxPlayers = gc.getMAX_PLAYERS()
		for iPlayer in range(iMaxPlayers):
				pPlayer = gc.getPlayer(iPlayer)
				# Hunnen sollen nur auftauchen, wenn es nicht bereits Hunnen gibt
				if pPlayer.getCivilizationType() == CivHuns and pPlayer.isAlive():
						bHunsAlive = True
						break

		if not bHunsAlive:
				for iPlayer in range(iMaxPlayers):
						pPlayer = gc.getPlayer(iPlayer)

						# Message PopUps
						if iHuns >= 20 and pPlayer.isAlive() and pPlayer.isHuman():
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								if iHuns == 20:
										popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_HUNNEN_1", ("", )))
								elif iHuns == 24:
										CyAudioGame().Play2DSound("AS2D_THEIRDECLAREWAR")
										popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_HUNNEN_2", ("", )))
								else:
										popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_HUNNEN_3", ("", )))
								popupInfo.addPopup(pPlayer.getID())

				iMapW = gc.getMap().getGridWidth()
				iMapH = gc.getMap().getGridHeight()
				iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

				# 15 Versuche einen Plot zu finden
				bPlot = False
				for _ in range(15):
						# Diese Koordinaten entsprechen Nord-Osten
						iRandX = iMapW - 15 + CvUtil.myRandom(15, "W2")
						iRandY = iMapH - 15 + CvUtil.myRandom(15, "H2")
						loopPlot = gc.getMap().plot(iRandX, iRandY)
						if loopPlot is not None and not loopPlot.isNone():
								if loopPlot.getFeatureType() != iDarkIce and not loopPlot.isUnit() and not loopPlot.isWater() and not loopPlot.isOwned() and not loopPlot.isPeak():
										bPlot = True
										break

				if not bPlot:
						return

				# Hunnen versuchen zu erstellen  False: Ausgeschaltet!
				if iGameTurn >= 375 and gc.getGame().countCivPlayersAlive() < iMaxPlayers and False:
						# freie PlayerID herausfinden
						iHunsID = 0
						for i in range(iMaxPlayers):
								j = iMaxPlayers-i-1
								pPlayer = gc.getPlayer(j)
								if not pPlayer.isAlive():
										iHunsID = j
										break

						if iHunsID == 0:
								return

						# Hunnen erstellen
						LeaderHuns = gc.getInfoTypeForString("LEADER_ATTILA")
						gc.getGame().addPlayer(iHunsID, LeaderHuns, CivHuns)
						pPlayer = gc.getPlayer(iHunsID)

						iUnitSettler = gc.getInfoTypeForString("UNIT_SETTLER")
						iUnitSpearman = gc.getInfoTypeForString("UNIT_SPEARMAN")
						iUnitWorker = gc.getInfoTypeForString("UNIT_WORKER")
						iUnitKeshik = gc.getInfoTypeForString("UNIT_MONGOL_KESHIK")
						iUnitArcher = gc.getInfoTypeForString("UNIT_REFLEX_ARCHER")
						iUnitHorse = gc.getInfoTypeForString("UNIT_HORSE")
						for _ in range(4):
								CvUtil.spawnUnit(iUnitSettler, loopPlot, pPlayer)
						for _ in range(12):
								CvUtil.spawnUnit(iUnitSpearman, loopPlot, pPlayer)
						for _ in range(8):
								CvUtil.spawnUnit(iUnitWorker, loopPlot, pPlayer)
						for _ in range(40):
								CvUtil.spawnUnit(iUnitKeshik, loopPlot, pPlayer)
						for _ in range(12):
								CvUtil.spawnUnit(iUnitArcher, loopPlot, pPlayer)
						for _ in range(4):
								CvUtil.spawnUnit(iUnitHorse, loopPlot, pPlayer)

						pPlayer.setCurrentEra(3)
						pPlayer.setGold(4000)

						# increasing Anger to all other CIVs
						# and looking for best tech player
						pTeam = gc.getTeam(pPlayer.getTeam())
						iPlayerBestTechScore = -1
						iTechScore = 0
						for i in range(iMaxPlayers):
								pSecondPlayer = gc.getPlayer(i)
								# increases Anger for all AIs
								if pSecondPlayer.getID() != pPlayer.getID() and pSecondPlayer.isAlive():
										# Haltung aendern
										pPlayer.AI_changeAttitudeExtra(i, -5)
										# Krieg erklaeren
										pTeam.declareWar(pSecondPlayer.getTeam(), 0, 6)
										# TechScore herausfinden
										if iTechScore < pSecondPlayer.getTechScore():
												iTechScore = pSecondPlayer.getTechScore()
												iPlayerBestTechScore = i

						# Techs geben
						if iPlayerBestTechScore > -1:
								xTeam = gc.getTeam(gc.getPlayer(iPlayerBestTechScore).getTeam())
								iTechNum = gc.getNumTechInfos()
								for iTech in range(iTechNum):
										if gc.getTechInfo(iTech) is not None and xTeam.isHasTech(iTech) and not pTeam.isHasTech(iTech) and gc.getTechInfo(iTech).isTrade():
												pTeam.setHasTech(iTech, 1, iHunsID, 0, 0)

				else:
						iUnitType = gc.getInfoTypeForString("UNIT_MONGOL_KESHIK")
						pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
						for _ in range(iHuns):
								CvUtil.spawnUnit(iUnitType, loopPlot, pBarbPlayer)


def doVikings():
		iBarbPlayer = gc.getBARBARIAN_PLAYER()
		pBarbPlayer = gc.getPlayer(iBarbPlayer)
		iUnitTypeShip = gc.getInfoTypeForString("UNIT_VIKING_1")
		iUnitTypeUnit = gc.getInfoTypeForString("UNIT_VIKING_2")
		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()
		bMeldung = False

		for _ in range(4):
				iRandX = CvUtil.myRandom(iMapW, "W")
				iRandY = iMapH - CvUtil.myRandom(5, "H")
				loopPlot = gc.getMap().plot(iRandX, iRandY)
				if loopPlot is not None and not loopPlot.isNone():
						if loopPlot.getFeatureType() == iDarkIce:
								continue
						if not loopPlot.isUnit() and loopPlot.isWater() and not loopPlot.isLake() and not loopPlot.isOwned():
								# Wikinger erstellen
								bMeldung = True
								CvUtil.spawnUnit(iUnitTypeShip, loopPlot, pBarbPlayer)
								for _ in range(4):
										CvUtil.spawnUnit(iUnitTypeUnit, loopPlot, pBarbPlayer)

		if bMeldung:
				if gc.getGame().getGameTurnYear() == 500:
						for iPlayer in range(gc.getMAX_PLAYERS()):
								pPlayer = gc.getPlayer(iPlayer)
								if pPlayer.isAlive() and pPlayer.isHuman():
										popupInfo = CyPopupInfo()
										popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
										popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_VIKINGS", ("", )))
										popupInfo.addPopup(pPlayer.getID())
						CyAudioGame().Play2DSound("AS2D_THEIRDECLAREWAR")


def doOnUnitMove(pUnit, pPlot, pOldPlot):
		# Seevoelkereinheit wird entladen, leere Seevoelkerschiffe werden gekillt
		if pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SEEVOLK"):
			if not pUnit.hasCargo():
				# COMMAND_DELETE can cause CtD if used in onUnitMove()
				# pUnit.doCommand(CommandTypes.COMMAND_DELETE, 1, 1)
				pUnit.kill(True, -1)
				return True
			else:
				if pOldPlot.getOwner() == -1 and pPlot.getOwner() != -1:
					if gc.getPlayer(pPlot.getOwner()).isHuman():
						CyInterface().addMessage(pPlot.getOwner(), True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_SEEVOLK_ALERT", ()), None, 2, pUnit.getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
					if pPlot.getOwner() == gc.getGame().getActivePlayer():
						CyAudioGame().Play2DSound("AS2D_THEIRDECLAREWAR")

		# Ziegen bleiben auf Bergen, wenn sie wegen Kulturgrenzen ausgeschlossen sind
		if pPlot.isPeak() and pOldPlot.isPeak():
			if CvUtil.myRandom(3, "killGoatsOnPeaks") == 1:
				pUnit.kill(True, -1)
				return True

		# Elephants can spread the bonus resource
		if pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_ELEFANT"):
			if CvUtil.myRandom(10, "ElephantSpreadsBonus") == 1:
				iJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
				iBonus = gc.getInfoTypeForString("BONUS_IVORY")
				if pPlot.getFeatureType() == iJungle:
					iX = pPlot.getX()
					iY = pPlot.getY()
					iRange = 2
					iAnzJungle = 0
					iAnzWhatever = 0
					lPlayers = []
					for x in range(-iRange, iRange):
							for y in range(-iRange, iRange):
									loopPlot = plotXY(iX, iY, x, y)
									if not loopPlot.isNone() and not loopPlot.isWater() and not loopPlot.isPeak():

										if loopPlot.getBonusType(-1) == iBonus or loopPlot.getBonusType(loopPlot.getOwner()) == iBonus:
											return False

										if loopPlot.getFeatureType() == iJungle: iAnzJungle += 1
										else: iAnzWhatever += 1
										
										if loopPlot.getOwner() != -1:
											if loopPlot.getOwner() not in lPlayers:
												lPlayers.append(loopPlot.getOwner())

					if iAnzJungle >= iAnzWhatever / 2:
						pPlot.setBonusType(iBonus)
						if len(lPlayers):
							for iPlayer in lPlayers:
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_POPUP_ELEPHANT_SPREADS_BONUS", (gc.getBonusInfo(iBonus).getDescription(),)),
												None, 2, gc.getBonusInfo(iBonus).getButton(), ColorTypes(8), pPlot.getX(), pPlot.getY(), True, True)
						pUnit.kill(True, -1)
						return True

		return False


def checkNearbyUnits(pPlot, iRange):
		iX = pPlot.getX()
		iY = pPlot.getY()
		for x in range(-iRange, iRange):
				for y in range(-iRange, iRange):
						loopPlot = plotXY(iX, iY, x, y)
						if not loopPlot.isWater() and loopPlot.getNumUnits() > 0:
								return True
		return False


def countNearbyUnits(pPlot, iRange, iPlayer):
		iAnz = 0
		iX = pPlot.getX()
		iY = pPlot.getY()
		for x in range(-iRange, iRange+1):
				for y in range(-iRange, iRange+1):
						loopPlot = plotXY(iX, iY, x, y)
						if loopPlot.getNumUnits() > 0 and loopPlot.getUnit(0).getOwner() == iPlayer:
								iAnz += loopPlot.getNumUnits()
		return iAnz

# Rebellen, Partisanen, Freiheitskämpfer (freedom fighters)
def getPartisan(pPlayer):
	pTeam = gc.getTeam(pPlayer.getTeam())
	#UNIT_AXEWARRIOR ST 4
	#UNIT_LIGHT_SPEARMAN ST 4
	#UNIT_AXEMAN ST 6
	#UNIT_REBELL ST 6
	#UNIT_SPEARMAN ST 8
	#UNIT_FREEDOM_FIGHTER ST 8
	#UNIT_AXEMAN2 ST 10
	lPartisans = []

	if pTeam.isHasTech(gc.getInfoTypeForString("TECH_EISENWAFFEN")):
		lPartisans.append(gc.getInfoTypeForString("UNIT_AXEMAN2"))
		lPartisans.append(gc.getInfoTypeForString("UNIT_FREEDOM_FIGHTER"))
	elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_ARMOR")):
		lPartisans.append(gc.getInfoTypeForString("UNIT_REBELL"))
		lPartisans.append(gc.getInfoTypeForString("UNIT_FREEDOM_FIGHTER"))
	elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_BEWAFFNUNG2")):
		lPartisans.append(gc.getInfoTypeForString("UNIT_REBELL"))
	elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_BEWAFFNUNG")):
		lPartisans.append(gc.getInfoTypeForString("UNIT_AXEWARRIOR"))
		lPartisans.append(gc.getInfoTypeForString("UNIT_LIGHT_SPEARMAN"))
	else:
		lPartisans.append(gc.getInfoTypeForString("UNIT_WARRIOR"))

	iRand = CvUtil.myRandom(len(lPartisans), "getPartisan")
	return lPartisans[iRand]
