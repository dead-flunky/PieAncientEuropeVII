# Trade and Cultivation feature
# From BoggyB

# Imports
from CvPythonExtensions import (CyGlobalContext, CyInterface,
																CyTranslator, DomainTypes, CyMap,
																ColorTypes, CyPopupInfo,
																ButtonPopupTypes, plotXY)
# import CvEventInterface
import CvUtil

import PAE_Unit
import PAE_Trade
import PAE_Lists as L
# Defines
gc = CyGlobalContext()

# Update (Ramk): CvUtil-Functions unpack an dict. You could directly use int, etc.
# Used keys for UnitScriptData:
# "b": index of bonus stored in merchant/cultivation unit (only one at a time)


def _getCitiesInRange(pPlot, iPlayer):
		iX = pPlot.getX()
		iY = pPlot.getY()
		lCities = []
		iRange = 2
		for x in range(-iRange, iRange+1):
				for y in range(-iRange, iRange+1):
						# Ecken weglassen
						if (x == -2 or x == 2) and (y == -2 or y == 2):
								continue
						pLoopPlot = plotXY(iX, iY, x, y)
						if pLoopPlot is not None and not pLoopPlot.isNone():
								# if (iPlayer == -1 or pLoopPlot.getOwner() == iPlayer) and pLoopPlot.isCity():
								if pLoopPlot.getOwner() == iPlayer and pLoopPlot.isCity():
										lCities.append(pLoopPlot.getPlotCity())
		return lCities

# iTyp: grain/livestock or strategic (horse, camel, ele, dog)


def _isCityCultivationPossible(pCity, iTyp):
		iMax = getCityCultivationAmount(pCity, iTyp)
		iBonusAnzahl = getCityCultivatedBonuses(pCity, iTyp)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, pCity.getName() + " iTyp:  " + str(iTyp) + " iBonusAnzahl:  " + str(iBonusAnzahl) + " iMax: " + str(iMax), None, 2, None, ColorTypes(10), 0, 0, False, False)
		return iBonusAnzahl < iMax


def _isCityCultivationPossibleCoast(pCity, eBonus):
		if not pCity.isCoastal(4):
				return False
		if isCityHasBonus(pCity, eBonus):
				return False
		return True


def getCityCultivationAmount(pCity, iTyp):
		# 1: wenn sich alles konkurrieren soll
		if iTyp == 1:
				return 4
		if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_METROPOLE")):
				iAnz = 4
		elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZ")):
				iAnz = 3
		elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STADT")):
				iAnz = 2
		else:
				iAnz = 1
		return iAnz


def getCityCultivatedBonuses(pCity, iTyp):
		if iTyp == -1:
				List = L.LBonusStratCultivatable + L.LBonusCultivatable + L.LBonusCultivatableCoast
		elif iTyp == 1:
				List = L.LBonusStratCultivatable
		else:
				List = L.LBonusCultivatable #+ L.LBonusCultivatableCoast
		iAnz = 0
		for i in range(gc.getNUM_CITY_PLOTS()):
				pLoopPlot = pCity.getCityIndexPlot(i)
				if pLoopPlot and not pLoopPlot.isNone():
						iLoopBonus = pLoopPlot.getBonusType(-1)
						if iTyp != -1 and iLoopBonus in L.LBonusPlantation:
								continue  # nur wenns ein Limit pro Stadtstufe gibt
						elif iLoopBonus in List:  # and pCity.canWork(pLoopPlot => Nicht, weil sonst viel mehr verbreitet werden kann
								iAnz += 1
		return iAnz


def getCityCultivatedPlots(pCity, eBonus):
		if eBonus == -1:
				List = L.LBonusStratCultivatable + L.LBonusCultivatable + L.LBonusCultivatableCoast
		else:
				iTyp = getBonusCultivationType(eBonus)
				if iTyp == 1:
						List = L.LBonusStratCultivatable
				else:
						List = L.LBonusCultivatable
		plots = []
		for i in range(gc.getNUM_CITY_PLOTS()):
				pLoopPlot = pCity.getCityIndexPlot(i)
				if pLoopPlot and not pLoopPlot.isNone():
						bonus = pLoopPlot.getBonusType(-1)
						if bonus in List:
								plots.append(pLoopPlot)
		return plots


def getCityCultivatablePlots(pCity, eBonus):
		iOwner = pCity.getOwner()
		plots = []
		for iI in range(gc.getNUM_CITY_PLOTS()):
				pLoopPlot = pCity.getCityIndexPlot(iI)
				if pLoopPlot and not pLoopPlot.isNone():
						ePlotBonus = pLoopPlot.getBonusType(-1)
						if ePlotBonus == eBonus:
								return []
						if ePlotBonus == eBonus or ePlotBonus == -1 and _isBonusCultivationChance(iOwner, pLoopPlot, eBonus, False, pCity):
								plots.append(pLoopPlot)
		return plots


def isCityHasBonus(pCity, eBonus):
		iAnz = 0
		for i in range(gc.getNUM_CITY_PLOTS()):
				pLoopPlot = pCity.getCityIndexPlot(i)
				if pLoopPlot is not None and not pLoopPlot.isNone():
						if pLoopPlot.getBonusType(-1) == eBonus or pLoopPlot.getBonusType(pLoopPlot.getTeam()) == eBonus:
								iAnz += 1
		return iAnz


def _isBonusCultivationChance(iPlayer, pPlot, eBonus, bVisibleOnly=True, pCity=None):
		"""
		Returns chance to cultivate eBonus on pPlot. Currently: either 0 (impossible) or 80 (possible)
		bVisibleOnly: Non-cultivatable bonuses cannot be replaced. If there is an invisible (tech reveal) bonus on pPlot, player receives NO information.
		In particular, the normal cultivation chance will be displayed, but bVisibleOnly=False prevents invisible bonus from removal.
		"""
		# iTyp 0 = Grain/Livestock 
		# iTyp 1 = Strategics (Horse, Camel, Elefant, Dog)
		iTyp = getBonusCultivationType(eBonus)
		if iTyp == 1:
				List = L.LBonusStratCultivatable
		else:
				List = L.LBonusCultivatable + L.LBonusCultivatableCoast

		# Variety of invalid situations
		if (eBonus not in List
				or pPlot is None or pPlot.isNone()
				or pPlot.getOwner() != iPlayer
				or pPlot.isCity()
				or pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_DARK_ICE")
				or pPlot.isPeak()
				):
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "peak/water/black ice", None, 2, None, ColorTypes(10), 0, 0, False, False)
				return False

		# Stadt auf ner Insel
		if pCity != None and eBonus not in L.LBonusCultivatableCoast:
				if pPlot.getArea() != pCity.plot().getArea():
						return False

		eTeam = -1
		if bVisibleOnly:
				eTeam = pPlot.getTeam()
		ePlotBonus = pPlot.getBonusType(eTeam)
		if ePlotBonus != -1 and (ePlotBonus not in List or ePlotBonus == eBonus):
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "uncultivatable bonus present", None, 2, None, ColorTypes(10), 0, 0, False, False)
				return False

		# Fertility conditions
		# or (eBonus in L.LBonusCorn and not pPlot.isFreshWater()) # siehe https://www.civforum.de/showthread.php?97599-PAE-Bonusressourcen&p=7653686&viewfull=1#post7653686
		if not canHaveBonus(pPlot, eBonus, True):
				return False

		# Auf Plots mit gleichem Typ darf immer gesetzt werden (City Limit muss hier nicht gecheckt werden)
		#if ePlotBonus in L.LBonusCorn and eBonus in L.LBonusCorn or ePlotBonus in L.LBonusLivestock and eBonus in L.LBonusLivestock:
		#		return True

		# Regel: Resourcen pro Stadt und dessen Status
		lCities = _getCitiesInRange(pPlot, iPlayer)
		for pCity in lCities:
				if eBonus in L.LBonusCultivatableCoast:
						if _isCityCultivationPossibleCoast(pCity, eBonus):
								return True
				elif eBonus in L.LBonusPlantation or eBonus in L.LBonusStratCultivatable:
						if not isCityHasBonus(pCity, eBonus):
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, pCity.getName() + " (*) true " + str(iTyp) + " | " + str(len(lCities)), None, 2, None, ColorTypes(10), 0, 0, False, False)
								return True

				# VARIANTE 1: Pro Stadt jedes Gut erlaubt
				#elif not isCityHasBonus(pCity, eBonus):
				#		return True

				# VARIANTE 2: Pro Stadtstufe kann eine bestimmte Anzahl verbreitet werden, aber jedes Bonusgut nur 1x
				elif not isCityHasBonus(pCity, eBonus):
						if _isCityCultivationPossible(pCity, iTyp):
								return True

				# VARIANTE 3: Pro Stadtstufe eine bestimmte Anzahl bestimmter Typen (Vieh oder Getreide) erlaubt
				#elif _isCityCultivationPossible(pCity, iTyp):
				#		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, pCity.getName() + " true " + str(iTyp) + " | " + str(len(lCities)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				#		return True

		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "no city in range has capacity " + str(iTyp), None, 2, None, ColorTypes(10), 0, 0, False, False)
		return False


def canHaveBonus(pPlot, eBonus, bIgnoreLatitude):
		"""Variation of the SDK version of the same name. Allows cultivation of ressources also if a non-fitting, removable feature is still on the plot (i.e. forest for wheat)"""
		if eBonus == -1:
				return True

		# ## ist hier schon was?
		# if pPlot.getBonusType() != -1:
				# return False
		# Gipfel
		if pPlot.isPeak():
				return False

		# wenn die Ressource auf Huegeln vorkommen muss
		if pPlot.isHills():
				if not gc.getBonusInfo(eBonus).isHills():
						return False
		# xor auf Flachland
		elif pPlot.isFlatlands():
				if not gc.getBonusInfo(eBonus).isFlatlands():
						return False

		# Falls die Ressource nicht am Flussufer vorkommen darf
		if gc.getBonusInfo(eBonus).isNoRiverSide():
				if pPlot.isRiverSide():
						return False

		# Ist die Insel gross genug
		if gc.getBonusInfo(eBonus).getMinAreaSize() != -1:
				if pPlot.area().getNumTiles() < gc.getBonusInfo(eBonus).getMinAreaSize():
						return False
						# Breitengrad
		if not bIgnoreLatitude:
				if pPlot.getLatitude() > gc.getBonusInfo(eBonus).getMaxLatitude():
						return False
				if pPlot.getLatitude() < gc.getBonusInfo(eBonus).getMinLatitude():
						return False
		# Von einem Landplot erreichbar? Nimmt keine Ruecksicht auf Gipfel oder sonstige Landfelder, auf denen man nicht gruenden kann.
		if not pPlot.isPotentialCityWork():
				return False

		# Sonderfaelle, die nicht im XML einstellbar sind
		# or (eBonus == gc.getInfoTypeForString("BONUS_DATTELN") and not pPlot.isFreshWater())
		# or (eBonus == gc.getInfoTypeForString("BONUS_GRAPES") and not pPlot.isFreshWater())
		if eBonus == gc.getInfoTypeForString("BONUS_OLIVES") and not pPlot.isCoastalLand():
				return False

		# Bei Eles muss ein Dschungel auf dem Terrain sein
		if eBonus == gc.getInfoTypeForString("BONUS_IVORY") and pPlot.getFeatureType() != gc.getInfoTypeForString("FEATURE_JUNGLE"):
				return False

		# Kamele nicht auf Oasen oder Schwemmland
		if eBonus == gc.getInfoTypeForString("BONUS_CAMEL"):
				if pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_OASIS") or pPlot.getFeatureType() == gc.getInfoTypeForString("FEATURE_FLOOD_PLAINS"):
						return False

		# Pferde nicht auf bebauten Bauernhoefen zulassen
		#if eBonus == gc.getInfoTypeForString("BONUS_HORSE") and pPlot.getImprovementType() == gc.getInfoTypeForString("IMPROVEMENT_FARM"):
		#		return False

		if eBonus == gc.getInfoTypeForString("BONUS_CAMEL") or eBonus == gc.getInfoTypeForString("BONUS_HORSE"):
				if pPlot.getBonusType(-1) != -1: return False

		# wenn das Terrain passt
		if gc.getBonusInfo(eBonus).isTerrain(pPlot.getTerrainType()):
				return True

		# wenn das Feature zum Terrain passt
		if pPlot.getFeatureType() != -1:
				if gc.getBonusInfo(eBonus).isFeature(pPlot.getFeatureType()):
						if gc.getBonusInfo(eBonus).isFeatureTerrain(pPlot.getTerrainType()):
								return True

		return False


def doCultivateBonus(pPlot, pUnit, eBonus, replace=False):
		# Dertuek: replace fix
		"""Cultivates eBonus on current plot (80% chance). Unit does not need to stand on pPlot (cultivation from city)"""
		if pPlot is None or pUnit is None or eBonus == -1:
				return False

		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		bOnlyVisible = False
		bCanCultivate = replace or _isBonusCultivationChance(iPlayer, pPlot, eBonus, bOnlyVisible, None)
		if eBonus in L.LBonusLivestock:
				iChance = 100
		elif not pPlayer.hasBonus(eBonus):
				iChance = 100
		elif eBonus in L.LBonusStratCultivatable:
				iChance = 100
		else:
				iChance = 80
		#CyInterface().addMessage(iPlayer, True, 10, str(eBonus), None, 2, None, ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
		if bCanCultivate:
				if CvUtil.myRandom(100, "doCultivateBonus") < iChance:
						pPlot.setBonusType(eBonus)
						if pUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
								pPlot.setImprovementType(gc.getInfoTypeForString("IMPROVEMENT_FISHING_BOATS"))
						if pPlayer.isHuman():
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_POPUP_BONUSVERBREITUNG_DONE", (gc.getBonusInfo(eBonus).getDescription(),)),
																				 None, 2, gc.getBonusInfo(eBonus).getButton(), ColorTypes(8), pPlot.getX(), pPlot.getY(), True, True)
						# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
						pUnit.kill(True, -1)  # RAMK_CTD
				else:
						CvUtil.removeScriptData(pUnit, "b")
						# DERTUEK
						CvUtil.removeScriptData(pUnit, "x")
						CvUtil.removeScriptData(pUnit, "y")
						CvUtil.removeScriptData(pUnit, "originCiv")

						if pPlayer.isHuman():
								if pPlot.isCity():
										pCity = pPlot.getPlotCity()
								else:
										pCity = pPlot.getWorkingCity()
								if eBonus in L.LBonusCultivatableCoast:
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_INFO_BONUSVERBREITUNG_NEG2", (gc.getBonusInfo(eBonus).getDescription(), pCity.getName())),
																						 None, 2, gc.getBonusInfo(eBonus).getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
								else:
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_INFO_BONUSVERBREITUNG_NEG", (gc.getBonusInfo(eBonus).getDescription(), pCity.getName())),
																						 None, 2, gc.getBonusInfo(eBonus).getButton(), ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
						pUnit.finishMoves()
						PAE_Unit.doGoToNextUnit(pUnit)
		return bCanCultivate


def getCityCultivationPlot(pCity, eBonus):
		"""
										Cultivates eBonus on random plot within radius of iRange around pUnit.
										Never replaces existing bonus.
		"""
		iPlayer = pCity.getOwner()
		lPrio1 = []  # Valid plot with correct improvement
		lPrio2 = []  # Valid plot without improvemnt
		lPrio3 = []  # with camps
		lPrio3Imps = [gc.getInfoTypeForString("IMPROVEMENT_CAMP"), gc.getInfoTypeForString("IMPROVEMENT_LUMBER_CAMP")]
		lPrio4 = []  # with quarries or mines
		lPrio4Imps = [gc.getInfoTypeForString("IMPROVEMENT_QUARRY"), gc.getInfoTypeForString("IMPROVEMENT_MINE")]
		lPrio5 = []  # gc.getImprovementInfo(iImprovement).getDefenseModifier(): villages, forts

		for iI in range(gc.getNUM_CITY_PLOTS()):
				pLoopPlot = pCity.getCityIndexPlot(iI)
				if pLoopPlot is not None and not pLoopPlot.isNone():
						ePlotBonus = pLoopPlot.getBonusType(-1)
						if ePlotBonus == -1 and _isBonusCultivationChance(iPlayer, pLoopPlot, eBonus, False, pCity):
								iImprovement = pLoopPlot.getImprovementType()
								if iImprovement != -1 and gc.getImprovementInfo(iImprovement).isImprovementBonusMakesValid(eBonus):
										lPrio1.append(pLoopPlot)
								elif iImprovement == -1:
										lPrio2.append(pLoopPlot)
								elif iImprovement in lPrio3Imps:
										lPrio3.append(pLoopPlot)
								elif iImprovement in lPrio4Imps:
										lPrio4.append(pLoopPlot)
								elif gc.getImprovementInfo(iImprovement).getDefenseModifier() > 0:
										lPrio5.append(pLoopPlot)

		lPlotList = []
		if len(lPrio1):
				lPlotList = lPrio1
		elif len(lPrio2):
				lPlotList = lPrio2
		elif len(lPrio3):
				lPlotList = lPrio3
		elif len(lPrio4):
				lPlotList = lPrio4
		elif len(lPrio5):
				lPlotList = lPrio5

		if len(lPlotList):
				return lPlotList[CvUtil.myRandom(len(lPlotList), "getCityCultivationPlot")]
		return None

# Returns list of bonuses which can be cultivated by this particular cultivation unit
# Checks fertility conditions AND unit store
# if iIsCity == 1, 5x5 square is checked. Otherwise: Only current plot.


def isBonusCultivatable(pUnit):
		if not pUnit.getUnitType() in L.LCultivationUnits + L.LTradeUnits:
				return False

		eBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
		if eBonus == -1:
				return False

		pPlot = pUnit.plot()
		if pPlot.isCity():
				# Cultivation from city (comfort function), no replacement of existing bonuses
				return _bonusIsCultivatableFromCity(pUnit.getOwner(), pPlot.getPlotCity(), eBonus, False)
		# Cultivation on current plot, bonus can be replaced (player knows what he's doing)
		return _isBonusCultivationChance(pUnit.getOwner(), pPlot, eBonus, False, None)

# Returns True if eBonus can be (principally) cultivated by iPlayer from pCity
# Independent from cultivation unit, only checks fertility conditions


def _bonusIsCultivatableFromCity(iPlayer, pCity, eBonus, bVisibleOnly=True):
		for iI in range(gc.getNUM_CITY_PLOTS()):
				pLoopPlot = pCity.getCityIndexPlot(iI)
				if pLoopPlot is not None and not pLoopPlot.isNone():
						ePlotBonus = pLoopPlot.getBonusType(-1)
						if ePlotBonus == -1 and _isBonusCultivationChance(iPlayer, pLoopPlot, eBonus, bVisibleOnly, pCity):
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, pCity.getName() + ": true  ", None, 2, None, ColorTypes(10), 0, 0, False, False)
								return True
		return False


# returns best plot within city radius
def AI_bestCultivation(pCity, iSkipN=-1, eBonus=-1):
		iPlayer = pCity.getOwner()
		if eBonus != -1:
				for iPass in range(2):
						for iI in range(gc.getNUM_CITY_PLOTS()):
								pLoopPlot = pCity.getCityIndexPlot(iI)
								if pLoopPlot is not None and not pLoopPlot.isNone():
										ePlotBonus = pLoopPlot.getBonusType(pLoopPlot.getTeam())
										eImprovement = pLoopPlot.getImprovementType()
										bAlreadyImproved = False
										if eImprovement != -1 and gc.getImprovementInfo(eImprovement).isImprovementBonusTrade(eBonus):
												bAlreadyImproved = True
										# first pass: only plots without bonus or its improvement
										if ePlotBonus == -1 or bAlreadyImproved or iPass > 0:
												# second pass: no improved plots or matching improved plots
												if eImprovement == -1 or bAlreadyImproved or iPass > 0:
														if _isBonusCultivationChance(iPlayer, pLoopPlot, eBonus, False, pCity):
																if iSkipN > 0:
																		iSkipN -= 1
																		continue
																if iSkipN <= 0:
																		return pLoopPlot
		else:
				return None
				# TODO: find overall best plot, i.e. prefer food and rare resources

# Lets pUnit cultivate bonus at nearest city


def doCultivation_AI(pUnit):

		if not pUnit.getUnitType() in L.LCultivationUnits:
				return False

		# do not check every turn
		if gc.getGame().getGameTurn() % 5 != 0:
				return False

		lFood = L.LBonusCorn + L.LBonusLivestock + L.LBonusPlantation

		pUnitPlot = pUnit.plot()
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		eBonusOnBoard = CvUtil.getScriptData(pUnit, ["b"], -1)
		# if eBonusOnBoard == -1: return False
		# iTyp = getBonusCultivationType(eBonusOnBoard)

		lCities = []
		# list of player's cities with distance (2-tuples (distance, city))
		# The nearest city which can still cultivate a bonus is chosen.
		(loopCity, pIter) = pPlayer.firstCity(False)
		while loopCity:

				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "doCultivation_AI: City: " + loopCity.getName() + " " + str(_isCityCultivationPossible(loopCity)), None, 2, None, ColorTypes(2), 0, 0, False, False)

				iValue = 0
				pCityPlot = loopCity.plot()
				iDistance = CyMap().calculatePathDistance(pUnitPlot, pCityPlot)
				# exclude unreachable cities
				if iDistance != -1:
						if eBonusOnBoard in L.LBonusCultivatableCoast:
								if _isCityCultivationPossibleCoast(loopCity, eBonusOnBoard):
										if iDistance == 0:
												iValue = 1
										else:
												iValue = 1/iDistance
						elif eBonusOnBoard in L.LBonusPlantation:
								if not isCityHasBonus(loopCity, eBonusOnBoard):
										if iDistance == 0:
												iValue = 1
										else:
												iValue = 1/iDistance

						# VARIANTE 1: Jedes Bonusgut darf 1x pro Stadt verbreitet werden
						elif not isCityHasBonus(loopCity, eBonusOnBoard):
								if iDistance == 0:
										iValue = 2
								else:
										iValue = 1/iDistance

						# VARIANTE 2: Je nach Stadtstufe kann ein Gut 1x verbreitet werden
						#elif not isCityHasBonus(loopCity, eBonusOnBoard):
						#		if _isCityCultivationPossible(loopCity, iTyp):
						#				if iDistance == 0: iValue = 2
						#				else: iValue = 1/iDistance

						# VARIANTE 3: Je nach Stadtstufe kann ein Gut eines Typs (Getreide oder Vieh) x Mal verbreitet werden
						# elif _isCityCultivationPossible(loopCity, iTyp):
						#		if iDistance == 0: iValue = 2
						#		else: iValue = 1/iDistance
				if iValue != 0:
						lCities.append((iValue, loopCity))
				(loopCity, pIter) = pPlayer.nextCity(pIter, False)

		lSortedCities = sorted(lCities, key=lambda value: lCities[0], reverse=True)

		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "doCultivation_AI: Cities: " + str(len(lSortedCities)), None, 2, None, ColorTypes(2), 0, 0, False, False)

		for iTry in range(2):
				for tTuple in lSortedCities:
						pLoopCity = tTuple[1]
						if eBonusOnBoard != -1:
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "doCultivation_AI: Karren hat Bonusgut: " + gc.getBonusInfo(eBonusOnBoard).getDescription(), None, 2, None, ColorTypes(2), 0, 0, False, False)
								if _bonusIsCultivatableFromCity(iPlayer, pLoopCity, eBonusOnBoard, False):
										if pUnit.atPlot(pLoopCity.plot()):
												pPlot = getCityCultivationPlot(pLoopCity, eBonusOnBoard)
												if pPlot != None:
														doCultivateBonus(pPlot, pUnit, eBonusOnBoard, False)
										else:
												pUnit.getGroup().pushMoveToMission(pLoopCity.getX(), pLoopCity.getY())
										return True
						else:
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "doCultivation_AI: Karren hat keinen Bonus geladen.", None, 2, None, ColorTypes(2), 0, 0, False, False)

								lLocalCityBonuses = []
								pLocalCity = None
								if pUnitPlot.isCity():  # and iPlayer == pUnitPlot.getOwner():
										pLocalCity = pUnitPlot.getPlotCity()
										lLocalCityBonuses = _getCollectableGoods4Cultivation(pLocalCity, pUnit)

								lCityBonuses = _getCollectableGoods4Cultivation(pLoopCity, pUnit)  # bonuses that city has access to
								# bonuses for which fertility conditions are met
								lBonuses = []
								for eBonus in lCityBonuses+lLocalCityBonuses:
										# has this city capacity to cultivate?
										if _bonusIsCultivatableFromCity(iPlayer, pLoopCity, eBonus, False):
												lBonuses.append(eBonus)
								# prefer food if possible
								lFoodIntersect = CvUtil.getIntersection(lBonuses, lFood)
								if lFoodIntersect:
										lBonuses = lFoodIntersect

								# kauf was, das es hier gibt und dort gebraucht wird und los geht's
								for eBonus in lBonuses:
										iLocalPrice = -1
										iPrice = _calculateBonusBuyingPrice4Cultivation(eBonus, iPlayer, pLoopCity.plot())
										if eBonus in lLocalCityBonuses:
												iLocalPrice = _calculateBonusBuyingPrice4Cultivation(eBonus, iPlayer, pLocalCity.plot())
										if iLocalPrice != -1 and iLocalPrice <= iPrice:
												# buy here. wait if not enough money
												#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "doCultivation_AI: Karren beladet sich mit Bonusgut: " + gc.getBonusInfo(eBonus).getDescription(), None, 2, None, ColorTypes(2), 0, 0, False, False)
												doBuyBonus4Cultivation(pUnit, eBonus)
												pUnit.finishMoves()
												return True
										elif iPrice != -1:
												# move to destination
												#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, "doCultivation_AI: Karren jagt zur Stadt " + pLoopCity.getName(), None, 2, None, ColorTypes(2), 0, 0, False, False)
												pUnit.getGroup().pushMoveToMission(pLoopCity.getX(), pLoopCity.getY())
												return True
				# if we didn't find a city which could use the loaded bonus, delete it and refund the AI
				if eBonusOnBoard != -1:
						CvUtil.removeScriptData(pUnit, "b")
						# DERTUEK
						CvUtil.removeScriptData(pUnit, "x")
						CvUtil.removeScriptData(pUnit, "y")
						CvUtil.removeScriptData(pUnit, "originCiv")

						iPrice = PAE_Trade.getBonusValue(eBonusOnBoard)
						pPlayer.changeGold(iPrice)

		# TODO get a ship
		return False


# Collect bonus on current plot ('stored' in cultivation unit)
def doCollectBonus4Cultivation(pUnit):
		iTeam = pUnit.getTeam()
		pPlot = pUnit.plot()
		eBonus = pPlot.getBonusType(iTeam)  # If there is an invisible bonus on pPlot, it will not be removed
		if eBonus == -1:
				return False

		if eBonus not in L.LBonusCultivatable + L.LBonusStratCultivatable + L.LBonusCultivatableCoast:
				return False

		eUnitBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
		if eUnitBonus != -1:
				# TODO: Popup Ressource geladen, ueberschreiben?
				# CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Die Einheit hatte bereits eine Ressource geladen. Die ist jetzt futsch.",)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				return False

		# Bonusgut in den Karren laden
		CvUtil.addScriptData(pUnit, "b", eBonus)
		# Dertuek: Update the coordinates where the resource have been loaded
		CvUtil.addScriptData(pUnit, "x", pPlot.getX())
		CvUtil.addScriptData(pUnit, "y", pPlot.getY())
		# Dertuek: Remove potential infos from the previous cargo
		CvUtil.removeScriptData(pUnit, "originCiv")

		iPrice = 0
		# Bonusgut vom Plot entfernen, ausgenommen Handelsposten, um die Waren nicht "stehlen" zu können
		# PAE 6.4: vom Vasall: nix entfernen, Vasall bekommt Gold
		if pPlot.getOwner() != pUnit.getOwner():
				
				if pPlot.getOwner() != -1:
					iPrice = PAE_Trade.getBonusValue(eBonus)
					gc.getPlayer(pPlot.getOwner()).changeGold(iPrice)
					gc.getPlayer(pUnit.getOwner()).changeGold(-iPrice)

		elif pPlot.getImprovementType() != gc.getInfoTypeForString("IMPROVEMENT_HANDELSPOSTEN"):
				pPlot.setBonusType(-1)  # remove bonus

				# Modernisierung entfernen
				lImprovements = [
						gc.getInfoTypeForString("IMPROVEMENT_PASTURE"),
						gc.getInfoTypeForString("IMPROVEMENT_CAMP"),
						gc.getInfoTypeForString("IMPROVEMENT_OLIVE_PRESS"),
						gc.getInfoTypeForString("IMPROVEMENT_PLANTATION"),
						gc.getInfoTypeForString("IMPROVEMENT_WINERY"),
						gc.getInfoTypeForString("IMPROVEMENT_FISHING_BOATS")
				]
				if pPlot.getImprovementType() in lImprovements:
						pPlot.setImprovementType(-1)

		if gc.getPlayer(pUnit.getOwner()).isHuman():
				CyInterface().addMessage(pUnit.getOwner(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_TRADE_COLLECT_GOODS", (gc.getBonusInfo(
						eBonus).getDescription(), -iPrice)), "AS2D_COINS", 2, None, ColorTypes(13), pUnit.getX(), pUnit.getY(), False, False)

		pUnit.finishMoves()
		PAE_Unit.doGoToNextUnit(pUnit)
		return True

# List of selectable cultivation goods


def getCollectableGoods4Cultivation(pUnit):
		pPlot = pUnit.plot()
		if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				lGoods = _getCollectableGoods4Cultivation(pCity, pUnit)
		else:
				ePlotBonus = pPlot.getBonusType(pPlot.getTeam())
				if ePlotBonus != -1 and ePlotBonus in L.LBonusCultivatable:
						lGoods = [ePlotBonus]

		return lGoods

# Returns list of the cultivatable bonuses which pCity has access to / Liste kultivierbarer Ressis im Handelsnetz von pCity


def _getCollectableGoods4Cultivation(pCity, pUnit):
		lGoods = []
		LBonus = []
		if pUnit.getDomainType() == DomainTypes.DOMAIN_SEA:
				iTeam = gc.getPlayer(pUnit.getOwner()).getTeam()
				pTeam = gc.getTeam(iTeam)
				if pTeam.isHasTech(gc.getInfoTypeForString("TECH_AQUA")):
						LBonus = L.LBonusCultivatableCoast
		else:
				LBonus = L.LBonusCultivatable + L.LBonusStratCultivatable
		for eBonus in LBonus:
				if pCity.hasBonus(eBonus):
						lGoods.append(eBonus)
		return lGoods


def _calculateBonusBuyingPrice4Cultivation(eBonus, iBuyer, pPlot):
		"""
		# Price of cultivation goods
		# regional (on plot): *1
		# national: *2
		# international: *3
		"""
		iPrice = PAE_Trade.getBonusValue(eBonus)
		pCity = pPlot.getPlotCity()
		if pCity is None:
				# Bonus on plot: regional price
				if pPlot.getBonusType(pPlot.getTeam()) == eBonus:
						return iPrice
				return -1

		if not pCity.hasBonus(eBonus):
				return -1

		# Bonus in city radius: regional price
		for iI in range(gc.getNUM_CITY_PLOTS()):
				pLoopPlot = pCity.getCityIndexPlot(iI)
				if pLoopPlot is not None and not pLoopPlot.isNone():
						if pLoopPlot.getBonusType(pLoopPlot.getTeam()) == eBonus:
								return iPrice

		# Bonus in realm: national price
		iRange = CyMap().numPlots()
		for iI in range(iRange):
				pLoopPlot = CyMap().plotByIndex(iI)
				if pLoopPlot.getOwner() == iBuyer:
						if pLoopPlot.getBonusType(pLoopPlot.getTeam()) == eBonus:
								return iPrice * 2

		# Bonus international
		return iPrice * 3


def doBuyBonus4Cultivation(pUnit, eBonus):
		if not pUnit.getUnitType() in L.LCultivationUnits + L.LTradeUnits:
				return False
		if eBonus == -1:
				return False

		iBuyer = pUnit.getOwner()

		eUnitBonus = CvUtil.getScriptData(pUnit, ["b"], -1)
		if eBonus == eUnitBonus:
				#CyInterface().addMessage(iBuyer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Das haben wir bereits geladen.",)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				return False
		if eUnitBonus != -1:
				# TODO: Popup Ressource geladen, ueberschreiben?
				#CyInterface().addMessage(iBuyer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Die Einheit hat bereits eine Ressource geladen.",)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				return False

		iPrice = _calculateBonusBuyingPrice4Cultivation(eBonus, iBuyer, pUnit.plot())
		if iPrice == -1:
				return False

		pBuyer = gc.getPlayer(iBuyer)
		if pBuyer.getGold() < iPrice:
				CyInterface().addMessage(iBuyer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TRADE_COLLECT_NO_GOODS", ("",)),
																 None, 2, "Art/Interface/PlotPicker/Warning.dds", ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)
				return False

		pBuyer.changeGold(-iPrice)
		CvUtil.addScriptData(pUnit, "b", eBonus)
		# Dertuek: Update the coordinates where the resource have been loaded
		CvUtil.addScriptData(pUnit, "x", pUnit.getX())
		CvUtil.addScriptData(pUnit, "y", pUnit.getY())
		CvUtil.addScriptData(pUnit, "originCiv", pUnit.plot().getOwner())

		if pBuyer.isHuman():
				CyInterface().addMessage(iBuyer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_TRADE_COLLECT_GOODS", (gc.getBonusInfo(
						eBonus).getDescription(), -iPrice)), "AS2D_COINS", 2, None, ColorTypes(13), pUnit.getX(), pUnit.getY(), False, False)

		pUnit.finishMoves()
		PAE_Unit.doGoToNextUnit(pUnit)
		return True

# Creates popup with all possible cultivation bonuses of the plot or city


def doPopupChooseBonus4Cultivation(pUnit):
		if pUnit is None or pUnit.isNone():
				return False
		pPlot = pUnit.plot()
		iPlayer = pUnit.getOwner()

		lGoods = getCollectableGoods4Cultivation(pUnit)

		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TRADE_CHOOSE_BONUS", ("", )))
		popupInfo.setOnClickedPythonCallback("popupTradeChooseBonus4Cultivation")
		popupInfo.setData1(iPlayer)
		popupInfo.setData2(pUnit.getID())

		for eBonus in lGoods:
				sBonusDesc = gc.getBonusInfo(eBonus).getDescription()
				iPrice = _calculateBonusBuyingPrice4Cultivation(eBonus, iPlayer, pPlot)
				iNumBonus = gc.getPlayer(iPlayer).countOwnedBonuses(eBonus)
				sText = CyTranslator().getText("TXT_KEY_BUY_BONUS", (sBonusDesc, iPrice, iNumBonus))
				if not _isBonusCultivableInRealm(iPlayer, eBonus):
						sText += u"\n<color=255,0,0,0><font=2>" + CyTranslator().getText("TXT_KEY_BONUS_NOT_CULTIVABLE", ()) + u"</font></color>"
				sBonusButton = gc.getBonusInfo(eBonus).getButton()
				popupInfo.addPythonButton(sText, sBonusButton)

		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ("", )), "Art/Interface/Buttons/Actions/Cancel.dds")
		popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
		popupInfo.addPopup(iPlayer)


def _isBonusCultivableInRealm(iPlayer, eBonus):
		pPlayer = gc.getPlayer(iPlayer)
		(loopCity, pIter) = pPlayer.firstCity(False)
		while loopCity:
				if not loopCity.isNone() and loopCity.getOwner() == pPlayer.getID():
						for iI in range(gc.getNUM_CITY_PLOTS()):
								pLoopPlot = loopCity.getCityIndexPlot(iI)
								if pLoopPlot is not None and not pLoopPlot.isNone():
										if _isBonusCultivationChance(iPlayer, pLoopPlot, eBonus, True, loopCity):
												return True
				(loopCity, pIter) = pPlayer.nextCity(pIter, False)
		return False


def wine(pCity):
		iPlayer = pCity.getOwner()
		# pPlayer = gc.getPlayer(iPlayer)
		eBonus = gc.getInfoTypeForString("BONUS_GRAPES")
		# sorted by priority
		lTerrains = [
				gc.getInfoTypeForString("TERRAIN_PLAINS"),
				gc.getInfoTypeForString("TERRAIN_GRASS")
		]
		iFirstBlock = len(lTerrains)
		# Improvements fuer Prioritaet
		lImprovements = [
				gc.getInfoTypeForString("IMPROVEMENT_CITY_RUINS"),
				gc.getInfoTypeForString("IMPROVEMENT_GOODY_HUT"),
				gc.getInfoTypeForString("IMPROVEMENT_LUMBER_CAMP"),
				gc.getInfoTypeForString("IMPROVEMENT_FARM"),
				gc.getInfoTypeForString("IMPROVEMENT_MINE"),
				gc.getInfoTypeForString("IMPROVEMENT_COTTAGE")
		]
		iSecondBlock = len(lImprovements)

		# lPlotPrio = [[],[],[],[],[],[],[],[],[]]
		lPlotPrio = [[] for x in range(0, iFirstBlock + iSecondBlock + 1)]

		for iI in range(gc.getNUM_CITY_PLOTS()):
				loopPlot = pCity.getCityIndexPlot(iI)
				# die beste position finden:
				if loopPlot is not None and not loopPlot.isNone():
						# wenn bereits eine Weinressource im Umkreis der Stadt ist
						if loopPlot.getBonusType(-1) == eBonus:
								return []
						if loopPlot.getTerrainType() in lTerrains:
								if loopPlot.isHills():
										if loopPlot.getOwner() == pCity.getOwner():
												# damit es nicht auf Inseln aufploppt
												if loopPlot.getArea() == pCity.plot().getArea():
														if canHaveBonus(loopPlot, eBonus, True):
																if _canBuildingCultivate(loopPlot, iPlayer):
																		if loopPlot.getImprovementType() == -1:
																				if loopPlot.isHills():
																						for iJ in range(iFirstBlock):
																								if loopPlot.getTerrainType() == lTerrains[iJ]:
																										lPlotPrio[iJ].append(loopPlot)
																				# 3. irgendeinen passenden ohne Improvement
																				else:
																						lPlotPrio[iFirstBlock].append(loopPlot)
																		# 4. nach Improvements selektieren
																		else:
																				for iJ in range(iSecondBlock):
																						if loopPlot.getImprovementType() == lImprovements[iJ]:
																								lPlotPrio[iJ + iFirstBlock + 1].append(loopPlot)
																								break
		return trimPlots(lPlotPrio)


def horse(pCity, bPrioPlotOnly):
		iPlayer = pCity.getOwner()
		eBonus = gc.getInfoTypeForString("BONUS_HORSE")

		bIsHuman = gc.getPlayer(iPlayer).isHuman()

		# wenn es bereits ein Bonusgut im eigenen Territorium gibt
		# if seekBonusOnOwnedPlots(eBonus, iPlayer): return []

		# sorted by priority
		lTerrains = [
				gc.getInfoTypeForString("TERRAIN_PLAINS"),
				gc.getInfoTypeForString("TERRAIN_GRASS")
		]
		iFirstBlock = len(lTerrains)

		# Improvements fuer Prioritaet
		# sorted by priority
		lImprovements = [
				gc.getInfoTypeForString("IMPROVEMENT_CITY_RUINS"),
				gc.getInfoTypeForString("IMPROVEMENT_GOODY_HUT"),
				gc.getInfoTypeForString("IMPROVEMENT_CAMP"),
				gc.getInfoTypeForString("IMPROVEMENT_QUARRY"),
				gc.getInfoTypeForString("IMPROVEMENT_COTTAGE"),
				gc.getInfoTypeForString("IMPROVEMENT_LUMBER_CAMP"),
				gc.getInfoTypeForString("IMPROVEMENT_HAMLET")
		]
		iSecondBlock = len(lImprovements)

		# lPlotPrio = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
		lPlotPrio = [[] for x in range(0, iFirstBlock + iSecondBlock + 1)]
		lAllPossiblePlots = []

		for iI in range(gc.getNUM_CITY_PLOTS()):
				loopPlot = pCity.getCityIndexPlot(iI)
				# die beste position finden:
				if loopPlot is not None and not loopPlot.isNone():
						if loopPlot.getBonusType(-1) in L.LBonusStratCultivatable and loopPlot.getBonusType(-1) != eBonus:
								return []
						elif loopPlot.getTerrainType() in lTerrains:
								if loopPlot.getOwner() == pCity.getOwner():
										# damit es nicht auf Inseln aufploppt
										if loopPlot.getArea() == pCity.plot().getArea():
												if canHaveBonus(loopPlot, eBonus, True):
														if _canBuildingCultivate(loopPlot, iPlayer):
																lAllPossiblePlots.append(loopPlot)
																if loopPlot.getImprovementType() == -1:
																		for iJ in range(iFirstBlock):
																				if loopPlot.getTerrainType() == lTerrains[iJ]:
																						if loopPlot.getFeatureType() == -1:
																								lPlotPrio[0].append(loopPlot)
																						else:
																								lPlotPrio[1].append(loopPlot)
																						break
																# nach Improvements selektieren
																elif not bIsHuman:
																		for iJ in range(iSecondBlock):
																				if loopPlot.getImprovementType() == lImprovements[iJ]:
																						lPlotPrio[iJ + iFirstBlock + 1].append(loopPlot)
		if bPrioPlotOnly:
				return trimPlots(lPlotPrio)
		else:
				return lAllPossiblePlots


def camel(pCity, bPrioPlotOnly):
		iPlayer = pCity.getOwner()
		eBonus = gc.getInfoTypeForString("BONUS_CAMEL")

		# Improvements fuer Prioritaet
		iImpType1 = gc.getInfoTypeForString("IMPROVEMENT_CAMP")
		# sorted by priority
		lTerrains = [
				gc.getInfoTypeForString("TERRAIN_DESERT")
		]
		lFeatures = [
				gc.getInfoTypeForString("FEATURE_OASIS"),
				gc.getInfoTypeForString("FEATURE_FLOOD_PLAINS"),
				gc.getInfoTypeForString("FEATURE_DARK_ICE")
		]
		iFirstBlock = len(lTerrains)

		# lPlotPrio = [[],[],[],[],[]]
		lPlotPrio = [[] for x in range(0, iFirstBlock + 3)]
		lAllPossiblePlots = []

		for iI in range(gc.getNUM_CITY_PLOTS()):
				loopPlot = pCity.getCityIndexPlot(iI)
				# die beste position finden:
				if loopPlot is not None and not loopPlot.isNone():
						if loopPlot.getBonusType(-1) in L.LBonusStratCultivatable and loopPlot.getBonusType(-1) != eBonus:
								return []
						elif not loopPlot.isHills():
								if loopPlot.getTerrainType() in lTerrains:
										if loopPlot.getOwner() == pCity.getOwner():
												if loopPlot.getFeatureType() not in lFeatures:
														if loopPlot.getArea() == pCity.plot().getArea():
																if canHaveBonus(loopPlot, eBonus, True):
																		if _canBuildingCultivate(loopPlot, iPlayer):
																				lAllPossiblePlots.append(loopPlot)
																				# 1. nach Improvements selektieren
																				if loopPlot.getImprovementType() == iImpType1:
																						lPlotPrio[0].append(loopPlot)
																				elif loopPlot.getImprovementType() == -1:
																						for iJ in range(iFirstBlock):
																								if loopPlot.getTerrainType() == lTerrains[iJ]:
																										lPlotPrio[iJ+1].append(loopPlot)
																										break
																								# 4. irgendeinen passenden ohne Improvement
																								else:
																										lPlotPrio[iFirstBlock+1].append(loopPlot)
																				else:
																						lPlotPrio[iFirstBlock+2].append(loopPlot)
		if bPrioPlotOnly:
				return trimPlots(lPlotPrio)
		else:
				return lAllPossiblePlots


def elephant(pCity, bPrioPlotOnly):
		iPlayer = pCity.getOwner()

		lFeatures = [
				gc.getInfoTypeForString("FEATURE_JUNGLE")
		]
		iFirstBlock = len(lFeatures)
		lTerrains = [
				gc.getInfoTypeForString("TERRAIN_GRASS"),
				gc.getInfoTypeForString("TERRAIN_PLAINS")
		]
		iSecondBlock = len(lTerrains)

		eBonus = gc.getInfoTypeForString("BONUS_IVORY")

		# Improvements fuer Prioritaet
		iImpCamp = gc.getInfoTypeForString("IMPROVEMENT_CAMP")

		# lPlotPrio = [[],[],[],[],[],[],[]]
		lPlotPrio = [[] for x in range(0, iFirstBlock + iSecondBlock + 3)]
		lAllPossiblePlots = []

		for iI in range(gc.getNUM_CITY_PLOTS()):
				loopPlot = pCity.getCityIndexPlot(iI)
				# die beste position finden:
				if loopPlot is not None and not loopPlot.isNone():
						if loopPlot.getBonusType(-1) in L.LBonusStratCultivatable and loopPlot.getBonusType(-1) != eBonus:
								return []
						elif not loopPlot.isHills():
								if loopPlot.getOwner() == pCity.getOwner():
										if loopPlot.getTerrainType() in lTerrains and loopPlot.getFeatureType() in lFeatures:
												if loopPlot.getArea() == pCity.plot().getArea():
														if canHaveBonus(loopPlot, eBonus, True):
																if _canBuildingCultivate(loopPlot, iPlayer):
																		lAllPossiblePlots.append(loopPlot)
																		if loopPlot.getImprovementType() == -1:
																				if loopPlot.getFeatureType() in lFeatures:
																						# 1. jungle, unworked
																						for iJ in range(iFirstBlock):
																								if loopPlot.getFeatureType() == lFeatures[iJ]:
																										lPlotPrio[iJ].append(loopPlot)
																										break
																				elif loopPlot.getTerrainType() in lTerrains:
																						# 2. grass, unworked
																						# 3. plains, unworked
																						for iJ in range(iSecondBlock):
																								if loopPlot.getTerrainType() == lTerrains[iJ]:
																										lPlotPrio[iJ + iFirstBlock + 1].append(loopPlot)
																										break
																				else:
																						# 4. irgendeinen passenden ohne Improvement
																						lPlotPrio[iFirstBlock + iSecondBlock + 1].append(loopPlot)
																		# 3. nach Improvements selektieren
																		elif loopPlot.getImprovementType() == iImpCamp:
																				lPlotPrio[iFirstBlock].append(loopPlot)
																		# 7. irgendeinen passenden mit falschem Improvement
																		# TODO: kann gewachsene Huetten zerstoeren
																		else:
																				lPlotPrio[iFirstBlock + iSecondBlock + 2].append(loopPlot)
		if bPrioPlotOnly:
				return trimPlots(lPlotPrio)
		else:
				return lAllPossiblePlots


def dog(pCity, bPrioPlotOnly):
		iPlayer = pCity.getOwner()
		eBonus = gc.getInfoTypeForString("BONUS_HUNDE")

		# wenn es bereits ein Bonusgut im eigenen Territorium gibt
		# if seekBonusOnOwnedPlots(eBonus, iPlayer): return []

		lTerrains = [
				gc.getInfoTypeForString("TERRAIN_TUNDRA"),
				gc.getInfoTypeForString("TERRAIN_PLAINS"),
				gc.getInfoTypeForString("TERRAIN_GRASS"),
		]
		iFirstBlock = len(lTerrains)

		# Improvements fuer Prioritaet
		lImprovements = [
				gc.getInfoTypeForString("IMPROVEMENT_CITY_RUINS"),
				# gc.getInfoTypeForString("IMPROVEMENT_GOODY_HUT"),
				gc.getInfoTypeForString("IMPROVEMENT_CAMP"),
				gc.getInfoTypeForString("IMPROVEMENT_LUMBER_CAMP"),
				gc.getInfoTypeForString("IMPROVEMENT_FARM"),
				gc.getInfoTypeForString("IMPROVEMENT_MINE"),
				gc.getInfoTypeForString("IMPROVEMENT_COTTAGE")
		]
		iSecondBlock = len(lImprovements)

		lPlotPrio = [[] for x in range(0, iFirstBlock + iSecondBlock + 1)]
		lAllPossiblePlots = []

		for iI in range(gc.getNUM_CITY_PLOTS()):
				loopPlot = pCity.getCityIndexPlot(iI)
				# die beste position finden:
				if loopPlot is not None and not loopPlot.isNone():
						# if loopPlot.getBonusType(-1) in L.LBonusStratCultivatable and loopPlot.getBonusType(-1) != eBonus: return []
						if loopPlot.getTerrainType() in lTerrains:
								if loopPlot.getOwner() == pCity.getOwner():
										if loopPlot.getArea() == pCity.plot().getArea():
												if canHaveBonus(loopPlot, eBonus, True):
														if _canBuildingCultivate(loopPlot, iPlayer):
																lAllPossiblePlots.append(loopPlot)
																# unworked
																if loopPlot.getImprovementType() == -1:
																		if not loopPlot.isHills():
																				for iJ in range(iFirstBlock):
																						if loopPlot.getTerrainType() == lTerrains[iJ]:
																								lPlotPrio[iJ].append(loopPlot)
																								break
																		# 3. irgendeinen passenden ohne Improvement
																		else:
																				lPlotPrio[iFirstBlock].append(loopPlot)
																# 4. nach Improvements selektieren
																else:
																		for iJ in range(iSecondBlock):
																				if loopPlot.getImprovementType() == lImprovements[iJ]:
																						lPlotPrio[iJ + iFirstBlock + 1].append(loopPlot)
		if bPrioPlotOnly:
				return trimPlots(lPlotPrio)
		else:
				return lAllPossiblePlots


def trimPlots(lPlots):
		if len(lPlots):
				for k in lPlots:
						if k:
								return k


def doBuildingCultivate(pCity, iBuildingType):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		# iImprovement = -1
		eBonus = -1
		bRemoveFeature = False
		bText = False
		sText = "dummy"
		lPlotPrio = []

		# WEIN - FEATURE ---------------------
		# Winzer / Vintager -> Winery / Weinverbreitung (Trauben)
		# if iBuildingType == gc.getInfoTypeForString("BUILDING_WINERY"):
		#    eBonus = gc.getInfoTypeForString("BONUS_GRAPES")
		#    if isCityHasBonus(pCity, eBonus): return
		#    if pCity.getNumBonuses(eBonus) < 3:
		#        lPlotPrio = wine(pCity)
		#        bRemoveFeature = True
		#        iImprovement = gc.getInfoTypeForString("IMPROVEMENT_WINERY")
		#        bText = True
		#        iRand = 1 + CvUtil.myRandom(4, "WeinText")
		#        sText = CyTranslator().getText("TXT_KEY_MESSAGE_VINTAGER_BUILT"+str(iRand), (pCity.getName(),))

		# HORSE - FEATURE ---------------------
		# Pferdeverbreitung
		# elif iBuildingType == gc.getInfoTypeForString("BUILDING_STABLE"):
		#    eBonus = gc.getInfoTypeForString("BONUS_HORSE")
		#    if isCityHasBonus(pCity, eBonus): return
		#    lPlotPrio = horse(pCity, True)
		#    bRemoveFeature = True
		#    iImprovement = gc.getInfoTypeForString("IMPROVEMENT_PASTURE")

		# KAMEL - FEATURE ---------------------
		# Kamelverbreitung
		# elif iBuildingType == gc.getInfoTypeForString("BUILDING_CAMEL_STABLE"):
		#    eBonus = gc.getInfoTypeForString("BONUS_CAMEL")
		#    if isCityHasBonus(pCity, eBonus): return
		#    lPlotPrio = camel(pCity, True)
		#    iImprovement = gc.getInfoTypeForString("IMPROVEMENT_CAMP")

		# ELEFANT - FEATURE ---------------------
		# Elefantverbreitung
		# elif iBuildingType == gc.getInfoTypeForString("BUILDING_ELEPHANT_STABLE"):
		#    eBonus = gc.getInfoTypeForString("BONUS_IVORY")
		#    if isCityHasBonus(pCity, eBonus): return
		#    lPlotPrio = elephant(pCity, True)
		#    iImprovement = gc.getInfoTypeForString("IMPROVEMENT_CAMP")

		# HUNDE - FEATURE ---------------------
		# Hundeverbreitung
		if iBuildingType == gc.getInfoTypeForString("BUILDING_HUNDEZUCHT"):
				eBonus = gc.getInfoTypeForString("BONUS_HUNDE")
				if isCityHasBonus(pCity, eBonus):
						return
				lPlotPrio = dog(pCity, True)
				# iImprovement = gc.getInfoTypeForString("IMPROVEMENT_CAMP")

		if lPlotPrio and len(lPlotPrio):
				p = []
				for k in lPlotPrio:
						if k:
								p.append(k)

				iLen = len(p)
				if iLen:
						if iLen < 2:
								pPlot = p[0]
						else:
								pPlot = p[CvUtil.myRandom(iLen, "Gebaeudeverbreitung")]
						pPlot.setBonusType(eBonus)
						# Modernisierung soll extra gebaut werden
						# pPlot.setImprovementType(iImprovement)
						# Feature (Wald) entfernen
						if bRemoveFeature:
								pPlot.setFeatureType(-1, 0)
						if bText and pPlayer.isHuman():
								CyInterface().addMessage(iPlayer, True, 10, sText, None, 2, gc.getBonusInfo(eBonus).getButton(), ColorTypes(8), pPlot.getX(), pPlot.getY(), True, True)
						return


def _canBuildingCultivate(pPlot, iPlayer):
		if not pPlot.isPeak():
				if pPlot.getBonusType(-1) == -1:
						if pPlot.getOwner() == iPlayer or pPlot.getOwner() == -1:
								if not pPlot.isCity():
										lFeatures = [
												gc.getInfoTypeForString("FEATURE_OASIS"),
												gc.getInfoTypeForString("FEATURE_FLOOD_PLAINS"),
												gc.getInfoTypeForString("FEATURE_DARK_ICE")
										]
										if pPlot.getFeatureType() not in lFeatures:
												return True
		return False


def seekBonusOnOwnedPlots(iBonus, iPlayer):
		iMapW = gc.getMap().getGridWidth()
		iMapH = gc.getMap().getGridHeight()
		iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")

		for x in range(iMapW):
				for y in range(iMapH):
						loopPlot = gc.getMap().plot(x, y)
						if loopPlot is not None and not loopPlot.isNone():
								if loopPlot.getFeatureType() == iDarkIce:
										continue
								if loopPlot.getOwner() == iPlayer:
										if loopPlot.getBonusType(-1) == iBonus:
												return True
		return False


def getBonusCultivationType(eBonus):
		if eBonus in L.LBonusStratCultivatable:
				return 1
		return 0
