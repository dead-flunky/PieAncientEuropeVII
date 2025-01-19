# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
# Edited by pierre@voak.at (pie), Austria
# Implementation of miscellaneous game functions
# Some functions are only available when changed in Assets/PythonCallbackDefines.xml  (but not all!)

import CvUtil
from CvPythonExtensions import (CyGlobalContext, PlotStyles, OrderTypes,
																PlotLandscapeLayers, CyTranslator, plotXY,
																DomainTypes, ColorTypes, CyMap,
																UnitAITypes, CommandTypes, CyInterface,
																DirectionTypes, CyCity, FontSymbols,
																CyGame, CyEngine, MissionTypes, YieldTypes,
																TechTypes, CommerceTypes, BuildingTypes,
																CyGameTextMgr, WidgetTypes,
																UnitTypes, isLimitedWonderClass,
																plotDirection, MissionAITypes)
# import CvEventInterface
# import Popup as PyPopup
import PyHelpers
#import CvRiverUtil
import PAE_Trade
import PAE_Cultivation
import PAE_City
import PAE_Unit
import PAE_Sklaven
import PAE_Lists as L

# TODO remove
# DEBUG code for Python 3 linter
# unicode = str
# xrange = range

# globals
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
PyCity = PyHelpers.PyCity
PyGame = PyHelpers.PyGame


class CvGameUtils:
		"Miscellaneous game functions"

		def __init__(self):
				# PAE Veterans to Reservists feature
				# self.lUnitsNoAIReservists => PAE_Lists.LUnitsNoAIReservists
				# self.lUnitAuxiliar => PAE_Lists.LUnitAuxiliar

				# PAE - vars for AI feature checks (for better turn times)
				self.PAE_AI_ID = -1
				self.PAE_AI_ID2 = -1
				self.PAE_AI_Cities_Slaves = []
				self.PAE_AI_Cities_Slavemarket = []

		# Wird am Ende einer Runde ausgefuehrt
		def isVictoryTest(self):

				# --- PAE: Automated trade routes (Boggy, Flunky, Pie)
				# --- PAE: AI Generals with Rhetorik adds morale to all units they move through
				iRange = gc.getMAX_PLAYERS()
				for i in range(iRange):
						pPlayer = gc.getPlayer(i)
						# if pPlayer.isHuman():
						(pLoopUnit, pIter) = pPlayer.firstUnit(False)
						while pLoopUnit:
								if pLoopUnit.getUnitType() in L.LTradeUnits:
										PAE_Trade.doAutomateMerchant(pLoopUnit)
								elif pLoopUnit.getLeaderUnitType() > -1 and not pPlayer.isHuman():
										if pLoopUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RHETORIK")):
												PAE_Unit.doMoralUnitsAI(pLoopUnit)
								(pLoopUnit, pIter) = pPlayer.nextUnit(pIter, False)

				# --- BTS ---
				return gc.getGame().getElapsedGameTurns() > 10

		def isVictory(self, argsList):
				# eVictory = argsList[0]
				return True

		def isPlayerResearch(self, argsList):
				# ePlayer = argsList[0]
				return True

		def getExtraCost(self, argsList):
				# ePlayer = argsList[0]
				return 0

		def createBarbarianCities(self):
				return False

		def createBarbarianUnits(self):
				return False

		def skipResearchPopup(self, argsList):
				# ePlayer = argsList[0]
				return False

		def showTechChooserButton(self, argsList):
				# ePlayer = argsList[0]
				return True

		def getFirstRecommendedTech(self, argsList):
				# ePlayer = argsList[0]
				return TechTypes.NO_TECH

		def getSecondRecommendedTech(self, argsList):
				# ePlayer = argsList[0]
				# eFirstTech = argsList[1]
				return TechTypes.NO_TECH

		def canRazeCity(self, argsList):
				# iRazingPlayer, pCity = argsList
				return True

		def canDeclareWar(self, argsList):
				# iAttackingTeam, iDefendingTeam = argsList
				return True

		def skipProductionPopup(self, argsList):
				# pCity = argsList[0]
				return False

		def showExamineCityButton(self, argsList):
				# pCity = argsList[0]
				return True

		def getRecommendedUnit(self, argsList):
				# pCity = argsList[0]
				return UnitTypes.NO_UNIT

		def getRecommendedBuilding(self, argsList):
				# pCity = argsList[0]
				return BuildingTypes.NO_BUILDING

		def updateColoredPlots(self):
				pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
				if pHeadSelectedUnit is not None and not pHeadSelectedUnit.isNone():
						# if pHeadSelectedUnit.plot().getOwner() == pHeadSelectedUnit.getOwner():
						iUnitType = pHeadSelectedUnit.getUnitType()
						iPlayer = pHeadSelectedUnit.getOwner()
						pPlayer = gc.getPlayer(iPlayer)
						iTeam = pPlayer.getTeam()
						pTeam = gc.getTeam(iTeam)
						
						# PAE VII: Vasall und Team Mitglieder
						lTeamPlayer = []
						iRange = gc.getMAX_PLAYERS()
						for i in range(iRange):
							pTmp = gc.getPlayer(i)
							iTmp = pTmp.getTeam()
							if iTmp == iTeam or gc.getTeam(iTmp).isVassal(iTeam):
								lTeamPlayer.append(i)

						if not CyInterface().isCityScreenUp():
								# Worker, Arbeitstrupp oder Sklave, Slave
								if (iUnitType == gc.getInfoTypeForString("UNIT_WORKER") or iUnitType == gc.getInfoTypeForString("UNIT_SLAVE") or iUnitType == gc.getInfoTypeForString("UNIT_WORK_ELEPHANT")):
										if iUnitType == gc.getInfoTypeForString("UNIT_SLAVE"):
												bSlave = True
										else:
												bSlave = False
										iMapW = gc.getMap().getGridWidth()
										iMapH = gc.getMap().getGridHeight()
										iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
										iOreCamp = gc.getInfoTypeForString("IMPROVEMENT_ORE_CAMP")
										iCamp = gc.getInfoTypeForString("IMPROVEMENT_CAMP")
										lCampBonus = [
												gc.getInfoTypeForString("BONUS_DEER"),
												gc.getInfoTypeForString("BONUS_FUR"),
												gc.getInfoTypeForString("BONUS_LION"),
												gc.getInfoTypeForString("BONUS_CAMEL"),
												gc.getInfoTypeForString("BONUS_HUNDE"),
												gc.getInfoTypeForString("BONUS_WALRUS"),
												gc.getInfoTypeForString("BONUS_IVORY"),
												gc.getInfoTypeForString("BONUS_IVORY2")
										]
										for x in range(iMapW):
												for y in range(iMapH):
														loopPlot = gc.getMap().plot(x, y)
														if loopPlot is not None and not loopPlot.isNone():
																if loopPlot.getFeatureType() == iDarkIce:
																		continue
																if loopPlot.isWater() or loopPlot.isPeak() or loopPlot.isCity():
																		continue
																if loopPlot.getOwner() == iPlayer:
																		eBonus = loopPlot.getBonusType(iPlayer)
																		if eBonus != -1:
																				iImprovement = loopPlot.getImprovementType()
																				# or not loopPlot.isConnectedToCapital(iPlayer)
																				if (iImprovement == -1 or
																						not gc.getImprovementInfo(iImprovement).isImprovementBonusTrade(eBonus) and not gc.getImprovementInfo(iImprovement).isActsAsCity() or
																						not loopPlot.isBonusNetwork(pPlayer.getTeam())
																				):
																						CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_HIGHLIGHT_TEXT", 1)
																				elif iImprovement == iCamp and eBonus not in lCampBonus:
																						if loopPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_FOREST"):
																								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_BEWAFFNUNG")):
																										CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_HIGHLIGHT_TEXT", 1)
																						elif loopPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_DICHTERWALD"):
																								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_BEWAFFNUNG2")):
																										CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_HIGHLIGHT_TEXT", 1)
																				elif iImprovement == iOreCamp:
																						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_MINING")):
																								CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_HIGHLIGHT_TEXT", 1)
																		# Latifundium oder Village/Dorf
																		if bSlave:
																				iImprovement = loopPlot.getImprovementType()
																				if iImprovement != -1 and (iImprovement in L.LLatifundien or iImprovement in L.LVillages):
																						CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_TECH_GREEN", 1)

										# Sklavenmarkt
										if bSlave:
												for i in lTeamPlayer:
														loopPlayer = gc.getPlayer(i)
														(loopCity, pIter) = loopPlayer.firstCity(False)
														while loopCity:
																if not loopCity.isNone():
																		if loopCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STADT")):
																				if not loopCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")):
																						CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
																(loopCity, pIter) = loopPlayer.nextCity(pIter, False)

								# Hunter
								if iUnitType == gc.getInfoTypeForString("UNIT_HUNTER"):
										loopPlot = PAE_Unit.huntingCity(pHeadSelectedUnit)
										if loopPlot:
												CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_GREEN", 1)

										# Cities im Jagdradius
										#(loopCity, pIter) = pPlayer.firstCity(False)
										#while loopCity:
										#		loopPlot = loopCity.plot()
										#		if PAE_Unit.huntingDistance(loopPlot, pHeadSelectedUnit.plot()):
										#				CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_GREEN", 1)
										#		else:
										#				CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_RED", 1)
										#		(loopCity, pIter) = pPlayer.nextCity(pIter, False)

										# Wälder ohne Lager (nur bei Deer und Fur)
										#iMapW = gc.getMap().getGridWidth()
										#iMapH = gc.getMap().getGridHeight()
										#iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
										#iCamp = gc.getInfoTypeForString("IMPROVEMENT_CAMP")
										#lBonus = [
										#		gc.getInfoTypeForString("BONUS_DEER"),
										#		gc.getInfoTypeForString("BONUS_FUR")
										#]
										#for x in range(iMapW):
										#		for y in range(iMapH):
										#				loopPlot = gc.getMap().plot(x, y)
										#				if loopPlot is not None and not loopPlot.isNone():
										#						if loopPlot.getFeatureType() == iDarkIce:
										#								continue
										#						if loopPlot.isWater() or loopPlot.isPeak() or loopPlot.isCity():
										#								continue
										#						#if loopPlot.getFeatureType() in L.LForests:
										#						if loopPlot.getOwner() == iPlayer:
										#								if loopPlot.getBonusType(iPlayer) in lBonus:
										#										eBonus = loopPlot.getBonusType(iPlayer)
										#										eImprovement = loopPlot.getImprovementType()
										#										if eImprovement == -1 or not gc.getImprovementInfo(eImprovement).isImprovementBonusTrade(eBonus):
										#												CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_HIGHLIGHT_TEXT", 1)
										#								elif loopPlot.getFeatureType() in L.LForests:
										#										if loopPlot.getImprovementType() == -1:
										#												CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_PLAYER_DARK_GREEN", 1)


								# Auswanderer
								elif iUnitType == gc.getInfoTypeForString("UNIT_EMIGRANT"):
										iMapW = gc.getMap().getGridWidth()
										iMapH = gc.getMap().getGridHeight()
										iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
										iCottage = gc.getInfoTypeForString("IMPROVEMENT_COTTAGE")
										iTeam = pPlayer.getTeam()
										for x in range(iMapW):
												for y in range(iMapH):
														loopPlot = gc.getMap().plot(x, y)
														if loopPlot is not None and not loopPlot.isNone():
																if loopPlot.getFeatureType() == iDarkIce or loopPlot.isWater() or loopPlot.isPeak() or loopPlot.isCity():
																		continue
																if loopPlot.getOwner() == iPlayer:
																		if loopPlot.isPlayerCityRadius(iPlayer):
																				# Village/Dorf
																				iImprovement = loopPlot.getImprovementType()
																				if iImprovement in L.LVillages or (iImprovement == -1 and loopPlot.canHaveImprovement(iCottage, iTeam, False)):
																						CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_TECH_GREEN", 1)
																				elif iImprovement == gc.getInfoTypeForString("IMPROVEMENT_VILLAGE") and pTeam.isHasTech(gc.getInfoTypeForString("TECH_HEILKUNDE")):
																						CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_TECH_GREEN", 1)


								# Cultivation
								elif iUnitType in L.LCultivationUnits + L.LTradeUnits:

										# Workboat, Arbeitsboot
										if iUnitType == gc.getInfoTypeForString("UNIT_WORKBOAT"):
												iMapW = gc.getMap().getGridWidth()
												iMapH = gc.getMap().getGridHeight()
												iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
												for x in range(iMapW):
														for y in range(iMapH):
																loopPlot = gc.getMap().plot(x, y)
																if loopPlot is not None and not loopPlot.isNone():
																		if loopPlot.getFeatureType() == iDarkIce:
																				continue
																		if not loopPlot.isWater():
																				continue
																		if loopPlot.getOwner() in lTeamPlayer:
																				eBonus = loopPlot.getBonusType(loopPlot.getOwner())
																				if eBonus != -1:
																						iImprovement = loopPlot.getImprovementType()
																						if iImprovement == -1:
																								CyEngine().addColoredPlotAlt(loopPlot.getX(), loopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_HIGHLIGHT_TEXT", 1)

										eBonus = CvUtil.getScriptData(pHeadSelectedUnit, ["b"], -1)
										if eBonus != -1:  # and not gc.getActivePlayer().isOption(PlayerOptionTypes.PLAYEROPTION_NO_UNIT_RECOMMENDATIONS):
												if eBonus in L.LBonusStratCultivatable:
														self.colorPlots4strategicBonus(pHeadSelectedUnit, eBonus)
												else:
														(loopCity, pIter) = pPlayer.firstCity(False)
														while loopCity:
																#loopCity = pHeadSelectedUnit.plot().getWorkingCity()
																if not loopCity.isNone() and loopCity.getOwner() == pPlayer.getID():
																		for iI in range(gc.getNUM_CITY_PLOTS()):
																				pLoopPlot = loopCity.getCityIndexPlot(iI)
																				if pLoopPlot is not None and not pLoopPlot.isNone():
																						if PAE_Cultivation._isBonusCultivationChance(iPlayer, pLoopPlot, eBonus, False, loopCity):
																								CyEngine().addColoredPlotAlt(pLoopPlot.getX(), pLoopPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_TECH_GREEN", 1)
																						elif eBonus not in L.LBonusPlantation:
																								lPlots = PAE_Cultivation.getCityCultivatedPlots(loopCity, eBonus)
																								for p in lPlots:
																										ePlotBonus = p.getBonusType(pHeadSelectedUnit.getOwner())
																										if ePlotBonus in L.LBonusCorn and eBonus in L.LBonusCorn or ePlotBonus in L.LBonusLivestock and eBonus in L.LBonusLivestock:
																												CyEngine().addColoredPlotAlt(p.getX(), p.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_YIELD_FOOD", 1)
																										else:
																												CyEngine().addColoredPlotAlt(p.getX(), p.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_PLAYER_PALE_RED", 1)
																		#pBestPlot = PAE_Cultivation.AI_bestCultivation(loopCity, 0, eBonus)
																		# if pBestPlot:
																		#    CyEngine().addColoredPlotAlt(pBestPlot.getX(), pBestPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_HIGHLIGHT_TEXT", 1.0)
																		#    pSecondBestPlot = PAE_Cultivation.AI_bestCultivation(loopCity, 1, eBonus)
																		#    if pSecondBestPlot:
																		#        CyEngine().addColoredPlotAlt(pSecondBestPlot.getX(), pSecondBestPlot.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_HIGHLIGHT_TEXT", 1.0)
																(loopCity, pIter) = pPlayer.nextCity(pIter, False)

								# Donkey/Esel
								elif iUnitType == gc.getInfoTypeForString("UNIT_ESEL"):
										eBonus = gc.getInfoTypeForString("BONUS_ESEL")
										self.colorPlots4strategicBonus(pHeadSelectedUnit, eBonus)

								# Horse/Pferd
								elif iUnitType == gc.getInfoTypeForString("UNIT_HORSE"):
										eBonus = gc.getInfoTypeForString("BONUS_HORSE")
										self.colorPlots4strategicBonus(pHeadSelectedUnit, eBonus)

								# Camel/Kamel
								elif iUnitType == gc.getInfoTypeForString("UNIT_CAMEL"):
										eBonus = gc.getInfoTypeForString("BONUS_CAMEL")
										self.colorPlots4strategicBonus(pHeadSelectedUnit, eBonus)

								# Elephant/Elefant
								# elif iUnitType == gc.getInfoTypeForString("UNIT_ELEFANT"):
								#    eBonus = gc.getInfoTypeForString("BONUS_IVORY")
								#    self.colorPlots4strategicBonus(pHeadSelectedUnit, eBonus)

								# Handelskarren, Karawanen
								elif iUnitType in L.LTradeUnits and pHeadSelectedUnit.getDomainType() == DomainTypes.DOMAIN_LAND:
										iMapW = gc.getMap().getGridWidth()
										iMapH = gc.getMap().getGridHeight()
										iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
										for x in range(iMapW):
												for y in range(iMapH):
														loopPlot = gc.getMap().plot(x, y)
														if loopPlot and not loopPlot.isNone():
																if loopPlot.getFeatureType() == iDarkIce:
																		continue
																if loopPlot.isWater() or loopPlot.isPeak() or loopPlot.isCity():
																		continue
																if loopPlot.getOwner() != -1 or loopPlot.getBonusType(iPlayer) == -1:
																		continue
																if loopPlot.isActiveVisible(0) and (loopPlot.getImprovementType() == -1 or loopPlot.getImprovementType() != -1 and loopPlot.getOwner() == -1):
																		CyEngine().addColoredPlotAlt(x, y, PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)

								# Great General
								elif iUnitType == gc.getInfoTypeForString("UNIT_GREAT_GENERAL"):
										iBuilding1 = gc.getInfoTypeForString("BUILDING_ROMAN_SHRINE")
										iBuilding2 = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationBuildings(gc.getInfoTypeForString("BUILDINGCLASS_HEROIC_EPIC"))
										iBuilding3 = gc.getInfoTypeForString("BUILDING_MILITARY_ACADEMY")
										iBuilding4 = gc.getInfoTypeForString("BUILDING_SIEGESSTATUE")
										iBuilding5 = gc.getInfoTypeForString("BUILDING_SIEGESSAEULE")
										iBuilding6 = gc.getInfoTypeForString("BUILDING_ELEPHANTMONUMENT")
										iBuilding7 = gc.getInfoTypeForString("BUILDING_TRIUMPH")
										(loopCity, pIter) = pPlayer.firstCity(False)
										while loopCity:
												if not loopCity.isNone():
														if pHeadSelectedUnit.canConstruct(loopCity.plot(), iBuilding1):
																CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_GREEN", 1)
														elif pHeadSelectedUnit.canConstruct(loopCity.plot(), iBuilding2):
																CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
														elif pHeadSelectedUnit.canConstruct(loopCity.plot(), iBuilding3):
																CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
														elif pHeadSelectedUnit.canConstruct(loopCity.plot(), iBuilding4):
																CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
														elif pHeadSelectedUnit.canConstruct(loopCity.plot(), iBuilding5):
																CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
														elif pHeadSelectedUnit.canConstruct(loopCity.plot(), iBuilding6):
																CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
														elif pHeadSelectedUnit.canConstruct(loopCity.plot(), iBuilding7):
																CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
												(loopCity, pIter) = pPlayer.nextCity(pIter, False)


								# Gladiator
								elif iUnitType == gc.getInfoTypeForString("UNIT_GLADIATOR") and not pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MERCENARY")):
										if not pTeam.isHasTech(gc.getInfoTypeForString("TECH_KONZIL5")) and pTeam.isHasTech(gc.getInfoTypeForString("TECH_GLADIATOR2")):
												iBuilding1 = gc.getInfoTypeForString("BUILDING_STADT")
												iBuilding2 = gc.getInfoTypeForString("BUILDING_GLADIATORENSCHULE")
												(loopCity, pIter) = pPlayer.firstCity(False)
												while loopCity:
														if not loopCity.isNone():
																if loopCity.isHasBuilding(iBuilding1) and not loopCity.isHasBuilding(iBuilding2):
																		CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
														(loopCity, pIter) = pPlayer.nextCity(pIter, False)

								# Reliquie / Relic
								elif iUnitType == gc.getInfoTypeForString("UNIT_RELIC"):
										iBuilding = gc.getInfoTypeForString("BUILDING_MARTYRION")
										(loopCity, pIter) = pPlayer.firstCity(False)
										while loopCity:
												if not loopCity.isNone():
														if not loopCity.isHasBuilding(iBuilding):
																CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
												(loopCity, pIter) = pPlayer.nextCity(pIter, False)

								# Versorgungskarren / Heldendenkmal
								elif iUnitType == gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"):
										iBuilding = PAE_Unit.getHeldendenkmal(pHeadSelectedUnit)
										if iBuilding != -1:
												(loopCity, pIter) = pPlayer.firstCity(False)
												while loopCity:
														if not loopCity.isNone():
																if not loopCity.isHasBuilding(iBuilding):
																		CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
														(loopCity, pIter) = pPlayer.nextCity(pIter, False)

								# UNITAI_MISSIONARY = 14
								elif pHeadSelectedUnit.getUnitAIType() == 14:
										pUnit = pHeadSelectedUnit
										iReligion = self.getUnitReligion(pUnit.getUnitType())
										if iReligion != -1:
												(loopCity, pIter) = pPlayer.firstCity(False)
												while loopCity:
														if not loopCity.isNone():
																if not loopCity.isHasReligion(iReligion):
																		CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
														(loopCity, pIter) = pPlayer.nextCity(pIter, False)
												# Cities of vassals
												iPlayerTeam = pPlayer.getTeam()
												iRange = gc.getMAX_PLAYERS()
												for iVassal in range(iRange):
														pVassal = gc.getPlayer(iVassal)
														if pVassal.isAlive():
																iVassalTeam = pVassal.getTeam()
																pVassalTeam = gc.getTeam(iVassalTeam)
																if pVassalTeam.isVassal(iPlayerTeam):
																		(loopCity, pIter) = pVassal.firstCity(False)
																		while loopCity:
																				if not loopCity.isNone():
																						if not loopCity.isHasReligion(iReligion):
																								CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
																				(loopCity, pIter) = pVassal.nextCity(pIter, False)

										iKult = self.getUnitKult(pUnit.getUnitType())
										if iKult != -1:
												(loopCity, pIter) = pPlayer.firstCity(False)
												while loopCity:
														if not loopCity.isNone():
																if not loopCity.isHasCorporation(iKult):
																		CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
														(loopCity, pIter) = pPlayer.nextCity(pIter, False)
												# Cities of vassals
												iPlayerTeam = pPlayer.getTeam()
												iRange = gc.getMAX_PLAYERS()
												for iVassal in range(iRange):
														pVassal = gc.getPlayer(iVassal)
														if pVassal.isAlive():
																iVassalTeam = pVassal.getTeam()
																pVassalTeam = gc.getTeam(iVassalTeam)
																if pVassalTeam.isVassal(iPlayerTeam):
																		(loopCity, pIter) = pVassal.firstCity(False)
																		while loopCity:
																				if not loopCity.isNone():
																						if not loopCity.isHasCorporation(iKult):
																								CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
																				(loopCity, pIter) = pVassal.nextCity(pIter, False)

								# Goldkarren | Units Rank/Rang Promo Up
								elif iUnitType == gc.getInfoTypeForString("UNIT_GOLDKARREN") or CvUtil.getScriptData(pHeadSelectedUnit, ["P", "t"]) == "RangPromoUp":
										iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")
										iBuilding2 = gc.getInfoTypeForString("BUILDING_PRAEFECTUR")

										(loopCity, pIter) = pPlayer.firstCity(False)
										while loopCity:
												if not loopCity.isNone():
														if loopCity.isCapital() or loopCity.isHasBuilding(iBuilding) or loopCity.isHasBuilding(iBuilding2):
																CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_GREEN", 1)
												(loopCity, pIter) = pPlayer.nextCity(pIter, False)

								# Governor | Statthalter
								elif pHeadSelectedUnit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_STATTHALTER") or \
												pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_HERO")):

										iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")

										(loopCity, pIter) = pPlayer.firstCity(False)
										while loopCity:
												if not loopCity.isNone():
														if loopCity.isHasBuilding(iBuilding):
																CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_GREEN", 1)
														# elif loopCity.canConstruct (iBuilding, False, False, True):
														#  CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_GREEN", 1)
												(loopCity, pIter) = pPlayer.nextCity(pIter, False)

								# Legionaries koennen in Kastellen oder MilAks ausgebildet werden (Auxiliari nicht)
								elif pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_1")) or \
												pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_1")):

										if not pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_11")) and \
														not pHeadSelectedUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_10")):

												if pHeadSelectedUnit.getUnitType() not in L.LUnitAuxiliar:
														iBuilding1 = gc.getInfoTypeForString("BUILDING_MILITARY_ACADEMY")
														iBuilding2 = gc.getInfoTypeForString("BUILDING_BARRACKS")

														(loopCity, pIter) = pPlayer.firstCity(False)
														while loopCity:
																if not loopCity.isNone():
																		if loopCity.isHasBuilding(iBuilding1) or loopCity.isHasBuilding(iBuilding2):
																				CyEngine().addColoredPlotAlt(loopCity.getX(), loopCity.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_PLAYER_DARK_GREEN", 1)
																(loopCity, pIter) = pPlayer.nextCity(pIter, False)

								# Praetorianer, Cohortes Urbanae koennen Latifundien bauen
								elif gc.getUnitInfo(pHeadSelectedUnit.getUnitType()).getBuilds(gc.getInfoTypeForString("BUILD_LATIFUNDIUM")):
										# elif iUnitType == gc.getInfoTypeForString("UNIT_PRAETORIAN"):
										if pTeam.isHasTech(gc.getInfoTypeForString("TECH_RESERVISTEN")):
												iMapW = gc.getMap().getGridWidth()
												iMapH = gc.getMap().getGridHeight()
												iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
												iBuild = gc.getInfoTypeForString("BUILD_LATIFUNDIUM")
												for x in range(iMapW):
														for y in range(iMapH):
																loopPlot = gc.getMap().plot(x, y)
																if loopPlot is not None and not loopPlot.isNone():
																		if loopPlot.getFeatureType() == iDarkIce:
																				continue
																		if loopPlot.isWater() or loopPlot.isPeak() or loopPlot.isCity():
																				continue
																		if loopPlot.getOwner() != iPlayer or loopPlot.getBonusType(iPlayer) == -1:
																				continue
																		if loopPlot.canBuild(iBuild, iPlayer, False):
																				CyEngine().addColoredPlotAlt(x, y, PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_GREEN", 1)

				return False

		def colorPlots4strategicBonus(self, pHeadSelectedUnit, eBonus):
				iPlayer = pHeadSelectedUnit.getOwner()
				pPlayer = gc.getPlayer(iPlayer)

				# PAE VII: Vasall und Team Mitglieder
				iTeam = pPlayer.getTeam()
				pTeam = gc.getTeam(iTeam)
				lTeamPlayer = []
				iRange = gc.getMAX_PLAYERS()
				for i in range(iRange):
					pTmp = gc.getPlayer(i)
					iTmp = pTmp.getTeam()
					if iTmp == iTeam or gc.getTeam(iTmp).isVassal(iTeam):
						lTeamPlayer.append(i)

				eBuilding = -1
				#eCityStatus = gc.getInfoTypeForString("BUILDING_KOLONIE")
				#if eBonus == gc.getInfoTypeForString("BONUS_HORSE"): eBuilding = gc.getInfoTypeForString("BUILDING_STABLE")
				#elif eBonus == gc.getInfoTypeForString("BONUS_CAMEL"): eBuilding = gc.getInfoTypeForString("BUILDING_CAMEL_STABLE")
				# elif eBonus == gc.getInfoTypeForString("BONUS_IVORY"): eBuilding = gc.getInfoTypeForString("BUILDING_ELEPHANT_STABLE")
				# elif eBonus == gc.getInfoTypeForString("BONUS_HUNDE"): eBuilding = gc.getInfoTypeForString("BUILDING_HUNDEZUCHT")

				# iUnitX = pHeadSelectedUnit.plot().getX()
				# iUnitY = pHeadSelectedUnit.plot().getY()

				for i in lTeamPlayer:
					pLoopPlayer = gc.getPlayer(i)
					(loopCity, pIter) = pLoopPlayer.firstCity(False)
					while loopCity:
						# if loopCity.isHasBuilding(eCityStatus):
						if eBuilding == -1 or not loopCity.isHasBuilding(eBuilding):

								iX = loopCity.getX()
								iY = loopCity.getY()
								lPlots = PAE_Cultivation.getCityCultivatedPlots(loopCity, eBonus)

								for p in lPlots:
										if p.getBonusType(-1) == eBonus:
												iImp = p.getImprovementType()
												if iImp != -1 and gc.getImprovementInfo(iImp).isImprovementBonusMakesValid(eBonus):
														#CyEngine().addColoredPlotAlt(iX, iY, PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_RED", 1)
														CyEngine().addColoredPlotAlt(p.getX(), p.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_PLAYER_PALE_RED", 1)
												else:
														CyEngine().addColoredPlotAlt(p.getX(), p.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_PLAYER_ORANGE", 1)

								lPlots = PAE_Cultivation.getCityCultivatablePlots(loopCity, eBonus)
								if lPlots:
										CyEngine().addColoredPlotAlt(iX, iY, PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_WHITE", 1)
										for p in lPlots:
												if p:
														CyEngine().addColoredPlotAlt(p.getX(), p.getY(), PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_HIGHLIGHT_TEXT", 1)

						# else:
						#    CyEngine().addColoredPlotAlt(iX, iY, PlotStyles.PLOT_STYLE_CIRCLE, PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_RECOMMENDED_PLOTS, "COLOR_PLAYER_PALE_RED", 1)
						(loopCity, pIter) = pLoopPlayer.nextCity(pIter, False)

		def isActionRecommended(self, argsList):
				pUnit = argsList[0]
				iAction = argsList[1]
				# TEST ungueltige Action abgefragt, wo kommt das her.
				if iAction == -1:
						CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", (pUnit.getName, iAction)), None, 2, None, ColorTypes(12), 0, 0, False, False)
				elif gc.getActionInfo(iAction).getMissionType() == MissionTypes.MISSION_CONSTRUCT:
						return True
				return False

		def unitCannotMoveInto(self, argsList):
				# ePlayer = argsList[0]
				# iUnitId = argsList[1]
				iPlotX = argsList[2]
				iPlotY = argsList[3]
				###########################################
				# Max Units on a Plot
				# Only available when changed in Assets/PythonCallbackDefines.xml
				pPlot = CyMap().plot(iPlotX, iPlotY)
				iNum = pPlot.getNumUnits()
				# CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_GROWTH",("X",iNum)), None, 2, None, ColorTypes(12), 0, 0, False, False)
				if not pPlot.isWater() and not pPlot.isCity() and iNum >= 14:
						return True
				# --------- end ---------------------------
				return False

		def cannotHandleAction(self, argsList):
				# pPlot = argsList[0]
				# iAction = argsList[1]
				# bTestVisible = argsList[2]
				return False

		# In PythonCallbackDefines.xml wieder deaktiviert, weil es BTS exrem verlangsamt (soll deaktiviert bleiben)
		def canBuild(self, argsList):
				iX, iY, iBuild, iPlayer = argsList

				# Aussenhandelsposten nicht im eigenen Land
				# if iBuild == gc.getInfoTypeForString("BUILD_HANDELSPOSTEN"):
				#  if CyMap().plot(iX, iY).getOwner() != -1:
				#    return 0

				if iBuild == gc.getInfoTypeForString("BUILD_LATIFUNDIUM"):
						if not CyMap().plot(iX, iY).isFlatlands():
								return 0

				elif iBuild == gc.getInfoTypeForString("BUILD_KASTELL") or iBuild in L.LBuildLimes:
						pPlot = CyMap().plot(iX, iY)
						if pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_DARK_ICE"):
								return 0
						if pPlot.isWater() or pPlot.isPeak() or pPlot.isCity():
								return 0
						if pPlot.getImprovementType() != -1:
								return 0
						if iBuild == gc.getInfoTypeForString("BUILD_KASTELL") and not pPlot.isFlatlands():
								return 0
						return 1

				return -1  # Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can

		def cannotFoundCity(self, argsList):
				iPlayer, iPlotX, iPlotY = argsList
				return False

		def cannotSelectionListMove(self, argsList):
				# pPlot = argsList[0]
				# bAlt = argsList[1]
				# bShift = argsList[2]
				# bCtrl = argsList[3]
				return False

		def cannotSelectionListGameNetMessage(self, argsList):
				# eMessage = argsList[0]
				# iData2 = argsList[1]
				# iData3 = argsList[2]
				# iData4 = argsList[3]
				# iFlags = argsList[4]
				# bAlt = argsList[5]
				# bShift = argsList[6]
				return False

		def cannotDoControl(self, argsList):
				# eControl = argsList[0]
				return False

		def canResearch(self, argsList):
				# ePlayer = argsList[0]
				# eTech = argsList[1]
				# bTrade = argsList[2]
				return False

		# PAE 6.10: activated for city states
		def cannotResearch(self, argsList):
				ePlayer = argsList[0]
				eTech = argsList[1]
				# bTrade = argsList[2]

				# city states / Stadtstaaten
				if eTech == gc.getInfoTypeForString("TECH_COLONIZATION"):
						# if gc.getPlayer(ePlayer).countNumBuildings(gc.getInfoTypeForString("BUILDING_CITY_STATE")) > 0:
						if gc.getTeam(gc.getPlayer(ePlayer).getTeam()).isHasTech(gc.getInfoTypeForString("TECH_CITY_STATE")):
								return True

				return False

		def canDoCivic(self, argsList):
				ePlayer = argsList[0]
				eCivic = argsList[1]
				# Trait Imperialist: Herrscherkult und Imperator von Anfang an / ruler cult right from the beginning
				if ePlayer != -1:
						pPlayer = gc.getPlayer(ePlayer)
						if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_IMPERIALIST")):
								if eCivic == gc.getInfoTypeForString("CIVIC_IMPERATOR") or eCivic == gc.getInfoTypeForString("CIVIC_HERRSCHERKULT"):
										return True
				# --
				return False

		def cannotDoCivic(self, argsList):
				ePlayer = argsList[0]
				# eCivic = argsList[1]

				# Szenarien: Wechsel erst ab einer bestimmten Runde möglich
				sScenarioName = CvUtil.getScriptData(CyMap().plot(0, 0), ["S", "t"])
				iRound = gc.getGame().getGameTurn() - gc.getGame().getStartTurn()
				if sScenarioName == "PeloponnesianWarKeinpferd" or sScenarioName == "FirstPunicWar" or sScenarioName == "WarOfDiadochi":
						if not gc.getPlayer(ePlayer).isHuman() and iRound <= 50:
								return True
				if sScenarioName == "480BC" or sScenarioName == "LimesGermanicus":
						if not gc.getPlayer(ePlayer).isHuman() and iRound <= 20:
								return True
				return False

		def canTrain(self, argsList):
				# pCity = argsList[0]
				# eUnit = argsList[1]
				# bContinue = argsList[2]
				# bTestVisible = argsList[3]
				# bIgnoreCost = argsList[4]
				# bIgnoreUpgrades = argsList[5]

				return False

		# Diese funktion ist im PythonCallback.xml AKTIVIERT
		def cannotTrain(self, argsList):
				pCity = argsList[0]
				eUnit = argsList[1]
				# bContinue = argsList[2]
				# bTestVisible = argsList[3]
				# bIgnoreCost = argsList[4]
				# bIgnoreUpgrades = argsList[5]

				#pUnit = gc.getUnitInfo(eUnit)

				# PAE Trade units
				if eUnit in L.LTradeUnits:
						iPlayer = pCity.getOwner()
						pPlayer = gc.getPlayer(iPlayer)
						if not PAE_Trade.canCreateTradeUnit(pPlayer, pCity):
								return True

				# PAE Emigrants
				if eUnit == gc.getInfoTypeForString("UNIT_EMIGRANT"):
						if pCity.getPopulation() < 6:
								return True
						if pCity.goodHealth() - pCity.badHealth(False) > 0 and pCity.happyLevel() - pCity.unhappyLevel(0) > 0:
								return True

				# KI Rammen Problem
				if eUnit in L.LRammen:
						iPlayer = pCity.getOwner()
						pPlayer = gc.getPlayer(iPlayer)
						if pPlayer.getUnitClassCountPlusMaking(gc.getUnitInfo(eUnit).getUnitClassType()) > 10:
								return True

				return False

		def canConstruct(self, argsList):
				# pCity = argsList[0]
				# eBuilding = argsList[1]
				# bContinue = argsList[2]
				# bTestVisible = argsList[3]
				# bIgnoreCost = argsList[4]
				return False

		# Diese funktion ist im PythonCallback.xml AKTIVIERT
		def cannotConstruct(self, argsList):
				pCity = argsList[0]
				eBuilding = argsList[1]
				# bContinue = argsList[2]
				# bTestVisible = argsList[3]
				# bIgnoreCost = argsList[4]

				# Stallungen: Pferd, Kamel, Ele / Stables: horse, camel, ele
				lStrategicBonusBuildings = [
						gc.getInfoTypeForString("BUILDING_STABLE"),
						gc.getInfoTypeForString("BUILDING_CAMEL_STABLE"),
						gc.getInfoTypeForString("BUILDING_ELEPHANT_STABLE")
				]
				if eBuilding in lStrategicBonusBuildings:
						eBonus = gc.getBuildingInfo(eBuilding).getPrereqAndBonus()
						# lPlots = PAE_Cultivation.getCityCultivatedPlots(pCity, eBonus)

						# Ressource muss im Stadtradius sein
						for i in range(gc.getNUM_CITY_PLOTS()):
								p = pCity.getCityIndexPlot(i)
								if p is not None and not p.isNone():
										if p.getBonusType(-1) == eBonus and p.getOwner() == pCity.getOwner():
												iImp = p.getImprovementType()
												if iImp != -1 and gc.getImprovementInfo(iImp).isImprovementBonusMakesValid(eBonus):
														return False

						# Bau uebers Handelsnetz ermoeglichen:
						# if pCity.hasBonus(eBonus) and PAE_Cultivation._bonusIsCultivatableFromCity(pCity.getOwner(), pCity, eBonus, False):
						#    if not lPlots: 
						#        return False

						return True

				# Buildings für erweiterten Radius (3x3)
				elif eBuilding == gc.getInfoTypeForString("BUILDING_IVORY_MARKET"):
						lBonus = [
								gc.getInfoTypeForString("BONUS_WALRUS"),
								gc.getInfoTypeForString("BONUS_IVORY"),
								gc.getInfoTypeForString("BONUS_IVORY2")
						]

						# Erweiterter Radius
						iRange = 3
						iX = pCity.getX()
						iY = pCity.getY()
						for i in range(-iRange, iRange+1):
								for j in range(-iRange, iRange+1):
										loopPlot = plotXY(iX, iY, i, j)
										if loopPlot is not None and not loopPlot.isNone():
												eBonus = loopPlot.getBonusType(-1)
												if eBonus in lBonus:
														iImp = loopPlot.getImprovementType()
														if iImp != -1 and gc.getImprovementInfo(iImp).isImprovementBonusMakesValid(eBonus):
																return False
						return True

				# Wasserrad etc. im BuildingInfos.xml als bRiver deklariert
				# elif eBuilding in lRiverBuildings:
				#  if not pCity.plot().isRiver(): return True

				# Akropolis
				elif eBuilding == gc.getInfoTypeForString("BUILDING_ACROPOLIS"):
						# Um die Stadt bzw unter der Stadt muss ein Hill sein
						iRange = 1
						iX = pCity.getX()
						iY = pCity.getY()
						for i in range(-iRange, iRange+1):
								for j in range(-iRange, iRange+1):
										loopPlot = plotXY(iX, iY, i, j)
										if loopPlot is not None and not loopPlot.isNone():
												if loopPlot.isHills():
														return False
						return True

				# Ausbildungslager / first type of barracks
				elif eBuilding == gc.getInfoTypeForString("BUILDING_BARRACKS"):
						if not gc.getPlayer(pCity.getOwner()).isCivic(gc.getInfoTypeForString("CIVIC_BERUFSARMEE")):
								return True

				# Aqueducts
				elif eBuilding == gc.getInfoTypeForString("BUILDING_AQUEDUCT"):
						if gc.getPlayer(pCity.getOwner()).getCivilizationType() not in L.LCivsWithAqueduct:
								return True

				# Wonder Gorgan Walls
				elif eBuilding == gc.getInfoTypeForString("BUILDING_GREAT_WALL_GORGAN"):
						pPlayer = gc.getPlayer(pCity.getOwner())
						if gc.getTeam(pPlayer.getTeam()).getAtWarCount(True) < 2:
								return True

				# Buildings, die pro Ressource baubar sind
				elif eBuilding == gc.getInfoTypeForString("BUILDING_SCHMIEDE_BRONZE"):
						pPlayer = gc.getPlayer(pCity.getOwner())
						#iAnzB = pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString("BUILDINGCLASS_SCHMIEDE_BRONZE")) => BTS Befehl funkt nicht richtig (Gebäude wird ständig unterbrochen)
						iAnzB = self.getBuildingClassCountPlusOtherCitiesMaking(pPlayer, pCity, eBuilding, gc.getInfoTypeForString("BUILDINGCLASS_SCHMIEDE_BRONZE"))
						iAnz1 = pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_COPPER"))
						iAnz2 = pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_COAL"))
						iAnz2 += pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_ZINN"))
						iCheck = min(iAnz1, iAnz2)
						if iCheck == 0 or iAnzB >= iCheck:
								return True

				elif eBuilding == gc.getInfoTypeForString("BUILDING_SCHMIEDE_MESSING"):
						pPlayer = gc.getPlayer(pCity.getOwner())
						iAnzB = self.getBuildingClassCountPlusOtherCitiesMaking(pPlayer, pCity, eBuilding, gc.getInfoTypeForString("BUILDINGCLASS_SCHMIEDE_MESSING"))
						iAnz1 = pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_COPPER"))
						iAnz2 = pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_ZINK"))
						iCheck = min(iAnz1, iAnz2)
						if iCheck == 0 or iAnzB >= iCheck:
								return True

				# Goldschmied: nur wenn man mehr von einer Resource besitzt
				elif eBuilding == gc.getInfoTypeForString("BUILDING_GOLDSCHMIED"):
						pPlayer = gc.getPlayer(pCity.getOwner())
						iAnzB = self.getBuildingClassCountPlusOtherCitiesMaking(pPlayer, pCity, eBuilding, gc.getInfoTypeForString("BUILDINGCLASS_GOLDSCHMIED"))
						sAnz = []
						sAnz.append(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_GOLD")))
						sAnz.append(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_SILVER")))
						sAnz.append(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_PEARL")))
						sAnz.append(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_GEMS")))
						sAnz.append(pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_BERNSTEIN")))
						if iAnzB >= max(sAnz):
								return True

				elif eBuilding == gc.getInfoTypeForString("BUILDING_GUSS_IRON"):
						pPlayer = gc.getPlayer(pCity.getOwner())
						iAnzB = self.getBuildingClassCountPlusOtherCitiesMaking(pPlayer, pCity, eBuilding, gc.getInfoTypeForString("BUILDINGCLASS_GUSS_IRON"))
						iAnz = pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString("BONUS_IRON"))
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Building",iAnzB)), None, 2, None, ColorTypes(10), 0, 0, False, False)
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Bonus",iAnz)), None, 2, None, ColorTypes(10), 0, 0, False, False)
						if iAnzB >= iAnz:
								return True

				# Palisaden nur wenn Wald im angrenzenden Gebiet ist (5x5)
				elif eBuilding == gc.getInfoTypeForString("BUILDING_PALISADE"):
						LForests = [
								gc.getInfoTypeForString("FEATURE_JUNGLE"),
								gc.getInfoTypeForString("FEATURE_FOREST"),
								gc.getInfoTypeForString("FEATURE_DICHTERWALD")
						]
						iRange = 2
						iX = pCity.getX()
						iY = pCity.getY()
						for i in range(-iRange, iRange+1):
								for j in range(-iRange, iRange+1):
										loopPlot = plotXY(iX, iY, i, j)
										if loopPlot is not None and not loopPlot.isNone():
												if loopPlot.getFeatureType() in LForests:
														return False
						return True

				# Buildings, die ihre notwendige Ressource im Stadtradius brauchen
				lBonusBuildings = [
						gc.getInfoTypeForString("BUILDING_WINERY"),
						gc.getInfoTypeForString("BUILDING_PAPYRUSPOST"),
						gc.getInfoTypeForString("BUILDING_MUREX"),
						#gc.getInfoTypeForString("BUILDING_GERBEREI"),
						gc.getInfoTypeForString("BUILDINGCLASS_WINDOFEN_NATIONAL"),
						gc.getInfoTypeForString("BUILDING_GUSS_BLEI"),
						gc.getInfoTypeForString("BUILDING_GUSS_COPPER"),
						gc.getInfoTypeForString("BUILDING_GUSS_ZINN"),
						gc.getInfoTypeForString("BUILDING_GUSS_ZINK"),
						gc.getInfoTypeForString("BUILDING_FURRIER"),
						gc.getInfoTypeForString("BUILDING_MARMOR_WERKSTATT")
				]
				if eBuilding in lBonusBuildings:
						bonus = PAE_City.bonusMissingCity(pCity, eBuilding)
						if bonus is not None:
								return True

				# Standard-Einstellung: alles baubar
				return False

		def canCreate(self, argsList):
				# pCity = argsList[0]
				# eProject = argsList[1]
				# bContinue = argsList[2]
				# bTestVisible = argsList[3]
				return False

		def cannotCreate(self, argsList):
				pCity = argsList[0]
				eProject = argsList[1]
				# bContinue = argsList[2]
				# bTestVisible = argsList[3]

				if eProject == gc.getInfoTypeForString("PROJECT_OLYMPIC_GAMES"):
						if not pCity.isHasReligion(gc.getInfoTypeForString("RELIGION_GREEK")):
								return True

				return False

		def canMaintain(self, argsList):
				# pCity = argsList[0]
				# eProcess = argsList[1]
				# bContinue = argsList[2]
				return False

		def cannotMaintain(self, argsList):
				# pCity = argsList[0]
				# eProcess = argsList[1]
				# bContinue = argsList[2]
				return False

		def AI_chooseTech(self, argsList):
				ePlayer = argsList[0]
				# bFree = argsList[1]
				pPlayer = gc.getPlayer(ePlayer)
				iCiv = pPlayer.getCivilizationType()
				pTeam = gc.getTeam(pPlayer.getTeam())
				iTech = -1
				iBronze = gc.getInfoTypeForString('BONUS_BRONZE')
				iHorse = gc.getInfoTypeForString('BONUS_HORSE')
				iEles = gc.getInfoTypeForString('BONUS_IVORY')
				iCamel = gc.getInfoTypeForString('BONUS_CAMEL')
				# iStone = gc.getInfoTypeForString('BONUS_STONE')
				# iMarble = gc.getInfoTypeForString('BONUS_MARBLE')

				# Hauptabfragen, um nicht zuviele if-Checks zu haben:
				lTechs = []

				# vor Fuehrerschaft
				if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_LEADERSHIP')):

						# 1. Jagd (Lager)
						lTechs.append(gc.getInfoTypeForString('TECH_HUNTING'))
						# 2. Mystik (Forschung)
						lTechs.append(gc.getInfoTypeForString('TECH_MYSTICISM'))

						# Religionsweg
						# Egypt und Sumer
						if (iCiv == gc.getInfoTypeForString('CIVILIZATION_EGYPT') or
							 iCiv == gc.getInfoTypeForString('CIVILIZATION_SUMERIA') or
							 iCiv == gc.getInfoTypeForString('CIVILIZATION_INDIA')
							):
								# 3. Schamanismus (Monolith)
								lTechs.append(gc.getInfoTypeForString('TECH_SCHAMANISMUS'))
								# Hindu
								lTechs.append(gc.getInfoTypeForString('TECH_RELIGION_HINDU'))
								# 4. Polytheismus (Kleines Orakel)
								lTechs.append(gc.getInfoTypeForString('TECH_POLYTHEISM'))
								# 5. Religion
								lTechs.append(gc.getInfoTypeForString('TECH_RELIGION_EGYPT'))
								# 5. Religion
								lTechs.append(gc.getInfoTypeForString('TECH_RELIGION_SUMER'))
								# 6. Priestertum (Civic)
								lTechs.append(gc.getInfoTypeForString('TECH_PRIESTHOOD'))
						# Wirtschaftsweg
						else:
								# 4+5. Fischen oder Viehzucht
								if pPlayer.countNumCoastalCities() > 0:
										lTechs.append(gc.getInfoTypeForString('TECH_FISHING'))
										lTechs.append(gc.getInfoTypeForString('TECH_BOOTSBAU'))
								else:
										lTechs.append(gc.getInfoTypeForString('TECH_ANIMAL_HUSBANDRY'))
										lTechs.append(gc.getInfoTypeForString('TECH_FENCES'))
								# 6. Bogenschiessen
								lTechs.append(gc.getInfoTypeForString('TECH_ARCHERY'))
						# Wieder Alle
						# 7. Fuehrerschaft
						lTechs.append(gc.getInfoTypeForString('TECH_LEADERSHIP'))

				# vor Binnenkolonisierung
				if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_COLONIZATION')):

						# Landwirtschaft (Worker, Farm)
						lTechs.append(gc.getInfoTypeForString('TECH_BRUNNEN'))
						lTechs.append(gc.getInfoTypeForString('TECH_AGRICULTURE'))
						lTechs.append(gc.getInfoTypeForString('TECH_PFLUG'))
						# Viehzucht
						lTechs.append(gc.getInfoTypeForString('TECH_ANIMAL_HUSBANDRY'))
						lTechs.append(gc.getInfoTypeForString('TECH_FENCES'))

						# aegyptischer Papyrus
						if iCiv == gc.getInfoTypeForString('CIVILIZATION_EGYPT'):
								lTechs.append(gc.getInfoTypeForString('TECH_FISHING'))
								lTechs.append(gc.getInfoTypeForString('TECH_BOOTSBAU'))

						# Polytheismus (Kleines Orakel)
						lTechs.append(gc.getInfoTypeForString('TECH_SCHAMANISMUS'))
						lTechs.append(gc.getInfoTypeForString('TECH_POLYTHEISM'))

						# Those Civs shall get their neighbour religion at least after leadership
						lTechs.append(gc.getInfoTypeForString('TECH_RELIGION_EGYPT'))
						lTechs.append(gc.getInfoTypeForString('TECH_RELIGION_SUMER'))

						# Bogenschiessen
						lTechs.append(gc.getInfoTypeForString('TECH_ARCHERY'))

						# Metallverarbeitung
						lTechs.append(gc.getInfoTypeForString('TECH_POTTERY'))
						lTechs.append(gc.getInfoTypeForString('TECH_METAL_CASTING'))
						lTechs.append(gc.getInfoTypeForString('TECH_STEINABBAU'))
						lTechs.append(gc.getInfoTypeForString('TECH_METAL_SMELTING'))

						# Priestertum (Civic)
						lTechs.append(gc.getInfoTypeForString('TECH_PRIESTHOOD'))

						# Religious Civs (Civic)
						if pPlayer.getStateReligion() != -1:
								lTechs.append(gc.getInfoTypeForString('TECH_MOND'))
								lTechs.append(gc.getInfoTypeForString('TECH_CEREMONIAL'))

						# Staatenbildung
						lTechs.append(gc.getInfoTypeForString('TECH_STAATENBILDUNG'))
						# Binnenkolonisierung (Siedler)
						lTechs.append(gc.getInfoTypeForString('TECH_COLONIZATION'))

				# vor der BRONZEZEIT
				if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
						# Astronomie (Sternwarte)
						lTechs.append(gc.getInfoTypeForString('TECH_ASTRONOMIE'))
						# Spearmen
						lTechs.append(gc.getInfoTypeForString('TECH_SPEERSPITZEN'))
						# Food
						lTechs.append(gc.getInfoTypeForString('TECH_TAUBENZUCHT'))
						# Wein, wenn Trauben vorhanden
						if pPlayer.countOwnedBonuses(gc.getInfoTypeForString('BONUS_GRAPES')) > 0:
								lTechs.append(gc.getInfoTypeForString('TECH_WEINBAU'))
						# Waffen
						lTechs.append(gc.getInfoTypeForString('TECH_THE_WHEEL'))
						lTechs.append(gc.getInfoTypeForString('TECH_BEWAFFNUNG'))
						# Erster Kult
						lTechs.append(gc.getInfoTypeForString('TECH_CALENDAR'))
						lTechs.append(gc.getInfoTypeForString('TECH_KULTIVIERUNG'))
						lTechs.append(gc.getInfoTypeForString('TECH_FRUCHTBARKEIT'))

						# Hochkulturen
						lTechs.append(gc.getInfoTypeForString('TECH_WRITING'))
						lTechs.append(gc.getInfoTypeForString('TECH_WRITING2'))

						# Bronze
						lTechs.append(gc.getInfoTypeForString('TECH_MINING'))
						lTechs.append(gc.getInfoTypeForString('TECH_BRONZE_WORKING'))

				# vor der EISENZEIT
				if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):

						# Hochkulturen
						lTechs.append(gc.getInfoTypeForString('TECH_ZAHLENSYSTEME'))
						lTechs.append(gc.getInfoTypeForString('TECH_GEOMETRIE'))
						# Warenhandel und Strassen
						lTechs.append(gc.getInfoTypeForString('TECH_WARENHANDEL'))
						lTechs.append(gc.getInfoTypeForString('TECH_THE_WHEEL2'))
						# Bauwerke und Versklavung
						lTechs.append(gc.getInfoTypeForString('TECH_MASONRY'))
						lTechs.append(gc.getInfoTypeForString('TECH_HOLZWEHRANLAGEN'))
						lTechs.append(gc.getInfoTypeForString('TECH_KONSERVIERUNG'))
						lTechs.append(gc.getInfoTypeForString('TECH_ENSLAVEMENT'))
						# Weitere Basics
						lTechs.append(gc.getInfoTypeForString('TECH_TEMPELWIRTSCHAFT'))
						lTechs.append(gc.getInfoTypeForString('TECH_BLASEBALG'))
						lTechs.append(gc.getInfoTypeForString('TECH_MEDICINE2'))
						lTechs.append(gc.getInfoTypeForString('TECH_CODEX'))
						lTechs.append(gc.getInfoTypeForString('TECH_MASONRY2'))
						lTechs.append(gc.getInfoTypeForString('TECH_SCHMIEDEKUNST'))

						# Streitwagen
						if pPlayer.countOwnedBonuses(gc.getInfoTypeForString('BONUS_HORSE')) > 0:
								lTechs.append(gc.getInfoTypeForString('TECH_THE_WHEEL3'))

						lTechs.append(gc.getInfoTypeForString('TECH_SOELDNERTUM'))

						# Griechen
						if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GREEK')):
								lTechs.append(gc.getInfoTypeForString('TECH_ASTROLOGIE'))
								lTechs.append(gc.getInfoTypeForString('TECH_RELIGION_GREEK'))

						lTechs.append(gc.getInfoTypeForString('TECH_ARCHERY2'))

						# Perser
						if iCiv == gc.getInfoTypeForString('CIVILIZATION_PERSIA') or iCiv == gc.getInfoTypeForString('CIVILIZATION_ASSYRIA'):
								lTechs.append(gc.getInfoTypeForString('TECH_ASTROLOGIE'))
								lTechs.append(gc.getInfoTypeForString('TECH_DUALISMUS'))

						# Streitaxt
						lTechs.append(gc.getInfoTypeForString('TECH_BEWAFFNUNG2'))

						# Schiffsbau
						if pPlayer.countNumCoastalCities() > 0:
								lTechs.append(gc.getInfoTypeForString('TECH_SCHIFFSBAU'))

						# Religionen
						lTechs.append(gc.getInfoTypeForString('TECH_ASTROLOGIE'))
						lTechs.append(gc.getInfoTypeForString('TECH_MANTIK'))
						lTechs.append(gc.getInfoTypeForString('TECH_RELIGION_CELTIC'))
						lTechs.append(gc.getInfoTypeForString('TECH_RELIGION_NORDIC'))
						lTechs.append(gc.getInfoTypeForString('TECH_HEILIGER_ORT'))
						lTechs.append(gc.getInfoTypeForString('TECH_RELIGION_PHOEN'))

						# Bessere Waffen
						lTechs.append(gc.getInfoTypeForString('TECH_BRANDSCHATZEN'))
						lTechs.append(gc.getInfoTypeForString('TECH_BEWAFFNUNG3'))
						lTechs.append(gc.getInfoTypeForString('TECH_ARCHERY3'))
						# Basics
						lTechs.append(gc.getInfoTypeForString('TECH_DEFENCES'))
						lTechs.append(gc.getInfoTypeForString('TECH_IRRIGATION'))
						lTechs.append(gc.getInfoTypeForString('TECH_AGRICULTURE2'))

						# Eisenverarbeitung
						lTechs.append(gc.getInfoTypeForString('TECH_IRON_WORKING'))

				# Dies kommt ganz unten nochmal vor
				if len(lTechs):
					for iTech in lTechs:
						if not pTeam.isHasTech(iTech):
							if pPlayer.canResearch(iTech, False):
								return iTech

				# Ab nun freie Entscheidung der KI (bis auf Ausnahmen)

				# --- Eisenzeit ---

				# Judentum
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_ISRAEL'):
						if not pTeam.isHasTech(gc.getInfoTypeForString('TECH_MONOTHEISM')):
								if pTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
										iTech = gc.getInfoTypeForString('TECH_BELAGERUNG')
										if not pTeam.isHasTech(iTech) and pPlayer.canResearch(iTech, False):
												return iTech
										iTech = gc.getInfoTypeForString('TECH_BUCHSTABEN')
										if not pTeam.isHasTech(iTech) and pPlayer.canResearch(iTech, False):
												return iTech
										iTech = gc.getInfoTypeForString('TECH_THEOKRATIE')
										if not pTeam.isHasTech(iTech) and pPlayer.canResearch(iTech, False):
												return iTech
										iTech = gc.getInfoTypeForString('TECH_ALPHABET')
										if not pTeam.isHasTech(iTech) and pPlayer.canResearch(iTech, False):
												return iTech
										iTech = gc.getInfoTypeForString('TECH_MONOTHEISM')
										if not pTeam.isHasTech(iTech) and pPlayer.canResearch(iTech, False):
												return iTech

				# Kriegstechs
				if pTeam.getAtWarCount(True) >= 1:
						lTechs.append(gc.getInfoTypeForString('TECH_BELAGERUNG'))
						lTechs.append(gc.getInfoTypeForString('TECH_TORSION'))

				# Camels / Kamele
				if pPlayer.getNumAvailableBonuses(iCamel) > 0:
						lTechs.append(gc.getInfoTypeForString('TECH_KAMELZUCHT'))

				# Eledome
				if pPlayer.getNumAvailableBonuses(iCamel) > 0:
						lTechs.append(gc.getInfoTypeForString('TECH_ELEFANTENZUCHT'))

				# Seefahrt
				if pPlayer.countNumCoastalCities() > 3:
						lTechs.append(gc.getInfoTypeForString('TECH_COLONIZATION2'))
						lTechs.append(gc.getInfoTypeForString('TECH_RUDERER2'))
						lTechs.append(gc.getInfoTypeForString('TECH_HANDELSSCHIFFE'))
						lTechs.append(gc.getInfoTypeForString('TECH_RUDERER3'))
						lTechs.append(gc.getInfoTypeForString('TECH_KARTOGRAPHIE'))
						lTechs.append(gc.getInfoTypeForString('TECH_KARTEN'))
						lTechs.append(gc.getInfoTypeForString('TECH_HELLENISMUS'))
						lTechs.append(gc.getInfoTypeForString('TECH_KUESTE'))

				# Geldwesen
				lTechs.append(gc.getInfoTypeForString('TECH_MUENZEN'))
				lTechs.append(gc.getInfoTypeForString('TECH_CURRENCY'))
				lTechs.append(gc.getInfoTypeForString('TECH_BANKWESEN'))

				# Heroen
				lTechs.append(gc.getInfoTypeForString('TECH_GLADIATOR'))

				# Wissen
				lTechs.append(gc.getInfoTypeForString('TECH_LIBRARY'))

				# Wunder
				# Mauern von Babylon
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_BABYLON'):
						lTechs.append(gc.getInfoTypeForString('TECH_CONSTRUCTION'))
				# Artemistempel
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_LYDIA'):
						lTechs.append(gc.getInfoTypeForString('TECH_BAUKUNST'))
				# Ninive
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_ASSYRIA'):
						lTechs.append(gc.getInfoTypeForString('TECH_CONSTRUCTION'))
						lTechs.append(gc.getInfoTypeForString('TECH_PHILOSOPHY'))
				# 1000 Saeulen
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_PERSIA'):
						lTechs.append(gc.getInfoTypeForString('TECH_KUNST'))
						lTechs.append(gc.getInfoTypeForString('TECH_MOSAIK'))

				# CIV - Trennung: zB Religionen
				# Buddhismus
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_INDIA'):
						lTechs.append(gc.getInfoTypeForString('TECH_MEDITATION'))
						lTechs.append(gc.getInfoTypeForString('TECH_ASKESE'))

				# Roman Gods
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_ROME'):
						lTechs.append(gc.getInfoTypeForString('TECH_THEOKRATIE'))
						lTechs.append(gc.getInfoTypeForString('TECH_RELIGION_ROME'))

				# Voelkerspezifisches Wissen
				# Perser
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_PERSIA'):
						lTechs.append(gc.getInfoTypeForString('TECH_PERSIAN_ROAD'))

				# Griechen
				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_GREEK')):
						lTechs.append(gc.getInfoTypeForString('TECH_ARMOR'))
						lTechs.append(gc.getInfoTypeForString('TECH_PHALANX'))


				# Roemer
				if pTeam.isHasTech(gc.getInfoTypeForString('TECH_ROMAN')):
						lTechs.append(gc.getInfoTypeForString('TECH_CORVUS'))
						lTechs.append(gc.getInfoTypeForString('TECH_MANIPEL'))
						lTechs.append(gc.getInfoTypeForString('TECH_PILUM'))
						lTechs.append(gc.getInfoTypeForString('TECH_MARIAN_REFORM'))
						lTechs.append(gc.getInfoTypeForString('TECH_CALENDAR2'))
						lTechs.append(gc.getInfoTypeForString('TECH_ROMAN_ROADS'))
						lTechs.append(gc.getInfoTypeForString('TECH_FEUERWEHR'))
						lTechs.append(gc.getInfoTypeForString('TECH_LORICA_SEGMENTATA'))


				if len(lTechs):
					for iTech in lTechs:
						if not pTeam.isHasTech(iTech):
							if pPlayer.canResearch(iTech, False):
								return iTech

				return TechTypes.NO_TECH

		def AI_chooseProduction(self, argsList):
				pCity = argsList[0]
				iOwner = pCity.getOwner()
				# Barbs ausgeschlossen
				if iOwner == gc.getBARBARIAN_PLAYER():
						return False

				pPlayer = gc.getPlayer(iOwner)
				eCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
				pTeam = gc.getTeam(pPlayer.getTeam())

				# AI soll sofort Palast bauen, wenn baubar
				# if pPlayer.getCapitalCity().getID() == -1:
				#pCapital = pPlayer.getCapitalCity()
				# if pCapital is None or pCapital.isNone():
				#    iBuilding = gc.getInfoTypeForString("BUILDING_PALACE")
				#    iBuilding = eCiv.getCivilizationBuildings(iBuilding)
				#    if pCity.canConstruct(iBuilding, 0, 0, 0):
				#        bDoIt = True
				#        # Stadtproduktionen durchgehen
				#        (loopCity, pIter) = pPlayer.firstCity(False)
				#        while loopCity:
				#            if loopCity.getProductionBuilding() == iBuilding:
				#                bDoIt = False
				#                break
				#            (loopCity, pIter) = pPlayer.nextCity(pIter, False)
				#        if bDoIt:
				#            pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT, iBuilding, -1, False, False, False, True)
				#            return True

				# Projects
				bDoIt = True
				# Stadtproduktionen durchgehen
				(loopCity, pIter) = pPlayer.firstCity(False)
				while loopCity:
						if loopCity.isProductionProject():
								bDoIt = False
								break
						(loopCity, pIter) = pPlayer.nextCity(pIter, False)
				if bDoIt:
						iProject = -1
						# Seidenstrasse: wenn Zugang zu Seide
						iProjectX = gc.getInfoTypeForString("PROJECT_SILKROAD")
						if pCity.canCreate(iProjectX, 0, 0) and not pCity.isProductionProject():
								iBonus = gc.getInfoTypeForString("BONUS_SILK")
								if pCity.hasBonus(iBonus):
										iProject = iProjectX
								elif pTeam.isHasTech(gc.getInfoTypeForString("TECH_DEFENCES")):
										iProject = iProjectX

						# Antonius Kloster: wenn die Staatsreligion das Christentum ist
						iProjectX = gc.getInfoTypeForString("PROJECT_ANTONIUS_KLOSTER")
						if pCity.canCreate(iProjectX, 0, 0) and not pCity.isProductionProject():
								iReligion = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
								if pPlayer.getStateReligion() == iReligion:
										iProject = iProjectX

						# Akasha Chronik
						iProjectX = gc.getInfoTypeForString("PROJECT_AKASHA_CHRONIK")
						if pCity.canCreate(iProjectX, 0, 0) and not pCity.isProductionProject():
								iReligion = gc.getInfoTypeForString("RELIGION_HINDUISM")
								if pPlayer.getStateReligion() == iReligion:
										iProject = iProjectX

						# Olympische Spiele
						iProjectX = gc.getInfoTypeForString("PROJECT_OLYMPIC_GAMES")
						if pCity.canCreate(iProjectX, 0, 0) and not pCity.isProductionProject():
								iReligion = gc.getInfoTypeForString("RELIGION_GREEK")
								if pPlayer.getStateReligion() == iReligion:
										iProject = iProjectX

						# Projekt in Auftrag geben
						if iProject != -1:
								pCity.pushOrder(OrderTypes.ORDER_CREATE, iProject, -1, False, False, True, False)
								return True

				# Einheitenproduktion -----------
				# Aber erst ab Pop 5
				if pCity.getPopulation() > 4:
						# Bei Goldknappheit, Haendler in Auftrag geben (50%)
						if pCity.getPopulation() > 5:
								if pPlayer.getGold() < 500:
										if pPlayer.calculateGoldRate() < 5:
												if CvUtil.myRandom(2, "ai_build_merchant") == 1:
														iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_TRADE_MERCHANTMAN"))
														if pCity.canTrain(iUnit, 0, 0):
																pCity.pushOrder(OrderTypes.ORDER_TRAIN, iUnit, -1, False, False, True, False)
																return True
														iUnit = eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_TRADE_MERCHANT"))
														if pCity.canTrain(iUnit, 0, 0):
																pArea = pCity.area()
																if pArea.getNumCities() > 1:
																		if pArea.getNumTiles() > pArea.getNumOwnedTiles() * 2:
																				pCity.pushOrder(OrderTypes.ORDER_TRAIN, iUnit, -1, False, False, True, False)
																				return True

						# Sonstige spezielle Einheiten
						iRand = CvUtil.myRandom(10, "ai_build_div")
						# Chance of 20%
						if iRand < 2:
								lUnit = []
								# Inselstadt soll nur Handelsschiffe bauen
								Plots = 0
								for i in range(3):
										for j in range(3):
												loopPlot = gc.getMap().plot(pCity.getX() + i - 1, pCity.getY() + j - 1)
												if loopPlot is not None and not loopPlot.isNone():
														if not loopPlot.isWater():
																Plots = Plots + 1
								if Plots < 7:
										lUnit.append(eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_CARVEL_TRADE")))
										lUnit.append(eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_TRADE_MERCHANTMAN")))
								else:
										if pPlayer.isStateReligion():
												lUnit.append(eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_INQUISITOR")))
										lUnit.extend([
												eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_TRADE_MERCHANT")),
												eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_TRADE_MERCHANTMAN")),
												eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SUPPLY_WAGON")),
												eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_CARAVAN"))
										])
										if pCity.getPopulation() > 5:
												lUnit.append(eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_HORSE")))
										lUnit.append(eCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SUPPLY_FOOD")))

								# Unit already exists
								bUnit = False
								for iUnit in lUnit:
										if pCity.canTrain(iUnit, 0, 0):
												# if there is a Unit, don't Build one
												(pUnit, pIter) = pPlayer.firstUnit(False)
												while pUnit:
														if pUnit.getUnitType() == iUnit:
																bUnit = True
																break
														(pUnit, pIter) = pPlayer.nextUnit(pIter, False)
												if not bUnit:
														# Stadtproduktion durchgehen
														(loopCity, pIter) = pPlayer.firstCity(False)
														while loopCity:
																if not loopCity.isNone() and loopCity.getOwner() == iOwner:  # only valid cities
																		if loopCity.isProductionUnit():
																				if loopCity.getUnitProduction(iUnit):
																						bUnit = True
																						break
																(loopCity, pIter) = pPlayer.nextCity(pIter, False)
														# Auf zur Produktion
														if not bUnit:
																pCity.pushOrder(OrderTypes.ORDER_TRAIN, iUnit, -1, False, False, True, False)
																return True
				return False

		# global
		def AI_unitUpdate(self, argsList):
				pUnit = argsList[0]
				iOwner = pUnit.getOwner()
				pOwner = gc.getPlayer(iOwner)
				pTeam = gc.getTeam(pOwner.getTeam())
				# eCiv = gc.getCivilizationInfo(pOwner.getCivilizationType())
				iBarbarianPlayer = gc.getBARBARIAN_PLAYER()
				pPlot = pUnit.plot()

				if not pOwner.isHuman():
						iUnitType = pUnit.getUnitType()
						lCities = PyPlayer(iOwner).getCityList()

						# PAE AI Unit Instances (better turn time)
						if self.PAE_AI_ID != iOwner:
								#self.PAE_AI_ID = iOwner
								self.PAE_AI_Cities_Slaves = []
								self.PAE_AI_Cities_Slavemarket = []


						# Hunter (771): Lager oder Beobachtungsturm
						if iUnitType == gc.getInfoTypeForString("UNIT_HUNTER"):
								# Lager / Camp
								#if pTeam.isHasTech(gc.getInfoTypeForString("TECH_HUNTING")):
								#		if pPlot.getOwner() == pUnit.getOwner() and pPlot.getImprovementType() == -1:
								#				if pPlot.isCultureRangeCity(iOwner, 2) and pPlot.getFeatureType() in L.LForests:
								#						pPlot.setImprovementType(gc.getInfoTypeForString("IMPROVEMENT_CAMP"))
								#						pUnit.finishMoves()
								#						return True
								# Beobachtungsturm / Spähturm / Look-out
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_HOLZWEHRANLAGEN")):
										if pPlot.isHills() and pPlot.getImprovementType() == -1 and pPlot.getBonusType(-1) == -1 and not pPlot.isCity():
												if pPlot.getOwner() == -1 or pPlot.getOwner() == pUnit.getOwner() and not pPlot.isCultureRangeCity(iOwner, 2):
														# Check, ob im Umkreis Türme sind
														bTurm = False
														eTurm = gc.getInfoTypeForString("IMPROVEMENT_TURM")
														iRange = 3
														iX = pPlot.getX()
														iY = pPlot.getY()
														for i in range(-iRange, iRange+1):
																for j in range(-iRange, iRange+1):
																		loopPlot = plotXY(iX, iY, i, j)
																		if loopPlot is not None and not loopPlot.isNone():
																				if loopPlot.getImprovementType() == eTurm:
																						bTurm = True
																						break
																if bTurm: break

														if not bTurm:
																pPlot.setImprovementType(eTurm)
																pUnit.finishMoves()
																return True

						# Worker (771): Schürflager
						#if iUnitType == gc.getInfoTypeForString("UNIT_WORKER"):
						#		if not pTeam.isHasTech(gc.getInfoTypeForString("TECH_MINING")):
						#				if pTeam.isHasTech(gc.getInfoTypeForString("TECH_METAL_SMELTING")):
						#						if pPlot.getOwner() == pUnit.getOwner():
						#								iLager = gc.getInfoTypeForString("IMPROVEMENT_ORE_CAMP")
						#								eBonus = pPlot.getBonusType(iOwner)
						#								if eBonus != -1 and gc.getImprovementInfo(iLager).isImprovementBonusMakesValid(eBonus): #and pPlot.getImprovementType() != iLager
						#										pPlot.setImprovementType(iLager)
						#										pUnit.finishMoves()
						#										return True


						# Barbs -------------------------
						if iUnitType == gc.getInfoTypeForString("UNIT_TREIBGUT"):
								# CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("TreibgutAI",)), None, 2, None, ColorTypes(11), pUnit.getX(), pUnit.getY(), False, False)
								PAE_Unit.move2nextPlot(pUnit, True)
								pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, True, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
								return True
						elif iUnitType == gc.getInfoTypeForString("UNIT_STRANDGUT"):
								# CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_TEST", ("StrandgutAI",)), None, 2, None, ColorTypes(11), pUnit.getX(), pUnit.getY(), False, False)
								if CvUtil.myRandom(20, "entferne_Strandgut") < 2:
										pUnit.kill(True, -1)
								else:
										pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, True, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
								return True
						elif iUnitType == gc.getInfoTypeForString("UNIT_SEEVOLK"):  # and pUnit.plot().isCity():
								if pUnit.canUnloadAll() and pUnit.plot().getOwner() != -1 or not pUnit.hasCargo():
										pUnit.doCommand(CommandTypes.COMMAND_UNLOAD_ALL, 0, 0)
										pUnit.kill(True, -1)

						if iOwner == iBarbarianPlayer:
								# Barbs vom FortDefence
								iPromo = gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS")  # Moves -1
								iPromo2 = gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS2")  # Moves -2
								if pUnit.getUnitAIType() == UnitAITypes.UNITAI_CITY_DEFENSE or pUnit.isHasPromotion(iPromo) or pUnit.isHasPromotion(iPromo2):
										if pUnit.plot().isCity() or pUnit.plot().getImprovementType() in L.LImprFortShort:
												pUnit.getGroup().pushMission(MissionTypes.MISSION_FORTIFY, 0, 0, 0, True, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
												return True
										else:
												pUnit.setUnitAIType(UnitAITypes.UNITAI_ATTACK)
												pUnit.setHasPromotion(iPromo, False)
												pUnit.setHasPromotion(iPromo2, False)

								# Barbarische Emigranten stehen nur rum und benoetigen unnoetig Rechenzeit
								elif pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_EMIGRANT"):
										pUnit.kill(True, -1)
										return True
								# Barbarische befreite Sklaven stehen nur rum und benoetigen unnoetig Rechenzeit
								elif pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_FREED_SLAVE"):
										pUnit.kill(True, -1)
										return True
								# Barbarische Haendler sind unnoetig
								elif pUnit.getUnitType() in L.LTradeUnits:
										pUnit.kill(True, -1)
										return True
								# Barbarische Tiere sollen keine Stadt betreten / Barbarian animals will be disbanded when moving into a city
								elif pUnit.getUnitAIType() == UnitAITypes.UNITAI_ANIMAL:
										if pPlot.isCity() or pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_DARK_ICE"):
												pUnit.kill(True, -1)
												return True

								# ab hier mit BarbUnits raus aus der kompletten Funktion AI_unitUpdate
								return False
						# -------------------------------

						# Inquisitor
						if iUnitType in L.LInquisitors:
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("AI Inquisitor",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
								if self.doInquisitorCore_AI(pUnit):
										return True

						# Freed slaves
						elif iUnitType == gc.getInfoTypeForString("UNIT_FREED_SLAVE"):
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("AI Freed Slave",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
								if self._doSettleFreedSlaves_AI(pUnit):
										return True

						# UNITAI_MISSIONARY = 14
						elif pUnit.getUnitAIType() == 14:
								self.doAIMissionReligion(pUnit)

						# Elefant (Zucht/Elefantenstall)
						# if iUnitType == gc.getInfoTypeForString("UNIT_ELEFANT"):
						#    #CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("AI Elefant",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
						#    if pTeam.isHasTech(gc.getInfoTypeForString("TECH_ELEFANTENZUCHT")):
						#        #if self.doElefant_AI(pUnit):
						#        if self.doSpreadStrategicBonus_AI(pUnit, gc.getInfoTypeForString("BUILDING_ELEPHANT_STABLE"), gc.getInfoTypeForString("BONUS_IVORY")):
						#            return True

						# Kamel (Zucht/Kamellager)
						elif iUnitType == gc.getInfoTypeForString("UNIT_CAMEL"):
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("AI Camel",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KAMELZUCHT")):
										if self.doSpreadStrategicBonus_AI(pUnit, gc.getInfoTypeForString("BUILDING_CAMEL_STABLE"), gc.getInfoTypeForString("BONUS_CAMEL")):
												return True

						# Great Prophet makes Capital to Holy City (769)
						elif iUnitType == gc.getInfoTypeForString("UNIT_PROPHET"):
								pCapital = pOwner.getCapitalCity()
								iReligions = gc.getNumReligionInfos()
								for iReligion in range(iReligions):
										if iReligion in L.LRelisRemapCapital:
												if gc.getGame().isReligionFounded(iReligion):
														pHolyCity = gc.getGame().getHolyCity(iReligion)
														if not pHolyCity.isNone() and pHolyCity.getID() == pCapital.getID(): 
																continue
														else:
																# Es darf auch dann die Heilige Stadt gesetzt werden, wenn sie zB zerstört wurde
																if pCapital.isHasReligion(iReligion) and (pHolyCity.isNone() or pHolyCity.getOwner() == iOwner):
																		gc.getGame().setHolyCity(iReligion, pCapital, 0)
																		
																		for iPlayer in range(gc.getMAX_PLAYERS()):
																				if not gc.getPlayer(iPlayer).isNone() and gc.getPlayer(iPlayer).isHuman():
																						CyInterface().addMessage(iPlayer, True, 10,
																							CyTranslator().getText("TXT_KEY_MESSAGE_GREAT_PROPHET_HOLY_CITY", (pCapital.getName(),gc.getReligionInfo(iReligion).getDescription())),
																							"AS2D_WELOVEKING", 2, "Art/Interface/Buttons/Actions/button_action_holycity.dds", ColorTypes(13), pCapital.getX(), pCapital.getY(), True, True)
																		
																		pUnit.kill(True, -1)
																		return True

						# Trade and cultivation (Boggy). First, try cultivation. If unsuccessfull, try trade.
						# if pUnit.getUnitAIType() ==
						# gc.getInfoTypeForString("UNITAI_MERCHANT") and iUnitType != gc.getInfoTypeForString("UNIT_MERCHANT"):
						if iUnitType in L.LCultivationUnits:
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "CultivationUnit: " + pOwner.getName(), None, 2, None, ColorTypes(5), 0, 0, False, False)
								if PAE_Cultivation.doCultivation_AI(pUnit):
										#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Python AI Cultivation",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
										return True

								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "CultivationUnit: False", None, 2, None, ColorTypes(5), 0, 0, False, False)
								if iUnitType != gc.getInfoTypeForString("UNIT_WORKBOAT") and not pUnit.plot().isCity():
										pCity = PAE_Unit.getNearestCity(pUnit)
										if pCity != None:
												pUnit.getGroup().pushMoveToMission(pCity.getX(), pCity.getY())
												return True
										pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, True, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
										return True

								if pOwner.getUnitClassCount(pUnit.getUnitClassType()) > 3:
										pOwner.changeGold(25)
										pUnit.kill(True, -1)
										return True


						if iUnitType in L.LTradeUnits:

								# Debug
								# if iOwner != 0: return True
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "TradeUnit: " + pOwner.getName() + u"(%d)" % pOwner.getGold(), None, 2, None, ColorTypes(5), 0, 0, False, False)

								if pOwner.getUnitClassCount(pUnit.getUnitClassType()) > 9:
										pOwner.changeGold(25)
										pUnit.kill(True, -1)
										return True

								# Handelsschiffe tauchen in Inlandsstädten auf
								if not pPlot.isCoastalLand() and pUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
										pOwner.changeGold(25)
										pUnit.kill(True, -1)
										return True


								# if pUnit.getGroup().getLengthMissionQueue() > 0: return True
								# if PAE_Trade.doAutomateMerchant(pUnit):
								#    if iOwner == 12: CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "AI doAutomateMerchant", None, 2, None, ColorTypes(10), 0, 0, False, False)
								#    return True
								# elif PAE_Trade.doAssignTradeRoute_AI(pUnit):
								#    if iOwner == 12: CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "AI doAssignTradeRoute_AI", None, 2, None, ColorTypes(10), 0, 0, False, False)
								#    # try again
								#    if PAE_Trade.doAutomateMerchant(pUnit):
								#        if iOwner == 12: CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "AI automate merchant new trade route", None, 2, None, ColorTypes(10), 0, 0, False, False)
								#        return True

								bTradeRouteActive = int(CvUtil.getScriptData(pUnit, ["autA", "t"], 0))
								if bTradeRouteActive:
										PAE_Trade.doAutomateMerchant(pUnit)
										return True
								elif not PAE_Trade.doAssignTradeRoute_AI(pUnit):
										pOwner.changeGold(25)
										pUnit.kill(True, -1)  # RAMK_CTD
										return True

								if pUnit.getDamage() > 0:
										pUnit.getGroup().pushMission(MissionTypes.MISSION_HEAL, 0, 0, 0, True, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
								#pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, True, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
								return False

						# Supply waggon
						if iUnitType == gc.getInfoTypeForString("UNIT_SUPPLY_FOOD"):
								# Option: Stadt mit Nahrung versorgen
								pCity = PAE_Unit.getNearestCity(pUnit)
								if pCity != None and not pCity.isNone():
										pUnit.getGroup().pushMoveToMission(pCity.getX(), pCity.getY())
										if pUnit.getX() == pCity.getX() and pUnit.getY() == pCity.getY():
												pCity.changeFood(PAE_Unit.getUnitSupplyFood())
												pUnit.kill(True, -1)  # RAMK_CTD
										return True

						iCivType = pUnit.getCivilizationType()

						# PAE Veterans und Rank Unit Promo Features

						# PAE 6.5 Katapult -> Feuerkatapult
						if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_ACCURACY3")):
								if pUnit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_CATAPULT"):
										PAE_Unit.doUpgradeVeteran(pUnit, gc.getInfoTypeForString("UNIT_FIRE_CATAPULT"), True)
										return True

						# Unit Rang Promo -------
						if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT4")):
								# LEGION zu Praetorians
								if iUnitType in L.LUnits4Praetorians:
										if not pTeam.isHasTech(gc.getInfoTypeForString("TECH_GRENZHEER")):
												if pOwner.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_PRAETORIAN")) == 0:
														if pOwner.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_LEGION_TRIBUN")):
																if (pOwner.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_LEGION_CENTURIO")) or 
																		pOwner.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_LEGION_CENTURIO2")) ):
																		if (pOwner.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_LEGION_OPTIO")) or
																				pOwner.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_LEGION_OPTIO2")) ):
																				iNewUnit = gc.getInfoTypeForString("UNIT_PRAETORIAN")
																				PAE_Unit.doUpgradeVeteran(pUnit, iNewUnit, True)
																				return True
						# KI: immer und kostenlos
						iNewUnit = PAE_Unit.canUpgradeUnit(pUnit)
						if iNewUnit != -1: # and CvUtil.getScriptData(pUnit, ["P", "t"]) == "RangPromoUp":
								if PAE_Unit.doUpgradeRang(iOwner, pUnit.getID()):
										return True

						# Legion Kastell
						# KI: immer, aber mit Kosten
						# nie hoeher als Tribun/General
						# Romans/Etruscans only
						if iCivType == gc.getInfoTypeForString("CIVILIZATION_ROME") or iCivType == gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"):
								if (pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_1")) and not
										pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_15"))
										or
										pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_1")) and not
										pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_10"))
										):

										# Kostet 25, aber wegen Reserve
										if pOwner.getGold() > 50:
												PAE_Unit.doKastell(iOwner, pUnit.getID())
												return True

						# Terrain Promos - Ausbildner / Trainer (in City)
						lTrainerPromotions = [
								gc.getInfoTypeForString("PROMOTION_WOODSMAN5"),
								gc.getInfoTypeForString("PROMOTION_GUERILLA5"),
								gc.getInfoTypeForString("PROMOTION_JUNGLE5"),
								gc.getInfoTypeForString("PROMOTION_SUMPF5"),
								gc.getInfoTypeForString("PROMOTION_DESERT5"),
								gc.getInfoTypeForString("PROMOTION_CITY_RAIDER5"),
								gc.getInfoTypeForString("PROMOTION_CITY_GARRISON5"),
								gc.getInfoTypeForString("PROMOTION_PILLAGE5"),
								gc.getInfoTypeForString("PROMOTION_NAVIGATION4")
						]
						for iPromo in lTrainerPromotions:
								if pUnit.isHasPromotion(iPromo):
										if self._AI_SettleTrainer(pUnit):
												# wenn die Einheit per AISettleTrainer gekillt wurde, dann raus hier
												return True

						# BEGIN Unit -> Horse UPGRADE
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_HORSEBACK_RIDING_2")):
								if iUnitType in L.LUnitAuxiliar or iUnitType == gc.getInfoTypeForString("UNIT_FOEDERATI"):

										bSearchPlot = False

										if iUnitType in L.LUnitAuxiliar:
												iNewUnitType = gc.getInfoTypeForString("UNIT_AUXILIAR_HORSE")
												bSearchPlot = True
										elif iUnitType == gc.getInfoTypeForString("UNIT_FOEDERATI"):
												if pTeam.isHasTech(gc.getInfoTypeForString("TECH_HUFEISEN")):
														iNewUnitType = gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN")
														bSearchPlot = True

										# Pferd suchen
										if bSearchPlot:
												UnitHorse = gc.getInfoTypeForString("UNIT_HORSE")
												iRange = pPlot.getNumUnits()
												for i in range(iRange):
														pLoopUnit = pPlot.getUnit(i)
														if pLoopUnit.getUnitType() == UnitHorse and pLoopUnit.getOwner() == iOwner:
																# Create a new unit
																NewUnit = pOwner.initUnit(iNewUnitType, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
																PAE_Unit.initUnitFromUnit(pUnit, NewUnit)
																NewUnit.setDamage(pUnit.getDamage(), -1)
																NewUnit.changeMoves(90)
																# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																pUnit.kill(True, -1)  # RAMK_CTD
																pLoopUnit.kill(False, -1)  # andere Einheit direkt toeten, siehe isSuicide im CombatResult
																return True
						# END Unit -> Horse UPGRADE

						# Slaves settle into city
						if iUnitType == gc.getInfoTypeForString("UNIT_SLAVE"):
								if pPlot.isCity() and pPlot.getOwner() == iOwner:
										pCity = pPlot.getPlotCity()
										if not pCity.isNone() and pCity.getID() not in self.PAE_AI_Cities_Slaves:
												eSpecialistGlad = gc.getInfoTypeForString("SPECIALIST_GLADIATOR")
												eSpecialistHouse = gc.getInfoTypeForString("SPECIALIST_SLAVE")
												eSpecialistFood = gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD")
												eSpecialistProd = gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD")
												iCityPop = pCity.getPopulation()
												iCityGlads = pCity.getFreeSpecialistCount(eSpecialistGlad)
												iCitySlaves = pCity.getFreeSpecialistCount(eSpecialistHouse)
												iCitySlavesFood = pCity.getFreeSpecialistCount(eSpecialistFood)
												iCitySlavesProd = pCity.getFreeSpecialistCount(eSpecialistProd)

												# Zuerst Sklavenmarkt bauen
												bSlaveMarket = False
												iBuilding1 = gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")
												iBuilding2 = gc.getInfoTypeForString("BUILDING_STADT")
												if pCity.isHasBuilding(iBuilding1):
														bSlaveMarket = True
												elif pCity.isHasBuilding(iBuilding2):
														pCity.setNumRealBuilding(iBuilding1, 1)
														# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1) # RAMK_CTD
														pUnit.kill(True, -1)
														return True

												# Weitere Cities auf Sklavenmarkt checken und Sklaven zuerst dort hinschicken
												if len(lCities) > len(self.PAE_AI_Cities_Slavemarket):
														if CvUtil.myRandom(10, "ai_sklavenmarkt") < 2:
																(loopCity, pIter) = pOwner.firstCity(False)
																while loopCity:
																		if loopCity.getID() not in self.PAE_AI_Cities_Slavemarket:
																				# PAE AI City Instance
																				self.PAE_AI_Cities_Slavemarket.append(loopCity.getID())
																				if not loopCity.isHasBuilding(iBuilding1):
																						if loopCity.isHasBuilding(iBuilding2):
																								pUnit.getGroup().pushMoveToMission(loopCity.getX(), loopCity.getY())
																								return True
																		(loopCity, pIter) = pOwner.nextCity(pIter, False)

												iCitySlavesAll = iCitySlaves + iCitySlavesFood + iCitySlavesProd

												## TEST ##
												#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("AI Slave",iCitySlavesAll)), None, 2, None, ColorTypes(10), 0, 0, False, False)

												bHasGladTech = False
												iNumGlads = 0
												if pTeam.isHasTech(gc.getInfoTypeForString("TECH_GLADIATOR")):
														bHasGladTech = True
														# Gladidatorenplatz reservieren fuer Glads aber nur ab Pop 6
														if iCityPop > 5:
																iNumGlads = 3

												# settle as slaves
												if pCity.happyLevel() > iCitySlavesAll:
														if iCitySlavesAll + iCityGlads + iNumGlads < iCityPop:
																if iCitySlavesFood == 0:
																		pCity.changeFreeSpecialistCount(eSpecialistFood, 1)
																elif iCitySlavesProd == 0:
																		pCity.changeFreeSpecialistCount(eSpecialistProd, 1)
																elif iCitySlavesFood < iCitySlavesProd or iCitySlavesFood < iCitySlaves:
																		pCity.changeFreeSpecialistCount(eSpecialistFood, 1)
																elif iCitySlavesProd < iCitySlavesFood or iCitySlavesProd < iCitySlaves:
																		pCity.changeFreeSpecialistCount(eSpecialistProd, 1)
																else:
																		pCity.changeFreeSpecialistCount(eSpecialistHouse, 1)

																# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																pUnit.kill(True, -1)  # RAMK_CTD
																return True

														# settle as gladiators
														if bHasGladTech:
																if iCitySlavesAll + iCityGlads <= iCityPop:
																		pCity.changeFreeSpecialistCount(eSpecialistGlad, 1)
																		# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																		pUnit.kill(True, -1)  # RAMK_CTD
																		return True

												# Priority 1 - Schule

												# assign to school
												iBuilding1 = gc.getInfoTypeForString('BUILDING_SCHULE')
												if pCity.isHasBuilding(iBuilding1):
														iCulture = pCity.getBuildingCommerceByBuilding(CommerceTypes.COMMERCE_RESEARCH, iBuilding1)
														if iCulture < 10:
																iNewCulture = iCulture + 2
																pCity.setBuildingCommerceChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), CommerceTypes.COMMERCE_RESEARCH, iNewCulture)
																# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																pUnit.kill(True, -1)  # RAMK_CTD
																return True

												# assign to library
												iBuilding1 = gc.getInfoTypeForString('BUILDING_LIBRARY')
												if pCity.isHasBuilding(iBuilding1):
														iCulture = pCity.getBuildingCommerceByBuilding(CommerceTypes.COMMERCE_RESEARCH, iBuilding1)
														if iCulture < 10:
																iNewCulture = iCulture + 2
																pCity.setBuildingCommerceChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), CommerceTypes.COMMERCE_RESEARCH, iNewCulture)
																# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																pUnit.kill(True, -1)  # RAMK_CTD
																return True

												# Priority 2a - Brotmanufaktur
												# assign to bread manufactory
												iBuilding1 = gc.getInfoTypeForString('BUILDING_BROTMANUFAKTUR')
												if pCity.isHasBuilding(iBuilding1):
														iFood = pCity.getBuildingYieldChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), YieldTypes.YIELD_FOOD)
														if iFood < 3:
																iFood += 1
																pCity.setBuildingYieldChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), YieldTypes.YIELD_FOOD, iFood)
																# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																pUnit.kill(True, -1)  # RAMK_CTD
																return True

												# Priority 2b - Manufaktur
												# assign to manufactory
												iBuilding1 = gc.getInfoTypeForString('BUILDING_CORP3')
												if pCity.isHasBuilding(iBuilding1):
														#iFood = pCity.getBuildingYieldChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), YieldTypes.YIELD_FOOD)
														iProd = pCity.getBuildingYieldChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), YieldTypes.YIELD_PRODUCTION)
														if iProd < 5:  # and iProd <= iFood:
																iProd += 1
																pCity.setBuildingYieldChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), YieldTypes.YIELD_PRODUCTION, iProd)
																# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																pUnit.kill(True, -1)  # RAMK_CTD
																return True
														# elif iFood < 5:
														#    iFood += 1
														#    pCity.setBuildingYieldChange(gc.getBuildingInfo(iBuilding1).getBuildingClassType(), YieldTypes.YIELD_FOOD, iFood)
														#    # pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
														#    pUnit.kill(True, -1)  # RAMK_CTD
														#    return True

												# Priority 3 - Bordell
												# assign to the house of pleasure (bordell/freudenhaus)
												if PAE_Sklaven.doSlave2Bordell(pCity, pUnit):
														return True

												# Priority 4 - Theater
												# assign to the theatre
												if PAE_Sklaven.doSlave2Theatre(pCity, pUnit):
														return True

												# Priority 5 - Palace
												# assign to the Palace  10%
												if CvUtil.myRandom(10, "assign_slave_palace") == 1:
														if PAE_Sklaven.doSlave2Palace(pCity, pUnit):
																return True

												# Priority 6 - Temples
												# assign to a temple 10%
												if CvUtil.myRandom(10, "assign_slave_temple") == 1:
														if PAE_Sklaven.doSlave2Temple(pCity, pUnit):
																return True

												# Priority 7 - Feuerwehr
												# assign to the fire station 10%
												if CvUtil.myRandom(10, "assign_slave_temple") == 1:
														if PAE_Sklaven.doSlave2Feuerwehr(pCity, pUnit):
																return True

												# Priority 8 - Sell slave 25%
												if bSlaveMarket:
														if CvUtil.myRandom(4, "ai_sell_slave") == 1:
																pUnit.getGroup().pushMission(MissionTypes.MISSION_TRADE, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pPlot, pUnit)
																return True

												# PAE AI City Instance
												self.PAE_AI_Cities_Slaves.append(pCity.getID())

												# Sklaven sicherheitshalber in die Hauptstadt schicken
												pCapital = pOwner.getCapitalCity()
												if pCapital.getID() != -1 and pPlot.getArea() == pCapital.area().getID():
														if pCapital is not None and not pCapital.isNone():
																if not pUnit.atPlot(pCapital.plot()):
																		pUnit.getGroup().pushMoveToMission(pCapital.getX(), pCapital.getY())
																		return True

								# end: if pPlot.isCity

								# Slave -> Villages (secondary)
								LImpUpgrade = []
								for i in L.LVillages:
										if pOwner.getImprovementCount(i) > 0:
												LImpUpgrade = L.LVillages
												break

								# Slave -> Latifundium (primary)
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_RESERVISTEN")):
										for i in L.LLatifundien:
												if pOwner.getImprovementCount(i) > 0:
														LImpUpgrade = L.LLatifundien
														break

								if LImpUpgrade:
										for i in xrange(CyMap().numPlots()):
												pLoopPlot = CyMap().sPlotByIndex(i)
												if pLoopPlot.getOwner() == iOwner:
														iImp = pLoopPlot.getImprovementType()
														if iImp in LImpUpgrade:
																if pLoopPlot.getUpgradeTimeLeft(iImp, iOwner) > 1:
																		if iImp in L.LVillages:
																				pLoopPlot.changeUpgradeProgress(10)
																		else:
																				PAE_Sklaven.doUpgradeLatifundium(pLoopPlot)
																		pUnit.kill(True, -1)
																		return True

						# Horses - create stables
						elif iUnitType == gc.getInfoTypeForString("UNIT_HORSE"):
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_PFERDEZUCHT")):

										if self.doSpreadStrategicBonus_AI(pUnit, gc.getInfoTypeForString("BUILDING_STABLE"), gc.getInfoTypeForString("BONUS_HORSE")):
												return True

										if pPlot.isCity() and pPlot.getOwner() == iOwner:

												# Pferd verkaufen
												if pUnit.getGroup().getLengthMissionQueue() == 0 and pOwner.getUnitClassCount(pUnit.getUnitClassType()) > 2:
														pOwner.changeGold(25)
														pUnit.kill(True, -1)
														return True

										# auf zur naechsten Stadt
										else:
												pCity = PAE_Unit.getNearestCity(pUnit)
												if pCity != None:
														pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pCity.getX(), pCity.getY(), 1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
														return True

						# Auswanderer / Emigrant
						elif iUnitType == gc.getInfoTypeForString("UNIT_EMIGRANT"):

								# Auswanderer sollen Gemeinden bauen
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_HEILKUNDE")):
										LImpUpgradePlot = None
										iDistance = 999
										for i in xrange(CyMap().numPlots()):
												pLoopPlot = CyMap().sPlotByIndex(i)
												if pLoopPlot.getOwner() == iOwner:
														iImp = pLoopPlot.getImprovementType()
														if iImp == gc.getInfoTypeForString("IMPROVEMENT_VILLAGE"):
														
																iDistanceCheck = CyMap().calculatePathDistance(pUnit.plot(), pLoopPlot)
																if iDistanceCheck != -1 and iDistanceCheck < iDistance:
																		iDistance = iDistanceCheck
																		LImpUpgradePlot = pLoopPlot

										if LImpUpgradePlot != None:
												if LImpUpgradePlot.getX() == pUnit.getX() and LImpUpgradePlot.getY() == pUnit.getY():
														LImpUpgradePlot.setImprovementType(gc.getInfoTypeForString("IMPROVEMENT_TOWN"))
														pUnit.kill(True, -1)
														return True
												else:
														pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, LImpUpgradePlot.getX(), LImpUpgradePlot.getY(), 1, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)

								# zu schwachen Staedten
								if pPlot.isCity() and pPlot.getOwner() == iOwner:

										lCityX = None
										iCityPop = 0
										for lCity in lCities:
												iPop = lCity.getPopulation()
												if lCityX is None or iPop < iCityPop:
														iCityPop = iPop
														lCityX = lCity

										if lCityX:
												if not pUnit.atPlot(lCityX.plot()) and pUnit.generatePath(lCityX.plot(), 0, False, None):  # generatePath returns True, if a path was found.
														pUnit.getGroup().pushMoveToMission(lCityX.getX(), lCityX.getY())
												else:
														lCityX.changePopulation(1)
														# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
														pUnit.kill(True, -1)  # RAMK_CTD
												return True

						# Beutegold / Treasure / Goldkarren -> zur Hauptstadt oder zur naechst gelegenen Stadt (Insel)
						elif iUnitType == gc.getInfoTypeForString("UNIT_GOLDKARREN"):

								if pUnit.getGroup().getLengthMissionQueue() == 0:

										if pOwner.getNumCities() > 0:

												if pPlot.isCity():
														pCity = pPlot.getPlotCity()
														if pCity.isCapital() or pCity.isGovernmentCenter():
																iGold = 50 + CvUtil.myRandom(50, "ai_beutegold")  # KI Bonus (HI: 10 + x)
																pOwner.changeGold(iGold)
																# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																pUnit.kill(True, -1)  # RAMK_CTD
																return True
														else:
																bAccess = PAE_Unit.move2GovCenter(pUnit)
																# bAccess = true: wenn eine Stadt angepeilt wurde
																# bAccess = false: wenn die Einheit in einer Stadt steht aber der Weg abgeschnitten ist bzw nicht möglich ist
																if not bAccess:
																		# 1:20, dass das Gold auch ohne Hauptstadt/Provinzhauptstadt in die Kassa kommt
																		if CvUtil.myRandom(20, "do_ai_beutegold") == 1:
																				iGold = 50 + CvUtil.myRandom(30, "ai_beutegold")  # KI Bonus dafür weniger als oben
																				pOwner.changeGold(iGold)
																				# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																				pUnit.kill(True, -1)  # RAMK_CTD
																				return True
												else:
														PAE_Unit.move2GovCenter(pUnit)
														#pCity = PAE_Unit.getNearestCity(pUnit)
														# if pCity != None:
														#    pUnit.getGroup().pushMoveToMission(pCity.getX(), pCity.getY())

								return False

						# Trojanisches Pferd
						elif iUnitType == gc.getInfoTypeForString("UNIT_TROJAN_HORSE"):
								# 1: wenn das pferd in der naehe einer feindlichen stadt ist und diese ueber 100% defense hat -> anwenden

								iX = pUnit.getX()
								iY = pUnit.getY()

								for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
										loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
										if loopPlot is not None and not loopPlot.isNone():
												if loopPlot.isCity():
														loopCity = loopPlot.getPlotCity()
														if loopCity.getOwner() != pUnit.getOwner():
																if gc.getTeam(gc.getPlayer(pUnit.getOwner()).getTeam()).isAtWar(gc.getPlayer(loopCity.getOwner()).getTeam()):
																		iDamage = loopCity.getDefenseModifier(0)
																		if iDamage > 100:
																				loopCity.changeDefenseDamage(iDamage)
																				# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																				pUnit.kill(True, -1)  # RAMK_CTD
																				return True

						# Gladiator und Gladiatorenschule
						elif iUnitType == gc.getInfoTypeForString("UNIT_GLADIATOR") and not pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MERCENARY")):
								# nur wenn die Einheit im eigenen Terrain ist (und nicht im Kriegsgebiet)
								if pPlot.getOwner() == iOwner:
										if not pTeam.isHasTech(gc.getInfoTypeForString("TECH_KONZIL5")) and pTeam.isHasTech(gc.getInfoTypeForString("TECH_GLADIATOR2")):
												iBuilding1 = gc.getInfoTypeForString("BUILDING_STADT")
												iBuilding2 = gc.getInfoTypeForString("BUILDING_GLADIATORENSCHULE")
												(loopCity, pIter) = pOwner.firstCity(False)
												while loopCity:
														if not loopCity.isNone():
																if loopCity.isHasBuilding(iBuilding1) and not loopCity.isHasBuilding(iBuilding2):
																		loopCity.setNumRealBuilding(iBuilding2, 1)
																		pUnit.kill(True, -1)
																		return True
														(loopCity, pIter) = pOwner.nextCity(pIter, False)
						# -----------------

						# Legend can become a Great General
						if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT6")):
								if not pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
										if pPlot.getOwner() == iOwner:
												pNewUnit = CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_GREAT_GENERAL"), pUnit.plot(), pOwner)
												GG_Name = PAE_Unit.getGGName(pOwner)
												if GG_Name != "":
														pNewUnit.setName(GG_Name)
												lPromos = [
														gc.getInfoTypeForString("PROMOTION_COMBAT6"),
														gc.getInfoTypeForString("PROMOTION_COMBAT5"),
														gc.getInfoTypeForString("PROMOTION_COMBAT4"),
														gc.getInfoTypeForString("PROMOTION_COMBAT3"),
														gc.getInfoTypeForString("PROMOTION_COMBAT2"),
														gc.getInfoTypeForString("PROMOTION_HERO")
												]
												for iPromo in lPromos:
														if pUnit.isHasPromotion(iPromo):
																pUnit.setHasPromotion(iPromo, False)
												# Reduce XP
												pUnit.setExperience(pUnit.getExperience() / 2, -1)

												# if pUnit.getLevel() > 3:
												#  pUnit.setLevel(pUnit.getLevel() - 3)
												# else:
												#  pUnit.setLevel(1)
						# -----------------

						# Moral kann von Rhetorik Helden oder Leader vergeben werden
						iPromo = gc.getInfoTypeForString("PROMOTION_RHETORIK")
						if pUnit.isHasPromotion(iPromo):
								# nur phasenweise machen
								if CvUtil.myRandom(5, "AI_doChanceGiveMoralePromo") == 1:
										PAE_Unit.doMoralUnits(pUnit, 1)

						# Druide soll Sklaven opfern
						if iUnitType == gc.getInfoTypeForString("UNIT_DRUIDE"):
								# Checken, ob es Einheiten ohne Moral gibt und ob sich ein Sklave auf dem Plot befindet
								bSlaves = False
								bMorale = False
								iUnitSlave = gc.getInfoTypeForString("UNIT_SLAVE")
								iPromo = gc.getInfoTypeForString("PROMOTION_MORALE")

								for iUnit in range(pPlot.getNumUnits()):
										loopUnit = pPlot.getUnit(iUnit)
										if loopUnit.getOwner() == iOwner:
												if loopUnit.getUnitType() == iUnitSlave:
														bSlaves = True
												if loopUnit.isMilitaryHappiness():
														if not loopUnit.isHasPromotion(iPromo):
																if pUnit.getID() != loopUnit.getID():
																		bMorale = True

										if bSlaves and bMorale:
												PAE_Unit.doMoralUnits(pUnit, 2)
												PAE_Unit.doKillSlaveFromPlot(pUnit)
												pUnit.finishMoves()
												return True

						# Kaufbare Promotions ------------------

						# In einer Stadt
						if pPlot.isCity():
								pCity = pPlot.getPlotCity()

								# Kauf einer edlen Ruestung (Promotion)
								if pTeam.isHasTech(gc.getInfoTypeForString("TECH_ARMOR")):
										iPromo = gc.getInfoTypeForString("PROMOTION_EDLE_RUESTUNG")
										iPromoPrereq = gc.getInfoTypeForString("PROMOTION_COMBAT5")
										if not pUnit.isHasPromotion(iPromo) and pUnit.isHasPromotion(iPromoPrereq):
												if pUnit.getUnitCombatType() not in L.LCombatNoRuestung:
														# Removed 'is not None' check getUnitCombatType() never returns None
														if pUnit.getUnitType() not in L.LUnitNoRuestung:
																iBuilding = gc.getInfoTypeForString("BUILDING_FORGE_WEAPONS")
																bonus1 = gc.getInfoTypeForString("BONUS_OREICHALKOS")
																bonus2 = gc.getInfoTypeForString("BONUS_MESSING")
																if pCity.isHasBuilding(iBuilding) and (pCity.hasBonus(bonus1) or pCity.hasBonus(bonus2)):
																		iCost = gc.getUnitInfo(pUnit.getUnitType()).getCombat() * 12
																		if iCost <= 0:
																				iCost = 180
																		if pOwner.getGold() > iCost * 3:
																				# AI soll zu 25% die Ruestung kaufen
																				if CvUtil.myRandom(4, "ai_ruestung") == 1:
																						pOwner.changeGold(-iCost)
																						pUnit.setHasPromotion(iPromo, True)
																						pUnit.finishMoves()
																						return True

								# Schiffe
								if pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_NAVAL"):
										# Kauf eines Wellen-Oils (Promotion)
										if pTeam.isHasTech(gc.getInfoTypeForString("TECH_KUESTE")):
												bonus1 = gc.getInfoTypeForString("BONUS_OLIVES")
												iPromo = gc.getInfoTypeForString("PROMOTION_OIL_ON_WATER")
												iPromo2 = gc.getInfoTypeForString("PROMOTION_COMBAT2")

												if not pUnit.isHasPromotion(iPromo) and pUnit.isHasPromotion(iPromo2) and pCity.hasBonus(bonus1):
														iCost = int(PyInfo.UnitInfo(pUnit.getUnitType()).getProductionCost() / 2)
														if iCost <= 0:
																iCost = 80
														if pOwner.getGold() > iCost:
																pOwner.changeGold(-iCost)
																pUnit.setHasPromotion(iPromo, True)
																pUnit.finishMoves()
																return True
										# Mit Magnetkompass ausrüsten (Promotion)
										if pTeam.isHasTech(gc.getInfoTypeForString("TECH_MAGNETISM")):
												bonus1 = gc.getInfoTypeForString("BONUS_MAGNETIT")
												iPromo = gc.getInfoTypeForString("PROMOTION_KOMPASS")

												if not pUnit.isHasPromotion(iPromo) and pCity.hasBonus(bonus1):
														iCost = 20
														if pOwner.getGold() > iCost:
																pOwner.changeGold(-iCost)
																pUnit.setHasPromotion(iPromo, True)
																pUnit.finishMoves()
																return True
										# Schiff reparieren
										if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_WERFT")):
												iCost = pUnit.getDamage()
												if pOwner.getGold() > iCost + 200:
														if CvUtil.myRandom(2, "AI_Ship_Repair") == 1:
																pOwner.changeGold(-iCost)
																pUnit.setDamage(0, -1)
																pUnit.finishMoves()
																return True

								# Bless units (PAE V Patch 4)
								if pUnit.isMilitaryHappiness():
										iCost = 50  # 50% for HI
										if pOwner.getGold() > iCost:
												iPromo = gc.getInfoTypeForString("PROMOTION_BLESSED")
												if not pUnit.isHasPromotion(iPromo):
														iBuilding1 = gc.getInfoTypeForString("BUILDING_CHRISTIAN_CATHEDRAL")
														iBuilding2 = gc.getInfoTypeForString("BUILDING_HAGIA_SOPHIA")
														if pCity.isHasBuilding(iBuilding1) or pCity.isHasBuilding(iBuilding2):
																pOwner.changeGold(-iCost)
																pUnit.setHasPromotion(iPromo, True)
																pUnit.finishMoves()
																return True

								# Escorte
								if iUnitType in L.LTradeUnits and pUnit.getDomainType() == DomainTypes.DOMAIN_LAND:
										iPromo == gc.getInfoTypeForString("PROMOTION_SCHUTZ")
										if not pUnit.isHasPromotion(iPromo):
												iCost = 20
												if pOwner.isCivic(gc.getInfoTypeForString("CIVIC_SOELDNERTUM")):
														iCost = 15
												if pOwner.getGold() > iCost:
														pUnit.setHasPromotion(iPromo, True)
														pUnit.finishMoves()
														return True

								# General oder Rhetoriker
								if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RHETORIK")) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
										if pCity.getOccupationTimer() > 0:
												pCity.setOccupationTimer(0)
										elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")):
												pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR"), 0)

						# in einer Stadt
						else:
								# ausserhalb einer Stadt

								# LEADER
								if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
										# Wald niederbrennen
										if pPlot.getOwner() != -1:
												if pPlot.getFeatureType() in L.LForests:
														if gc.getTeam(gc.getPlayer(pPlot.getOwner()).getTeam()).isAtWar(pUnit.getTeam()):
																if CvUtil.myRandom(4, "AI_Leader_BurnDownTheForest") == 1:
																		PAE_Unit.doBurnDownForest(pUnit)
																		return True


						# Governor / Statthalter
						# if pUnit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_STATTHALTER"):
						#    PAE_Unit.doStatthalterTurn_AI(pUnit)
						#    return True

				return False

		def AI_doWar(self, argsList):
				# eTeam = argsList[0]
				return False

		def AI_doDiplo(self, argsList):
				# ePlayer = argsList[0]
				return False

		def calculateScore(self, argsList):
				ePlayer = argsList[0]
				bFinal = argsList[1]
				bVictory = argsList[2]

				iPopulationScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getPopScore(), gc.getGame().getInitPopulation(
				), gc.getGame().getMaxPopulation(), gc.getDefineINT("SCORE_POPULATION_FACTOR"), True, bFinal, bVictory)
				iLandScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getLandScore(), gc.getGame().getInitLand(), gc.getGame().getMaxLand(), gc.getDefineINT("SCORE_LAND_FACTOR"), True, bFinal, bVictory)
				iTechScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getTechScore(), gc.getGame().getInitTech(), gc.getGame().getMaxTech(), gc.getDefineINT("SCORE_TECH_FACTOR"), True, bFinal, bVictory)
				iWondersScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getWondersScore(), gc.getGame().getInitWonders(),
																								 gc.getGame().getMaxWonders(), gc.getDefineINT("SCORE_WONDER_FACTOR"), False, bFinal, bVictory)
				return int(iPopulationScore + iLandScore + iWondersScore + iTechScore)

		def doHolyCity(self):
				# Reli-Gruendungsfehler rausfiltern
				iTech = gc.getInfoTypeForString("TECH_LIBERALISM")
				bTech = False
				iRange = gc.getMAX_PLAYERS()
				for i in range(iRange):
						pTeam = gc.getTeam(gc.getPlayer(i).getTeam())
						if pTeam.isHasTech(iTech):
								bTech = True
								break

				if not bTech:
						return True
				return False

		def doHolyCityTech(self, argsList):
				# eTeam = argsList[0]
				# ePlayer = argsList[1]
				# eTech = argsList[2]
				# bFirst = argsList[3]
				return False

		def doGold(self, argsList):
				# ePlayer = argsList[0]
				return False

		def doResearch(self, argsList):
				# ePlayer = argsList[0]
				return False

		def doGoody(self, argsList):
				# ePlayer = argsList[0]
				# pPlot = argsList[1]
				# pUnit = argsList[2]
				return False

		def doGrowth(self, argsList):
				# pCity = argsList[0]
				return False

		def doProduction(self, argsList):
				# pCity = argsList[0]
				return False

		def doCulture(self, argsList):
				# pCity = argsList[0]
				return False

		def doPlotCulture(self, argsList):
				# pCity = argsList[0]
				# bUpdate = argsList[1]
				# ePlayer = argsList[2]
				# iCultureRate = argsList[3]
				return False

		def doReligion(self, argsList):
				# pCity = argsList[0]
				return False

		def cannotSpreadReligion(self, argsList):
				iOwner, iUnitID, iReligion, iX, iY = argsList[0]
				return False

		def doGreatPeople(self, argsList):
				# pCity = argsList[0]
				return False

		def doMeltdown(self, argsList):
				# pCity = argsList[0]
				return False

		def doReviveActivePlayer(self, argsList):
				"allows you to perform an action after an AIAutoPlay"
				# iPlayer = argsList[0]
				return False

		def doPillageGold(self, argsList):
				"controls the gold result of pillaging"
				pPlot = argsList[0]
				pUnit = argsList[1]

				iPillageGold = 0
				iPillageGold = CvUtil.myRandom(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "ai_pillage_gold_1")
				iPillageGold += CvUtil.myRandom(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "ai_pillage_gold_2")

				iPillageGold += (pUnit.getPillageChange() * iPillageGold) / 100

				return iPillageGold

		def doCityCaptureGold(self, argsList):
				"controls the gold result of capturing a city"

				pOldCity = argsList[0]

				iCaptureGold = 0

				iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
				iCaptureGold += (pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION"))
				iCaptureGold += CvUtil.myRandom(gc.getDefineINT("CAPTURE_GOLD_RAND1"), "ai_capture_gold_1")
				iCaptureGold += CvUtil.myRandom(gc.getDefineINT("CAPTURE_GOLD_RAND2"), "ai_capture_gold_2")

				if gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0:
						iCaptureGold *= min(max(gc.getGame().getGameTurn() - pOldCity.getGameTurnAcquired(), 0), gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"))
						iCaptureGold /= gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")

				return iCaptureGold

		def citiesDestroyFeatures(self, argsList):
				iX, iY = argsList
				return True

		def canFoundCitiesOnWater(self, argsList):
				iX, iY = argsList
				return False

		def doCombat(self, argsList):
				pSelectionGroup, pDestPlot = argsList
				return False

		def getConscriptUnitType(self, argsList):
				# iPlayer = argsList[0]
				iConscriptUnitType = -1  # return this with the value of the UNIT TYPE you want to be conscripted, -1 uses default system

				return iConscriptUnitType

		def getCityFoundValue(self, argsList):
				iPlayer, iPlotX, iPlotY = argsList
				iFoundValue = -1  # Any value besides -1 will be used

				return iFoundValue

		def canPickPlot(self, argsList):
				# pPlot = argsList[0]
				return True

		def getUnitCostMod(self, argsList):
				iPlayer, iUnit = argsList
				iCostMod = -1  # Any value > 0 will be used

				if iPlayer != -1:
						pPlayer = gc.getPlayer(iPlayer)

						# Nomads (TEST)
						# if pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_HUNNEN"): return 0

						# Trait Aggressive: Einheiten 20% billiger / units 20% cheaper
						if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_AGGRESSIVE")) and gc.getUnitInfo(iUnit).isMilitaryHappiness():
								iCostMod = 80

				return iCostMod

		def getBuildingCostMod(self, argsList):
				iPlayer, iCityID, iBuilding = argsList
				pBuildingClass = gc.getBuildingClassInfo(gc.getBuildingInfo(iBuilding).getBuildingClassType())

				iCostMod = -1  # Any value > 0 will be used
				# Trait Builder/Bauherr: buildings 15% cheaper, wonders 25%
				if iPlayer != -1:
						pPlayer = gc.getPlayer(iPlayer)
						#pCity = pPlayer.getCity(iCityID)
						if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_INDUSTRIOUS")):
								if pBuildingClass.getMaxGlobalInstances() == -1 and pBuildingClass.getMaxTeamInstances() == -1 and pBuildingClass.getMaxPlayerInstances() == -1:
										iCostMod = 85
								else:
										iCostMod = 75
				# --
				return iCostMod

		def canUpgradeAnywhere(self, argsList):
				# pUnit = argsList

				bCanUpgradeAnywhere = 0

				return bCanUpgradeAnywhere

		def getWidgetHelp(self, argsList):
				eWidgetType, iData1, iData2, bOption = argsList
				
				# PB Mod
				if iData1 == 302016:
						return localText.getText("TXT_KEY_MOD_UNPAUSE_DESC", ())
				if iData1 == 47292:
						if iData2 == 1:
								return localText.getText("TXT_KEY_MOD_F9_DESELECT_OPPONENTS", ())
						if iData2 == 2:
								return localText.getText("TXT_KEY_MOD_F9_SELECT_ALL", ())
						if iData2 == 3:
								return localText.getText("TXT_KEY_MOD_F9_SELECT_BY_F4", ())

## ---------------------- ##
##   Platy WorldBuilder   ##
## ---------------------- ##
## Religion Screen ##
				if eWidgetType == WidgetTypes.WIDGET_HELP_RELIGION:
						if iData1 == -1:
								return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
## Mouse Over Civ Score List ##
				elif eWidgetType == WidgetTypes.WIDGET_CONTACT_CIV:
						pPlayer = gc.getPlayer(iData1)
						iTeam = pPlayer.getTeam()
						pTeam = gc.getTeam(iTeam)
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_CITY_STATE")):
								return CyTranslator().getText("[NEWLINE]", ()) + u" %c " % CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR) + CyTranslator().getText("TXT_KEY_TECH_CITY_STATE", ()).upper()
## Platy WorldBuilder ##
				elif eWidgetType == WidgetTypes.WIDGET_PYTHON:
						if iData1 == 1027:
								return CyTranslator().getText("TXT_KEY_WB_PLOT_DATA", ())
						elif iData1 == 1028:
								return gc.getGameOptionInfo(iData2).getHelp()
						elif iData1 == 1029:
								if iData2 == 0:
										sText = CyTranslator().getText("TXT_KEY_WB_PYTHON", ())
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onFirstContact"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onChangeWar"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onVassalState"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityAcquired"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityBuilt"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCultureExpansion"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGoldenAge"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onEndGoldenAge"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGreatPersonBorn"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlayerChangeStateReligion"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionFounded"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionSpread"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionRemove"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationFounded"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationSpread"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationRemove"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitCreated"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitLost"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitPromoted"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onBuildingBuilt"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onProjectBuilt"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onTechAcquired"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementBuilt"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementDestroyed"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onRouteBuilt"
										sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlotRevealed"
										return sText
								elif iData2 == 1:
										return CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ())
								elif iData2 == 2:
										return CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ())
								elif iData2 == 3:
										return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ())
								elif iData2 == 4:
										return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ())
								elif iData2 == 5:
										return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ())
								elif iData2 == 6:
										return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ())
								elif iData2 == 7:
										return CyTranslator().getText("TXT_KEY_WB_CITY_DATA2", ())
								elif iData2 == 8:
										return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ())
								elif iData2 == 9:
										return "Platy Builder\nVersion: 4.10"
								elif iData2 == 10:
										return CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS", ())
								elif iData2 == 11:
										return CyTranslator().getText("TXT_KEY_WB_RIVER_PLACEMENT", ())
								elif iData2 == 12:
										return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ())
								elif iData2 == 13:
										return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ())
								elif iData2 == 14:
										return CyTranslator().getText("TXT_KEY_WB_PLOT_TYPE", ())
								elif iData2 == 15:
										return CyTranslator().getText("TXT_KEY_CONCEPT_TERRAIN", ())
								elif iData2 == 16:
										return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_ROUTE", ())
								elif iData2 == 17:
										return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ())
								elif iData2 == 18:
										return CyTranslator().getText("TXT_KEY_MISSION_BUILD_CITY", ())
								elif iData2 == 19:
										return CyTranslator().getText("TXT_KEY_WB_ADD_BUILDINGS", ())
								elif iData2 == 20:
										return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ())
								elif iData2 == 21:
										return CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS", ())
								elif iData2 == 22:
										return CyTranslator().getText("TXT_KEY_ESPIONAGE_CULTURE", ())
								elif iData2 == 23:
										return CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS", ())
								elif iData2 == 24:
										return CyTranslator().getText("TXT_KEY_WB_SENSIBILITY", ())
								elif iData2 == 27:
										return CyTranslator().getText("TXT_KEY_WB_ADD_UNITS", ())
								elif iData2 == 28:
										return CyTranslator().getText("TXT_KEY_WB_TERRITORY", ())
								elif iData2 == 29:
										return CyTranslator().getText("TXT_KEY_WB_ERASE_ALL_PLOTS", ())
								elif iData2 == 30:
										return CyTranslator().getText("TXT_KEY_WB_REPEATABLE", ())
								elif iData2 == 31:
										return CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ())
								elif iData2 == 32:
										return CyTranslator().getText("TXT_KEY_WB_STARTING_PLOT", ())
								elif iData2 == 33:
										return CyTranslator().getText("TXT_KEY_INFO_SCREEN", ())
								elif iData2 == 34:
										return CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ())
								elif iData2 == 35:
										return CyTranslator().getText("TXT_KEY_WB_RIVER_FORD", ())
								elif iData2 == 36:
										return CyTranslator().getText("TXT_KEY_WB_RIVER_AUTOMATIC", ())
								elif iData2 == 37:
										return CyTranslator().getText("TXT_KEY_WB_RIVER_BRANCH", ())
								elif iData2 == 38:
										return CyTranslator().getText("TXT_KEY_WB_RIVER_COMPLETE", ())
						elif iData1 > 1029 and iData1 < 1040:
								if iData1 % 2:
										return "-"
								return "+"
						elif iData1 == 6782:
								return CyGameTextMgr().parseCorporationInfo(iData2, False)
						elif iData1 == 6785:
								return CyGameTextMgr().getProjectHelp(iData2, False, CyCity())
						elif iData1 == 6787:
								return gc.getProcessInfo(iData2).getDescription()
						elif iData1 == 6788:
								if iData2 == -1:
										return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
								return gc.getRouteInfo(iData2).getDescription()
## City Hover Text ##
						elif iData1 > 7199 and iData1 < 7300:
								iPlayer = iData1 - 7200
								pPlayer = gc.getPlayer(iPlayer)
								pCity = pPlayer.getCity(iData2)
								if CyGame().GetWorldBuilderMode():
										sText = "<font=3>"
										if pCity.isCapital():
												sText += CyTranslator().getText("[ICON_STAR]", ())
										elif pCity.isGovernmentCenter():
												sText += CyTranslator().getText("[ICON_SILVER_STAR]", ())
										sText += u"%s: %d<font=2>" % (pCity.getName(), pCity.getPopulation())
										sTemp = ""
										if pCity.isConnectedToCapital(iPlayer):
												sTemp += CyTranslator().getText("[ICON_TRADE]", ())
										for i in range(gc.getNumReligionInfos()):
												if pCity.isHolyCityByType(i):
														sTemp += u"%c" % (gc.getReligionInfo(i).getHolyCityChar())
												elif pCity.isHasReligion(i):
														sTemp += u"%c" % (gc.getReligionInfo(i).getChar())

										for i in range(gc.getNumCorporationInfos()):
												if pCity.isHeadquartersByType(i):
														sTemp += u"%c" % (gc.getCorporationInfo(i).getHeadquarterChar())
												elif pCity.isHasCorporation(i):
														sTemp += u"%c" % (gc.getCorporationInfo(i).getChar())
										if sTemp:
												sText += "\n" + sTemp

										iMaxDefense = pCity.getTotalDefense(False)
										if iMaxDefense > 0:
												sText += u"\n%s: " % (CyTranslator().getText("[ICON_DEFENSE]", ()))
												iCurrent = pCity.getDefenseModifier(False)
												if iCurrent != iMaxDefense:
														sText += u"%d/" % (iCurrent)
												sText += u"%d%%" % (iMaxDefense)

										sText += u"\n%s: %d/%d" % (CyTranslator().getText("[ICON_FOOD]", ()), pCity.getFood(), pCity.growthThreshold())
										iFoodGrowth = pCity.foodDifference(True)
										if iFoodGrowth != 0:
												sText += u" %+d" % (iFoodGrowth)

										if pCity.isProduction():
												sText += u"\n%s:" % (CyTranslator().getText("[ICON_PRODUCTION]", ()))
												if not pCity.isProductionProcess():
														sText += u" %d/%d" % (pCity.getProduction(), pCity.getProductionNeeded())
														iProduction = pCity.getCurrentProductionDifference(False, True)
														if iProduction != 0:
																sText += u" %+d" % (iProduction)
												sText += u" (%s)" % (pCity.getProductionName())

										iGPRate = pCity.getGreatPeopleRate()
										iProgress = pCity.getGreatPeopleProgress()
										if iGPRate > 0 or iProgress > 0:
												sText += u"\n%s: %d/%d %+d" % (CyTranslator().getText("[ICON_GREATPEOPLE]", ()), iProgress, pPlayer.greatPeopleThreshold(False), iGPRate)

										sText += u"\n%s: %d/%d (%s)" % (CyTranslator().getText("[ICON_CULTURE]", ()), pCity.getCulture(iPlayer),
																										pCity.getCultureThreshold(), gc.getCultureLevelInfo(pCity.getCultureLevel()).getDescription())

										lTemp = []
										for i in range(CommerceTypes.NUM_COMMERCE_TYPES):
												iAmount = pCity.getCommerceRateTimes100(i)
												if iAmount <= 0:
														continue
												sTemp = u"%d.%02d%c" % (pCity.getCommerceRate(i), pCity.getCommerceRateTimes100(i) % 100, gc.getCommerceInfo(i).getChar())
												lTemp.append(sTemp)
										if lTemp:
												sText += "\n"
												sText += ', '.join([lT for lT in lTemp])

										iMaintenance = pCity.getMaintenanceTimes100()
										if iMaintenance != 0:
												sText += "\n" + CyTranslator().getText("[COLOR_WARNING_TEXT]", ()) + CyTranslator().getText("INTERFACE_CITY_MAINTENANCE", ()) + " </color>"
												sText += u"-%d.%02d%c" % (iMaintenance/100, iMaintenance % 100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

										lBuildings = []
										lWonders = []
										for i in range(gc.getNumBuildingInfos()):
												if pCity.isHasBuilding(i):
														Info = gc.getBuildingInfo(i)
														if isLimitedWonderClass(Info.getBuildingClassType()):
																lWonders.append(Info.getDescription())
														else:
																lBuildings.append(Info.getDescription())
										if lBuildings:
												lBuildings.sort()
												sText += "\n" + CyTranslator().getText("[COLOR_BUILDING_TEXT]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()) + ": </color>"
												sText += ', '.join([lB for lB in lBuildings])

										if lWonders:
												lWonders.sort()
												sText += "\n" + CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()) + ": </color>"
												sText += ', '.join([lW for lW in lWonders])

										sText += "</font>"
										return sText
						## Religion Widget Text##
						elif iData1 == 7869:
								return CyGameTextMgr().parseReligionInfo(iData2, False)
						## Building Widget Text##
						elif iData1 == 7870:
								return CyGameTextMgr().getBuildingHelp(iData2, False, False, False, None)
						## Tech Widget Text##
						elif iData1 == 7871:
								if iData2 == -1:
										return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
								return CyGameTextMgr().getTechHelp(iData2, False, False, False, False, -1)
						## Civilization Widget Text##
						elif iData1 == 7872:
								iCiv = iData2 % 10000
								return CyGameTextMgr().parseCivInfos(iCiv, False)
						## Promotion Widget Text##
						elif iData1 == 7873:
								return CyGameTextMgr().getPromotionHelp(iData2, False)
						## Feature Widget Text##
						elif iData1 == 7874:
								if iData2 == -1:
										return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
								iFeature = iData2 % 10000
								return CyGameTextMgr().getFeatureHelp(iFeature, False)
						## Terrain Widget Text##
						elif iData1 == 7875:
								return CyGameTextMgr().getTerrainHelp(iData2, False)
						## Leader Widget Text##
						elif iData1 == 7876:
								iLeader = iData2 % 10000
								return CyGameTextMgr().parseLeaderTraits(iLeader, -1, False, False)
						## Improvement Widget Text##
						elif iData1 == 7877:
								if iData2 == -1:
										return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
								return CyGameTextMgr().getImprovementHelp(iData2, False)
						## Bonus Widget Text##
						elif iData1 == 7878:
								if iData2 == -1:
										return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
								return CyGameTextMgr().getBonusHelp(iData2, False)
						## Specialist Widget Text##
						elif iData1 == 7879:
								return CyGameTextMgr().getSpecialistHelp(iData2, False)
						## Yield Text##
						elif iData1 == 7880:
								return gc.getYieldInfo(iData2).getDescription()
						## Commerce Text##
						elif iData1 == 7881:
								return gc.getCommerceInfo(iData2).getDescription()
						## Corporation Screen ##
						elif iData1 == 8201:
								return CyGameTextMgr().parseCorporationInfo(iData2, False)
						## Military Screen ##
						elif iData1 == 8202:
								if iData2 == -1:
										return CyTranslator().getText("TXT_KEY_PEDIA_ALL_UNITS", ())
								return CyGameTextMgr().getUnitHelp(iData2, False, False, False, None)
						elif iData1 > 8299 and iData1 < 8400:
								iPlayer = iData1 - 8300
								pUnit = gc.getPlayer(iPlayer).getUnit(iData2)
								sText = CyGameTextMgr().getSpecificUnitHelp(pUnit, True, False)
								if CyGame().GetWorldBuilderMode():
										sText += "\n" + CyTranslator().getText("TXT_KEY_WB_UNIT", ()) + " ID: " + str(iData2)
										sText += "\n" + CyTranslator().getText("TXT_KEY_WB_GROUP", ()) + " ID: " + str(pUnit.getGroupID())
										sText += "\n" + "X: " + str(pUnit.getX()) + ", Y: " + str(pUnit.getY())
										sText += "\n" + CyTranslator().getText("TXT_KEY_WB_AREA_ID", ()) + ": " + str(pUnit.plot().getArea())
								return sText
						## Civics Screen ##
						elif iData1 == 8205 or iData1 == 8206:
								sText = CyGameTextMgr().parseCivicInfo(iData2, False, True, False)
								if gc.getCivicInfo(iData2).getUpkeep() > -1:
										sText += "\n" + gc.getUpkeepInfo(gc.getCivicInfo(iData2).getUpkeep()).getDescription()
								else:
										sText += "\n" + CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
								return sText
## River Feature Widget Text##
						elif iData1 == 8999:
								return CyTranslator().getText("TXT_KEY_WB_RIVER_DATA", ())
						elif iData1 in [9000, 9001]:
								if iData2 == -1:
										return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())

								# iFeatureRiver = CvUtil.findInfoTypeNum(
										# gc.getFeatureInfo,
										# gc.getNumFeatureInfos(),
										# 'FEATURE_RIVER')
								# return CyGameTextMgr().getFeatureHelp(iFeatureRiver, False)

								#if iData2 in [1000, 1001]:
								#		sText = CyTranslator().getText(CvRiverUtil.RiverKeymap["EMPTY"], ())
								#		if iData2 == 1001:
								#				sText += "\n" + CyTranslator().getText("TXT_KEY_WITH_RIVER_FORD", ())
								#		return sText
								#iRow = 0
								#for rtype in CvRiverUtil.RiverTypes:
								#		for align in CvRiverUtil.RiverTypes[rtype]:
								#				if iRow == iData2:
								#						sText = CyTranslator().getText(CvRiverUtil.RiverKeymap[rtype+"_"+align], ())
								#						if iData1 == 9001:
								#								sText += "\n" + CyTranslator().getText("TXT_KEY_WITH_RIVER_FORD", ())
								#						return sText
								#				iRow += 1
						elif iData1 in [9010, 9020, 9030, 9040, 9050, 9060, 9070]:
								return " "  # Returning of empty string would be problematic..
## ---------------------- ##
## Platy WorldBuilder End ##
## ---------------------- ##

				# if (eWidgetType == WidgetTypes.WIDGET_ACTION):
						# #PAE TradeRoute Advisor
						# if iData1 == -1:
								# if iData2 == 1: return CyTranslator().getText("TXT_KEY_TRADE_ROUTE_ADVISOR_SCREEN",())
								# if iData2 == 2: return CyTranslator().getText("TXT_KEY_TRADE_ROUTE2_ADVISOR_SCREEN",())

				if eWidgetType == WidgetTypes.WIDGET_GENERAL:
						# PAE TradeRoute Advisor
						if iData1 == 10000:
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_TRADE_ROUTE_ADVISOR_SCREEN", ())
								if iData2 == 2:
										return CyTranslator().getText("TXT_KEY_TRADE_ROUTE2_ADVISOR_SCREEN", ())

						# Inquisitor
						elif iData1 == 665:
								return CyTranslator().getText("TXT_KEY_GODS_INQUISTOR_CLEANSE_MOUSE_OVER", ())
						# Horse down
						elif iData1 == 666:
								return CyTranslator().getText("TXT_KEY_BUTTON_HORSE_DOWN", ())
						# Horse up
						elif iData1 == 667:
								return CyTranslator().getText("TXT_KEY_BUTTON_HORSE_UP", ())
						# Sklave -> Bordell
						elif iData1 == 668:
								return CyTranslator().getText("TXT_KEY_BUTTON_BORDELL", ())
						# Sklave -> Gladiator
						elif iData1 == 669:
								return CyTranslator().getText("TXT_KEY_BUTTON_GLADIATOR", ())
						# Sklave -> Theater
						elif iData1 == 670:
								return CyTranslator().getText("TXT_KEY_BUTTON_THEATRE", ())

						# ID 671 PopUp Vassal01 und Vassal02

						# Auswanderer / Emigrant
						elif iData1 == 672:
								return CyTranslator().getText("TXT_KEY_BUTTON_EMIGRANT", ())
						# Stadt aufloesen / disband city
						elif iData1 == 673:
								if bOption:
										return CyTranslator().getText("TXT_KEY_BUTTON_DISBAND_CITY", ())
								return CyTranslator().getText("TXT_KEY_BUTTON_DISBAND_CITY2", ())

						# ID 674 vergeben durch Hunnen-PopUp (CvScreensInterface - popupHunsPayment)

						# ID 675 vergeben durch Revolten-PopUp (CvScreensInterface - popupRevoltPayment)

						# 676 Freie UNIT durch TECH
						elif iData1 == 676:
								# 1 = Kultisten
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_MESSAGE_TECH_UNIT_1", ())
								# 2 = Missionare (Religion)
								elif iData2 == 2:
										return CyTranslator().getText("TXT_KEY_MESSAGE_TECH_UNIT_2", ())
								# 3 = Siedler
								elif iData2 == 3:
										return CyTranslator().getText("TXT_KEY_MESSAGE_TECH_UNIT_3", ())

						# Goldkarren
						elif iData1 == 677:
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_MESSAGE_GOLDKARREN", ())
								else:
										return CyTranslator().getText("TXT_KEY_HELP_GOLDKARREN2GOVCENTER", ())

						# ID 678 vergeben durch Provinz-PopUp (CvScreensInterface - popupProvinzPayment)

						# Sklave -> Schule
						elif iData1 == 679:
								return CyTranslator().getText("TXT_KEY_BUTTON_SCHULE", ())

						# Sklave -> Manufaktur Nahrung
						elif iData1 == 680:
								return CyTranslator().getText("TXT_KEY_BUTTON_MANUFAKTUR_FOOD", ())

						# Sklave -> Manufaktur Produktion
						elif iData1 == 681:
								return CyTranslator().getText("TXT_KEY_BUTTON_MANUFAKTUR_PROD", ())

						# ID 682 PopUp Vassal03
						# ID 683 PopUp Vassal04
						# ID 684 PopUp Vassal05
						# ID 685 PopUp Vassal06
						# ID 686 PopUp Vassal07
						# ID 687 PopUp Vassal08
						# ID 688 PopUp Vassal09
						# ID 689 PopUp Vassal10
						# ID 690 PopUp Vassal11
						# ID 691 PopUp Vassal12

						# Sklave -> Palace
						elif iData1 == 692:
								return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE2PALACE", ())
						# Sklave -> Temple
						elif iData1 == 693:
								return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE2TEMPLE", ())
						# Sklave -> sell
						elif iData1 == 694:
								return CyTranslator().getText("TXT_KEY_BUTTON_SELL_SLAVE", ())
						# Unit -> sell
						elif iData1 == 695:
								return CyTranslator().getText("TXT_KEY_BUTTON_SELL_UNIT", (iData2,))
						# Slave -> Feuerwehr
						elif iData1 == 696:
								return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE2FEUERWEHR", ())
						# Trojanisches Pferd
						elif iData1 == 697:
								return CyTranslator().getText("TXT_KEY_BUTTON_TROJAN_HORSE", ())
						# 698 INFO RangPromoUp (gemeinsam mit 751)
						# Unit -> Edle Ruestung
						elif iData1 == 699:
								if bOption:
										return CyTranslator().getText("TXT_KEY_BUTTON_BUY_EDLE_RUESTUNG", (iData2,))
								elif iData2 == -1:
										return CyTranslator().getText("TXT_KEY_BUTTON_BUY_EDLE_RUESTUNG_3", (iData2,))
								return CyTranslator().getText("TXT_KEY_BUTTON_BUY_EDLE_RUESTUNG_2", (iData2,))
						# Pillage road
						elif iData1 == 700:
								return CyTranslator().getText("TXT_KEY_MESSAGE_PILLAGE_ROAD", ())
						# Unit -> Wellen-Oil
						elif iData1 == 701:
								if bOption:
										return CyTranslator().getText("TXT_KEY_BUTTON_BUY_WATER_OIL", (iData2,))
								elif iData2 == -1:
										return CyTranslator().getText("TXT_KEY_BUTTON_BUY_WATER_OIL_3", (iData2,))
								return CyTranslator().getText("TXT_KEY_BUTTON_BUY_WATER_OIL_2", (iData2,))

						# ID 702 PopUp VassalTech HI-Hegemon
						# ID 703 PopUp VassalTech HI-Vassal
						# ID 704 PopUp Religionsaustreibung

						# Veteran -> Unit Upgrade eg. Principes + Hastati -> Triarii
						elif iData1 == 705 and iData2 > -1:
								return CyTranslator().getText("TXT_KEY_HELP_VETERAN2ELITE", (PyInfo.UnitInfo(iData2).getDescription(), gc.getUnitCombatInfo(PyInfo.UnitInfo(iData2).getUnitCombatType()).getDescription(), gc.getUnitInfo(iData2).getCombat(), gc.getUnitInfo(iData2).getMoves(), gc.getUnitInfo(iData2).getExtraCost()))

						# ID 706 PopUp Renegade City (keep or raze)

						# PopUp Hire/Assign Mercenaries (City Button)
						elif iData1 == 707:
								return CyTranslator().getText("TXT_KEY_HELP_MERCENARIES_CITYBUTTON", ())

						# ID 708-715 Hire/Assign Mercenaries
						elif iData1 == 709:
								return CyTranslator().getText("TXT_KEY_POPUP_MERCENARIES_ASSIGN", ())

						# ID 716-717 Torture of assigend mercenary

						# Unit Formations
						elif iData2 == 718:
								# CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("718 GameUtils erreicht",)), None, 2, None, ColorTypes(10), 0, 0, False, False)
								return u"<color=155,255,255,0>%s</color>" % gc.getPromotionInfo(iData1).getDescription()

						# ID 719 Promo 1 Trainer Building (Forest 1, Hills 1, City Defense 1, City Attack 1,...)
						elif iData1 == 719:
								if iData2 > -1:
										try:
												return CyTranslator().getText("TXT_KEY_HELP_PROMO_BUILDING", (gc.getBuildingInfo(iData2).getDescription(), gc.getPromotionInfo(L.DBuildingPromo[iData2]).getDescription()))
										except KeyError:
												pass

						# Legendary Hero can become a Great General
						elif iData1 == 720:
								return CyTranslator().getText("TXT_KEY_HELP_LEGEND_HERO_TO_GENERAL", ())

						# INFO BUTTONS: Techs/ Elefanten / Kamel / Hunter
						elif iData1 == 721:
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_HELP_ELEFANTENSTALL1", ())
								elif iData2 == 2:
										return CyTranslator().getText("TXT_KEY_HELP_ELEFANTENSTALL2", ())
								elif iData2 == 3:
										return CyTranslator().getText("TXT_KEY_HELP_ELEFANTENSTALL3", ())
								elif iData2 == 4:
										return CyTranslator().getText("TXT_KEY_HELP_KAMELSTALL1", ())
								elif iData2 == 5:
										return CyTranslator().getText("TXT_KEY_HELP_KAMELSTALL2", ())
								elif iData2 == 6:
										return CyTranslator().getText("TXT_KEY_HELP_KAMELSTALL3", ())
								elif iData2 == 7:
										return CyTranslator().getText("TXT_KEY_HELP_FEATURE_HUNTING", ())
								elif iData2 == 8:
										return CyTranslator().getText("TXT_KEY_HELP_UNIT_LEGION", ())
								elif iData2 == 9:
										return CyTranslator().getText("TXT_KEY_HELP_UNIT_PRAETORIAN", ())
								elif iData2 == 10:
										return CyTranslator().getText("TXT_KEY_HELP_UNIT_SUPPLY_WAGON", (PAE_Unit.getStackLimit(), PAE_Unit.getStackLimit()+20))
								elif iData2 == 11:
										return CyTranslator().getText("TXT_KEY_HELP_UNIT_SUPPLY_FOOD", (PAE_Unit.getUnitSupplyFood(),))
								elif iData2 == 12:
										return CyTranslator().getText("TXT_KEY_HELP_TRADE_UNITS", ())
								elif iData2 == 13:
										return CyTranslator().getText("TXT_KEY_HELP_UNIT_CAMP", ())
								elif iData2 == 14:
										return CyTranslator().getText("TXT_KEY_HELP_PFERDESTALL", ())
								elif iData2 == 15:
										return CyTranslator().getText("TXT_KEY_HELP_ELITE_MERCENARIES", ())
								elif iData2 == 16:
										return CyTranslator().getText("TXT_KEY_TECH_PATRONAT_HELP", ())
								elif iData2 == 17:
										return CyTranslator().getText("TXT_KEY_DYING_SLAVE_MINE_HELP", ())
								elif iData2 == 18:
										return CyTranslator().getText("TXT_KEY_DYING_SLAVE_FARM_HELP", ())
								elif iData2 == 19:
										return CyTranslator().getText("TXT_KEY_DYING_SLAVE_TECH_REDUCE_HELP", ())
								elif iData2 == 20:
										return CyTranslator().getText("TXT_KEY_HELP_ADD_ESEL", ())
								elif iData2 == 21:
										return CyTranslator().getText("TXT_KEY_HELP_TECH_VILLAGE2TOWN", ())

						# Piraten-Feature
						elif iData1 == 722:
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_HELP_GO2PIRATE", ())
								elif iData2 == 2:
										return CyTranslator().getText("TXT_KEY_HELP_GO2PIRATE2", ())
								elif iData2 == 3:
										return CyTranslator().getText("TXT_KEY_HELP_GO2PIRATE4", ())

						# EspionageInfos (TechChooser)
						elif iData1 == 723:
								return gc.getEspionageMissionInfo(iData2).getText()
						# Veteran -> Reservist
						elif iData1 == 724:
								return CyTranslator().getText("TXT_KEY_SPECIALIST_RESERVIST_STRATEGY", ())
						# Reservist -> Veteran
						elif iData1 == 725:
								return CyTranslator().getText("TXT_KEY_HELP_RESERVIST_TO_VETERAN", ())
						# Bonusverbreitung (FREI?)
						elif iData1 == 726:
								return CyTranslator().getText("TXT_KEY_HELP_BONUSVERBREITUNG", ())
						# iData2 = 1: UNIT_SUPPLY_FOOD: Nahrung abliefern
						# iData2 = 2: UNIT_SUPPLY_WAGON: Nahrung aufnehmen
						elif iData1 == 727:
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_HELP_GETREIDE_ABLIEFERN", (PAE_Unit.getUnitSupplyFood(),))
								elif iData2 == 2:
										return CyTranslator().getText("TXT_KEY_HELP_GETREIDE_AUFNEHMEN", ())
						# Karte zeichnen
						elif iData1 == 728:
								return CyTranslator().getText("TXT_KEY_HELP_KARTE_ZEICHNEN", ())
						# Slave -> Library
						elif iData1 == 729:
								return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE2LIBRARY", ())
						# Release slaves
						elif iData1 == 730:
								return CyTranslator().getText("TXT_KEY_BUTTON_RELEASESLAVES", ())
						# Send Missionary to a friendly city and spread its religion
						elif iData1 == 731:
								return CyTranslator().getText("TXT_KEY_BUTTON_SPREAD_RELIGION", ())
						# Send Trade Merchant into next foreign city
						# if (iData1 == 732):
						#  return CyTranslator().getText("TXT_KEY_MISSION_AUTOMATE_MERCHANT",())
						# Limes
						elif iData1 == 733:
								if iData2 == -1:
										return CyTranslator().getText("TXT_KEY_INFO_LIMES_0", ())
								elif iData2 == 0:
										return CyTranslator().getText("TXT_KEY_INFO_LIMES_1", ())
								return CyTranslator().getText("TXT_KEY_INFO_LIMES_2", ())
						# Sklave -> SPECIALIST_SLAVE_FOOD oder SPECIALIST_SLAVE_PROD
						elif iData1 == 734:
								if iData2 == 1:
										if bOption:
												return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE2SPECIALIST1_TRUE", (iData2,))
										return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE2SPECIALIST1_FALSE", (iData2,))
								elif iData2 == 2:
										if bOption:
												return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE2SPECIALIST2_TRUE", (iData2,))
										return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE2SPECIALIST2_FALSE", (iData2,))
						# Salae oder Dezimierung
						elif iData1 == 735:
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_ACTION_SALAE_1", ())
								elif iData2 == 2:
										return CyTranslator().getText("TXT_KEY_ACTION_DECIMATIO_1", ())
						# Handelsposten errichten
						elif iData1 == 736:
								return CyTranslator().getText("TXT_KEY_BUTTON_HANDELSPOSTEN", (gc.getBonusInfo(iData2).getDescription(),)) + u" %c" % (gc.getBonusInfo(iData2).getChar())
						# Provinzstatthalter / Tribut
						elif iData1 == 737:
								return CyTranslator().getText("TXT_KEY_BUTTON_CONTACT_STATTHALTER", ())
						# Cultivation / Trade
						elif iData1 == 738:
								if bOption:
										return CyTranslator().getText("TXT_KEY_BUTTON_CULTIVATE_BONUS_FROM_CITY", ())
								return CyTranslator().getText("TXT_KEY_BUTTON_CULTIVATE_BONUS", ())
						elif iData1 == 739:
								if bOption:
										if iData2 == -1:
												return CyTranslator().getText("TXT_KEY_BUTTON_COLLECT_BONUS2", ())
										elif iData2 == 0:
												return CyTranslator().getText("TXT_KEY_BUTTON_COLLECT_BONUS", ())
										elif iData2 == 3:
												return CyTranslator().getText("TXT_KEY_BUTTON_COLLECT_BONUS3", ())
										else:
												return CyTranslator().getText("TXT_KEY_BUTTON_COLLECT_BONUS_CITY", ())
								else:
										return CyTranslator().getText("TXT_KEY_BUTTON_COLLECT_BONUS_IMPOSSIBLE", ())
						elif iData1 == 740:
								return CyTranslator().getText("TXT_KEY_BUTTON_BUY_BONUS", ())
						elif iData1 == 741:
								return CyTranslator().getText("TXT_KEY_BUTTON_SELL_BONUS", (iData2,))
						elif iData1 == 742:
								return CyTranslator().getText("TXT_KEY_SPREAD_IMPOSSIBLE_" + str(iData2), ())
						elif iData1 == 744:
								return CyTranslator().getText("TXT_KEY_CREATE_TRADE_ROUTE", ())
						elif iData1 == 748:
								return CyTranslator().getText("TXT_KEY_CANCEL_TRADE_ROUTE", ())
						# -------------------------------------
						# Allgemeine Infos (aktionslose Buttons)
						elif iData1 == 749:
								# 1: no cults with civic Animism
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_INFO_CIVIC_NOCULT", ())
								# 2-4: Siegesstele/Siegestempel/Monument Infos
								elif iData2 == 2:
										return CyTranslator().getText("TXT_KEY_MONUMENT_INFO_1", ())
								elif iData2 == 3:
										return CyTranslator().getText("TXT_KEY_MONUMENT_INFO_2", ())
								elif iData2 == 4:
										return CyTranslator().getText("TXT_KEY_MONUMENT_INFO_3", ())
								# Dienstgrade Info im TechChooser
								elif iData2 == 5:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_GER", ())
								elif iData2 == 6:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_EGYPT", ())
								elif iData2 == 7:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_SUMER", ())
								elif iData2 == 8:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_ASSUR", ())
								elif iData2 == 9:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_SPARTA", ())
								elif iData2 == 10:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_MACEDON", ())
								elif iData2 == 11:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_PERSIA", ())
								elif iData2 == 12:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_GREEK", ())
								elif iData2 == 13:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_CARTH", ())
								elif iData2 == 14:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_ROM", ())
								elif iData2 == 15:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_ROM_EQUES", ())
								elif iData2 == 16:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_ROM_LATE", ())
								elif iData2 == 17:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_HUN", ())
								elif iData2 == 18:
										return CyTranslator().getText("TXT_KEY_RANK_START_INFO_PERSIA2", ())
								elif iData2 == 19:
										iBuild = gc.getInfoTypeForString("BUILD_ORE_CAMP")
										return CyTranslator().getText("TXT_KEY_TECH_OBSOLETES_NO_LINK", (gc.getBuildInfo(iBuild).getDescription(),))
								# Domestic Advisor Icon Info
								elif iData2 == 20:
										nl = CyTranslator().getText("[NEWLINE]", ())
										sText = u"%c " % CyGame().getSymbolID(FontSymbols.STAR_CHAR) + CyTranslator().getText("TXT_KEY_INFO_DOMESTIC_ADVISOR_1", ())
										sText += nl + u"%c " % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR) + CyTranslator().getText("TXT_KEY_INFO_DOMESTIC_ADVISOR_2", ())
										sText += nl + u"%c " % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR) + CyTranslator().getText("TXT_KEY_INFO_DOMESTIC_ADVISOR_3", ())
										sText += nl + u"%c " % CyGame().getSymbolID(FontSymbols.MAP_CHAR) + CyTranslator().getText("TXT_KEY_INFO_DOMESTIC_ADVISOR_4", ())
										sText += nl + u"%c " % gc.getReligionInfo(gc.getInfoTypeForString("RELIGION_GREEK")).getChar() + CyTranslator().getText("TXT_KEY_INFO_DOMESTIC_ADVISOR_5", ())
										sText += nl + u"%c " % gc.getReligionInfo(gc.getInfoTypeForString("RELIGION_NORDIC")).getChar() + CyTranslator().getText("TXT_KEY_INFO_DOMESTIC_ADVISOR_6", ())
										return sText


						# -------------------------------------
						# Unit Ethnic (MainInterface Unit Detail Promo Icons)
						elif iData1 == 750 and iData2 > -1:
								return gc.getCivilizationInfo(iData2).getAdjective(0)

						# Unit Rang Promo (INFO TEXT Military ranking)
						# 751 für die Ausführung in CvEventManager
						# 698 nur für die INFO (wird nicht im CvEventManager ausgeführt)
						elif iData1 == 751 or iData1 == 698:
								iPlayer = gc.getGame().getActivePlayer()
								iUnit = gc.getPlayer(iPlayer).getUnit(iData2).getUnitType()
								iNewUnit = PAE_Unit.getUpgradeUnit(iPlayer, iUnit)

								sText = u"<font=3>" + CyTranslator().getText("TXT_KEY_BUTTON_RANG_PROMO_UP", ()) + u"</font>"
								sText += u"<font=2>" + CyTranslator().getText("TXT_KEY_BUTTON_RANG_PROMO_UP2", ()) + u"</font>"
								if iNewUnit in L.LCapitalPromoUpUnits:
										sText += CyTranslator().getText("[NEWLINE][ICON_BULLET]", ()) + u"<font=3>" + CyTranslator().getText("TXT_KEY_BUTTON_RANG_PROMO_UP3", ()) + u"</font>"

								sText += u"<font=2>"
								if iUnit != -1 and iNewUnit != -1:
										sText += CyTranslator().getText("TXT_KEY_BUTTON_RANG_PROMO_UP4", (gc.getUnitInfo(iUnit).getDescription(),gc.getUnitInfo(iNewUnit).getDescription()))
										sText += CyTranslator().getText("  %d1[ICON_STRENGTH]", (gc.getUnitInfo(iNewUnit).getCombat(),))
										sText += CyTranslator().getText(" %d1[ICON_MOVES]", (gc.getUnitInfo(iNewUnit).getMoves(),))
										if gc.getUnitInfo(iNewUnit).getExtraCost() > 0:
												sText += CyTranslator().getText(" +%d1[ICON_GOLD]", (gc.getUnitInfo(iNewUnit).getExtraCost(),))
										iUnitCombatType = gc.getUnitInfo(iNewUnit).getUnitCombatType()
										sText += CyTranslator().getText("[NEWLINE][COLOR_UNIT_TEXT](%s1)[COLOR_REVERT][NEWLINE][NEWLINE]", (gc.getUnitCombatInfo(iUnitCombatType).getDescription(),))

								sText += CyTranslator().getText("TXT_KEY_BUTTON_RANG_PROMO_UP5", ())
								iDiff = gc.getUnitInfo(iNewUnit).getCombat() - gc.getUnitInfo(iUnit).getCombat()
								if iDiff > 0:
										sText += CyTranslator().getText(" +%d1[ICON_STRENGTH]", (iDiff,))
								iDiff = gc.getUnitInfo(iNewUnit).getMoves() - gc.getUnitInfo(iUnit).getMoves()
								if iDiff > 0:
										sText += CyTranslator().getText(" +%d1[ICON_MOVES]", (iDiff,))
								iDiff = gc.getUnitInfo(iNewUnit).getExtraCost() - gc.getUnitInfo(iUnit).getExtraCost()
								if iDiff > 0:
										sText += CyTranslator().getText(" +%d1[ICON_GOLD]", (iDiff,))
								iNewUnit2 = PAE_Unit.getUpgradeUnit(iPlayer, iNewUnit)
								if iNewUnit2 != -1:
										sText += CyTranslator().getText("TXT_KEY_BUTTON_RANG_PROMO_UP6", (gc.getUnitInfo(iNewUnit2).getDescription(),))
										sText += CyTranslator().getText("  %d1[ICON_STRENGTH]", (gc.getUnitInfo(iNewUnit2).getCombat(),))
										sText += CyTranslator().getText(" %d1[ICON_MOVES]", (gc.getUnitInfo(iNewUnit2).getMoves(),))
										if gc.getUnitInfo(iNewUnit2).getExtraCost() > 0:
												sText += CyTranslator().getText(" +%d1[ICON_GOLD]", (gc.getUnitInfo(iNewUnit2).getExtraCost(),))
										iUnitCombatType = gc.getUnitInfo(iNewUnit2).getUnitCombatType()
										sText += CyTranslator().getText("[NEWLINE][COLOR_HIGHLIGHT_TEXT](%s1)[COLOR_REVERT]", (gc.getUnitCombatInfo(iUnitCombatType).getDescription(),))
								sText += CyTranslator().getText("</font>[NEWLINE]", ())

								return sText

						# Bless units (Hagia Sophia, Great General)
						# Increase morale (Zeus)
						elif iData1 == 752:
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_BUTTON_MORALE_UNIT", ())
								else:
										return CyTranslator().getText("TXT_KEY_BUTTON_BLESS_UNITS", ())
						# Slave -> Village, Latifundium, Emigrant -> Village/Town, Settler -> Village->Town
						elif iData1 == 753:
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE2LATIFUNDIUM", ())
								elif iData2 == 2:
										return CyTranslator().getText("TXT_KEY_BUTTON_VILLAGE2TOWN", ())
								else:
										return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE2VILLAGE", ())
						# Obsolete units (Tech Screen)
						elif iData1 == 754:
								if bOption:
										return CyTranslator().getText("TXT_KEY_TECH_OBSOLETES_NO_LINK", (gc.getUnitInfo(iData2).getDescription(),))
								else:
										return CyTranslator().getText("TXT_KEY_TECH_OBSOLETES_NO_LINK", (gc.getProjectInfo(iData2).getDescription(),))
						# Sklave -> Brotmanufaktur Nahrung
						elif iData1 == 755:
								return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE_BROTMANUFAKTUR", ())
						# Rang Promo: Legion ins Ausbildungscamp: Increase Ranking of Legionaries
						elif iData1 == 756:
								if bOption:
										return CyTranslator().getText("TXT_KEY_BUTTON_LEGION2RANG", ())
						# Statthalter ansiedeln
						elif iData1 == 757:
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_BUTTON_SETTLE_STATTHALTER2", ())  # General or Hero
								else:
										return CyTranslator().getText("TXT_KEY_BUTTON_SETTLE_STATTHALTER", ())  # Statthalter
						# Heldendenkmal / Siegesdenkmal aufnehmen / bauen
						elif iData1 == 758:
								if iData2 == 0:
										return CyTranslator().getText("TXT_KEY_BUTTON_HELDENDENKMAL1", ())  # aufnehmen
								else:
										return CyTranslator().getText("TXT_KEY_BUTTON_HELDENDENKMAL2", (gc.getBuildingInfo(iData2).getDescription(),))  # bauen
						# Give morale to units
						elif iData1 == 759:
								if iData2 == 2:
										return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE_DRUIDE", ())
								else:
										return CyTranslator().getText("TXT_KEY_BUTTON_MORALE_UNITS", ())
						# Slaves on plot: head off -> gives morale
						elif iData1 == 760:
								return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE_HEAD", ())
						# Slaves on plot: fight against to gain XP
						elif iData1 == 761:
								if bOption:
										return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE_FIGHT4XP", ())
								else:
										return CyTranslator().getText("TXT_KEY_BUTTON_SLAVE_FIGHT4XP_INFO", ())
						# Escorte
						elif iData1 == 762:
								txt = CyTranslator().getText("TXT_KEY_HELP_UNIT_ESCORTE", (iData2,))
								txt += u" " + CyTranslator().getText("TXT_KEY_INFO_CIVIC_SOELDNERTUM_BONUS", ())
								return txt
						# Forts/Handelsposten erobern
						# elif iData1 == 763:
						#    return CyTranslator().getText("TXT_KEY_BUTTON_CAPTURE_FORT", ())
						# Vasallen entlassen bzw Städte geben
						elif iData1 == 764:
								return CyTranslator().getText("TXT_KEY_POPUP_VASALLEN_BUTTON", ())

						# General: Verbrannte Erde
						elif iData1 == 765:
								return CyTranslator().getText("TXT_KEY_ACTION_BURN_FOREST", ())

						# Pferdewechsel / Horse Swap
						elif iData1 == 766:
								if iData2 == 1:
										return CyTranslator().getText("TXT_KEY_ACTION_CAMEL_SWAP", ())
								else:
										return CyTranslator().getText("TXT_KEY_ACTION_HORSE_SWAP", ())

						# Magnetkompass
						elif iData1 == 767:
								return CyTranslator().getText("TXT_KEY_BUTTON_BUY_KOMPASS", ())

						# Schiff reparieren
						elif iData1 == 768:
								return CyTranslator().getText("TXT_KEY_BUTTON_REPAIR_SHIP", (iData2,))

						# Great Prophet Holy City
						elif iData1 == 769:
								return CyTranslator().getText("TXT_KEY_BUTTON_GREAT_PROPHET_HOLY_CITY", ()) + u" %c" % (gc.getReligionInfo(iData2).getChar())

						# General: Ramme bauen
						elif iData1 == 770:
								return CyTranslator().getText("TXT_KEY_ACTION_FOREST_RAM", ())

						# Hunter: Lager oder Beobachtungsturm
						elif iData1 == 771:
								# Lager
								if iData2 == 1:
										text = u"<color=155,255,255,0>%s</color> " % CyTranslator().getText("TXT_KEY_BUILD_CAMP", ())
										text += CyTranslator().getText("+1[ICON_FOOD]", ())
										if bOption:
												text += CyTranslator().getText(", +1[ICON_COMMERCE]", ())
										text += CyTranslator().getText("[NEWLINE]", ())
										text += CyTranslator().getText("TXT_KEY_ACTION_CHANCE_DISCOVER", ()) + u"%c" % gc.getBonusInfo(gc.getInfoTypeForString("BONUS_DEER")).getChar()
										text += CyTranslator().getText("[NEWLINE]", ())
										text += CyTranslator().getText("TXT_KEY_ACTION_CHANCE_DISCOVER", ()) + u"%c" % gc.getBonusInfo(gc.getInfoTypeForString("BONUS_FUR")).getChar()
										text += CyTranslator().getText("[NEWLINE]", ())
										text += CyTranslator().getText("TXT_KEY_BUILD_CAMP_HUNTER", ())
										return text
								# Beobachtungsturm
								elif iData2 == 2:
										# Dertuek
										text = CyTranslator().getText("[COLOR_HIGHLIGHT_TEXT]", ())
										text += CyTranslator().getText("TXT_KEY_BUILD_TURM", ())
										text += CyTranslator().getText("[COLOR_REVERT][NEWLINE]", ())
										text += CyTranslator().getText("TXT_KEY_BUILD_TURM_HELP", ())
										return text
								# Schürflager
								elif iData2 == 3:
										text = u"<color=155,255,255,0>%s</color> " % CyTranslator().getText("TXT_KEY_BUILD_ORE_CAMP", ())
										text += CyTranslator().getText("[NEWLINE][ICON_BULLET]+1[ICON_COMMERCE]", ())
										text += CyTranslator().getText("[NEWLINE]", ())
										text += CyTranslator().getText("TXT_KEY_BUILD_CAMP_HUNTER", ())
										return text
								# Pfad / Path
								elif iData == 4:
										return

						# Gladiator: Gladiatorenschule bauen
						elif iData1 == 772:
								return CyTranslator().getText("TXT_KEY_BUILD_GLADIATORENSCHULE", ())



						# CITY_TAB replacements
						elif iData1 == 88000:
								return gc.getCityTabInfo(iData2).getDescription()

				elif eWidgetType == WidgetTypes.WIDGET_HELP_PROMOTION:
						if iData2 == 718 and iData1 == -1:
								return u"<color=155,255,255,0>%s</color>" % CyTranslator().getText("TXT_KEY_PROMOTION_FORM_NONE", ())

				# Dertuek
				elif eWidgetType in (WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, WidgetTypes.WIDGET_CREATE):
						sHelp = gc.getProjectInfo(iData1).getHelp()
						if sHelp:
								return u"\n" + sHelp

				# ***TEST***
				#CyInterface().addMessage(CyGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("X",iData1)), None, 2, None, ColorTypes(12), 0, 0, False, False)

				return u""

		def getUpgradePriceOverride(self, argsList):
				iPlayer, iUnitID, iUnitTypeUpgrade = argsList

				pPlayer = gc.getPlayer(iPlayer)
				pUnit = pPlayer.getUnit(iUnitID)

				iPrice = gc.getDefineINT("BASE_UNIT_UPGRADE_COST")

				# PAE (for iCost -1 Units)
				iSub = pPlayer.getUnitProductionNeeded(pUnit.getUnitType())
				if iSub <= 1:
						iSub = pPlayer.getUnitProductionNeeded(iUnitTypeUpgrade) / 4 * 3

				iPrice += (max(0, (pPlayer.getUnitProductionNeeded(iUnitTypeUpgrade) - iSub)) * gc.getDefineINT("UNIT_UPGRADE_COST_PER_PRODUCTION"))

				if not pPlayer.isHuman() and not pPlayer.isBarbarian():
						pHandicapInfo = gc.getHandicapInfo(gc.getGame().getHandicapType())
						iPrice *= pHandicapInfo.getAIUnitUpgradePercent() / 100
						iPrice *= max(0, ((pHandicapInfo.getAIPerEraModifier() * pPlayer.getCurrentEra()) + 100)) / 100

				iPrice = iPrice * (100 - pUnit.getUpgradeDiscount()) / 100
				if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_ORGANIZED")):
						iPrice /= 2
				return max(0, iPrice)

		# AI: Strategische Bonusresourcenverbreitung
		# Pferd, Kamel, Ele, Hund / horse, camel, ele, dog

		def doSpreadStrategicBonus_AI(self, pUnit, eBuilding, eBonus):
				pUnitGroup = pUnit.getGroup()
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, u"Schritt 0: missionType: " + str(pUnitGroup.getMissionType(0)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				# Mission 0: moveTo, -1: none
				if pUnitGroup.getMissionType(0) != 0:
						iOwner = pUnit.getOwner()
						pPlayer = gc.getPlayer(iOwner)

						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, u"Schritt 1: " + pUnit.getName() + " iOwner: " + str(iOwner) + " PAE_AI_ID: " + str(self.PAE_AI_ID), None, 2, None, ColorTypes(10), 0, 0, False, False)

						# kultivieren wenn die Einheit auf dem korrekten Plot steht
						if self.PAE_AI_ID2 == pUnit.getID():
								if PAE_Cultivation._isBonusCultivationChance(pUnit.getOwner(), pUnit.plot(), eBonus, False, None):
										PAE_Cultivation.doCultivateBonus(pUnit.plot(), pUnit, eBonus, False)
										pUnit.kill(True, -1)
										return True

						# Nur 1x pro Runde alle Staedte checken
						# PAE AI Unit Instances (better turn time)
						if self.PAE_AI_ID != iOwner:
								self.PAE_AI_ID = iOwner
								self.PAE_AI_ID2 = pUnit.getID()

								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, u"Schritt 2: iBonus: " + str(eBonus), None, 2, None, ColorTypes(10), 0, 0, False, False)
								#eCityStatus = gc.getInfoTypeForString("BUILDING_KOLONIE")
								iDistance = 99
								pCity = None
								lPlots = []

								(loopCity, pIter) = pPlayer.firstCity(False)
								while loopCity:
										# if loopCity.isHasBuilding(eCityStatus):
										if not loopCity.isHasBuilding(eBuilding):
												if pUnit.plot().getArea() == loopCity.plot().getArea():
														#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, u"Schritt 3: CultivationCheck - " + loopCity.getName(), None, 2, None, ColorTypes(10), 0, 0, False, False)
														lPlotsCheck = PAE_Cultivation.getCityCultivatablePlots(loopCity, eBonus)
														if lPlotsCheck:
																iDistanceCheck = CyMap().calculatePathDistance(pUnit.plot(), loopCity.plot())
																if iDistanceCheck != -1 and iDistanceCheck < iDistance:
																		iDistance = iDistanceCheck
																		pCity = loopCity
																		lPlots = lPlotsCheck
										(loopCity, pIter) = pPlayer.nextCity(pIter, False)

								if pCity is not None and lPlots:
										iRand = CvUtil.myRandom(len(lPlots), "GameUtils_doSpreadStrategicBonus_AI")
										pPlot = lPlots[iRand]

										if pUnit.generatePath(pPlot, 0, False, None):
												if not pUnit.atPlot(pPlot):
														pUnitGroup.clearMissionQueue()
														pUnit.getGroup().pushMoveToMission(pPlot.getX(), pPlot.getY())
														#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, u"Schritt 4: moveTo" + pCity.getName() + u" " + str(pPlot.getX()) + u":" + str(pPlot.getY()), None, 2, None, ColorTypes(10), 0, 0, False, False)
												else:
														PAE_Cultivation.doCultivateBonus(pPlot, pUnit, eBonus, False)
														pUnit.kill(True, -1)
														#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, u"Schritt 5: doCultivateBonus", None, 2, None, ColorTypes(10), 0, 0, False, False)
												return True
								
								## wenn keine Stadt gefunden wurde: Bonusgut mit dem meisten Bonusgut ersetzen
								## aber nur, wenn AI keins oder nur 1 davon besitzt
								## Bonus checken
								#iNum = pPlayer.countOwnedBonuses(eBonus)
								#if iNum < 2:
								#		iErsetzeBonus = -1
								#		for B in  L.LBonusStratCultivatable:
								#				if eBonus != B:
								#					iCheck = pPlayer.countOwnedBonuses(B)
								#					if iCheck > iNum:
								#							iNum = iCheck
								#							iErsetzeBonus = B
								#		# Stadt aussuchen
								#		if iErsetzeBonus != -1:
								#				(loopCity, pIter) = pPlayer.firstCity(False)
								#				while loopCity:
								#						if loopCity.isHasBuilding(eCityStatus):
								#							if not loopCity.isHasBuilding(eBuilding):
								#
								#								bOK = False
								#								lPlots = PAE_Cultivation.getCityCultivatedPlots(loopCity, iErsetzeBonus)
								#								if len(lPlots):
								#									for p in lPlots:
								#										if p.getBonusType(-1) == iErsetzeBonus:
								#											if PAE_Cultivation._bonusIsCultivatableFromCity(iOwner, loopCity, eBonus, False):
								#													p.setBonusType(-1)
								#													p.setImprovementType(-1)
								#													loopCity.setNumRealBuilding(eBuilding, 1)
								#													PAE_Cultivation.doBuildingCultivate(loopCity, eBuilding)
								#													pUnit.kill(True, -1)
								#													return True
								#
								#						(loopCity, pIter) = pPlayer.nextCity(pIter, False)
								
								# wenn gar nix geht, Unit verkaufen
								iRand = CvUtil.myRandom(10, "GameUtils_doSpreadStrategicBonus_AI_sellHorse")
								if iRand == 1:
										pPlayer.changeGold(25)
										pUnit.kill(True, -1)
										return True
				return False

		# Inquisitor -------------------
		def doInquisitorCore_AI(self, pUnit):
				iOwner = pUnit.getOwner()
				pOwner = gc.getPlayer(iOwner)
				iStateReligion = pOwner.getStateReligion()

				# CAN AI use inquisitor
				if iStateReligion >= 0 and pUnit.getGroup().getMissionType(0) != 0:
						#iTurn = gc.getGame().getGameTurn()
						#iOwnCulture = pOwner.getCultureHistory(iTurn)
						#lPlayers = PyGame().getCivPlayerList()
						lCities = PyPlayer(iOwner).getCityList()

						for pyCity in lCities:
								# has this city probably unhappiness of religion cause
								if pyCity.getAngryPopulation() > 0:
										lReligions = pyCity.getReligions()
										if len(lReligions) > 1:
												pCity = pOwner.getCity(pyCity.getID())
												for iReligion in lReligions:
														if iReligion != iStateReligion:
																if pCity.isHolyCityByType(iReligion) == 0:
																		# Makes the unit purge it
																		PAE_City.doInquisitorPersecution2(iOwner, pCity.getID(), -1, iReligion, pUnit.getID())
																		return True

		def getExperienceNeeded(self, argsList):
				# use this function to set how much experience a unit needs
				iLevel, iOwner = argsList

				iExperienceNeeded = 0

				# BTS: regular epic game experience
				# GlobalDefines: MIN_EXPERIENCE_PER_COMBAT, MAX_EXPERIENCE_PER_COMBAT: 1, 2
				# and PAE VI again
				# 2,5,10,17,26
				#iExperienceNeeded = iLevel * iLevel + 1

				# PAE IV: ab Lvl 7 mehr XP notwendig
				#if iLevel > 7: iExperienceNeeded += iLevel * 2

				# PAE V: L * (L+2) - (L / 2)
				# Min, Max: 1, 2
				# 2,7,13,22,32
				#iExperienceNeeded = iLevel * (iLevel+2) - iLevel/2
				
				# PAE 6.14: L * (L+2)
				# Min, Max: 1, 3
				# 3, 8, 15, 24, 35
				iExperienceNeeded = iLevel * (iLevel+2)

				iModifier = gc.getPlayer(iOwner).getLevelExperienceModifier()
				if iModifier != 0:
						iExperienceNeeded += (iExperienceNeeded * iModifier + 99) / 100   # ROUND UP

				return iExperienceNeeded

		# Freed slaves for AI
		def _doSettleFreedSlaves_AI(self, pUnit):
				pUnitGroup = pUnit.getGroup()

				if pUnitGroup.getMissionType(0) != 0:
						iOwner = pUnit.getOwner()
						pOwner = gc.getPlayer(iOwner)

						pSeekCity = None
						iSeek = 0

						(loopCity, pIter) = pOwner.firstCity(False)
						while loopCity:
								iNum = loopCity.getYieldRate(1)
								if iNum <= iSeek or iNum == 0:
										pSeekCity = loopCity
										iSeek = iNum
								(loopCity, pIter) = pOwner.nextCity(pIter, False)

						# PAE Better AI soll direkt ansiedeln
						if pSeekCity is not None and not pSeekCity.isNone():
								pSeekCity.changeFreeSpecialistCount(0, 1)  # Spezialist Citizen
								# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
								pUnit.kill(True, -1)  # RAMK_CTD
								return True

		# Veteran -> Reservist in city for AI

		def _doReservist_AI(self, pUnit):
				pUnitGroup = pUnit.getGroup()

				if pUnitGroup.getMissionType(0) != 0:
						iOwner = pUnit.getOwner()
						pOwner = gc.getPlayer(iOwner)

						# nur im Friedensfall
						bWar = False
						iThisTeam = pOwner.getTeam()
						pThisTeam = gc.getTeam(iThisTeam)

						if pThisTeam.isHasTech(gc.getInfoTypeForString("TECH_RESERVISTEN")):
								iRange = gc.getMAX_CIV_TEAMS()
								for i in range(iRange):
										if gc.getPlayer(i).isAlive():
												iTeam = gc.getPlayer(i).getTeam()
												if pThisTeam.isAtWar(iTeam):
														bWar = True

								if not bWar:
										if pUnit.getUnitType() not in L.LUnitsNoAIReservists:

												pSeekCity = None
												iSeek = 0

												(pCity, pIter) = pOwner.firstCity(False)
												while pCity:
														iNum = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_RESERVIST"))
														if iNum <= iSeek or iNum == 0:
																pSeekCity = pCity
																iSeek = iNum
														(pCity, pIter) = pOwner.nextCity(pIter, False)

												# PAE Better AI soll direkt ansiedeln - rausgegeben
												if pSeekCity is not None and not pSeekCity.isNone():
														if pUnit.getX() != pSeekCity.getX() or pUnit.getY() != pSeekCity.getY():
																pUnitGroup.clearMissionQueue()
																pUnit.getGroup().pushMoveToMission(pSeekCity.getX(), pSeekCity.getY())
														else:
																pSeekCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_RESERVIST"), 1)
																# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																pUnit.kill(True, -1)  # RAMK_CTD
																return True

		# Promotion Trainer Building (Forest 1, Hills 1, ...) -------------------

		def _AI_SettleTrainer(self, pUnit):
				iPlayer = pUnit.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				pPlot = pUnit.plot()

				# An necessary advantage for the AI: AI does not need to move unit into a city
				# An undone possibility: units gets some strong escort units to move to an own city
				if pPlot.getOwner() == iPlayer:
						lBuildings = []
						for iPromo in L.DPromosForPromoBuilding:
								if pUnit.isHasPromotion(iPromo):
										lBuildings.append((L.DPromosForPromoBuilding[iPromo], iPromo))

						for iBuilding, iPromo in lBuildings:
								(loopCity, pIter) = pPlayer.firstCity(False)
								while loopCity:
										if not loopCity.isHasBuilding(iBuilding):
												if iPromo != gc.getInfoTypeForString("PROMOTION_NAVIGATION4") or loopCity.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
														loopCity.setNumRealBuilding(iBuilding, 1)
														# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
														pUnit.kill(True, -1)  # RAMK_CTD
														return True
										(loopCity, pIter) = pPlayer.nextCity(pIter, False)
				return False

		# Religion des Missionars herausfinden
		def getUnitReligion(self, iUnitType):
				if iUnitType == gc.getInfoTypeForString("UNIT_CELTIC_MISSIONARY"):
						return 0
				elif iUnitType == gc.getInfoTypeForString("UNIT_NORDIC_MISSIONARY"):
						return 1
				elif iUnitType == gc.getInfoTypeForString("UNIT_PHOEN_MISSIONARY"):
						return 2
				elif iUnitType == gc.getInfoTypeForString("UNIT_EGYPT_MISSIONARY"):
						return 3
				elif iUnitType == gc.getInfoTypeForString("UNIT_ROME_MISSIONARY"):
						return 4
				elif iUnitType == gc.getInfoTypeForString("UNIT_ZORO_MISSIONARY"):
						return 5
				elif iUnitType == gc.getInfoTypeForString("UNIT_GREEK_MISSIONARY"):
						return 6
				elif iUnitType == gc.getInfoTypeForString("UNIT_SUMER_MISSIONARY"):
						return 7
				elif iUnitType == gc.getInfoTypeForString("UNIT_HINDU_MISSIONARY"):
						return 8
				elif iUnitType == gc.getInfoTypeForString("UNIT_BUDDHIST_MISSIONARY"):
						return 9
				elif iUnitType == gc.getInfoTypeForString("UNIT_JEWISH_MISSIONARY"):
						return 10
				elif iUnitType == gc.getInfoTypeForString("UNIT_CHRISTIAN_MISSIONARY"):
						return 11
				#elif iUnitType == gc.getInfoTypeForString("UNIT_MISSIONARY_JAINISMUS"):
				#		return 12
				#elif iUnitType == gc.getInfoTypeForString("UNIT_ORTHODOX_MISSIONARY"):
				#		return 13
				elif iUnitType == gc.getInfoTypeForString("UNIT_ISLAMIC_MISSIONARY"):
						return 14
				return -1

		# Kult eines Kultisten herausfinden
		def getUnitKult(self, iUnitType):
				if iUnitType == gc.getInfoTypeForString("UNIT_EXECUTIVE_1"):
						return 0
				elif iUnitType == gc.getInfoTypeForString("UNIT_EXECUTIVE_2"):
						return 1
				elif iUnitType == gc.getInfoTypeForString("UNIT_EXECUTIVE_3"):
						return 2
				elif iUnitType == gc.getInfoTypeForString("UNIT_EXECUTIVE_4"):
						return 3
				elif iUnitType == gc.getInfoTypeForString("UNIT_EXECUTIVE_5"):
						return 4
				elif iUnitType == gc.getInfoTypeForString("UNIT_EXECUTIVE_6"):
						return 5
				elif iUnitType == gc.getInfoTypeForString("UNIT_EXECUTIVE_7"):
						return 6
				elif iUnitType == gc.getInfoTypeForString("UNIT_EXECUTIVE_8"):
						return 7
				elif iUnitType == gc.getInfoTypeForString("UNIT_EXECUTIVE_9"):
						return 8
				return -1

		# Missioniere automatisch nur Cities die ausserhalb des kontinentalen Bereichs sind
		def doAIMissionReligion(self, pUnit):
				if CvUtil.myRandom(10, "doAIMissionReligion") != 1:
						return

				iPlayer = pUnit.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				iReligion = self.getUnitReligion(pUnit.getUnitType())

				if iReligion == -1:
						return

				if pPlayer.getStateReligion() != iReligion:
						return

				(loopCity, pIter) = pPlayer.firstCity(False)
				while loopCity:
						if not loopCity.isNone():
								if not loopCity.isHasReligion(iReligion):

										# mission automatically
										if loopCity.plot().getArea() != pUnit.plot().getArea():
												loopCity.setHasReligion(iReligion, 1, 1, 0)
												return

						(loopCity, pIter) = pPlayer.nextCity(pIter, False)
				# Cities of vassals
				iPlayerTeam = pPlayer.getTeam()
				iRange = gc.getMAX_PLAYERS()
				for iVassal in range(iRange):
						pVassal = gc.getPlayer(iVassal)
						if pVassal.isAlive():
								iVassalTeam = pVassal.getTeam()
								pVassalTeam = gc.getTeam(iVassalTeam)
								if pVassalTeam.isVassal(iPlayerTeam):
										(loopCity, pIter) = pVassal.firstCity(False)
										while loopCity:
												if not loopCity.isNone():
														if not loopCity.isHasReligion(iReligion):

																# mission automatically
																if loopCity.plot().getArea() != pUnit.plot().getArea():
																		loopCity.setHasReligion(iReligion, 1, 1, 0)
																		return

												(loopCity, pIter) = pVassal.nextCity(pIter, False)

		def getBuildingClassCountPlusOtherCitiesMaking(self, pPlayer, pCity, eBuilding, eBuildingClass):
				iAnzB = pPlayer.getBuildingClassCountPlusMaking(eBuildingClass)
				for iOrderCurrentCity in range(pCity.getOrderQueueLength()):
						pOrder = pCity.getOrderFromQueue(iOrderCurrentCity)
						if pOrder.eOrderType == OrderTypes.ORDER_CONSTRUCT and pOrder.iData1 == eBuilding:
								iAnzB -= 1
								break
				return iAnzB
