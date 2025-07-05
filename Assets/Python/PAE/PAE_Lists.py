#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Listen die an diversen Stellen für Vergleiche genutzt werden.
# Zur Unterscheidung von lokalen Variablen beginnen sie mit einem
# Großbuchstaben.
# Namenkonventionen: Vorne L/D für list/dict und danach meist der in der
# Liste verwendete Typ, z.B. 'Impr' für IMPROVMENT_XYZ
#
# Diese Datei sollte nur einmal, in CvUtil, importiert werden.
#

# Wrap definition of values into init() because during loading stage
# getInfoTypeForString() returns always -1
from CvPythonExtensions import (CyGlobalContext,CyTranslator)
gc = CyGlobalContext()
localText = CyTranslator()

LGuerilla = []
LWoodsman = []
LJungle = []
LSwamp = []
LDesert = []
LTradeUnits = []
LCultivationUnits = []
LBonusCultivatable = []
LBonusCultivatableCoast = []
LBonusStrategic = []
LBonusStratCultivatable = []
LBonusUntradeable = []  # List of untradeable bonuses
LBonusCorn = []  # Lists of cultivatable bonuses
LBonusGetreide = []
LBonusLivestock = []
LBonusPlantation = []
LBonusLuxury = []  # List of bonuses which may create trade routes
LBonusRarity = []  # List of bonuses which may create trade routes
LBonus4Units = []  # List of bonus for better AI attitude
LUnitWarAnimals = []
LUnitLootLessSeaUnits = []
LUnitCanBeDomesticated = []
LUnitWildAnimals = []
DJagd = {}
LArcherCombats = []
LMeleeCombats = []
LMeleeSupplyCombats = []
LMountedSupplyCombats = []
LLimes = []
LBuildLimes = []
LImprFort = []
# LFeatureArray = []
LImprFortShort = []
LImprFortSentry = []
DCaptureFromPirate = {}
DCaptureByPirate = {}
LFormationNoNaval = []
LFormationMountedArcher = []
LCivPirates = []
LCivPartherschuss = []
LUnitPartherschuss = []
LKeilUnits = []
LNoSchildwallUnitClasses = []
LNoSchildwallUnits = []
LDrillUnits = []
LTestudoUnits = []
LUnits4Praetorians = []
LPraetorians = []
LFluchtCombats = []
LFormationen = []
LUnitsNoAIReservists = []
LUnitAuxiliar = []
LUnitNoSlaves = []
LCombatNoRuestung = []
LUnitNoRuestung = []
LUnitsHeadRang = []
LUnitSkirmish = []
LClassSkirmish = []
LFernangriffNoCosts = []
DFernangriffCosts = {}
LSeewind = []
LBuildArchers = []
LBuildCatapults = []
DManufakturen = {}
DImprSupplyBonus = {}
DBuildingPromo = {}
DPromosForPromoBuilding = {}
LVillages = []
LLatifundien = []
LFarms = []
LMines = []
LTemples = []
LPromoPillage = []
LWoodRemovedByLumberCamp = []
LCityGarrison = []
LVeteranForbiddenPromos = []
LVeteranForbiddenPromos1 = []
LCityRaider = []
LVeteranForbiddenPromos4 = []
LCivGermanen = []
DHorseDownMap = {}
DHorseUpMap = {}
LGGStoneAge = []
LGGStandard = []
DGGNames = {}
LRelisRemapCapital = []
LGreeks = []
LNearEast = []
LNorthern = []
LegioNames = []
LHeldendenkmal = []
LRankUnits = []
LNoRankUnits = []
LRankUnitBuilt = []
LAngstUnits = []
LUnitsNoFoodCosts = []
LCivsWithAqueduct = []
LCapitalPromoUpUnits = []
LMonoReligions = []
LForests = []
LFireUnits = []
LCamelUnits = []
LUnits4HorseSwap = []
LMovingBonus = []
LRammen = []
LInquisitors = []
LGlobalTechs = []


def init():
		global LGuerilla
		global LWoodsman
		global LJungle
		global LSwamp
		global LDesert
		global LTradeUnits
		global LCultivationUnits
		global LBonusCultivatable
		global LBonusCultivatableCoast
		global LBonusStrategic
		global LBonusStratCultivatable
		global LBonusUntradeable
		global LBonusCorn
		global LBonusGetreide
		global LBonusLivestock
		global LBonusPlantation
		global LBonusLuxury
		global LBonusRarity
		global LBonus4Units
		global LUnitWarAnimals
		global LUnitLootLessSeaUnits
		global LUnitCanBeDomesticated
		global LUnitWildAnimals
		global DJagd
		global LArcherCombats
		global LMeleeCombats
		global LMeleeSupplyCombats
		global LMountedSupplyCombats
		global LLimes
		global LBuildLimes
		global LImprFort
		global LImprFortSentry
		#global  LFeatureArray
		global LImprFortShort
		global DCaptureFromPirate
		global DCaptureByPirate
		global LFormationNoNaval
		global LFormationMountedArcher
		global LCivPirates
		global LCivPartherschuss
		global LUnitPartherschuss
		global LKeilUnits
		global LNoSchildwallUnitClasses
		global LNoSchildwallUnits
		global LDrillUnits
		global LTestudoUnits
		global LUnits4Praetorians
		global LPraetorians
		global LFluchtCombats
		global LFormationen
		global LUnitsNoAIReservists
		global LUnitAuxiliar
		global LUnitNoSlaves
		global LCombatNoRuestung
		global LUnitNoRuestung
		global LUnitsHeadRang
		global LUnitSkirmish
		global LClassSkirmish
		global LFernangriffNoCosts
		global DFernangriffCosts
		global LSeewind
		global LBuildArchers
		global LBuildCatapults
		global DManufakturen
		global DImprSupplyBonus
		global DBuildingPromo
		global DPromosForPromoBuilding
		global LVillages
		global LLatifundien
		global LFarms
		global LMines
		global LTemples
		global LPromoPillage
		global LWoodRemovedByLumberCamp
		global LCityGarrison
		global LVeteranForbiddenPromos
		global LVeteranForbiddenPromos1
		global LCityRaider
		global LVeteranForbiddenPromos4
		global LCivGermanen
		global DHorseDownMap
		global DHorseUpMap
		global LGGStoneAge
		global LGGStandard
		global DGGNames
		global LRelisRemapCapital
		global LGreeks
		global LNearEast
		global LNorthern
		global LegioNames
		global LHeldendenkmal
		global LRankUnits
		global LNoRankUnits
		global LRankUnitBuilt
		global LAngstUnits
		global LUnitsNoFoodCosts
		global LCivsWithAqueduct
		global LCapitalPromoUpUnits
		global LMonoReligions
		global LForests
		global LFireUnits
		global LCamelUnits
		global LUnits4HorseSwap
		global LMovingBonus
		global LRammen
		global LInquisitors
		global LGlobalTechs

		if gc.getInfoTypeForString("COLOR_EMPTY") == -1:
				raise Exception("Called init() to early. getInfoTypeForString() returns -1.")

		# gc.getInfoTypeForString("UNIT_GAULOS"),
		LTradeUnits = [
				gc.getInfoTypeForString("UNIT_TRADE_MERCHANT_MAN"),
				gc.getInfoTypeForString("UNIT_TRADE_MERCHANT"),
				gc.getInfoTypeForString("UNIT_CARAVAN"),
				gc.getInfoTypeForString("UNIT_CARVEL_TRADE"),
				gc.getInfoTypeForString("UNIT_GAULOS"),
				gc.getInfoTypeForString("UNIT_TRADE_MERCHANTMAN")
		]
		LCultivationUnits = [
				gc.getInfoTypeForString("UNIT_SUPPLY_FOOD"),
				gc.getInfoTypeForString("UNIT_WORKBOAT")
		]
		# Renegade Ausnahmen
		LUnitLootLessSeaUnits = [
				gc.getInfoTypeForString("UNIT_WORKBOAT"),
				gc.getInfoTypeForString("UNIT_TREIBGUT"),
				gc.getInfoTypeForString("UNIT_CARVEL_TRADE"),
				gc.getInfoTypeForString("UNIT_GAULOS"),
				gc.getInfoTypeForString("UNIT_TRADE_MERCHANTMAN")
		]
		LUnitWarAnimals = [
				gc.getInfoTypeForString("UNIT_BEGLEITHUND"),
				gc.getInfoTypeForString("UNIT_KAMPFHUND"),
				gc.getInfoTypeForString("UNIT_KAMPFHUND_TIBET"),
				gc.getInfoTypeForString("UNIT_KAMPFHUND_MACEDON"),
				gc.getInfoTypeForString("UNIT_KAMPFHUND_BRITEN"),
				gc.getInfoTypeForString("UNIT_BURNING_PIGS")
		]
		LUnitCanBeDomesticated = [
				gc.getInfoTypeForString("UNIT_ESEL"),
				gc.getInfoTypeForString("UNIT_HORSE"),
				gc.getInfoTypeForString("UNIT_CAMEL"),
				gc.getInfoTypeForString("UNIT_ELEFANT")
		]
		LUnitWildAnimals = [
				gc.getInfoTypeForString("UNIT_LION"),
				gc.getInfoTypeForString("UNIT_LIONESS"),
				gc.getInfoTypeForString("UNIT_BEAR"),
				gc.getInfoTypeForString("UNIT_BEAR2"),
				gc.getInfoTypeForString("UNIT_PANTHER"),
				gc.getInfoTypeForString("UNIT_WOLF"),
				gc.getInfoTypeForString("UNIT_WOLF2"),
				gc.getInfoTypeForString("UNIT_BOAR"),
				gc.getInfoTypeForString("UNIT_TIGER"),
				gc.getInfoTypeForString("UNIT_LEOPARD"),
				gc.getInfoTypeForString("UNIT_HYENA"),
				gc.getInfoTypeForString("UNIT_DEER"),
				gc.getInfoTypeForString("UNIT_UR"),
				gc.getInfoTypeForString("UNIT_BERGZIEGE")
		]

		# Value = (iFoodMin, iFoodRand)
		DJagd = {
				None: (2, 2),  # Default for Lion, Wolf, etc. 2 - 3
				gc.getInfoTypeForString("UNIT_BOAR"): (5, 4),
				gc.getInfoTypeForString("UNIT_DEER"): (5, 4),
				gc.getInfoTypeForString("UNIT_CAMEL"): (4, 3),
				gc.getInfoTypeForString("UNIT_BEAR"): (4, 3),
				gc.getInfoTypeForString("UNIT_BEAR2"): (4, 3),
				gc.getInfoTypeForString("UNIT_HORSE"): (4, 4),
				gc.getInfoTypeForString("UNIT_ELEFANT"): (6, 4),
		}

		LArcherCombats = [
				gc.getInfoTypeForString("UNITCOMBAT_ARCHER"),
				gc.getInfoTypeForString("UNITCOMBAT_SKIRMISHER")
		]
		LMeleeCombats = [
				gc.getInfoTypeForString("UNITCOMBAT_MELEE"),
				gc.getInfoTypeForString("UNITCOMBAT_AXEMAN"),
				gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN"),
				gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN")
		]
		LMeleeSupplyCombats = LMeleeCombats+LArcherCombats

		LMountedSupplyCombats = [
				gc.getInfoTypeForString("UNITCOMBAT_CHARIOT"),
				gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"),
				gc.getInfoTypeForString("UNITCOMBAT_ELEPHANT")
		]
		LLimes = [
				gc.getInfoTypeForString("IMPROVEMENT_LIMES1"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES3"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES4"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES5"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES6"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES7"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES8"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES9"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_1"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_2"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_3"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_4"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_5"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_6"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_7"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_8"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_9")
		]
		LBuildLimes = [
				gc.getInfoTypeForString("BUILD_LIMES1"),
				gc.getInfoTypeForString("BUILD_LIMES2"),
				gc.getInfoTypeForString("BUILD_LIMES3"),
				gc.getInfoTypeForString("BUILD_LIMES4"),
				gc.getInfoTypeForString("BUILD_LIMES5"),
				gc.getInfoTypeForString("BUILD_LIMES6"),
				gc.getInfoTypeForString("BUILD_LIMES7"),
				gc.getInfoTypeForString("BUILD_LIMES8"),
				gc.getInfoTypeForString("BUILD_LIMES9"),
				gc.getInfoTypeForString("BUILD_LIMES2_1"),
				gc.getInfoTypeForString("BUILD_LIMES2_2"),
				gc.getInfoTypeForString("BUILD_LIMES2_3"),
				gc.getInfoTypeForString("BUILD_LIMES2_4"),
				gc.getInfoTypeForString("BUILD_LIMES2_5"),
				gc.getInfoTypeForString("BUILD_LIMES2_6"),
				gc.getInfoTypeForString("BUILD_LIMES2_7"),
				gc.getInfoTypeForString("BUILD_LIMES2_8"),
				gc.getInfoTypeForString("BUILD_LIMES2_9")
		]

		LImprFort = [
				gc.getInfoTypeForString("IMPROVEMENT_TURM2"),
				gc.getInfoTypeForString("IMPROVEMENT_FORT"),
				gc.getInfoTypeForString("IMPROVEMENT_FORT2"),
				gc.getInfoTypeForString("IMPROVEMENT_HANDELSPOSTEN"),
				gc.getInfoTypeForString("IMPROVEMENT_KASTELL")
		]
		LImprFort.append(LLimes)

		LImprFortSentry = [
				gc.getInfoTypeForString("IMPROVEMENT_TURM"),
				gc.getInfoTypeForString("IMPROVEMENT_TURM2"),
				gc.getInfoTypeForString("IMPROVEMENT_FORT"),
				gc.getInfoTypeForString("IMPROVEMENT_FORT2"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES9"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_9"),
				gc.getInfoTypeForString("IMPROVEMENT_KASTELL")
		]

		# LFeatureArray = [
		#     gc.getInfoTypeForString("FEATURE_FOREST"),
		#     gc.getInfoTypeForString("FEATURE_DICHTERWALD"),
		# ]

		# Für Festungsformation genutzt und für Kultur!
		LImprFortShort = [
				gc.getInfoTypeForString("IMPROVEMENT_HANDELSPOSTEN"),
				gc.getInfoTypeForString("IMPROVEMENT_TURM2"),
				gc.getInfoTypeForString("IMPROVEMENT_FORT"),
				gc.getInfoTypeForString("IMPROVEMENT_FORT2"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES9"),
				gc.getInfoTypeForString("IMPROVEMENT_LIMES2_9"),
				gc.getInfoTypeForString("IMPROVEMENT_BARBARENFORT")
		]

		DCaptureFromPirate = {
				gc.getInfoTypeForString("UNIT_PIRAT_KONTERE"): gc.getInfoTypeForString("UNIT_KONTERE"),
				gc.getInfoTypeForString("UNIT_PIRAT_BIREME"): gc.getInfoTypeForString("UNIT_BIREME"),
				gc.getInfoTypeForString("UNIT_PIRAT_TRIREME"): gc.getInfoTypeForString("UNIT_TRIREME"),
				gc.getInfoTypeForString("UNIT_PIRAT_LIBURNE"): gc.getInfoTypeForString("UNIT_LIBURNE")
		}
		DCaptureByPirate = dict((v, k) for k, v in DCaptureFromPirate.items())

		LFormationNoNaval = [
				gc.getInfoTypeForString("UNIT_WORKBOAT"),
				gc.getInfoTypeForString("UNIT_KILIKIEN"),
				gc.getInfoTypeForString("UNIT_PIRAT_KONTERE"),
				gc.getInfoTypeForString("UNIT_PIRAT_BIREME"),
				gc.getInfoTypeForString("UNIT_PIRAT_TRIREME"),
				gc.getInfoTypeForString("UNIT_PIRAT_LIBURNE")
		]
		LFormationMountedArcher = [
				gc.getInfoTypeForString("UNIT_CHARIOT_ARCHER"),
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER"),
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER_ROMAN"),
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER_SCYTHS"),
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER_BAKTRIEN"),
				gc.getInfoTypeForString("UNIT_ARABIA_CAMELARCHER")
		]
		LCivPirates = [
				gc.getInfoTypeForString("CIVILIZATION_BERBER"),
				gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"),
				gc.getInfoTypeForString("CIVILIZATION_HETHIT"),
				gc.getInfoTypeForString("CIVILIZATION_IBERER"),
				gc.getInfoTypeForString("CIVILIZATION_ILLYRIA"),
				gc.getInfoTypeForString("CIVILIZATION_LIBYA"),
				gc.getInfoTypeForString("CIVILIZATION_LYDIA"),
				gc.getInfoTypeForString("CIVILIZATION_NUBIA"),
				gc.getInfoTypeForString("CIVILIZATION_NUMIDIA"),
				gc.getInfoTypeForString("CIVILIZATION_VANDALS")
		]
		LCivPartherschuss = [
				gc.getInfoTypeForString("CIVILIZATION_HETHIT"),
				gc.getInfoTypeForString("CIVILIZATION_PHON"),
				gc.getInfoTypeForString("CIVILIZATION_ISRAEL"),
				gc.getInfoTypeForString("CIVILIZATION_PERSIA"),
				gc.getInfoTypeForString("CIVILIZATION_BABYLON"),
				gc.getInfoTypeForString("CIVILIZATION_SUMERIA"),
				gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"),
				gc.getInfoTypeForString("CIVILIZATION_SKYTHEN"),
				gc.getInfoTypeForString("CIVILIZATION_PARTHER"),
				gc.getInfoTypeForString("CIVILIZATION_HUNNEN"),
				gc.getInfoTypeForString("CIVILIZATION_INDIA"),
				gc.getInfoTypeForString("CIVILIZATION_BARBARIAN")
		]
		# Fast wie LFormationMountedArcher...
		LUnitPartherschuss = [
				# gc.getInfoTypeForString("UNIT_CHARIOT_ARCHER"),
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER"),
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER_ROMAN"),
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER_SCYTHS"),
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER_BAKTRIEN"),
				gc.getInfoTypeForString("UNIT_ARABIA_CAMELARCHER")
		]
		LKeilUnits = [
				gc.getInfoTypeForString("UNIT_BEGLEITHUND"),
				gc.getInfoTypeForString("UNIT_KAMPFHUND"),
				gc.getInfoTypeForString("UNIT_KAMPFHUND_TIBET"),
				gc.getInfoTypeForString("UNIT_KAMPFHUND_MACEDON"),
				gc.getInfoTypeForString("UNIT_KAMPFHUND_BRITEN"),
				gc.getInfoTypeForString("UNIT_MOUNTED_SACRED_BAND_CARTHAGE"),
				gc.getInfoTypeForString("UNIT_EQUITES"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_EQUITES2"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO"),
				gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"),
				gc.getInfoTypeForString("UNIT_CATAPHRACT"),
				gc.getInfoTypeForString("UNIT_CATAPHRACT_PERSIA"),
				gc.getInfoTypeForString("UNIT_CATAPHRACT_ROME"),
				gc.getInfoTypeForString("UNIT_CLIBANARII"),
				gc.getInfoTypeForString("UNIT_CLIBANARII_ROME"),
				gc.getInfoTypeForString("UNIT_CELTIBERIAN_CAVALRY"),
				gc.getInfoTypeForString("UNIT_MONGOL_KESHIK"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN_RIDER"),
				gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN"),
				gc.getInfoTypeForString("UNIT_CAMEL_CATAPHRACT")
		]
		LNoSchildwallUnitClasses = [
				gc.getInfoTypeForString("UNITCLASS_WARRIOR"),
				gc.getInfoTypeForString("UNITCLASS_AXEWARRIOR"),
				gc.getInfoTypeForString("UNITCLASS_WURFAXT"),
				gc.getInfoTypeForString("UNITCLASS_KURZSCHWERT"),
				gc.getInfoTypeForString("UNITCLASS_LIGHT_SPEARMAN"),
				gc.getInfoTypeForString("UNITCLASS_BEGLEITHUND"),
				gc.getInfoTypeForString("UNITCLASS_KAMPFHUND"),
				gc.getInfoTypeForString("UNITCLASS_BURNING_PIGS")
		]
		LNoSchildwallUnits = [
				gc.getInfoTypeForString("UNIT_AXEMAN"),
				gc.getInfoTypeForString("UNIT_BERSERKER_GERMAN"),
				gc.getInfoTypeForString("UNIT_CELTIC_GALLIC_WARRIOR"),
				gc.getInfoTypeForString("UNIT_THRAKIEN_WARRIOR"),
				gc.getInfoTypeForString("UNIT_TEUTONEN")
		]
		LDrillUnits = [
				gc.getInfoTypeForString("UNIT_LEGION"),
				gc.getInfoTypeForString("UNIT_LEGION2"),
				gc.getInfoTypeForString("UNIT_LEGION_OPTIO"),
				gc.getInfoTypeForString("UNIT_LEGION_OPTIO2"),
				gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"),
				gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN2"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN3")
		]
		LTestudoUnits = [
				gc.getInfoTypeForString("UNIT_LEGION"),
				gc.getInfoTypeForString("UNIT_LEGION2"),
				gc.getInfoTypeForString("UNIT_LEGION_OPTIO"),
				gc.getInfoTypeForString("UNIT_LEGION_OPTIO2"),
				gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"),
				gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN2"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN3")
		]
		LUnits4Praetorians = [
				gc.getInfoTypeForString("UNIT_LEGION"),
				gc.getInfoTypeForString("UNIT_LEGION2"),
				gc.getInfoTypeForString("UNIT_LEGION_OPTIO"),
				gc.getInfoTypeForString("UNIT_LEGION_OPTIO2"),
				gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"),
				gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2")
		]
		LPraetorians = [
				gc.getInfoTypeForString("UNIT_PRAETORIAN"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN2"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN3"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN_RIDER")
		]
		LFluchtCombats = [
				gc.getInfoTypeForString("UNITCOMBAT_MELEE"),
				gc.getInfoTypeForString("UNITCOMBAT_AXEMAN"),
				gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN"),
				gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"),
				gc.getInfoTypeForString("UNITCOMBAT_ARCHER"),
				gc.getInfoTypeForString("UNITCOMBAT_SKIRMISHER")
		]
		LFormationen = [
				gc.getInfoTypeForString("PROMOTION_FORM_SCHILDWALL"),
				gc.getInfoTypeForString("PROMOTION_FORM_CLOSED_FORM"),    # TECH_CLOSED_FORM
				gc.getInfoTypeForString("PROMOTION_FORM_PHALANX"),        # TECH_PHALANX
				gc.getInfoTypeForString("PROMOTION_FORM_PHALANX2"),       # TECH_PHALANX2
				gc.getInfoTypeForString("PROMOTION_FORM_SCHIEF"),         # TECH_PHALANX2
				gc.getInfoTypeForString("PROMOTION_FORM_MANIPEL"),        # TECH_MANIPEL
				gc.getInfoTypeForString("PROMOTION_FORM_TREFFEN"),        # TECH_TREFFEN
				gc.getInfoTypeForString("PROMOTION_FORM_KOHORTE"),        # TECH_MARIAN_REFORM
				gc.getInfoTypeForString("PROMOTION_FORM_KEIL"),           # TECH_KAMPFHUNDE
				gc.getInfoTypeForString("PROMOTION_FORM_ZANGENANGRIFF"),  # TECH_HORSEBACK_RIDING_2
				gc.getInfoTypeForString("PROMOTION_FORM_FLANKENSCHUTZ"),  # TECH_TREFFEN
				gc.getInfoTypeForString("PROMOTION_FORM_GASSE"),          # TECH_GEOMETRIE2
				gc.getInfoTypeForString("PROMOTION_FORM_TESTUDO"),        # TECH_MARIAN_REFORM
				gc.getInfoTypeForString("PROMOTION_FORM_PARTHER"),
				gc.getInfoTypeForString("PROMOTION_FORM_KANTAKREIS"),
				gc.getInfoTypeForString("PROMOTION_FORM_FOURAGE"),        # TECH_BRANDSCHATZEN
				gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_KEIL"),     # TECH_LOGIK
				gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_ZANGE"),    # TECH_LOGIK
				gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS"),
				gc.getInfoTypeForString("PROMOTION_FORM_FORTRESS2"),
				gc.getInfoTypeForString("PROMOTION_FORM_NAVAL_FULL_SPEED"),
				gc.getInfoTypeForString("PROMOTION_FORM_LEADER_POSITION")
		]
		LUnitsNoAIReservists = [
				gc.getInfoTypeForString("UNIT_TRIARII"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN2"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN3"),
				gc.getInfoTypeForString("UNIT_CELERES"),
				gc.getInfoTypeForString("UNIT_ARCHER_LEGION"),
				gc.getInfoTypeForString("UNIT_HOPLIT_2"),
				gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"),
				gc.getInfoTypeForString("UNIT_GREEK_STRATEGOS"),
				gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK2"),
				gc.getInfoTypeForString("UNIT_SPARTA_2"),
				gc.getInfoTypeForString("UNIT_SPARTA_3"),
				gc.getInfoTypeForString("UNIT_UNSTERBLICH_2"),
				gc.getInfoTypeForString("UNIT_HYPASPIST2"),
				gc.getInfoTypeForString("UNIT_HYPASPIST3"),
				gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"),
				gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"),
				gc.getInfoTypeForString("UNIT_NUBIAFUERST"),
				gc.getInfoTypeForString("UNIT_MACCABEE"),
				gc.getInfoTypeForString("UNIT_STAMMESFUERST"),
				gc.getInfoTypeForString("UNIT_FUERST_DAKER"),
				gc.getInfoTypeForString("UNIT_GERMAN_HARIER"),
				gc.getInfoTypeForString("UNIT_RADSCHA"),
				gc.getInfoTypeForString("UNIT_INDIAN_NAYAR"),
				gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER"),
				gc.getInfoTypeForString("UNIT_MOUNTED_SACRED_BAND_CARTHAGE"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN_RIDER")
		]
		LUnitAuxiliar = [
				gc.getInfoTypeForString("UNIT_AUXILIAR"),
				gc.getInfoTypeForString("UNIT_AUXILIAR_ROME"),
				gc.getInfoTypeForString("UNIT_AUXILIAR_MACEDON")
		]
		LUnitNoSlaves = LUnitWarAnimals
		LCombatNoRuestung = [
				gc.getInfoTypeForString("UNITCOMBAT_NAVAL"),
				gc.getInfoTypeForString("UNITCOMBAT_SIEGE"),
				gc.getInfoTypeForString("UNITCOMBAT_RECON"),
				gc.getInfoTypeForString("UNITCOMBAT_HEALER"),
				gc.getInfoTypeForString("UNITCOMBAT_ARCHER"),
				-1,  # UnitCombatTypes.NO_UNITCOMBAT,
				# gc.getInfoTypeForString("NONE"),  # also -1
		]
		LUnitNoRuestung = [
				gc.getInfoTypeForString("UNIT_WARRIOR"),
				gc.getInfoTypeForString("UNIT_AXEWARRIOR"),
				gc.getInfoTypeForString("UNIT_HUNTER"),
				gc.getInfoTypeForString("UNIT_LIGHT_SPEARMAN"),
				gc.getInfoTypeForString("UNIT_KURZSCHWERT"),
				gc.getInfoTypeForString("UNIT_KRUMMSAEBEL"),
				gc.getInfoTypeForString("UNIT_FALCATA_IBERIA"),
				gc.getInfoTypeForString("UNIT_CELTIC_GALLIC_WARRIOR"),
				gc.getInfoTypeForString("UNIT_LIGHT_CHARIOT"),
				gc.getInfoTypeForString("UNIT_CHARIOT_ARCHER"),
				gc.getInfoTypeForString("UNIT_MERC_HORSEMAN"),
				gc.getInfoTypeForString("UNIT_HORSEMAN"),
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER"),
				gc.getInfoTypeForString("UNIT_ARABIA_CAMELARCHER")
		]
		LUnitNoRuestung.extend(LUnitWarAnimals)

		# Belobigte Krieger - hoechster Rang
		LUnitsHeadRang = [
				gc.getInfoTypeForString("UNIT_STAMMESFUERST"),
				gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN_HUN")
		]

		LUnitSkirmish = [
				gc.getInfoTypeForString("UNIT_BALEAREN"),
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER_BAKTRIEN"),
				gc.getInfoTypeForString("UNIT_MONGOL_KESHIK"),
				gc.getInfoTypeForString("UNIT_THRAKIEN_PELTAST")
		]
		LClassSkirmish = [
				gc.getInfoTypeForString("UNITCLASS_PELTIST"),
				gc.getInfoTypeForString("UNITCLASS_SKIRMISHER"),
				gc.getInfoTypeForString("UNITCLASS_CHARIOT_ARCHER"),
				gc.getInfoTypeForString("UNITCLASS_HORSE_ARCHER"),
				gc.getInfoTypeForString("UNITCLASS_CAMEL_ARCHER")
		]
		LFernangriffNoCosts = [
				gc.getInfoTypeForString("CIVILIZATION_BERBER"),
				gc.getInfoTypeForString("CIVILIZATION_HUNNEN"),
				gc.getInfoTypeForString("CIVILIZATION_SKYTHEN")
		]
		# Individuelle Kosten fuer iAirRange-Units
		DFernangriffCosts = {
				gc.getInfoTypeForString("UNITCLASS_HUNTER"): 0,
				gc.getInfoTypeForString("UNITCLASS_LIGHT_ARCHER"): 0,
				gc.getInfoTypeForString("UNITCLASS_ARCHER"): 1,
				gc.getInfoTypeForString("UNITCLASS_COMPOSITE_ARCHER"): 2,
				gc.getInfoTypeForString("UNIT_ARCHER_KRETA"): 2,
				gc.getInfoTypeForString("UNITCLASS_REFLEX_ARCHER"): 2,
				gc.getInfoTypeForString("UNITCLASS_ARCHER_LEGION"): 2,
				gc.getInfoTypeForString("UNIT_INDIAN_LONGBOW"): 3,
				gc.getInfoTypeForString("UNIT_LIBYAN_AMAZON"): 3,
				gc.getInfoTypeForString("UNITCLASS_PELTIST"): 0,
				gc.getInfoTypeForString("UNIT_BALEAREN"): 1,
				gc.getInfoTypeForString("UNIT_CHARIOT_RUNNER"): 1,
				gc.getInfoTypeForString("UNITCLASS_SKIRMISHER"): 2,
				gc.getInfoTypeForString("UNIT_THRAKIEN_PELTAST"): 2,
				gc.getInfoTypeForString("UNITCLASS_CHARIOT_ARCHER"): 2,
				gc.getInfoTypeForString("UNIT_HETHIT_WARCHARIOT"): 2,
				gc.getInfoTypeForString("UNIT_HORSE_ARCHER_SCYTHS"): 2,
				gc.getInfoTypeForString("UNIT_BAKTRIEN"): 2,
				gc.getInfoTypeForString("UNITCLASS_HORSE_ARCHER"): 2,
				gc.getInfoTypeForString("UNITCLASS_CAMEL_ARCHER"): 2,
				gc.getInfoTypeForString("UNIT_SCORPION"): 1,
				gc.getInfoTypeForString("UNITCOMBAT_SIEGE"): 1,
				gc.getInfoTypeForString("UNIT_ROME_DECAREME"): 3
		}

		LSeewind = [
				gc.getInfoTypeForString("FEATURE_WIND_N"),
				gc.getInfoTypeForString("FEATURE_WIND_NE"),
				gc.getInfoTypeForString("FEATURE_WIND_E"),
				gc.getInfoTypeForString("FEATURE_WIND_SE"),
				gc.getInfoTypeForString("FEATURE_WIND_S"),
				gc.getInfoTypeForString("FEATURE_WIND_SW"),
				gc.getInfoTypeForString("FEATURE_WIND_W"),
				gc.getInfoTypeForString("FEATURE_WIND_NW")
		]

		# Für UNITAI-Vergabe in onBuild
		LBuildArchers = [
				gc.getInfoTypeForString("UNIT_LIGHT_ARCHER"),
				gc.getInfoTypeForString("UNIT_ARCHER"),
				gc.getInfoTypeForString("UNIT_COMPOSITE_ARCHER")
		]
		LBuildCatapults = [
				gc.getInfoTypeForString("UNIT_ONAGER"),
				gc.getInfoTypeForString("UNIT_CATAPULT"),
				gc.getInfoTypeForString("UNIT_FIRE_CATAPULT")
		]

		# PAE Waffenmanufakturen - adds a second unit (PAE V Patch 4)
		DManufakturen = {
				gc.getInfoTypeForString("UNITCOMBAT_SWORDSMAN"): gc.getInfoTypeForString("BUILDING_WAFFENMANUFAKTUR_SCHWERT"),
				gc.getInfoTypeForString("UNITCOMBAT_AXEMAN"): gc.getInfoTypeForString("BUILDING_WAFFENMANUFAKTUR_AXT"),
				gc.getInfoTypeForString("UNITCOMBAT_ARCHER"): gc.getInfoTypeForString("BUILDING_WAFFENMANUFAKTUR_BOGEN"),
				gc.getInfoTypeForString("UNITCOMBAT_SPEARMAN"): gc.getInfoTypeForString("BUILDING_WAFFENMANUFAKTUR_SPEER"),
				gc.getInfoTypeForString("UNITCOMBAT_SKIRMISHER"): gc.getInfoTypeForString("BUILDING_WAFFENMANUFAKTUR_SPEER"),
				gc.getInfoTypeForString("UNITCOMBAT_SIEGE"): gc.getInfoTypeForString("BUILDING_WAFFENMANUFAKTUR_SIEGE"),
				gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"): gc.getInfoTypeForString("BUILDING_WAFFENMANUFAKTUR_HORSE")
		}

		DImprSupplyBonus = {
				gc.getInfoTypeForString("IMPROVEMENT_FARM"): 50,
				gc.getInfoTypeForString("IMPROVEMENT_PASTURE"): 50,
				gc.getInfoTypeForString("IMPROVEMENT_PLANTATION"): 30,
				gc.getInfoTypeForString("IMPROVEMENT_BRUNNEN"): 20,
				gc.getInfoTypeForString("IMPROVEMENT_COTTAGE"): 10,
				gc.getInfoTypeForString("IMPROVEMENT_HAMLET"): 15,
				gc.getInfoTypeForString("IMPROVEMENT_VILLAGE"): 20,
				gc.getInfoTypeForString("IMPROVEMENT_TOWN"): 25,
				gc.getInfoTypeForString("IMPROVEMENT_HANDELSPOSTEN"): 25,
				gc.getInfoTypeForString("IMPROVEMENT_FORT"): 30,
				gc.getInfoTypeForString("IMPROVEMENT_FORT2"): 40
		}

		DBuildingPromo = {
				gc.getInfoTypeForString("BUILDING_PROMO_FOREST"): gc.getInfoTypeForString("PROMOTION_WOODSMAN1"),
				gc.getInfoTypeForString("BUILDING_PROMO_HILLS"): gc.getInfoTypeForString("PROMOTION_GUERILLA1"),
				gc.getInfoTypeForString("BUILDING_PROMO_JUNGLE"): gc.getInfoTypeForString("PROMOTION_JUNGLE1"),
				gc.getInfoTypeForString("BUILDING_PROMO_SWAMP"): gc.getInfoTypeForString("PROMOTION_SUMPF1"),
				gc.getInfoTypeForString("BUILDING_PROMO_DESERT"): gc.getInfoTypeForString("PROMOTION_DESERT1"),
				gc.getInfoTypeForString("BUILDING_PROMO_CITY_A"): gc.getInfoTypeForString("PROMOTION_CITY_RAIDER1"),
				gc.getInfoTypeForString("BUILDING_PROMO_CITY_D"): gc.getInfoTypeForString("PROMOTION_CITY_GARRISON1"),
				gc.getInfoTypeForString("BUILDING_PROMO_PILLAGE"): gc.getInfoTypeForString("PROMOTION_PILLAGE1"),
				gc.getInfoTypeForString("BUILDING_PROMO_NAVI"): gc.getInfoTypeForString("PROMOTION_NAVIGATION1")
		}
		DPromosForPromoBuilding = {
				gc.getInfoTypeForString("PROMOTION_WOODSMAN5"): gc.getInfoTypeForString("BUILDING_PROMO_FOREST"),
				gc.getInfoTypeForString("PROMOTION_GUERILLA5"): gc.getInfoTypeForString("BUILDING_PROMO_HILLS"),
				gc.getInfoTypeForString("PROMOTION_JUNGLE5"): gc.getInfoTypeForString("BUILDING_PROMO_JUNGLE"),
				gc.getInfoTypeForString("PROMOTION_SUMPF5"): gc.getInfoTypeForString("BUILDING_PROMO_SWAMP"),
				gc.getInfoTypeForString("PROMOTION_DESERT5"): gc.getInfoTypeForString("BUILDING_PROMO_DESERT"),
				gc.getInfoTypeForString("PROMOTION_CITY_RAIDER5"): gc.getInfoTypeForString("BUILDING_PROMO_CITY_A"),
				gc.getInfoTypeForString("PROMOTION_CITY_GARRISON5"): gc.getInfoTypeForString("BUILDING_PROMO_CITY_D"),
				gc.getInfoTypeForString("PROMOTION_PILLAGE5"): gc.getInfoTypeForString("BUILDING_PROMO_PILLAGE"),
				gc.getInfoTypeForString("PROMOTION_NAVIGATION4"): gc.getInfoTypeForString("BUILDING_PROMO_NAVI")
		}
		# Upgrades for slaves and emigrants
		LVillages = [
				gc.getInfoTypeForString("IMPROVEMENT_COTTAGE"),
				gc.getInfoTypeForString("IMPROVEMENT_HAMLET"),
				gc.getInfoTypeForString("IMPROVEMENT_COTTAGE_HILL"),
				gc.getInfoTypeForString("IMPROVEMENT_HAMLET_HILL")
		]
		LLatifundien = [
				gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM1"),
				gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM2"),
				gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM3"),
				gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM4")
		]
		# gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM5")
		LFarms = [
				gc.getInfoTypeForString("IMPROVEMENT_PASTURE"),
				gc.getInfoTypeForString("IMPROVEMENT_FARM"),
				gc.getInfoTypeForString("IMPROVEMENT_PLANTATION"),
				gc.getInfoTypeForString("IMPROVEMENT_WINERY"),
				gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM1"),
				gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM2"),
				gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM3"),
				gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM4"),
				gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM5")
		]
		LMines = [
				gc.getInfoTypeForString("IMPROVEMENT_MINE"),
				gc.getInfoTypeForString("IMPROVEMENT_QUARRY"),
				gc.getInfoTypeForString("IMPROVEMENT_TORF")
		]
		LTemples = [
				gc.getInfoTypeForString("BUILDING_ZORO_TEMPLE"),
				gc.getInfoTypeForString("BUILDING_PHOEN_TEMPLE"),
				gc.getInfoTypeForString("BUILDING_SUMER_TEMPLE"),
				gc.getInfoTypeForString("BUILDING_ROME_TEMPLE"),
				gc.getInfoTypeForString("BUILDING_GREEK_TEMPLE"),
				gc.getInfoTypeForString("BUILDING_CELTIC_TEMPLE"),
				gc.getInfoTypeForString("BUILDING_EGYPT_TEMPLE"),
				gc.getInfoTypeForString("BUILDING_NORDIC_TEMPLE")
		]
		LHeldendenkmal = [
				gc.getInfoTypeForString("BUILDING_OBELISK"),
				gc.getInfoTypeForString("BUILDING_TEHEN"),
				gc.getInfoTypeForString("BUILDING_SIEGESSTELE"),
				gc.getInfoTypeForString("BUILDING_SIEGESTEMPEL"),
				gc.getInfoTypeForString("BUILDING_SIEGESSTATUE"),
				gc.getInfoTypeForString("BUILDING_SIEGESSAEULE"),
				gc.getInfoTypeForString("BUILDING_ELEPHANTMONUMENT"),
				gc.getInfoTypeForString("BUILDING_MONUMENT"),
				gc.getInfoTypeForString("BUILDING_TRIUMPH")
		]
		LWoodRemovedByLumberCamp = [
				gc.getInfoTypeForString("BUILD_REMOVE_JUNGLE"),
				gc.getInfoTypeForString("BUILD_REMOVE_FOREST"),
				gc.getInfoTypeForString("BUILD_REMOVE_FOREST_BURNT")
		]
		LCityRaider = [
				gc.getInfoTypeForString("PROMOTION_CITY_RAIDER1"),
				gc.getInfoTypeForString("PROMOTION_CITY_RAIDER2"),
				gc.getInfoTypeForString("PROMOTION_CITY_RAIDER3"),
				gc.getInfoTypeForString("PROMOTION_CITY_RAIDER4"),
				gc.getInfoTypeForString("PROMOTION_CITY_RAIDER5")
		]
		LPromoPillage = [
				gc.getInfoTypeForString("PROMOTION_PILLAGE1"),
				gc.getInfoTypeForString("PROMOTION_PILLAGE2"),
				gc.getInfoTypeForString("PROMOTION_PILLAGE3"),
				gc.getInfoTypeForString("PROMOTION_PILLAGE4"),
				gc.getInfoTypeForString("PROMOTION_PILLAGE5")
		]
		LGuerilla = [
				gc.getInfoTypeForString("PROMOTION_GUERILLA1"),
				gc.getInfoTypeForString("PROMOTION_GUERILLA2"),
				gc.getInfoTypeForString("PROMOTION_GUERILLA3"),
				gc.getInfoTypeForString("PROMOTION_GUERILLA4"),
				gc.getInfoTypeForString("PROMOTION_GUERILLA5")
		]
		LWoodsman = [
				gc.getInfoTypeForString("PROMOTION_WOODSMAN1"),
				gc.getInfoTypeForString("PROMOTION_WOODSMAN2"),
				gc.getInfoTypeForString("PROMOTION_WOODSMAN3"),
				gc.getInfoTypeForString("PROMOTION_WOODSMAN4"),
				gc.getInfoTypeForString("PROMOTION_WOODSMAN5")
		]
		LJungle = [
				gc.getInfoTypeForString("PROMOTION_JUNGLE1"),
				gc.getInfoTypeForString("PROMOTION_JUNGLE2"),
				gc.getInfoTypeForString("PROMOTION_JUNGLE3"),
				gc.getInfoTypeForString("PROMOTION_JUNGLE4"),
				gc.getInfoTypeForString("PROMOTION_JUNGLE5")
		]
		LSwamp = [
				gc.getInfoTypeForString("PROMOTION_SUMPF1"),
				gc.getInfoTypeForString("PROMOTION_SUMPF2"),
				gc.getInfoTypeForString("PROMOTION_SUMPF3"),
				gc.getInfoTypeForString("PROMOTION_SUMPF4"),
				gc.getInfoTypeForString("PROMOTION_SUMPF5")
		]
		LDesert = [
				gc.getInfoTypeForString("PROMOTION_DESERT1"),
				gc.getInfoTypeForString("PROMOTION_DESERT2"),
				gc.getInfoTypeForString("PROMOTION_DESERT3"),
				gc.getInfoTypeForString("PROMOTION_DESERT4"),
				gc.getInfoTypeForString("PROMOTION_DESERT5")
		]
		LCityGarrison = [
				gc.getInfoTypeForString("PROMOTION_CITY_GARRISON1"),
				gc.getInfoTypeForString("PROMOTION_CITY_GARRISON2"),
				gc.getInfoTypeForString("PROMOTION_CITY_GARRISON3"),
				gc.getInfoTypeForString("PROMOTION_CITY_GARRISON4"),
				gc.getInfoTypeForString("PROMOTION_CITY_GARRISON5")
		]
		LVeteranForbiddenPromos = [
				gc.getInfoTypeForString("PROMOTION_COMBAT3"),
				gc.getInfoTypeForString("PROMOTION_COMBAT4"),
				gc.getInfoTypeForString("PROMOTION_COMBAT5"),
				gc.getInfoTypeForString("PROMOTION_COMBAT6")
		]
		LVeteranForbiddenPromos1 = [
				gc.getInfoTypeForString("PROMOTION_SKIRMISH1"),
				gc.getInfoTypeForString("PROMOTION_SKIRMISH2"),
				gc.getInfoTypeForString("PROMOTION_SKIRMISH3")
		]
		LVeteranForbiddenPromos4 = [
				gc.getInfoTypeForString("PROMOTION_RANG_ROM_1"),
				gc.getInfoTypeForString("PROMOTION_RANG_ROM_2"),
				gc.getInfoTypeForString("PROMOTION_RANG_ROM_3"),
				gc.getInfoTypeForString("PROMOTION_RANG_ROM_4"),
				gc.getInfoTypeForString("PROMOTION_RANG_ROM_5")
		]

		# Kelten, Germanen, Gallier, etc.
		LCivGermanen = [
				gc.getInfoTypeForString("CIVILIZATION_GERMANEN"),
				gc.getInfoTypeForString("CIVILIZATION_CELT"),
				gc.getInfoTypeForString("CIVILIZATION_GALLIEN"),
				gc.getInfoTypeForString("CIVILIZATION_DAKER"),
				gc.getInfoTypeForString("CIVILIZATION_BRITEN"),
				gc.getInfoTypeForString("CIVILIZATION_VANDALS")
		]

		# [Unitkey] => { [Civkey] => [Unitkey], None -> [Default Unitkey]}
		DHorseDownMap = {
				gc.getInfoTypeForString("UNIT_AUXILIAR_HORSE"): {
						None: gc.getInfoTypeForString("UNIT_AUXILIAR"),
						gc.getInfoTypeForString("CIVILIZATION_ROME"): gc.getInfoTypeForString("UNIT_AUXILIAR_ROME"),
						gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"): gc.getInfoTypeForString("UNIT_AUXILIAR_ROME"),
						gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"): gc.getInfoTypeForString("UNIT_AUXILIAR_MACEDON")
				},
				gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN"): {
						None: gc.getInfoTypeForString("UNIT_FOEDERATI")
				},
				gc.getInfoTypeForString("UNIT_MOUNTED_SACRED_BAND_CARTHAGE"): {
						None: gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER")
				},
				gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH_RIDER"): {
						None: gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH")
				},
				gc.getInfoTypeForString("UNIT_MOUNTED_SCOUT"): {
						None: gc.getInfoTypeForString("UNIT_SCOUT"),
						gc.getInfoTypeForString("CIVILIZATION_ATHENS"): gc.getInfoTypeForString("UNIT_SCOUT_GREEK"),
						gc.getInfoTypeForString("CIVILIZATION_GREECE"): gc.getInfoTypeForString("UNIT_SCOUT_GREEK")
				},
				gc.getInfoTypeForString("UNIT_WAR_CHARIOT"): {
						None: -1,
						gc.getInfoTypeForString("CIVILIZATION_DAKER"): gc.getInfoTypeForString("UNIT_STAMMESFUERST"),
						gc.getInfoTypeForString("CIVILIZATION_GERMANEN"): gc.getInfoTypeForString("UNIT_STAMMESFUERST"),
						gc.getInfoTypeForString("CIVILIZATION_VANDALS"): gc.getInfoTypeForString("UNIT_STAMMESFUERST"),
						gc.getInfoTypeForString("CIVILIZATION_GALLIEN"): gc.getInfoTypeForString("UNIT_STAMMESFUERST"),
						gc.getInfoTypeForString("CIVILIZATION_CELT"): gc.getInfoTypeForString("UNIT_STAMMESFUERST"),
						gc.getInfoTypeForString("CIVILIZATION_BRITEN"): gc.getInfoTypeForString("UNIT_STAMMESFUERST")
				}
		}
		# gc.getInfoTypeForString("UNIT_PRAETORIAN_RIDER"): {
		#     None: gc.getInfoTypeForString("UNIT_PRAETORIAN"),
		# },

		DHorseUpMap = {
				"auxiliar": gc.getInfoTypeForString("UNIT_AUXILIAR_HORSE"),
				gc.getInfoTypeForString("UNIT_FOEDERATI"): gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN"),
				gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER"): gc.getInfoTypeForString("UNIT_MOUNTED_SACRED_BAND_CARTHAGE"),
				gc.getInfoTypeForString("UNIT_SCOUT"): gc.getInfoTypeForString("UNIT_MOUNTED_SCOUT"),
				gc.getInfoTypeForString("UNIT_SCOUT_GREEK"): gc.getInfoTypeForString("UNIT_MOUNTED_SCOUT"),
				gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"): gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH_RIDER"),
				gc.getInfoTypeForString("UNIT_STAMMESFUERST"): gc.getInfoTypeForString("UNIT_WAR_CHARIOT")
		}
		# gc.getInfoTypeForString("UNIT_PRAETORIAN"): gc.getInfoTypeForString("UNIT_PRAETORIAN_RIDER"),

		# Names for great generals (UNIT_GREAT_GENERAL)
		LGGStoneAge = [
			"Spikie", "Spookie", "Stonie", "Marshie", "Creep",
			"Elder", "Horn", "Groo", "Bear", "Loo", "Craa", "Samu",
			"Lonar", "Conan", "Ara", "Woolv", "Sha", "Skeltar",
			"Moss", "Beast", "Strongo", "Wildar", "Gewar", "Flamma",
			"Spicul", "Korob", "Leoch", "Oxyth", "Diokles", "Oibota",
			"Macho", "Lyncho", "Hammer", "Axtill", "Jagga", "Fufun",
			"Dasmon", "Hypos", "Orsippo", "Pullo", "Polos", "Tellis",
			"Lampis", "Menos", "Atheradas", "Pantakles", "Ikaros",
			"Phano", "Pagonda", "Kallistro", "Charmis", "Eleer", "Philome",
			"Eury", "Cratin", "Komaio", "Chionis", "Myron", "Eutelid",
			"Gelon", "Polymor", "Antikra", "Hetomo", "Epityl", "Hagnon"
		]

		LGGStandard = [
				"Adiantunnus", "Divico", "Albion",
				"Malorix", "Inguiomer", "Archelaos",
				"Dorimachos", "Helenos", "Kerkidas",
				"Mikythos", "Philopoimen", "Pnytagoras",
				"Sophainetos", "Theopomopos", "Gylippos",
				"Proxenos", "Theseus", "Balakros",
				"Bar Kochba", "Julian ben Sabar", "Justasas",
				"Patricius", "Schimon bar Giora", "Artaphernes",
				"Harpagos", "Atropates", "Bahram Chobin",
				"Datis", "Schahin", "Egnatius",
				"Curius Aentatus", "Antiochos II", "Spartacus",
				"Herodes I", "Calgacus", "Suebonius Paulinus",
				"Maxentus", "Sapor II", "Alatheus",
				"Saphrax", "Honorius", "Aetius",
				"Achilles", "Herodes", "Heros",
				"Odysseus", "Anytos"]

		DGGNames = {
				gc.getInfoTypeForString("CIVILIZATION_ROME"):
				["Agilo", "Marellus", "Flavius Theodosius",
				 "Flavius Merobaudes", "Flavius Bauto", "Flavius Saturnius",
				 "Flavius Fravitta", "Sextus Pompeius", "Publius Canidius Crassus",
				 "Marcus Claudius Marellus", "Marcus Cato Censorius", "Flavius Felix",
				 "Flavius Aetius", "Gnaeus Pompeius Strabo", "Ricimer",
				 "Flavius Ardaburius Aspar", "Publius Quinctilius Varus", "Marcus Vispanius Agrippa",
				 "Marcus Antonius Primus", "Tiberius Gracchus", "Petillius Cerialis",
				 "Gaius Suetonius Paulimius", "Titus Labienus", "Gnaeus Iulius Verus",
				 "Aulus Allienus", "Marcellinus", "Flavius Castinus",
				 "Lucius Fannius", "Aulus Didius Gallus", "Rufio",
				 "Publius Servilius Rullus", "Papias"],
				gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"):
				["Lars Tolumnius", "Lucius Tarquinius Priscus", "Arrunte Tarquinius",
				 "Celio Vibenna", "Elbio Vulturreno", "Arrunte Porsena",
				 "Tito Tarquinius", "Aulus Caecina Alienus", "Mezentius",
				 "Aulus Caecina Severerus", "Sextus Tarquinius", "Velthur Spurinna"],
				gc.getInfoTypeForString("CIVILIZATION_CELT"):
				["Ortiagon", "Adiatunnus", "Boduognatus",
										 "Indutiomarus", "Catuvolcus", "Deiotaros",
										 "Viridomarus", "Chiomara", "Voccio",
										 "Kauaros", "Komontorios"],
				gc.getInfoTypeForString("CIVILIZATION_GALLIEN"):
				["Vergobret", "Viridovix", "Acco",
				 "Amandus", "Camulogenus", "Postumus",
				 "Aelianus", "Capenus", "Tibatto",
										 "Julias Classicus", "Diviciacus"],
				gc.getInfoTypeForString("CIVILIZATION_GERMANEN"):
				["Valamir", "Athaulf ", "Eurich",
				 "Sigerich", "Walia", "Julius Civilis",
										 "Malorix", "Edekon", "Vestralp",
										 "Chnodomar", "Agenarich", "Ardarich",
										 "Verritus", "Thuidimir", "Gundioch",
										 "Priarius", "Kniva", "Radagaisus",
										 "Alaviv", "Athanarich", "Hunulf",
										 "Hunimund", "Rechiar", "Rechila",
										 "Cannabaudes", "Eriulf", "Adovacrius",
										 "Gundomad", "Hariobaud", "Hortar",
										 "Suomar", "Marcomer", "Gennobaudes",
										 "Sunno", "Merogaisus", "Segimer",
										 "Inguiomer", "Vadomar", "Ascaricus",
										 "Ursicinus", "Arbogast"],
				gc.getInfoTypeForString("CIVILIZATION_DAKER"):
				["Cotisone", "Oroles", "Duras",
										 "Rubobostes", "Dromichaetes", "Rholes",
										 "Zyraxes", "Dapys", "Fastida",
										 "Zenon"],
				gc.getInfoTypeForString("CIVILIZATION_ILLYRIA"):
				["Bardylis", "Glaukias", "Monunios II",
										 "Skerdilaidas", "Bato I", "Demetrios Pharos",
										 "Pleuratos I", "Sirras", "Bato II",
										 "Epulon", "Longarus", "Pinnes Pannonien",
										 "Cleitus", "Bardylis II", "Genthios"],
				gc.getInfoTypeForString("CIVILIZATION_GREECE"):
				["Adeimantos", "Xenokleides", "Timonides Leukas",
				 "Pyrrhias", "Philopoimen", "Milon",
										 "Leosthenes", "Kineas", "Dorimachos",
										 "Daochos I", "Ameinias", "Herakleides",
										 "Panares", "Lasthenes", "Onomarchus",
										 "Menon Pharsalos", "Timoleon", "Hermokrates",
										 "Archytas Tarent", "Keridas"],
				gc.getInfoTypeForString("CIVILIZATION_ATHENS"):
				["Konon", "Miltiades", "Perikles",
				 "Leon", "Menon", "Aristeides",
				 "Autokles", "Chares", "Eukrates",
										 "Hippokrates", "Kallistratos", "Thrasyllos",
										 "Timomachos", "Xanthippos", "Xenophon",
										 "Demosthenes", "Anytos"],
				gc.getInfoTypeForString("CIVILIZATION_THEBAI"):
				["Kleomenes Boeotarich", "Pagondas", "Pelopidas",
				 "Proxenos", "Coeratadas", "Gorgidas",
										 "Peisis Thespiai", "Theagenes Boeotarich", "Apollokrates",
										 "Polyxenos"],
				gc.getInfoTypeForString("CIVILIZATION_SPARTA"):
				["Brasidas", "Eurybiades", "Klearchos",
										 "Xanthippos", "Mindaros", "Peisander",
										 "Therimenes", "Thibron", "Agesilaos",
										 "Gylippos", "Astyochos", "Aiantides Milet",
										 "Antalkidas", "Archidamos II", "Aristodemos",
										 "Chalkideus", "Derkylidas", "Euryanax",
										 "Eurylochos", "Hippokrates Sparta", "Kallikratidas",
										 "Phoibidas", "Cheirisophos"],
				gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"):
				["Admetos", "Attalos", "Antipatros",
				 "Antigonos", "Antigenes", "Demetrios Althaimenes",
				 "Gorgias", "Herakon", "Karanos",
				 "Kleitos", "Memnon", "Nikanor",
				 "Parmenion", "Philippos", "Pleistarchos",
				 "Meleagros", "Menidas", "Menandros",
				 "Telesphoros", "Demetrios I Poliorketes", "Adaios Alektryon",
				 "Alexandros", "Koinos", "Zopyrion"],
				gc.getInfoTypeForString("CIVILIZATION_HETHIT"):
				["Pithana", "Anitta", "Labarna",
				 "Mursili I", "Hantili I", "Arnuwanda II",
				 "Muwattalli II", "Suppiluliuma II", "Kantuzzili",
				 "Kurunta"],
				gc.getInfoTypeForString("CIVILIZATION_LYDIA"):
				["Ardys II", "Sadyattes II", "Gyges",
										 "Paktyes", "Mazares", "Myrsus",
										 "Lydus", "Manes", "Agron",
										 "Meles"],
				gc.getInfoTypeForString("CIVILIZATION_PHON"):
				["Luli", "Abdi-Milkutti", "Straton I",
				 "Tabnit", "Abd-Melqart", "Azemilkos",
				 "Baal I", "Ithobaal III", "Elukaios",
				 "Baal II", "Panam-muwa II", "Esmun-ezer"],
				gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"):
				["Adherbal", "Bomilkar", "Hannibal Gisko",
										 "Boodes", "Hamilkar", "Mago",
										 "Maharbal", "Hanno", "Himilkon",
										 "Gisco", "Hannibal Bomilkars", "Hasdrubal Cartagagena",
										 "Hasdrubal Barkas", "Hasdrubal Hannos", "Hasdrubal Gisco",
										 "Mago Barkas", "Malchus"],
				gc.getInfoTypeForString("CIVILIZATION_ISRAEL"):
				["Bar Kochbar", "Jonathan", "Judas Makkabaeus",
				 "Justasas", "Schimon bar Giora", "Simon Makkabaeus",
										 "Johann Gischala", "Barak", "Patricius",
										 "Abner", "Scheba", "Jaobs",
										 "Benaja", "Omri", "Jeha",
										 "Goliath"],
				gc.getInfoTypeForString("CIVILIZATION_SUMERIA"):
				["Agga", "Ur-Nammu", "Gudea",
				 "Eanatum", "Amar-Sin", "Sulgi",
				 "Utuhengal", "Lugalbanda", "Enuk-duanna",
				 "Rim-Anum", "Ibbi-Sin"],
				gc.getInfoTypeForString("CIVILIZATION_BABYLON"):
				["Sumu-abum", "Sumulael", "Sabium",
				 "Hammurapi", "Eriba-Marduk", "Burna-burias I",
				 "Neriglissar", "Abi-esuh", "Nergalscharrussar",
				 "Ulamburiasch", "Musezib-Marduk", "Bel-simanni",
				 "Agum III", "Marduk-apla-iddina II", "Nabu-nasir",
										 "Bel-ibni"],
				gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"):
				["Dajan-Assur", "Samsi-ilu", "Sin-sumu-lisir",
				 "Assur-bela-ka-in", "Bel-lu-Ballet", "Nergal-ilaya",
				 "Nabu-da-inannil", "Inurta-ilaya", "Tustanu",
				 "Schanabuschu", "Assur-dan I", "Assur-nirari V",
				 "Eriba-Adad I", "Assur-dan II", "Sanherib",
				 "Asarhaddon"],
				gc.getInfoTypeForString("CIVILIZATION_PERSIA"):
				["Artaphernes", "Artasyras", "Shahrbaraz",
				 "Harpagos", "Mardonios", "Xenias Parrhasia",
										 "Otanes Sisamnes", "Tissaphernes", "Hydarnes",
										 "Pharnabazos II", "Tithraustes",
										 "Smerdomenes", "Tritantaichmes", "Tiribazos",
										 "Megabazos", "Megabates", "Artabozos I",
										 "Pharnabazos III", "Pherendates", "Abrokomas",
										 "Atropates", "Datis", "Satibarzanes",
										 "Oxyathres", "Struthas"],
				gc.getInfoTypeForString("CIVILIZATION_EGYPT"):
				["Ahmose", "Djehuti", "Ahmose Pennechbet",
				 "Antef", "Seti", "Psammetich I",
				 "Sib-e", "Ramses III", "Psammetich III",
				 "Merenptah", "Haremhab", "Amasis",
				 "Amenemhab", "Re-e", "Djefaihap",
				 "Kanefer"],
				gc.getInfoTypeForString("CIVILIZATION_NUBIA"):
				["Kaschta", "Pije", "Schabaka",
				 "Schabataka", "Tanotamun", "Aspelta",
				 "Pekartror", "Harsijotef", "Charamadoye",
				 "Cheperkare"],
				gc.getInfoTypeForString("CIVILIZATION_IBERER"):
				["Mandonio", "Caro Segeda", "Megara",
										 "Olindico", "Culcas", "Gauson",
										 "Hilerno", "Istolacio", "Luxinio",
										 "Punico", "Besadino", "Budar",
										 "Edecon", "Indortes"],
				gc.getInfoTypeForString("CIVILIZATION_NUMIDIA"):
				["Gauda", "Gulussa", "Matho",
				 "Tacfarinas", "Syphax", "Hiempsal I",
				 "Micipsa", "Arabion", "Suburra",
				 "Mastanabal"],
				gc.getInfoTypeForString("CIVILIZATION_BERBER"):
				["Masties", "Lusius Quietus", "Firmus",
				 "Gildon", "Quintus Lollius Urbicus", "Sabalus",
				 "Bagas", "Bogud", "Bocchus II",
				 "Lucius Balbus Minor"],
				gc.getInfoTypeForString("CIVILIZATION_LIBYA"):
				["Osorkon II", "Namilt I", "Iupet",
				 "Osochor", "Paschedbastet", "Namilt II",
				 "Takelot II", "Petubastis I", "Osorkon III",
				 "Bakenntah"],
				gc.getInfoTypeForString("CIVILIZATION_SKYTHEN"):
				["Idanthyrsos", "Maues", "Satrakes",
				 "Skilurus", "Scopasis", "Palacus",
										 "Madius", "Eunones", "Octamasadas",
										 "Azes I"],
				gc.getInfoTypeForString("CIVILIZATION_HUNNEN"):
				["Balamir", "Dengizich", "Ellac",
				 "Oktar", "Rua", "Uldin",
				 "Kursisch""Hormidac", "Ernak", "Charaton"],
				gc.getInfoTypeForString("CIVILIZATION_INDIA"):
				["Pushyamitra Shunga", "Kujula Kadphises", "Chandragupta II",
				 "Samudragupta", "Kharavela", "Skandagupta",
				 "Dhana Nanda", "Vidudabha", "Vishvamitra",
				 "Bimbisara", "Ajatashatru", "Bindusara",
				 "Kanishka", "Vima Kadphises", "Soter Megas"],
				gc.getInfoTypeForString("CIVILIZATION_BRITEN"):
				["Cassivelanaunus", "Cingetorix", "Carvillius",
				 "Taximagulus", "Segovax", "Ambrosius Aurelius",
				 "Hengest", "Horsa", "Vortigern",
				 "Riothamus", "Venutius", "Togodumnus",
				 "Allectus", "Nennius", "Calgacus"],
				gc.getInfoTypeForString("CIVILIZATION_PARTHER"):
				["Surena", "Artabanus V", "Vologase I",
				 "Vologase IV", "Phraates IV", "Osreos I",
				 "Phraates II", "Pakoros I", "Artabanus IV",
				 "Barzapharnes", "Pharnapates"],
				gc.getInfoTypeForString("CIVILIZATION_VANDALS"):
				["Godigisel", "Gunderich", "Gunthamund",
				 "Gento", "Thrasamund", "Hoamer",
				 "Wisimar", "Flavius Stilicho",
				 "Andevoto", "Hilderich"]
		}

		LRelisRemapCapital = [
				gc.getInfoTypeForString("RELIGION_SUMER"),
				gc.getInfoTypeForString("RELIGION_EGYPT"),
				gc.getInfoTypeForString("RELIGION_PHOEN"),
				gc.getInfoTypeForString("RELIGION_CELTIC"),
				gc.getInfoTypeForString("RELIGION_NORDIC"),
				gc.getInfoTypeForString("RELIGION_GREEK"),
				gc.getInfoTypeForString("RELIGION_ROME"),
				gc.getInfoTypeForString("RELIGION_ZORO"),
				gc.getInfoTypeForString("RELIGION_HINDUISM")
		]

		LGreeks = [
				gc.getInfoTypeForString("CIVILIZATION_GREECE"),
				gc.getInfoTypeForString("CIVILIZATION_ATHENS"),
				gc.getInfoTypeForString("CIVILIZATION_THEBAI")
		]
		LNearEast = [
				gc.getInfoTypeForString("CIVILIZATION_PHON"),
				gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"),
				gc.getInfoTypeForString("CIVILIZATION_BABYLON"),
				gc.getInfoTypeForString("CIVILIZATION_ISRAEL"),
				gc.getInfoTypeForString("CIVILIZATION_SUMERIA")
		]
		LNorthern = [
				gc.getInfoTypeForString("CIVILIZATION_CELT"),
				gc.getInfoTypeForString("CIVILIZATION_GALLIEN"),
				gc.getInfoTypeForString("CIVILIZATION_BRITEN"),
				gc.getInfoTypeForString("CIVILIZATION_GERMANEN"),
				gc.getInfoTypeForString("CIVILIZATION_DAKER"),
				gc.getInfoTypeForString("CIVILIZATION_VANDALS")
		]
		LegioNames = [
				"Legio I Adiutrix", "Legio I Germanica", "Legio I Italica",
				"Legio I Macriana Liberatrix", "Legio I Minervia", "Legio I Parthica",
				"Legio II Adiutrix", "Legio II Augusta", "Legio II Italica",
				"Legio II Parthica", "Legio II Traiana Fortis", "Legio III Augusta",
				"Legio III Cyrenaica", "Legio III Gallica", "Legio III Italica",
				"Legio III Parthica", "Legio III Macedonica", "Legio IV Flavia Felix",
				"Legio IV Scythica", "Legio V Alaudae", "Legio V Macedonica",
				"Legio VI Ferrata", "Legio VI Victrix", "Legio VII Claudia",
				"Legio VII Gemina", "Legio VIII Augusta", "Legio IX Hispana",
				"Legio X Fretensis", "Legio X Equestris", "Legio XI Claudia",
				"Legio XII Fulminata", "Legio XIII Gemina", "Legio XIV Gemina",
				"Legio XV Apollinaris", "Legio XV Primigenia", "Legio XVI Gallica",
				"Legio XVI Flavia Firma", "Legio XVII", "Legio XVIII",
				"Legio XIX", "Legio XX Valeria Victrix", "Legio XXI Rapax",
				"Legio XXII Deiotariana", "Legio XXII Primigenia", "Legio X"+"XX Ulpia Victrix",
				"Legio I Iulia Alpina", "Legio I Armeniaca", "Legio I Flavia Constantia",
				"Legio I Flavia Gallicana", "Legio I Flavia Martis", "Legio I Flavia Pacis",
				"Legio I Illyricorum", "Legio I Iovia", "Legio I Isaura Sagitaria",
				"Legio I Martia", "Legio I Maximiana", "Legio I Noricorum",
				"Legio I Pontica", "Legio II Iulia Alpina", "Legio II Armeniaca",
				"Legio II Brittannica", "Legio II Flavia Virtutis", "Legio II Herculia",
				"Legio II Isaura", "Legio III Iulia Alpina", "Legio III Diocletiana",
				"Legio III Flavia Salutis", "Legio III Herculia", "Legio III Isaura",
				"Legio IV Italica", "Legio IV Martia", "Legio IV Parthica",
				"Legio V Iovia", "Legio V Parthica", "Legio VI Gallicana",
				"Legio VI Herculia", "Legio VI Hispana", "Legio VI Parthica",
				"Legio XII Victrix", "Legio Thebaica",
		]

		# BonusClass indices
		eGrain = gc.getInfoTypeForString("BONUSCLASS_GRAIN")  # WHEAT, GERSTE, HAFER, ROGGEN, HIRSE, RICE
		eLivestock = gc.getInfoTypeForString("BONUSCLASS_LIVESTOCK")  # COW, PIG, SHEEP
		ePlantation = gc.getInfoTypeForString("BONUSCLASS_PLANTATION")  # GRAPES, OLIVES, DATTELN, BANANA
		eGeneral = gc.getInfoTypeForString("BONUSCLASS_GENERAL")  # COAL (Blei), ZINN, ZINK, ZEDERNHOLZ, COPPER, BRONZE, IRON, HORSE, CAMEL, HUNDE, PAPYRUS_PAPER
		eLuxury = gc.getInfoTypeForString("BONUSCLASS_LUXURY")  # GOLD, SILVER, PEARL, LION, SALT, DYE, FUR, INCENSE, MYRRHE, IVORY, SPICES, WINE, MUSIC, MESSING
		eRarity = gc.getInfoTypeForString("BONUSCLASS_RARITY")  # MAGNETIT, OBSIDIAN, OREICHALKOS, GLAS, BERNSTEIN, ELEKTRON, WALRUS, GEMS, SILK, SILPHIUM, TERRACOTTA
		eWonder = gc.getInfoTypeForString("BONUSCLASS_WONDER")  # MARBLE, STONE
		# eMisc =  gc.getInfoTypeForString("BONUSCLASS_MISC") # CRAB, DEER, FISH, CLAM, PAPYRUS
		# eMerc =  gc.getInfoTypeForString("BONUSCLASS_MERCENARY") # BALEAREN, TEUTONEN, BAKTRIEN, KRETA, KILIKIEN, MARS, THRAKIEN

		iNumBonuses = gc.getNumBonusInfos()
		LBonusCorn = []
		LBonusLivestock = []
		LBonusPlantation = []
		LBonusLuxury = []
		LBonusRarity = []
		LBonusUntradeable = [
				gc.getInfoTypeForString("BONUS_DEER"),
				gc.getInfoTypeForString("BONUS_FISH"),
				gc.getInfoTypeForString("BONUS_BANANA")
		]
		LBonusCultivatableCoast = [
				gc.getInfoTypeForString("BONUS_CRAB"),
				gc.getInfoTypeForString("BONUS_CLAM")
		]

		LBonus4Units = []
		for eBonus in range(iNumBonuses):
				pBonusInfo = gc.getBonusInfo(eBonus)
				iClass = pBonusInfo.getBonusClassType()
				if iClass == eGrain:
						LBonusCorn.append(eBonus)
				elif iClass == eLivestock:
						LBonusLivestock.append(eBonus)
				elif iClass == ePlantation:
						LBonusPlantation.append(eBonus)
				elif iClass == eLuxury:
						LBonusLuxury.append(eBonus)
				elif iClass == eRarity:
						LBonusRarity.append(eBonus)
				# eg BONUSCLASS_MISC
				elif iClass != eWonder and iClass != eGeneral and eBonus not in LBonusCultivatableCoast:
						LBonusUntradeable.append(eBonus)
				# BonusClass wonder and general are not stored separately (bc. unnecessary)

		LBonusCultivatable = LBonusCorn + LBonusLivestock + LBonusPlantation  # + [gc.getInfoTypeForString("BONUS_HORSE")]

		LBonusGetreide = LBonusCorn
		LBonusGetreide.remove(gc.getInfoTypeForString("BONUS_RICE"))

		LBonusStrategic = [
				gc.getInfoTypeForString("BONUS_BRONZE"),
				gc.getInfoTypeForString("BONUS_IRON"),
				gc.getInfoTypeForString("BONUS_CAMEL"),
				gc.getInfoTypeForString("BONUS_IVORY"),
				gc.getInfoTypeForString("BONUS_ESEL"),
				gc.getInfoTypeForString("BONUS_HORSE"),
				gc.getInfoTypeForString("BONUS_STONE"),
				gc.getInfoTypeForString("BONUS_MARBLE"),
				gc.getInfoTypeForString("BONUS_SLAVES"),
				gc.getInfoTypeForString("BONUS_HUNDE")
		]

		LBonusStratCultivatable = [
				gc.getInfoTypeForString("BONUS_ESEL"),
				gc.getInfoTypeForString("BONUS_CAMEL"),
				gc.getInfoTypeForString("BONUS_HORSE")
		]

		LBonus4Units = [
				gc.getInfoTypeForString("BONUS_BRONZE"),
				gc.getInfoTypeForString("BONUS_IRON"),
				gc.getInfoTypeForString("BONUS_ESEL"),
				gc.getInfoTypeForString("BONUS_HORSE"),
				gc.getInfoTypeForString("BONUS_HUNDE")
		]

		# List besteht aus: Civ, iUnit oder (-1: Fusstrupp, -2: Beritten), iNewUnit, req Promo
		# Eine erweiterte Liste befindet sich auch in CvPediaMain (inkl UNIT_PRAETORIAN-Belobigungen)
		# Legionstufen zu Praetorians geht via Python (CvMainInterface und CvGameUtils)
		# UNIT_PRAETORIAN Upgrades zu den 3 Typen (Garde, Cohors Urbana, Equites) geht via XML
		# CvPediaMain: (-1,0,0,0) = Leerzeile
		iRome = gc.getInfoTypeForString("CIVILIZATION_ROME")
		LRankUnits = [
						(iRome, gc.getInfoTypeForString("UNIT_ARCHER_ROME"), gc.getInfoTypeForString("UNIT_ARCHER_LEGION"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_ARCHER_LEGION"), gc.getInfoTypeForString("UNIT_HORSE_ARCHER_ROMAN"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_HASTA"), gc.getInfoTypeForString("UNIT_CELERES"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_PRINCIPES"), gc.getInfoTypeForString("UNIT_TRIARII"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_HASTATI"),   gc.getInfoTypeForString("UNIT_TRIARII"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_PILUMNI"),   gc.getInfoTypeForString("UNIT_TRIARII"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_TRIARII"), gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION"), gc.getInfoTypeForString("UNIT_LEGION_OPTIO"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_OPTIO"), gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_7")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"), gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_11")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION2"), gc.getInfoTypeForString("UNIT_LEGION_OPTIO2"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_OPTIO2"), gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_7")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"), gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_11")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_EVOCAT"), gc.getInfoTypeForString("UNIT_PRAETORIAN3"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_PRAETORIAN2"),   gc.getInfoTypeForString("UNIT_PRAETORIAN3"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COHORTES_URBANAE"), gc.getInfoTypeForString("UNIT_PRAETORIAN3"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_EQUITES"), gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_3")),
						(iRome, gc.getInfoTypeForString("UNIT_EQUITES"), gc.getInfoTypeForString("UNIT_PRAETORIAN_RIDER"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_HORSEMAN_EQUITES2"), gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_3")),
						(iRome, gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO"),  gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_LIMITANEI"), gc.getInfoTypeForString("UNIT_ROME_LIMITANEI_GARDE"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COMITATENSES"),  gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2"), gc.getInfoTypeForString("UNIT_ROME_COMITATENSES3"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_10")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COMITATENSES"),  gc.getInfoTypeForString("UNIT_ROME_PALATINI"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2"), gc.getInfoTypeForString("UNIT_ROME_PALATINI"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COMITATENSES3"), gc.getInfoTypeForString("UNIT_ROME_PALATINI"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_PALATINI"),   gc.getInfoTypeForString("UNIT_ROME_SCHOLAE"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_CLIBANARII_ROME"), gc.getInfoTypeForString("UNIT_ROME_SCHOLAE"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_CATAPHRACT_ROME"), gc.getInfoTypeForString("UNIT_ROME_SCHOLAE"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_HOPLIT"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_HOPLIT"), gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_HOPLIT_SPARTA"), gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_HOPLIT"), gc.getInfoTypeForString("UNIT_HOPLIT_2"), gc.getInfoTypeForString("PROMOTION_RANG_GREEK_4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), gc.getInfoTypeForString("UNIT_HOPLIT_2"), gc.getInfoTypeForString("PROMOTION_RANG_GREEK_4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_HOPLIT_2"), gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"), gc.getInfoTypeForString("PROMOTION_RANG_GREEK_7")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"), gc.getInfoTypeForString("UNIT_GREEK_STRATEGOS"), gc.getInfoTypeForString("PROMOTION_RANG_GREEK_10")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK"), gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK2"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), -2, gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_SPARTA"), gc.getInfoTypeForString("UNIT_HOPLIT"), gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_SPARTA"), gc.getInfoTypeForString("UNIT_HOPLIT_SPARTA"), gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_SPARTA"), -1, gc.getInfoTypeForString("UNIT_SPARTA_1"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_SPARTA"), gc.getInfoTypeForString("UNIT_SPARTA_1"), gc.getInfoTypeForString("UNIT_SPARTA_2"), gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_4")),
						(gc.getInfoTypeForString("CIVILIZATION_SPARTA"), gc.getInfoTypeForString("UNIT_SPARTA_2"), gc.getInfoTypeForString("UNIT_SPARTA_3"), gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_7")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK"), gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK2"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_HYPASPIST"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_HYPASPIST"), gc.getInfoTypeForString("UNIT_HYPASPIST2"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_7")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_HYPASPIST2"), gc.getInfoTypeForString("UNIT_HYPASPIST3"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_9")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_PEZHETAIROI2"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_PEZHETAIROI"), gc.getInfoTypeForString("UNIT_PEZHETAIROI2"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_PEZHETAIROI2"), gc.getInfoTypeForString("UNIT_PEZHETAIROI3"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_7")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_PEZHETAIROI3"), gc.getInfoTypeForString("UNIT_PEZHETAIROI4"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_9")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON"), gc.getInfoTypeForString("UNIT_COMPANION_CAVALRY"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_COMPANION_CAVALRY"), gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON3"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON3"), gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON4"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON4"), gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_UNSTERBLICH"), gc.getInfoTypeForString("UNIT_UNSTERBLICH_2"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), -1, gc.getInfoTypeForString("UNIT_APFELTRAEGER"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_5")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_APFELTRAEGER"), gc.getInfoTypeForString("UNIT_UNSTERBLICH_2"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_7")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_APFELTRAEGER"), gc.getInfoTypeForString("UNIT_PERSIA_AZADAN"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_10")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_UNSTERBLICH_2"), gc.getInfoTypeForString("UNIT_PERSIA_AZADAN"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_10")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_HORSEMAN_PERSIA"), gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE1"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_5")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE1"), gc.getInfoTypeForString("UNIT_CATAPHRACT_PERSIA"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_7")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_CATAPHRACT_PERSIA"), gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE2"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_11")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_EGYPT"), -1, gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_EGYPT"), gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"), gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"), gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_5")),
						(gc.getInfoTypeForString("CIVILIZATION_EGYPT"), gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"), gc.getInfoTypeForString("UNIT_WAR_CHARIOT"), gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_10")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_NUBIA"), -1, gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_NUBIA"), gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"), gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"), gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_5")),
						(gc.getInfoTypeForString("CIVILIZATION_NUBIA"), gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"), gc.getInfoTypeForString("UNIT_WAR_CHARIOT"), gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_10")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_2")),
						(gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_2")),
						(gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_4")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_PHON"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_PHON"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_PHON"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_2")),
						(gc.getInfoTypeForString("CIVILIZATION_PHON"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_2")),
						(gc.getInfoTypeForString("CIVILIZATION_PHON"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_4")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"), -1, gc.getInfoTypeForString("UNIT_ASSUR_RANG1"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_3")),
						(gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"), gc.getInfoTypeForString("UNIT_ASSUR_RANG2"), gc.getInfoTypeForString("UNIT_ASSUR_RANG3"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_6")),
						(gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"), gc.getInfoTypeForString("UNIT_ASSUR_RANG3"), gc.getInfoTypeForString("UNIT_ELITE_ASSUR"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_10")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_BABYLON"), -1, gc.getInfoTypeForString("UNIT_ASSUR_RANG1"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_3")),
						(gc.getInfoTypeForString("CIVILIZATION_BABYLON"), gc.getInfoTypeForString("UNIT_ASSUR_RANG2"), gc.getInfoTypeForString("UNIT_ASSUR_RANG3"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_6")),
						(gc.getInfoTypeForString("CIVILIZATION_BABYLON"), gc.getInfoTypeForString("UNIT_ASSUR_RANG3"), gc.getInfoTypeForString("UNIT_ELITE_ASSUR"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_10")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_SUMERIA"), -1, gc.getInfoTypeForString("UNIT_ELITE_SUMER"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_SUMERIA"), -1, gc.getInfoTypeForString("UNIT_SUMER_RANG1"), gc.getInfoTypeForString("PROMOTION_RANG_SUMER_4")),
						(gc.getInfoTypeForString("CIVILIZATION_SUMERIA"), gc.getInfoTypeForString("UNIT_SUMER_RANG1"), gc.getInfoTypeForString("UNIT_SUMER_RANG2"), gc.getInfoTypeForString("PROMOTION_RANG_SUMER_9")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_ISRAEL"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_MACCABEE"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_INDIA"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_RADSCHA"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_INDIA"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_INDIAN_NAYAR"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_DAKER"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_FUERST_DAKER"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_GERMANEN"), -1, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_GERMANEN"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_GERMAN_HARIER"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_GERMANEN"), gc.getInfoTypeForString("UNIT_AXEMAN2"), gc.getInfoTypeForString("UNIT_BERSERKER_GERMAN"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_CELT"), -1, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_GALLIEN"), -1, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_VANDALS"), -1, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_BRITEN"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_CELTIC_FIANNA"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_BRITEN"), -1, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_HUNNEN"), gc.getInfoTypeForString("UNIT_MONGOL_KESHIK"), gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN_HUN"), gc.getInfoTypeForString("PROMOTION_COMBAT5"))
		]

		LNoRankUnits = [
				gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH_RIDER"),
				gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH"),
				gc.getInfoTypeForString("UNIT_ELITE_SUMER"),
				gc.getInfoTypeForString("UNIT_ELITE_ASSUR"),
				gc.getInfoTypeForString("UNIT_WAR_CHARIOT"),
				gc.getInfoTypeForString("UNIT_PERSIAN_WARCHARIOT"),
				gc.getInfoTypeForString("UNIT_PERSIA_AZADAN"),
				gc.getInfoTypeForString("UNIT_INDIAN_WARCHARIOT"),
				gc.getInfoTypeForString("UNIT_STAMMESFUERST"),
				gc.getInfoTypeForString("UNIT_FUERST_DAKER"),
				gc.getInfoTypeForString("UNIT_MACCABEE"),
				gc.getInfoTypeForString("UNIT_BELGIER"),
				gc.getInfoTypeForString("UNIT_BERSERKER_GERMAN"),
				gc.getInfoTypeForString("UNIT_HYPASPIST3"),
				gc.getInfoTypeForString("UNIT_PEZHETAIROI4"),
				gc.getInfoTypeForString("UNIT_FOEDERATI"),
				gc.getInfoTypeForString("UNIT_INDIAN_NAYAR"),
				gc.getInfoTypeForString("UNIT_THRAKIEN_WARRIOR"),
				gc.getInfoTypeForString("UNIT_MARS"),
				gc.getInfoTypeForString("UNIT_CROSSBOWMAN_ROME"),
				gc.getInfoTypeForString("UNIT_CLIBANARII"),
				gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN"),
				gc.getInfoTypeForString("UNIT_WAR_ELEPHANT"),
				gc.getInfoTypeForString("UNIT_STATTHALTER_NORTH")
		]

		LRankUnitBuilt = [
				gc.getInfoTypeForString("CIVILIZATION_EGYPT"),
				gc.getInfoTypeForString("CIVILIZATION_NUBIA"),
				gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"),
				gc.getInfoTypeForString("CIVILIZATION_BABYLON"),
				gc.getInfoTypeForString("CIVILIZATION_SUMERIA")
		]

		LAngstUnits = [
				gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"),
				gc.getInfoTypeForString("UNITCOMBAT_CHARIOT"),
				gc.getInfoTypeForString("UNITCOMBAT_ELEPHANT")
		]

		LUnitsNoFoodCosts = [
				gc.getInfoTypeForString("UNIT_WARRIOR"),
				gc.getInfoTypeForString("UNIT_HUNTER")
		]

		LCivsWithAqueduct = [
				gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"),
				gc.getInfoTypeForString("CIVILIZATION_BABYLON"),
				gc.getInfoTypeForString("CIVILIZATION_ISRAEL"),
				gc.getInfoTypeForString("CIVILIZATION_GREECE"),
				gc.getInfoTypeForString("CIVILIZATION_ATHENS"),
				gc.getInfoTypeForString("CIVILIZATION_THEBAI"),
				gc.getInfoTypeForString("CIVILIZATION_SPARTA"),
				gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"),
				gc.getInfoTypeForString("CIVILIZATION_ROME")
		]

		# diese Einheiten muessen in der Hauptstadt oder Provinzhauptstadt belobigt werden
		LCapitalPromoUpUnits = [
				gc.getInfoTypeForString("UNIT_PRAETORIAN"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN2"),
				gc.getInfoTypeForString("UNIT_PRAETORIAN3"),
				gc.getInfoTypeForString("UNIT_ROME_COHORTES_URBANAE"),
				gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"),
				gc.getInfoTypeForString("UNIT_ROME_SCHOLAE"),
				gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON3"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON4"),
				gc.getInfoTypeForString("UNIT_HYPASPIST3"),
				gc.getInfoTypeForString("UNIT_PEZHETAIROI3"),
				gc.getInfoTypeForString("UNIT_PEZHETAIROI4"),
				gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH"),
				gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER"),
				gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"),
				gc.getInfoTypeForString("UNIT_MOUNTED_SACRED_BAND_CARTHAGE"),
				gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"),
				gc.getInfoTypeForString("UNIT_ASSUR_RANG2"),
				gc.getInfoTypeForString("UNIT_ELITE_ASSUR"),
				gc.getInfoTypeForString("UNIT_SUMER_RANG2"),
				gc.getInfoTypeForString("UNIT_ELITE_SUMER"),
				gc.getInfoTypeForString("UNIT_RADSCHA"),
				gc.getInfoTypeForString("UNIT_INDIAN_NAYAR"),
				gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE2"),
				gc.getInfoTypeForString("UNIT_PERSIA_AZADAN")
		]

		# monotheistische Religionen
		LMonoReligions = [
				#gc.getInfoTypeForString("RELIGION_BUDDHISM"),
				gc.getInfoTypeForString("RELIGION_ZORO"),
				gc.getInfoTypeForString("RELIGION_JUDAISM"),
				gc.getInfoTypeForString("RELIGION_CHRISTIANITY"),
				gc.getInfoTypeForString("RELIGION_ISLAM")
		]

		LForests = [
				gc.getInfoTypeForString("FEATURE_JUNGLE"),
				gc.getInfoTypeForString("FEATURE_SAVANNA"),
				gc.getInfoTypeForString("FEATURE_FOREST"),
				gc.getInfoTypeForString("FEATURE_DICHTERWALD")
		]

		LFireUnits = [
				gc.getInfoTypeForString("UNIT_BURNING_PIGS"),
				gc.getInfoTypeForString("UNIT_FIRE_CATAPULT")
		]

		# Pferdewechsel: berittener General UND diese Einheit (MainInterface)
		LCamelUnits = [
				gc.getInfoTypeForString("UNIT_ARABIA_CAMELARCHER"),
				gc.getInfoTypeForString("UNIT_CAMEL_CATAPHRACT"),
				gc.getInfoTypeForString("UNIT_CAMEL_CATAPHRACT_ROME")
		]

		# Pferdewechsel: berittener General ODER diese Einheit (MainInterface)
		LUnits4HorseSwap = [
				gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"),
				gc.getInfoTypeForString("UNIT_ROME_SCHOLAE"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON3"),
				gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON4"),
				gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE2"),
				gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH"),
				gc.getInfoTypeForString("UNIT_PERSIA_AZADAN"),
				gc.getInfoTypeForString("UNIT_SUMER_RANG2"),
				gc.getInfoTypeForString("UNIT_ASSUR_RANG3")
		]

		LMovingBonus = [
				gc.getInfoTypeForString("BONUS_FISH"),
				gc.getInfoTypeForString("BONUS_ESEL"),
				gc.getInfoTypeForString("BONUS_HORSE"),
				gc.getInfoTypeForString("BONUS_CAMEL"),
				gc.getInfoTypeForString("BONUS_COW"),
				gc.getInfoTypeForString("BONUS_PIG"),
				gc.getInfoTypeForString("BONUS_SHEEP"),
				gc.getInfoTypeForString("BONUS_DEER"),
				gc.getInfoTypeForString("BONUS_IVORY")
		]

		LRammen = [
				gc.getInfoTypeForString("UNIT_RAM"),
				gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
				gc.getInfoTypeForString("UNIT_SIEGE_TOWER"),
				gc.getInfoTypeForString("UNIT_BATTERING_RAM2")
		]

		LInquisitors = [
				gc.getInfoTypeForString("UNIT_EGYPT_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_SUMER_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_ZORO_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_PHOEN_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_GREEK_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_ROME_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_CELTIC_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_NORDIC_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_HINDU_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_BUDDHIST_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_JEWISH_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_CHRISTIAN_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_ISLAMIC_MISSIONARY"),
				gc.getInfoTypeForString("UNIT_INQUISITOR")
		]

		LGlobalTechs = [
				gc.getInfoTypeForString("TECH_KONZIL1"),
				gc.getInfoTypeForString("TECH_KONZIL2"),
				gc.getInfoTypeForString("TECH_KONZIL3"),
				gc.getInfoTypeForString("TECH_KONZIL4"),
				gc.getInfoTypeForString("TECH_KONZIL5"),
				gc.getInfoTypeForString("TECH_KONZIL6"),
				gc.getInfoTypeForString("TECH_KONZIL7")
		]

		# # Transfer local defined variables into module ones.
		# lnames = [l for l in locals().keys() if l[0] != "_" and l != "gc"]
		# for l in lnames:
		# globals()[l] = locals()[l]
