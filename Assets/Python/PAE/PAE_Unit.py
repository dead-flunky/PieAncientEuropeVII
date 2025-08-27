# Imports
import re
from CvPythonExtensions import (CyGlobalContext, CyInterface, CyMap, CyGame,
											CyTranslator, DirectionTypes, CommerceTypes,
											InterfaceMessageTypes, CommandTypes, YieldTypes,
											ColorTypes, UnitAITypes, CyPopupInfo, GameOptionTypes,
											ButtonPopupTypes, MissionTypes, MissionAITypes,
											DomainTypes, plotXY, plotDirection, FontSymbols,
											plotDistance, directionXYFromPlot)

import CvUtil
import PyHelpers
import PAE_City
import PAE_Vassal
import PAE_Lists as L

# TODO remove
# DEBUG code for Python 3 linter
# unicode = str
# xrange = range


# Defines
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

# PAE - for units in getting Fighting-Promotions (per turn)
# [PlayerID, UnitID]
PAEInstanceFightingModifier = []

# PAE - Great General Names
GG_UsedNames = []

# Naval unit movement
def onUnitMoveOnSea(pUnit):
		pPlot = pUnit.plot()
		# ------ Seewind -----
		if pPlot.getFeatureType() > -1:
				iPlotWind = pPlot.getFeatureType()
				if iPlotWind in L.LSeewind:
						iWindIdx = L.LSeewind.index(iPlotWind)

						iUnitDirection = pUnit.getFacingDirection()

						# CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("direction",iUnitDirection)), None, 2, None, ColorTypes(10), 0, 0, False, False)
						# 1 plot move = 60
						# Ocean movement and feature movement cost = 1
						# +1 Bewegung in Wind,...
						iInWind = -120
						iInSchraegWind = -60
						iSeitenWind = 0
						iGegenSchraegWind = 60
						iGegenWind = 120
						if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_NAVIGATION1")):
								iSeitenWind = -60
								if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_NAVIGATION2")):
										iGegenSchraegWind = 0
										iGegenWind = 60
										if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_NAVIGATION3")):
												iInSchraegWind = -120

						lMoves = [
								iGegenWind,
								iGegenSchraegWind,
								iSeitenWind,
								iInSchraegWind,
								iInWind,
								iInSchraegWind,
								iSeitenWind,
								iGegenSchraegWind,
						]
						# CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("wind",lMoves[abs(iWindIdx-iUnitDirection)])), None, 2, None, ColorTypes(10), 0, 0, False, False)
						pUnit.changeMoves(lMoves[abs(iWindIdx-iUnitDirection)])
		# -- end Wind

		# Handelsschiffe von allen Schaden ausnehmen
		if pUnit.getUnitType() in L.LTradeUnits:
				return

		# ------ Verletzte Schiffe bzw Cargo
		iDamage = pUnit.getDamage()
		# mit PAEVII in CvUnit::doTurn()
		#if iDamage > 10:
		#		pUnit.changeMoves(iDamage/3)
		# Beladene Schiffe (nicht mehr ab Patch 4)
		#iCargo = pUnit.getCargo()
		# if iCargo > 0:
		#    pUnit.changeMoves(iCargo*10)

		# Workboats sink in unknown terrain (neutral or from other team): Chance 1:8
		if pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_WORKBOAT"):
				if pPlot.getOwner() != pUnit.getOwner():
						if CvUtil.myRandom(8, "WorkboatSink") == 1:
								if gc.getPlayer(pUnit.getOwner()).isHuman():
										CyInterface().addMessage(pUnit.getOwner(), True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_SINKING_SHIP", (pUnit.getName(),)),
																						 "AS2D_SINKING_W0RKBOAT", 2, pUnit.getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
								# COMMAND_DELETE can cause CtD if used in onUnitMove()
								# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
								pUnit.kill(True, -1)
								return

		# Schiffe auf Hoher See erleiden Sturmschaden
		elif pPlot.isWater() and pPlot.getFeatureType() == -1 and not pPlot.isCity():
				if pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_OCEAN") or pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DEEP_OCEAN"):
						# Damage (100=tot)
						iSchaden = 20
						# iDamage von oben
						if iDamage <= 90 - iSchaden:
								# Chance auf Schaden: 1:10 + Worldsize * x
								# Worldsize: 0 (Duell) - 5 (Huge)
								iChance = 10 + gc.getMap().getWorldSize() * 3
								if pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DEEP_OCEAN"):
										iChance = 10  # immer 10% bei tiefem Ozean
								if CvUtil.myRandom(iChance, "Sturmschaden") == 1:
										iDamage += iSchaden
										pUnit.setDamage(iDamage, -1)
										# Types of Damage (Messages)
										# 0 = Storm
										iRand = CvUtil.myRandom(6, "SturmschadenTyp")
										if iRand == 0:
												pPlot.setFeatureType(gc.getInfoTypeForString("FEATURE_SEESTURM"), 0)
												if gc.getPlayer(pUnit.getOwner()).isHuman():
														CyInterface().addMessage(pUnit.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_DAMAGE_SHIP_STORM", (pUnit.getName(), iSchaden)),
																										 "AS2D_UNIT_BUILD_GALLEY", 2, pUnit.getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
										elif gc.getPlayer(pUnit.getOwner()).isHuman():
												CyInterface().addMessage(pUnit.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_DAMAGE_SHIP_"+str(iRand), (pUnit.getName(), iSchaden)),
																								 "AS2D_UNIT_BUILD_GALLEY", 2, pUnit.getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)

		return

# Init ab wieviel Einheiten der Stack versorgt werden muss
def getStackLimit():
		# Handicap: 0 (Settler) - 8 (Deity) ; 5 = King
		iHandicap = gc.getGame().getHandicapType()
		if iHandicap == 0:
				return 20
		elif iHandicap == 1:
				return 20
		elif iHandicap == 2:
				return 15
		elif iHandicap == 3:
				return 10
		elif iHandicap == 4:
				return 10
		elif iHandicap == 5:
				return 10
		elif iHandicap == 6:
				return 15
		elif iHandicap == 7:
				return 20
		else:
				return 20


def stackDoTurn(iPlayer, iGameTurn):
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()
		pTeam = gc.getTeam(iTeam)

		# PAE 6.10: no unit supply for AI
		# Ab 6.16 doch nicht
		#if not pPlayer.isHuman():
		#		return

		PlotArrayRebellion = []
		PlotArraySupply = []
		PlotArrayStackAI = []
		lHealerPlots = []
		lFormationPlots = []
		iPromoFort = gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS")
		iPromoFort2 = gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS2")

		# Plots herausfinden
		# if iPlayer != gc.getBARBARIAN_PLAYER():
		# iPlayer > -1: wegen einrueckung!
		# PAE Better AI:
		# HI: 20 : 40 Units
		# AI: 30 : 50 Units

		iStackLimit1 = getStackLimit()
		iStackLimit2 = iStackLimit1 * 3  # Rebellionschance
		if not pPlayer.isHuman():
				iStackLimit1 += 20
				iStackLimit2 += 20

		(sUnit, pIter) = pPlayer.firstUnit(False)
		while sUnit:
				# tmpA: OBJECTS (tmpPlot) KANN MAN NICHT mit NOT IN in einer Liste pruefen!
				tmpA = [sUnit.getX(), sUnit.getY()]
				tmpPlot = sUnit.plot()
				if not tmpPlot.isWater():
						# if sUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_HEALER"):
						if sUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"):
								if tmpA not in lHealerPlots:
										lHealerPlots.append(tmpA)
						# PAE V: bei den Staedten gibts ne eigene funktion bei city supply
						if not tmpPlot.isCity():
								if tmpA not in PlotArraySupply:
										# 1. Instanz - Versorgung auf Land
										tmpAnz = tmpPlot.getNumDefenders(iPlayer)
										if tmpAnz >= 10:
												# AI Stack ausserhalb einer Stadt, in feindlichem Terrain
												if not pPlayer.isHuman():
														tmpOwner = tmpPlot.getOwner()
														if tmpOwner != -1 and tmpOwner != iPlayer:
																if tmpA not in PlotArrayStackAI:
																		if pTeam.isAtWar(gc.getPlayer(tmpOwner).getTeam()):
																				PlotArrayStackAI.append(tmpA)

												if tmpAnz >= iStackLimit1:
														PlotArraySupply.append(tmpA)
														# 2. Instanz - Rebellionsgefahr auf Land
														# wird weiter unten in PlotArraySuppy neu berechnet
														# if tmpAnz > iStackLimit2:
														#    PlotArrayRebellion.append(tmpA)
														# ***TEST***
														#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Stack (Zeile 3377)", tmpPlot.getNumDefenders(iPlayer))), None, 2, None, ColorTypes(10), 0, 0, False, False)

				# PAE V - Formations ++++

				# AI Formations
				if not pPlayer.isHuman():
						if tmpPlot.getNumUnits() > 2:
								if tmpA not in lFormationPlots:
										if not tmpPlot.isCity():
												doAIPlotFormations(tmpPlot, iPlayer)
										lFormationPlots.append(tmpA)
						# more than 50% damage -> go defensive
						elif sUnit.getDamage() > 50:
								doAIUnitFormations(sUnit, False, False, False)

						# Missing fort on a plot
						if sUnit.isHasPromotion(iPromoFort) or sUnit.isHasPromotion(iPromoFort2):
								iImp = tmpPlot.getImprovementType()
								if iImp > -1:
										if gc.getImprovementInfo(iImp).getDefenseModifier() < 10 or tmpPlot.getOwner() != sUnit.getOwner():
												doUnitFormation(sUnit, -1)
								else:
										doUnitFormation(sUnit, -1)

				(sUnit, pIter) = pPlayer.nextUnit(pIter, False)
		# while end

		# AI Stacks vor einer gegnerischen Stadt ---------------------------------------
		for h in PlotArrayStackAI:
				pPlotEnemyCity = None
				for x in range(3):
						for y in range(3):
								loopPlot = gc.getMap().plot(h[0]-1+x, h[1]-1+y)
								if loopPlot is not None and not loopPlot.isNone():
										iLoopPlotOwner = loopPlot.getOwner()
										if iLoopPlotOwner != -1 and loopPlot.isCity():
												if pTeam.isAtWar(gc.getPlayer(iLoopPlotOwner).getTeam()):
														pPlotEnemyCity = loopPlot
														break
						if pPlotEnemyCity is not None:
								break

				# vor den Toren der feindlichen Stadt
				if pPlotEnemyCity is not None:
						# Bombardement
						pStackPlot = gc.getMap().plot(h[0], h[1])
						iNumUnits = pStackPlot.getNumUnits()
						for i in range(iNumUnits):
								pUnit = pStackPlot.getUnit(i)
								if pUnit.getOwner() == iPlayer:
										if pUnit.isRanged():
												if not pUnit.isMadeAttack() and pUnit.getImmobileTimer() <= 0:
														# getbestdefender -> getDamage
														pBestDefender = pPlotEnemyCity.getBestDefender(-1, -1, pUnit, 1, 0, 0)
														# Ab ca 50% Schaden aufhoeren
														if pBestDefender.getDamage() < 55:
																pUnit.rangeStrike(pPlotEnemyCity.getX(), pPlotEnemyCity.getY())
														else:
																break

		# +++++ Aufladen der Versorger UNIT_SUPPLY_WAGON ---------------------------------------
		for h in lHealerPlots:
				loopPlot = gc.getMap().plot(h[0], h[1])
				iX = h[0]
				iY = h[1]

				# Units calc
				lHealer = []
				iRange = loopPlot.getNumUnits()
				for iUnit in range(iRange):
						pLoopUnit = loopPlot.getUnit(iUnit)
						if pLoopUnit.getOwner() == iPlayer:
								# if pLoopUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_HEALER"):
								if pLoopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"):
										if getSupply(pLoopUnit) < getMaxSupply(pLoopUnit):
												lHealer.append(pLoopUnit)

				# Plot inits
				bFill = False
				iSupplyChange = getSupplyFromPlot(iPlayer, loopPlot)

				# Inits for Supply Units (nur notwendig, wenns Versorger gibt)
				if len(lHealer) > 0:
						iLoopOwner = loopPlot.getOwner()
						# Eigenes Terrain
						if iLoopOwner == iPlayer:
								bFill = True
						# Fremdes Terrain
						else:
								if iLoopOwner != -1:
										pLoopOwner = gc.getPlayer(iLoopOwner)
										iTeamPlot = pLoopOwner.getTeam()
										pTeamPlot = gc.getTeam(iTeamPlot)

										# Versorger auf Vassalenterrain - Aufladechance - Stadt: 100%, Land 30%
										if pTeamPlot.isVassal(iTeam) and iSupplyChange > 0:
												if loopPlot.isCity():
														bFill = True
												elif CvUtil.myRandom(10, "Versorger_1") < 3:
														bFill = True

												if pPlayer.isHuman() and bFill:
														CyInterface().addMessage(iPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_SUPPLY_RELOAD_1",
														(pLoopOwner.getCivilizationAdjectiveKey(), 0)), None, 2, lHealer[0].getButton(), ColorTypes(8), iX, iY, True, True)

										# Versorger auf freundlichem Terrain - Aufladechance 30%, 20% oder 10%
										elif not pTeam.isAtWar(iTeamPlot):
												# Attitudes
												# 0 = Furious
												# 1 = Annoyed
												# 2 = Cautious
												# 3 = Polite
												# 4 = Gracious
												iAtt = pLoopOwner.AI_getAttitude(iPlayer)
												if iAtt == 4:
														iChance = 3
												elif iAtt == 3:
														iChance = 2
												elif iAtt == 2:
														iChance = 1
												else:
														iChance = 0
												if iChance > 0 and CvUtil.myRandom(10, "Versorger_2") < iChance:
														bFill = True
														if loopPlot.isCity():
																pCity = loopPlot.getPlotCity()
																# PAE V
																if pCity.getYieldRate(0) - loopPlot.getNumDefenders(iPlayer) > 0:
																		iSupplyChange = pCity.getYieldRate(0) - loopPlot.getNumDefenders(iLoopOwner)
																# PAE IV
																#if pCity.happyLevel() - pCity.unhappyLevel(0) > 0 and pCity.goodHealth() - pCity.badHealth(False) > 0: iSupplyChange += 50
														if pPlayer.isHuman() and bFill:
																CyInterface().addMessage(iPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_SUPPLY_RELOAD_2",
																(pLoopOwner.getCivilizationAdjectiveKey(), 0)), None, 2, lHealer[0].getButton(), ColorTypes(8), iX, iY, True, True)

										# Versorger steht auf feindlichem Terrain
										else: bFill = True

						if bFill and iSupplyChange > 0:
								# ++++ Supply Units update ------------
								# 1. Aufladen
								for loopUnit in lHealer:
										if iSupplyChange <= 0:
												break
										iSupplyChange = fillSupply(loopUnit, iSupplyChange)

		# +++++ Versorgung der Armee - supply wagon ---------------------------------------
		if PlotArraySupply:
				iUnitSupplyWagon = gc.getInfoTypeForString("UNIT_SUPPLY_WAGON")

				for h in PlotArraySupply:
						loopPlot = gc.getMap().plot(h[0], h[1])
						# Init
						iMounted = 0
						iMelee = 0
						lHealer = []
						iSupplyChange = 0
						iNumUnits = loopPlot.getNumUnits()
						# PAE V: Stack Limit mit iStackLimit1 einbeziehen
						if loopPlot.getNumDefenders(iPlayer) - iStackLimit1 > 0:
								# Units calc
								for i in range(iNumUnits):
										pLoopUnit = loopPlot.getUnit(i)
										if pLoopUnit.getOwner() == iPlayer:
												iUnitType = pLoopUnit.getUnitCombatType()
												# if iUnitType == gc.getInfoTypeForString("UNITCOMBAT_HEALER"):
												if pLoopUnit.getUnitType() == iUnitSupplyWagon:
														lHealer.append(pLoopUnit)
												else:
														if iUnitType in L.LMountedSupplyCombats:
																iMounted += 1
														elif iUnitType in L.LMeleeSupplyCombats:
																iMelee += 1

						# ***TEST***
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("UNITCOMBAT_MELEE", iMelee)), None, 2, None, ColorTypes(10), 0, 0, False, False)
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("UNITCOMBAT_HEALER", len(lHealer))), None, 2, None, ColorTypes(10), 0, 0, False, False)

						# Plot properties
						bDesert = (loopPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DESERT"))

						# 1. Versorgen
						for loopUnit in lHealer:
								if iMounted <= 0 and iMelee <= 0:
										break
								iSupplyValue = getSupply(loopUnit)

								# ***TEST***
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Supply Unit init "+str(loopUnit.getID()), iSupplyValue)), None, 2, None, ColorTypes(10), 0, 0, False, False)

								if iSupplyValue > 0:
										# Mounted Units
										if bDesert:
												if iSupplyValue > iMounted * 2:
														iSupplyValue -= iMounted * 2
														iMounted = 0
												else:
														iCalc = iSupplyValue / 2
														iSupplyValue -= iCalc * 2
														iMounted -= iCalc
										else:
												iSupplyValue -= iMounted
												if iSupplyValue < 0:
														iMounted = (-1)*iSupplyValue
														iSupplyValue = 0
												else:
														iMounted = 0

										# Melee Units
										iSupplyValue -= iMelee
										if iSupplyValue < 0:
												iMelee = (-1)*iSupplyValue
												iSupplyValue = 0
										else:
												iMelee = 0
										setSupply(loopUnit, iSupplyValue)

								# ***TEST***
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",( "Supply Unit changed", iSupplyValue)), None, 2, None, ColorTypes(10), 0, 0, False, False)

						# 2. Units verletzen
						iSum = iMounted + iMelee

						# for Stack Rebellion
						if iSum > iStackLimit2:
								PlotArrayRebellion.append(loopPlot)

						if iSum > 0 and iSum > iStackLimit1:
								# PAE - Message for StacksOfDoom only once per turn
								iUnitStackMelee = 0
								iUnitStackMounted = 0

								iRange = loopPlot.getNumUnits()
								for iUnit in range(iRange):
										if iSum <= 0:
												break
										xUnit = loopPlot.getUnit(iUnit)
										xDamage = xUnit.getDamage()

										# AI: wenn der Schaden zu groß ist, sollen die überschüssigen Einheiten in die nächste Stadt
										if xDamage > 60 and not pPlayer.isHuman():
												pCity = getNearestCity(xUnit)
												if pCity != None:
														xUnit.getGroup().pushMoveToMission(pCity.getX(), pCity.getY())
														iSum -= 1
														continue

										if xUnit.getUnitCombatType() in L.LMountedSupplyCombats:
												if xDamage + 25 < 100:
														xUnit.changeDamage(15, False)
														xUnit.getGroup().pushMission(MissionTypes.MISSION_IDLE, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, xUnit.plot(), xUnit)
														iUnitStackMounted += 1
														iSum -= 1
										elif xUnit.getUnitCombatType() in L.LMeleeSupplyCombats:
												if xDamage + 30 < 100:
														xUnit.changeDamage(20, False)
														xUnit.getGroup().pushMission(MissionTypes.MISSION_IDLE, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, xUnit.plot(), xUnit)
														iUnitStackMelee += 1
														iSum -= 1

								if iUnitStackMelee and pPlayer.isHuman():
										CyInterface().addMessage(iPlayer, True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_NOSUPPLY_PLOT_1", (iUnitStackMelee, 20, iStackLimit1)), None, 2, None, ColorTypes(12), loopPlot.getX(), loopPlot.getY(), True, True)

								if iUnitStackMounted and pPlayer.isHuman():
										CyInterface().addMessage(iPlayer, True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_NOSUPPLY_PLOT_2", (iUnitStackMounted, 15, iStackLimit1)), None, 2, None, ColorTypes(12), loopPlot.getX(), loopPlot.getY(), True, True)




		# +++++ Rebellious STACKs ---------------
		# Stack can become independent / rebellious
		# per Unit 0.5%, pro Runde 25% check chance
		if PlotArrayRebellion and CvUtil.myRandom(4, "StackRebellion") == 1:
				doStackRebellion(iPlayer, PlotArrayRebellion, iStackLimit2)


def doStackRebellion(iPlayer, PlotArrayRebellion, iStackLimit2):
		if iPlayer == -1:
				return

		pPlayer = gc.getPlayer(iPlayer)
		bAtWar = False
		iRange = gc.getMAX_PLAYERS()
		for i in range(iRange):
				if gc.getPlayer(i).isAlive():
						if gc.getTeam(pPlayer.getTeam()).isAtWar(gc.getPlayer(i).getTeam()):
								bAtWar = True
								break

		iPromoLeader = gc.getInfoTypeForString('PROMOTION_LEADER')
		iPromoHero = gc.getInfoTypeForString('PROMOTION_HERO')
		# Loyale Einheiten sind dem Feldherren loyal gewesen!
		#      iPromoLoyal = gc.getInfoTypeForString('PROMOTION_LOYALITAT')

		# h is nun ein Object (PAE 6.5.2)
		for h in PlotArrayRebellion:
				sPlot = h  # gc.getMap().plot(h[0], h[1])
				iNumUnits = sPlot.getNumUnits()
				iX = sPlot.getX()  # h[0]
				iY = sPlot.getY()  # h[1]
				iPlotOwner = sPlot.getOwner()

				# (Inaktiv: 30 / 5 = 4. Daher ziehe ich 5 ab, damit es bei 1% beginnt)
				#iPercent = int(iNumUnits / 2)
				iPercent = 0

				# wenn Krieg ist -20%
				if bAtWar:
						iPercent -= 20

				# for each general who accompanies the stack: -10%
				iCombatSiege = gc.getInfoTypeForString("UNITCOMBAT_SIEGE")
				iCombatUnits = 0
				for i in range(iNumUnits):
						pLoopUnit = sPlot.getUnit(i)
						if pLoopUnit.getOwner() == iPlayer:
								if pLoopUnit.isMilitaryHappiness():
										if pLoopUnit.getUnitCombatType() != iCombatSiege:
												iCombatUnits += 1
								if pLoopUnit.isHasPromotion(iPromoLeader):
										iPercent -= 20
								if pLoopUnit.isHasPromotion(iPromoHero):
										iPercent -= 10

				if iCombatUnits >= iStackLimit2:
						# PAE better AI
						if pPlayer.isHuman():
								iPercent += iCombatUnits
						else:
								iPercent += iCombatUnits / 2
				else:
						iPercent = -1

				# Loyale Einheiten sind dem Feldherren loyal gewesen!
				#if sPlot.getUnit(i).isHasPromotion(iPromoLoyal): fPercent -= 0.1
				# auf eigenem Terrain -2, auf feindlichem +2, auf neutralem 0
				#if iPlotOwner == iPlayer: iPercent -= 1
				# elif iPlotOwner != -1: iPercent += 1

				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("iPlayer", iPlayer)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Units", iNumUnits)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("iPercent", iPercent)), None, 2, None, ColorTypes(10), 0, 0, False, False)

				if iPercent > 0:
						iBarbarianPlayer = gc.getBARBARIAN_PLAYER()
						pBarbarianPlayer = gc.getPlayer(iBarbarianPlayer)
						iRand = CvUtil.myRandom(100, "STACKs_1")
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("iRand", iRand)), None, 2, None, ColorTypes(10), 0, 0, False, False)

						# PAE IV Update: 1. Check
						if iRand < iPercent:
								# PAE IV Update: 2. Check: 25% Rebellion, 75% Meldung
								# PAE V: 2. Check: 20% Rebellion, 80% Meldung
								iRand = CvUtil.myRandom(5, "STACKs_2")
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("2.Check", iRand)), None, 2, None, ColorTypes(10), 0, 0, False, False)
								# Rebellious stack
								if iRand == 1:
										#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("REBELLION", 1)), None, 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(10), sPlot.getX(), sPlot.getY(), True, True)

										# Einen guenstigen Plot auswaehlen
										rebelPlotArray = []
										rebelPlotArrayB = []
										for i in range(3):
												for j in range(3):
														loopPlot = gc.getMap().plot(sPlot.getX() + i - 1, sPlot.getY() + j - 1)
														if loopPlot is not None and not loopPlot.isNone() and not loopPlot.isUnit():
																if loopPlot.isHills():
																		rebelPlotArray.append(loopPlot)
																if not loopPlot.isWater() and not loopPlot.isImpassable() and not loopPlot.isCity():
																		rebelPlotArrayB.append(loopPlot)

										if not rebelPlotArray:
												rebelPlotArray = rebelPlotArrayB

										# es kann rebelliert werden
										if rebelPlotArray:
												iRebelPlot = CvUtil.myRandom(len(rebelPlotArray), "STACKs_3")
												pRebelPlot = rebelPlotArray[iRebelPlot]
												# Anzahl der rebellierenden Einheiten
												iNumRebels = CvUtil.myRandom(iNumUnits, "STACKs_4")
												if iNumRebels < 10:
														iNumRebels = 9

												# kleine Rebellion
												if iNumRebels * 2 < iNumUnits:
														text = CyTranslator().getText("TXT_KEY_MESSAGE_STACK_REBELS_1", ("Units", iNumUnits))
														if pPlayer.isHuman():
																CyInterface().addMessage(iPlayer, True, 5, text, "AS2D_THEIRDECLAREWAR", 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), iX, iY, True, True)
														PAE_City.doNextCityRevolt(iX, iY, iPlayer, gc.getBARBARIAN_PLAYER())

												# grosse Rebellion (+ Generalseinheit)
												else:
														if pPlayer.isHuman():
																text = CyTranslator().getText("TXT_KEY_MESSAGE_STACK_REBELS_2", ("Units", iNumUnits))
																CyInterface().addMessage(iPlayer, True, 5, text, "AS2D_THEIRDECLAREWAR", 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), iX, iY, True, True)

														listNamesStandard = ["Adiantunnus", "Divico", "Albion", "Malorix", "Inguiomer", "Archelaos", "Dorimachos", "Helenos", "Kerkidas", "Mikythos", "Philopoimen", "Pnytagoras", "Sophainetos", "Theopomopos", "Gylippos", "Proxenos", "Theseus", "Balakros", "Bar Kochba", "Julian ben Sabar", "Justasas", "Patricius", "Schimon bar Giora",
																								 "Artaphernes", "Harpagos", "Atropates", "Bahram Chobin", "Datis", "Schahin", "Egnatius", "Curius Aentatus", "Antiochos II", "Spartacus", "Herodes I", "Calgacus", "Suebonius Paulinus", "Maxentus", "Sapor II", "Alatheus", "Saphrax", "Honorius", "Aetius", "Achilles", "Herodes", "Heros", "Odysseus", "Anytos"]
														iName = CvUtil.myRandom(len(listNamesStandard), "GG_name")

														iUnitType = gc.getInfoTypeForString("UNIT_GREAT_GENERAL")
														unit = pBarbarianPlayer.initUnit(iUnitType, pRebelPlot.getX(), pRebelPlot.getY(), UnitAITypes.UNITAI_GENERAL, DirectionTypes.DIRECTION_SOUTH)
														unit.setName(listNamesStandard[iName])
														PAE_City.doNextCityRevolt(iX, iY, iPlayer, iBarbarianPlayer)
														PAE_City.doNextCityRevolt(iX, iY, iPlayer, iBarbarianPlayer)

												# PopUp
												if pPlayer.isHuman():
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(text)
														popupInfo.addPopup(iPlayer)

												# ***TEST***
												#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Stack Rebellion (Zeile 2028)", iPlayer)), None, 2, None, ColorTypes(10), sPlot.getX(), sPlot.getY(), True, True)

												# Units become rebels
												for i in range(iNumRebels):
														# Zufallsunit, getnumunits muss jedesmal neu ausgerechnet werden, da ja die rebell. units auf diesem plot wegfallen
														iRand = CvUtil.myRandom(sPlot.getNumDefenders(iPlayer), "rebels")
														# Unit kopieren
														pRandUnit = sPlot.getUnit(iRand)
														if pRandUnit.getOwner() == iPlayer:
																rebell(pRandUnit, pBarbarianPlayer, pRebelPlot)

												# Meldung an den Spieler auf dem Territorium einer dritten Partei
												if iPlotOwner != -1:
														if iPlotOwner != iPlayer and gc.getPlayer(iPlotOwner).isHuman():
																CyInterface().addMessage(iPlotOwner, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_STACK_REBELS_4", (pPlayer.getCivilizationAdjective(1),)),
																												 "AS2D_REBELLION", 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), iX, iY, True, True)

												# ***TEST***
												#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Rebellisches Stack (Zeile 1557)", 1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

								# ne kleine Warnung ausschicken
								else:
										if pPlayer.isHuman():
												CyInterface().addMessage(iPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_STACK_REBELS_0", ("",)),
																								 "AS2D_REBELLION", 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), iX, iY, True, True)
										else:
												# AI kills a weak unit to prevent a rebellion
												#iST = seekUnit = seekST = 0
												# for i in range(iNumUnits):
												#  iST = sPlot.getUnit(i).baseCombatStr()
												#  if iST < seekST and iST > 0 or seekST == 0:
												#   seekUnit = i
												#   seekST = iST
												#pUnit = sPlot.getUnit(seekUnit)
												## pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
												# pUnit.kill(True, -1)  # RAMK_CTD

												# AI teilt Stack (jede 4. Einheit)
												for i in range(iNumUnits):
														if i % 4 == 1:
																pLoopUnit = sPlot.getUnit(i)
																if pLoopUnit.getOwner() == iPlayer:
																		pLoopUnit.jumpToNearestValidPlot()

												# Meldung an den Spieler auf dem Territorium einer dritten Partei
												if iPlotOwner != -1:
														if iPlotOwner != iPlayer and gc.getPlayer(iPlotOwner).isHuman():
																CyInterface().addMessage(iPlotOwner, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_STACK_REBELS_3", (pPlayer.getCivilizationAdjective(1),)),
																												 "AS2D_REBELLION", 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), iX, iY, True, True)


# +++++ Rebellious Stack -- end ---------------------------------------------

# Upgrade Veteran Unit to Elite Unit - Belobigung
# CommandUpgrade geht nur, wenn
# - die Einheit auch wirklich zu dieser Einheit laut XML upgegradet werden kann
# - alle Vorraussetzungen fuer die neuen Einheit erfuellt sind
# - im eigenen Territorium
#pUnit.doCommand (CommandTypes.COMMAND_UPGRADE, gc.getInfoTypeForString("UNIT_TRIARII"), 0)
def doUpgradeVeteran(pUnit, iNewUnit, bChangeCombatPromo):
		if iNewUnit == -1:
				return
		if not iNewUnit in range(gc.getNumUnitInfos()):
				# ***TEST***
				CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",
								("Upgrade Veteran: Invalid New Unit Type", iNewUnit)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				return

		if pUnit is not None and not pUnit.isNone():
				pUnitOwner = gc.getPlayer(pUnit.getOwner())
				if pUnitOwner is not None and not pUnitOwner.isNone():

						NewUnit = pUnitOwner.initUnit(iNewUnit, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

						# Einheit: max Combat 2
						forbiddenPromos = L.LVeteranForbiddenPromos
						if pUnit.getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_ARCHER"):
								forbiddenPromos.extend(L.LVeteranForbiddenPromos1)
						else:
								forbiddenPromos.extend(L.LCityRaider)

						if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
								forbiddenPromos.extend(L.LCityGarrison)
						elif iNewUnit == gc.getInfoTypeForString("UNIT_PRAETORIAN"):
								forbiddenPromos.extend(L.LVeteranForbiddenPromos4)

						iRange = gc.getNumPromotionInfos()
						for j in range(iRange):
								if "_FORM_" in gc.getPromotionInfo(j).getType():
										continue
								if j not in forbiddenPromos:
										if pUnit.isHasPromotion(j):
												NewUnit.setHasPromotion(j, True)

						NewUnit.setExperience(pUnit.getExperience(), -1)
						NewUnit.setLevel(pUnit.getLevel())

						copyName(NewUnit, pUnit.getUnitType(), pUnit.getName())

						# if unit was a general  (PROMOTION_LEADER)
						if pUnit.getLeaderUnitType() > -1:
								NewUnit.setLeaderUnitType(pUnit.getLeaderUnitType())
								pUnit.setLeaderUnitType(-1)  # avoids ingame message "GG died in combat"

						NewUnit.setDamage(pUnit.getDamage(), -1)
						NewUnit.setImmobileTimer(1)

						# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
						pUnit.kill(True, -1)  # RAMK_CTD

						return NewUnit

# Unit Rang/Rank Promos (PAE, ModMessage:751)
# PromoUp

def canUpgradeUnit(pUnit):
		if pUnit is None or pUnit.isNone():
				return -1
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = pPlayer.getCivilizationType()
		pTeam = gc.getTeam(pPlayer.getTeam())
		iUnitType = pUnit.getUnitType()
		iNewUnit = -1

		if iUnitType in L.LNoRankUnits:
				return -1

		eMounted = gc.getInfoTypeForString("UNITCOMBAT_MOUNTED")
		eBonus = gc.getInfoTypeForString("BONUS_HORSE")

		# Etrusker = Rom
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"):
				iCiv = gc.getInfoTypeForString("CIVILIZATION_ROME")
		# Griechen
		if iCiv in L.LGreeks:
				iCiv = gc.getInfoTypeForString("CIVILIZATION_GREECE")

		for data in L.LRankUnits:
				if iCiv == data[0]:
						# Praetorianer Check, im 2 Jhd. n. Chr. wurden Praetorianer abgeschafft
						if iUnitType in L.LPraetorians or data[1] in L.LPraetorians or data[2] in L.LPraetorians:
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_GRENZHEER")):
										return -1

						if iUnitType == data[2]:
								continue

						if (iUnitType == data[1] 
									or data[1] == -1 and pUnit.getUnitCombatType() in L.LMeleeCombats
									or data[1] == -2 and pUnit.getUnitCombatType() == eMounted
								):
								# neue Unit darf nicht schwächer sein als die alte
								if gc.getUnitInfo(iUnitType).getCombat() > gc.getUnitInfo(data[2]).getCombat():
										return -1
								# bestimmte Promotion erforderlich
								if pUnit.isHasPromotion(data[3]):
										if pTeam.isHasTech(gc.getUnitInfo(data[2]).getPrereqAndTech()):
												iNewUnit = data[2]
												if gc.getUnitInfo(data[2]).getUnitCombatType() == eMounted and not pPlayer.hasBonus(eBonus):
														iNewUnit = -1
		return iNewUnit

# Kein Check (notwendig den Helptext in den CvGameUtils)
def getUpgradeUnit(iPlayer, iUnitType):
		pPlayer = gc.getPlayer(iPlayer)
		iCiv = pPlayer.getCivilizationType()
		iNewUnit = -1
		
		LPromo = [
				gc.getInfoTypeForString("PROMOTION_COMBAT4"),
				gc.getInfoTypeForString("PROMOTION_COMBAT5")
		]

		for data in L.LRankUnits:
				if iCiv == data[0]:
						if iUnitType == data[2]:
								continue
						if (iUnitType == data[1] 
									or data[1] == -1 and gc.getUnitInfo(iUnitType).getUnitCombatType() in L.LMeleeCombats
									or data[1] == -2 and gc.getUnitInfo(iUnitType).getUnitCombatType() == iMounted
								):
								iNewUnit = data[2]
								# Primär die Einheit schicken, die mit Rang und nicht mit Veteranstatus befördert wird
								if data[3] not in LPromo:
										return iNewUnit

		return iNewUnit

		"""
		# Rome
		if iUnitType == gc.getInfoTypeForString("UNIT_LEGION"):
				return gc.getInfoTypeForString("UNIT_LEGION_OPTIO")
		elif iUnitType == gc.getInfoTypeForString("UNIT_LEGION2"):
				return gc.getInfoTypeForString("UNIT_LEGION_OPTIO2")
		elif iUnitType == gc.getInfoTypeForString("UNIT_LEGION_OPTIO"):
				return gc.getInfoTypeForString("UNIT_LEGION_CENTURIO")
		elif iUnitType == gc.getInfoTypeForString("UNIT_LEGION_OPTIO2"):
				return gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2")
		elif iUnitType == gc.getInfoTypeForString("UNIT_LEGION_CENTURIO") or iUnitType == gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"):
				if pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
						return gc.getInfoTypeForString("UNIT_LEGION_TRIBUN")
		elif iUnitType == gc.getInfoTypeForString("UNIT_EQUITES") or iUnitType == gc.getInfoTypeForString("UNIT_HORSEMAN_EQUITES2"):
				return gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO")
		elif iUnitType == gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO"):
				return gc.getInfoTypeForString("UNIT_LEGION_TRIBUN")
		elif iUnitType == gc.getInfoTypeForString("UNIT_ROME_COMITATENSES"):
				return gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2")
		elif iUnitType == gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2"):
				return gc.getInfoTypeForString("UNIT_ROME_COMITATENSES3")

		# Griechen
		elif iUnitType == gc.getInfoTypeForString("UNIT_HOPLIT"):
				return gc.getInfoTypeForString("UNIT_HOPLIT_2")
		elif iUnitType == gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"):
				return gc.getInfoTypeForString("UNIT_HOPLIT_2")
		elif iUnitType == gc.getInfoTypeForString("UNIT_HOPLIT_2"):
				return gc.getInfoTypeForString("UNIT_ELITE_HOPLIT")
		elif iUnitType == gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"):
				if pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
						return gc.getInfoTypeForString("UNIT_GREEK_STRATEGOS")

		# Sparta
		elif iUnitType == gc.getInfoTypeForString("UNIT_SPARTA_1"):
				return gc.getInfoTypeForString("UNIT_SPARTA_2")
		elif iUnitType == gc.getInfoTypeForString("UNIT_SPARTA_2"):
				return gc.getInfoTypeForString("UNIT_SPARTA_3")
		# Makedonen
		elif iUnitType == gc.getInfoTypeForString("UNIT_PEZHETAIROI") and iCivType == gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"):
				return gc.getInfoTypeForString("UNIT_PEZHETAIROI2")
		elif iUnitType == gc.getInfoTypeForString("UNIT_PEZHETAIROI2"):
				return gc.getInfoTypeForString("UNIT_PEZHETAIROI3")
		elif iUnitType == gc.getInfoTypeForString("UNIT_PEZHETAIROI3"):
				return gc.getInfoTypeForString("UNIT_PEZHETAIROI4")
		elif iUnitType == gc.getInfoTypeForString("UNIT_SCHILDTRAEGER") and iCivType == gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"):
				return gc.getInfoTypeForString("UNIT_HYPASPIST")
		elif iUnitType == gc.getInfoTypeForString("UNIT_HYPASPIST"):
				return gc.getInfoTypeForString("UNIT_HYPASPIST2")
		elif iUnitType == gc.getInfoTypeForString("UNIT_HYPASPIST2"):
				return gc.getInfoTypeForString("UNIT_HYPASPIST3")
		# Perser
		elif iUnitType == gc.getInfoTypeForString("UNIT_SPEARMAN_PERSIA") or iUnitType == gc.getInfoTypeForString("UNIT_UNSTERBLICH") or iUnitType == gc.getInfoTypeForString("UNIT_HOPLIT_PERSIA"):
				return gc.getInfoTypeForString("UNIT_APFELTRAEGER")
		elif iUnitType == gc.getInfoTypeForString("UNIT_APFELTRAEGER"):
				if pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
						if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_THE_WHEEL3")):
								return gc.getInfoTypeForString("UNIT_PERSIA_AZADAN")
		elif iUnitType == gc.getInfoTypeForString("UNIT_HORSEMAN_PERSIA"):
				return gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE1")
		elif iUnitType == gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE1"):
				return gc.getInfoTypeForString("UNIT_CATAPHRACT_PERSIA")
		elif iUnitType == gc.getInfoTypeForString("UNIT_CATAPHRACT_PERSIA"):
				return gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE2")

		# Egypt, Nubia
		elif iCivType == gc.getInfoTypeForString("CIVILIZATION_EGYPT") or iCivType == gc.getInfoTypeForString("CIVILIZATION_NUBIA"):
				if iUnitType == gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"):
						if pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
								if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_THE_WHEEL3")):
										return gc.getInfoTypeForString("UNIT_WAR_CHARIOT")
				else:
						return gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT")
		# Karthago
		elif iUnitType == gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD") or iUnitType == gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT"):
				return gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2")
		elif iUnitType == gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"):
				return gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER")
		# Assyrer und Babylonier
		elif iCivType == gc.getInfoTypeForString("CIVILIZATION_ASSYRIA") or iCivType == gc.getInfoTypeForString("CIVILIZATION_BABYLON"):
				if iUnitType == gc.getInfoTypeForString("UNIT_ASSUR_RANG1"):
						return gc.getInfoTypeForString("UNIT_ASSUR_RANG2")
				elif iUnitType == gc.getInfoTypeForString("UNIT_ASSUR_RANG2"):
						if pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
								if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_THE_WHEEL3")):
										return gc.getInfoTypeForString("UNIT_ASSUR_RANG3")
				elif iUnitType == gc.getInfoTypeForString("UNIT_ASSUR_RANG3"):
						return gc.getInfoTypeForString("UNIT_ELITE_ASSUR")
				else:
						return gc.getInfoTypeForString("UNIT_ASSUR_RANG1")
		# Sumerer
		elif iCivType == gc.getInfoTypeForString("CIVILIZATION_SUMERIA"):
				if iUnitType == gc.getInfoTypeForString("UNIT_SUMER_RANG1"):
						if pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
								if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_THE_WHEEL3")):
										return gc.getInfoTypeForString("UNIT_SUMER_RANG2")
				else:
						return gc.getInfoTypeForString("UNIT_SUMER_RANG1")
		# Germanen, Vandalen, Hunnen
		elif iCivType in L.LCivGermanen:
				return gc.getInfoTypeForString("UNIT_STAMMESFUERST")
		elif iCivType == gc.getInfoTypeForString("CIVILIZATION_HUNNEN"):
				return gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN_HUN")

		return -1
		"""


def doUpgradeRang(iPlayer, iUnit):
		pPlayer = gc.getPlayer(iPlayer)
		pUnit = pPlayer.getUnit(iUnit)
		iUnitType = pUnit.getUnitType()
		iCivType = pPlayer.getCivilizationType()
		iNewUnit = -1
		bInfoBonus = False
		iInfoTech = -1

		iNewUnit = canUpgradeUnit(pUnit)

		LRomanLegion = [
				gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"),
				gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO")
		]

		# Warum die Einheit nicht upgegradet werden kann
		if iNewUnit == -1:
				# Rome
				if iUnitType == gc.getInfoTypeForString("UNIT_LEGION_CENTURIO") or iUnitType == gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"):
						if not pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
								bInfoBonus = True

				# Griechen
				elif iUnitType == gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"):
						if not pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
								bInfoBonus = True

				# Perser
				elif iNewUnit == gc.getInfoTypeForString("UNIT_PERSIA_AZADAN"):
						if pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
								if not gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_THE_WHEEL3")):
										iInfoTech = gc.getInfoTypeForString("TECH_THE_WHEEL3")
						else:
								bInfoBonus = True

				# Egypt, Nubia
				elif iCivType == gc.getInfoTypeForString("CIVILIZATION_EGYPT") or iCivType == gc.getInfoTypeForString("CIVILIZATION_NUBIA"):
						if iUnitType == gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"):
								if pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
										if not gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_THE_WHEEL3")):
												iInfoTech = gc.getInfoTypeForString("TECH_THE_WHEEL3")
								else:
										bInfoBonus = True

				# Assyrer und Babylonier
				elif iCivType == gc.getInfoTypeForString("CIVILIZATION_ASSYRIA") or iCivType == gc.getInfoTypeForString("CIVILIZATION_BABYLON"):
						if iUnitType == gc.getInfoTypeForString("UNIT_ASSUR_RANG2"):
								if pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
										if not gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_THE_WHEEL3")):
												iInfoTech = gc.getInfoTypeForString("TECH_THE_WHEEL3")
								else:
										bInfoBonus = True
				# Sumerer
				elif iCivType == gc.getInfoTypeForString("CIVILIZATION_SUMERIA"):
						if iUnitType == gc.getInfoTypeForString("UNIT_SUMER_RANG1"):
								if pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
										if not gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_THE_WHEEL3")):
												iInfoTech = gc.getInfoTypeForString("TECH_THE_WHEEL3")
								else:
										bInfoBonus = True

				# Meldung no bonus
				if bInfoBonus and iPlayer == gc.getGame().getActivePlayer():
						CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_RANK_BONUS_INFO", ("",)), None, 2, None, ColorTypes(7), 0, 0, False, False)
				elif iInfoTech != -1 and iPlayer == gc.getGame().getActivePlayer():
						CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_RANK_TECH_INFO", (gc.getTechInfo(iInfoTech).getDescription(),)), None, 2, None, ColorTypes(7), 0, 0, False, False)

				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Upgrade Rang: not possible (wrong unit, horse or tech)", iUnitType)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				return False

		# Neue Einheit
		else:
				# ScriptData leeren
				CvUtil.removeScriptData(pUnit, "P")
				pNewUnit = doUpgradeVeteran(pUnit, iNewUnit, True)

				# Rome
				if iUnitType in LRomanLegion:
						setLegionName(pNewUnit)

				if pPlayer.isHuman():
						pPlayer.changeGold(-30)
						if iPlayer == gc.getGame().getActivePlayer():
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_RANK_PROMOTED", (gc.getUnitInfo(
										iUnitType).getDescription(), gc.getUnitInfo(iNewUnit).getDescription())), None, 2, None, ColorTypes(8), 0, 0, False, False)

				return True


# Legion in Ausbildung (PAE, ModMessage:756)
def doKastell(iPlayer, iUnit):
		pPlayer = gc.getPlayer(iPlayer)
		pUnit = pPlayer.getUnit(iUnit)
		iPrice = 25

		pPlayer.changeGold(-iPrice)

		doRankPromo(pUnit)

		pUnit.finishMoves()
		doGoToNextUnit(pUnit)


# PAE UNIT FORMATIONS ------------------------------
def canDoFormation(pUnit, iFormation):
		if not pUnit.canMove() or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MERCENARY")):
				return False

		iUnitType = pUnit.getUnitType()
		iUnitCombatType = pUnit.getUnitCombatType()
		pPlayer = gc.getPlayer(pUnit.getOwner())
		pTeam = gc.getTeam(pPlayer.getTeam())

		# Naval
		if iUnitCombatType == gc.getInfoTypeForString("UNITCOMBAT_NAVAL"):
				if iUnitType not in L.LFormationNoNaval:
						if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_KEIL") or iFormation == gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_ZANGE"):
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_LOGIK")):
										return True
						else:
								return True

		# Mounted mit Fernangriff
		elif iUnitCombatType == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
				# Fourage
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_FOURAGE"):
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_BRANDSCHATZEN")):
								if iUnitType not in L.LUnitWarAnimals:
										return True

				# Partherschuss oder Kantabrischer Kreis
				elif iFormation == gc.getInfoTypeForString("PROMOTION_FORM_PARTHER") or iFormation == gc.getInfoTypeForString("PROMOTION_FORM_KANTAKREIS"):
						if iUnitType in L.LUnitPartherschuss:
								# Partherschuss
								if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_PARTHER"):
										if pTeam.isHasTech(gc.getInfoTypeForString("TECH_PARTHERSCHUSS")):
												if pUnit.getCivilizationType() in L.LCivPartherschuss:
														return True
								# Kantabrischer Kreis
								elif iFormation == gc.getInfoTypeForString("PROMOTION_FORM_KANTAKREIS"):
										if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KANTAKREIS")):
												return True

				# Keil (fuer schwere Kavallerie)
				elif iFormation == gc.getInfoTypeForString("PROMOTION_FORM_KEIL"):
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KAMPFHUNDE")):
								if iUnitType in L.LKeilUnits:
										return True

		# Melee and Spear
		elif iUnitCombatType in L.LMeleeCombats:
				# Fortress
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS") and pUnit.baseMoves() == 1:
						return True
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS2") and pUnit.baseMoves() > 1:
						return True

				# Schildwall
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_SCHILDWALL"):
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_ARMOR")):
								if iUnitType not in L.LNoSchildwallUnits and pUnit.getUnitClassType() not in L.LNoSchildwallUnitClasses:
										return True

				# Drill: Manipel, Phalanx, ...
				if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DRILL1")):
						# Roman Legion (Kohorte)
						if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_KOHORTE"):
								if pUnit.getUnitType() in L.LDrillUnits:
										return True
						# Treffen-Taktik
						elif iFormation == gc.getInfoTypeForString("PROMOTION_FORM_TREFFEN"):
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_TREFFEN")):
										return True
						# Manipel
						elif iFormation == gc.getInfoTypeForString("PROMOTION_FORM_MANIPEL"):
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_MANIPEL")):
										return True
						# Phalanx-Arten (nur Speer)
						elif iFormation == gc.getInfoTypeForString("PROMOTION_FORM_SCHIEF"):
								if iUnitCombatType == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"):
										if pTeam.isHasTech(gc.getInfoTypeForString("TECH_PHALANX2")):
												return True
						elif iFormation == gc.getInfoTypeForString("PROMOTION_FORM_PHALANX2"):
								if iUnitCombatType == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"):
										if pTeam.isHasTech(gc.getInfoTypeForString("TECH_PHALANX2")):
												return True
						elif iFormation == gc.getInfoTypeForString("PROMOTION_FORM_PHALANX"):
								if iUnitCombatType == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"):
										if pTeam.isHasTech(gc.getInfoTypeForString("TECH_PHALANX")):
												return True
						# Geschlossene Formation (alle Melee)
						elif iFormation == gc.getInfoTypeForString("PROMOTION_FORM_CLOSED_FORM"):
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_CLOSED_FORM")):
										return True
						# Testudo
						elif iFormation == gc.getInfoTypeForString("PROMOTION_FORM_TESTUDO"):
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_TESTUDO")):
										if pUnit.getUnitType() in L.LTestudoUnits:
												return True
				# -- Drill end

				# Keil
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_KEIL"):
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KAMPFHUNDE")):
								return True
				# Zangenangriff
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_ZANGENANGRIFF"):
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_MILIT_STRAT")):
								return True
				# Flankenschutz (nur Speer)
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_FLANKENSCHUTZ"):
						if iUnitCombatType == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"):
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_TREFFEN")):
										return True
				# Elefantengasse (auch weiter unten fuer Bogen)
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_GASSE"):
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_GEOMETRIE2")):
								return True

		# Archers
		elif iUnitCombatType in L.LArcherCombats:
				# Fortress
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS") and pUnit.baseMoves() == 1:
						return True
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS2") and pUnit.baseMoves() > 1:
						return True
				# Elefantengasse (auch weiter unten fuer Bogen)
				if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_GASSE"):
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_GEOMETRIE2")):
								return True

		# Flucht
		if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_FLIGHT"):
				if pUnit.getDamage() >= 70:
						if iUnitCombatType in L.LFluchtCombats:
								if pUnit.baseMoves() == 1:
										return True
		if iFormation == gc.getInfoTypeForString("PROMOTION_FORM_LEADER_POSITION"):
				if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
						if pUnit.getDamage() < 25:
								return True

		return False
		# can do Formationen / Formations End ------

# PAE UNIT FORMATIONS ------------------------------


def doUnitFormation(pUnit, iNewFormation):
		pPlayer = gc.getPlayer(pUnit.getOwner())

		# Human
		if pPlayer.isHuman():
				# Fuer alle Einheiten dieser Gruppe
				unitGroup = pUnit.getGroup()
				iNumUnits = unitGroup.getNumUnits()
				for i in range(iNumUnits):
						loopUnit = unitGroup.getUnitAt(i)
						# Formation geben
						if iNewFormation != -1:
								if canDoFormation(loopUnit, iNewFormation):
										# Formationen auf NULL setzen
										for j in L.LFormationen:
												# if loopUnit.isHasPromotion(j):
												loopUnit.setHasPromotion(j, False)
										# Formation geben
										loopUnit.setHasPromotion(iNewFormation, True)
						# Formationen entfernen
						else:
								# Formationen auf NULL setzen
								for j in L.LFormationen:
										# if loopUnit.isHasPromotion(j):
										loopUnit.setHasPromotion(j, False)
		# AI
		else:
				# Formationen auf NULL setzen
				for j in L.LFormationen:
						# if loopUnit.isHasPromotion(j):
						pUnit.setHasPromotion(j, False)
				# Formation geben
				if iNewFormation != -1:
						pUnit.setHasPromotion(iNewFormation, True)


def doAIPlotFormations(pPlot, iPlayer):
		# bContinue = False
		pPlayer = gc.getPlayer(iPlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		bSupplyUnit = False
		bCity = False
		bElefant = False
		lPlayerUnits = []
		lMountedUnits = []
		iCountDamage = 0
		iStackStatus = 0
		# 0: > 75% stength: 80% offensive
		# 1: > 50% strength: 50% offensive
		# 2: > 25% strength: 10% offensive
		# 3: < 25% strength: flight

		# Naval or Land
		if pPlot.isWater():
				if not pTeam.isHasTech(gc.getInfoTypeForString("TECH_LOGIK")):
						return
		elif not pTeam.isHasTech(gc.getInfoTypeForString("TECH_BRANDSCHATZEN")):
				return

		# City
		iRange = 1
		iX = pPlot.getX()
		iY = pPlot.getY()
		for x in range(-iRange, iRange+1):
				for y in range(-iRange, iRange+1):
						loopPlot = plotXY(iX, iY, x, y)
						if loopPlot is not None and not loopPlot.isNone():
								if loopPlot.isCity():
										pCity = loopPlot.getPlotCity()
										if pCity.getOwner() != iPlayer:
												if pTeam.isAtWar(gc.getPlayer(pCity.getOwner()).getTeam()):
														bCity = True

		lUnitTypes = [
				# gc.getInfoTypeForString("UNITCOMBAT_MELEE"),
				gc.getInfoTypeForString("UNITCOMBAT_AXEMAN"),
				gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN"),
				gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"),
				gc.getInfoTypeForString("UNITCOMBAT_SKIRMISHER"),
				gc.getInfoTypeForString("UNITCOMBAT_ARCHER"),
				gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"),
				gc.getInfoTypeForString("UNITCOMBAT_NAVAL")
		]
		# Init Units
		iRange = pPlot.getNumUnits()
		for i in range(iRange):
				if pPlot.getUnit(i).getOwner() == iPlayer:
						if pPlot.getUnit(i).getUnitCombatType() in lUnitTypes:
								lPlayerUnits.append(pPlot.getUnit(i))
								# Supply
								if not bSupplyUnit:
										if pPlot.getUnit(i).isHasPromotion(gc.getInfoTypeForString("PROMOTION_MEDIC2")):
												bSupplyUnit = True
								iCountDamage += pPlot.getUnit(i).getDamage()

		# StackStatus
		iCountUnits = len(lPlayerUnits)
		iLimit = 0
		if iCountUnits > 0:
				if iCountUnits * 100 - iCountDamage > iCountUnits * 75:
						iStackStatus = 0
						iLimit = iCountUnits / 10 * 8
				elif iCountUnits * 100 - iCountDamage > iCountUnits * 50:
						iStackStatus = 1
						iLimit = iCountUnits / 2
				elif iCountUnits * 100 - iCountDamage > iCountUnits * 25:
						iStackStatus = 2
						iLimit = iCountUnits / 10
				else:
						iStackStatus = 3

				if iStackStatus == 3:
						for unit in lPlayerUnits:
								if unit.getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
										doUnitFormation(unit, gc.getInfoTypeForString("PROMOTION_FORM_FLIGHT"))
				else:
						i = 0
						for unit in lPlayerUnits:
								if not bSupplyUnit:
										if unit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
												if unit.getUnitType() not in L.LUnitWarAnimals:
														lMountedUnits.append(unit)
								if i <= iLimit:
										doAIUnitFormations(unit, True, bCity, bElefant)
								else:
										doAIUnitFormations(unit, False, bCity, bElefant)
								i += 1

						# Fourage - Supply
						if not bSupplyUnit:
								if lMountedUnits:
										iLevel = 10
										if pTeam.isHasTech(gc.getInfoTypeForString("TECH_BRANDSCHATZEN")):
												pUnit = lMountedUnits[0]
												for unit in lMountedUnits:
														if unit.getLevel() < iLevel:
																pUnit = unit
																iLevel = unit.getLevel()
												doUnitFormation(pUnit, gc.getInfoTypeForString("PROMOTION_FORM_FOURAGE"))


def doAIUnitFormations(pUnit, bOffensive, bCity, bElefant):
		if (pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MERCENARY"))
				or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS"))
						or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS2"))):
				return
		if pUnit.getUnitAIType() == UnitAITypes.UNITAI_ANIMAL or pUnit.getUnitAIType() == UnitAITypes.UNITAI_EXPLORE:
				return

		# AI great general
		if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
				if pUnit.plot().getNumUnits() > 1 and pUnit.getDamage() < 25:
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_FORM_LEADER_POSITION"), True)
						return

		lFormations = []

		# Naval
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_NAVAL"):
				if bOffensive:
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_KEIL"))
				else:
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_ZANGE"))
		else:
				# Mounted
				lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_PARTHER"))
				lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_KANTAKREIS"))
				if bOffensive:
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_KEIL"))
				# Melee
				if bCity and CvUtil.myRandom(2, "Testudo") == 0:
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_TESTUDO"))
				lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_KOHORTE"))
				# Elefantengasse
				if bElefant and (pUnit.getUnitCombatType() in L.LArcherCombats or CvUtil.myRandom(4, "Elefantengasse") == 0):
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_GASSE"))
				if bOffensive:
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_TREFFEN"))
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_MANIPEL"))
						# Schiefe Schlachtordnung
						if CvUtil.myRandom(2, "Schiefe Schlachtordnung") == 0:
								lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_SCHIEF"))
						# Manipular-Phalanx
						else:
								lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_PHALANX2"))
						# Phalanx
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_PHALANX"))
						# Geschlossene Formation (alle Melee mit Drill)
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_CLOSED_FORM"))
				# Defensive
				else:
						# Flankenschutz (nur Speer)
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_FLANKENSCHUTZ"))
						# Zangenangriff (dem Keil vorziehen)
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_ZANGENANGRIFF"))
				lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_SCHILDWALL"))
				# Archer, vor allem Skirmisher
				if bElefant:
						lFormations.append(gc.getInfoTypeForString("PROMOTION_FORM_GASSE"))

		if len(lFormations):
				# Max len() Versuche
				for i in lFormations:
						iRand = CvUtil.myRandom(len(lFormations), "doAIUnitFormations")
						iFormation = lFormations[iRand]
						if canDoFormation(pUnit, iFormation):
								doUnitFormation(pUnit, iFormation)
								return
# PAE UNIT FORMATIONS END ------------------------------


# PAE UNIT BATTLE PROMOTION
def doUnitGetsPromo(pUnitTarget, pUnitSource, pPlot, bMadeAttack, bOpponentAnimal):
		# Keine Seeeinheiten
		if pUnitTarget.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_NAVAL"):
				return False
		# Unit promos --------------------
		# UNITCOMBAT_ARCHER: PROMOTION_COVER1
		# UNITCOMBAT_SKIRMISHER: PROMOTION_PARADE_SKIRM1
		# UNITCOMBAT_AXEMAN: PROMOTION_PARADE_AXE1
		# UNITCOMBAT_SWORDSMAN: PROMOTION_PARADE_SWORD1
		# UNITCOMBAT_SPEARMAN: PROMOTION_PARADE_SPEAR1

		# UNITCOMBAT_CHARIOT: PROMOTION_AGAINST_CHARIOTS
		# UNITCOMBAT_MOUNTED: PROMOTION_AGAINST_MOUNTED
		# UNITCOMBAT_ELEPHANT: PROMOTION_AGAINST_ELEPHANTS
		# UNITCOMBAT_SIEGE: PROMOTION_CHARGE
		# Terrain promos -----------------
		# isHills: PROMOTION_GUERILLA1 - 5
		# FEATURE_FOREST, FEATURE_DICHTERWALD: PROMOTION_WOODSMAN1 - 5
		# FEATURE_JUNGLE: PROMOTION_JUNGLE1 - 5
		# TERRAIN_SWAMP: PROMOTION_SUMPF1 - 5
		# TERRAIN_DESERT: PROMOTION_DESERT1 - 5
		# Extra promos -------------------
		# City Attack: PROMOTION_CITY_RAIDER1 - 5
		# City Defense: PROMOTION_CITY_GARRISON1 - 5
		# isRiverSide(): PROMOTION_AMPHIBIOUS

		# pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DESERT")
		# pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_FOREST")
		# pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MELEE")

		iNewPromo = -1
		iPlayer = pUnitTarget.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		bCity = pPlot.isCity()

		lFirstPromos = [
				gc.getInfoTypeForString("PROMOTION_WOODSMAN1"),
				gc.getInfoTypeForString("PROMOTION_GUERILLA1"),
				gc.getInfoTypeForString("PROMOTION_DESERT1"),
				gc.getInfoTypeForString("PROMOTION_JUNGLE1"),
				gc.getInfoTypeForString("PROMOTION_SUMPF1"),
				gc.getInfoTypeForString("PROMOTION_CITY_RAIDER1"),
				gc.getInfoTypeForString("PROMOTION_CITY_GARRISON1")
		]
		iFirstPromos = 0
		for i in lFirstPromos:
				if pUnitTarget.isHasPromotion(i):
						iFirstPromos += 1

		iDivisor = 1
		# PAEInstanceFightingModifier for wins in the same turn
		if (iPlayer, pUnitTarget.getID()) in PAEInstanceFightingModifier:
				iDivisor = 5

		# Chances --- Inits -------------
		iChanceCityDefense = 10 / iDivisor
		iChanceUnitType = 10 / iDivisor
		iChanceTerrain = 15 / (iFirstPromos*2 + 1) / iDivisor
		# Static chance of Promo 2-5 of a terrain
		iChanceTerrain2 = 5 / iDivisor
		# -------------------------------

		# 1. chance: Either City or Open Field
		# City
		if bCity:
				iRand = CvUtil.myRandom(100, "cityPromo")
				if iChanceCityDefense > iRand:
						if bMadeAttack:
								# Attacker
								if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_CITY_RAIDER5")):
										for iPromo in L.LCityRaider:
												if not pUnitTarget.isHasPromotion(iPromo):
														iNewPromo = iPromo
														break
										iChanceUnitType = iChanceUnitType / 2
										# Trait Conquereror / Eroberer: Automatische Heilung bei Stadtangriffs-Promo / auto-healing when receiving city raider promo
										# if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_EROBERER")):
										#    pUnitTarget.setDamage(0, -1)
						# Defender
						else:
								if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_CITY_GARRISON5")):
										for iPromo in L.LCityGarrison:
												if not pUnitTarget.isHasPromotion(iPromo):
														iNewPromo = iPromo
														break
										iChanceUnitType = iChanceUnitType / 2
										# Trait Protective: Automatische Heilung bei Stadtverteidigungs-Promo / auto-healing when receiving city garrison promo
										# if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_PROTECTIVE")):
										#    pUnitTarget.setDamage(0, -1)

		# on open field
		else:
				iRandTerrain = CvUtil.myRandom(100, "fieldPromo")
				if iChanceTerrain > iRandTerrain:
						# either hill, terrain or feature, river
						# init unit promos and terrains
						lTerrain = []
						if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_GUERILLA5")) and pPlot.isHills():
								lTerrain.append("Hills")

						# thx to Dertuek:
						if bMadeAttack and pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT3")):
								if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_AMPHIBIOUS")):
										pPlotAttack = pUnitTarget.plot()
										pPlotDefense = pUnitSource.plot()
										if pPlotAttack.isWater() and not pPlotDefense.isWater():
												lTerrain.append("River")
										elif pPlotAttack.isRiverSide():
												if pPlotAttack.isRiverCrossing(directionXYFromPlot(pPlotAttack, pPlotDefense)):
														lTerrain.append("River")

						# old source code
						# if pPlot.isRiverSide() and bMadeAttack:
						#  if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_AMPHIBIOUS")):
						#    if pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT3")):
						#      lTerrain.append("River")

						if pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DESERT"):
								if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DESERT5")):
										lTerrain.append("Desert")

						# Forest, Jungle and Swamp nicht fuer Mounted
						if (not pUnitTarget.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_CHARIOT")
								and not pUnitTarget.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED")
								and not pUnitTarget.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_ELEPHANT")
										and not pUnitTarget.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SIEGE")):
								if pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_FOREST") or pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_DICHTERWALD"):
										if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_WOODSMAN5")):
												lTerrain.append("Forest")
								elif pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_JUNGLE"):
										if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_JUNGLE5")):
												lTerrain.append("Jungle")
								elif pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_SWAMP"):
										if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SUMPF5")):
												lTerrain.append("Swamp")

						if lTerrain:
								iChanceUnitType = iChanceUnitType / 2
								iRand = CvUtil.myRandom(len(lTerrain), "terrainPromo")
								lPromos = []
								if lTerrain[iRand] == "River":
										iNewPromo = gc.getInfoTypeForString("PROMOTION_AMPHIBIOUS")
								else:
										if lTerrain[iRand] == "Hills":
												lPromos = L.LGuerilla
										elif lTerrain[iRand] == "Forest":
												lPromos = L.LWoodsman
										elif lTerrain[iRand] == "Jungle":
												lPromos = L.LJungle
										elif lTerrain[iRand] == "Swamp":
												lPromos = L.LSwamp
										elif lTerrain[iRand] == "Desert":
												lPromos = L.LDesert

										for iPromo in lPromos:
												if not pUnitTarget.isHasPromotion(iPromo):
														iNewPromo = iPromo
														break

								# Chances of Promos 2-5
								if iNewPromo not in lFirstPromos and iRandTerrain >= iChanceTerrain2:
										iNewPromo = -1

		if iNewPromo != -1:
				if not bOpponentAnimal or iNewPromo in lFirstPromos:
						# naechste Chance verringern
						iChanceUnitType = iChanceUnitType / 2
						pUnitTarget.setHasPromotion(iNewPromo, True)
						PAEInstanceFightingModifier.append((pUnitTarget.getOwner(), pUnitTarget.getID()))
						if gc.getPlayer(pUnitTarget.getOwner()).isHuman():
								CyInterface().addMessage(pUnitTarget.getOwner(), True, 10,
									CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_PROMOTION", (pUnitTarget.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
									"AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pUnitTarget.getX(), pUnitTarget.getY(), True, True)

		# 2. chance: enemy combat type
		iNewPromo = -1
		iRand = CvUtil.myRandom(100, "combatTypePromo")
		if iChanceUnitType > iRand:
				iChanceUnitType = iChanceUnitType / 2
				if pUnitSource.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_ARCHER"):
						if pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COVER2")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_COVER3")
						elif pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COVER1")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_COVER2")
						elif not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COVER1")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_COVER1")

				elif pUnitSource.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SKIRMISHER"):
						if pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_SKIRM2")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_SKIRM3")
						elif pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_SKIRM1")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_SKIRM2")
						elif not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_SKIRM1")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_SKIRM1")

				# elif pUnitSource.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MELEE"):
				#  if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SHOCK2")):  iNewPromo = gc.getInfoTypeForString("PROMOTION_SHOCK2")
				#  elif not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SHOCK")): iNewPromo = gc.getInfoTypeForString("PROMOTION_SHOCK")

				elif pUnitSource.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_AXEMAN"):
						if pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_AXE2")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_AXE3")
						elif pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_AXE1")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_AXE2")
						elif not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_AXE1")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_AXE1")

				elif pUnitSource.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN"):
						if pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_SWORD2")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_SWORD3")
						elif pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_SWORD1")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_SWORD2")
						elif not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_SWORD1")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_SWORD1")

				elif pUnitSource.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"):
						if pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_SPEAR2")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_SPEAR3")
						elif pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_SPEAR1")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_SPEAR2")
						elif not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PARADE_SPEAR1")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_PARADE_SPEAR1")

				elif pUnitSource.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_CHARIOT"):
						if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_AGAINST_CHARIOTS")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_AGAINST_CHARIOTS")
				elif pUnitSource.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
						if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_AGAINST_MOUNTED")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_AGAINST_MOUNTED")
				elif pUnitSource.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_ELEPHANT"):
						if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_AGAINST_ELEPHANTS")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_AGAINST_ELEPHANTS")
				elif pUnitSource.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SIEGE"):
						if not pUnitTarget.isHasPromotion(gc.getInfoTypeForString("PROMOTION_CHARGE")):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_CHARGE")

				if iNewPromo != -1:
						pUnitTarget.setHasPromotion(iNewPromo, True)
						PAEInstanceFightingModifier.append((iPlayer, pUnitTarget.getID()))
						if pPlayer.isHuman():
								CyInterface().addMessage(iPlayer, True, 10,
									CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_PROMOTION", (pUnitTarget.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
									"AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pUnitTarget.getX(), pUnitTarget.getY(), True, True)
						return True

		# PAE 7.11 (25.08.25): Chance für Kommandanten der römischen Spätantike (Comes)
		if iNewPromo == -1:
			LRome = [
				gc.getInfoTypeForString("CIVILIZATION_ROME"),
				gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS")
			]
			if pPlayer.getCivilizationType() in LRome:
				iRand = CvUtil.myRandom(100, "combatTypePromoComes")
				if iChanceUnitType > iRand:
					if pUnitTarget.getUnitType() == gc.getInfoTypeForString("UNIT_ROME_PROTECTORES"):
						iNewPromo = gc.getInfoTypeForString("PROMOTION_PROTECTOR")
					elif pUnitTarget.getUnitType() == gc.getInfoTypeForString("UNIT_ROME_EXCUBITORES"):
						iNewPromo = gc.getInfoTypeForString("PROMOTION_EXCUBITOR")
					if iNewPromo != -1:
						pUnitTarget.setHasPromotion(iNewPromo, True)
						PAEInstanceFightingModifier.append((iPlayer, pUnitTarget.getID()))
						if pPlayer.isHuman():
								CyInterface().addMessage(iPlayer, True, 10,
									CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_PROMOTION", (pUnitTarget.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
									"AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pUnitTarget.getX(), pUnitTarget.getY(), True, True)

		return False


def doRetireVeteran(pUnit):
		lPromos = [
				gc.getInfoTypeForString("PROMOTION_COMBAT3"),
				gc.getInfoTypeForString("PROMOTION_COMBAT4"),
				gc.getInfoTypeForString("PROMOTION_COMBAT5"),
				gc.getInfoTypeForString("PROMOTION_COMBAT6"),
				gc.getInfoTypeForString("PROMOTION_MORAL_NEG1"),
				gc.getInfoTypeForString("PROMOTION_MORAL_NEG2"),
				gc.getInfoTypeForString("PROMOTION_MORAL_NEG3"),
				gc.getInfoTypeForString("PROMOTION_MORAL_NEG4"),
				gc.getInfoTypeForString("PROMOTION_MORAL_NEG5")
		]
		# lPromos.append(gc.getInfoTypeForString("PROMOTION_HERO"))
		for iPromo in lPromos:
				if pUnit.isHasPromotion(iPromo):
						pUnit.setHasPromotion(iPromo, False)

		# Reduce XP
		pUnit.setExperience(pUnit.getExperience() / 2, -1)
		# Reduce Lvl: deactivated
		# if pUnit.getLevel() > 3:
		#  pUnit.setLevel(pUnit.getLevel() - 3)
		# else:
		#  pUnit.setLevel(1)


def doMobiliseFortifiedArmy(pCity):
		# PAE V ab Patch 3: Wenn Hauptstadt angegriffen wird, sollen alle Einheiten in Festungen remobilisiert werden (Promo FORTRESS)
		# PAE 6.6: auch bei normalen Städten, wenn im Umkreis eine Festung ist

		# PAE 6.6: ausser Barbaren
		if pCity.getOwner() == gc.getBARBARIAN_PLAYER():
				return

		pPlayer = gc.getPlayer(pCity.getOwner())
		if pCity is not None:
				iX = pCity.getX()
				iY = pCity.getY()
				iPromoFort = gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS")
				iPromoFort2 = gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS2")

				if pCity.isCapital():
						(pUnit, pIter) = pPlayer.firstUnit(False)
						while pUnit:
								pUnit.setHasPromotion(iPromoFort, False)
								pUnit.setHasPromotion(iPromoFort2, False)
								pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iX, iY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
								(pUnit, pIter) = pPlayer.nextUnit(pIter, False)
				else:
						iCityOwner = pCity.getOwner()
						iRange = 4  # Radius
						for x in range(-iRange, iRange+1):
								for y in range(-iRange, iRange+1):
										loopPlot = plotXY(iX, iY, x, y)
										if loopPlot.getImprovementType() in L.LImprFortSentry:
												iRange2 = loopPlot.getNumUnits()
												for iLoopUnit in range(iRange2):
														pUnit = loopPlot.getUnit(iLoopUnit)
														if pUnit:
																if pUnit.getOwner() == iCityOwner:
																		pUnit.setHasPromotion(iPromoFort, False)
																		pUnit.setHasPromotion(iPromoFort2, False)
																		pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iX, iY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)

# Handelsposten errichten (soll kein Gold kosten ab PAE 6.5.2)
# Grund: Strassen kosten Geld, Einheit kostet Geld (indirekt beim Bau, pro Runde)
def doBuildHandelsposten(pUnit):
		#iPrice = 25
		iPlayer = pUnit.getOwner()
		# pPlayer = gc.getPlayer(iPlayer)
		# if pPlayer.getGold() < iPrice:
		#    # TODO: eigener Text
		#    CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TRADE_COLLECT_NO_GOODS", ("",)), None, 2, "Art/Interface/PlotPicker/Warning.dds", ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
		#    return
		pPlot = pUnit.plot()
		# Fix by Dertuek
		if pPlot.getRouteType() == -1:
				pPlot.setRouteType(0)
		pPlot.setImprovementType(gc.getInfoTypeForString("IMPROVEMENT_HANDELSPOSTEN"))
		CvUtil.addScriptData(pPlot, "p", iPlayer)
		pPlot.setCulture(iPlayer, 1, True)
		pPlot.setOwner(iPlayer)
		# pPlayer.changeGold(-iPrice)
		# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
		pUnit.kill(True, -1)  # RAMK_CTD

# isHills: PROMOTION_GUERILLA1
# FEATURE_FOREST, FEATURE_DICHTERWALD: PROMOTION_WOODSMAN1
# FEATURE_JUNGLE: PROMOTION_JUNGLE1
# TERRAIN_SWAMP: PROMOTION_SUMPF1
# TERRAIN_DESERT: PROMOTION_DESERT1
# City Attack: PROMOTION_CITY_RAIDER1
# City Defense: PROMOTION_CITY_GARRISON1
# isRiverSide: PROMOTION_AMPHIBIOUS

# PAE CITY builds UNIT -> auto promotions (land units)
def doCityUnitPromotions(pCity, pUnit):
		initChanceCity = 1  # ab Stadt: Chance * City Pop
		initChance = 2      # Chance * Plots
		# initChanceRiver = 2 # for PROMOTION_AMPHIBIOUS only
		# --------------
		# iCityAttack = 0
		# iCityDefense = 0
		iHills = 0
		iForest = 0
		iJungle = 0
		iSwamp = 0
		iDesert = 0
		# iRiver = 0

		iMinAnz = 2  # Mindestanzahl an Plots notwendig

		# not for rams
		lRams = [
				gc.getInfoTypeForString("UNIT_RAM"),
				gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
				gc.getInfoTypeForString("UNIT_BATTERING_RAM2")
		]
		if pUnit.getUnitType() in lRams:
				return

		if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STADT")):
				if pCity.getPopulation() * initChanceCity > CvUtil.myRandom(100, "doCityUnitPromotions1"):
						if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_ARCHER"):
								iPromoGarrison = gc.getInfoTypeForString("PROMOTION_CITY_GARRISON1")
								if not pUnit.isHasPromotion(iPromoGarrison):
										doGiveUnitPromo(pUnit, iPromoGarrison, pCity)
										return
						elif pUnit.getUnitCombatType() in [gc.getInfoTypeForString("UNITCOMBAT_AXEMAN"), gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN")]:
								iPromoRaider = gc.getInfoTypeForString("PROMOTION_CITY_RAIDER1")
								if not pUnit.isHasPromotion(iPromoRaider):
										doGiveUnitPromo(pUnit, iPromoRaider, pCity)
										return

		# Blessed Units
		#iBuilding = gc.getInfoTypeForString("BUILDING_CHRISTIAN_CATHEDRAL")
		#if pCity.isHasBuilding(iBuilding):
		#		# Chance: 25% a unit gets blessed
		#		if CvUtil.myRandom(4, "unit_gets_blessed") == 1:
		#				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_BLESSED"), True)
		# PAE VI 6.12d
		eMardukPriest = gc.getInfoTypeForString("UNIT_MARDUK_PRIEST")
		pPlot = pCity.plot()
		iRange = pPlot.getNumUnits()
		for iUnit in range(iRange):
				loopUnit = pPlot.getUnit(iUnit)
				if loopUnit.getUnitType() == eMardukPriest:
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_BLESSED"), True)
						break

		# Start seeking plots for promos. Nur umliegende Plots!
		# for i in range(3):
		#  for j in range(3):
		#    pLoopPlot = gc.getMap().plot(pCity.getX() + i - 1, pCity.getY() + j - 1)
		iRange = gc.getNUM_CITY_PLOTS() - 12
		for iI in range(iRange):
				pLoopPlot = pCity.getCityIndexPlot(iI)
				if pLoopPlot is not None and not pLoopPlot.isNone():
						if pLoopPlot.isPeak():
								continue
						if pLoopPlot.isHills():
								iHills += 1
						#if pLoopPlot.isRiverSide(): iRiver += 1
						if pLoopPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DESERT"):
								iDesert += 1
						elif pLoopPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_SWAMP"):
								iSwamp += 1
						if pLoopPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_FOREST"):
								iForest += 1
						elif pLoopPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_DICHTERWALD"):
								iForest += 1
						elif pLoopPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_JUNGLE"):
								iJungle += 1

		# River - deactivated
		# if iRiver > 0:
		#  iRand = CvUtil.myRandom(100, "doCityUnitPromotions2")
		#  if iRiver * initChanceRiver > iRand:
		#    if not pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_AMPHIBIOUS")): doGiveUnitPromo(pUnit, gc.getInfoTypeForString("PROMOTION_AMPHIBIOUS"), pCity)

		# PAE V Patch 7: nur 1 Terrain Promo soll vergeben werden
		lPossiblePromos = []

		# Hills
		iPromoHills = gc.getInfoTypeForString("PROMOTION_GUERILLA1")
		if iHills >= iMinAnz and iHills * initChance > CvUtil.myRandom(100, "doCityUnitPromotions3"):
				if not pUnit.isHasPromotion(iPromoHills):
						lPossiblePromos.append(iPromoHills)

		# Desert
		iPromoDesert = gc.getInfoTypeForString("PROMOTION_DESERT1")
		if iDesert >= iMinAnz and iDesert * initChance > CvUtil.myRandom(100, "doCityUnitPromotions4"):
				if not pUnit.isHasPromotion(iPromoDesert):
						lPossiblePromos.append(iPromoDesert)

		# Forest
		iPromoForest = gc.getInfoTypeForString("PROMOTION_WOODSMAN1")
		if iForest >= iMinAnz and iForest * initChance > CvUtil.myRandom(100, "doCityUnitPromotions5"):
				if not pUnit.isHasPromotion(iPromoForest):
						lPossiblePromos.append(iPromoForest)

		# Swamp
		iPromoSumpf = gc.getInfoTypeForString("PROMOTION_SUMPF1")
		if iSwamp >= iMinAnz and iSwamp * initChance > CvUtil.myRandom(100, "doCityUnitPromotions6"):
				if not pUnit.isHasPromotion(iPromoSumpf):
						lPossiblePromos.append(iPromoSumpf)

		# Jungle
		iPromoJungle = gc.getInfoTypeForString("PROMOTION_JUNGLE1")
		if iJungle >= iMinAnz and iJungle * initChance > CvUtil.myRandom(100, "doCityUnitPromotions7"):
				if not pUnit.isHasPromotion(iPromoJungle):
						lPossiblePromos.append(iPromoJungle)

		# only 1 of the pot
		if lPossiblePromos:
				iPromo = lPossiblePromos[CvUtil.myRandom(len(lPossiblePromos), "doCityUnitPromotions8")]
				doGiveUnitPromo(pUnit, iPromo, pCity)

# PAE CITY builds UNIT -> auto promotions (ships)
def doCityUnitPromotions4Ships(pCity, pUnit):
		initChance = 5
		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		iWater = 0
		# Start seeking plots for promos
		for iI in range(gc.getNUM_CITY_PLOTS()):
				pLoopPlot = pCity.getCityIndexPlot(iI)
				if pLoopPlot is not None and not pLoopPlot.isNone():
						if pLoopPlot.getFeatureType() == iDarkIce:
								continue
						if pLoopPlot.isWater():
								iWater += 1

		if iWater > 3:
				iRand = CvUtil.myRandom(100, "doCityUnitPromotions4Ships")
				if iWater * initChance > iRand:
						iPromo = gc.getInfoTypeForString("PROMOTION_NAVIGATION1")
						if not pUnit.isHasPromotion(iPromo):
								doGiveUnitPromo(pUnit, iPromo, pCity)


def doGiveUnitPromo(pUnit, iNewPromo, pCity):
		pUnit.setHasPromotion(iNewPromo, True)
		iPlayer = pUnit.getOwner()
		if gc.getPlayer(iPlayer).isHuman():
				if iNewPromo == gc.getInfoTypeForString("PROMOTION_CITY_GARRISON1") or iNewPromo == gc.getInfoTypeForString("PROMOTION_CITY_RAIDER1"):
						CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_PROMOTION_3", (pUnit.getName(), gc.getPromotionInfo(iNewPromo).getDescription(), pCity.getName())),
																		 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pUnit.getX(), pUnit.getY(), True, True)
				else:
						CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_PROMOTION_2", (pUnit.getName(), gc.getPromotionInfo(iNewPromo).getDescription(), pCity.getName())),
																		 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pUnit.getX(), pUnit.getY(), True, True)

# ++++++++ Names for Legions +++++++++++++++++
# Reusing names of fallen Legions


def setLegionName(pUnit):
		pPlayer = gc.getPlayer(pUnit.getOwner())

		LegioUsedNames = []
		(loopUnit, pIter) = pPlayer.firstUnit(False)
		while loopUnit:
				sName = loopUnit.getName()
				if "Legio" in sName:
						LegioUsedNames.append(re.sub(r" \(.*?\)", "", sName))
				(loopUnit, pIter) = pPlayer.nextUnit(pIter, False)

		for sName in L.LegioNames:
				if sName not in LegioUsedNames:
						pUnit.setName(sName)
						break

# 752, iData2 = 0
def doBlessUnits(pUnit):
		pPlayer = gc.getPlayer(pUnit.getOwner())
		iPromo = gc.getInfoTypeForString("PROMOTION_BLESSED")
		iCost = 30

		# Fuer alle Einheiten dieser Gruppe
		unitGroup = pUnit.getGroup()
		iNumUnits = unitGroup.getNumUnits()
		for i in range(iNumUnits):
				if pPlayer.getGold() < iCost:
						break

				loopUnit = unitGroup.getUnitAt(i)
				if not loopUnit.isHasPromotion(iPromo):
						# Gold abziehen
						pPlayer.changeGold(-iCost)
						# Promo geben
						loopUnit.setHasPromotion(iPromo, True)
						loopUnit.finishMoves()

# onModNetMessage 759, iTyp (1: Rhetorik, 2: Sklavenopfer, 3: Zeus)
def doMoralUnits(pUnit, iTyp):
		pPlayer = gc.getPlayer(pUnit.getOwner())
		iPromo = gc.getInfoTypeForString("PROMOTION_MORALE")
		iUnits = 0
		iAnz = 0
		pPlot = pUnit.plot()
		iNumUnits = pPlot.getNumUnits()
		for iUnit in range(iNumUnits):
				loopUnit = pPlot.getUnit(iUnit)
				if loopUnit != pUnit:
						if loopUnit.getOwner() == pUnit.getOwner():
								if not loopUnit.isHasPromotion(iPromo):
										if loopUnit.isMilitaryHappiness():
												if pUnit.getID() != loopUnit.getID():
														iUnits += 1
														# Promo geben: Chance 1:4
														if iTyp != 1 or CvUtil.myRandom(4, "doMoralUnits") == 1:
																doMoralUnit(loopUnit)
																iAnz += 1
														loopUnit.finishMoves()

		if pPlayer.isHuman():
				if iTyp == 2:
						txt = CyTranslator().getText("TXT_KEY_MESSAGE_DRUIDE_SACRIFICE_MORALE", ())
				else:
						txt = CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_MORALE", (iAnz, iUnits))
				CyInterface().addMessage(pUnit.getOwner(), True, 8, txt, "", 2, "", ColorTypes(8), -1, -1, False, False)


# onModNetMessage 760, doMoralUnits
# onModNetMessage 752, iData2 = 1
def doMoralUnit(pUnit):
		if pUnit != None:
				if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG5")):
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG5"), False)
				elif pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG4")):
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG4"), False)
				elif pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG3")):
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG3"), False)
				elif pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG2")):
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG2"), False)
				elif pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG1")):
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG1"), False)
				elif pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_ANGST")):
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ANGST"), False)
				else:
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORALE"), True)


def doMoralUnitsAI(pUnit):
		# pPlayer = gc.getPlayer(pUnit.getOwner())
		iPromo = gc.getInfoTypeForString("PROMOTION_MORALE")
		pPlot = pUnit.plot()
		iNumUnits = pPlot.getNumUnits()
		for iUnit in range(iNumUnits):
				loopUnit = pPlot.getUnit(iUnit)
				if loopUnit != pUnit:
						if loopUnit.getOwner() == pUnit.getOwner():
								if not loopUnit.isHasPromotion(iPromo):
										if loopUnit.isMilitaryHappiness():
												doMoralUnitAI(loopUnit)


def doMoralUnitAI(pUnit):
		if pUnit != None:
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG5"), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG4"), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG3"), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG2"), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORAL_NEG1"), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ANGST"), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MORALE"), True)

# PAE Angst - EventManager: onCombatResult
def doCheckAngst(pWinnerUnit, pLoserUnit):
		# pWinnerPlot = pWinnerUnit.plot()
		# pLoserPlot = pLoserUnit.plot()

		bW = pWinnerUnit.getUnitCombatType() in L.LAngstUnits  # if winner is Angst Unit
		bL = pLoserUnit.getUnitCombatType() in L.LAngstUnits  # if Loser is Angst Unit
		# bWG = isPlotHasAngstUnits(pWinnerUnit) # winner's group/stack
		bLG = isPlotHasAngstUnits(pLoserUnit)  # loser's group/stack

		if bW or not bW and bL:

				# unset Angst
				if doSetAngst(pWinnerUnit, False):
						if gc.getPlayer(pWinnerUnit.getOwner()).isHuman():
								# Der Sieg der Einheit %s hat unseren Truppen die Angst genommen.
								CyInterface().addMessage(pWinnerUnit.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_ANGST_3", (pWinnerUnit.getName(),)), "AS2D_WELOVEKING", 2,
																				 gc.getPromotionInfo(gc.getInfoTypeForString("PROMOTION_ANGST")).getButton(), ColorTypes(8), pWinnerUnit.getX(), pWinnerUnit.getY(), True, True)
						elif gc.getPlayer(pLoserUnit.getOwner()).isHuman():
								# Der Sieg der Einheit %s hat den gegnerischen Truppen die Angst genommen.
								CyInterface().addMessage(pLoserUnit.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_ANGST_4", (pWinnerUnit.getName(),)), "AS2D_CITY_REVOLT", 2,
																				 gc.getPromotionInfo(gc.getInfoTypeForString("PROMOTION_ANGST")).getButton(), ColorTypes(7), pWinnerUnit.getX(), pWinnerUnit.getY(), True, True)

				# set Angst
				if bW and not bLG:
						if doSetAngst(pLoserUnit, True):
								if gc.getPlayer(pLoserUnit.getOwner()).isHuman():
										# Die Art der gegnerischen Kriegsführung jagt unseren Truppen Angst ein!
										CyInterface().addMessage(pLoserUnit.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_ANGST_1", ("",)), "AS2D_WELOVEKING", 2,
																						 gc.getPromotionInfo(gc.getInfoTypeForString("PROMOTION_ANGST")).getButton(), ColorTypes(7), pLoserUnit.getX(), pLoserUnit.getY(), True, True)
								elif gc.getPlayer(pWinnerUnit.getOwner()).isHuman():
										# Die Art unserer Kriegsführung jagt den gegnerischen Truppen Angst ein!
										CyInterface().addMessage(pWinnerUnit.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_ANGST_2", ("",)), "AS2D_CITY_REVOLT", 2,
																						 gc.getPromotionInfo(gc.getInfoTypeForString("PROMOTION_ANGST")).getButton(), ColorTypes(8), pLoserUnit.getX(), pLoserUnit.getY(), True, True)


def isPlotHasAngstUnits(pUnit):
		pPlot = pUnit.plot()
		iNumUnits = pPlot.getNumUnits()
		if iNumUnits > 1:
				for iUnit in range(iNumUnits):
						loopUnit = pPlot.getUnit(iUnit)
						if loopUnit.isMilitaryHappiness():
								if loopUnit.getUnitCombatType() in L.LAngstUnits:
										if loopUnit.getID() != pUnit.getID():
												return True
		return False


def doSetAngst(pUnit, bSet):
		bInfo = False
		iPromo = gc.getInfoTypeForString("PROMOTION_ANGST")
		pPlot = pUnit.plot()
		iNumUnits = pPlot.getNumUnits()
		for iUnit in range(iNumUnits):
				loopUnit = pPlot.getUnit(iUnit)
				if loopUnit.getOwner() == pUnit.getOwner():
						if loopUnit.isMilitaryHappiness():
								if not loopUnit.isDead():
										if (bSet and not loopUnit.isHasPromotion(iPromo) or not bSet and loopUnit.isHasPromotion(iPromo)):
												loopUnit.setHasPromotion(iPromo, bSet)
												bInfo = True
		return bInfo
# PAE Angst Ende --------------------

# onModNetMessage 760, doGetXPbySlave
def doKillSlaveFromPlot(pUnit):
		iUnitOwner = pUnit.getOwner()
		iUnitSlave = gc.getInfoTypeForString("UNIT_SLAVE")
		pPlot = pUnit.plot()
		iRange = pPlot.getNumUnits()
		for iUnit in range(iRange):
				loopUnit = pPlot.getUnit(iUnit)
				if loopUnit.getUnitType() == iUnitSlave and loopUnit.getOwner() == iUnitOwner:
						loopUnit.kill(True, -1)
						break

# onModNetMessage 761
def doGetXPbySlave(pUnit):
		# Sklave killen
		doKillSlaveFromPlot(pUnit)

		# Unit gewinnt oder verliert, je nach Schaden
		iDamage = CvUtil.myRandom(100, "doGetXPbySlave")
		iUnitDamage = pUnit.getDamage()

		if iUnitDamage + iDamage > 99:
				if gc.getPlayer(pUnit.getOwner()).isHuman():
						txt = CyTranslator().getText("TXT_KEY_GET_XP_BY_SLAVE_LOSE", ())
						CyInterface().addMessage(pUnit.getOwner(), True, 8, txt, "", 2, "", ColorTypes(7), -1, -1, False, False)
				pUnit.kill(True, -1)
		else:
				# XP geben
				pUnit.setExperience(pUnit.getExperience() + 1, -1)
				if gc.getPlayer(pUnit.getOwner()).isHuman():
						txt = CyTranslator().getText("TXT_KEY_GET_XP_BY_SLAVE_WIN", ())
						CyInterface().addMessage(pUnit.getOwner(), True, 8, txt, "", 2, "", ColorTypes(8), -1, -1, False, False)
				# Einheit verletzen
				pUnit.setDamage(iUnitDamage + iDamage, -1)
				pUnit.finishMoves()
				# next unit
				doGoToNextUnit(pUnit)


def doUnitGetsHero(pWinner, pLoser):
		iWinnerPlayer = pWinner.getOwner()
		pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
		iPromoHero = gc.getInfoTypeForString("PROMOTION_HERO")
		iPromoLeader = gc.getInfoTypeForString("PROMOTION_LEADER")
		pWinner.setExperience(pWinner.getExperience()+3, -1)
		if not pWinner.isHasPromotion(iPromoHero):
				pWinner.setHasPromotion(iPromoHero, True)
				if pWinnerPlayer.isHuman():
						if pLoser.isHasPromotion(iPromoLeader):
								txtPopUpHero = CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_HERO_3", (pWinner.getName(), pLoser.getName()))
								CyInterface().addMessage(iWinnerPlayer, True, 10, txtPopUpHero, "AS2D_WELOVEKING", 2, pWinner.getButton(), ColorTypes(8), pWinner.getX(), pWinner.getY(), True, True)
						else:
								txtPopUpHero = CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_HERO_4", (pWinner.getName(), 0))
								CyInterface().addMessage(iWinnerPlayer, True, 10, txtPopUpHero, "AS2D_WELOVEKING", 2, pWinner.getButton(), ColorTypes(8), pWinner.getX(), pWinner.getY(), True, True)
				return True
		return False


def getExperienceForLeader(pWinner, pLoser, bPromoHero):
		iWinnerPlayer = pWinner.getOwner()
		pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
		iPromoHero = gc.getInfoTypeForString("PROMOTION_HERO")
		iPromoLeader = gc.getInfoTypeForString("PROMOTION_LEADER")
		bLeaderAnwesend = False
		pWinnerPlot = pWinner.plot()
		iNumUnits = pWinnerPlot.getNumUnits()
		for i in range(iNumUnits):
				pLoopUnit = pWinnerPlot.getUnit(i)
				if pLoopUnit.getOwner() == iWinnerPlayer:
						if pLoopUnit.isHasPromotion(iPromoLeader):
								bLeaderAnwesend = True
								# XP
								if CvUtil.myRandom(10, "XP") == 0:
										pLoopUnit.setExperience(pLoopUnit.getExperience() + 1, -1)
								# First general in stack who doesnt possess hero promo gets it
								if bPromoHero:
										if not pLoopUnit.isHasPromotion(iPromoHero):
												pLoopUnit.setHasPromotion(iPromoHero, True)
												bPromoHero = False
												if pWinnerPlayer.isHuman():
														if pLoser.isHasPromotion(iPromoLeader):
																txtPopUpHero = CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_HERO_1", (pLoopUnit.getName(), pLoser.getName()))
																CyInterface().addMessage(iWinnerPlayer, True, 10, txtPopUpHero, "AS2D_WELOVEKING", 2, pLoopUnit.getButton(), ColorTypes(8), pWinner.getX(), pWinner.getY(), True, True)
														else:
																txtPopUpHero = CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_HERO_2", (pLoopUnit.getName(), 0))
																CyInterface().addMessage(iWinnerPlayer, True, 10, txtPopUpHero, "AS2D_WELOVEKING", 2, pLoopUnit.getButton(), ColorTypes(8), pWinner.getX(), pWinner.getY(), True, True)
		return bLeaderAnwesend

def isLeaderAnwesend(iPlayer,pPlot):
		iPromo = gc.getInfoTypeForString("PROMOTION_LEADER")
		iNumUnits = pPlot.getNumUnits()
		for i in range(iNumUnits):
				pLoopUnit = pPlot.getUnit(i)
				if pLoopUnit.getOwner() == iPlayer and pLoopUnit.isHasPromotion(iPromo):
						return True
		return False

def isHeroAnwesend(iPlayer,pPlot):
		iPromo = gc.getInfoTypeForString("PROMOTION_HERO")
		iNumUnits = pPlot.getNumUnits()
		for i in range(iNumUnits):
				pLoopUnit = pPlot.getUnit(i)
				if pLoopUnit.getOwner() == iPlayer and pLoopUnit.isHasPromotion(iPromo):
						return True
		return False

def removeMercenaryPromo(pWinner):
		iPlayer = pWinner.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iPromo = gc.getInfoTypeForString("PROMOTION_MERCENARY")
		if pWinner.isHasPromotion(iPromo):
				iChance = 2
				if isLeaderAnwesend(iPlayer,pWinner.plot()) or isHeroAnwesend(iPlayer,pWinner.plot()):
						iChance = 5
				
				if iChance > CvUtil.myRandom(10, "removing Mercenary promo"):
						pWinner.setHasPromotion(iPromo, False)
						if pPlayer.isHuman():
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_HERO_6", (pWinner.getName(),)),
								"AS2D_WELOVEKING", 2, pWinner.getButton(), ColorTypes(8), pWinner.getX(), pWinner.getY(), True, True)


def doHunterHero(pWinner, pLoser):
		iWinnerPlayer = pWinner.getOwner()
		pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
		iPromoHero = gc.getInfoTypeForString("PROMOTION_HERO")
		if gc.getUnitInfo(pWinner.getUnitType()).getCombat() < gc.getUnitInfo(pLoser.getUnitType()).getCombat():
				if pLoser.getUnitType() == gc.getInfoTypeForString("UNIT_UR") or pLoser.getLevel() > 4:
						if pLoser.isDead():
								if not pWinner.isHasPromotion(iPromoHero):
										pWinner.setHasPromotion(iPromoHero, True)
										pWinner.changeExperience(3, -1, 1, 0, 0)
										if pWinnerPlayer.isHuman():
												txtPopUpHero = CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_GETS_HERO_5", (pWinner.getName(), pLoser.getName()))
												CyInterface().addMessage(iWinnerPlayer, True, 10, txtPopUpHero, "AS2D_WELOVEKING", 2, pWinner.getButton(), ColorTypes(8), pWinner.getX(), pWinner.getY(), True, True)

												popupInfo = CyPopupInfo()
												popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)  # Text PopUp only!
												popupInfo.setText(txtPopUpHero)
												popupInfo.addPopup(iWinnerPlayer)

# Unit rang / Dienstgrade / unit ranking / rang promo / promo rang
def doRankPromo(pWinner):
		iWinnerPlayer = pWinner.getOwner()
		pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
		pWinnerTeam = gc.getTeam(pWinnerPlayer.getTeam())
		iWinnerCiv = pWinnerPlayer.getCivilizationType()
		iUnitType = pWinner.getUnitType()
		iNewPromo = -1

		# DEBUG
		#iHumanPlayer = gc.getGame().getActivePlayer()
		#CyInterface().addMessage(iHumanPlayer, True, 10, "Player: " + str(iWinnerPlayer) + " Unit: " + pWinner.getName(), None, 2, None, ColorTypes(10), pWinner.getX(), pWinner.getY(), True, True)

		# kann keine Stufe aufsteigen, wenn eine Belobigung ansteht
		if CvUtil.getScriptData(pWinner, ["P", "t"]) == "RangPromoUp":
				return

		# Manche units sollen keinen Rang bekommen
		if iUnitType in L.LNoRankUnits:
				return

		# Ab PAE 6.14: bestimmte Rankings nur für bestimmte CIVs
		LRome = [
			gc.getInfoTypeForString("CIVILIZATION_ROME"),
			gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS")
		]
		LGreece = [
			gc.getInfoTypeForString("CIVILIZATION_GREECE"),
			gc.getInfoTypeForString("CIVILIZATION_ATHENS"),
			gc.getInfoTypeForString("CIVILIZATION_THEBAI")
		]
		LEgypt = [
			gc.getInfoTypeForString("CIVILIZATION_EGYPT"),
			gc.getInfoTypeForString("CIVILIZATION_NUBIA")
		]
		LBabylon = [
			gc.getInfoTypeForString("CIVILIZATION_BABYLON"),
			gc.getInfoTypeForString("CIVILIZATION_ASSYRIA")
		]
		LCarthago = [
			gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"),
			gc.getInfoTypeForString("CIVILIZATION_PHON")
		]

		if pWinnerPlayer.getCivilizationType() in LRome:
				# ROM Pedes
				if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_1")):
						if not pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_15")):
								iNumPromos = gc.getNumPromotionInfos()-1
								iPromo = iNumPromos
								for iPromo in xrange(iNumPromos, 0, -1):
										iPromoType = gc.getPromotionInfo(iPromo).getType()
										if "_TRAIT_" in iPromoType:
												break
										if "_RANG_ROM_LATE" in iPromoType:
												continue
										if "_RANG_ROM_EQUES" in iPromoType:
												continue
										if "_RANG_ROM_" in iPromoType:
												if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
														#if iPromo == gc.getInfoTypeForString("PROMOTION_RANG_ROM_4") or iPromo == gc.getInfoTypeForString("PROMOTION_RANG_ROM_7") or iPromo == gc.getInfoTypeForString("PROMOTION_RANG_ROM_11"):
														if canUpgradeUnit(pWinner) != -1:
																# Auxiliar nur bis ausgenommen Optio
																if iUnitType not in L.LUnitAuxiliar:
																		CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
														else:
																pWinner.setHasPromotion(iNewPromo, True)
																# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																if pWinnerPlayer.isHuman():
																		CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																														 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
														break
												else:
														iNewPromo = iPromo
				# ROM Eques
				elif pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_1")):
								# Chance: 1:4
								# if CvUtil.myRandom(4, "RangEques") == 1:
								iNumPromos = gc.getNumPromotionInfos() - 1
								for iPromo in xrange(iNumPromos, -1, -1):  # -1 als zweites Argument, damit es bis 0 runterzaehlt.
										iPromoType = gc.getPromotionInfo(iPromo).getType()
										if "_TRAIT_" in iPromoType:
												break
										if "_RANG_ROM_EQUES" in iPromoType:
												if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
														#if iPromo == gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_3"):
														if canUpgradeUnit(pWinner) != -1:
																CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
														else:
																pWinner.setHasPromotion(iNewPromo, True)
																# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																if pWinnerPlayer.isHuman():
																		CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																														 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
														break

												else:
														iNewPromo = iPromo
				# ROM Late Antike
				elif pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_1")):
						if not pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_15")):
								iNumPromos = gc.getNumPromotionInfos()-1
								iPromo = iNumPromos
								for iPromo in xrange(iNumPromos, 0, -1):
										iPromoType = gc.getPromotionInfo(iPromo).getType()
										if "_TRAIT_" in iPromoType:
												break
										if "_RANG_ROM_LATE" in iPromoType:
												if pWinner.isHasPromotion(iPromo):
														#if iPromo == gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_5") or iPromo == gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_10"):
														if canUpgradeUnit(pWinner) != -1:
																CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
														else:
																pWinner.setHasPromotion(iNewPromo, True)
																# Der Kommandant Eurer Einheit (%s1) hat nun den Rang eines %s2!
																if pWinnerPlayer.isHuman():
																		CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																														 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
														break

												else:
														iNewPromo = iPromo
		# Griechen (Athen, Theben, Griechen allgemein)
		elif pWinnerPlayer.getCivilizationType() in LGreece:
				if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_GREEK_1")):
						if not pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_GREEK_12")):
								iNumPromos = gc.getNumPromotionInfos()-1
								iPromo = iNumPromos
								for iPromo in xrange(iNumPromos, 0, -1):
										iPromoType = gc.getPromotionInfo(iPromo).getType()
										if "_RANG_ROM_" in iPromoType:
												break
										if "_RANG_SPARTA_" in iPromoType:
												continue
										if "_RANG_GREEK_" in iPromoType:
												if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
														#if iPromo == gc.getInfoTypeForString("PROMOTION_RANG_GREEK_4") or iPromo == gc.getInfoTypeForString("PROMOTION_RANG_GREEK_7") or iPromo == gc.getInfoTypeForString("PROMOTION_RANG_GREEK_10"):
														if canUpgradeUnit(pWinner) != -1:
																CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
														else:
																pWinner.setHasPromotion(iNewPromo, True)
																# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																if pWinnerPlayer.isHuman():
																		CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																														 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
														break
												else:
														iNewPromo = iPromo
		# Sparta
		elif pWinnerPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_SPARTA"):
				if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_10")):
						return
				if pWinnerTeam.isHasTech(gc.getInfoTypeForString("TECH_PHALANX")):
						if pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN") or pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_1")
								if pWinner.isHasPromotion(iNewPromo):
										iNumPromos = gc.getNumPromotionInfos()-1
										iPromo = iNumPromos
										for iPromo in xrange(iNumPromos, 0, -1):
												iPromoType = gc.getPromotionInfo(iPromo).getType()
												if "_RANG_GREEK_" in iPromoType:
														break
												if "_RANG_SPARTA_" in iPromoType:
														if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
																#if iPromo == gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_4") or iPromo == gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_7"):
																if canUpgradeUnit(pWinner) != -1:
																		CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
																else:
																		pWinner.setHasPromotion(iNewPromo, True)
																		# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																		if pWinnerPlayer.isHuman():
																				CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																																 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
																break
														else:
																iNewPromo = iPromo
								else:
										pWinner.setHasPromotion(iNewPromo, True)
										# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
										if pWinnerPlayer.isHuman():
												CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																								 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)

		# Makedonen
		elif pWinnerPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"):
				if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_10")):
						return
				if pWinnerTeam.isHasTech(gc.getInfoTypeForString("TECH_PHALANX2")):
						if pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN") or pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_1")
								if pWinner.isHasPromotion(iNewPromo):
										iNumPromos = gc.getNumPromotionInfos()-1
										iPromo = iNumPromos
										iNewPromo = -1
										for iPromo in xrange(iNumPromos, 0, -1):
												iPromoType = gc.getPromotionInfo(iPromo).getType()
												if "_RANG_SPARTA_" in iPromoType:
														break
												if "_RANG_MACEDON_" in iPromoType:
														if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
																#if iPromo == gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_4") or iPromo == gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_7") or iPromo == gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_9"):
																if canUpgradeUnit(pWinner) != -1:
																		CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
																else:
																		pWinner.setHasPromotion(iNewPromo, True)
																		# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																		if pWinnerPlayer.isHuman():
																				CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																																 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
																break
														else:
																iNewPromo = iPromo
								else:
										pWinner.setHasPromotion(iNewPromo, True)
										# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
										if pWinnerPlayer.isHuman():
												CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																								 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)

		# Perser
		elif pWinnerPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_PERSIA"):
				# Perser Reiter
				if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_1")):
						if not pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_15")):
								iNumPromos = gc.getNumPromotionInfos()-1
								iPromo = iNumPromos
								for iPromo in xrange(iNumPromos, 0, -1):
										iPromoType = gc.getPromotionInfo(iPromo).getType()
										if "_RANG_PERSIA_" in iPromoType:
												break
										if "_RANG_PERSIA2_" in iPromoType:
												if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
														if canUpgradeUnit(pWinner) != -1:
																CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
														else:
																pWinner.setHasPromotion(iNewPromo, True)
																# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																if pWinnerPlayer.isHuman():
																		CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																														 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
														break
												else:
														iNewPromo = iPromo
				# Perser Fusssoldaten
				elif pWinnerTeam.isHasTech(gc.getInfoTypeForString("TECH_SKIRMISH_TACTICS")):
						iNewPromo = gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_1")
						if pWinner.isHasPromotion(iNewPromo):
								if not pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_10")):
										iNewPromo = -1
										iNumPromos = gc.getNumPromotionInfos()-1
										iPromo = iNumPromos
										for iPromo in xrange(iNumPromos, 0, -1):
												iPromoType = gc.getPromotionInfo(iPromo).getType()
												if "_RANG_MACEDON_" in iPromoType:
														break
												if "_RANG_PERSIA_" in iPromoType:
														if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
																#if iPromo == gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_5") or iPromo == gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_7"):
																if canUpgradeUnit(pWinner) != -1:
																		CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
																else:
																		pWinner.setHasPromotion(iNewPromo, True)
																		# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																		if pWinnerPlayer.isHuman():
																				CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																																 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
																break
														else:
																iNewPromo = iPromo
						else:
								pWinner.setHasPromotion(iNewPromo, True)
								# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
								if pWinnerPlayer.isHuman():
										CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																						 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)



		# Egypt, Nubia
		elif pWinnerPlayer.getCivilizationType() in LEgypt:
				if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_10")):
						return
				if pWinnerTeam.isHasTech(gc.getInfoTypeForString("TECH_BEWAFFNUNG3")):
						if pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN") or \
										pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN") or \
										pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_AXEMAN"):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_1")
								if pWinner.isHasPromotion(iNewPromo):
										iRand = CvUtil.myRandom(2, "PROMOTION_RANG_EGYPT")
										if iRand == 1:
												iNumPromos = gc.getNumPromotionInfos()-1
												iPromo = iNumPromos
												iNewPromo = -1
												for iPromo in xrange(iNumPromos, 0, -1):
														iPromoType = gc.getPromotionInfo(iPromo).getType()
														if "_RANG_PERSIA2_" in iPromoType:
																break
														if "_RANG_EGYPT_" in iPromoType:
																if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
																		if canUpgradeUnit(pWinner) != -1:
																				CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
																		else:
																				pWinner.setHasPromotion(iNewPromo, True)
																				# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																				if pWinnerPlayer.isHuman():
																						CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																																		 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
																		break
																else:
																		iNewPromo = iPromo
								else:
										pWinner.setHasPromotion(iNewPromo, True)
										# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
										if pWinnerPlayer.isHuman():
												CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																								 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)

		# Karthago
		elif pWinnerPlayer.getCivilizationType() in LCarthago:
			if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_1")):
				if not pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_6")):
						iRand = CvUtil.myRandom(3, "PROMOTION_RANG_CARTHAGE")
						if iRand == 1:
								iNumPromos = gc.getNumPromotionInfos()-1
								iPromo = iNumPromos
								for iPromo in xrange(iNumPromos, 0, -1):
										iPromoType = gc.getPromotionInfo(iPromo).getType()
										if "_RANG_EGYPT_" in iPromoType:
												break
										if "_RANG_CARTHAGE_" in iPromoType:
												if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
														if canUpgradeUnit(pWinner) != -1:
																CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
														else:
																pWinner.setHasPromotion(iNewPromo, True)
																# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																if pWinnerPlayer.isHuman():
																		CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																														 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
														break
												else:
														iNewPromo = iPromo

		# Assur, Babylon
		elif pWinnerPlayer.getCivilizationType() in LBabylon:
				if not pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_12")):
						if pWinnerTeam.isHasTech(gc.getInfoTypeForString("TECH_BUERGERSOLDATEN")):
								if pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN") or \
												pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN") or \
												pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_AXEMAN"):
										iNewPromo = gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_1")
										if pWinner.isHasPromotion(iNewPromo):
												iNumPromos = gc.getNumPromotionInfos()-1
												iPromo = iNumPromos
												iNewPromo = -1
												for iPromo in xrange(iNumPromos, 0, -1):
														iPromoType = gc.getPromotionInfo(iPromo).getType()
														if "_RANG_CARTHAGE_" in iPromoType:
																break
														if "_RANG_ASSUR_" in iPromoType:
																if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
																		if canUpgradeUnit(pWinner) != -1:
																						CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
																		else:
																				pWinner.setHasPromotion(iNewPromo, True)
																				# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																				if pWinnerPlayer.isHuman():
																						CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																																		 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
																		break
																else:
																		iNewPromo = iPromo
										else:
												pWinner.setHasPromotion(iNewPromo, True)
												# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
												if pWinnerPlayer.isHuman():
														CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																										 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)

		# Sumer
		elif pWinnerPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_SUMERIA"):
				if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_SUMER_10")):
						return
				if pWinnerTeam.isHasTech(gc.getInfoTypeForString("TECH_BUERGERSOLDATEN")):
						if pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN") or \
										pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN") or \
										pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_AXEMAN"):
								iNewPromo = gc.getInfoTypeForString("PROMOTION_RANG_SUMER_1")
								if pWinner.isHasPromotion(iNewPromo):
										iRand = CvUtil.myRandom(2, "PROMOTION_RANG_SUMER")
										if iRand == 1:
												iNumPromos = gc.getNumPromotionInfos()-1
												iPromo = iNumPromos
												iNewPromo = -1
												for iPromo in xrange(iNumPromos, 0, -1):
														iPromoType = gc.getPromotionInfo(iPromo).getType()
														if "_RANG_ASSUR_" in iPromoType:
																break
														if "_RANG_SUMER_" in iPromoType:
																if pWinner.isHasPromotion(iPromo) and iNewPromo != -1:
																		if canUpgradeUnit(pWinner) != -1:
																						CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
																		else:
																				pWinner.setHasPromotion(iNewPromo, True)
																				# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
																				if pWinnerPlayer.isHuman():
																						CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																																		 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
																		break
																else:
																		iNewPromo = iPromo
								else:
										pWinner.setHasPromotion(iNewPromo, True)
										# Der Kommandant Eurer Einheit (%s1) hat nun den Rang: %s2!
										if pWinnerPlayer.isHuman():
												CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																								 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)

		# Ab Kriegerethos : kampferfahren
		if pWinnerTeam.isHasTech(gc.getInfoTypeForString("TECH_KRIEGERETHOS")):
				if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT3")):
						if iUnitType not in L.LUnitsHeadRang:
								if pWinnerPlayer.getCivilizationType() in L.LCivGermanen:
										if not pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_GER_3")):
												iRand = CvUtil.myRandom(4, "PROMOTION_RANG_GER_3")
												if iRand == 1:
														iNewPromo = gc.getInfoTypeForString("PROMOTION_RANG_GER_1")
														if pWinner.isHasPromotion(iNewPromo):
																iNewPromo = gc.getInfoTypeForString("PROMOTION_RANG_GER_2")
														if pWinner.isHasPromotion(iNewPromo):
																iNewPromo = gc.getInfoTypeForString("PROMOTION_RANG_GER_3")
														pWinner.setHasPromotion(iNewPromo, True)
														if pWinnerPlayer.isHuman():
																CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																												 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
										else:
												CvUtil.addScriptData(pWinner, "P", "RangPromoUp")
								# Hunnen
								if pWinnerPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_HUNNEN"):
										if pWinner.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
												if not pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_HUN")):
														iRand = CvUtil.myRandom(15, "PROMOTION_RANG_HUN")
														if iRand == 1:
																iNewPromo = gc.getInfoTypeForString("PROMOTION_RANG_HUN")
																pWinner.setHasPromotion(iNewPromo, True)
																if pWinnerPlayer.isHuman():
																		CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_CIV_RANG", (pWinner.getName(), gc.getPromotionInfo(iNewPromo).getDescription())),
																														 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iNewPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
												# Geissel Gottes ab Panzerreiter (nur als Kaghan)
												elif pWinnerTeam.isHasTech(gc.getInfoTypeForString("TECH_PANZERREITER")):
														CvUtil.addScriptData(pWinner, "P", "RangPromoUp")


def flee(pLoser, pWinner, iWinnerDamage):
		"""
		# Flucht der Einheit / Escape of units --------
		# Defending unit only (inaktiv)
		# Nur wenn die Einheit nicht desertiert hat: bUnitDone
		# if not bUnitDone and not pLoser.isAttacking():
		# PAE V: defending units in cities gets flight (hiding behind walls) with max 70%. units kept on the city plot
		"""
		iWinnerPlayer = pWinner.getOwner()
		pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
		iLoserPlayer = pLoser.getOwner()
		pLoserPlayer = gc.getPlayer(iLoserPlayer)
		bUnitFlucht = False
		NewUnit = None

		iMaxHealth = 5  # Standard: max 10% Gesundheit
		iChance = 2  # Standard Fluchtchance: 20%
		iChanceShipsAndRiders = 3  # Standard: 30%

		iGeneralForm = gc.getInfoTypeForString("PROMOTION_FORM_LEADER_POSITION")
		bGeneralForm = False

		# Eine einzelne kaperbare Unit darf nicht fluechten
		# if pLoser.getCaptureUnitType(pLoser.getOwner()) > -1 and pLoser.plot().getNumUnits() > 1:
		# oder mit der UnitInfo CaptureClass? gc.getUnitInfo(pLoser.getUnitType()).getUnitCaptureClassType()
		# PAE 6.16: Verlierer darf nicht angegriffen haben (zB von einer Stadt aufs Feld angreifen)
		if not pLoser.isMadeAttack() and (pLoser.getCaptureUnitType(pLoser.getCivilizationType()) == -1 or pLoser.isHasPromotion(iGeneralForm)):
				bIsCity = False
				bIsVillage = False
				pLoserPlot = pLoser.plot()
				if pLoserPlot.isCity():
						bIsCity = True
						iCityStatus = PAE_City.getCityStatus(pLoserPlot.getPlotCity(), 0, 0, False)

				# Tiere
				if pLoser.getUnitAIType() == UnitAITypes.UNITAI_ANIMAL:
						if pLoser.getUnitType() == gc.getInfoTypeForString("UNIT_UR") or pLoser.getLevel() > 2:
								iChance = 8
								iMaxHealth = 40
						elif pLoser.getLevel() > 1:
								iChance = 6
								iMaxHealth = 30
						else:
								iChance = 4
								iMaxHealth = 20

				# nun nach Chance geordnet
				# Promo Flucht III - 80%, max 20
				elif pLoser.isHasPromotion(gc.getInfoTypeForString("PROMOTION_FLUCHT3")):
						iChance = 8
						iMaxHealth = 20
				# Metropole
				elif bIsCity and iCityStatus == 4:
						iChance = 6
						iMaxHealth = 20
				# Promo Flucht II - 60%, max 15
				elif pLoser.isHasPromotion(gc.getInfoTypeForString("PROMOTION_FLUCHT2")):
						iChance = 6
						iMaxHealth = 15
				# Provinzstadt
				elif bIsCity and iCityStatus == 3:
						iChance = 5
						iMaxHealth = 18
				# Stadt
				elif bIsCity and iCityStatus == 2:
						iChance = 4
						iMaxHealth = 15
				# Promo Flucht I - 40%, max 10
				elif pLoser.isHasPromotion(gc.getInfoTypeForString("PROMOTION_FLUCHT1")):
						iChance = 4
				# Gemeinde
				elif pLoserPlot.getImprovementType() == gc.getInfoTypeForString("IMPROVEMENT_TOWN"):
						bIsVillage = True
						iChance = 3
						iMaxHealth = 15
				elif (pLoserPlot.getImprovementType() == gc.getInfoTypeForString("IMPROVEMENT_VILLAGE")
								or pLoserPlot.getImprovementType() == gc.getInfoTypeForString("IMPROVEMENT_VILLAGE_HILL")):
						bIsVillage = True
						iChance = 2
						iMaxHealth = 12

				# Bei Schiffen eine Extra-Berechnung
				if pLoser.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_NAVAL"):
						if iWinnerDamage >= 50:
								iChance = 8  # 80%: somit muss man womoeglich ein Schiff 2x angreifen, bevor es sinkt
						elif iChance < 4:
								iChance = iChanceShipsAndRiders

				# Berittene
				elif iChance < 4 and pLoser.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"):
						iChance = iChanceShipsAndRiders

				# Generals Formation
				if pLoser.isHasPromotion(iGeneralForm):
						iChance = 10
						bGeneralForm = True

				iRand = CvUtil.myRandom(10, "Escape")

				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Fluchtchance (Zeile 2924)", iRand)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Max Health (Zeile 2925)", iMaxHealth)), None, 2, None, ColorTypes(10), 0, 0, False, False)

				if iRand < iChance:
						bUnitFlucht = True

						# Create a new unit
						#pPlot = pLoser.plot()
						#if pPlot.getNumUnits() == 1: pLoser.jumpToNearestValidPlot()
						NewUnit = pLoserPlayer.initUnit(pLoser.getUnitType(), pLoser.getX(), pLoser.getY(), UnitAITypes(pLoser.getUnitAIType()), DirectionTypes.DIRECTION_SOUTH)
						if pLoser.isMadeAttack():
								NewUnit.finishMoves()

						if pLoser.getUnitCombatType() != -1 or pLoser.getUnitAIType() == UnitAITypes.UNITAI_ANIMAL or pLoser.getUnitAIType() == UnitAITypes.UNITAI_EXPLORE:

								if not bGeneralForm:
										iRandHealth = 1 + CvUtil.myRandom(iMaxHealth, "EscapeHealth")
										NewUnit.setDamage(100 - iRandHealth, -1)  # Max Health
								NewUnit.setExperience(pLoser.getExperience(), -1)
								NewUnit.setLevel(pLoser.getLevel())

								# Check its promotions
								iRange = gc.getNumPromotionInfos()
								for iPromotion in range(iRange):
										# init all promotions the unit had
										if pLoser.isHasPromotion(iPromotion):
												NewUnit.setHasPromotion(iPromotion, True)

								if bGeneralForm:
										NewUnit.setHasPromotion(iGeneralForm, False)

						copyName(NewUnit, pLoser.getUnitType(), pLoser.getName())

						# Fluchtplot
						if not bIsCity and not bIsVillage:
								iX = pLoserPlot.getX()
								iY = pLoserPlot.getY()
								plots = []
								for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
										loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
										if loopPlot is not None and not loopPlot.isNone() and pLoser.canMoveInto(loopPlot, 0, 0, 1):
												plots.append(loopPlot)
								if len(plots) == 0:
										NewUnit.jumpToNearestValidPlot()
								else:
										iPlot = CvUtil.myRandom(len(plots), "PAE_Unit_FluchtPlot")
										NewUnit.setXY(plots[iPlot].getX(), plots[iPlot].getY(), False, True, True)

						if pLoserPlayer.isHuman():
								if bIsVillage:
										CyInterface().addMessage(iLoserPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_ESCAPE_4", (NewUnit.getName(),)), None, 2, None, ColorTypes(8), 0, 0, False, False)
								elif bIsCity:
										CyInterface().addMessage(iLoserPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_ESCAPE_3", (NewUnit.getName(),)), None, 2, None, ColorTypes(8), 0, 0, False, False)
								else:
										CyInterface().addMessage(iLoserPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_ESCAPE", (NewUnit.getName(), pWinner.getName())), None, 2, None, ColorTypes(8), 0, 0, False, False)
						if pWinnerPlayer.isHuman():
								if bIsVillage:
										CyInterface().addMessage(iWinnerPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_ESCAPE_4", (NewUnit.getName(),)), None, 2, None, ColorTypes(13), 0, 0, False, False)
								elif bIsCity:
										CyInterface().addMessage(iWinnerPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_ESCAPE_3", (NewUnit.getName(),)), None, 2, None, ColorTypes(13), 0, 0, False, False)
								else:
										CyInterface().addMessage(iWinnerPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_ESCAPE_2", (NewUnit.getName(), pWinner.getName())), None, 2, None, ColorTypes(13), 0, 0, False, False)

						# if Unit was a leader (PROMOTION_LEADER)
						if pLoser.getLeaderUnitType() > -1:
								NewUnit.setLeaderUnitType(pLoser.getLeaderUnitType())
								pLoser.setLeaderUnitType(-1)  # avoids ingame message "GG died in combat"

						# ***TEST***
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Einheit fluechtet (Zeile 2774)", iChance)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		return bUnitFlucht, NewUnit


def doAutomatedRanking(pWinner, pLoser):
		# Feature - Automated Unit Ranking via Promotions: Trained, Experienced, Seasoned, Veteran, Elite, Legendary
		# Trainiert, Kampferfahren, Routiniert, Veteran, Elite, Legende
		# Each promotion gives +x% Strength
		# Animal Attack brings only 1st Ranking

		# tuple contain (Promo, %-Probabiblity)
		LPromo = [
				(gc.getInfoTypeForString("PROMOTION_COMBAT1"), 80),
				(gc.getInfoTypeForString("PROMOTION_COMBAT2"), 70),
				(gc.getInfoTypeForString("PROMOTION_COMBAT3"), 60),
				(gc.getInfoTypeForString("PROMOTION_COMBAT4"), 50),
				(gc.getInfoTypeForString("PROMOTION_COMBAT5"), 30),
				(gc.getInfoTypeForString("PROMOTION_COMBAT6"), 10)
		]
		LPromoNegative = [
				(gc.getInfoTypeForString("PROMOTION_MORAL_NEG1"), 10),
				(gc.getInfoTypeForString("PROMOTION_MORAL_NEG2"), 20),
				(gc.getInfoTypeForString("PROMOTION_MORAL_NEG3"), 30),
				(gc.getInfoTypeForString("PROMOTION_MORAL_NEG4"), 40),
				(gc.getInfoTypeForString("PROMOTION_MORAL_NEG5"), 50)
		]

		if (pLoser.isMilitaryHappiness()
				or pLoser.getUnitAIType() in [UnitAITypes.UNITAI_ANIMAL, UnitAITypes.UNITAI_EXPLORE]
						or pLoser.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_NAVAL")):
				iPlayer = pWinner.getOwner()

				# PAE V: Old veterans needs more time to get fit again (elite needs longer)
				# Better AI: HI only
				if gc.getPlayer(iPlayer).isHuman():
						if pWinner.isHasPromotion(LPromo[5][0]) and pWinner.getDamage() < 50:
								pWinner.setDamage(50, -1)
						elif pWinner.isHasPromotion(LPromo[4][0]) and pWinner.getDamage() < 70:
								pWinner.setDamage(30, -1)
						# elif pWinner.isHasPromotion(LPromo[3][0]) and pWinner.getDamage() < 20: pWinner.setDamage(20, -1)

				if pWinner.isHasPromotion(LPromo[2][0]) and (
						pLoser.getOwner() == gc.getBARBARIAN_PLAYER() or
						pLoser.getUnitAIType() == UnitAITypes.UNITAI_ANIMAL or
						pLoser.getUnitAIType() == UnitAITypes.UNITAI_EXPLORE
					):
					return False

				if not pWinner.isHasPromotion(LPromo[-1][0]):
						for iPromo, iChance in LPromo:
								if not pWinner.isHasPromotion(iPromo):
										break

						# PAE for better AI: KI +15% Chance
						if not gc.getPlayer(iPlayer).isHuman():
								iChance += 15

						if CvUtil.myRandom(100, "automatedRanking") < iChance:
								if (iPlayer, pWinner.getID()) not in PAEInstanceFightingModifier:
										PAEInstanceFightingModifier.append((iPlayer, pWinner.getID()))
										pWinner.setHasPromotion(iPromo, True)
										if gc.getPlayer(iPlayer).isHuman():
												CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_RANKING", (pWinner.getName(), gc.getPromotionInfo(iPromo).getDescription())),
																								 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iPromo).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
										return True
						# War weariness parallel ab Elite
						elif pWinner.isHasPromotion(LPromo[4][0]) and not pWinner.isHasPromotion(LPromoNegative[-1][0]):
								if (iPlayer, pWinner.getID()) not in PAEInstanceFightingModifier:
										for iPromo, iChance in LPromoNegative:
												if not pWinner.isHasPromotion(iPromo):
														if iChance > CvUtil.myRandom(100, "war weariness"):
																PAEInstanceFightingModifier.append((iPlayer, pWinner.getID()))
																pWinner.setHasPromotion(iPromo, True)
																if gc.getPlayer(iPlayer).isHuman():
																		CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_WAR_WEARINESS", (pWinner.getName(), gc.getPromotionInfo(iPromo).getDescription())),
																														 "AS2D_REBELLION", 2, gc.getPromotionInfo(iPromo).getButton(), ColorTypes(12), pWinner.getX(), pWinner.getY(), True, True)
																return True
														break

				# PAE V: Gewinner kann Mercenary-Promo ab Veteran verlieren
				# PAE 6.14: Gewinner kann diese immer verlieren
				iPromoMercenary = gc.getInfoTypeForString("PROMOTION_MERCENARY")
				if pWinner.isHasPromotion(iPromoMercenary): # and pWinner.isHasPromotion(LPromo[3][0]) 
						if gc.getPlayer(iPlayer).isHuman():
								iPromoLoyal = gc.getInfoTypeForString("PROMOTION_LOYALITAT")
								iPromoLeader = gc.getInfoTypeForString("PROMOTION_LEADER")
								iPromoLeadership = gc.getInfoTypeForString("PROMOTION_LEADERSHIP")

								if pWinner.isHasPromotion(iPromoLoyal) or pWinner.isHasPromotion(iPromoLeader) or pWinner.isHasPromotion(iPromoLeadership):
										iChance = 2  # 50%
								else:
										iChance = 4  # 25%
						else:
								iChance = 3  # Better AI: always 33%

						if CvUtil.myRandom(iChance, "remove Mercenary promo") == 1:
								pWinner.setHasPromotion(iPromoMercenary, False)
								if gc.getPlayer(iPlayer).isHuman():
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_UNDO_PROMO_MERCENARY", (pWinner.getName(), )),
																						 "AS2D_IF_LEVELUP", 2, gc.getPromotionInfo(iPromoMercenary).getButton(), ColorTypes(13), pWinner.getX(), pWinner.getY(), True, True)
								return True

		return False

# Horse down 666
def doHorseDown(pUnit):
		iUnitType = pUnit.getUnitType()
		# iOwner = pUnit.getOwner()
		iX = pUnit.getX()
		iY = pUnit.getY()
		iNewUnitType = -1

		# Get civilization specific unmounted unit type.
		dTmp = L.DHorseDownMap.get(iUnitType)
		if dTmp:
				iNewUnitType = dTmp.get(pUnit.getCivilizationType(), dTmp[None])

		if iNewUnitType != -1:
				# Create horse unit
				NewUnit = gc.getPlayer(pUnit.getOwner()).initUnit(gc.getInfoTypeForString("UNIT_HORSE"), iX, iY, UnitAITypes.UNITAI_RESERVE, DirectionTypes.DIRECTION_SOUTH)
				NewUnit.finishMoves()

				# Create a new unit
				NewUnit = gc.getPlayer(pUnit.getOwner()).initUnit(iNewUnitType, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				NewUnit.setExperience(pUnit.getExperience(), -1)
				NewUnit.setLevel(pUnit.getLevel())
				NewUnit.setDamage(pUnit.getDamage(), -1)
				if pUnit.getName() != gc.getUnitInfo(iUnitType).getText():
						UnitName = pUnit.getName()
						UnitName = re.sub(r" \(.*?\)", "", UnitName)
						NewUnit.setName(UnitName)
				# Check its promotions
				iRange = gc.getNumPromotionInfos()
				for iPromotion in range(iRange):
						# init all promotions the unit had
						if pUnit.isHasPromotion(iPromotion):
								NewUnit.setHasPromotion(iPromotion, True)

				# Mercenary promo
				iPromotion = gc.getInfoTypeForString("PROMOTION_MERCENARY")
				if not pUnit.isHasPromotion(iPromotion):
						NewUnit.setHasPromotion(iPromotion, False)

				# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
				pUnit.kill(True, -1)  # RAMK_CTD
				NewUnit.finishMoves()

				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Horse Down (Zeile 5014)", 1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

				# end Horse down

# Horse up 667
def doHorseUp(pPlot, pUnit):
		iUnitType = pUnit.getUnitType()
		# iOwner = pUnit.getOwner()
		iX = pUnit.getX()
		iY = pUnit.getY()
		iNewUnitType = -1

		# Pferd suchen und killen
		UnitHorse = gc.getInfoTypeForString("UNIT_HORSE")
		iRange = pPlot.getNumUnits()
		for iUnit in range(iRange):
				pLoopUnit = pPlot.getUnit(iUnit)
				if pLoopUnit.getUnitType() == UnitHorse:
						# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
						pLoopUnit.kill(True, -1)  # RAMK_CTD
						break

		if iUnitType in L.LUnitAuxiliar:
				iNewUnitType = L.DHorseUpMap["auxiliar"]
		else:
				iNewUnitType = L.DHorseUpMap.get(iUnitType, -1)

		if iNewUnitType != -1:
				# Create a new unit
				NewUnit = gc.getPlayer(pUnit.getOwner()).initUnit(iNewUnitType, iX, iY, UnitAITypes.UNITAI_RESERVE, DirectionTypes.DIRECTION_SOUTH)
				NewUnit.setExperience(pUnit.getExperience(), -1)
				NewUnit.setLevel(pUnit.getLevel())
				NewUnit.changeMoves(-60)
				NewUnit.setDamage(pUnit.getDamage(), -1)
				if pUnit.getName() != gc.getUnitInfo(iUnitType).getText():
						UnitName = pUnit.getName()
						UnitName = re.sub(r"( \(.*?\))", "", UnitName)
						NewUnit.setName(UnitName)
				# Check its promotions
				iRange = gc.getNumPromotionInfos()
				for iPromotion in range(iRange):
						# init all promotions the unit had
						if pUnit.isHasPromotion(iPromotion):
								NewUnit.setHasPromotion(iPromotion, True)

				# Mercenary promo
				iPromotion = gc.getInfoTypeForString("PROMOTION_MERCENARY")
				if not pUnit.isHasPromotion(iPromotion):
						NewUnit.setHasPromotion(iPromotion, False)

				# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
				pUnit.kill(True, -1)  # RAMK_CTD

				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Horse Up (Zeile 5057)", 1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

				# end Horse up

# Trojanisches Pferd
def doTrojanHorse(pCity, pUnit):
		iCityPlayer = pCity.getOwner()
		iUnitPlayer = pUnit.getOwner()
		pCityPlayer = gc.getPlayer(iCityPlayer)
		pUnitPlayer = gc.getPlayer(iUnitPlayer)

		iDamage = pCity.getDefenseModifier(0)
		pCity.changeDefenseDamage(iDamage)

		if pCityPlayer is not None and pUnitPlayer is not None:
				if pCityPlayer.isHuman():
						CyInterface().addMessage(
								iCityPlayer, False, 25,
								CyTranslator().getText("TXT_KEY_MESSAGE_TROJAN_HORSE_CITY",
																			 (pCity.getName(),
																				pUnitPlayer.getCivilizationAdjective(2))),
								None, InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(),
								ColorTypes(11), pCity.getX(), pCity.getY(), True, True)
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_TROJAN_HORSE_CITY", (pCity.getName(), pUnitPlayer.getCivilizationAdjective(1))))
						popupInfo.addPopup(iCityPlayer)
				if pUnitPlayer.isHuman():
						CyInterface().addMessage(
								iUnitPlayer, False, 25,
								CyTranslator().getText("TXT_KEY_MESSAGE_TROJAN_HORSE_UNIT",
																			 (pCity.getName(),
																				pCityPlayer.getCivilizationAdjective(2))),
								None, InterfaceMessageTypes.MESSAGE_TYPE_INFO, pUnit.getButton(),
								ColorTypes(11), pCity.getX(), pCity.getY(), True, True)
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText(
								"TXT_KEY_MESSAGE_TROJAN_HORSE_UNIT",
								(pCity.getName(), pCityPlayer.getCivilizationAdjective(1))))
						popupInfo.addPopup(iUnitPlayer)

				# if iCityPlayer == gc.getGame().getActivePlayer() or iUnitPlayer == gc.getGame().getActivePlayer():
				#    CyAudioGame().Play2DSound("AS2D_THEIRDECLAREWAR")

				# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
				pUnit.kill(True, -1)  # RAMK_CTD

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Trojanisches Pferd (Zeile 9497)", 0)), None, 2, None, ColorTypes(10), 0, 0, False, False)

# PAE Feature: Auswirkungen, wenn ein General oder Held stirbt
def doDyingGeneral(pUnit, iWinnerPlayer=-1):
		# PROMOTION_LEADER
		if pUnit.getLeaderUnitType() > -1: # or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_HERO")):
				# Inits
				iPromoMercenary = gc.getInfoTypeForString("PROMOTION_MERCENARY")
				iPlayer = pUnit.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				# PAE 6.14
				bNoCivilWar = pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_POLYARCHIE"))
				eBuildingStadt = gc.getInfoTypeForString("BUILDING_STADT")
				eBuildingClass = gc.getBuildingInfo(eBuildingStadt).getBuildingClassType()

				iTeam = pPlayer.getTeam()
				pTeam = gc.getTeam(iTeam)
				pPlot = pUnit.plot()
				#iNumLeadersOnPlot = 0 # bis PAE 6.13

				# Anzahl der Generaele des Spielers
				#iLeader = 0
				#(loopUnit, pIter) = pPlayer.firstUnit(False)
				#while loopUnit:
				#		if loopUnit.getLeaderUnitType() > -1:
				#				if loopUnit.getID() != pUnit.getID():
				#						iLeader += 1
				#		(loopUnit, pIter) = pPlayer.nextUnit(pIter, False)

				# Units: bekommen Mercenary-Promo
				iNumUnits = pPlot.getNumUnits()
				# 1. Check Generals im Stack
				#for i in range(iNumUnits):
				#		pLoopUnit = pPlot.getUnit(i)
				#		if pLoopUnit.getOwner() == iPlayer:
				#				if pLoopUnit.getLeaderUnitType() > -1:
				#						iNumLeadersOnPlot += 1

				# 2. Vergabe der Promo
				for i in range(iNumUnits):
						pLoopUnit = pPlot.getUnit(i)
						if pLoopUnit is not None and pLoopUnit.getOwner() == iPlayer:
								#if i % iNumLeadersOnPlot == 0:
								if pLoopUnit.isMilitaryHappiness():
										pLoopUnit.setHasPromotion(iPromoMercenary, True)

				# PopUp
				if pPlayer.isHuman():
						iRand = 1 + CvUtil.myRandom(9, "Stadtaufruhr_Message")
						szTextKey = "TXT_KEY_MESSAGE_CITY_DYING_GENERAL_" + str(iRand)
						szText = CyTranslator().getText(szTextKey, ("",))
						szText += CyTranslator().getText("[NEWLINE]", ())
						szText += CyTranslator().getText("TXT_KEY_MESSAGE_CITY_DYING_GENERAL_NEGATIVE", ())
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(szText)
						popupInfo.addPopup(iPlayer)

				# Cities: Stadtaufruhr
				# PAE 6.14: vorübergehend -1 :) in jeder Stadt (Status Stadt)
				(loopCity, pIter) = pPlayer.firstCity(False)
				while loopCity:
						if not loopCity.isNone():  # only valid cities
								
								#if CvUtil.myRandom(iLeader, "Stadtaufruhr1") == 0: # bis PAE 6.14
								# PAE 6.15: Chance 10%
								if not bNoCivilWar and CvUtil.myRandom(10, "Stadtaufruhr1") == 0:
										# 2 bis 4 Runden Aufstand!
										#iRand = 2 + CvUtil.myRandom(2, "Stadtaufruhr2")

										# in Abhaengigkeit von HURRY_ANGER_DIVISOR (GlobalDefines.xml) und iHurryConscriptAngerPercent (GameSpeedInfo.xml)
										#iRand = loopCity.flatHurryAngerLength()
										# loopCity.changeHurryAngerTimer(iRand)

										# Stadt ohne Kulturgrenzen
										#iRand = 2 + CvUtil.myRandom(3, "Stadtaufruhr3")
										#loopCity.setOccupationTimer (iRand)
										# if pPlayer.isHuman():
										#    CyInterface().addMessage(iPlayer, True, 5, CyTranslator().getText("TXT_KEY_MAIN_CITY_RIOT", (loopCity.getName(),)), "AS2D_REVOLTSTART", 2, ",Art/Interface/Buttons/Promotions/Combat5.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,5,10", ColorTypes(7), loopCity.getX(), loopCity.getY(), True, True)

										# Civil War (ab PAE 6.3.2)
										PAE_City.doStartCivilWar(loopCity, 100)

								# PAE 6.14: -1 in jeder Stadt (Stadtstatus: Stadt)
								if loopCity.isHasBuilding(eBuildingStadt):
										iHappy = loopCity.getBuildingHappyChange(eBuildingClass)
										iHappy -= 1
										loopCity.setBuildingHappyChange(eBuildingClass, iHappy)

										#if pPlayer.isHuman():
										#		CyInterface().addMessage(
										#			iPlayer, False, 20, "", None, 2, "Art/Interface/Buttons/General/button_icon_angry.dds",
										#			ColorTypes(7), loopCity.getX(), loopCity.getY(), True, True
										#		)

						(loopCity, pIter) = pPlayer.nextCity(pIter, False)


				if iWinnerPlayer != -1:
						pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
						# War Weariness
						pTeam.changeWarWeariness(pWinnerPlayer.getTeam(), 10)

						# PAE Movie (only a Great General)
						if pUnit.getLeaderUnitType() > -1 and (pPlayer.isHuman() and pPlayer.isTurnActive() or pWinnerPlayer.isHuman() and pWinnerPlayer.isTurnActive()):

								if pPlayer.getCurrentEra() > 2 or pWinnerPlayer.getCurrentEra() > 2:
										iVids = 14
								else:
										iVids = 11
								# GG dying movies (CvWonderMovieScreen)
								iMovie = 1 + CvUtil.myRandom(iVids, "GGDyingMovie")

								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
								popupInfo.setData1(iMovie)  # dynamicID in CvWonderMovieScreen
								popupInfo.setData2(-1)  # fix pCity.getID()
								popupInfo.setData3(4)  # fix PAE Movie ID for GG dies
								popupInfo.setText(u"showWonderMovie")
								if pPlayer.isHuman():
										popupInfo.addPopup(iPlayer)
								elif pWinnerPlayer.isHuman():
										popupInfo.addPopup(iWinnerPlayer)

						# PAE 6.14: +1 :) in jeder Stadt (Status Stadt, sofern Happyness < 0

						# PopUp
						#[H1]Ein gegnerischer General ist gefallen![\H1]
						if pWinnerPlayer.isHuman():
								iRand = 1 + CvUtil.myRandom(9, "Stadtaufruhr_Message")
								szTextKey = "TXT_KEY_MESSAGE_CITY_DYING_GENERAL2_" + str(iRand)
								szText = CyTranslator().getText("TXT_KEY_MESSAGE_CITY_DYING_GENERAL_TITLE", ())
								szText += CyTranslator().getText("[NEWLINE]", ())
								szText += CyTranslator().getText(szTextKey, ("",))
								szText += CyTranslator().getText("[NEWLINE]", ())
								szText += CyTranslator().getText("TXT_KEY_MESSAGE_CITY_DYING_GENERAL_POSITIVE", ())
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(szText)
								popupInfo.addPopup(iWinnerPlayer)

						(loopCity, pIter) = pWinnerPlayer.firstCity(False)
						while loopCity:
								if not loopCity.isNone():  # only valid cities
										if loopCity.isHasBuilding(eBuildingStadt):
												iHappy = loopCity.getBuildingHappyChange(eBuildingClass)
												#if iHappy < 0:
												iHappy += 1
												loopCity.setBuildingHappyChange(eBuildingClass, iHappy)

												#if pWinnerPlayer.isHuman():
												#		CyInterface().addMessage(
												#			iWinnerPlayer, False, 20, "", None, 2, "Art/Interface/Buttons/General/button_icon_happy.dds",
												#			ColorTypes(8), loopCity.getX(), loopCity.getY(), True, True
												#		)

								(loopCity, pIter) = pWinnerPlayer.nextCity(pIter, False)

						# PAE 6.16
						# --- Vasallen-Feature / Vassal feature
						# wenn ein General stirbt sollen die Vasallenverhältnisse gecheckt werden
						if not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_VASSAL_STATES):
								PAE_Vassal.onCityAcquired(None, iWinnerPlayer, iPlayer)


def unsettledSlaves(iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		lSlaves = []
		eUnitSlave = gc.getInfoTypeForString("UNIT_SLAVE")
		(loopUnit, pIter) = pPlayer.firstUnit(False)
		while loopUnit:
				if not loopUnit.isDead():  # is the unit alive and valid?
						if loopUnit.getUnitType() == eUnitSlave and loopUnit.getMoves() > 0:
								lSlaves.append(loopUnit)
				(loopUnit, pIter) = pPlayer.nextUnit(pIter, False)

		for pUnit in lSlaves:
				# Nicht als Cargo
				pPlot = pUnit.plot()
				if not pPlot.isWater():
						iChance = 8
						# Civic that increase rebelling
						if pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_FOEDERALISMUS")):
								iChance += 4
						# Military units decrease odds
						if pPlot.getNumDefenders(pUnit.getOwner()) > 0:
								iChance -= 4

						if iChance > CvUtil.myRandom(100, "Stehende Sklaven"):
								# wenn das Christentum gegruendet wurde / if christianity was found
								# Christ : Rebell = 1 : 4
								iReligion = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
								if gc.getGame().isReligionFounded(iReligion) and CvUtil.myRandom(4, "Stehende Sklaven Christ") == 1:
										iUnitType = gc.getInfoTypeForString("UNIT_CHRISTIAN_MISSIONARY")
										pPlayer.initUnit(iUnitType, pUnit.getX(), pUnit.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
										if pPlayer.isHuman():
												CyInterface().addMessage(iPlayer, True, 8, CyTranslator().getText("TXT_KEY_MESSAGE_SLAVE_2_CHRIST", (0,)), None, 2,
																								 "Art/Interface/Buttons/Actions/button_kreuz.dds", ColorTypes(14), pUnit.getX(), pUnit.getY(), True, True)
										# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
										pUnit.kill(True, -1)  # RAMK_CTD

										# ***TEST***
										#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Sklave zu Christ. Missionar (Zeile 1275)", 1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

								else:
										# Ein Sklave auf fremden Terrain kann nicht rebellieren sondern verschwindet oder macht einen Fluchtversuch 50:50
										if pPlot.getOwner() != pUnit.getOwner():
												if pPlayer.isHuman():
														iRand = 1 + CvUtil.myRandom(4, "FluchtversuchText")
														CyInterface().addMessage(iPlayer, True, 8, CyTranslator().getText("TXT_KEY_MESSAGE_SLAVE_LOST_"+str(iRand), (0, "")),
																										 None, 2, "Art/Interface/Buttons/Units/button_slave.dds", ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
												# Barbareneinheit erschaffen
												if CvUtil.myRandom(2, "Fluchtversuch") == 1:
														# Einen guenstigen Plot auswaehlen
														rebelPlotArray = []
														iX = pUnit.getX()
														iY = pUnit.getY()
														for i in range(3):
																for j in range(3):
																		loopPlot = gc.getMap().plot(iX + i - 1, iY + j - 1)
																		if loopPlot is not None and not loopPlot.isNone() and not loopPlot.isUnit():
																				if not loopPlot.isImpassable() and not loopPlot.isWater() and not loopPlot.isPeak():
																						rebelPlotArray.append(loopPlot)
														if rebelPlotArray:
																pPlot = rebelPlotArray[CvUtil.myRandom(len(rebelPlotArray), "Fluchtversuch3")]
																iUnitType = gc.getInfoTypeForString("UNIT_SLAVE")
																CvUtil.spawnUnit(iUnitType, pPlot, gc.getPlayer(gc.getBARBARIAN_PLAYER()))

												# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
												pUnit.kill(True, -1)  # RAMK_CTD
												# ***TEST***
												#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Slave lost in enemy territory (Zeile 1297)", 1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

										else:
												# Einen guenstigen Plot auswaehlen
												rebelPlotArray = []
												rebelPlotArrayB = []
												iX = pUnit.getX()
												iY = pUnit.getY()
												for i in range(3):
														for j in range(3):
																loopPlot = gc.getMap().plot(iX + i - 1, iY + j - 1)
																if loopPlot is not None and not loopPlot.isNone() and not loopPlot.isUnit():
																		if loopPlot.getOwner() == iPlayer:
																				if loopPlot.isHills():
																						rebelPlotArray.append(loopPlot)
																				if not loopPlot.isWater() and not loopPlot.isImpassable() and not loopPlot.isCity():
																						rebelPlotArrayB.append(loopPlot)

												if not rebelPlotArray:
														rebelPlotArray = rebelPlotArrayB

												# es kann rebelliert werden
												if rebelPlotArray:
														pPlot = rebelPlotArray[CvUtil.myRandom(len(rebelPlotArray), "rebelPlotArray3")]
														iUnitType = gc.getInfoTypeForString("UNIT_REBELL")
														CvUtil.spawnUnit(iUnitType, pPlot, gc.getPlayer(gc.getBARBARIAN_PLAYER()))
														if pPlayer.isHuman():
																CyInterface().addMessage(iPlayer, True, 8, CyTranslator().getText("TXT_KEY_MESSAGE_SLAVE_2_REBELL", (0,)), None, 2,
																												 "Art/Interface/Buttons/Units/button_rebell.dds", ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
														# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
														pUnit.kill(True, -1)  # RAMK_CTD
														# ***TEST***
														#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Sklave zu Rebell (Zeile 1327)", 1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

# Next Unit after NetMessage
def doGoToNextUnit(pUnit):
		# go to and select next Unit
		if gc.getPlayer(pUnit.getOwner()).isHuman():
				pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)


def copyName(NewUnit, iUnitType, sUnitName):
		if sUnitName != gc.getUnitInfo(iUnitType).getText():
				sUnitName = re.sub(r" \(.*?\)", "", sUnitName)
				NewUnit.setName(sUnitName)


def copyPromotions(OldUnit, NewUnit):
		iRange = gc.getNumPromotionInfos()
		for iPromo in range(iRange):
				if OldUnit.isHasPromotion(iPromo):
						NewUnit.setHasPromotion(iPromo, True)
		NewUnit.setExperience(OldUnit.getExperience(), -1)
		NewUnit.setLevel(OldUnit.getLevel())


def initSupply(pUnit):
		iMaxSupply = getMaxSupply(pUnit)
		setSupply(pUnit, iMaxSupply)


def fillSupply(pUnit, iChange):
		iMaxSupply = getMaxSupply(pUnit)
		iCurrentSupply = getSupply(pUnit)
		if iCurrentSupply != iMaxSupply:
				if iCurrentSupply + iChange > iMaxSupply:
						iChange -= (iMaxSupply - iCurrentSupply)
						iCurrentSupply = iMaxSupply
				else:
						iCurrentSupply += iChange
						iChange = 0

		setSupply(pUnit, iCurrentSupply)
		return iChange


def setSupply(pUnit, iValue):
		CvUtil.addScriptData(pUnit, "s", iValue)


def getSupply(pUnit):
		iMaxSupply = getMaxSupply(pUnit)

		# kein Eintrag == fabriksneu
		iCurrentSupply = CvUtil.getScriptData(pUnit, ["s"], iMaxSupply)
		if iCurrentSupply > iMaxSupply:
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Current Supply is bogus", iCurrentSupply)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				setSupply(pUnit, iMaxSupply)
				iCurrentSupply = iMaxSupply
		return iCurrentSupply


def getMaxSupply(pUnit):
		iMaxSupply = 100 # Medic1 sollte die Einheit schon haben, die diese Funktion aufruft
		if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MEDIC2")): iMaxSupply += 100
		if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MEDIC3")): iMaxSupply += 100
		if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MEDIC4")): iMaxSupply += 100
		if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MEDIC5")): iMaxSupply += 100
		# Trait Strategist / Stratege: +50% Kapazitaet / +50% capacity
		if gc.getPlayer(pUnit.getOwner()).hasTrait(gc.getInfoTypeForString("TRAIT_STRATEGE")):
				iMaxSupply += int(iMaxSupply/2)
		return iMaxSupply


def getHeldendenkmal(pUnit):
		return CvUtil.getScriptData(pUnit, ["hd"], -1)


def renegade(pWinner, pLoser):
		iWinnerPlayer = pWinner.getOwner()
		pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
		iLoserPlayer = pLoser.getOwner()
		pLoserPlayer = gc.getPlayer(iLoserPlayer)
		pLoserPlot = pLoser.plot()
		pWinnerPlot = pWinner.plot()
		iWinnerUnitAIType = pWinner.getUnitAIType()
		iWinnerUnitType = pWinner.getUnitType()
		iLoserUnitAIType = pLoser.getUnitAIType()
		iLoserUnitType = pLoser.getUnitType()

		bUnitRenegades = True

		iPromoMercenary = gc.getInfoTypeForString("PROMOTION_MERCENARY")
		iPromoLeader = gc.getInfoTypeForString("PROMOTION_LEADER")

		#iPromoSurrender = gc.getInfoTypeForString("PROMOTION_FORM_WHITEFLAG")
		lUnitAI = [UnitAITypes.UNITAI_ANIMAL, UnitAITypes.UNITAI_EXPLORE]

		# Ausnahmen - using UnitArray from above
		if iWinnerUnitAIType in lUnitAI:
				bUnitRenegades = False
		elif iWinnerUnitType in L.LUnitWildAnimals:
				bUnitRenegades = False
		elif iLoserUnitAIType in lUnitAI:
				bUnitRenegades = False
		elif(iLoserUnitType in L.LUnitWarAnimals or
				 iLoserUnitType in L.LUnitLootLessSeaUnits or
				 iLoserUnitType in L.LUnitCanBeDomesticated or
				 iLoserUnitType in L.LTradeUnits or
				 iLoserUnitType in L.LUnitWildAnimals):
				bUnitRenegades = False
		# Rammen und Katapulte sollen nicht erobern
		# PAE V: Piraten sollen nur kentern: UnitInfos.xml: bNoCapture=1
		elif pWinner.isNoCapture():
				bUnitRenegades = False
		elif pLoser.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SIEGE"):
				bUnitRenegades = False
		# elif pLoser.isHasPromotion(iPromoSurrender): bUnitRenegades = True
		elif pLoser.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LOYALITAT")) and not pLoser.isHasPromotion(iPromoMercenary):
				bUnitRenegades = False
		elif pLoser.isHasPromotion(iPromoLeader) or pLoser.isHasPromotion(gc.getInfoTypeForString("PROMOTION_BRANDER")) or pWinner.isNoCapture():
				bUnitRenegades = False
		elif pLoser.isHasPromotion(gc.getInfoTypeForString("PROMOTION_HERO")) or pLoser.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADERSHIP")):
				bUnitRenegades = False
		# elif pLoser.hasCargo() and pLoser.canAttack():
		#    bUnitRenegades = False
		elif pLoserPlot.getNumUnits() == 1 and pLoser.getCaptureUnitType(pLoser.getCivilizationType()) != -1:
				bUnitRenegades = False
		# Attacking from Coast
		elif pWinner.isCargo():
				if pWinnerPlot.isWater():
						iNumCargoSpace = 0
						iNumCargoUnits = 0
						iRange = pWinnerPlot.getNumUnits()
						for i in range(iRange):
								pLoopUnit = pWinnerPlot.getUnit(i)
								if pLoopUnit.getOwner() == iWinnerPlayer:
										iNumCargoSpace += pLoopUnit.cargoSpace()
										iNumCargoUnits += pLoopUnit.getCargo()
						if iNumCargoSpace <= iNumCargoUnits:
								bUnitRenegades = False

		if bUnitRenegades:
				# if pLoser.isHasPromotion(iPromoSurrender): iRandMax = 0 #100%
				iUnitRenegadeChance = 30  # 30%
				if pWinner.isHasPromotion(iPromoLeader):
						iUnitRenegadeChance += 10
				if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_HERO")):
						iUnitRenegadeChance += 10
				# Trait Charismatic: Mehr Ueberlaeufer / more renegades
				if pWinnerPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_CHARISMATIC")):
						iUnitRenegadeChance += 10
				if pLoserPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_CHARISMATIC")):
						iUnitRenegadeChance -= 10
				if pLoser.isHasPromotion(iPromoMercenary):
						iUnitRenegadeChance += 10

				if pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS3")):
						iUnitRenegadeChance = 75
				elif pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS2")):
						iUnitRenegadeChance = 50
				elif pWinner.isHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS1")):
						iUnitRenegadeChance = 30

				iRand = CvUtil.myRandom(100, "renegade")
				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Einheit allegiance Chance (Zeile 4150)", iRand)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				# Winner gets Loser Unit
				if iRand < iUnitRenegadeChance:
						bUnitRenegades = doRenegadeUnit(pLoser, pWinner, pLoserPlayer, pWinnerPlayer)
				else:
						bUnitRenegades = False
		return bUnitRenegades


def doNavalOnCombatResult(pWinner, pLoser, bWinnerIsDead):
		bUnitDone = False
		iWinnerPlayer = pWinner.getOwner()
		pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
		iLoserUnitType = pLoser.getUnitType()

		if not bWinnerIsDead:
				# ---- Schiffe sollen nach dem Angriff die Haelfte der uebrigen Bewegungspunkte haben "
				pWinner.changeMoves((pWinner.maxMoves()-pWinner.getMoves())/2)

		# Seeeinheiten (Treibgut erzeugen)
		iUnitTreibgut = gc.getInfoTypeForString("UNIT_TREIBGUT")
		# ---- SEA: Schiffe sollen Treibgut erzeugen
		if pLoser.getUnitType() not in L.LUnitLootLessSeaUnits:
				# Treibgut Chance 50%
				if CvUtil.myRandom(2, "Treibgut") == 0:
						terrain1 = gc.getInfoTypeForString("TERRAIN_OCEAN")
						terrain2 = gc.getInfoTypeForString("TERRAIN_COAST")
						iIce = gc.getInfoTypeForString("FEATURE_ICE")
						iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

						# Freie Plots finden
						SeaPlots = []
						iX = pLoser.getX()
						iY = pLoser.getY()
						for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
								loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
								if loopPlot is not None and not loopPlot.isNone():
										if loopPlot.getFeatureType() == iDarkIce or loopPlot.getFeatureType() == iIce:
												continue
										if not loopPlot.isPeak() and not loopPlot.isCity() and not loopPlot.isHills():
												if loopPlot.getTerrainType() == terrain1 or loopPlot.getTerrainType() == terrain2:
														if not loopPlot.isUnit():
																SeaPlots.append(loopPlot)

						if SeaPlots:
								if gc.getUnitInfo(iLoserUnitType).getProductionCost() > 180:
										iMaxTreibgut = 2
								else:
										iMaxTreibgut = 1
								barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

								for _ in range(iMaxTreibgut):
										if not SeaPlots:
												break
										iRand = CvUtil.myRandom(len(SeaPlots), "SeaPlots")
										loopPlot = SeaPlots[iRand]
										# Treibgut erzeugen
										NewUnit = barbPlayer.initUnit(iUnitTreibgut, loopPlot.getX(), loopPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
										# NewUnit.setImmobileTimer(2)
										if pWinnerPlayer.isHuman():
												CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_UNIT_ERSTELLT", (gc.getUnitInfo(iUnitTreibgut).getDescription(),)),
																								 None, 2, gc.getUnitInfo(iUnitTreibgut).getButton(), ColorTypes(11), loopPlot.getX(), loopPlot.getY(), True, True)
										# Plot aus der Liste entfernen
										SeaPlots.remove(loopPlot)

		# --- Treibgut gibt Sklaven oder Gold, wenn iCargo nicht voll is
		elif pLoser.getUnitType() == iUnitTreibgut:
				bUnitDone = True
				bMove2NextPlot = False
				# Ist ein freier Platz am Schiff?
				if not bWinnerIsDead and pWinner.getCargo() < pWinner.cargoSpace():
						# Treibgut einfangen
						iRand = CvUtil.myRandom(3, "Treibgut einfangen")
						if iRand == 0:
								iUnit = gc.getInfoTypeForString("UNIT_SLAVE")
								NewUnit = pWinnerPlayer.initUnit(iUnit, pWinner.getX(), pWinner.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								NewUnit.setTransportUnit(pWinner)
								NewUnit.finishMoves()
								if pWinnerPlayer.isHuman():
										CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_UNIT_TREIBGUT_SLAVE", ("",)),
																						 None, 2, gc.getUnitInfo(iUnit).getButton(), ColorTypes(8), pLoser.getX(), pLoser.getY(), True, True)
						elif iRand == 1:
								iRand = 11 + CvUtil.myRandom(20, "Treibgut einfangen3")
								pWinnerPlayer.changeGold(iRand)
								if pWinnerPlayer.isHuman():
										CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MONEY_UNIT_KILLED", ("", iRand)),
																						 None, 2, gc.getUnitInfo(iUnitTreibgut).getButton(), ColorTypes(8), pLoser.getX(), pLoser.getY(), True, True)
						# Treibgut nicht eingefangen
						else:
								# Einheit Treibgut neu erzeugen
								bMove2NextPlot = True
								if pWinnerPlayer.isHuman():
										iRand = 1 + CvUtil.myRandom(9, "Treibgut einfangen4")
										szText = CyTranslator().getText("TXT_KEY_UNIT_TREIBGUT_CATCHME"+str(iRand), ())
										CyInterface().addMessage(iWinnerPlayer, True, 10, szText, None, 2, gc.getUnitInfo(iUnitTreibgut).getButton(), ColorTypes(11), pLoser.getX(), pLoser.getY(), True, True)
				# Cargo voll
				else:
						# Einheit Treibgut neu erzeugen
						bMove2NextPlot = True
						if pWinnerPlayer.isHuman():
								CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_UNIT_TREIBGUT_NOSPACE", ("",)), None,
																				 2, gc.getUnitInfo(iUnitTreibgut).getButton(), ColorTypes(11), pLoser.getX(), pLoser.getY(), True, True)

				# Treibgut soll nicht ausserhalb der Kulturgrenze wiederauftauchen (jumpToNearestValidPlot), sondern gleich 1 Plot daneben (sofern frei)
				if bMove2NextPlot:
						lNewPlot = []
						iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
						iX = pLoser.getX()
						iY = pLoser.getY()
						for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
								loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
								if loopPlot and not loopPlot.isNone():
										if loopPlot.getFeatureType() != iDarkIce:
												if not loopPlot.isUnit():
														if loopPlot.isWater():
																lNewPlot.append(loopPlot)
						pJumpPlot = None
						if lNewPlot:
								iRand = CvUtil.myRandom(len(lNewPlot), "Treibgut einfangen5")
								pJumpPlot = lNewPlot[iRand]
						else: 
								pJumpPlot = getNearestValidPlot(pLoser)
						# elif pLoser.jumpToNearestValidPlot():
						# 		pJumpPlot = pLoser.plot()
						if pJumpPlot is not None:
								# Create unit
								CvUtil.spawnUnit(iUnitTreibgut, pJumpPlot, gc.getPlayer(gc.getBARBARIAN_PLAYER()))
		return bUnitDone

def getNearestValidPlot(pUnit):
	#pNearestCity = gc.getMap().findCity(pUnit.getX(), pUnit.getY(), pUnit.getOwner(),-1,True,False,-1,4,None)
	iBestValue = 999 #MAX_INT ? = welcher Wert war dafür gedacht?
	pBestPlot = None

	for iI in xrange(gc.getMap().numPlots()):
		pLoopPlot = gc.getMap().plotByIndex(iI)

		if pLoopPlot.isValidDomainForLocation(pUnit):
			if pUnit.canMoveInto(pLoopPlot, False, False, True):
				if pUnit.canEnterArea(pLoopPlot.getTeam(), pLoopPlot.area(), False):  # and not pUnit.isEnemy(pLoopPlot.getTeam(), pLoopPlot):
					if (pUnit.getDomainType() != DomainTypes.DOMAIN_AIR) or pLoopPlot.isFriendlyCity(pUnit, True):
						if pLoopPlot.isRevealed(pUnit.getTeam(), False):
							iValue = plotDistance(pUnit.getX(), pUnit.getY(), pLoopPlot.getX(), pLoopPlot.getY())
							#if pNearestCity:
							#	iValue += plotDistance(pLoopPlot.getX(), pLoopPlot.getY(), pNearestCity.getX(), pNearestCity.getY())
							if pUnit.getDomainType() == DomainTypes.DOMAIN_SEA and not pUnit.plot().isWater():
								if not pLoopPlot.isWater() or not pLoopPlot.isAdjacentToArea(pUnit.area()):
									iValue *= 3
							elif pLoopPlot.area() != pUnit.area():
								iValue *= 3
							if iValue < iBestValue:
								iBestValue = iValue
								pBestPlot = pLoopPlot
	return pBestPlot


def doLoserLoseHorse(pLoser, iWinnerPlayer):
		iLoserPlayer = pLoser.getOwner()
		pLoserPlayer = gc.getPlayer(iLoserPlayer)
		pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
		pLoserPlot = pLoser.plot()
		iLoserUnitType = pLoser.getUnitType()
		bDoIt = False
		iNewUnitType = -1
		if iLoserUnitType in L.DHorseDownMap:
				dTmp = L.DHorseDownMap.get(iLoserUnitType)
				if dTmp:
						iNewUnitType = dTmp.get(pLoser.getCivilizationType(), dTmp[None])

				bDoIt = True
		elif pLoser.getUnitType() == gc.getInfoTypeForString("UNIT_PRAETORIAN_RIDER"):
				iNewUnitType = gc.getInfoTypeForString("UNIT_PRAETORIAN")
				bDoIt = True

		# basic chariots only horses
		elif gc.getUnitInfo(pLoser.getUnitType()).getPrereqAndBonus() == gc.getInfoTypeForString("BONUS_HORSE"):
				bDoIt = True

		if bDoIt:
				iRand = CvUtil.myRandom(10, "mountedToMelee")
				if iRand < 5 and iNewUnitType != -1:
						# Create a new unit
						NewUnit = pLoserPlayer.initUnit(iNewUnitType, pLoser.getX(), pLoser.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						NewUnit.setExperience(pLoser.getExperience(), -1)
						NewUnit.setLevel(pLoser.getLevel())
						NewUnit.finishMoves()
						NewUnit.setDamage(50, -1)
						# Check its promotions
						iRange = gc.getNumPromotionInfos()
						for iPromotion in range(iRange):
								# init all promotions the unit had
								if pLoser.isHasPromotion(iPromotion):
										NewUnit.setHasPromotion(iPromotion, True)

						if pWinnerPlayer.isHuman():
								CyInterface().addMessage(iWinnerPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_LOST_HORSE_1",
																																												(gc.getUnitInfo(iLoserUnitType).getDescription(), 0)), None, 2, None, ColorTypes(7), 0, 0, False, False)
						if pLoserPlayer.isHuman():
								CyInterface().addMessage(iLoserPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_LOST_HORSE_2", (gc.getUnitInfo(iLoserUnitType).getDescription(), 0)), None, 2, None, ColorTypes(8), 0, 0, False, False)
						return True
				if iRand < 3:
						# Create horse unit
						iUnitType = gc.getInfoTypeForString("UNIT_HORSE")
						# Seek a Plot
						rebelPlotArray = []
						iX = pLoser.getX()
						iY = pLoser.getY()
						for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
								loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
								if loopPlot is not None and not loopPlot.isNone() and not loopPlot.isUnit():
										if not loopPlot.isWater() and not loopPlot.isImpassable() and not loopPlot.isCity():
												rebelPlotArray.append(loopPlot)

						# Create Barbarian Horse Unit
						if rebelPlotArray:
								barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
								iPlot = CvUtil.myRandom(len(rebelPlotArray), "horseLost")
								CvUtil.spawnUnit(iUnitType, rebelPlotArray[iPlot], barbPlayer)
						else:
								CvUtil.spawnUnit(iUnitType, pLoserPlot, pLoserPlayer)
						if pLoserPlayer.isHuman():
								CyInterface().addMessage(iLoserPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_ONLY_HORSE_LEFT", (gc.getUnitInfo(iLoserUnitType).getDescription(), 0)), None, 2, None, ColorTypes(6), 0, 0, False, False)
						return True
		return False


def huntingResult(pLoser, pWinner):
		iWinnerPlayer = pWinner.getOwner()
		pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
		iWinnerUnitType = pWinner.getUnitType()
		iLoserUnitType = pLoser.getUnitType()
		if pLoser.getCaptureUnitType(pWinnerPlayer.getCivilizationType()) != -1:
				# unit will be captured, thus not butchered
				return

		iJagd = gc.getInfoTypeForString("TECH_HUNTING")
		team = gc.getTeam(pWinnerPlayer.getTeam())
		if team.isHasTech(iJagd):
				
				# Bestimmte Stadt (im Umkreis)
				pHunterCityPlot = huntingCity(pWinner)
				if pHunterCityPlot is not None:
						iFoodMin, iFoodRand = L.DJagd.get(iLoserUnitType, L.DJagd[None])

						iFoodAdd = iFoodMin + CvUtil.myRandom(iFoodRand, "Hunt")

						# Hunter gets double bonus
						if iWinnerUnitType == gc.getInfoTypeForString("UNIT_HUNTER"):
								iFoodAdd *= 2

						pHunterCity = pHunterCityPlot.getPlotCity()
						pHunterCity.changeFood(iFoodAdd)
						if pWinnerPlayer.isHuman():
								CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_ADD_FOOD", (pWinner.getName(),
								pHunterCity.getName(), iFoodAdd)), None, 2, pLoser.getButton(), ColorTypes(14), pLoser.getX(), pLoser.getY(), True, True)

				# Irgendeine Stadt im Umkreis (bis PAE 6.18)
				#CityArray = []
				#(loopCity, pIter) = pWinnerPlayer.firstCity(False)
				#while loopCity:
				#		if huntingDistance(loopCity.plot(), pWinner.plot()) or huntingDistance(loopCity.plot(), pLoser.plot()):
				#				CityArray.append(loopCity)
				#		(loopCity, pIter) = pWinnerPlayer.nextCity(pIter, False)
				#if CityArray:
				#		iFoodMin, iFoodRand = L.DJagd.get(iLoserUnitType, L.DJagd[None])
				#		iFoodAdd = iFoodMin + CvUtil.myRandom(iFoodRand, "Hunt")
				#		# Hunter gets double bonus
				#		if iWinnerUnitType == gc.getInfoTypeForString("UNIT_HUNTER"):
				#				iFoodAdd *= 2
				#		iCity = CvUtil.myRandom(len(CityArray), "HuntCity")
				#		CityArray[iCity].changeFood(iFoodAdd)
				#		if pWinnerPlayer.isHuman():
				#				CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_ADD_FOOD", (pWinner.getName(),
				#				CityArray[iCity].getName(), iFoodAdd)), None, 2, pLoser.getButton(), ColorTypes(13), pLoser.getX(), pLoser.getY(), True, True)

def huntingDistance(pPlot1, pPlot2):
		if pPlot1 is not None and not pPlot1.isNone():
				if pPlot2 is not None and not pPlot2.isNone():
						# if pPlot1.getArea() == pPlot2.getArea():
						#iDist = gc.getMap().calculatePathDistance(pPlot1, pPlot2)
						iDistance = getHuntingDistance()
						iDist = plotDistance(pPlot1.getX(), pPlot1.getY(), pPlot2.getX(), pPlot2.getY())
						if iDist > -1 and iDist <= iDistance:
								return True
		return False

def getHuntingDistance():
	sScenarioName = CvUtil.getScriptData(CyMap().plot(0, 0), ["S", "t"])
	# Szenario: Weg der Goten
	#[EVENT-1.2] Jagdgebiet wird erweitert:
	#8 Plots um eigene Städte kann Nahrung erjagt werden
	if sScenarioName == "WegDerGoten": return 8
	else: return 4

def huntingCity(pUnit):
		iX = pUnit.getX()
		iY = pUnit.getY()
		iUnitOwner = pUnit.getOwner()
		# PAE VII: auch bei Vasallen oder MP Team Games
		pPlayer = gc.getPlayer(iUnitOwner)
		iTeam = pPlayer.getTeam()
		lTeamPlayer = []
		iRange = gc.getMAX_PLAYERS()
		for i in range(iRange):
			pTmp = gc.getPlayer(i)
			iTmp = pTmp.getTeam()
			if iTmp == iTeam or gc.getTeam(iTmp).isVassal(iTeam):
				lTeamPlayer.append(i)

		iCityPop = 0
		iCityDist = 0
		pPlot = None
		iDistance = getHuntingDistance()
		for x in range(-iDistance,iDistance):
				for y in range(-iDistance,iDistance):
						loopPlot = gc.getMap().plot(iX+x, iY+y)
						if loopPlot is not None and not loopPlot.isNone():
								if loopPlot.isCity() and loopPlot.getOwner() in lTeamPlayer:
										iPopCheck = loopPlot.getPlotCity().getPopulation()
										iDist = plotDistance(loopPlot.getX(), loopPlot.getY(), iX, iY)
										if iCityPop == 0 or (iCityPop > iPopCheck or iCityDist > iDist):
												pPlot = loopPlot
												iCityPop = iPopCheck
												iCityDist = iDist
		return pPlot


def rebell(pOldUnit, pNewPlayer, pPlot):
		iUnitType = pOldUnit.getUnitType()
		pNewUnit = pNewPlayer.initUnit(iUnitType, pPlot.getX(), pPlot.getY(), UnitAITypes(pOldUnit.getUnitAIType()), DirectionTypes.DIRECTION_SOUTH)
		initUnitFromUnit(pOldUnit, pNewUnit)
		pNewUnit.setDamage(pOldUnit.getDamage(), -1)
		# Original unit killen
		# pOldUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
		pOldUnit.kill(True, -1)  # RAMK_CTD


def doRenegadeUnit(pLoser, pWinner, pLoserPlayer, pWinnerPlayer):
		bUnitDone = False
		iLoserUnitType = pLoser.getUnitType()
		# Winner gets Loser Unit
		if CvUtil.myRandom(4, "actualRenegade") == 0:
				# Piratenschiffe werden normale Schiffe, alles weitere bleibt der gleiche UnitType
				iNewUnitType = L.DCaptureFromPirate.get(iLoserUnitType, iLoserUnitType)

				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("UnitType zum Ueberlaufen: ", iNewUnitType)), None, 2, None, ColorTypes(14), pWinner.getX(), pWinner.getY(), False, False)
				# Create a new unit
				NewUnit = pWinnerPlayer.initUnit(iNewUnitType, pWinner.getX(), pWinner.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				NewUnit.finishMoves()

				if pLoser.getUnitCombatType() != -1:
						NewUnit = initUnitFromUnit(pLoser, NewUnit)
						NewUnit.setDamage(90, -1)

						iPromoLoyal = gc.getInfoTypeForString("PROMOTION_LOYALITAT")
						iPromoMercenary = gc.getInfoTypeForString("PROMOTION_MERCENARY")
						iPromoAngst = gc.getInfoTypeForString("PROMOTION_ANGST")
						# PAE V: Loyal weg, Mercenary dazu
						if NewUnit.isHasPromotion(iPromoLoyal):
								NewUnit.setHasPromotion(iPromoLoyal, False)
						if not NewUnit.isHasPromotion(iPromoMercenary):
								NewUnit.setHasPromotion(iPromoMercenary, True)
						# PAE VI 6.11: Angst weg
						if NewUnit.isHasPromotion(iPromoAngst):
								NewUnit.setHasPromotion(iPromoAngst, False)

						# Remove formations
						doUnitFormation(NewUnit, -1)

						# PAE V: Trait-Promotions
						# 1. Agg und Protect Promos weg
						# (2. Trait nur fuer Eigenbau: eroberte Einheiten sollen diese Trait-Promos nicht erhalten) Stimmt nicht, sie erhalten die Promo bei initUnit() sowieso
						if not pWinnerPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_AGGRESSIVE")):
								iPromo = gc.getInfoTypeForString("PROMOTION_TRAIT_AGGRESSIVE")
								if NewUnit.isHasPromotion(iPromo):
										NewUnit.setHasPromotion(iPromo, False)

				if pWinnerPlayer.isHuman():
						CyInterface().addMessage(pWinnerPlayer.getID(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_DESERTION_1",
						(gc.getUnitInfo(iLoserUnitType).getDescription(), 0)), None, 2, None, ColorTypes(14), pWinner.getX(), pWinner.getY(), False, False)
				if pLoserPlayer.isHuman():
						CyInterface().addMessage(pLoserPlayer.getID(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_DESERTION_2",
						(gc.getUnitInfo(iLoserUnitType).getDescription(), 0)), None, 2, None, ColorTypes(12), pWinner.getX(), pWinner.getY(), False, False)
				bUnitDone = True

				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Gewinner (" + str(pWinner.getOwner()) + ") bekommt Verlierer (" + str(pLoser.getOwner()) + ")", 1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

		# Winner gets Slave
		elif pWinner.getDomainType() == DomainTypes.DOMAIN_LAND:
				# Ausnahmen
				if pLoser.getUnitType() not in L.LUnitNoSlaves and pLoser.getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_SIEGE"):
						iTechEnslavement = gc.getInfoTypeForString("TECH_ENSLAVEMENT")
						iThisTeam = pWinnerPlayer.getTeam()
						team = gc.getTeam(iThisTeam)
						if team.isHasTech(iTechEnslavement):
								# Create a slave unit
								NewUnit = pWinnerPlayer.initUnit(gc.getInfoTypeForString("UNIT_SLAVE"), pWinner.getX(), pWinner.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								NewUnit.finishMoves()
								if pWinnerPlayer.isHuman():
										CyInterface().addMessage(pWinnerPlayer.getID(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_SLAVERY_1",
										(gc.getUnitInfo(iLoserUnitType).getDescription(), 0)), None, 2, None, ColorTypes(14), 0, 0, False, False)
								if pLoserPlayer.isHuman():
										CyInterface().addMessage(pLoserPlayer.getID(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_SLAVERY_2",
										(gc.getUnitInfo(iLoserUnitType).getDescription(), 0)), None, 2, None, ColorTypes(12), 0, 0, False, False)
								bUnitDone = True
								# ***TEST***
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Gewinner bekommt Sklave (Zeile 2627)", 1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		return bUnitDone


def convert(pOldUnit, iNewUnit, pPlayer):
		pNewUnit = pPlayer.initUnit(iNewUnit, pOldUnit.getX(), pOldUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes(pOldUnit.getFacingDirection()))
		pNewUnit = initUnitFromUnit(pOldUnit, pNewUnit)
		pNewUnit.setDamage(pOldUnit.getDamage(), -1)
		# 1 Bewegungspunkt Verlust
		pNewUnit.changeMoves(pOldUnit.getMoves() + 60)
		# extra fuer Piraten
		# Veteran und Mercenary Promo checken
		# Veteran ohne Mercenary bleibt ohne Mercenary
		#iPromoMercenary = gc.getInfoTypeForString("PROMOTION_MERCENARY")
		#if pOldUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT4")):
		#		if not pOldUnit.isHasPromotion(iPromoMercenary):
		#				if pNewUnit.isHasPromotion(iPromoMercenary):
		#						pNewUnit.setHasPromotion(iPromoMercenary, False)

		# Original unit killen
		#pOldUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
		pOldUnit.kill(True, -1)


def initUnitFromUnit(pOldUnit, pNewUnit):
		if pOldUnit is None or pOldUnit.isNone():
				return pNewUnit
		if pNewUnit is None or pNewUnit.isNone():
				return pNewUnit
		pNewUnit.setExperience(pOldUnit.getExperience(), -1)
		pNewUnit.setLevel(pOldUnit.getLevel())
		copyName(pNewUnit, pOldUnit.getUnitType(), pOldUnit.getName())
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",(pNewUnit.getName(),pNewUnit.getID())), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",(pOldUnit.getName(),pOldUnit.getID())), None, 2, None, ColorTypes(10), 0, 0, False, False)
		# Check its promotions
		if pNewUnit.canAcquirePromotionAny():
				iRange = gc.getNumPromotionInfos()
				for j in range(iRange):
						if "_FORM_" in gc.getPromotionInfo(j).getType():
								continue
						if pOldUnit.isHasPromotion(j) and pNewUnit.canAcquirePromotion(j):
								pNewUnit.setHasPromotion(j, True)
		return pNewUnit


def TrojanHorsePossible(pUnit):
		iX = pUnit.getX()
		iY = pUnit.getY()
		iUnitOwner = pUnit.getOwner()
		for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
				loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
				if loopPlot is not None and not loopPlot.isNone():
						if loopPlot.isCity():
								loopCity = loopPlot.getPlotCity()
								iCityOwner = loopCity.getOwner()
								if iCityOwner != iUnitOwner:
										if gc.getTeam(iUnitOwner).isAtWar(loopCity.getTeam()):
												iDefense = loopCity.getDefenseModifier(0)
												if iDefense >= 100:
														return True
		return False


def getNearestCity(pUnit):
		pUnitPlot = pUnit.plot()
		pPlayer = gc.getPlayer(pUnit.getOwner())
		iBestDistance = 999

		pCity = None
		(loopCity, pIter) = pPlayer.firstCity(False)
		while loopCity:
				if not loopCity.isNone():
						iDistance = CyMap().calculatePathDistance(pUnitPlot, loopCity.plot())
						if iDistance != -1 and iDistance < iBestDistance:
								pCity = loopCity
								iBestDistance = iDistance
				(loopCity, pIter) = pPlayer.nextCity(pIter, False)
		return pCity


def getGovCenter(pUnit):
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")
		iBuilding2 = gc.getInfoTypeForString("BUILDING_PRAEFECTUR")

		(loopCity, pIter) = pPlayer.firstCity(False)
		while loopCity:
				if not loopCity.isNone():
						if loopCity.isCapital() or loopCity.getNumBuilding(iBuilding) > 0 or loopCity.getNumBuilding(iBuilding2) > 0:
								iDist = gc.getMap().calculatePathDistance(loopCity.plot(), pUnit.plot())
								if iDist != -1:
										return True
				(loopCity, pIter) = pPlayer.nextCity(pIter, False)
		return False


def move2GovCenter(pUnit):
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")
		iBuilding2 = gc.getInfoTypeForString("BUILDING_PRAEFECTUR")
		iBestDist = 0
		pCity = None

		(loopCity, pIter) = pPlayer.firstCity(False)
		while loopCity:
				if not loopCity.isNone():
						if loopCity.isCapital() or loopCity.getNumBuilding(iBuilding) > 0 or loopCity.getNumBuilding(iBuilding2) > 0:
								iDist = gc.getMap().calculatePathDistance(loopCity.plot(), pUnit.plot())
								if iDist != -1 and (iBestDist == 0 or iDist < iBestDist):
										pCity = loopCity
										iBestDist = iDist
				(loopCity, pIter) = pPlayer.nextCity(pIter, False)

		if pCity != None:
				pUnit.getGroup().pushMoveToMission(pCity.getX(), pCity.getY())
				return True
		# bleib in der Stadt stehn
		elif pUnit.plot().isCity():
				return False
				pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, True, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
		# beweg dich in die nächstgelegene Stadt
		else:
				pCity = getNearestCity(pUnit)
				if pCity != None:
						pUnit.getGroup().pushMoveToMission(pCity.getX(), pCity.getY())
						return True
		# doGoToNextUnit(pUnit)

# Governor | Statthalter ---------------------------------------------
# Werte des Statthalters / governor
# --- 0: philosophisch: +5 Wissen
# --- 1: spirituell: +5 Kultur
# --- 2: finanziell: +5 Gold
# --- 3: industriell: +5 Hammer
# --- 4: kreativ: +5 Kommerz
# --- 5: imperialistisch: +5 Spio
# --- 6: organisiert: +2 Happy
# --- 7: expansiv: +2 Health
# Eventmanager: onUnitBuilt
def initStatthalter(pUnit):
		iRand = CvUtil.myRandom(8, "initStatthalter")
		CvUtil.addScriptData(pUnit, "typ", iRand)


def doSettleStatthalter(pUnit, pCity):
		# pPlayer = gc.getPlayer(pUnit.getOwner())
		iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")
		iBuildingClass = gc.getBuildingInfo(iBuilding).getBuildingClassType()
		# Statthalter Happiness holen
		iHappy = pCity.getBuildingHappyChange(iBuildingClass)
		# Statthaltersitz Werte resetten
		pCity.setNumRealBuilding(iBuilding, 1)
		pCity.setBuildingCommerceChange(iBuildingClass, CommerceTypes.COMMERCE_RESEARCH, 0)
		pCity.setBuildingCommerceChange(iBuildingClass, CommerceTypes.COMMERCE_CULTURE, 0)
		pCity.setBuildingCommerceChange(iBuildingClass, CommerceTypes.COMMERCE_GOLD, 0)
		pCity.setBuildingYieldChange(iBuildingClass, YieldTypes.YIELD_PRODUCTION, 0)
		pCity.setBuildingYieldChange(iBuildingClass, YieldTypes.YIELD_COMMERCE, 0)
		pCity.setBuildingCommerceChange(iBuildingClass, CommerceTypes.COMMERCE_ESPIONAGE, 0)
		pCity.setBuildingHappyChange(iBuildingClass, 0)
		pCity.setBuildingHealthChange(iBuildingClass, 0)
		# Werte des Statthalters adden
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("StatthalterClass",pUnit.getUnitClassType())), None, 2, None, ColorTypes(10), 0, 0, False, False)
		if pUnit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_STATTHALTER"):
				iTyp = CvUtil.getScriptData(pUnit, ["typ"], -1)
				# Test Message
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Statthaltertyp",iTyp)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				if iTyp == 0:
						pCity.setBuildingCommerceChange(iBuildingClass, CommerceTypes.COMMERCE_RESEARCH, 5)
				elif iTyp == 1:
						pCity.setBuildingCommerceChange(iBuildingClass, CommerceTypes.COMMERCE_CULTURE, 5)
				elif iTyp == 2:
						pCity.setBuildingCommerceChange(iBuildingClass, CommerceTypes.COMMERCE_GOLD, 5)
				elif iTyp == 3:
						pCity.setBuildingYieldChange(iBuildingClass, YieldTypes.YIELD_PRODUCTION, 5)
				elif iTyp == 4:
						pCity.setBuildingYieldChange(iBuildingClass, YieldTypes.YIELD_COMMERCE, 5)
				elif iTyp == 5:
						pCity.setBuildingCommerceChange(iBuildingClass, CommerceTypes.COMMERCE_ESPIONAGE, 5)
				elif iTyp == 6:
						iHappy += 2
				elif iTyp == 7:
						pCity.setBuildingHealthChange(iBuildingClass, 2)
				pCity.setBuildingHappyChange(iBuildingClass, iHappy)
		# Held oder Feldherr ansiedeln
		else:
				pCity.setBuildingYieldChange(iBuildingClass, YieldTypes.YIELD_COMMERCE, 5)
				pCity.setBuildingHappyChange(iBuildingClass, iHappy + 1)

		# Unit killen
		pUnit.kill(True, -1)


def doStatthalterTurn_AI(pUnit):

		return

		#pPlayer = gc.getPlayer(pUnit.getOwner())
		#iBuilding = gc.getInfoTypeForString("BUILDING_STATTHALTER")
		#iCityStatus = gc.getInfoTypeForString("BUILDING_STADT")

		#(loopCity, pIter) = pPlayer.firstCity(False)
		# while loopCity:
		#    if loopCity is not None and not loopCity.isNone():
		#        if loopCity.isHasBuilding(iCityStatus):
		#            if not loopCity.isHasBuilding(iBuilding):
		#                iDist = gc.getMap().calculatePathDistance(loopCity.plot(), pUnit.plot())
		#                if iDist == -1:
		#                    doSettleStatthalter(pUnit,loopCity)
		#                else:
		#                    pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, loopCity.getX(), loopCity.getY(), 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
		#                break
		#    (loopCity, pIter) = pPlayer.nextCity(pIter, False)
		#pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
		# doGoToNextUnit(pUnit)
# ------------------------------------------------------

# Heldendenkmal / Siegesdenkmal ------------------------
# Creates popup with all possible cultivation bonuses of the plot or city
def doPopupChooseHeldendenkmal(pUnit):
		# Unit check
		if pUnit is None or pUnit.isNone():
				return False

		pPlot = pUnit.plot()
		iPlayer = pUnit.getOwner()

		# City check
		pCity = pPlot.getPlotCity()
		if pCity is None or pCity.isNone():
				return False

		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_CHOOSE_HELDENDENKMAL", ("", )))
		popupInfo.setOnClickedPythonCallback("popupChooseHeldendenkmal")
		popupInfo.setData1(iPlayer)
		popupInfo.setData2(pUnit.getID())

		for iBuilding in L.LHeldendenkmal:
				if pCity.isHasBuilding(iBuilding):
						popupInfo.addPythonButton(gc.getBuildingInfo(iBuilding).getDescription(), gc.getBuildingInfo(iBuilding).getButton())

		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ("", )), "Art/Interface/Buttons/Actions/Cancel.dds")
		popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
		popupInfo.addPopup(iPlayer)


def doCollectHeldendenkmal(pUnit, iBuilding):
		if pUnit is None or pUnit.isNone():
				return False
		if iBuilding == -1:
				return False

		pCity = CyMap().plot(pUnit.getX(), pUnit.getY()).getPlotCity()
		pCity.setNumRealBuilding(iBuilding, 0)
		CvUtil.addScriptData(pUnit, "hd", iBuilding)

		pUnit.finishMoves()
		doGoToNextUnit(pUnit)


def doSetHeldendenkmal(pUnit):
		if pUnit is None or pUnit.isNone():
				return False
		iBuilding = int(CvUtil.getScriptData(pUnit, ["hd"], -1))
		if iBuilding == -1:
				return False

		pCity = CyMap().plot(pUnit.getX(), pUnit.getY()).getPlotCity()
		pCity.setNumRealBuilding(iBuilding, 1)
		CvUtil.addScriptData(pUnit, "hd", -1)
		CvUtil.removeScriptData(pUnit, "hd")

		pUnit.finishMoves()
		doGoToNextUnit(pUnit)
# -------------------------------------------------


def doBuyEscort(pUnit, iCost):
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		if (pPlayer.getGold() >= iCost):
				pPlayer.changeGold(-iCost)
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SCHUTZ"), True)
				# pUnit.finishMoves()
				if int(CvUtil.getScriptData(pUnit, ["autA", "t"], 0)) != 0:
						doGoToNextUnit(pUnit)


def getUnitSupplyFood():
		# 0 = GAMESPEED_MARATHON
		# 1 = GAMESPEED_EPIC
		# 2 = GAMESPEED_NORMAL
		# 3 = GAMESPEED_QUICK
		iSpeed = gc.getGame().getGameSpeedType()
		if iSpeed < 2:
				return 75 - (iSpeed * 25)
		else:
				return 25

# PAE unit costs some food from storage
def doDecreaseFoodOnUnitBuilt(pCity, pUnit):
		# Civic Bauernmiliz
		if gc.getPlayer(pUnit.getOwner()).isCivic(gc.getInfoTypeForString("CIVIC_BAUERNMILIZ")):
				return

		if pUnit.isMilitaryHappiness():
				if pUnit.getUnitType() not in L.LUnitsNoFoodCosts:

						# 50% der Produktionskosten werden vom Nahrungslager abgezogen
						# pro Getreidesorte gibts 10% Erm. dazu (TXT_KEY_BONUS_GRAIN_HELP anpassen)
						iFaktor = 50
						for i in L.LBonusGetreide:
								if pCity.hasBonus(i):
										iFaktor -= 10

						# PAE 6.2: KI nochmal 50% weniger Kosten
						if not gc.getPlayer(pUnit.getOwner()).isHuman():
								iFaktor /= 2

						if iFaktor > 0:
								iCostFood = min(int(gc.getUnitInfo(pUnit.getUnitType()).getProductionCost() * iFaktor / 100), pCity.getFood())
								if iCostFood > 0:
										pCity.changeFood(-iCostFood)

										if gc.getPlayer(pUnit.getOwner()).isHuman():
												# TXT_KEY_INFO_UNIT_FOOD: Die Einheit %s1_unit in %s2_city verbrauchte %d3% der [ICON_PRODUCTION]-Kosten: %d4[ICON_FOOD]
												text = CyTranslator().getText("TXT_KEY_INFO_UNIT_FOOD", (pUnit.getName(), pCity.getName(), iFaktor, iCostFood))
												CyInterface().addMessage(pUnit.getOwner(), True, 5, text, None, 2, None, ColorTypes(14), -1, -1, False, False)

# PAE supply wagon UNIT_SUPPLY_WAGON
def getSupplyFromPlot(iPlayer, pPlot):
		# Init
		iTeam = gc.getPlayer(iPlayer).getTeam()
		iLoopOwner = pPlot.getOwner()
		iSupplyChange = 10
		# Plot properties
		eImprovement = pPlot.getImprovementType()
		bDesert = pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DESERT")
		if bDesert: iSupplyChange -= 30

		lImpFood1 = [
				gc.getInfoTypeForString("IMPROVEMENT_FARM"),
				gc.getInfoTypeForString("IMPROVEMENT_PASTURE")
		]
		lImpFood2 = [
				gc.getInfoTypeForString("IMPROVEMENT_PLANTATION"),
				gc.getInfoTypeForString("IMPROVEMENT_BRUNNEN")
		]

		# Eigenes Terrain
		if iLoopOwner == iPlayer:
				if pPlot.isCity():
						pCity = pPlot.getPlotCity()
						# PAE V
						if pCity.getYieldRate(0) - pPlot.getNumDefenders(iPlayer) > 0:
								iSupplyChange = pCity.getYieldRate(0) - pPlot.getNumDefenders(iPlayer)
				else:
						if eImprovement == gc.getInfoTypeForString("IMPROVEMENT_FORT"):
								iSupplyChange += 35
						elif eImprovement == gc.getInfoTypeForString("IMPROVEMENT_FORT2"):
								iSupplyChange += 35
						elif eImprovement == gc.getInfoTypeForString("IMPROVEMENT_HANDELSPOSTEN"):
								iSupplyChange += 25
		# Fremdes Terrain
		else:
				if iLoopOwner != -1:
						pLoopOwner = gc.getPlayer(iLoopOwner)
						iTeamPlot = pLoopOwner.getTeam()
						pTeamPlot = gc.getTeam(iTeamPlot)

						# Vassalenterrain
						if pTeamPlot.isVassal(iTeam):
								if pPlot.isCity():
										pCity = pPlot.getPlotCity()
										# PAE V
										if pCity.getYieldRate(0) - pPlot.getNumDefenders(iPlayer) > 0:
												iSupplyChange = pCity.getYieldRate(0) - pPlot.getNumDefenders(iLoopOwner)
								iSupplyChange += 20

						# feindliches Terrain
						elif gc.getTeam(iTeam).isAtWar(iTeamPlot) and eImprovement != -1:
								# Plot wird beschlagnahmt
								iSupplyChange += 20

		# Allgemeines
		if eImprovement in lImpFood1:
				iSupplyChange += 20
		if eImprovement in lImpFood2:
				iSupplyChange += 15
		# Oase
		if pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_OASIS"):
				iSupplyChange += 10
		# Fluss oder fresh water
		if pPlot.isRiver() or pPlot.isFreshWater():
				iSupplyChange += 10

		if iSupplyChange <= 0: return 0

		return iSupplyChange

# PAE supply wagon UNIT_SUPPLY_WAGON
def getPlotSupplyCost(iPlayer, pPlot):
	# Init
	iMounted = 0
	iMelee = 0
	iStackLimit1 = getStackLimit()
	# Plot properties
	bDesert = (pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DESERT"))

	# PAE V: Stack Limit mit iStackLimit1 einbeziehen
	if pPlot.getNumDefenders(iPlayer) - iStackLimit1 <= 0:
		return 0

	# Units calc
	iNumUnits = pPlot.getNumUnits()
	for i in range(iNumUnits):
		pLoopUnit = pPlot.getUnit(i)
		if pLoopUnit.getOwner() == iPlayer:
			iUnitType = pLoopUnit.getUnitCombatType()
			if iUnitType in L.LMountedSupplyCombats:
				if bDesert:
					iMounted += 2
				else:
					iMounted += 1
			elif iUnitType in L.LMeleeSupplyCombats:
				iMelee += 1

	if iMounted + iMelee - iStackLimit1 <= 0:
		return 0
	else:
		return iMounted + iMelee


def move2nextPlot(pUnit, bWater):
	lNewPlot = []
	iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
	iX = pUnit.getX()
	iY = pUnit.getY()
	for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
		loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
		if loopPlot is not None and not loopPlot.isNone():
			if loopPlot.getFeatureType() != iDarkIce:
				if not loopPlot.isUnit():
					if bWater and loopPlot.isWater() or not bWater and not loopPlot.isWater():
						lNewPlot.append(loopPlot)
	pJumpPlot = None
	if lNewPlot:
		iRand = CvUtil.myRandom(len(lNewPlot), "move2nextPlot")
		pJumpPlot = lNewPlot[iRand]
		# move unit: setXY (INT iX, INT iY, BOOL bGroup, BOOL bUpdate, BOOL bShow)
		pUnit.setXY(pJumpPlot.getX(), pJumpPlot.getY(), True, True, True)
	else:
		pUnit.finishMoves()
	return

# Wald niederbrennen (765)
def doBurnDownForest(pUnit):
	pPlot = pUnit.plot()
	# Verbrannten Wald erzeugen
	pPlot.setFeatureType(gc.getInfoTypeForString("FEATURE_FOREST_BURNT"), 0)
	# Modernisierung entfernen
	pPlot.setImprovementType(-1)
	pUnit.getGroup().setActivityType(-1)  # to reload the map!
	pUnit.finishMoves()
	return

# Einheit Kultur geben
def setUnitCulture(pUnit):
	pPlot = pUnit.plot()
	# iCulture = city.findHighestCulture() Klappt nicht, da Kultur des Stadtplots benoetigt wird
	# Muss selbst bestimmt werden, da plot.findHighestCultureTeam() das Team, aber nicht die Civ zurueckgibt
	iCulture = -1
	iTmp = -1
	iRange = gc.getMAX_PLAYERS()
	for i in range(iRange):
		if pPlot.getCulture(i) > iTmp:
			iTmp = pPlot.getCulture(i)
			iCulture = i

	# Sollte auf dem Plot keine Kultur sein, gehoert der Auswanderer zur Kultur des Besitzers
	if iTmp == -1 or iCulture == -1:
		iCulture = pUnit.getOwner()

	CvUtil.addScriptData(pUnit, "p", iCulture)
	return

# Einheit Religion geben
def setUnitReligion(pUnit):
	pPlot = pUnit.plot()
	if not pPlot.isCity():
		return
	pCity = pPlot.getPlotCity()
	iReligion = PAE_City.getCityReligion(pCity)

	# Nur monotheistische Religionen zulassen
	if iReligion > -1 and iReligion in L.LMonoReligions:
		CvUtil.addScriptData(pUnit, "rel", iReligion)
	return

# Names for Great Generals
def getGGName(pPlayer):

	lUnitNames = []
	iMaxPlayers = gc.getMAX_PLAYERS()
	for i in range(iMaxPlayers):
		loopPlayer = gc.getPlayer(i)
		if loopPlayer is not None and not loopPlayer.isNone() and loopPlayer.isAlive():
			lUnits = PyPlayer(loopPlayer.getID()).getUnitList()
			for loopUnit in lUnits:
					if loopUnit is not None and not loopUnit.isNone():
							if loopUnit.isMilitaryHappiness() and loopUnit.getName() not in lUnitNames:
								lUnitNames.append(loopUnit.getName())

	GG_Name = ""
	listNames = []

	if pPlayer.getCurrentEra() >= 2:
		if pPlayer.getCivilizationType() in L.DGGNames:
			listNames = L.DGGNames[pPlayer.getCivilizationType()]

		# 1st: CIV names Iron Age
		if len(listNames):
			for iName in listNames:
				if iName not in GG_UsedNames and iName not in lUnitNames:
					GG_Name = iName
					break

		# 2nd: generic names Iron Age
		if GG_Name == "":
			listNames = L.LGGStandard
			for iName in listNames:
				if iName not in GG_UsedNames and iName not in lUnitNames:
					GG_Name = iName
					break

	# save official names only
	if GG_Name != "" and GG_Name not in GG_UsedNames:
		GG_UsedNames.append(GG_Name)

	# 3rd: random names stone/bronze age
	if GG_Name == "":
		listNames = L.LGGStoneAge
		listlength = len(listNames)
		for i in xrange(listlength):
				iRand = CvUtil.myRandom(listlength, "GGNames stone age")
				if listNames[iRand] not in lUnitNames:
						GG_Name = listNames[iRand]
						break

	return GG_Name

def onModNetMessage(argsList):
	iData0, iData1, iData2, iData3, iData4 = argsList
	iData5 = iData4
	iData4 = iData3
	iData3 = iData2
	iData2 = iData1
	iData1 = iData0

	# Unit mission button: Go2City
	# iData2: keine Stadt -1 oder StadtID
	if iData1 == 773:
		pPlayer = gc.getPlayer(iData4)
		pUnit = pPlayer.getUnit(iData5)
		pCapital = False

		lCities = []
		(loopCity, pIter) = pPlayer.firstCity(False)
		if loopCity is not None and not loopCity.isNone():
			while loopCity:
				if not loopCity.isNone():
					if pUnit.plot().getArea() == loopCity.plot().getArea() and not pUnit.atPlot(loopCity.plot()):
						if loopCity.isCapital():
							pCapital = (loopCity.getName(),loopCity.getID())
						else:
							lCities.append((loopCity.getName(),loopCity.getID()))
				(loopCity, pIter) = pPlayer.nextCity(pIter, False)

		lCities.sort()
		if pCapital: lCities.insert(0,pCapital)

		# PopUp choose city
		if iData2 == -1:

			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("popupGo2City")
			popupInfo.setData1(iData4) # iPlayer
			popupInfo.setData2(iData5) # iUnitID
			popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_GO2CITY", ("", )))

			for lCity in lCities:
				loopCity = gc.getPlayer(iData4).getCity(lCity[1])
				szText = lCity[0]
				if loopCity.isCapital(): szText = szText + u" %c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)
				elif loopCity.isGovernmentCenter(): szText = szText + u" %c" % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR)

				popupInfo.addPythonButton(szText, PAE_City.getCityStatus(loopCity, -1, -1, True))

			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ("", )), "Art/Interface/Buttons/Actions/Cancel.dds")
			popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
			popupInfo.addPopup(iData4)

		# Move unit 2 city
		else:
			pCity = gc.getPlayer(iData4).getCity(lCities[iData2][1])
			pUnit.getGroup().pushMoveToMission(pCity.getX(), pCity.getY())
			#doGoToNextUnit(pUnit)

# --- end onModNetMessage -----