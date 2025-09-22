# Plot features and events per turn

# Imports
from CvPythonExtensions import (CyGlobalContext, CyInterface, CyMap,
																CyTranslator, DirectionTypes, CommerceTypes,
																ColorTypes, UnitAITypes, CyPopupInfo,
																ButtonPopupTypes, plotXY, plotDirection,
																GameOptionTypes)
# import CvEventInterface
import CvUtil
import PAE_Barbaren
import PAE_Lists as L

import PyHelpers
# Defines
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

bMultiPlayer = False
bGoodyHuts = True
bBarbForts = True
bRageBarbs = False
# PAE VI: kein Treibgut mehr erstellen, es gibt eh soviel durch Seeschlachten
bFlotsam = False  # activates flotsam after a certain tech
bMovingBonus = True # nicht kultivierte oder von mind. 1 Einheit besetze Bonusressourcen sollen sich bewegen (Kuh, Schaf, Schwein, Pferd,..)

if gc.getGame().isGameMultiPlayer():
		bMultiPlayer = True
if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_GOODY_HUTS):
		bGoodyHuts = False
if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
		bBarbForts = False
if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_RAGING_BARBARIANS):
		bRageBarbs = True

# ------ Handelsposten erzeugen Kultur (PAE V Patch 3: und wieder Forts/Festungen)
# ------ Berberloewen erzeugen
# ------ Wildpferde, Wildelefanten, Wildkamele ab PAE V
# ------ Barbarenfort beleben (PAE V Patch 4)
# ------ Goody-Doerfer erstellen (goody-huts / GoodyHuts / Goodies / Villages)
# ------ Treibgut erstellen (wenn aktiviert)


def doPlotFeatures():

		iGameTurn = gc.getGame().getElapsedGameTurns()
		if iGameTurn < 5:
				return

		# Inits
		iBarbPlayer = gc.getBARBARIAN_PLAYER()
		pBarbPlayer = gc.getPlayer(iBarbPlayer)

		# Flotsam
		terrOzean = gc.getInfoTypeForString("TERRAIN_OCEAN")
		bFlot = gc.getTeam(pBarbPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_RUDERER2"))

		# Barbaren improvements
		impBarbFort = gc.getInfoTypeForString("IMPROVEMENT_BARBARENFORT")
		impCave = gc.getInfoTypeForString("IMPROVEMENT_CAVE")
		impGoody = gc.getInfoTypeForString("IMPROVEMENT_GOODY_HUT")
		iBarbForts = 0
		iCaves = 0
		iGoodyHuts = 0

		# Animals
		bonus_lion = gc.getInfoTypeForString("BONUS_LION")
		bonus_horse = gc.getInfoTypeForString("BONUS_HORSE")
		bonus_camel = gc.getInfoTypeForString("BONUS_CAMEL")
		bonus_ivory = gc.getInfoTypeForString("BONUS_IVORY")
		# bonus_dogs = gc.getInfoTypeForString("BONUS_HUNDE")
		bonus_deer = gc.getInfoTypeForString("BONUS_DEER")
		# bonus_pig = gc.getInfoTypeForString("BONUS_PIG")
		bonus_esel = gc.getInfoTypeForString("BONUS_ESEL")
		# features
		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
		iFeatBurned = gc.getInfoTypeForString("FEATURE_FOREST_BURNT")
		iFeatSeuche = gc.getInfoTypeForString("FEATURE_SEUCHE")
		iTerrDesert = gc.getInfoTypeForString("TERRAIN_DESERT")
		iTerrPlains = gc.getInfoTypeForString("TERRAIN_PLAINS")
		iTerrTundra = gc.getInfoTypeForString("TERRAIN_TUNDRA")
		iFeatForest = gc.getInfoTypeForString("FEATURE_FOREST")
		iFeatDenseForest = gc.getInfoTypeForString("FEATURE_DICHTERWALD")
		iFeatJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")

		# Heuschrecken/Grasshopper
		iFeatGrasshopper = gc.getInfoTypeForString("FEATURE_GRASSHOPPER")
		# Desert Storm
		iFeatDesertstorm = gc.getInfoTypeForString("FEATURE_FALLOUT")
		lDesertStorm = []

		# Plots
		Ocean = []
		Desert = []
		Forest = []
		DenseForest = []
		Tundra = []
		Plains = []
		Jungle = []
		Hills = []
		Peaks = []
		# GoodyPlots = []
		MovingBonus = []

		# Inits for plots check
		eHandelsposten = gc.getInfoTypeForString("IMPROVEMENT_HANDELSPOSTEN")
		eLion = gc.getInfoTypeForString("UNIT_LION")
		eBear = gc.getInfoTypeForString("UNIT_BEAR")
		eWolf = gc.getInfoTypeForString("UNIT_WOLF")
		eHorse = gc.getInfoTypeForString("UNIT_HORSE")
		eHorseTech = gc.getInfoTypeForString("TECH_PFERDEZUCHT")
		eCamel = gc.getInfoTypeForString("UNIT_CAMEL")
		eCamelTech = gc.getInfoTypeForString("TECH_KAMELZUCHT")
		eElefant = gc.getInfoTypeForString("UNIT_ELEFANT")
		eElefantTech = gc.getInfoTypeForString("TECH_ELEFANTENZUCHT")
		eEsel = gc.getInfoTypeForString("UNIT_ESEL")
		eEselTech = gc.getInfoTypeForString("TECH_FENCES")

		# map
		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()

		for x in range(iMapW):
				for y in range(iMapH):
						loopPlot = gc.getMap().plot(x, y)
						if loopPlot is not None and not loopPlot.isNone():

								iPlotFeature = loopPlot.getFeatureType()
								iPlotTerrain = loopPlot.getTerrainType()
								iPlotImprovement = loopPlot.getImprovementType()

								if iPlotFeature == iDarkIce:
										continue

								if iPlotFeature == iFeatGrasshopper:
										doMoveGrasshoppers(loopPlot)
										continue
								if iPlotFeature == iFeatDesertstorm:
										lDesertStorm.append(loopPlot)
										continue

								if loopPlot.getFeatureType() == iFeatBurned:
										if CvUtil.myRandom(50, "burntForest2Forest") == 1:
												loopPlot.setFeatureType(iFeatForest, 0)
										continue

								# isWater
								if loopPlot.isWater():

										# Treibgut nur alle 10 Runden erstellen (wenn aktiv)
										if bFlotsam and gc.getGame().getGameTurn() % 10 == 0:
												if bFlot and bGoodyHuts:
														if loopPlot.getOwner() == -1:
																if iPlotTerrain == terrOzean:
																		if loopPlot.getNumUnits() > 0:
																				Ocean.append(loopPlot)
								# isPeak
								elif loopPlot.isPeak():
										if loopPlot.getOwner() == -1:
												Peaks.append(loopPlot)
								# isLand
								else:
										iPlotOwner = loopPlot.getOwner()
										# nur ausserhalb von Cities
										if not loopPlot.isCity():

												# Forts oder Handelsposten
												if iPlotImprovement in L.LImprFortShort:

														# Init
														iOwner = -1
														iOwner = int(CvUtil.getScriptData(loopPlot, ["p", "t"], loopPlot.getOwner()))
														# Handelsposten entfernen, wenn der Plot in einem fremden Kulturkreis liegt
														if iPlotImprovement == eHandelsposten:
																if iOwner != iPlotOwner and iPlotOwner != -1:
																		loopPlot.setImprovementType(-1)
																		CvUtil.removeScriptData(loopPlot, "p")
																		if gc.getPlayer(iOwner).isHuman():
																				szText = CyTranslator().getText("TXT_KEY_INFO_CLOSED_TRADEPOST", ("",))
																				CyInterface().addMessage(iOwner, True, 15, szText, "AS2D_UNIT_BUILD_UNIT", 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), loopPlot.getX(), loopPlot.getY(), True, True)
																# Kultur setzen
																elif iPlotOwner == -1:
																		loopPlot.changeCulture(iOwner, 1, True)
																		loopPlot.setOwner(iOwner)
																		continue
														# Kultur bei Forts
														# else:
														#  doCheckFortCulture(loopPlot)

												# Check nur alle x Runden (Tier-Spawn)
												# + Bonus movement
												if iGameTurn % 2 == 0:

														# Lion
														if loopPlot.getBonusType(-1) == bonus_lion and iPlotImprovement == -1:
																if loopPlot.getNumUnits() == 0:
																		if CvUtil.myRandom(33, "lion") == 1:
																				pBarbPlayer.initUnit(eLion, x, y, UnitAITypes.UNITAI_ANIMAL, DirectionTypes.DIRECTION_SOUTH)
																				# ***TEST***
																				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "Barb. Atlasloewe erschaffen", None, 2, None, ColorTypes(10), 0, 0, False, False)
																				continue
														# Bear of Wolf
														elif loopPlot.getBonusType(-1) == bonus_deer and iPlotImprovement == -1:
																if loopPlot.getNumUnits() == 0:
																		iRand = CvUtil.myRandom(20, "bear or wolf")
																		if iRand == 0:
																				pBarbPlayer.initUnit(eWolf, x, y, UnitAITypes.UNITAI_ANIMAL, DirectionTypes.DIRECTION_SOUTH)
																				continue
																		elif iRand == 1:
																				pBarbPlayer.initUnit(eBear, x, y, UnitAITypes.UNITAI_ANIMAL, DirectionTypes.DIRECTION_SOUTH)
																				continue
														# Horse
														elif loopPlot.getBonusType(iPlotOwner) == bonus_horse:
																if loopPlot.getNumUnits() == 0:
																		if CvUtil.myRandom(45, "horse") == 1:
																				# Check Owner
																				iNewUnitOwner = iBarbPlayer
																				if iPlotOwner != -1 and iPlotOwner != iBarbPlayer:
																						if gc.getTeam(gc.getPlayer(iPlotOwner).getTeam()).isHasTech(eHorseTech):
																								iNewUnitOwner = iPlotOwner
																						elif gc.getPlayer(iPlotOwner).isHuman():
																								CyInterface().addMessage(iPlotOwner, True, 10, CyTranslator().getText("TXT_KEY_INFO_DOM_HORSE", ("",)), None, 2, gc.getBonusInfo(bonus_horse).getButton(), ColorTypes(13), x, y, True, True)
																				# Add Unit
																				gc.getPlayer(iNewUnitOwner).initUnit(eHorse, x, y, UnitAITypes.UNITAI_ANIMAL, DirectionTypes.DIRECTION_SOUTH)
																				continue
														# Camel
														elif loopPlot.getBonusType(iPlotOwner) == bonus_camel:
																if loopPlot.getNumUnits() == 0:
																		if CvUtil.myRandom(40, "camel") == 1:
																				# Check Owner
																				iNewUnitOwner = iBarbPlayer
																				if iPlotOwner != -1:
																						if gc.getTeam(gc.getPlayer(iPlotOwner).getTeam()).isHasTech(eCamelTech):
																								iNewUnitOwner = iPlotOwner
																						elif gc.getPlayer(iPlotOwner).isHuman():
																								CyInterface().addMessage(iPlotOwner, True, 10, CyTranslator().getText("TXT_KEY_INFO_DOM_CAMEL", ("",)), None, 2, gc.getBonusInfo(bonus_camel).getButton(), ColorTypes(13), x, y, True, True)
																				# Add Unit
																				gc.getPlayer(iNewUnitOwner).initUnit(eCamel, x, y, UnitAITypes.UNITAI_ANIMAL, DirectionTypes.DIRECTION_SOUTH)
																				continue
														# Elefant (ab Eisenzeit)
														elif loopPlot.getBonusType(iPlotOwner) == bonus_ivory and pBarbPlayer.getCurrentEra() >= 2:
																if loopPlot.getNumUnits() == 0:
																		if CvUtil.myRandom(50, "ele") == 1:
																				# Check Owner
																				iNewUnitOwner = iBarbPlayer
																				if iPlotOwner != -1:
																						if gc.getTeam(gc.getPlayer(iPlotOwner).getTeam()).isHasTech(eElefantTech):
																								iNewUnitOwner = iPlotOwner
																						elif gc.getPlayer(iPlotOwner).isHuman():
																								CyInterface().addMessage(iPlotOwner, True, 10, CyTranslator().getText("TXT_KEY_INFO_DOM_ELEFANT", ("",)), None, 2, gc.getBonusInfo(bonus_ivory).getButton(), ColorTypes(13), x, y, True, True)
																				# Add Unit
																				gc.getPlayer(iNewUnitOwner).initUnit(eElefant, x, y, UnitAITypes.UNITAI_ANIMAL, DirectionTypes.DIRECTION_SOUTH)
																				continue
														# Esel
														elif loopPlot.getBonusType(iPlotOwner) == bonus_esel:
																if loopPlot.getNumUnits() == 0:
																		if CvUtil.myRandom(45, "esel") == 1:
																				# Check Owner
																				iNewUnitOwner = iBarbPlayer
																				if iPlotOwner != -1 and iPlotOwner != iBarbPlayer:
																						if gc.getTeam(gc.getPlayer(iPlotOwner).getTeam()).isHasTech(eEselTech):
																								iNewUnitOwner = iPlotOwner
																				# Add Unit
																				gc.getPlayer(iNewUnitOwner).initUnit(eEsel, x, y, UnitAITypes.UNITAI_ANIMAL, DirectionTypes.DIRECTION_SOUTH)
																				continue


														# Movement of wild animal bonus resources (nur auf neutralem Terrain)
														if bMovingBonus and loopPlot.getBonusType(-1) in L.LMovingBonus and loopPlot.getNumUnits() == 0 and iPlotImprovement == -1 and iPlotOwner == -1:
																MovingBonus.append(loopPlot)


												# Barbarenforts/festungen (erzeugt barbarische Einheiten alle x Runden)
												if iPlotImprovement == impBarbFort:
														iBarbForts += 1
														# if iPlotOwner == -1 or iPlotOwner == iBarbPlayer:
														if loopPlot.getNumUnits() == 0:
																# Verteidiger setzen
																PAE_Barbaren.setFortDefence(loopPlot)
														elif loopPlot.getNumUnits() > 5:
																iNum = loopPlot.getNumUnits() - 5
																for k in range(iNum):
																		loopPlot.getUnit(k).kill(True, -1)

														if bRageBarbs:
																iTurns = 6
														else:
																iTurns = 8
														if pBarbPlayer.getCurrentEra() > 0:
																iTurns = iTurns / 2

														if gc.getGame().getGameTurn() % iTurns == 0:
																#iAnzUnits = PAE_Barbaren.countNearbyUnits(loopPlot, 2, iBarbPlayer)
																#if iAnzUnits < 6:
																# Einheiten) setzen
																PAE_Barbaren.createBarbUnit(loopPlot)
														continue
												# Baerenhoehle
												elif iPlotImprovement == impCave:
														iCaves += 1
														# if loopPlot.getNumUnits() <= 1:
														if CvUtil.myRandom(15, "cave bear") == 1:
																bCheck = PAE_Barbaren.checkNearbyUnits(loopPlot, 3)  # (Plot, Radius)
																if not bCheck:
																		setUnitIntoCave(loopPlot)
																continue
												# Goody huts
												elif iPlotImprovement == impGoody:
														iGoodyHuts += 1

												# Keine Seuche in Deserts
												if iPlotTerrain == iTerrDesert:
														if iPlotFeature == iFeatSeuche:
																loopPlot.setFeatureType(-1, 0)

												# leere Plots zwischenspeichern
												if iGameTurn > 150 and iGameTurn % 10 == 0:
														if iPlotOwner == -1:
																if loopPlot.getNumUnits() == 0 and not loopPlot.isActiveVisible(0):

																		# Empty Plots for Animals and Barbs
																		if iPlotTerrain == iTerrDesert:
																				Desert.append(loopPlot)
																		elif iPlotTerrain == iTerrTundra:
																				Tundra.append(loopPlot)
																		elif iPlotFeature == iFeatDenseForest:
																				DenseForest.append(loopPlot)
																		elif iPlotFeature == iFeatJungle:
																				Jungle.append(loopPlot)
																		elif iPlotFeature == iFeatForest:
																				Forest.append(loopPlot)
																		elif iPlotTerrain == iTerrPlains:
																				Plains.append(loopPlot)
																		if loopPlot.isHills():
																				Hills.append(loopPlot)
										# end if - not isCity
								# end if not isPeak

		# Plots verarbeiten --------------------------------

		# Flotsam (if activated)
		if bFlotsam and bFlot and bGoodyHuts:
				if Ocean:
						if CvUtil.myRandom(33, "setFlotsam") == 1:
								iUnit = gc.getInfoTypeForString("UNIT_TREIBGUT")
								iNum = gc.getMap().getWorldSize() + 1
								for i in range(iNum):
										CvUtil.spawnUnit(iUnit, Ocean[CvUtil.myRandom(len(Ocean), "spawnFlotsam")], pBarbPlayer)

		# Tiere setzen --------------------
		if len(Desert):
				iChance = CvUtil.myRandom(33, "setAnimals4Desert")
				if iChance == 1: setAnimals(gc.getInfoTypeForString("UNIT_LION"), Desert)
				elif iChance == 2: setAnimals(gc.getInfoTypeForString("UNIT_LIONESS"), Desert)
				elif iChance == 3: setAnimals(gc.getInfoTypeForString("UNIT_HYENA"), Desert)
		if len(DenseForest):
				iChance = CvUtil.myRandom(33, "setAnimals4DenseForest")
				if iChance == 1: setAnimals(gc.getInfoTypeForString("UNIT_BEAR"), DenseForest)
				elif iChance == 2: setAnimals(gc.getInfoTypeForString("UNIT_BEAR2"), DenseForest)
				elif iChance == 3: setAnimals(gc.getInfoTypeForString("UNIT_UR"), DenseForest)
		if len(Tundra):
				iChance = CvUtil.myRandom(33, "setAnimals4Tundra")
				if iChance == 1: setAnimals(gc.getInfoTypeForString("UNIT_WOLF"), Tundra)
				elif iChance == 2: setAnimals(gc.getInfoTypeForString("UNIT_WOLF2"), Tundra)
				elif iChance == 3: setAnimals(gc.getInfoTypeForString("UNIT_HORSE"), Tundra)
		if len(Jungle):
				iChance = CvUtil.myRandom(33, "setAnimals4Jungle")
				if iChance == 1: setAnimals(gc.getInfoTypeForString("UNIT_PANTHER"), Jungle)
				elif iChance == 2: setAnimals(gc.getInfoTypeForString("UNIT_TIGER"), Jungle)
				elif iChance == 3: setAnimals(gc.getInfoTypeForString("UNIT_LEOPARD"), Jungle)
		if len(Forest):
				iChance = CvUtil.myRandom(33, "setAnimals4Forest")
				if iChance == 1: setAnimals(gc.getInfoTypeForString("UNIT_WOLF"), Forest)
				elif iChance == 2: setAnimals(gc.getInfoTypeForString("UNIT_WOLF2"), Forest)
				elif iChance == 3: setAnimals(gc.getInfoTypeForString("UNIT_BOAR"), Forest)
				elif iChance == 4: setAnimals(gc.getInfoTypeForString("UNIT_DEER"), Forest)
				elif iChance == 5: setAnimals(gc.getInfoTypeForString("UNIT_ESEL"), Forest)
		# if len(Plains):
		#	if CvUtil.myRandom(33, "setAnimals4Plains") == 1:
		#		setAnimals(gc.getInfoTypeForString("UNIT_LEOPARD"),Plains)
		#		#setAnimals(gc.getInfoTypeForString("UNIT_HORSE"),Plains)
		if len(Peaks):
				if CvUtil.myRandom(50, "setAnimals4Peaks") == 1:
						setAnimals(gc.getInfoTypeForString("UNIT_BERGZIEGE"),Peaks)

		# Goody huts setzen
		if bGoodyHuts:
				nPlots = Jungle + Forest + Plains
				if len(nPlots):
						if CvUtil.myRandom(33, "setGoodyHuts") == 1:
								setGoodies(impGoody, iGoodyHuts, nPlots)

		# Barbaren Forts setzen
		if bBarbForts:
				nPlots = Hills
				if nPlots:
						if CvUtil.myRandom(33, "setBarbForts") == 1:
								setGoodies(impBarbFort, iBarbForts, nPlots)

		# Caves setzen
		nPlots = Jungle + Forest + DenseForest + Desert + Tundra
		if nPlots:
				if CvUtil.myRandom(33, "setCaves") == 1:
						setGoodies(impCave, iCaves, nPlots)

		# move Desertstorm / Sandsturm bewegen
		if lDesertStorm:
				doMoveDesertStorm(lDesertStorm)

		# unkultivierte Bonusressourcen bewegen
		if bMovingBonus and len(MovingBonus):
				doMoveBonus(MovingBonus)

		# Olympiade / Olympic Games / Panhellenic Games
		doOlympicGames()

		# Besonderes Thing
		doThing()


# Tiere erstellen
def setAnimals(eAnimal, plots):
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		eUnitClass = gc.getUnitInfo(eAnimal).getUnitClassType()
		iBarbUnits = pBarbPlayer.getUnitClassCount(eUnitClass)

		#  0 = WORLDSIZE_DUEL
		#  1 = WORLDSIZE_TINY
		#  2 = WORLDSIZE_SMALL
		#  3 = WORLDSIZE_STANDARD
		#  4 = WORLDSIZE_LARGE
		#  5 = WORLDSIZE_HUGE
		iMapSize = gc.getMap().getWorldSize() * 2
		iAnimals = iMapSize + 1 - iBarbUnits

		# Ausnahmen
		if eAnimal == gc.getInfoTypeForString("UNIT_UR"):
				iAnimals = 2 - iBarbUnits  # maximal 2
		if iAnimals <= 0:
				return

		# Tiere setzen
		i = 0
		while i < iAnimals:
				iRand = CvUtil.myRandom(len(plots), "spawnAnimalOnPlot")
				CvUtil.spawnUnit(eAnimal, plots[iRand], pBarbPlayer)
				# plots.remove(plots[iRand])
				i += 1

##### PAE V: Goody-Doerfer erstellen (goody-huts / GoodyHuts / Goodies / Villages) ####
# PAE VI: Barbarenforts und Caves erstellen
def setGoodies(eImprovement, eNum, plots):
		impBarbFort = gc.getInfoTypeForString("IMPROVEMENT_BARBARENFORT")
		impCave = gc.getInfoTypeForString("IMPROVEMENT_CAVE")
		impGoody = gc.getInfoTypeForString("IMPROVEMENT_GOODY_HUT")

		lGoodies = [impBarbFort, impCave, impGoody]

		#  0 = WORLDSIZE_DUEL
		#  1 = WORLDSIZE_TINY
		#  2 = WORLDSIZE_SMALL
		#  3 = WORLDSIZE_STANDARD
		#  4 = WORLDSIZE_LARGE
		#  5 = WORLDSIZE_HUGE
		iMapSize = gc.getMap().getWorldSize() * 3
		iAnz = iMapSize + 1 - eNum
		if iAnz <= 0:
				return

		i = 0
		while i < iAnz:
				bIgnore = False

				if len(plots) <= 0:
						return

				iRand = CvUtil.myRandom(len(plots), "setBarbFortsOrCavesOrGoodyHuts")
				plot = plots[iRand]

				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("setGoodies",len(plots))), None, 2, None, ColorTypes(11), 0, 0, False, False)

				# Umkreis checken
				iRange = 3
				for x in range(-iRange, iRange+1):
						for y in range(-iRange, iRange+1):
								loopPlot = plotXY(plot.getX(), plot.getY(), x, y)
								if loopPlot is not None and not loopPlot.isNone():
										if loopPlot.getImprovementType() in lGoodies or loopPlot.getOwner() != -1:
												bIgnore = True
												# Umkreis des gefundenen Plots aus der Plotliste entfernen
												for x2 in range(-iRange, iRange+1):
														for y2 in range(-iRange, iRange+1):
																loopPlot = plotXY(plot.getX(), plot.getY(), x2, y2)
																if loopPlot is not None and not loopPlot.isNone():
																		if loopPlot in plots:
																				plots.remove(loopPlot)
												break
						if bIgnore:
								break

				i += 1

				if bIgnore:
						continue

				# Improvement setzen
				plot.setImprovementType(eImprovement)

				# Einheit in die Festung setzen
				if eImprovement == impBarbFort:
						PAE_Barbaren.setFortDefence(plot)
				# Einheit in die Cave setzen
				elif eImprovement == impCave:
						setUnitIntoCave(plot)

				# Alle Plots im Umkreis von 4 Feldern aus der Liste entfernen
				iRange = 4
				for x in range(-iRange, iRange+1):
						for y in range(-iRange, iRange+1):
								loopPlot = plotXY(plot.getX(), plot.getY(), x, y)
								if loopPlot is not None and not loopPlot.isNone():
										if loopPlot in plots:
												plots.remove(loopPlot)
		return


def setUnitIntoCave(pPlot):
		lUnits = []
		if pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_FOREST"):
				lUnits.append(gc.getInfoTypeForString("UNIT_BEAR"))
				lUnits.append(gc.getInfoTypeForString("UNIT_WOLF"))
		elif pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_DICHTERWALD"):
				lUnits.append(gc.getInfoTypeForString("UNIT_BEAR"))
				lUnits.append(gc.getInfoTypeForString("UNIT_WOLF"))
				lUnits.append(gc.getInfoTypeForString("UNIT_UR"))
		elif pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_JUNGLE"):
				lUnits.append(gc.getInfoTypeForString("UNIT_PANTHER"))
				lUnits.append(gc.getInfoTypeForString("UNIT_LEOPARD"))
				lUnits.append(gc.getInfoTypeForString("UNIT_TIGER"))
		elif pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_DESERT"):
				lUnits.append(gc.getInfoTypeForString("UNIT_LION"))
				lUnits.append(gc.getInfoTypeForString("UNIT_HYENA"))
		elif pPlot.getTerrainType() == gc.getInfoTypeForString("TERRAIN_TUNDRA"):
				lUnits.append(gc.getInfoTypeForString("UNIT_WOLF"))

		if len(lUnits):
				iRand = CvUtil.myRandom(len(lUnits), "setUnitIntoCave")
				gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(lUnits[iRand], pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ANIMAL, DirectionTypes.DIRECTION_SOUTH)

# --------- Strandgut -----------
# -- PAE V: Treibgut -> Strandgut
def doStrandgut():
		iBarbPlayer = gc.getBARBARIAN_PLAYER()
		pBarbPlayer = gc.getPlayer(iBarbPlayer)
		iTreibgut = gc.getInfoTypeForString("UNIT_TREIBGUT")
		iStrandgut = gc.getInfoTypeForString("UNIT_STRANDGUT")
		iGoldkarren = gc.getInfoTypeForString("UNIT_GOLDKARREN")
		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
		eCoast = gc.getInfoTypeForString("TERRAIN_COAST")

		lUnits = PyPlayer(iBarbPlayer).getUnitsOfType(iTreibgut)
		# CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("Test",len(lUnits))), None, 2, None, ColorTypes(11), 0, 0, False, False)
		for loopUnit in lUnits:
				pPlot = loopUnit.plot()
				if pPlot.getTerrainType() == eCoast:
						lPlots = []
						iX = pPlot.getX()
						iY = pPlot.getY()
						# iRange = 1
						for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
								loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
								if loopPlot is not None and not loopPlot.isNone():
										if not loopPlot.isWater():
												if not loopPlot.isPeak() and not loopPlot.isUnit() and loopPlot.getFeatureType() != iDarkIce:
														lPlots.append(loopPlot)
						if lPlots:
								pPlot = lPlots[CvUtil.myRandom(len(lPlots), "strandgut")]
								# Create Strandgut
								CvUtil.spawnUnit(iStrandgut, pPlot, pBarbPlayer)
								iPlotOwner = pPlot.getOwner()
								if iPlotOwner != -1 and gc.getPlayer(iPlotOwner).isHuman():
										CyInterface().addMessage(iPlotOwner, True, 15, CyTranslator().getText("TXT_KEY_TREIB2STRANDGUT", ()), None, 2,
																						 "Art/Interface/Buttons/Units/button_unit_strandgut.dds", ColorTypes(11), pPlot.getX(), pPlot.getY(), True, True)
								# Disband Treibgut
								# loopUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
								loopUnit.kill(True, -1)  # RAMK_CTD
				elif pPlot.isCity():
						# Create Goldkarren
						CvUtil.spawnUnit(iGoldkarren, pPlot, pBarbPlayer)
						# Disband Treibgut
						# CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 15, CyTranslator().getText("disbandTreibgutCity", ()), None, 2, None, ColorTypes(11), pPlot.getX(), pPlot.getY(), False, False)
						# loopUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
						loopUnit.kill(True, -1)  # RAMK_CTD
						# --------- Strandgut -----------

# New Fair wind-Feature (Seewind) together with Elwood (ideas) and the TAC-Team (diagonal arrows)
def doSeewind():
		terr_ocean = gc.getInfoTypeForString("TERRAIN_OCEAN")
		terr_ocean2 = gc.getInfoTypeForString("TERRAIN_DEEP_OCEAN")
		feat_ice = gc.getInfoTypeForString("FEATURE_ICE")

		iNumDirection = 8
		iWindplots = 6  # amount of wind arrows (plots) per wind
		OceanPlots = []
		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()
		# get all ocean plots
		for i in range(iMapW):
				for j in range(iMapH):
						loopPlot = gc.getMap().plot(i, j)
						if loopPlot is not None and not loopPlot.isNone():
								if loopPlot.getTerrainType() == terr_ocean or loopPlot.getTerrainType() == terr_ocean2:
										if loopPlot.getFeatureType() != feat_ice and loopPlot.getFeatureType() != iDarkIce:
												OceanPlots.append(loopPlot)

		if OceanPlots:
				#  0 = WORLDSIZE_DUEL
				#  1 = WORLDSIZE_TINY
				#  2 = WORLDSIZE_SMALL
				#  3 = WORLDSIZE_STANDARD
				#  4 = WORLDSIZE_LARGE
				#  5 = WORLDSIZE_HUGE
				iMaxEffects = (gc.getMap().getWorldSize() + 1) * 2
				for i in range(iMaxEffects):
						# get first ocean plot
						iRand = CvUtil.myRandom(len(OceanPlots), "doSeewind1")
						loopPlot = OceanPlots[iRand]
						# First direction
						iDirection = CvUtil.myRandom(iNumDirection, "doSeewind2")

						# Start Windplots
						for j in range(iWindplots):
								if loopPlot and not loopPlot.isNone():
										if loopPlot.getFeatureType() == iDarkIce:
												continue
										if loopPlot.getFeatureType() != feat_ice and (loopPlot.getTerrainType() == terr_ocean or loopPlot.getTerrainType() == terr_ocean2):
												# Im Umkreis von 5 soll kein weiteres Windfeature sein
												bSet = True
												for iX in range(5):
														for iY in range(5):
																pPlot2 = gc.getMap().plot(loopPlot.getX() - 2 + iX, loopPlot.getY() - 2 + iY)
																if pPlot2.getFeatureType() in L.LSeewind:
																		bSet = False
																		break
														if not bSet:
																break

												if bSet:
														loopPlot.setFeatureType(L.LSeewind[iDirection], 0)
														iDirection = (iDirection+CvUtil.myRandom(3, "doSeewind3")-1) % iNumDirection
														loopPlot = plotDirection(loopPlot.getX(), loopPlot.getY(), DirectionTypes(iDirection))
												else:
														break

# ++++++++++++++++++ Historische Texte ++++++++++++++++++
def doHistory():
		lNumHistoryTexts = {
		-3480: 4,
		-3000: 5,
		-2680: 4,
		-2000: 6,
		-1680: 5,
		-1480: 7,
		-1280: 5,
		-1200: 6,
		-1000: 5,
		-800: 6,
		-750: 3,
		-700: 6,
		-615: 5,
		-580: 5,
		-540: 4,
		-510: 5,
		-490: 5,
		-450: 4,
		-400: 5,
		-350: 7,
		-330: 4,
		-260: 3,
		-230: 5,
		-215: 4,
		-200: 4,
		-150: 5,
		-120: 2,
		-100: 2,
		-70: 3,
		-50: 2,
		-30: 2,
		-20: 2,
		-10: 3,
		10: 3,
		60: 4,
		90: 3,
		130: 3,
		210: 3,
		250: 2,
		280: 2,
		370: 2,
		400: 2,
		440: 3,
		}
		iGameYear = gc.getGame().getGameTurnYear()
		# txts = 0
		if iGameYear in lNumHistoryTexts:
				txts = lNumHistoryTexts[iGameYear]
		# if txts > 0:
				iRand = CvUtil.myRandom(txts, "doHistory")

				# iRand 0 bedeutet keinen Text anzeigen. Bei mehr als 2 Texte immer einen einblenden
				if txts > 2:
						iRand += 1

				if iRand > 0:
						text = "TXT_KEY_HISTORY_"
						if iGameYear < 0:
								text = text + str(iGameYear * (-1)) + "BC_" + str(iRand)
						else:
								text = text + str(iGameYear) + "AD_" + str(iRand)

						text = CyTranslator().getText("TXT_KEY_HISTORY", ("",)) + " " + CyTranslator().getText(text, ("",))
						CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 15, text, None, 2, None, ColorTypes(14), 0, 0, False, False)


def doRevoltAnarchy(iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iRand = CvUtil.myRandom(3, "getAnarchyTurns")
		if iRand == 1:
				iBuilding = gc.getInfoTypeForString("BUILDING_PLAGUE")
				iNumCities = pPlayer.getNumCities()
				if iNumCities == 0:
						return
				iCityPlague = 0
				iCityRevolt = 0
				(loopCity, pIter) = pPlayer.firstCity(False)
				while loopCity:
						if not loopCity.isNone() and loopCity.getOwner() == iPlayer:  # only valid cities
								if loopCity.isHasBuilding(iBuilding):
										iCityPlague += 1
								if loopCity.getOccupationTimer() > 1:  # Flunky: changed 0->1, because the counter is not yet updated from the previous round.
										iCityRevolt += 1
						(loopCity, pIter) = pPlayer.nextCity(pIter, False)

				if iCityRevolt > 1 and iNumCities <= iCityRevolt * 2:
						pPlayer.changeAnarchyTurns(3)
						if pPlayer.isHuman():
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_PLAYER_ANARCHY_FROM_REVOLTS", ("", )))
								popupInfo.addPopup(iPlayer)

				elif iNumCities <= iCityPlague * 2:
						pPlayer.changeAnarchyTurns(2)
						if pPlayer.isHuman():
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_PLAYER_ANARCHY_FROM_PLAGUE", ("", )))
								popupInfo.addPopup(iPlayer)

# +++++ MAP Reveal to black fog - Kriegsnebel - Fog of War (FoW) - Karte schwarz zurueckfaerben
# AI auch, aber nur alle iPlayer-Runden
# AI wird wieder reingenommen -> wenn nur alle x Runden wahrscheinlich weniger Einheitenbewegung! -> no MAFs
def doFogOfWar(iPlayer, iGameTurn):
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()
		pTeam = gc.getTeam(iTeam)
		# Human oder KI alle x Runden, aber unterschiedliche Civs pro Runde fuer optimale Rundenzeiten
		if pPlayer.isHuman() or (iGameTurn % 20 == iPlayer % 20 and pTeam.isMapTrading()):
				bDontGoBlackAnymore = False
				bShowCoasts = False
				bShowPeaksAndRivers = False
				if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KARTOGRAPHIE2")):  # Strassenkarten
						bDontGoBlackAnymore = True
				elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_KARTEN")):  # Karte zeichnen
						bShowCoasts = True
						bShowPeaksAndRivers = True
				elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_KARTOGRAPHIE")):  # Kartographie: Erste Karten
						bShowCoasts = True

				if not bDontGoBlackAnymore:
						iRange = CyMap().numPlots()
						for iI in range(iRange):
								pPlot = CyMap().plotByIndex(iI)
								if not pPlot.isVisible(iTeam, 0):
										bGoBlack = True
										# fully black or standard fog of war
										if pPlot.isCity():
												pCity = pPlot.getPlotCity()
												if pCity.isCapital():
														bGoBlack = False
												elif pCity.getNumWorldWonders() > 0:
														bGoBlack = False
										# Holy Mountain Quest
										if bGoBlack:
												if CvUtil.getScriptData(pPlot, ["H", "t"]) == "X":
														bGoBlack = False
										# Improvements (to normal fog of war)
										# if bGoBlack:
										#  if pPlot.getImprovementType() == improv1 or pPlot.getImprovementType() == improv2: bGoBlack = False
										# 50% Chance Verdunkelung
										if bGoBlack:
												if CvUtil.myRandom(2, "bGoBlack") == 0:
														bGoBlack = False
										# Black fog
										if bGoBlack:
												if pPlot.isRevealed(iTeam, 0):
														# River and coast (land only)
														#if pPlot.isRevealed (iTeam, 0) and not (pPlot.isRiverSide() or pPlot.isCoastalLand()): pPlot.setRevealed (iTeam,0,0,-1)
														# River and coast (land and water)
														#if pPlot.isRevealed (iTeam, 0) and not (pPlot.isRiverSide() or pPlot.isCoastalLand() or (pPlot.isAdjacentToLand() and pPlot.isWater())): pPlot.setRevealed (iTeam,0,0,-1)
														if bShowCoasts:
																if pPlot.isCoastalLand() or pPlot.isAdjacentToLand() and pPlot.isWater():
																		continue
														if bShowPeaksAndRivers:
																if pPlot.isRiverSide() or pPlot.isPeak():
																		continue
														pPlot.setRevealed(iTeam, 0, 0, -1)


def doMoveGrasshoppers(pPlot):

		# Am Plot bleiben 2:3
		if CvUtil.myRandom(3, "doMoveGrasshoppers") > 0:
				return

		iFeatGrasshopper = gc.getInfoTypeForString("FEATURE_GRASSHOPPER")
		lPlots = []
		# Umkreis checken
		iRange = 1
		for x in range(-iRange, iRange+1):
				for y in range(-iRange, iRange+1):
						loopPlot = plotXY(pPlot.getX(), pPlot.getY(), x, y)
						if loopPlot is not None and not loopPlot.isNone():
								if loopPlot.getFeatureType() == -1:
										if not loopPlot.isWater() and not loopPlot.isPeak():
												lPlots.append(loopPlot)

		if len(lPlots):
				iRand = CvUtil.myRandom(len(lPlots), "doMoveGrasshoppers")
				# Heuschrecken vom alten Plot entfernen
				pPlot.setFeatureType(-1, 0)
				# Heuschrecken auf dem neuen Plot erzeugen
				lPlots[iRand].setFeatureType(iFeatGrasshopper, 0)
				# Farmen auf dem neuen Plot vernichten (ausgenommen Weiden)
				if lPlots[iRand].getImprovementType() != gc.getInfoTypeForString("IMPROVEMENT_PASTURE") \
								and lPlots[iRand].getImprovementType() in L.LFarms:
						lPlots[iRand].setImprovementType(-1)


def doMoveDesertStorm(lDesertStorm):
		iFeatDesertstorm = gc.getInfoTypeForString("FEATURE_FALLOUT")
		iTerrainDesert = gc.getInfoTypeForString("TERRAIN_DESERT")
		#iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		lImprovements = [
				gc.getInfoTypeForString("IMPROVEMENT_FORT"),
				gc.getInfoTypeForString("IMPROVEMENT_FORT2"),
				gc.getInfoTypeForString("IMPROVEMENT_TURM2"),
				gc.getInfoTypeForString("IMPROVEMENT_MINE")
		]

		# Wegen Wind von West nach Ost, die Reihenfolge der Plot-Liste umkehren
		lDesertStorm.reverse()

		for p in lDesertStorm:
				loopPlot = plotXY(p.getX(), p.getY(), 2, 0)  # 2-Plot-Schritte nach Osten
				if loopPlot is not None and not loopPlot.isNone():
						if loopPlot.getTerrainType() == iTerrainDesert:
								if loopPlot.getFeatureType() == -1:
										if not loopPlot.isPeak():
												bMeldung = False
												# Entferne Modernisierung 1:3
												if loopPlot.getImprovementType() not in lImprovements:
														if CvUtil.myRandom(3, "doDestroyImprovementDueToDesertStorm") == 1:
																loopPlot.setImprovementType(-1)
																bMeldung = True
												# Entferne Strasse 1:3
												if loopPlot.getRouteType() == 0 and not loopPlot.isCity():
														if CvUtil.myRandom(3, "doDestroyRouteDueToDesertStorm") == 1:
																loopPlot.setRouteType(-1)
																bMeldung = True
												# Sandsturm setzen
												loopPlot.setFeatureType(iFeatDesertstorm, 0)
												# Meldung an den Spieler
												if bMeldung and loopPlot.getOwner() != -1:
														if gc.getPlayer(loopPlot.getOwner()).isHuman():
																CyInterface().addMessage(gc.getPlayer(loopPlot.getOwner()).getID(), True, 12, CyTranslator().getText("TXT_KEY_DISASTER_DESERTSTORM", ("", )),
																												 None, 2, gc.getFeatureInfo(iFeatDesertstorm).getButton(), ColorTypes(7), loopPlot.getX(), loopPlot.getY(), True, True)
				# Sandsturm entfernen (vorheriger Plot)
				p.setFeatureType(-1, 0)

# Tiefsee / Deep Ocean setzen
def doPlaceDeepOcean():
		iNumMapPlots = gc.getMap().numPlots()
		# iDirectionTypes = DirectionTypes.NUM_DIRECTION_TYPES
		iCoast = gc.getInfoTypeForString("TERRAIN_COAST")
		iOcean = gc.getInfoTypeForString("TERRAIN_OCEAN")
		iDeepOcean = gc.getInfoTypeForString("TERRAIN_DEEP_OCEAN")
		iRange = 2

		for i in range(iNumMapPlots):
				pPlot = gc.getMap().plotByIndex(i)
				if not pPlot.isNone() and pPlot.getTerrainType() == iOcean:
						iX = pPlot.getX()
						iY = pPlot.getY()
						bSet = True
						for x in range(-iRange, iRange+1):
								for y in range(-iRange, iRange+1):
										pLoopPlot = plotXY(iX, iY, x, y)
										if pLoopPlot is None or pLoopPlot.isNone():
												continue
										if pLoopPlot.getTerrainType() == iCoast:
												bSet = False
												break
								if not bSet:
										break

						if bSet:
								# VOID setTerrainType (TerrainType eNewValue, BOOL bRecalculate, BOOL bRebuildGraphics)
								if (iX == 3 or iX % 6 == 0) and (iY == 3 or iY % 6 == 0):
										bRebuildGraphics = True
								else:
										bRebuildGraphics = False
								pPlot.setTerrainType(iDeepOcean, False, bRebuildGraphics)

# Panhellenische Spiele / Olympiade
def doOlympicGames():
		# wurde das Projekt erstellt?
		if gc.getGame().getProjectCreatedCount(gc.getInfoTypeForString("PROJECT_OLYMPIC_GAMES")) > 0:

				# alle 4 Runden
				if gc.getGame().getCalendar() == gc.getInfoTypeForString("CALENDAR_MONTHS"):
						iTurns = 48
				elif gc.getGame().getCalendar() == gc.getInfoTypeForString("CALENDAR_SEASONS"):
						iTurns = 16
				else:
						iTurns = 4

				if gc.getGame().getElapsedGameTurns() % iTurns == 1:

						# Inits
						lCities4Olympiade = []
						lHumans = []
						lPlayers = []

						iTechSchaukampf = gc.getInfoTypeForString("TECH_GLADIATOR")
						iTechImperialismus = gc.getInfoTypeForString("TECH_NATIONALISM")
						iTechPapsttum = gc.getInfoTypeForString("TECH_KONZIL2")
						iReligionGreek = gc.getInfoTypeForString("RELIGION_GREEK")
						iReligionRome = gc.getInfoTypeForString("RELIGION_ROME")

						iBuildingStadion = gc.getInfoTypeForString("BUILDING_STADION")
						iBuildingClassStadion = gc.getInfoTypeForString("BUILDINGCLASS_STADION")
						iBuildingOlympionike = gc.getInfoTypeForString("BUILDING_OLYMPIONIKE")
						iBuildingClassGymnasion = gc.getInfoTypeForString("BUILDINGCLASS_SPECIAL3")

						# Los gehts
						iNumPlayers = gc.getMAX_PLAYERS()
						for iPlayer in range(iNumPlayers):
								pPlayer = gc.getPlayer(iPlayer)
								if pPlayer is not None and not pPlayer.isNone() and pPlayer.isAlive():  # and not pPlayer.isBarbarian():

										# Hat der Spieler noch nicht Schaukampf erforscht, isser nicht dabei
										if not gc.getTeam(pPlayer.getTeam()).isHasTech(iTechSchaukampf):
												continue

										# Hat der Spieler bereits das Papsttum erforscht, is der Spass vorbei
										if gc.getTeam(pPlayer.getTeam()).isHasTech(iTechPapsttum):
												continue

										# Hat der Spieler Imperialismus erforscht?
										bAllowRomanGods = False
										if gc.getTeam(pPlayer.getTeam()).isHasTech(iTechImperialismus):
												bAllowRomanGods = True

										# Init des Spezialgebäudes Gymnasion, Gymnasium
										iBuildingGymnasion = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationBuildings(iBuildingClassGymnasion)

										# Cities
										iNumCities = pPlayer.getNumCities()
										for iCity in range(iNumCities):
												pCity = pPlayer.getCity(iCity)
												if not pCity.isNone():

														# Aktuellen Olympioniken rausschmeissen
														if pCity.isHasBuilding(iBuildingOlympionike):
																pCity.setNumRealBuilding(iBuildingOlympionike, 0)

														# Hat die Stadt die richtige Religion?
														if pCity.isHasReligion(iReligionGreek) or bAllowRomanGods and pCity.isHasReligion(iReligionRome):

																# Liste für Spielermeldungen
																if pPlayer.isHuman():
																		if iPlayer not in lHumans:
																				lHumans.append(iPlayer)

																# Liste verschiedener CIVs
																if iPlayer not in lPlayers:
																		lPlayers.append(iPlayer)

																# Stadt an den Spielen zulassen
																lCities4Olympiade.append(pCity)
																# Verbesserte Chancen:
																if pCity.isHasBuilding(iBuildingStadion):
																		lCities4Olympiade.append(pCity)
																if pCity.isHasBuilding(iBuildingGymnasion):
																		lCities4Olympiade.append(pCity)

						# Choose new Olympic Winner City
						# erst ab 2 CIVs
						if len(lPlayers) > 1:
								iRand = CvUtil.myRandom(len(lCities4Olympiade), "CityOfOlympiadWinner")
								pCity = lCities4Olympiade[iRand]

								# Olympionike in die Stadt stellen
								pCity.setNumRealBuilding(iBuildingOlympionike, 1)

								# Stadion verbessern +1 Kultur (Chance 25%)
								bStadion = False
								if pCity.isHasBuilding(iBuildingStadion):
									if CvUtil.myRandom(4, "Olympia_ChanceOfStationCulture") == 1:
										iCulture = pCity.getBuildingCommerceChange(iBuildingClassStadion, CommerceTypes.COMMERCE_CULTURE) + 1
										pCity.setBuildingCommerceChange(iBuildingClassStadion, CommerceTypes.COMMERCE_CULTURE, iCulture)
										bStadion = True

								# Goldkarren erzeugen
								CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_GOLDKARREN"), pCity.plot(), gc.getPlayer(pCity.getOwner()))
								CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_GOLDKARREN"), pCity.plot(), gc.getPlayer(pCity.getOwner()))
								# einen weiteren bei Seasons
								if iTurns >= 16:
										CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_GOLDKARREN"), pCity.plot(), gc.getPlayer(pCity.getOwner()))
										# einen weiteren bei Months (insg. 5)
										if iTurns > 16:
												CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_GOLDKARREN"), pCity.plot(), gc.getPlayer(pCity.getOwner()))

								# Chance eines beladenen Fuhrwerks
								eBonus = -1
								if CvUtil.myRandom(4, "Olympia_ChanceOfBonus") == 1:
										pNewUnit = CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_SUPPLY_FOOD"), pCity.plot(), gc.getPlayer(pCity.getOwner()))
										lBonuses = [
												gc.getInfoTypeForString("BONUS_OLIVES"),
												gc.getInfoTypeForString("BONUS_OLIVES"),
												gc.getInfoTypeForString("BONUS_OLIVES"),
												gc.getInfoTypeForString("BONUS_OLIVES"),
												gc.getInfoTypeForString("BONUS_OLIVES"),
												gc.getInfoTypeForString("BONUS_GRAPES"),
												gc.getInfoTypeForString("BONUS_GRAPES"),
												gc.getInfoTypeForString("BONUS_GRAPES"),
												gc.getInfoTypeForString("BONUS_ROGGEN"),
												gc.getInfoTypeForString("BONUS_HAFER"),
												gc.getInfoTypeForString("BONUS_GERSTE"),
												gc.getInfoTypeForString("BONUS_WHEAT"),
												gc.getInfoTypeForString("BONUS_HIRSE"),
												gc.getInfoTypeForString("BONUS_HORSE")
										]
										eBonus = CvUtil.myRandom(len(lBonuses), "Olympia_BonusType")
										eBonus = lBonuses[eBonus]
										CvUtil.addScriptData(pNewUnit, "b", eBonus)

								# Meldung an alle beteiligten Spieler
								for iPlayer in lHumans:
										xSound = None
										iColor = 14  # graublau
										bShow = False
										# Extra PopUp wenn HI der Gewinner ist
										if iPlayer == pCity.getOwner():
												xSound = "AS2D_WELOVEKING"
												iColor = 10  # cyan
												bShow = True
												popupInfo = CyPopupInfo()
												popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
												sText = CyTranslator().getText("TXT_KEY_INFO_OLYMPIC_GAMES_WINNER", (pCity.getName(), gc.getPlayer(iPlayer).getCivilizationShortDescription(0)))
												popupInfo.setText(sText)
												popupInfo.addPopup(iPlayer)

										# Ingame Text
										CyInterface().addMessage(iPlayer, True, 15, CyTranslator().getText("TXT_KEY_INFO_OLYMPIC_GAMES_WINNER", (pCity.getName(), gc.getPlayer(pCity.getOwner()).getCivilizationShortDescription(0))),
																		xSound, 2, "Art/Interface/Buttons/Buildings/button_building_olympionike.dds", ColorTypes(iColor), pCity.plot().getX(), pCity.plot().getY(), bShow, bShow)

										# Meldung für den extra Bonus
										if bShow:
											if bStadion:
												CyInterface().addMessage(iPlayer, True, 15, CyTranslator().getText("TXT_KEY_INFO_OLYMPIC_GAMES_WINNER_STADION", ()),
																				xSound, 2, "Art/Interface/Buttons/Buildings/button_building_olympionike.dds", ColorTypes(iColor), pCity.plot().getX(), pCity.plot().getY(), False, False)
											if eBonus != -1:
												CyInterface().addMessage(iPlayer, True, 15, CyTranslator().getText("TXT_KEY_INFO_OLYMPIC_GAMES_WINNER_BONUS", (gc.getBonusInfo(eBonus).getDescription(),"")),
																				xSound, 2, "Art/Interface/Buttons/Buildings/button_building_olympionike.dds", ColorTypes(iColor), pCity.plot().getX(), pCity.plot().getY(), False, False)
# -- Olympiade Ende --

# Besonderes Thing
def doThing():

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("doThing",gc.getGame().countKnownTechNumTeams(gc.getInfoTypeForString("TECH_CODE_OF_LAWS")))), None, 2, None, ColorTypes(10), 0, 0, False, False)

		# kann es Things geben?
		iTechRequired = gc.getInfoTypeForString("TECH_DEMOCRACY")
		if gc.getGame().countKnownTechNumTeams(iTechRequired) > 0:

				# alle 3 Jahre
				if gc.getGame().getCalendar() == gc.getInfoTypeForString("CALENDAR_MONTHS"):
						iTurns = 36
				# alle 3 Jahre
				elif gc.getGame().getCalendar() == gc.getInfoTypeForString("CALENDAR_SEASONS"):
						iTurns = 12
				# alle 5 Runden
				else:
						iTurns = 5

				if gc.getGame().getElapsedGameTurns() % iTurns == 1:

						# Inits
						lCities4BonusBuilding = []
						lHumans = []
						lPlayers = []

						iTechObsolete = gc.getInfoTypeForString("TECH_DIVINE_RIGHT")
						iBuildingRequired = gc.getInfoTypeForString("BUILDING_THING")
						iBuilding = gc.getInfoTypeForString("BUILDING_THING_CITY")

						# Los gehts
						iNumPlayers = gc.getMAX_PLAYERS()
						for iPlayer in range(iNumPlayers):
								pPlayer = gc.getPlayer(iPlayer)
								if pPlayer is not None and not pPlayer.isNone() and pPlayer.isAlive():  # and not pPlayer.isBarbarian():
									if pPlayer.getCivilizationType() in L.LCivGermanen and pPlayer.getStateReligion() not in L.LMonoReligions:

										# Hat der Spieler noch nicht die richtige Tech erforscht, isser nicht dabei
										if not gc.getTeam(pPlayer.getTeam()).isHasTech(iTechRequired):
												continue

										# Hat der Spieler bereits die obsolet machende Tech erforscht, is der Spass vorbei
										if gc.getTeam(pPlayer.getTeam()).isHasTech(iTechObsolete):
												continue

										# Cities
										iNumCities = pPlayer.getNumCities()
										for iCity in range(iNumCities):
												pCity = pPlayer.getCity(iCity)
												if not pCity.isNone():

														# Aktuelles Bonusgebäude entfernen
														if pCity.isHasBuilding(iBuilding):
																pCity.setNumRealBuilding(iBuilding, 0)

														# Hat die Stadt das notwendige Gebäude?
														if pCity.isHasBuilding(iBuildingRequired):

																# Liste für Spielermeldungen
																if pPlayer.isHuman():
																		if iPlayer not in lHumans:
																				lHumans.append(iPlayer)

																# Liste verschiedener CIVs
																if iPlayer not in lPlayers:
																		lPlayers.append(iPlayer)

																# Stadt an den Spielen zulassen
																lCities4BonusBuilding.append(pCity)


						# Choose new Bonus City
						# erst ab 2 CIVs
						if len(lPlayers) > 1:
								iRand = CvUtil.myRandom(len(lCities4BonusBuilding), "CityOfThing")
								pCity = lCities4BonusBuilding[iRand]

								# Thing in die Stadt stellen
								pCity.setNumRealBuilding(iBuilding, 1)

								# Meldung an alle beteiligten Spieler
								for iPlayer in lHumans:
										xSound = None
										iColor = 14  # graublau
										bShow = False
										
										#Text
										i = 1 + CvUtil.myRandom(5, "CityOfThingText1-5")
										Text = "TXT_KEY_INFO_THING_CITY_" + str(i)
										sText = CyTranslator().getText(Text, (pCity.getName(), gc.getPlayer(pCity.getOwner()).getCivilizationShortDescription(0)))
										
										# Extra PopUp wenn HI der Gewinner ist
										if iPlayer == pCity.getOwner():
												xSound = "AS2D_WELOVEKING"
												iColor = 10  # cyan
												bShow = True
												popupInfo = CyPopupInfo()
												popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
												popupInfo.setText(sText)
												popupInfo.addPopup(iPlayer)
										# Ingame Text
										CyInterface().addMessage(iPlayer, True, 15, sText, xSound, 2, "Art/Interface/Buttons/Buildings/button_thing.dds", ColorTypes(iColor), pCity.plot().getX(), pCity.plot().getY(), bShow, bShow)
# -- Besonderes Thing Ende --

# Kultur bei Forts (Feature deaktiviert: nur Vorteil für HI)
def doCheckFortCulture(pPlot):
		iPlotData = int(CvUtil.getScriptData(pPlot, ["p", "t"], pPlot.getOwner()))

		# Wenn der Plot bereits in kulturellem Besitz ist
		if pPlot.getOwner() > -1:
				if iPlotData != -1:
						CvUtil.removeScriptData(pPlot, "p")
				return

		# Wenn der Plot keinen Besitzer hat
		else:
				iNumUnits = pPlot.getNumUnits()

				# wenns keine Einheiten gibt
				if iNumUnits == 0:
						if iPlotData != -1:
								CvUtil.removeScriptData(pPlot, "p")
						return

				# wenn das Fort jemandem gehört
				# wird gecheckt, ob der Besitzer noch eine Einheit drin stehen hat
				if iPlotData != -1:
						for i in range(iNumUnits):
								if pPlot.getUnit(i).getOwner() == iPlotData:
										pPlot.setCulture(iPlotData, 1, True)
										pPlot.setOwner(iPlotData)
										return

				# wenn das Fort niemandem gehört oder der Besitzer nicht mehr drin ist,
				# bekommts der mit den meisten Einheiten drin
				dictPlayers = {}
				for i in range(iNumUnits):
						iPlayer = pPlot.getUnit(i).getOwner()
						if iPlayer not in dictPlayers:
								dictPlayers[iPlayer] = 1
						else:
								dictPlayers[iPlayer] += 1

				if len(dictPlayers):
						iPlayer = max(dictPlayers)  # , key=dictPlayers.get)

						CvUtil.addScriptData(pPlot, "p", iPlayer)
						pPlot.setCulture(iPlayer, 1, True)
						pPlot.setOwner(iPlayer)

# -- PAE VI, Patch 15: nicht kultivierte Bonusressourcen (Tiere) sollen den Standort wechseln
def doMoveBonus(BonusPlots):
		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
		LNoForest = [
				gc.getInfoTypeForString("BONUS_ESEL"),
				gc.getInfoTypeForString("BONUS_HORSE")
		]
		LForests = [
				gc.getInfoTypeForString("FEATURE_JUNGLE"),
				gc.getInfoTypeForString("FEATURE_FOREST"),
				gc.getInfoTypeForString("FEATURE_DICHTERWALD")
		]
		eJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")

		for i in range(len(BonusPlots)):
				# Chance 1:16
				if CvUtil.myRandom(16, "chance of moving wild animal bonus") == 1:
						pPlot = BonusPlots[i]
						eBonus = pPlot.getBonusType(-1)

						lPlots = []
						iX = pPlot.getX()
						iY = pPlot.getY()
						# iRange = 1
						for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
								loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
								if loopPlot is not None and not loopPlot.isNone():
										if not loopPlot.isUnit() and loopPlot.getFeatureType() != iDarkIce and loopPlot.getBonusType(-1) == -1:
												if loopPlot.canHaveBonus(eBonus, True):
														if eBonus in LNoForest and loopPlot.getFeatureType() in LForests:
																continue
														if eBonus == gc.getInfoTypeForString("BONUS_IVORY") and loopPlot.getFeatureType() != eJungle:
																continue
														if loopPlot.getImprovementType() != -1 or loopPlot.isRoute():
																continue
														# Wasserplots nur bei Fisch
														if loopPlot.isWater():
																if eBonus == gc.getInfoTypeForString("BONUS_FISH"):
																		lPlots.append(loopPlot)
														# nur Landplots
														else:
																lPlots.append(loopPlot)

						if lPlots:
								pNewPlot = lPlots[CvUtil.myRandom(len(lPlots), "picking plot of moving wild animal bonus")]
								pNewPlot.setBonusType(eBonus)
								pPlot.setBonusType(-1)
								iRange = gc.getMAX_PLAYERS()
								for iPlayer in range(iRange):
										pPlayer = gc.getPlayer(iPlayer)
										if pPlayer is not None and not pPlayer.isNone() and pPlayer.isAlive():
												iTeam = pPlayer.getTeam()
												#if gc.getPlayer(iPlayer).isHuman() and (pPlot.isRevealed(iTeam, False) or pNewPlot.isRevealed(iTeam, False)):
												if gc.getPlayer(iPlayer).isHuman() and pPlot.getOwner() == iPlayer:
														if eBonus == gc.getInfoTypeForString("BONUS_FISH"):
																text = "TXT_KEY_INFO_MOVE_ANIMAL_BONUS_FISH"
														else:
																text = "TXT_KEY_INFO_MOVE_ANIMAL_BONUS"
														CyInterface().addMessage(iPlayer, True, 20, CyTranslator().getText(text, (gc.getBonusInfo(eBonus).getDescription(),)), None, 2,
																										 gc.getBonusInfo(eBonus).getButton(), ColorTypes(10), pNewPlot.getX(), pNewPlot.getY(), True, True)
