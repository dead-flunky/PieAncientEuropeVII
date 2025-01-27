# Imports
import os
from CvPythonExtensions import (CyGlobalContext, CyInterface,
																CyTranslator, CyMap, DirectionTypes,
																ColorTypes, UnitAITypes, CyPopupInfo,
																ButtonPopupTypes, plotDirection, UnitTypes,
																CyAudioGame, plotDistance, plotXY,
																isWorldWonderClass, isTeamWonderClass,
																isNationalWonderClass, InterfaceMessageTypes)
# import CvEventInterface
import CvUtil

import PAE_Sklaven
import PAE_Unit
import PAE_Barbaren
import PAE_Christen
import PAE_Mercenaries
import PAE_Lists as L

# Defines
gc = CyGlobalContext()
PAEMod = "Pie'sAncientEurope"

# PAE Stadtstatus
iPopDorf = 3
iPopStadt = 6
iPopProvinz = 12
iPopMetropole = 20

# PAE Statthaltertribut
PAEStatthalterTribut = {}  # Statthalter koennen nur 1x pro Runde entlohnt werden


def onModNetMessage(argsList):
		iData0, iData1, iData2, iData3, iData4 = argsList
		iData5 = iData4
		iData4 = iData3
		iData3 = iData2
		iData2 = iData1
		iData1 = iData0

		# Provinzhauptstadt Statthalter Tribut
		if iData1 == 678:
				# iData2 = iPlayer, iData3 = CityID, iData4 = Antwort [0,1,2] , iData5 = Tribut
				pPlayer = gc.getPlayer(iData2)
				pCity = pPlayer.getCity(iData3)
				iTribut = iData5
				iTribut2 = iData5 / 2

				iGold = pPlayer.getGold()
				bDoRebellion = False
				iAddHappiness = -2
				bPaid = False
				bDouble = False
				iRandRebellion = CvUtil.myRandom(100, "iRandRebellion")

				if iGold >= iTribut:
						if iData4 == 0:
								pPlayer.changeGold(-iTribut)
								iAddHappiness = 1
								bPaid = True
								bDouble = True
						elif iData4 == 1:
								pPlayer.changeGold(-iTribut2)
								iAddHappiness = 0
								bPaid = True

				elif iGold >= iTribut2:
						if iData4 == 0:
								pPlayer.changeGold(-iTribut2)
								iAddHappiness = 0
								bPaid = True

				elif iGold > 0:
						if iData4 == 0:
								pPlayer.setGold(0)
								iAddHappiness = 0

				# Happiness setzen (Bug bei CIV, Man muss immer den aktuellen Wert + die Aenderung setzen)
				iBuildingClass = gc.getInfoTypeForString("BUILDINGCLASS_PROVINZPALAST")
				iBuildingHappiness = pCity.getBuildingHappyChange(iBuildingClass) + iAddHappiness
				pCity.setBuildingHappyChange(iBuildingClass, iBuildingHappiness)

				# Chance einer Rebellion: Unhappy Faces * Capital Distance
				iCityHappiness = pCity.happyLevel() - pCity.unhappyLevel(0)
				if iCityHappiness < 0:
						# Abstand zur Hauptstadt
						if not pPlayer.getCapitalCity().isNone() and pPlayer.getCapitalCity() is not None:
								iDistance = plotDistance(pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), pCity.getX(), pCity.getY())
						else:
								iDistance = 20
						iChance = iCityHappiness * (-1) * iDistance
						if iChance > iRandRebellion:
								bDoRebellion = True

				if bDoRebellion:
						CyInterface().addMessage(iData2, True, 10, CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_REACTION_NEG",
																																							(pCity.getName(),)), "AS2D_REVOLTSTART", 2, None, ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
						# Dies soll doppelte Popups in PB-Spielen vermeiden.
						if iData2 == gc.getGame().getActivePlayer():
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_REACTION_NEG", (pCity.getName(), )))
								popupInfo.addPopup(iData2)
						doProvinceRebellion(pCity)
				elif bPaid:
						CyInterface().addMessage(iData2, True, 10, CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_REACTION_POS",
																																							(pCity.getName(),)), "AS2D_BUILD_BANK", 2, None, ColorTypes(8), pCity.getX(), pCity.getY(), True, True)
						szBuffer = CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_THX_MAIN", (pCity.getName(), ))
						iRand = 1 + CvUtil.myRandom(23, "provinz_thx")
						szBuffer = szBuffer + CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_THX_"+str(iRand), ())

						# 1 Unit as gift:
						lGift = []
						# Auxiliar
						iAuxiliar = gc.getCivilizationInfo(gc.getPlayer(pCity.getOriginalOwner()).getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_AUXILIAR"))
						if iAuxiliar == -1:
								iAuxiliar = gc.getInfoTypeForString("UNIT_AUXILIAR")
						if pCity.canTrain(iAuxiliar, 0, 0):
								lGift.append(iAuxiliar)
						if pCity.canTrain(gc.getInfoTypeForString("UNIT_AUXILIAR_HORSE"), 0, 0):
								lGift.append(gc.getInfoTypeForString("UNIT_AUXILIAR_HORSE"))
						# Food
						# lGift.append(gc.getInfoTypeForString("UNIT_SUPPLY_FOOD"))
						# Slave
						# if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")):
						lGift.append(gc.getInfoTypeForString("UNIT_SLAVE"))
						# Mounted
						if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STABLE")):
								lGift.append(gc.getInfoTypeForString("UNIT_HORSE"))

								lMounted = [
										gc.getInfoTypeForString("UNIT_CHARIOT"),
										gc.getInfoTypeForString("UNIT_HORSE_ARCHER"),
										gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN")
								]
								for iUnit in lMounted:
										if pCity.canTrain(iUnit, 0, 0):
												lGift.append(iUnit)

						# Elefant
						if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_ELEPHANT_STABLE")):
								lGift.append(gc.getInfoTypeForString("UNIT_ELEFANT"))
								if pCity.canTrain(gc.getInfoTypeForString("UNIT_WAR_ELEPHANT"), 0, 0):
										lGift.append(gc.getInfoTypeForString("UNIT_WAR_ELEPHANT"))
						# Kamel
						if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_CAMEL_STABLE")):
								# lGift.append(gc.getInfoTypeForString("UNIT_CARAVAN"))
								if pCity.canTrain(gc.getInfoTypeForString("UNIT_ARABIA_CAMELARCHER"), 0, 0):
										lGift.append(gc.getInfoTypeForString("UNIT_ARABIA_CAMELARCHER"))
								if pCity.canTrain(gc.getInfoTypeForString("UNIT_CAMEL_CATAPHRACT"), 0, 0):
										lGift.append(gc.getInfoTypeForString("UNIT_CAMEL_CATAPHRACT"))

						# Choose unit
						iRand = CvUtil.myRandom(len(lGift), "unitgift")

						# Dies soll doppelte Popups in PB-Spielen vermeiden.
						if iData2 == gc.getGame().getActivePlayer():
								# Auxiliars as gift:
								#iAnz = 1 + CvUtil.myRandom(3, "Auxiliars as gift")
								#if iAnz == 1: szBuffer = szBuffer + CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_THX_MAIN2_SINGULAR",("", ))
								# else: szBuffer = szBuffer + CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_THX_MAIN2_PLURAL",(iAnz, ))
								szBuffer = szBuffer + CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_THX_MAIN2", (gc.getUnitInfo(lGift[iRand]).getDescriptionForm(0),))
								if bDouble:
										szBuffer = szBuffer + u" (2x)"

								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(szBuffer)
								popupInfo.addPopup(iData2)

						pPlayer.initUnit(lGift[iRand], pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						if bDouble:
								pPlayer.initUnit(lGift[iRand], pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		# Statthalter / Tribut
		if iData1 == 737:
				# iData1, iData2, ... , iData5
				# First:  737, iCityID, iPlayer, -1, -1
				# Second: 737, iCityID, iPlayer, iButtonID (Typ), -1
				# Third:  737, iCityID, iPlayer, iTyp, iButtonID
				pPlayer = gc.getPlayer(iData3)
				pCity = pPlayer.getCity(iData2)

				if not pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZPALAST")):
						return

				if iData4 == -1:
						# Dies soll doppelte Popups in PB-Spielen vermeiden.
						if iData3 == gc.getGame().getActivePlayer():
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_0", (pCity.getName(),)))
								popupInfo.setData1(iData2)  # CityID
								popupInfo.setData2(iData3)  # iPlayer
								popupInfo.setData3(-1)  # iTyp (Einfluss oder Tribut)
								popupInfo.setOnClickedPythonCallback("popupStatthalterTribut")

								# Button 0: Einfluss verbessern
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_1", ()), "Art/Interface/Buttons/Actions/button_statthalter_einfluss.dds")
								# Button 1: Tribut fordern
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_2", ()),
																					",Art/Interface/Buttons/Civics/Decentralization.dds,Art/Interface/Buttons/Civics_Civilizations_Religions_Atlas.dds,4,1")
								# Button 2: Statthalter entfernen
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_3", ()), "Art/Interface/Buttons/Buildings/button_city_provinz.dds")

								# Cancel button
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ("", )), "Art/Interface/Buttons/Actions/Cancel.dds")
								popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
								popupInfo.addPopup(iData3)

				# -- Einfluss verbessern --
				elif iData4 == 0:

						# iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")
						iBuildingHappiness = pCity.getExtraHappiness()
						# Button 0: kleine Spende
						iGold1 = pCity.getPopulation() * 4
						iHappy1 = 1
						# Button 1: grosse Spende
						iGold2 = pCity.getPopulation() * 8
						iHappy2 = 2

						# Gold-Check
						if iData5 == 0 and pPlayer.getGold() < iGold1:
								iData5 = -1
						if iData5 == 1 and pPlayer.getGold() < iGold2:
								iData5 = -1

						if iData5 == -1:
								# Dies soll doppelte Popups in PB-Spielen vermeiden.
								if iData3 == gc.getGame().getActivePlayer():
										szText = CyTranslator().getText("[H2]", ())\
												+ CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_1", ()).upper()\
												+ CyTranslator().getText(r"[\H2][NEWLINE]", ())
										szText += CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_HALTUNG", ())
										szText += u": %d " % (abs(iBuildingHappiness))
										if iBuildingHappiness < 0:
												szText += CyTranslator().getText("[ICON_UNHAPPY]", ())
										else:
												szText += CyTranslator().getText("[ICON_HAPPY]", ())

										popupInfo = CyPopupInfo()
										popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
										popupInfo.setText(szText)
										popupInfo.setData1(iData2)  # CityID
										popupInfo.setData2(iData3)  # iPlayer
										popupInfo.setData3(iData4)  # iTyp (Einfluss oder Tribut)
										popupInfo.setOnClickedPythonCallback("popupStatthalterTribut")

										# Button 0: kleine Spende
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_GOLD1", (iGold1, iHappy1)), "Art/Interface/Buttons/Actions/button_statthalter_gold1.dds")
										# Button 1: grosse Spende
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_GOLD2", (iGold2, iHappy2)), "Art/Interface/Buttons/Actions/button_statthalter_gold2.dds")

										# Cancel button
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ("", )), "Art/Interface/Buttons/Actions/Cancel.dds")
										popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
										popupInfo.addPopup(iData3)

						# Triumphzug
						elif iData5 == 0:
								pCity.changeExtraHappiness(iHappy1)
								pPlayer.changeGold(-iGold1)
								iImmo = 2

						# Mehrtaegiges Fest
						elif iData5 == 1:
								pCity.changeExtraHappiness(iHappy2)
								pPlayer.changeGold(-iGold2)
								iImmo = 3

						if iData5 == 0 or iData5 == 1:
								if iData3 == gc.getGame().getActivePlayer():
										CyAudioGame().Play2DSound("AS2D_COINS")
										CyAudioGame().Play2DSound("AS2D_WELOVEKING")

								# Einheiten sind nun beschaeftigt
								pPlot = pCity.plot()
								iNumUnits = pPlot.getNumUnits()
								if iNumUnits > 0:
										for k in range(iNumUnits):
												if iData3 == pPlot.getUnit(k).getOwner():
														pPlot.getUnit(k).setImmobileTimer(iImmo)

								# Do this only once per turn
								PAEStatthalterTribut.setdefault(iData3, 0)
								PAEStatthalterTribut[iData3] = 1

				# -- Tribut fordern --
				elif iData4 == 1:

						# iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")
						iBuildingHappiness = pCity.getExtraHappiness()
						iUnit1 = gc.getInfoTypeForString("UNIT_GOLDKARREN")
						iUnhappy1 = 2
						iUnit2 = gc.getCivilizationInfo(gc.getPlayer(pCity.getOriginalOwner()).getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_AUXILIAR"))
						if iUnit2 == -1:
								iUnit2 = gc.getInfoTypeForString("UNIT_AUXILIAR")
						iUnhappy2 = 1
						iUnit3 = gc.getInfoTypeForString("UNIT_SUPPLY_FOOD")
						iUnhappy3 = 1
						iUnit4 = gc.getInfoTypeForString("UNIT_SLAVE")
						iUnhappy4 = 1

						if iData5 == -1:
								# Dies soll doppelte Popups in PB-Spielen vermeiden.
								if iData3 == gc.getGame().getActivePlayer():
										szText = CyTranslator().getText("[H2]", ())\
												+ CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_2", ()).upper()\
												+ CyTranslator().getText(r"[\H2][NEWLINE]", ())
										szText += CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_HALTUNG", ())
										szText += u": %d " % (abs(iBuildingHappiness))
										if iBuildingHappiness < 0:
												szText += CyTranslator().getText("[ICON_UNHAPPY]", ())
										else:
												szText += CyTranslator().getText("[ICON_HAPPY]", ())

										popupInfo = CyPopupInfo()
										popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
										popupInfo.setText(szText)
										popupInfo.setData1(iData2)  # CityID
										popupInfo.setData2(iData3)  # iPlayer
										popupInfo.setData3(iData4)  # iTyp (Einfluss oder Tribut)
										popupInfo.setOnClickedPythonCallback("popupStatthalterTribut")

										# Button 0: Goldkarren
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_TRIBUT1",
																							(gc.getUnitInfo(iUnit1).getDescriptionForm(0), iUnhappy1)), gc.getUnitInfo(iUnit1).getButton())
										# Button 1: Hilfstrupp
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_TRIBUT2",
																							(gc.getUnitInfo(iUnit2).getDescriptionForm(0), iUnhappy2)), gc.getUnitInfo(iUnit2).getButton())
										# Button 2: Getreidekarren
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_TRIBUT3",
																							(gc.getUnitInfo(iUnit3).getDescriptionForm(0), iUnhappy3)), gc.getUnitInfo(iUnit3).getButton())
										# Button 3: Sklave
										if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")):
												popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_TRIBUT4",
																									(gc.getUnitInfo(iUnit4).getDescriptionForm(0), iUnhappy4)), gc.getUnitInfo(iUnit4).getButton())

										# Cancel button
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ("", )), "Art/Interface/Buttons/Actions/Cancel.dds")
										popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
										popupInfo.addPopup(iData3)

						# Goldkarren
						elif iData5 == 0:
								# pCity.setBuildingHappyChange geht nicht, weil die Stadt auch Negatives positiv anrechnet
								pCity.changeExtraHappiness(-iUnhappy1)
								NewUnit = pPlayer.initUnit(iUnit1, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								NewUnit.setImmobileTimer(1)
						# Hilfstrupp
						elif iData5 == 1:
								pCity.changeExtraHappiness(-iUnhappy2)
								NewUnit = pPlayer.initUnit(iUnit2, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								iRand = 1 + CvUtil.myRandom(3, "aux_promo")
								if iRand >= 1:
										NewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
								if iRand >= 2:
										NewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT2"), True)
								if iRand >= 3:
										NewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT3"), True)
								NewUnit.setImmobileTimer(1)
						# Getreide
						elif iData5 == 2:
								pCity.changeExtraHappiness(-iUnhappy3)
								NewUnit = pPlayer.initUnit(iUnit3, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								NewUnit.setImmobileTimer(1)
						# Sklaven
						elif iData5 == 3:
								pCity.changeExtraHappiness(-iUnhappy4)
								NewUnit = pPlayer.initUnit(iUnit4, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								NewUnit.setImmobileTimer(1)

						if iData5 > -1:
								if iData3 == gc.getGame().getActivePlayer():
										CyAudioGame().Play2DSound("AS2D_UNIT_BUILD_UNIT")

								# Do this only once per turn
								PAEStatthalterTribut.setdefault(iData3, 0)
								PAEStatthalterTribut[iData3] = 1

				# -- Provinzstatthalter aus der Stadt entfernen --
				elif iData4 == 2:

						if iData5 == -1:
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_4", (pCity.getName(),)))
								popupInfo.setData1(iData2)  # CityID
								popupInfo.setData2(iData3)  # iPlayer
								popupInfo.setData3(iData4)  # iTyp (Einfluss oder Tribut)
								popupInfo.setOnClickedPythonCallback("popupStatthalterTribut")

								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_YES2", ()), "Art/Interface/Buttons/General/CheckMark.dds")
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_NO2", ()), "Art/Interface/Buttons/Actions/Cancel.dds")

								popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
								popupInfo.addPopup(iData3)

						elif iData5 == 0:
								pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_PROVINZPALAST"), 0)
								if iData3 == gc.getGame().getActivePlayer():
										CyAudioGame().Play2DSound("AS2D_SS_CITY_ANCIENT_LARGE_BED")


def doMessageCityGrowing(pCity):
		if pCity is None or pCity.isNone():
				return

		if pCity.getFoodTurnsLeft() == 1 and pCity.foodDifference(True) > 0 and not pCity.isFoodProduction() and not pCity.AI_isEmphasize(5):

				# Inits
				iBuildingDorf = gc.getInfoTypeForString("BUILDING_KOLONIE")
				iBuildingStadt = gc.getInfoTypeForString("BUILDING_STADT")
				iBuildingProvinz = gc.getInfoTypeForString("BUILDING_PROVINZ")
				iBuildingMetropole = gc.getInfoTypeForString("BUILDING_METROPOLE")

				kBuildingDorf = gc.getBuildingInfo(iBuildingDorf)
				kBuildingStadt = gc.getBuildingInfo(iBuildingStadt)
				kBuildingProvinz = gc.getBuildingInfo(iBuildingProvinz)
				kBuildingMetropole = gc.getBuildingInfo(iBuildingMetropole)

				iPlayer = pCity.getOwner()
				# ---

				# MESSAGE: city will grow / Stadt wird wachsen
				iPop = pCity.getPopulation() + 1
				CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_WILL_GROW", (pCity.getName(), iPop)), None, 2, None, ColorTypes(13), 0, 0, False, False)

				# MESSAGE: city gets/is unhappy / Stadt wird/ist unzufrieden
				iBonusHealth = 0
				iBonusHappy = 0
				if iPop == iPopDorf:
						iBonusHealth = kBuildingDorf.getHealth()
						iBonusHappy = kBuildingDorf.getHappiness()
						# for iBonus in gc.getNumBonuses():
						# iAddHealth = kBuildingDorf.getBonusHealthChanges(iBonus)
						# if iAddHealth != -1:
						# iBonusHealth += iAddHealth
						# iAddHappy = kBuildingDorf.getBonusHappinessChanges(iBonus)
						# if iAddHappy != -1:
						# iBonusHappy += iAddHappy
				#elif iPop == iPopStadt and pCity.getNumRealBuilding(iBuildingStadt) == 0:
				elif iPop == iPopStadt and not pCity.isHasBuilding(iBuildingStadt):
						iBonusHealth = kBuildingStadt.getHealth()
						iBonusHappy = kBuildingStadt.getHappiness()
				elif iPop == iPopProvinz:
						iBonusHealth = kBuildingProvinz.getHealth()
						iBonusHappy = kBuildingProvinz.getHappiness()
				elif iPop == iPopMetropole:
						iBonusHealth = kBuildingMetropole.getHealth()
						iBonusHappy = kBuildingMetropole.getHappiness()

				if pCity.happyLevel() - pCity.unhappyLevel(0) + iBonusHappy <= 0:
						if pCity.happyLevel() - pCity.unhappyLevel(0) >= 0:
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_GETS_UNHAPPY", (pCity.getName(),)),
																				 None, 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
						else:
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_IS_UNHAPPY", (pCity.getName(),)), None,
																				 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

				# MESSAGE: city gets/is unhealthy / Stadt wird/ist ungesund
				if pCity.goodHealth() - pCity.badHealth(False) + iBonusHealth <= 0:
						if pCity.goodHealth() - pCity.badHealth(False) >= 0:
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_GETS_UNHEALTY", (pCity.getName(),)),
																				 None, 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
						else:
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_IS_UNHEALTY", (pCity.getName(),)),
																				 None, 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

				# -----------------


# PAE City status --------------------------
# Check City colony or province after events
# once getting a city: keep being a city
def doCheckCityState(pCity):
		if pCity is None or pCity.isNone():
				return

		iBuildingSiedlung = gc.getInfoTypeForString("BUILDING_SIEDLUNG")
		iBuildingKolonie = gc.getInfoTypeForString("BUILDING_KOLONIE")
		iBuildingCity = gc.getInfoTypeForString("BUILDING_STADT")
		iBuildingProvinz = gc.getInfoTypeForString("BUILDING_PROVINZ")
		iBuildingMetropole = gc.getInfoTypeForString("BUILDING_METROPOLE")

		# getNumBuilding instead getNumRealBuilding due of an c++ error
		if pCity.getNumBuilding(iBuildingSiedlung) == 0:
				pCity.setNumRealBuilding(iBuildingSiedlung, 1)

		if pCity.getPopulation() >= iPopDorf and pCity.getNumBuilding(iBuildingKolonie) == 0:
				pCity.setNumRealBuilding(iBuildingKolonie, 1)
				if gc.getPlayer(pCity.getOwner()).isHuman():
						CyInterface().addMessage(pCity.getOwner(), True, 15, CyTranslator().getText("TXT_INFO_CITYSTATUS_1", (pCity.getName(), 0)),
																		 "AS2D_WELOVEKING", 2, gc.getBuildingInfo(iBuildingKolonie).getButton(), ColorTypes(13), pCity.getX(), pCity.getY(), True, True)
				if pCity.getProductionProcess() != -1:
						pCity.clearOrderQueue()

		if pCity.getPopulation() >= iPopStadt and pCity.getNumBuilding(iBuildingCity) == 0:
				pCity.setNumRealBuilding(iBuildingCity, 1)
				if gc.getPlayer(pCity.getOwner()).isHuman():
						CyInterface().addMessage(pCity.getOwner(), True, 15, CyTranslator().getText("TXT_INFO_CITYSTATUS_2", (pCity.getName(), 0)),
																		 "AS2D_WELOVEKING", 2, gc.getBuildingInfo(iBuildingCity).getButton(), ColorTypes(13), pCity.getX(), pCity.getY(), True, True)
				if pCity.getProductionProcess() != -1:
						pCity.clearOrderQueue()

		if pCity.getPopulation() >= iPopProvinz and pCity.getNumBuilding(iBuildingProvinz) == 0:
				pCity.setNumRealBuilding(iBuildingProvinz, 1)
				if gc.getPlayer(pCity.getOwner()).isHuman():
						CyInterface().addMessage(pCity.getOwner(), True, 15, CyTranslator().getText("TXT_INFO_CITYSTATUS_3", (pCity.getName(), 0)),
																		 "AS2D_WELOVEKING", 2, gc.getBuildingInfo(iBuildingProvinz).getButton(), ColorTypes(13), pCity.getX(), pCity.getY(), True, True)

		if pCity.getPopulation() >= iPopMetropole and pCity.getNumBuilding(iBuildingMetropole) == 0:
				pCity.setNumRealBuilding(iBuildingMetropole, 1)
				if gc.getPlayer(pCity.getOwner()).isHuman():
						CyInterface().addMessage(pCity.getOwner(), True, 15, CyTranslator().getText("TXT_INFO_CITYSTATUS_5", (pCity.getName(), 0)),
																		 "AS2D_WELOVEKING", 2, gc.getBuildingInfo(iBuildingMetropole).getButton(), ColorTypes(13), pCity.getX(), pCity.getY(), True, True)

		# Falls extremer Bev.rueckgang: Meldungen von hoeheren Status beginnend
		if pCity.getPopulation() < iPopMetropole and pCity.getNumBuilding(iBuildingMetropole) == 1:
				pCity.setNumRealBuilding(iBuildingMetropole, 0)
				if gc.getPlayer(pCity.getOwner()).isHuman():
						CyInterface().addMessage(pCity.getOwner(), True, 15, CyTranslator().getText("TXT_INFO_CITYSTATUS_6", (pCity.getName(), 0)),
																		 "AS2D_PLAGUE", 2, gc.getBuildingInfo(iBuildingProvinz).getButton(), ColorTypes(13), pCity.getX(), pCity.getY(), True, True)
		if pCity.getPopulation() < iPopProvinz and pCity.getNumBuilding(iBuildingProvinz) == 1:
				pCity.setNumRealBuilding(iBuildingProvinz, 0)
				if gc.getPlayer(pCity.getOwner()).isHuman():
						CyInterface().addMessage(pCity.getOwner(), True, 15, CyTranslator().getText("TXT_INFO_CITYSTATUS_4", (pCity.getName(), 0)),
																		 "AS2D_PLAGUE", 2, gc.getBuildingInfo(iBuildingCity).getButton(), ColorTypes(13), pCity.getX(), pCity.getY(), True, True)

		# AI and its slaves
		if not gc.getPlayer(pCity.getOwner()).isHuman():
				PAE_Sklaven.doAIReleaseSlaves(pCity)


# --------------------------------
# Methode auch in CvWorldBuilderScreen.py - immer beide aendern
def doCheckTraitBuildings(pCity):
		pOwner = gc.getPlayer(pCity.getOwner())
		# lokale Trait-Gebaeude
		iCreativeLocal = gc.getInfoTypeForString("BUILDING_TRAIT_CREATIVE_LOCAL")
		eTraitCreative = gc.getInfoTypeForString("TRAIT_CREATIVE")
		# Tech, ab der Creative_Local gesetzt wird
		iTechCreativeLocal = gc.getInfoTypeForString("TECH_ALPHABET")

		# Alle nicht passenden Gebaeude entfernen
		# Nur lokale hinzufuegen, globale nicht
		if pOwner.hasTrait(eTraitCreative) and gc.getTeam(pOwner.getTeam()).isHasTech(iTechCreativeLocal):
				pCity.setNumRealBuilding(iCreativeLocal, 1)
		else:
				pCity.setNumRealBuilding(iCreativeLocal, 0)


def doCheckGlobalTraitBuildings(iPlayer, pCity=None, iOriginalOwner=-1):
		pOwner = gc.getPlayer(iPlayer)
		lGlobal = [
				(gc.getInfoTypeForString("TRAIT_MARITIME"), gc.getInfoTypeForString("BUILDING_TRAIT_MARITIME_GLOBAL")),
				(gc.getInfoTypeForString("TRAIT_CREATIVE"), gc.getInfoTypeForString("BUILDING_TRAIT_CREATIVE_GLOBAL")),
				(gc.getInfoTypeForString("TRAIT_PHILOSOPHICAL"), gc.getInfoTypeForString("BUILDING_TRAIT_PHILOSOPHICAL_GLOBAL"))
		]

		for (iTrait, iBuilding) in lGlobal:
				# es wurde ein Traitbuilding erobert
				if pCity is not None and pCity.isHasBuilding(iBuilding):
						pCity.setNumRealBuilding(iBuilding, 0)
						if iOriginalOwner != -1:
								doCheckGlobalBuilding(iOriginalOwner, iBuilding)

				if pOwner.hasTrait(iTrait):
						doCheckGlobalBuilding(iPlayer, iBuilding)


# Methode fuer lokalen Gebrauch
def doCheckGlobalBuilding(iPlayer, iBuilding):
		pPlayer = gc.getPlayer(iPlayer)
		(loopCity, pIter) = pPlayer.firstCity(False)
		if loopCity is not None and not loopCity.isNone():
				loopCity.setNumRealBuilding(iBuilding, 1)
				iCount = 0
				while loopCity:
						if not loopCity.isNone() and loopCity.isHasBuilding(iBuilding):
								iCount += 1
								if iCount > 1:
										loopCity.setNumRealBuilding(iBuilding, 0)
						(loopCity, pIter) = pPlayer.nextCity(pIter, False)

# Begin Inquisition -------------------------------
def InquisitionPossible(pCity, pUnit):
		pCityPlayer = gc.getPlayer(pCity.getOwner())
		iUnitOwner = pUnit.getOwner()
		if pCity.getOwner() == iUnitOwner or gc.getTeam(pCityPlayer.getTeam()).isVassal(gc.getPlayer(iUnitOwner).getTeam()):
				iStateReligion = gc.getPlayer(iUnitOwner).getStateReligion()
				if iStateReligion != -1:
						if pCity.isHasReligion(iStateReligion):
								for iReligion in range(gc.getNumReligionInfos()):
										if pCity.isHasReligion(iReligion):
												if pCity.isHolyCityByType(iReligion) == 0:
														if iReligion != iStateReligion:
																if iReligion != gc.getUnitInfo(pUnit.getUnitType()).getPrereqReligion():
																		return True
		return False

def doInquisitorPersecution(pCity, pUnit):
		pPlayer = gc.getPlayer(pCity.getOwner())
		iPlayer = pPlayer.getID()

		iNumReligions = gc.getNumReligionInfos()
		# HI soll PopUp bekommen
		if pPlayer.isHuman():
				# Dies soll doppelte Popups in PB-Spielen vermeiden.
				if iPlayer == gc.getGame().getActivePlayer():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_INQUISITION", (pCity.getName(), )))
						popupInfo.setData1(iPlayer)
						popupInfo.setData2(pCity.getID())
						popupInfo.setData3(pUnit.getID())
						popupInfo.setOnClickedPythonCallback("popupReliaustreibung")  # EntryPoints/CvScreenInterface und CvGameUtils / 704
						for iReligion in range(iNumReligions):
								if pCity.isHasReligion(iReligion) and iReligion != pPlayer.getStateReligion() and not pCity.isHolyCityByType(iReligion):
										if iReligion != gc.getUnitInfo(pUnit.getUnitType()).getPrereqReligion():
												popupInfo.addPythonButton(gc.getReligionInfo(iReligion).getText(), gc.getReligionInfo(iReligion).getButton())
						popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_INQUISITION_CANCEL", ("", )), "Art/Interface/Buttons/General/button_alert_new.dds")
						popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
						popupInfo.addPopup(iPlayer)


def doInquisitorPersecution2(iPlayer, iCity, iButton, iReligion, iUnit):
		pPlayer = gc.getPlayer(iPlayer)
		pCity = pPlayer.getCity(iCity)
		szButton = gc.getUnitInfo(gc.getInfoTypeForString("UNIT_INQUISITOR")).getButton()
		iStateReligion = pPlayer.getStateReligion()
		iNumReligions = gc.getNumReligionInfos()
		# gets a list of all religions in the city except state religion
		lCityReligions = []
		for iReligionLoop in range(iNumReligions):
				if pCity.isHasReligion(iReligionLoop):
						if pCity.isHolyCityByType(iReligionLoop) == 0 and iReligionLoop != iStateReligion:
								lCityReligions.append(iReligionLoop)

		# Wenn die Religion ueber PopUp kommt, muss sie mittels Buttonreihenfolge gefunden werden
		if iReligion == -1:
				iReligion = lCityReligions[iButton]

		if iReligion != -1:
				if iReligion == iStateReligion:
						iHC = -25
				else:
						iHC = 25
				pUnit = pPlayer.getUnit(iUnit)
				if pUnit is not None and not pUnit.isNone():
						# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
						pUnit.kill(True, -1)  # RAMK_CTD

				# Does Persecution succeed
				iRandom = CvUtil.myRandom(100, "pers_success")
				if iRandom < 60 + (len(lCityReligions) * 5) + iHC:
						pCity.setHasReligion(iReligion, 0, 0, 0)
						if pPlayer.isHuman():
								CyInterface().addMessage(iPlayer, True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION", (pCity.getName(),)), "AS2D_PLAGUE", 2, szButton, ColorTypes(8), pCity.getX(), pCity.getY(), True, True)

						# remove its buildings
						iRange = gc.getNumBuildingInfos()
						for iBuildingLoop in range(iRange):
								if pCity.isHasBuilding(iBuildingLoop):
										pBuilding = gc.getBuildingInfo(iBuildingLoop)
										if pBuilding.getPrereqReligion() == iReligion:
												# Wunder sollen nicht betroffen werden
												iBuildingClass = pBuilding.getBuildingClassType()
												#thisBuildingClass = gc.getBuildingClassInfo(iBuildingClass)
												# if thisBuildingClass.getMaxGlobalInstances() == -1 \
												# and thisBuildingClass.getMaxTeamInstances() == -1 and thisBuildingClass.getMaxPlayerInstances() == -1:
												if not isWorldWonderClass(iBuildingClass) and not isTeamWonderClass(iBuildingClass) and not isNationalWonderClass(iBuildingClass):
														pCity.setNumRealBuilding(iBuildingLoop, 0)
														# if pPlayer.isHuman():
														# Meldung dass das Gebaeude zerstoert wurde
														# CyInterface().addMessage(iPlayer,True,15,CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_Bildersturm",(pCity.getName(),)),"AS2D_PLAGUE",2,szButton,ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

						# increasing Anger or Sympathy for an AI
						iRange = gc.getMAX_PLAYERS()
						for iSecondPlayer in range(iRange):
								pSecondPlayer = gc.getPlayer(iSecondPlayer)
								pReligion = gc.getReligionInfo(iReligion)

								# increases Anger for all AIs which have this religion as State Religion
								if iReligion == pSecondPlayer.getStateReligion() and pSecondPlayer.isAlive():
										pSecondPlayer.AI_changeAttitudeExtra(iPlayer, -2)
								# increases Sympathy for all AIs which have the same State Religion as the inquisitor
								elif pPlayer.getStateReligion() == pSecondPlayer.getStateReligion() and pSecondPlayer.isAlive():
										pSecondPlayer.AI_changeAttitudeExtra(iPlayer, 1)

								# info for all
								if pSecondPlayer.isHuman():
										iSecTeam = pSecondPlayer.getTeam()
										if gc.getTeam(iSecTeam).isHasMet(pPlayer.getTeam()):
												CyInterface().addMessage(iSecondPlayer, True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_GLOBAL",
														(pCity.getName(), pReligion.getText())), None, 2, szButton, ColorTypes(10), pCity.getX(), pCity.getY(), True, True)

						# info for the player
						CyInterface().addMessage(iPlayer, True, 20, CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_GLOBAL_NEG",
								(pCity.getName(), pReligion.getText())), None, 2, szButton, ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
						CyInterface().addMessage(iPlayer, True, 20, CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_GLOBAL_POS",
								(pCity.getName(), pReligion.getText())), None, 2, szButton, ColorTypes(8), pCity.getX(), pCity.getY(), True, True)

						# decrease population by 1, even if mission fails
						if pCity.getPopulation() > 1:
								pCity.changePopulation(-1)
								doCheckCityState(pCity)

				# Persecution fails
				elif pPlayer.isHuman():
						CyInterface().addMessage(iPlayer, True, 15, CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_FAIL", (pCity.getName(),)), "AS2D_SABOTAGE", 2, szButton, ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

		# City Revolt
		pCity.changeOccupationTimer(1)
		# ------

# end Inquisition / Religionsaustreibung


def doTurnCityRevolt(pCity):
		if pCity is None or pCity.isNone():
				return
		if pCity.getOwner() == gc.getBARBARIAN_PLAYER():
				return
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		pPlot = pCity.plot()
		bCityIsInRevolt = False
		iCityRevoltTurns = 4
		# Einheiten senken Dauer
		if pPlot.getNumUnits() > pCity.getPopulation():
				iCityRevoltTurns = 2

		# Conquered city (% culture / 10)
		iOriginalOwner = pCity.getOriginalOwner()
		if iOriginalOwner != gc.getBARBARIAN_PLAYER() and iOriginalOwner != iPlayer and gc.getPlayer(iOriginalOwner).isAlive():
				iForeignCulture = pPlot.calculateTeamCulturePercent(gc.getPlayer(iOriginalOwner).getTeam())
				if iForeignCulture >= 20:
						# Pro Einheit 1% Bonus
						if CvUtil.myRandom(100, "doTurnCityRevolt1") + pPlot.getNumDefenders(iPlayer) < iForeignCulture / 10:
								bCityIsInRevolt = True
								text = "TXT_KEY_MESSAGE_CITY_REVOLT_YEARNING"

		# Nation is in anarchy (20%, AI 5%)
		if not bCityIsInRevolt:
				if pPlayer.getAnarchyTurns() > 0:
						if pPlayer.isHuman():
								iTmp = 5
						else:
								iTmp = 20
						if CvUtil.myRandom(iTmp, "doTurnCityRevolt2") == 0:
								bCityIsInRevolt = True
								iCityRevoltTurns = pPlayer.getAnarchyTurns()
								text = "TXT_KEY_MESSAGE_CITY_REVOLT_ANARCHY"

		# city has no state religion (3%, AI 1%)
		if not bCityIsInRevolt:
				iRel = pPlayer.getStateReligion()
				if iRel != -1 and not pCity.isHasReligion(iRel) and not pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_HENOTHEISM")):
						iBuilding = gc.getInfoTypeForString("BUILDING_STADT")
						if pCity.isHasBuilding(iBuilding):

								iTeam = pPlayer.getTeam()
								if gc.getTeam(iTeam).getBuildingClassCount(gc.getInfoTypeForString("BUILDINGCLASS_GREAT_PANTHEON")) == 0:

										if pPlayer.isHuman():
												iTmp = 20
										else:
												iTmp = 60
										if CvUtil.myRandom(iTmp, "doTurnCityRevolt3") == 0:
												bCityIsInRevolt = True
												text = "TXT_KEY_MESSAGE_CITY_REVOLT_RELIGION"

		# city is unhappy (3%, AI 1%)
		if not bCityIsInRevolt:
				if pCity.unhappyLevel(0) > pCity.happyLevel():
						if pPlayer.isHuman():
								iTmp = 30
						else:
								iTmp = 100
						if CvUtil.myRandom(iTmp, "doTurnCityRevolt4") == 0:
								bCityIsInRevolt = True
								text = "TXT_KEY_MESSAGE_CITY_REVOLT_UNHAPPINESS"

		# high taxes
		# PAE V: not for AI
		if not bCityIsInRevolt:
				iTaxesLimit = getTaxesLimit(pPlayer)
				if pPlayer.getCommercePercent(0) > iTaxesLimit and pPlayer.isHuman():
						iChance = int((pPlayer.getCommercePercent(0) - iTaxesLimit) / 5)
						# Pro Happy Citizen 5% Nachlass
						iChance = iChance - pCity.happyLevel() + pCity.unhappyLevel(0)
						if iChance > 0 and CvUtil.myRandom(100, "doTurnCityRevolt5") < iChance:
								bCityIsInRevolt = True
								iCityRevoltTurns = iChance
								text = "TXT_KEY_MESSAGE_CITY_REVOLT_TAXES"

		# City Revolt PopUp / Human and AI
		if bCityIsInRevolt:

				# Human PopUp 675
				if pPlayer.isHuman():
						CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText(text, (pCity.getName(),)), "AS2D_REVOLTSTART", 2,
																		 "Art/Interface/Buttons/Techs/button_brandschatzen.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
						popupInfo.setText(CyTranslator().getText(text, (pCity.getName(),)))
						popupInfo.setData1(iPlayer)
						popupInfo.setData2(pCity.getID())
						popupInfo.setData3(iCityRevoltTurns)
						popupInfo.setOnClickedPythonCallback("popupRevoltPayment")
						iGold = pCity.getPopulation()*10
						popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_REVOLT_1", (iGold,)), "")
						iGold = pCity.getPopulation()*5
						popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_REVOLT_2", (iGold,)), "")
						popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_REVOLT_CANCEL", ()), "")
						popupInfo.addPopup(iPlayer)

				# AI will pay (90%) if they have the money
				elif CvUtil.myRandom(100, "doTurnCityRevolt6") < 90:
						if pPlayer.getGold() > pCity.getPopulation() * 10:
								iBetrag = pCity.getPopulation() * 10
								iChance = 20
						elif pPlayer.getGold() > pCity.getPopulation() * 5:
								iBetrag = pCity.getPopulation() * 5
								iChance = 50
						else:
								iBetrag = 0
								iChance = 100
						pPlayer.changeGold(iBetrag)
						# even though, there is a chance of revolting
						if CvUtil.myRandom(100, "doTurnCityRevolt7") < iChance:
								# pCity.setOccupationTimer(iCityRevoltTurns)
								#doCityRevolt(pCity, iCityRevoltTurns)
								doStartCivilWar(pCity, 100)
				else:
						# pCity.setOccupationTimer(iCityRevoltTurns)
						#doCityRevolt(pCity, iCityRevoltTurns)
						doStartCivilWar(pCity, 100)

				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Stadtrevolte PopUp (Zeile 4222)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

				# City Revolt
				# iTurns = deaktiv


def doCityRevolt(pCity, iTurns):
		if pCity is None or pCity.isNone():
				return

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("City Revolt (Zeile 6485)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

		if iTurns < 2:
				iTurns = 2

		pPlot = pCity.plot()
		# Einheiten stilllegen
		iRange = pPlot.getNumUnits()
		for iUnit in range(iRange):
				pLoopUnit = pPlot.getUnit(iUnit)
				if pLoopUnit:
						iDamage = pLoopUnit.getDamage()
						if iDamage < 30:
								pLoopUnit.setDamage(30, -1)
						if CvUtil.myRandom(2, "cityRevolt") == 1:
								pLoopUnit.setImmobileTimer(iTurns)

		# Stadtaufruhr
		pCity.changeHurryAngerTimer(iTurns)
		#pCity.changeOccupationTimer (iTurns)
		pCity.setOccupationTimer(iTurns)

		# iPlayer = pCity.getOwner()
		# pPlayer = gc.getPlayer(iPlayer)
#    if gc.getNumEventTriggerInfos() > 0: # prevents mods that don't have events from getting an error
#       iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_DESPOT_REVOLT')
#       if iEvent != -1 and gc.getGame().isEventActive(iEvent):
#          triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCity.getX(), pCity.getY(), iPlayer, pCity.getID(), -1, -1, -1, -1)
#       else: pCity.setOccupationTimer(2)
#    else: pCity.setOccupationTimer(2)


# --- renegading city
# A nearby city of pCity will revolt
def doNextCityRevolt(iX, iY, iOwner, iAttacker):
		if iOwner != -1 and iOwner != gc.getBARBARIAN_PLAYER():
				pOwner = gc.getPlayer(iOwner)
				if pOwner.getNumCities() > 1:
						# ***TEST***
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Next City Revolt (Zeile 4766)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

						# Stadtentfernung messen und naeheste Stadt definieren / die Stadt soll innerhalb 10 Plots entfernt sein.
						iRevoltCity = -1
						iCityCheck = -1
						# City with forbidden palace shall not revolt
						# ~ if gc.getTeam(pOwner.getTeam()).isHasTech(gc.getInfoTypeForString('TECH_POLYARCHY')): iBuilding = gc.getInfoTypeForString('BUILDING_PRAEFECTUR')
						# ~ else: iBuilding = gc.getInfoTypeForString('BUILDING_PROVINZPALAST')
						iRange = pOwner.getNumCities()
						for i in range(iRange):
								pLoopCity = pOwner.getCity(i)
								if pLoopCity is not None and not pLoopCity.isNone():
										if not pLoopCity.isCapital() and pLoopCity.getOccupationTimer() < 1 and not pLoopCity.isGovernmentCenter() and pLoopCity.getOwner() != iAttacker:
												tmpX = pLoopCity.getX()
												tmpY = pLoopCity.getY()
												iBetrag = plotDistance(iX, iY, tmpX, tmpY)
												if iBetrag > 0 and iBetrag < 11 and (iCityCheck == -1 or iCityCheck > iBetrag):
														iCityCheck = iBetrag
														iRevoltCity = i
										#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("City",i)), None, 2, None, ColorTypes(10), 0, 0, False, False)
										#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Betrag",iBetrag)), None, 2, None, ColorTypes(10), 0, 0, False, False)

						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Revolt",iRevoltCity)), None, 2, None, ColorTypes(10), 0, 0, False, False)

						# Stadt soll revoltieren
						if iRevoltCity != -1:
								pCity = pOwner.getCity(iRevoltCity)
								# pCity.setOccupationTimer(3)
								doCityRevolt(pCity, 3)

								# Message for the other city revolt
								if gc.getPlayer(iAttacker).isHuman():
										iRand = 1 + CvUtil.myRandom(6, "msg_cityRevolt")
										CyInterface().addMessage(iAttacker, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_REVOLTS_1_"+str(iRand), (pCity.getName(), 0)),
																						 "AS2D_REVOLTSTART", 2, "Art/Interface/Buttons/Techs/button_brandschatzen.dds", ColorTypes(8), pCity.getX(), pCity.getY(), True, True)
								elif gc.getPlayer(iOwner).isHuman():
										iRand = 1 + CvUtil.myRandom(6, "msg_ownerCityRevolt")
										CyInterface().addMessage(iOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_REVOLTS_2_"+str(iRand), (pCity.getName(), 0)),
																						 "AS2D_REVOLTSTART", 2, "Art/Interface/Buttons/Techs/button_brandschatzen.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

				# --- next city revolt


def doCityCheckRevoltEnd(pCity):
		if pCity is None or pCity.isNone():
				return False
		pPlot = pCity.plot()
		iRange = pPlot.getNumUnits()
		for iUnit in range(iRange):
				pUnit = pPlot.getUnit(iUnit)
				# General oder Rhetoriker
				if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_RHETORIK")) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER")):
						if pCity.getOccupationTimer() > 0:
								pCity.setOccupationTimer(0)
						if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")):
								pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR"), 0)
						pPlayer = gc.getPlayer(pCity.getOwner())
						if pPlayer.isHuman():
								CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_1", (pCity.getName(),)), "AS2D_WELOVEKING", 2,
																				 gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")).getButton(), ColorTypes(8), pCity.getX(), pCity.getY(), True, True)
						return True
		return False


def doDesertification(pCity, pUnit):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iCurrentEra = pPlayer.getCurrentEra()
		iUnitCombatType = pUnit.getUnitCombatType()
		if iCurrentEra > 0 and iUnitCombatType > 0:
				if iUnitCombatType in [gc.getInfoTypeForString("UNITCOMBAT_ARCHER"), gc.getInfoTypeForString("UNITCOMBAT_SKIRMISHER")]:
						return

				lNoForgeUnit = [
						gc.getInfoTypeForString("UNIT_WARRIOR"),
						gc.getInfoTypeForString("UNIT_AXEWARRIOR"),
						gc.getInfoTypeForString("UNIT_LIGHT_SPEARMAN"),
						gc.getInfoTypeForString("UNIT_HUNTER"),
						gc.getInfoTypeForString("UNIT_SCOUT"),
						gc.getInfoTypeForString("UNIT_MOUNTED_SCOUT"),
						gc.getInfoTypeForString("UNIT_WORKBOAT"),
						gc.getInfoTypeForString("UNIT_DRUIDE"),
						gc.getInfoTypeForString("UNIT_BRAHMANE"),
						gc.getInfoTypeForString("UNIT_HORSE"),
						gc.getInfoTypeForString("UNIT_CAMEL"),
						gc.getInfoTypeForString("UNIT_ELEFANT")
				]

				if pUnit.getUnitType() not in lNoForgeUnit:
						# ***TEST***
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Waldrodung",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

						iLager = gc.getInfoTypeForString("IMPROVEMENT_CAMP")
						iHolzLager = gc.getInfoTypeForString("IMPROVEMENT_LUMBER_CAMP")
						iMine = gc.getInfoTypeForString("IMPROVEMENT_MINE")

						iFeatForest = gc.getInfoTypeForString("FEATURE_FOREST")
						iFeatSavanna = gc.getInfoTypeForString("FEATURE_SAVANNA")
						iFeatJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
						iFeatDichterWald = gc.getInfoTypeForString("FEATURE_DICHTERWALD")

						lFeatures = [iFeatForest, iFeatSavanna, iFeatJungle, iFeatDichterWald]
						# nicht bei Zedernholz
						iBonusZedern = gc.getInfoTypeForString("BONUS_ZEDERNHOLZ")

						# Einen guenstigen Plot auswaehlen
						# Priority:
						# 1. Leerer Wald oder Mine
						# 2. Leere Savanne
						# 3. Leerer Dschungel
						# 4. Bewirtschaftetes Feld mit Wald aber ohne Holzlager
						# 5. Dichter Wald
						# 6. Wald im feindlichen Terrain (-1 Beziehung zum Nachbarn), aber nur wenn kein Holzlager drauf is
						PlotArray1 = []
						PlotArray2 = []
						PlotArray3 = []
						PlotArray4 = []
						PlotArray5 = []
						PlotArray6 = []
						PlotArrayX = []

						for iI in range(gc.getNUM_CITY_PLOTS()):
								pLoopPlot = pCity.getCityIndexPlot(iI)
								if pLoopPlot is not None and not pLoopPlot.isNone():
										iPlotFeature = pLoopPlot.getFeatureType()
										if iPlotFeature in lFeatures:
												iPlotImprovement = pLoopPlot.getImprovementType()
												iLoopPlayer = pLoopPlot.getOwner()
												if pLoopPlot.getBonusType(iLoopPlayer) != iBonusZedern:
														if iLoopPlayer == iPlayer:
																if iPlotImprovement == iMine:
																		PlotArray1.append(pLoopPlot)
																if iPlotImprovement == -1:
																		if iPlotFeature == iFeatForest:
																				PlotArray1.append(pLoopPlot)
																		elif iPlotFeature == iFeatSavanna:
																				PlotArray2.append(pLoopPlot)
																		elif iPlotFeature == iFeatJungle:
																				PlotArray3.append(pLoopPlot)
																		elif iPlotFeature == iFeatDichterWald:
																				PlotArray5.append(pLoopPlot)
																elif iPlotImprovement != iHolzLager and iPlotImprovement != iLager:
																		PlotArray4.append(pLoopPlot)

														elif iPlotImprovement != iHolzLager and iPlotImprovement != iLager:
																if iPlotFeature != iFeatDichterWald:
																		# PAE V: no unit on the plot (Holzraub)
																		if pLoopPlot.getNumUnits() == 0:
																				PlotArray6.append(pLoopPlot)

						# Plot wird ausgewaehlt, nach Prioritaet zuerst immer nur Wald checken, wenn keine mehr da, dann Savanne, etc...
						# Wald: Chance: Bronzezeit: 4%, Eisenzeit: 5%, Klassik: 6%
						if PlotArray1:
								iChance = 30 - iCurrentEra * 5
								if CvUtil.myRandom(iChance, "des1") == 0:
										PlotArrayX = PlotArray1
						# Savanne: Bronze: 5%, Eisen: 10%, Klassik: 20%
						elif PlotArray2:
								iChance = 20 - iCurrentEra * 5
								if CvUtil.myRandom(iChance, "des2") == 0:
										PlotArrayX = PlotArray2
						# Dschungel: wie Wald
						elif PlotArray3:
								iChance = 30 - iCurrentEra * 5
								if CvUtil.myRandom(iChance, "des3") == 0:
										PlotArrayX = PlotArray3
						# Bewirt. Feld ohne Holzlager: wie Savanne
						elif PlotArray4:
								iChance = 20 - iCurrentEra * 5
								if CvUtil.myRandom(iChance, "des4") == 0:
										PlotArrayX = PlotArray4
						# Dichter Wald: Bronze: 2%, Eisen: 2.5%, Klassik: 3%
						elif PlotArray5:
								iChance = 60 - iCurrentEra * 10
								if CvUtil.myRandom(iChance, "des5") == 0:
										PlotArrayX = PlotArray5

						# Ausl. Feld 10%, erst wenn es nur mehr 1 Waldfeld gibt (das soll auch bleiben)
						if len(PlotArray1) + len(PlotArray2) + len(PlotArray3) + len(PlotArray4) + len(PlotArray5) < 2:
								PlotArrayX = []  # Feld leeren
								if PlotArray6 and CvUtil.myRandom(10, "des6") == 0:
										PlotArrayX = PlotArray6

						# Gibts einen Waldplot
						if PlotArrayX:
								iPlot = CvUtil.myRandom(len(PlotArrayX), "des7")
								pPlot = PlotArrayX[iPlot]
								iPlotPlayer = pPlot.getOwner()
								# Auswirkungen Feature (Wald) entfernen, Holzlager entfernen, Nachbar checken
								# Feature (Wald) entfernen
								# Dichten Wald zu normalen Wald machen
								if pPlot.getFeatureType() == iFeatDichterWald:
										pPlot.setFeatureType(iFeatForest, 0)
								else:
										pPlot.setFeatureType(-1, 0)
										# Lumber camp entfernen
										# Flunky: Holzlager-Felder werden garnicht erst ausgewaehlt
										#if PlotArrayX[iPlot].getImprovementType() == iHolzLager: PlotArrayX[iPlot].setImprovementType(-1)

								# Meldung
								# Attention: AS2D_CHOP_WOOD is additional defined in XML/Audio/Audio2DScripts.xml   (not used, AS2D_BUILD_FORGE instead)
								if iPlotPlayer == iPlayer:
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_RODUNG_1", (pCity.getName(), 0)), 'AS2D_BUILD_FORGE', 2,
																						 ',Art/Interface/Buttons/Builds/BuildChopDown.dds,Art/Interface/Buttons/Actions_Builds_LeaderHeads_Specialists_Atlas.dds,7,8', ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)

								elif iPlotPlayer > -1 and iPlotPlayer != gc.getBARBARIAN_PLAYER():
										pPlotPlayer = gc.getPlayer(iPlotPlayer)
										if pPlayer.isHuman():
												CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_RODUNG_2", (pPlotPlayer.getCivilizationShortDescription(0), pPlotPlayer.getCivilizationAdjective(1))), 'AS2D_BUILD_FORGE',
																								 2, ',Art/Interface/Buttons/Builds/BuildChopDown.dds,Art/Interface/Buttons/Actions_Builds_LeaderHeads_Specialists_Atlas.dds,7,8', ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
										if pPlotPlayer.isHuman():
												CyInterface().addMessage(iPlotPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_RODUNG_3", (pPlayer.getCivilizationShortDescription(0), 0)), 'AS2D_BUILD_FORGE', 2,
																								 ',Art/Interface/Buttons/Builds/BuildChopDown.dds,Art/Interface/Buttons/Actions_Builds_LeaderHeads_Specialists_Atlas.dds,7,8', ColorTypes(7), pPlot.getX(), pPlot.getY(), True, True)
										pPlotPlayer.AI_changeAttitudeExtra(iPlayer, -1)

		# Feature Waldrodung Ende

# Emigrant -----------------
def doEmigrant(pCity, pUnit):
		pPlot = pCity.plot()
		# Kultur auslesen
		txt = CvUtil.getScriptData(pUnit, ["p", "t"])
		if txt != "":
				iPlayerCulture = int(txt)
		else:
				iPlayerCulture = pUnit.getOwner()
		# Kultur
		iPlayerHC = pCity.findHighestCulture()
		if iPlayerHC == -1:
				iPlayerHC = pCity.getOwner()
		iCulture = pPlot.getCulture(iPlayerHC) / pCity.getPopulation()
		if pCity.getPopulation() == 1: iCulture /= 2

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("PlayerHC",iPlayerHC)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("PlayerHC Kultur",pPlot.getCulture(iPlayerHC))), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("iCulture",iCulture)), None, 2, None, ColorTypes(10), 0, 0, False, False)

		# der Stadt Kultur nehmen und geben
		if pPlot.getCulture(iPlayerHC) > iCulture:
				#pPlot.changeCulture(iPlayerHC, -iCulture, 1)
				pPlot.changeCulture(iPlayerCulture, iCulture, 1)
				# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)

		# Religion (ab PAE VII)
		txt = CvUtil.getScriptData(pUnit, ["rel", "t"])
		if txt != "":
				iReligion = int(txt)
				if not pCity.isHasReligion(iReligion):
						pCity.setHasReligion(iReligion, 1, 1, 0)

		pUnit.kill(True, -1)  # RAMK_CTD

		pCity.changePopulation(1)
		# PAE Provinzcheck
		doCheckCityState(pCity)

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Emigrant 2 City (Zeile 6458)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)


# disband city
def doDisbandCity(pCity, pUnit, pPlayer):
		iRand = CvUtil.myRandom(10, "disbandCity")
		if iRand < 9:

				# Missionar
				getCityMissionar(pCity, pCity.getOwner())

				# Emigrant
				if not isCityState(pCity.getOwner()):
						iUnitType = gc.getInfoTypeForString("UNIT_EMIGRANT")
						pNewUnit = pPlayer.initUnit(iUnitType, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						PAE_Unit.setUnitCulture(pNewUnit)
						PAE_Unit.setUnitReligion(pNewUnit)
						pNewUnit.finishMoves()
						pUnit.finishMoves()

				CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_DISBAND_CITY_OK",
																																										(pCity.getName(),)), "AS2D_PILLAGE", 2, None, ColorTypes(13), pCity.getX(), pCity.getY(), False, False)
				pPlayer.disband(pCity)

		else:
				CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_DISBAND_CITY_NOT_OK",
																																										(pCity.getName(),)), "AS2D_CITY_REVOLT", 2, None, ColorTypes(7), pCity.getX(), pCity.getY(), False, False)
				# pUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
				pUnit.kill(True, -1)  # RAMK_CTD

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Emigrant disbands/shrinks City (Zeile 6474)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)


# Spreading Plague -------------------------
def doSpreadPlague(pCity):
		pCityOrig = pCity
		iX = pCity.getX()
		iY = pCity.getY()
		iBuildingPlague = gc.getInfoTypeForString('BUILDING_PLAGUE')
		bSpread = False

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Pestausbreitung (Zeile 4818)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

		# Umkreis von 5 Feldern
		iRange = 5
		iCityCheck = 0
		for i in range(-iRange, iRange+1):
				for j in range(-iRange, iRange+1):
						sPlot = plotXY(iX, iY, i, j)
						if sPlot.isCity():
								sCity = sPlot.getPlotCity()
								if sCity.isConnectedTo(pCity) and not sCity.isHasBuilding(iBuildingPlague) and sCity.getPopulation() > 3:
										tmpX = sCity.getX()
										tmpY = sCity.getY()
										iBetrag = plotDistance(iX, iY, tmpX, tmpY)
										if iBetrag > 0 and (not bSpread or iCityCheck > iBetrag):
												iCityCheck = iBetrag
												PlagueCity = sCity
												bSpread = True

		# Handelsstaedte dieser Stadt
		if not bSpread:
				iTradeRoutes = pCity.getTradeRoutes()
				for i in range(iTradeRoutes):
						sCity = pCity.getTradeCity(i)
						if not sCity.isHasBuilding(iBuildingPlague) and sCity.getPopulation() > 3:
								PlagueCity = sCity
								bSpread = True
								break

		# Ausbreiten
		if bSpread:
				pCity = PlagueCity
				iPlayer = PlagueCity.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				iThisTeam = pPlayer.getTeam()
				# team = gc.getTeam(iThisTeam)

				#iMedicine1 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_MEDICINE1')
				#iMedicine2 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_MEDICINE2')
				#iMedicine3 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_MEDICINE3')
				#iMedicine4 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_HEILKUNDE')

				# City Revolt
				#if team.isHasTech(iMedicine1) or  team.isHasTech(iMedicine2) or  team.isHasTech(iMedicine3) or  team.isHasTech(iMedicine4): pCity.setOccupationTimer(2)
				# else: pCity.setOccupationTimer(3)

				# message for all
				iRange = gc.getMAX_PLAYERS()
				for iSecondPlayer in range(iRange):
						pSecondPlayer = gc.getPlayer(iSecondPlayer)
						if pSecondPlayer.isHuman():
								iSecTeam = pSecondPlayer.getTeam()
								if gc.getTeam(iSecTeam).isHasMet(iThisTeam):
										if pSecondPlayer.isHuman():
												CyInterface().addMessage(iSecondPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_SPREAD", (pCityOrig.getName(), pCity.getName())),
																								 "AS2D_PLAGUE", 2, 'Art/Interface/Buttons/Actions/button_skull.dds', ColorTypes(13), pCity.getX(), pCity.getY(), True, True)

				if pPlayer.isHuman():
						CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_SPREAD", (pCityOrig.getName(), pCity.getName())),
																		 "AS2D_PLAGUE", 2, 'Art/Interface/Buttons/Actions/button_skull.dds', ColorTypes(13), pCity.getX(), pCity.getY(), True, True)
				# end message

				# Plague building gets added into city => culture -50
				pCity.setNumRealBuilding(iBuildingPlague, 1)
				# --- plague spread


# Provinz Rebellion / Statthalter
def doProvinceRebellion(pCity):
		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Provinzrebellion (Zeile 4578)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		if pCity is None or pCity.isNone():
				return

		if pCity.isCapital():
				return

		iPlayer = pCity.getOwner()
		# pPlayer = gc.getPlayer(iPlayer)
		# iBuilding = gc.getInfoTypeForString('BUILDING_PROVINZPALAST')

		iNewOwner = gc.getBARBARIAN_PLAYER()
		iOriginal = pCity.getOriginalOwner()

		iMaxPlayers = gc.getMAX_PLAYERS()
		# iNewOwner herausfinden
		# 1. Moeglichkeit: gab es einen Vorbesitzer
		if iOriginal != iPlayer and (gc.getPlayer(iOriginal).isAlive() or gc.getGame().countCivPlayersAlive() < iMaxPlayers):
				iNewOwner = iOriginal
		# 2. Moeglichkeit: Spieler mit hoechster Kultur heraussuchen
		else:
				iPlayerHC = pCity.findHighestCulture()
				if iPlayerHC != iPlayer and iPlayerHC != -1 and gc.getPlayer(iPlayerHC).isAlive():
						iNewOwner = iPlayerHC
				# 3. Moeglichkeit: weitere Spieler mit Fremdkultur
				else:
						PlayerArray = []
						for i in range(iMaxPlayers):
								if i != iPlayer:
										if gc.getPlayer(i).isAlive() and pCity.getCulture(i) > 0:
												PlayerArray.append(i)
						if PlayerArray:
								iRand = CvUtil.myRandom(len(PlayerArray), "provReb")
								iNewOwner = PlayerArray[iRand]
		# ----------------

		# Radius 5x5 Plots und dessen Staedte checken
		iRange = 5
		iX = pCity.getX()
		iY = pCity.getY()
		for i in range(-iRange, iRange+1):
				for j in range(-iRange, iRange+1):
						loopPlot = plotXY(iX, iY, i, j)
						if loopPlot and not loopPlot.isNone():
								if loopPlot.isCity():
										loopCity = loopPlot.getPlotCity()
										if pCity.getID() != loopCity.getID() and not loopCity.isGovernmentCenter() and loopCity.getOwner() == iPlayer:
												iLoopX = iX+i
												iLoopY = iY+j
												iChance = 100
												for i2 in range(-iRange, iRange+1):
														for j2 in range(-iRange, iRange+1):
																loopPlot2 = plotXY(iLoopX, iLoopY, i2, j2)
																if loopPlot2 and not loopPlot2.isNone():
																		if loopPlot2.isCity():
																				loopCity2 = loopPlot2.getPlotCity()
																				if pCity.getID() != loopCity2.getID():
																						if loopCity2.isCapital():
																								iChance = 0
																								break
																						elif loopCity2.isGovernmentCenter():
																								iChance = 50
														if iChance == 0:
																break
												if CvUtil.myRandom(100, "provReb2") < iChance:
														doRenegadeCity(loopCity, iNewOwner, None)
		doRenegadeCity(pCity, iNewOwner, None)


def doRenegadeOnCombatResult(pLoser, pCity, iWinnerPlayer):
		# Trait Protective: Staedte laufen nicht ueber / cities do not renegade
		if pCity.hasTrait(gc.getInfoTypeForString("TRAIT_PROTECTIVE")):
				return False

		# if not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and
		if pCity.isCapital():
				return False

		# Nicht bei barbarischen Staedten:
		if pCity.getOwner() == gc.getBARBARIAN_PLAYER():
				return False

		# ab PAE V: soll nur mehr Staedte betreffen
		iBuilding = gc.getInfoTypeForString("BUILDING_STADT")
		if pCity.isHasBuilding(iBuilding):
				iLoserPlayer = pLoser.getOwner()
				pLoserPlayer = gc.getPlayer(iLoserPlayer)
				pWinnerPlayer = gc.getPlayer(iWinnerPlayer)
				pLoserPlot = pLoser.plot()
				# ab PAE V: ab Tech Enslavement / Sklaverei (removed)
				#iTech = gc.getInfoTypeForString("TECH_ENSLAVEMENT")
				iTeam = gc.getPlayer(pCity.getOwner()).getTeam()
				pTeam = gc.getTeam(iTeam)
				# if pTeam.isHasTech(iTech):

				# Anz Einheiten im Umkreis von 1 Feld, mit denen man im Krieg ist (military units)
				iUnitAnzahl = 0
				iX = pLoserPlot.getX()
				iY = pLoserPlot.getY()
				for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
						loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
						if loopPlot is not None and not loopPlot.isNone():
								iRange = loopPlot.getNumUnits()
								for iUnit in range(iRange):
										pLoopUnit = loopPlot.getUnit(iUnit)
										if pLoopUnit.isMilitaryHappiness():
												if pTeam.isAtWar(gc.getPlayer(pLoopUnit.getOwner()).getTeam()):
														iUnitAnzahl += 1

				# Anz Einheiten in der Stadt (military units)
				iPromoLoyal = gc.getInfoTypeForString("PROMOTION_LOYALITAT")
				iUnitCity = 0
				iChanceUnits = 0
				iRange = pLoserPlot.getNumUnits()
				for iUnit in range(iRange):
						pLoopUnit = pLoserPlot.getUnit(iUnit)
						if pLoopUnit.canFight():
								iUnitCity += 1
								# loyal units ?
								if pLoopUnit.isHasPromotion(iPromoLoyal):
										iChanceUnits += 3
								else:
										iChanceUnits += 1

				bCityRenegade = False
				if iUnitCity > 1 and iUnitCity * 4 < iUnitAnzahl and pCity.getPopulation() > 1:
						# Per defense point +1%
						iChanceDefense = pCity.getNaturalDefense() + pCity.getTotalDefense(0) - pCity.getDefenseDamage()
						# Per happy smile +5%
						iChanceHappiness = (pCity.happyLevel() - pCity.unhappyLevel(0)) * 2
						# Wonders: 1st +20%, 2nd +16%, 3rd +12%, 8, 4, 0
						iNumNWs = pCity.getNumNationalWonders()
						if iNumNWs < 6:
								iChanceNWs = iNumNWs * (11 - iNumNWs) * 2
						else:
								iChanceNWs = 60
						iNumWWs = pCity.getNumWorldWonders()
						if iNumWWs < 6:
								iChanceWWs = iNumWWs * (11 - iNumWWs) * 2
						else:
								iChanceWWs = 60
						# City population +5% each pop
						iChancePop = pCity.getPopulation() * 2
						# City connected with capital?
						if not pCity.isConnectedToCapital(pCity.getOwner()):
								iChancePop -= 10
						else:
								iChancePop += 10
						# bei negativ Nahrung - !
						iChancePop += pCity.foodDifference(1) * 5
						# Abstand zur Hauptstadt
						pCapitalCity = pLoserPlayer.getCapitalCity()
						if not pCapitalCity.isNone() and pCapitalCity is not None:
								iDistance = plotDistance(pCapitalCity.getX(), pCapitalCity.getY(), pCity.getX(), pCity.getY())
						else:
								iDistance = 50
						# Total
						iChanceTotal = iChanceUnits + iChanceDefense + iChanceHappiness + iChanceNWs + iChanceWWs + iChancePop - iUnitAnzahl - iDistance

						if iChanceTotal < 100:
								iChanceTotal = 100 - iChanceTotal
								iRand = CvUtil.myRandom(100, "City renegades")
								if iRand < iChanceTotal:
										bCityRenegade = True
						else:
								# don't feel too safe
								iChanceTotal = 1
						iChanceTotal = int(iChanceTotal)

						# Meldung an den Spieler
						if not bCityRenegade and pWinnerPlayer.isHuman():
								CyInterface().addMessage(iWinnerPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_RENEGADE_CHANCE", (pCity.getName(), iChanceTotal)), None, 2, None, ColorTypes(14), 0, 0, False, False)

				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("hier 1",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				# bCityRenegade = True # fuer testzwecke

				if bCityRenegade:
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, u"Renegade city: "+str(pCity.getOwner()), None, 2, None, ColorTypes(10), 0, 0, False, False)
						# Goldvergabe
						if pLoserPlayer.getNumCities() > 0:
								iGold = int(pLoserPlayer.getGold() / pLoserPlayer.getNumCities())
								pLoserPlayer.changeGold(-iGold)
								pWinnerPlayer.changeGold(iGold)
								if pWinnerPlayer.isHuman():
										CyInterface().addMessage(iWinnerPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_GOLD_1", ("", iGold)), None, 2, None, ColorTypes(8), 0, 0, False, False)
								if pLoserPlayer.isHuman():
										CyInterface().addMessage(iLoserPlayer, True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_GOLD_2", ("", iGold)), None, 2, None, ColorTypes(7), 0, 0, False, False)
						# City renegades
						doRenegadeCity(pCity, iWinnerPlayer, pLoser)

						# refresh the variable
						pAcquiredCity = pLoserPlot.getPlotCity()
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, u"Acquired city: "+str(pAcquiredCity.getOwner()), None, 2, None, ColorTypes(10), 0, 0, False, False)

						# Message
						if pWinnerPlayer.isHuman():
								if iWinnerPlayer == gc.getGame().getActivePlayer():
										CyAudioGame().Play2DSound('AS2D_REVOLTSTART')
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
								iRand = 1 + CvUtil.myRandom(5, "TXT_KEY_MESSAGE_CITY_RENEGADE_1_")
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_CITY_RENEGADE_1_"+str(iRand), (pAcquiredCity.getName(), )))

								popupInfo.setData1(pAcquiredCity.getOwner())
								popupInfo.setData2(pAcquiredCity.getID())
								popupInfo.setData3(iLoserPlayer)
								popupInfo.setOnClickedPythonCallback("popupRenegadeCity")  # EntryPoints/CvScreenInterface und CvGameUtils / 706
								# Button 0: Keep
								iRand = 1 + CvUtil.myRandom(5, "TXT_KEY_POPUP_RENEGADE_CITY_KEEP_")
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_RENEGADE_CITY_KEEP_"+str(iRand), ()),
																					",Art/Interface/Buttons/Actions/FoundCity.dds,Art/Interface/Buttons/Actions_Builds_LeaderHeads_Specialists_Atlas.dds,1,4")
								# Button 1: Enslave
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_RENEGADE_CITY_ENSLAVE_1", ()),
																					",Art/Interface/Buttons/Civics/Slavery.dds,Art/Interface/Buttons/Civics_Civilizations_Religions_Atlas.dds,8,2")
								# Button 2: Raze
								iRand = 1 + CvUtil.myRandom(5, "TXT_KEY_POPUP_RENEGADE_CITY_RAZE_")
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_RENEGADE_CITY_RAZE_"+str(iRand), ()),
																					",Art/Interface/Buttons/Builds/BuildCityRuins.dds,Art/Interface/Buttons/Actions_Builds_LeaderHeads_Specialists_Atlas.dds,8,9")
								popupInfo.addPopup(iWinnerPlayer)

						if pLoserPlayer.isHuman():
								if iLoserPlayer == gc.getGame().getActivePlayer():
										CyAudioGame().Play2DSound('AS2D_REVOLTSTART')
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								iRand = 1 + CvUtil.myRandom(5, "TXT_KEY_MESSAGE_CITY_RENEGADE_2_")
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_CITY_RENEGADE_2_"+str(iRand), (pAcquiredCity.getName(), )))
								popupInfo.addPopup(iLoserPlayer)

						return True
		return False


# ueberlaufende Stadt / City renegade
# When Unit gets attacked: LoserUnitID (must not get killed automatically) , no unit = None
def doRenegadeCity(pCity, iNewOwner, LoserUnit):
		if pCity is None or pCity.isNone():
				return
		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Renegae City New Owner",iNewOwner)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",(pCity.getName(),iNewOwner)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",(pCity.getName(),LoserUnit.getOwner())), None, 2, None, ColorTypes(10), 0, 0, False, False)

		if iNewOwner == -1:
				iNewOwner = gc.getBARBARIAN_PLAYER()
		if pCity.getOwner() == iNewOwner:
				return

		pNewOwner = gc.getPlayer(iNewOwner)
		
		iRebel = gc.getInfoTypeForString("UNIT_REBELL")
		iPartisan = gc.getInfoTypeForString("UNIT_FREEDOM_FIGHTER")
		lRebels = [iRebel, iPartisan]

		lTraitPromos = [gc.getInfoTypeForString("PROMOTION_TRAIT_AGGRESSIVE")]
		iPromoLoyal = gc.getInfoTypeForString("PROMOTION_LOYALITAT")

		iX = pCity.getX()
		iY = pCity.getY()
		pPlot = pCity.plot()
		iOldOwner = pCity.getOwner()

		# Einheiten auslesen bevor die Stadt ueberlaeuft
		UnitArray = []
		JumpArray = []

		# Kultur vorher entfernen (sonst CtD)
		pCity.setCulture(iNewOwner, 0, True)

		# Stadt wird überrannt
		if LoserUnit != None:
				# iLoserOwner = LoserUnit.getOwner()
				iLoserID = LoserUnit.getID()
		# Rebellion
		else:
				# iLoserOwner = -1
				iLoserID = -1

		iRange = pPlot.getNumUnits()
		for iUnit in range(iRange):
				pLoopUnit = pPlot.getUnit(iUnit)
				# Nicht die Einheit, die gerade gekillt wird killen, sonst Error
				if not pLoopUnit.isDead() and iLoserID != pLoopUnit.getID():
						if pLoopUnit.getCaptureUnitType(gc.getPlayer(iNewOwner).getCivilizationType()) != UnitTypes.NO_UNIT:
								continue
						# Freiheitskaempfer, Rebellen, Unsichtbare, Haendler rauswerfen
						if pLoopUnit.getUnitType() in lRebels or pLoopUnit.getInvisibleType() > -1 or pLoopUnit.getUnitType() in L.LTradeUnits:
								JumpArray.append(pLoopUnit)
						elif pLoopUnit.getOwner() == iOldOwner:
								# Einige Einheiten bleiben loyal und fliehen
								if pLoopUnit.isHasPromotion(iPromoLoyal):
										JumpArray.append(pLoopUnit)
								# die restlichen Einheiten desertieren Chance 8:10
								elif CvUtil.myRandom(10, "renCity1") < 8:
										if pLoopUnit.isCargo():
												#pLoopUnit.setTransportUnit(None)  # Fehlerquelle
												pLoopUnit.setXY(pPlot.getX(),pPlot.getY(),1,1,0)
										UnitArray.append(pLoopUnit)
								# else: Einheit kann sich noch aus dem Staub machen
								else:
										JumpArray.append(pLoopUnit)
						else:
								JumpArray.append(pLoopUnit)

		# Fremde Einheiten rauswerfen
		for pLoopUnit in JumpArray:
				pLoopUnit.jumpToNearestValidPlot()
		# auch diese Einheiten müssen temporär raus, sonst c++ error
		for pLoopUnit in UnitArray:
				pLoopUnit.jumpToNearestValidPlot()

		# Stadt laeuft automatisch ueber (CyCity pCity, BOOL bConquest, BOOL bTrade)
		pNewOwner.acquireCity(pCity, 0, 1)
		# Pointer pCity kaputt

		# Einheiten generieren
		for pLoopUnit in UnitArray:
				if pLoopUnit is None or pLoopUnit.isNone() or pLoopUnit.isDead():
						# TEST
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Test 1 - Unit none",iOldOwner)), None, 2, None, ColorTypes(10), 0, 0, False, False)
						continue

				iUnitType = pLoopUnit.getUnitType()
				# iUnitAIType = pLoopUnit.getUnitAIType() # Fehlerquelle
				iUnitAIType = -1
				iUnitCombatType = pLoopUnit.getUnitCombatType()

				# if gc.getUnitInfo(iUnitType).getUnitCaptureClassType() != -1:
				#  continue

				# UnitAIType -1 (NO_UNITAI) -> UNITAI_UNKNOWN = 0 , ATTACK = 4, City Defense = 10
				if iUnitAIType in [-1, 0]:
						if iUnitType == gc.getInfoTypeForString('UNIT_FREED_SLAVE'):
								iUnitAIType = 20  # UNITAI_ENGINEER
						elif iUnitType in [gc.getInfoTypeForString('UNIT_TRADE_MERCHANT'), gc.getInfoTypeForString('UNIT_TRADE_MERCHANTMAN')]:
								iUnitAIType = 19  # UNITAI_MERCHANT
						else:
								iUnitAIType = -1

				# Slaves will be freed, nur wenn dessen Besitzer neu ist
				if iUnitType == gc.getInfoTypeForString('UNIT_SLAVE'):
						iUnitType = gc.getInfoTypeForString('UNIT_FREED_SLAVE')
						NewUnit = pNewOwner.initUnit(iUnitType, iX, iY, UnitAITypes.UNITAI_ENGINEER, DirectionTypes.DIRECTION_SOUTH)
						PAE_Unit.copyName(NewUnit, iUnitType, pLoopUnit.getName())
				# Emigrant und dessen Kultur & Religion
				elif iUnitType == gc.getInfoTypeForString('UNIT_EMIGRANT'):
						NewUnit = pNewOwner.initUnit(iUnitType, iX, iY, UnitAITypes.UNITAI_SETTLE, DirectionTypes.DIRECTION_SOUTH)
						CvUtil.addScriptData(NewUnit, "p", iOldOwner)
						PAE_Unit.setUnitReligion(NewUnit)
						PAE_Unit.copyName(NewUnit, iUnitType, pLoopUnit.getName())
				elif iUnitType != -1:

						NewUnit = pNewOwner.initUnit(iUnitType, iX, iY, UnitAITypes(iUnitAIType), DirectionTypes.DIRECTION_SOUTH)
						PAE_Unit.copyName(NewUnit, iUnitType, pLoopUnit.getName())
						if iUnitCombatType != -1:

								#CvUtil.pyPrint('doRenegadeCity: PAE_City %s (%d/%d), Unit %s, ID: %d, isDead: %d' % (pCity.getName(),pCity.getX(),pCity.getY(),pLoopUnit.getName(),pLoopUnit.getID(), int(pLoopUnit.isDead())))

								PAE_Unit.initUnitFromUnit(pLoopUnit, NewUnit)
								NewUnit.setDamage(pLoopUnit.getDamage(), -1)
								# PAE V: Trait-Promotions
								# 1. Agg Promo weg
								# 2. Trait nur fuer Eigenbau: eroberte Einheiten sollen diese Trait-Promos nicht erhalten
								for iLoopPromo in lTraitPromos:
										NewUnit.setHasPromotion(iLoopPromo, False)

				# Nicht die Einheit, die gerade gekillt wird killen, sonst Error
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Loser ID",iLoserID)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",(pLoopUnit.getName(),pLoopUnit.getID())), None, 2, None, ColorTypes(10), 0, 0, False, False)
				pLoopUnit.kill(True, -1)

		if iNewOwner == gc.getBARBARIAN_PLAYER():
				iPartisan = PAE_Barbaren.getPartisan(pNewOwner)
				pNewOwner.initUnit(iPartisan, iX, iY, UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
				iPartisan = PAE_Barbaren.getPartisan(pNewOwner)
				pNewOwner.initUnit(iPartisan, iX, iY, UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
				iPartisan = PAE_Barbaren.getPartisan(pNewOwner)
				pNewOwner.initUnit(iPartisan, iX, iY, UnitAITypes.UNITAI_CITY_COUNTER, DirectionTypes.DIRECTION_SOUTH)

		# Nochmaliger Check: Fremde Einheiten rauswerfen
		for iUnit in range(pPlot.getNumUnits()):
				pLoopUnit = pPlot.getUnit(iUnit)
				# Nicht die Einheit, die gerade gekillt wird killen, sonst Error
				# ggf. check ob die Einheit sich dort aufhalten kann weil OG mit alt und neu?
				if not pLoopUnit.isDead() and pLoopUnit.getOwner() != iNewOwner and iLoserID != pLoopUnit.getID():
						#if pLoopUnit.getOwner() == gc.getBARBARIAN_PLAYER(): pLoopUnit.kill(True, -1)
						# else:
						pLoopUnit.jumpToNearestValidPlot()

		# Pointer anpassen
		if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				if pCity and not pCity.isNone():
						# Kultur auslesen
						iCulture = pCity.getCulture(iOldOwner)
						# Kultur regenerieren - funkt net
						if iCulture > 0:
								pCity.changeCulture(iNewOwner, iCulture, True)

						# Stadtgroesse kontrollieren
						iPop = pCity.getPopulation()
						if iPop < 1:
								pCity.setPopulation(1)

						# Kolonie/Provinz checken
						doCheckCityState(pCity)

		# Meldung an Spieler
		iOldTeam = gc.getPlayer(iOldOwner).getTeam()
		for iPlayer in range(gc.getMAX_PLAYERS()):
				if iPlayer != iNewOwner:
						pPlayer = gc.getPlayer(iPlayer)
						if pPlayer.isAlive() and pPlayer.isHuman():
								iTeam = pPlayer.getTeam()
								if gc.getTeam(iTeam).isHasMet(iOldTeam):
										button = getCityStatus(pCity, -1, -1, True)
										# Rebellion oder Belagerung
										if iLoserID == -1:
												text = "TXT_KEY_MESSAGE_RENEGADE_CITY_A"
										else:
												iRand = CvUtil.myRandom(5, "renCityMessageSiege") + 1
												text = "TXT_KEY_MESSAGE_RENEGADE_CITY_B_" + str(iRand)
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText(text, (pCity.getName(), gc.getPlayer(iOldOwner).getCivilizationDescription(0), pNewOwner.getCivilizationShortDescription(0))), "", 0, button, ColorTypes(10), iX, iY, True, True)

def AI_defendAndHire(pCity, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		pPlot = pCity.plot()
		iCiv = pPlayer.getCivilizationType()

		# Auf welchen Plots befinden sich gegnerische Einheiten
		if pPlot is not None and not pPlot.isNone():
				PlotArray = []
				iEnemyUnits = 0
				iRange = 1
				iX = pCity.getX()
				iY = pCity.getY()
				for x in range(-iRange, iRange+1):
						for y in range(-iRange, iRange+1):
								loopPlot = plotXY(iX, iY, x, y)
								if loopPlot is not None and not loopPlot.isNone():
										iNumUnits = loopPlot.getNumUnits()
										if iNumUnits >= 4:
												for i in range(iNumUnits):
														iOwner = loopPlot.getUnit(i).getOwner()
														if pTeam.isAtWar(gc.getPlayer(iOwner).getTeam()):
																if not loopPlot.getUnit(i).isInvisible(pPlayer.getTeam(), 0):
																		PlotArray.append(loopPlot)
																		iEnemyUnits += loopPlot.getNumUnits()
																		break
				# Stadteinheiten durchgehen
				if PlotArray:
						# Schleife fuer Stadteinheiten
						# Bombardement
						iNumUnits = pPlot.getNumUnits()
						for i in range(iNumUnits):
								pUnit = pPlot.getUnit(i)
								if pUnit.isRanged():
										if pUnit.getOwner() == iPlayer:
												if not pUnit.isMadeAttack() and pUnit.getImmobileTimer() <= 0:
														# getbestdefender -> getDamage
														BestDefender = []
														for plot in PlotArray:
																pBestDefender = plot.getBestDefender(-1, -1, pUnit, 1, 0, 0)
																BestDefender.append((pBestDefender.getDamage(), plot))
														# bestdefenderplot angreifen ->  pCityUnit.rangeStrike(x,y)
														BestDefender.sort()
														# Ab ca 50% Schaden aufhoeren
														if BestDefender[0][0] < 55:
																plot = BestDefender[0][1]
																pUnit.rangeStrike(plot.getX(), plot.getY())
														else:
																break

						# AI - Extern Unit support
						iCityUnits = pPlot.getNumUnits()
						iMaintainUnits = max(pCity.getYieldRate(0), 5) - iCityUnits
						# 1) Reservisten
						if iMaintainUnits > 0 and iCityUnits * 3 <= iEnemyUnits:
								iReservists = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_RESERVIST"))
								if iReservists > 0:
										# Einheiten definieren
										lResUnits = []
										# Schildtraeger fuer AI immer verfuegbar
										lResUnits.append(gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"))
										# Auxiliars
										iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_AUXILIAR"))
										if iUnit == -1:
												iUnit = gc.getInfoTypeForString("UNIT_AUXILIAR")
										if pTeam.isHasTech(gc.getUnitInfo(iUnit).getPrereqAndTech()):
												lResUnits.append(iUnit)
										iUnit = gc.getInfoTypeForString("UNIT_AUXILIAR_HORSE")
										if pTeam.isHasTech(gc.getUnitInfo(iUnit).getPrereqAndTech()) and pCity.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")):
												lResUnits.append(iUnit)
										# Archer
										iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_REFLEX_ARCHER"))
										if iUnit == -1:
												iUnit = gc.getInfoTypeForString("UNIT_REFLEX_ARCHER")
										if pCity.canTrain(iUnit, 0, 0):
												lResUnits.append(iUnit)
										else:
												lResUnits.append(gc.getInfoTypeForString("UNIT_ARCHER"))

										# PAE VI 6.2: special units
										iUnitX = -1
										# Griechen, Makedonen
										if iCiv in L.LGreeks or iCiv == gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"):
												iUnitX = gc.getInfoTypeForString("UNIT_KLERUCHOI")
										# Kelten, Germanen, Iberer
										elif iCiv in L.LNorthern or iCiv == gc.getInfoTypeForString("CIVILIZATION_IBERER"):
												iUnitX = gc.getInfoTypeForString("UNIT_SOLDURII")
										# Rom, Etrusker
										elif iCiv == gc.getInfoTypeForString("CIVILIZATION_ROME") or iCiv == gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"):
												iUnitX = gc.getInfoTypeForString("UNIT_LEGION_EVOCAT")

										if iUnitX != -1:
												if pTeam.isHasTech(gc.getUnitInfo(iUnitX).getPrereqAndTech()):
														# nur die Spezialeinheiten mobilisieren, wenn wenig Reservisten angesiedelt sind
														if iReservists < 3:
																lResUnits = [iUnitX]
														else:
																lResUnits.append(iUnitX)

										while iReservists > 0 and iMaintainUnits > 0:
												# choose unit
												iRand = CvUtil.myRandom(len(lResUnits), "AIdefend")
												iUnit = lResUnits[iRand]

												NewUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
												NewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
												NewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT2"), True)
												NewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT3"), True)
												NewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT4"), True)

												pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_RESERVIST"), -1)
												iReservists -= 1
												iMaintainUnits -= 1
												iCityUnits += 1

						# 2) Hire Mercenaries
						# Muessen Mercenaries angeheuert werden? AI Hire
						# 70% Archer
						# 30% Other
						# BETTER AI: half price
						PAE_Mercenaries.AI_doHireMercenaries(iPlayer, pCity, iMaintainUnits, iCityUnits, iEnemyUnits)


def doUnitSupply(pCity, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		pCityPlot = pCity.plot()
		popCity = pCity.getPopulation()

		iFactor = 1
		#iCityUnits = pCityPlot.getNumDefenders(iPlayer) # da sind SIEGE units dabei
		iCityUnits = 0
		iRange = pCityPlot.getNumUnits()
		for i in range(iRange):
				pLoopUnit = pCityPlot.getUnit(i)
				if pLoopUnit.isMilitaryHappiness() and pLoopUnit.getOwner() == iPlayer:
						iCityUnits += 1

		# bis Pop 3: 10 Einheiten erlaubt
		#if popCity < 3: iMaintainUnits = iCityUnits - 10
		iMaintainUnits = iCityUnits - max(pCity.getYieldRate(0), 5)  # - pCity.getCorporationYield(0)

		if iMaintainUnits <= 0:
				return

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("YieldRate " + pCity.getName(),pCity.getYieldRate(0))), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("iCityUnits",iCityUnits)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("iMaintainUnits",iMaintainUnits)), None, 2, None, ColorTypes(10), 0, 0, False, False)

		# Handicap: 0 (Settler) - 8 (Deity) ; 5 = King
		if gc.getGame().getHandicapType() < 5 or pPlayer.isHuman():
				# choose units
				# calculate food supply from SUPPLY_WAGON
				iExtraSupply = 0
				lUnitsAll = []
				iRange = pCityPlot.getNumUnits()
				for i in range(iRange):
						pLoopUnit = pCityPlot.getUnit(i)
						if pLoopUnit.getUnitCombatType() != -1 and pLoopUnit.getOwner() == iPlayer:
								if pLoopUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_HEALER"):
										if pLoopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"):
												iExtraSupply = PAE_Unit.getSupply(pLoopUnit)
												if iExtraSupply <= iMaintainUnits:
														iMaintainUnits -= iExtraSupply
														iExtraSupply = 0
												else:
														iExtraSupply -= iMaintainUnits
														iMaintainUnits = 0
												# set new supply tickets
												PAE_Unit.setSupply(pLoopUnit, iExtraSupply)
								else:
										lUnitsAll.append(pLoopUnit)

						if iMaintainUnits == 0:
								break
				numUnits = len(lUnitsAll)

				if iMaintainUnits <= 0 or numUnits <= 0:
						return

				# harm units
				#lUnitIndex = CvUtil.shuffle(numUnits, gc.getGame().getSorenRand())[:iMaintainUnits]

				# Shuffle List
				#random.shuffle(lUnitsAll) => verursacht OOS (checked 01.12.2024)

				# while len(lUnitIndex)<iMaintainUnits and iI < 3*numUnits:
				# iI += 1
				# iRand = CvUtil.myRandom(numUnits, "nextUnitSupply")
				# if not iRand in lUnitIndex:
				# lUnitIndex.append(iRand)

				# Betrifft Stadt
				# 20%: -1 Pop
				# 10%: FEATURE_SEUCHE
				iRand = CvUtil.myRandom(10, "seuche")
				# - 1 Pop
				if iRand < 2 and popCity > 1:
						pCity.changePopulation(-1)
						# bCheckCityState = True
						if pPlayer.isHuman():
								CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_UNITS_STARVATION_2", (pCity.getName(), (pCity.getYieldRate(
										0) * iFactor - iCityUnits)*(-1))), None, 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
				# Seuche
				elif iRand == 2:
						pCityPlot.setFeatureType(gc.getInfoTypeForString("FEATURE_SEUCHE"), 1)
						if pPlayer.isHuman():
								CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_UNITS_STARVATION_3", (pCity.getName(), (pCity.getYieldRate(
										0) * iFactor - iCityUnits)*(-1))), None, 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
				# less food
				elif pCity.getFood() > 10:
						# Warnung und -20% Food Storage
						iFoodStoreChange = pCity.getFood() / 100 * 20
						pCity.changeFood(-iFoodStoreChange)
						if pPlayer.isHuman():
								CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_UNITS_STARVATION_1", (pCity.getName(), (pCity.getYieldRate(
										0) * iFactor - iCityUnits)*(-1))), None, 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
				# ------

				# Betrifft Einheiten
				iJumpedOut = 0
				iRand = 0
				lRauswurf = []
				iMax = min(iMaintainUnits, len(lUnitsAll))
				for iI in range(iMax):
						while iRand not in lRauswurf:
								iRand = CvUtil.myRandom(len(lUnitsAll), "city unit supply: unit index harm")
								lRauswurf.append(iRand)
						pUnit = lUnitsAll[iRand]
						# Unit nicht mehr killen (Weihnachtsbonus :D ab 7.12.2012)
						iDamage = pUnit.getDamage()
						if iDamage < 70:
								pUnit.changeDamage(30, False)
								if gc.getPlayer(pUnit.getOwner()).isHuman():
										CyInterface().addMessage(pUnit.getOwner(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_NOSUPPLY_CITY",
										(pCity.getName(), pUnit.getName(), 30)), None, 2, None, ColorTypes(12), pUnit.getX(), pUnit.getY(), True, True)
						else:
								iJumpedOut += 1
								if pUnit.getDamage() < 85:
										pUnit.setDamage(85, pUnit.getOwner())
								pUnit.jumpToNearestValidPlot()
								if gc.getPlayer(pUnit.getOwner()).isHuman():
										CyInterface().addMessage(pUnit.getOwner(), True, 5, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_UNITS_STARVATION_4",
										(pCity.getName(), pUnit.getName())), None, 2, pUnit.getButton(), ColorTypes(12), pUnit.getX(), pUnit.getY(), True, True)

				# Wenn die Stadt durch Buildings stark heilt
				if iJumpedOut == 0:
						# Chance rauszuwerfen 33%
						if CvUtil.myRandom(3, "toomany1") == 1:
								iAnzahl = max(1, CvUtil.myRandom(iMaintainUnits, "toomany2"))
								#lUnitIndex2 = CvUtil.shuffle(iMaintainUnits, gc.getGame().getSorenRand())[:iAnzahl]
								iRand = 0
								lRauswurf = []
								iAnzahl = min(iAnzahl, len(lUnitsAll))
								for iI in range(iAnzahl):
										while iRand not in lRauswurf:
												iRand = CvUtil.myRandom(len(lUnitsAll), "city unit supply: unit index jump")
												lRauswurf.append(iRand)
										pUnit = lUnitsAll[iRand]
										pUnit.jumpToNearestValidPlot()
										if pPlayer.isHuman():
												CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_UNITS_STARVATION_4",
												(pCity.getName(), pUnit.getName())), "AS2D_STRIKE", 2, pUnit.getButton(), ColorTypes(7), pUnit.getX(), pUnit.getY(), True, True)


def doJewRevolt(pCity):
		if pCity is None or pCity.isNone():
				return False

		iReligionType = gc.getInfoTypeForString("RELIGION_JUDAISM")
		iRangeMaxPlayers = gc.getMAX_PLAYERS()
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.getStateReligion() == iReligionType:
				return False

		if pCity.happyLevel() < pCity.unhappyLevel(0):
				iChance = 3
		else:
				iChance = 1
		if iChance <= CvUtil.myRandom(50, "doJewRevolt"):
				return False

		#CivIsrael = CvUtil.findInfoTypeNum(gc.getCivilizationInfo, gc.getNumCivilizationInfos(), 'CIVILIZATION_ISRAEL')
		CivIsrael = gc.getInfoTypeForString("CIVILIZATION_ISRAEL")
		bIsraelAlive = False

		for i in range(iRangeMaxPlayers):
				loopPlayer = gc.getPlayer(i)
				# Israeliten sollen nur dann auftauchen, wenn es nicht bereits Israeliten gibt
				if loopPlayer.getCivilizationType() == CivIsrael and loopPlayer.isAlive():
						bIsraelAlive = True
						break

		# Israel versuchen zu erstellen
		iCivID = -1
		iCivID_new = -1
		iCivID_ex = -1
		if not bIsraelAlive:
				if gc.getGame().countCivPlayersAlive() < iRangeMaxPlayers:
						# nach einer bestehenden ISRAEL ID suchen
						for i in range(iRangeMaxPlayers):
								loopPlayer = gc.getPlayer(i)
								if loopPlayer.getCivilizationType() == CivIsrael and loopPlayer.isEverAlive():
										iCivID = i
										break
								if not loopPlayer.isEverAlive():
										iCivID_new = i
								if not loopPlayer.isAlive():
										iCivID_ex = i
						if iCivID == -1:
								if iCivID_new > -1:
										# freie PlayerID herausfinden
										iCivID = iCivID_new
								else:
										# wenn keine nagelneue ID frei ist, dann eine bestehende nehmen
										iCivID = iCivID_ex

		if iPlayer == gc.getGame().getActivePlayer():
				CyAudioGame().Play2DSound('AS2D_REVOLTSTART')

		# Einen guenstigen Plot auswaehlen
		rebelPlotArray = []
		rebelPlotArrayB = []
		iX = pCity.getX()
		iY = pCity.getY()

		for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
				loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
				if loopPlot and not loopPlot.isNone():
						if not loopPlot.isUnit() and loopPlot.getOwner() == iPlayer:
								if loopPlot.isHills():
										rebelPlotArray.append(loopPlot)
								elif not loopPlot.isWater() and not loopPlot.isImpassable() and not loopPlot.isCity():
										rebelPlotArrayB.append(loopPlot)
		if not rebelPlotArray:
				rebelPlotArray = rebelPlotArrayB

		if not rebelPlotArray:
				return False

		# es kann rebelliert werden
		if iCivID == -1:
				newPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		else:
				# Israel erstellen
				if CvUtil.myRandom(2, "doJewRevolt2") == 0:
						CivLeader = gc.getInfoTypeForString("LEADER_SALOMO")
				else:
						CivLeader = gc.getInfoTypeForString("LEADER_DAVID")
				gc.getGame().addPlayer(iCivID, CivLeader, CivIsrael)
				newPlayer = gc.getPlayer(iCivID)
				newTeam = gc.getTeam(newPlayer.getTeam())

				# Techs geben
				xTeam = gc.getTeam(pPlayer.getTeam())
				iTechNum = gc.getNumTechInfos()
				for iTech in range(iTechNum):
						if gc.getTechInfo(iTech):
								if xTeam.isHasTech(iTech):
										if gc.getTechInfo(iTech).isTrade():
												newTeam.setHasTech(iTech, 1, iCivID, 0, 0)

				iTech = gc.getInfoTypeForString("TECH_MILIT_STRAT")
				if not newTeam.isHasTech(iTech):
						newTeam.setHasTech(iTech, 1, iCivID, 0, 0)

				# Krieg erklaeren
				pPlayer.AI_changeAttitudeExtra(iCivID, -4)
				pTeam = gc.getTeam(pPlayer.getTeam())
				pTeam.declareWar(newPlayer.getTeam(), 0, 6)

				newPlayer.setCurrentEra(3)
				newPlayer.setGold(500)

		# Rebells x 1.5 of city pop
		iNumRebels = int(pCity.getPopulation() * 1.5)

		# City Revolt
		# pCity.setOccupationTimer(iNumRebelx)
		# City Defender damage
		doCityRevolt(pCity, pCity.getPopulation() / 2)

		rebelTypeArray = [
				gc.getInfoTypeForString("UNIT_FREEDOM_FIGHTER"),
				gc.getInfoTypeForString("UNIT_ARCHER"),
				gc.getInfoTypeForString("UNIT_SPEARMAN"),
				gc.getInfoTypeForString("UNIT_MACCABEE")
		]

		for _ in range(iNumRebels):
				iPlot = CvUtil.myRandom(len(rebelPlotArray), "doJewRevolt3")
				iUnitType = CvUtil.myRandom(len(rebelTypeArray), "doJewRevolt4")
				newPlayer.initUnit(rebelTypeArray[iUnitType], rebelPlotArray[iPlot].getX(), rebelPlotArray[iPlot].getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		for iLoopPlayer in range(iRangeMaxPlayers):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isHuman():
						pLoopTeam = gc.getTeam(pLoopPlayer.getTeam())
						if pLoopTeam.isHasMet(pPlayer.getTeam()):
								if iLoopPlayer == iPlayer:
										iColor = 7
								else:
										iColor = 10
								CyInterface().addMessage(iLoopPlayer, True, 5, CyTranslator().getText("TXT_KEY_JEWISH_REVOLT", (pPlayer.getCivilizationAdjective(1), pCity.getName())), None,
																				 InterfaceMessageTypes.MESSAGE_TYPE_INFO, 'Art/Interface/Buttons/Units/button_freedom_fighter.dds', ColorTypes(iColor), pCity.getX(), pCity.getY(), True, True)
								if pLoopPlayer.getStateReligion() == iReligionType:
										if iCivID != -1:
												pLoopPlayer.AI_changeAttitudeExtra(iCivID, 2)

				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Juedische Freiheitskaempfer (Zeile 4284)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		return True

# Statthalter verlangt Tribut
def provinceTribute(pCity):
		if pCity is None or pCity.isNone():
				return False
		# getNumRealBuilding geht nicht
		# getNumBuilding geht auch nicht
		if not pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZPALAST")):
				return False

		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		# PAE III
		#iCityIntervall = gc.getGame().getGameTurn() - pCity.getGameTurnFounded()
		# if iCityIntervall > 0 and iCityIntervall % 30 == 0 and iPlayer != -1:

		# PAE IV: 33 (3%), PAE V: 50 (2%)
		# if not gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_POLYARCHY")) and CvUtil.myRandom(50, "provinceTribute") < 1:

		if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_POLYARCHY")):
				return False
		bDoRebellion = False
		# PAE VI: alle 10 Runden, Chance 25%
		if pCity.getGameTurnFounded() % 10 == gc.getGame().getGameTurn() % 10 and CvUtil.myRandom(4, "provinceTribute") == 1:
				#bDoRebellion = False
				iBuildingClass = gc.getInfoTypeForString("BUILDINGCLASS_PROVINZPALAST")
				iGold = pPlayer.getGold()
				iTribut = pCity.getPopulation() * 6
				iTribut += CvUtil.myRandom(iTribut / 3, "Tribut")
				iTribut2 = iTribut / 2
				iBuildingHappiness = pCity.getBuildingHappyChange(iBuildingClass)
				# Human PopUp
				if pPlayer.isHuman():
						# Dies soll doppelte Popups in PB-Spielen vermeiden.
						if iPlayer == gc.getGame().getActivePlayer():
								iRand = CvUtil.myRandom(11, "TXT_KEY_POPUP_PROVINZHAUPTSTADT_DEMAND_")
								szText = CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_DEMAND_"+str(iRand), (pCity.getName(), iTribut))
								szText += CyTranslator().getText("[NEWLINE][NEWLINE]", ()) + CyTranslator().getText("TXT_KEY_POPUP_STATTHALTER_HALTUNG", ())
								szText += u": %d " % (abs(iBuildingHappiness))
								if iBuildingHappiness < 0:
										szText += CyTranslator().getText("[ICON_UNHAPPY]", ())
								else:
										szText += CyTranslator().getText("[ICON_HAPPY]", ())

								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
								popupInfo.setText(szText)
								popupInfo.setData1(iPlayer)
								popupInfo.setData2(pCity.getID())
								popupInfo.setData3(iTribut)
								popupInfo.setOnClickedPythonCallback("popupProvinzPayment")  # ModNetMessage 678

								if iGold >= iTribut:
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_ANSWER_1", (iTribut,)), "")
								if iGold >= iTribut2:
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_ANSWER_2", (iTribut2,)), "")
								if iGold > 0 and iGold < iTribut2:
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_ANSWER_2_1", (iGold,)), "")
								iRand = 1 + CvUtil.myRandom(10, "TXT_KEY_POPUP_PROVINZHAUPTSTADT_ANSWER_3_")
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_PROVINZHAUPTSTADT_ANSWER_3_"+str(iRand), ()), "")

								popupInfo.addPopup(iPlayer)
				else:
						# AI
						# Wenn iGold > iTribut * 3: 1 - 20%, 2 - 80%, 3 - 0%
						# Wenn iGold > iTribut * 2: 1 - 10%, 2 - 80%, 3 - 10%
						# Wenn iGold >= iTribut:    1 -  0%, 2 - 80%, 3 - 20%
						# Wenn iGold >= iTribut2:   1 -  0%, 2 - 70%, 3 - 30%
						# Wenn iGold > 0:           1 -  0%, 2 - 60%, 3 - 40%
						iAddHappiness = -1
						iRand = CvUtil.myRandom(10, "provinceTribute2")
						iRandRebellion = CvUtil.myRandom(100, "provinceTribute3")
						bPaid = False
						bDouble = False

						if iGold > iTribut * 3:
								if iRand < 2:
										pPlayer.changeGold(-iTribut)
										iAddHappiness = 2
										bDouble = True
								else:
										pPlayer.changeGold(-iTribut2)
										iAddHappiness = 1
								bPaid = True

						elif iGold > iTribut * 2:
								if iRand == 0:
										pPlayer.changeGold(-iTribut)
										iAddHappiness = 2
										bDouble = True
								elif iRand < 9:
										pPlayer.changeGold(-iTribut2)
										iAddHappiness = 1
								bPaid = True

						elif iGold >= iTribut:
								if iRand < 8:
										pPlayer.changeGold(-iTribut2)
										iAddHappiness = 1
										bPaid = True

						elif iGold >= iTribut2:
								if iRand < 7:
										pPlayer.changeGold(-iTribut2)
										iAddHappiness = 1
										bPaid = True

						elif iGold >= 0:
								if iRand < 6:
										pPlayer.setGold(0)
										iAddHappiness = 0

						# Happiness setzen (Man muss immer den aktuellen Wert + die Aenderung setzen)
						pCity.setBuildingHappyChange(iBuildingClass, iBuildingHappiness + iAddHappiness)

						# Chance einer Rebellion: Unhappy Faces * Capital Distance
						iCityHappiness = pCity.happyLevel() - pCity.unhappyLevel(0)
						if iCityHappiness < 0:
								# Abstand zur Hauptstadt
								pCapital = pPlayer.getCapitalCity()
								if pCapital and not pCapital.isNone():
										iDistance = plotDistance(pCapital.getX(), pCapital.getY(), pCity.getX(), pCity.getY())
								else:
										iDistance = 20
								iChance = iCityHappiness * (-1) * iDistance
								if iChance > iRandRebellion:
										bDoRebellion = True

						if bDoRebellion:
								doProvinceRebellion(pCity)
						elif bPaid:
								eOrigCiv = gc.getCivilizationInfo(gc.getPlayer(pCity.getOriginalOwner()).getCivilizationType())
								# 1 Unit as gift:
								lGift = []

								iUnit = eOrigCiv.getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_AUXILIAR"))
								if iUnit != -1:
										lGift.append(iUnit)
								else:
										lGift.append(gc.getInfoTypeForString("UNIT_AUXILIAR"))

								iUnit2 = gc.getInfoTypeForString("UNIT_AUXILIAR_HORSE")
								if pCity.canTrain(iUnit2, 0, 0):
										lGift.append(iUnit2)
								# Food
								lGift.append(gc.getInfoTypeForString("UNIT_SUPPLY_FOOD"))
								# Slave
								if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")):
										lGift.append(gc.getInfoTypeForString("UNIT_SLAVE"))
								# Mounted
								if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STABLE")):
										lGift.append(gc.getInfoTypeForString("UNIT_HORSE"))
										lMounted = [
												gc.getInfoTypeForString("UNIT_CHARIOT"),
												gc.getInfoTypeForString("UNIT_HORSE_ARCHER"),
												gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN")
										]
										for iUnit in lMounted:
												if pCity.canTrain(iUnit, 0, 0):
														lGift.append(iUnit)
								# Elefant
								if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_ELEPHANT_STABLE")):
										lGift.append(gc.getInfoTypeForString("UNIT_ELEFANT"))
										if pCity.canTrain(gc.getInfoTypeForString("UNIT_WAR_ELEPHANT"), 0, 0):
												lGift.append(gc.getInfoTypeForString("UNIT_WAR_ELEPHANT"))

								iRand = CvUtil.myRandom(len(lGift), "provinceTribute4")
								# ***TEST***
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Provinz Tribut Unit",lGift[iRand])), None, 2, None, ColorTypes(10), 0, 0, False, False)

								CvUtil.spawnUnit(lGift[iRand], pCity.plot(), pPlayer)
								if bDouble:
										CvUtil.spawnUnit(lGift[iRand], pCity.plot(), pPlayer)
		return bDoRebellion

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Provinz-HS Tribut-PopUp (Zeile 4367)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)


def removeCivicBuilding(pCity):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		# Buildings with prereq bonus gets checked : remove chance 10%
		building = gc.getInfoTypeForString("BUILDING_BARRACKS")
		if pCity.isHasBuilding(building):
				# Civic: Berufssoldaten/Berufsarmee -> Ausbildungslager
				if not pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_BERUFSARMEE")):
						if CvUtil.myRandom(10, "removeCivicBuilding") == 1:
								pCity.setNumRealBuilding(building, 0)
								# Meldung
								if pPlayer.isHuman():
										# Dies soll doppelte Popups in PB-Spielen vermeiden.
										if iPlayer == gc.getGame().getActivePlayer():
												szText = CyTranslator().getText("TXT_KEY_MESSAGE_CITY_CIVIC_BARRACKS", (pCity.getName(), ))
												# Ingame Message
												CyInterface().addMessage(iPlayer, True, 10, szText, None, 2, gc.getBuildingInfo(building).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
												# PopUp
												popupInfo = CyPopupInfo()
												popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
												popupInfo.setText(szText)
												popupInfo.addPopup(iPlayer)
												# Log
												CvUtil.pyPrint(szText)
								return


def removeNoBonusNoBuilding(pCity):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		bLager = False
		lLager = [
				gc.getInfoTypeForString("BUILDING_LAGERHAUS"),
				gc.getInfoTypeForString("BUILDING_LAGERHAUS_ASSYRIA")
		]
		for building in lLager:
				if pCity.isHasBuilding(building):
						bLager = True
						break

		# Buildings with prereq bonus gets checked : remove chance 5%
		building = gc.getInfoTypeForString("BUILDING_SCHMIEDE_BRONZE")
		if pCity.isHasBuilding(building):
				if bLager:
						iRand = 20
				else:
						iRand = 10
				if CvUtil.myRandom(iRand, "removeNoBonusNoBuilding1") == 1:
						bonus0 = gc.getInfoTypeForString("BONUS_COPPER")
						# bonus1 = gc.getInfoTypeForString("BONUS_COAL")
						# bonus2 = gc.getInfoTypeForString("BONUS_ZINN")
						bonus = bonusMissing(pCity, building)
						if bonus is not None:
								pCity.setNumRealBuilding(building, 0)
								# Welche Resi
								if bonus == bonus0:
										szText = "TXT_KEY_MESSAGE_CITY_NOBONUSNOBUILDING_1"
								else:
										szText = "TXT_KEY_MESSAGE_CITY_NOBONUSNOBUILDING_2"
								# Meldung
								if pPlayer.isHuman():
										# Dies soll doppelte Popups in PB-Spielen vermeiden.
										if iPlayer == gc.getGame().getActivePlayer():
												szText = CyTranslator().getText(szText, (pCity.getName(), gc.getBonusInfo(bonus).getDescription(), gc.getBuildingInfo(building).getDescription()))
												# Ingame Message
												CyInterface().addMessage(iPlayer, True, 10, szText, None, 2, gc.getBuildingInfo(building).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
												# Pop up
												popupInfo = CyPopupInfo()
												popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
												popupInfo.setText(szText)
												popupInfo.addPopup(iPlayer)
												# Log
												CvUtil.pyPrint(szText)
								return

		lBuildings = [
				gc.getInfoTypeForString("BUILDING_GRANARY"),
				gc.getInfoTypeForString("BUILDING_BRAUSTAETTE"),
				gc.getInfoTypeForString("BUILDING_BROTMANUFAKTUR")
		]
		if bLager:
				iRand = 30
		else:
				iRand = 15
		for building in lBuildings:
				if pCity.isHasBuilding(building):
						if CvUtil.myRandom(iRand, "removeNoBonusNoBuilding2") == 1:
								# bonus1 = gc.getInfoTypeForString("BONUS_WHEAT")
								# bonus2 = gc.getInfoTypeForString("BONUS_GERSTE")
								# bonus3 = gc.getInfoTypeForString("BONUS_HAFER")
								# bonus4 = gc.getInfoTypeForString("BONUS_ROGGEN")
								# bonus5 = gc.getInfoTypeForString("BONUS_HIRSE")
								bonus = bonusMissing(pCity, building)
								if bonus is not None:
										pCity.setNumRealBuilding(building, 0)
										# Meldung
										if pPlayer.isHuman():
												# Dies soll doppelte Popups in PB-Spielen vermeiden.
												if iPlayer == gc.getGame().getActivePlayer():
														szText = CyTranslator().getText("TXT_KEY_MESSAGE_CITY_NOBONUSNOBUILDING_3", (pCity.getName(), "", gc.getBuildingInfo(building).getDescription()))
														# Ingame message
														CyInterface().addMessage(iPlayer, True, 10, szText, None, 2, gc.getBuildingInfo(building).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
														# Pop Up
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(szText)
														popupInfo.addPopup(iPlayer)
														# Log
														CvUtil.pyPrint(szText)
										return

		# Resourcen, die im Handelsnetz sein muessen
		lBuildings = [
				gc.getInfoTypeForString("BUILDING_GRANARY2"),
				gc.getInfoTypeForString("BUILDING_SCHMIEDE_MESSING"),
				gc.getInfoTypeForString("BUILDING_GOLDSCHMIED"),
				gc.getInfoTypeForString("BUILDING_JUWELIER"),
				gc.getInfoTypeForString("BUILDING_BILDHAUER"),
				gc.getInfoTypeForString("BUILDING_GUSS_IRON"),
				gc.getInfoTypeForString("BUILDING_FORGE_WEAPONS")
		]
		if bLager:
				iRand = 30
		else:
				iRand = 15
		for building in lBuildings:
				if pCity.isHasBuilding(building):
						if CvUtil.myRandom(iRand, "removeNoBonusNoBuilding3") == 1:
								bonus = bonusMissing(pCity, building)
								if bonus is not None:
										pCity.setNumRealBuilding(building, 0)
										# Meldung
										if pPlayer.isHuman():
												if iPlayer == gc.getGame().getActivePlayer():
														# In %s1_city wurde durch das Fehlen der Bonusresource %s2_resource das Gebäude %s3_building abgebaut.
														szText = CyTranslator().getText("TXT_KEY_MESSAGE_CITY_NOBONUSNOBUILDING_1", (pCity.getName(), gc.getBonusInfo(bonus).getDescription(), gc.getBuildingInfo(building).getDescription()))
														# Ingame message
														CyInterface().addMessage(iPlayer, True, 10, szText, None, 2, gc.getBuildingInfo(building).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
														# Pop up
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(szText)
														popupInfo.addPopup(iPlayer)
														# Log
														CvUtil.pyPrint(szText)
										return

		# Resourcen, die im Stadtkreis sein muessen
		lBuildings = [
				gc.getInfoTypeForString("BUILDING_STABLE"),
				gc.getInfoTypeForString("BUILDING_ELEPHANT_STABLE"),
				gc.getInfoTypeForString("BUILDING_CAMEL_STABLE"),
				gc.getInfoTypeForString("BUILDING_WINERY"),
				gc.getInfoTypeForString("BUILDING_PAPYRUSPOST"),
				gc.getInfoTypeForString("BUILDING_MUREX"),
				#gc.getInfoTypeForString("BUILDING_GERBEREI"),
				gc.getInfoTypeForString("BUILDING_FURRIER"),
				gc.getInfoTypeForString("BUILDING_MARMOR_WERKSTATT")
		]
		lBuildings2 = [
				gc.getInfoTypeForString("BUILDING_GUSS_BLEI"),
				gc.getInfoTypeForString("BUILDING_GUSS_COPPER"),
				gc.getInfoTypeForString("BUILDING_GUSS_ZINN"),
				gc.getInfoTypeForString("BUILDING_GUSS_ZINK")
		]
		# Buildings mit 3x3 Radius
		lBuildings3 = [
				gc.getInfoTypeForString("BUILDING_IVORY_MARKET")
		]
		if bLager:
				iRand = 20
		else:
				iRand = 5
		for building in lBuildings + lBuildings2 + lBuildings3:
				if pCity.isHasBuilding(building):
						if CvUtil.myRandom(iRand, "removeNoBonusNoBuilding4") == 1:
								if building in lBuildings3:
										bonus = bonusMissingCity3x3(pCity, building)
								else:
										bonus = bonusMissingCity(pCity, building)
								if bonus is not None:
										pCity.setNumRealBuilding(building, 0)
										# Meldung
										if pPlayer.isHuman():
												# Dies soll doppelte Popups in PB-Spielen vermeiden.
												if iPlayer == gc.getGame().getActivePlayer():
														if building in lBuildings2:
																# In %s1_city wurde durch das Fehlen der Rohstoffe von %s2_resource das Gebäude %s3_building abgebaut
																szText = "TXT_KEY_MESSAGE_CITY_NOBONUSNOBUILDING_5"
														elif building in lBuildings3:
																# In %s1 wurde auf Grund fehlender Güter das Gebäude %s3 abgebaut.
																szText = "TXT_KEY_MESSAGE_CITY_NOBONUSNOBUILDING_4"
														else:
																# In %s1_city wurde durch das Fehlen der Bonusresource %s2_resource das Gebäude %s3_building abgebaut.
																szText = "TXT_KEY_MESSAGE_CITY_NOBONUSNOBUILDING_1"
														szText = CyTranslator().getText(szText, (pCity.getName(), gc.getBonusInfo(bonus).getDescription(), gc.getBuildingInfo(building).getDescription()))
														# Ingame message
														CyInterface().addMessage(iPlayer, True, 10, szText, None, 2, gc.getBuildingInfo(building).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
														# Pop up
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(szText)
														popupInfo.addPopup(iPlayer)
														# Log
														CvUtil.pyPrint(szText)
										return


def bonusMissing(pCity, eBuilding):
		eBonus = gc.getBuildingInfo(eBuilding).getPrereqAndBonus()
		if eBonus != -1:
				if not pCity.hasBonus(eBonus):
						return eBonus

		eRequiredBonus = None
		for iI in range(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
				eBonus = gc.getBuildingInfo(eBuilding).getPrereqOrBonuses(iI)
				if eBonus != -1:
						eRequiredBonus = eBonus
						if pCity.hasBonus(eBonus):
								eRequiredBonus = None
								break
		return eRequiredBonus


def bonusMissingCity(pCity, eBuilding):
		# Erste Abhängigkeit: fixes Bonusgut
		bBonus1Missing = False
		eBonus = gc.getBuildingInfo(eBuilding).getPrereqAndBonus()
		if eBonus != -1:
				bBonus1Missing = True
				for iI in range(gc.getNUM_CITY_PLOTS()):
						loopPlot = pCity.getCityIndexPlot(iI)
						if loopPlot is not None and not loopPlot.isNone():
								if loopPlot.getBonusType(-1) == eBonus:
										iImprovement = loopPlot.getImprovementType()
										if iImprovement != -1 and gc.getImprovementInfo(iImprovement).isImprovementBonusTrade(eBonus):
												bBonus1Missing = False
		if bBonus1Missing:
				return eBonus

		# Zweite Abhängigkeit: bonus1 AND (bonus2 OR bonus3 OR ...)
		bBonus2Missing = False
		lBonus2 = []
		for iI in range(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
				eBonus2 = gc.getBuildingInfo(eBuilding).getPrereqOrBonuses(iI)
				if eBonus2 != -1:
						bBonus2Missing = True
						lBonus2.append(eBonus2)

		if lBonus2:
				# wenn Bonus1 notwendig ist, dann reicht es, wenn die OR-Boni im Handelsnetz sind
				if eBonus != -1:
						for eBonus2 in lBonus2:
								if pCity.hasBonus(eBonus2):
										return None
				else:
						eBonus2 = lBonus2[0]
						for iI in range(gc.getNUM_CITY_PLOTS()):
								loopPlot = pCity.getCityIndexPlot(iI)
								if loopPlot is not None and not loopPlot.isNone():
										eBonusPlot = loopPlot.getBonusType(-1)
										if eBonusPlot in lBonus2:
												eBonus2 = eBonusPlot
												iImprovement = loopPlot.getImprovementType()
												if iImprovement != -1 and gc.getImprovementInfo(iImprovement).isImprovementBonusTrade(eBonusPlot):
														bBonus2Missing = False
		if bBonus2Missing:
				return eBonus2

		return None


def bonusMissingCity3x3(pCity, eBuilding):
		iRange = 3
		iX = pCity.getX()
		iY = pCity.getY()
		# Erste Abhängigkeit: fixes Bonusgut
		bBonus1Missing = False
		eBonus = gc.getBuildingInfo(eBuilding).getPrereqAndBonus()
		if eBonus != -1:
				bBonus1Missing = True
				for i in range(-iRange, iRange+1):
						for j in range(-iRange, iRange+1):
								loopPlot = plotXY(iX, iY, i, j)
								if loopPlot is not None and not loopPlot.isNone():
										if loopPlot.getBonusType(-1) == eBonus:
												iImp = loopPlot.getImprovementType()
												if iImp != -1 and gc.getImprovementInfo(iImp).isImprovementBonusMakesValid(eBonus):
														bBonus1Missing = False
		if bBonus1Missing:
				return eBonus

		# Zweite Abhängigkeit: bonus1 AND (bonus2 OR bonus3 OR ...)
		bBonus2Missing = False
		lBonus2 = []
		for iI in range(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
				eBonus2 = gc.getBuildingInfo(eBuilding).getPrereqOrBonuses(iI)
				if eBonus2 != -1:
						bBonus2Missing = True
						lBonus2.append(eBonus2)

		if lBonus2:
				# wenn Bonus1 notwendig ist, dann reicht es, wenn die OR-Boni im Handelsnetz sind
				if eBonus != -1:
						for eBonus2 in lBonus2:
								if pCity.hasBonus(eBonus2):
										return None
				else:
						eBonus2 = lBonus2[0]
						for i in range(-iRange, iRange+1):
								for j in range(-iRange, iRange+1):
										loopPlot = plotXY(iX, iY, i, j)
										if loopPlot is not None and not loopPlot.isNone():
												eBonusPlot = loopPlot.getBonusType(-1)
												if eBonusPlot in lBonus2:
														iImp = loopPlot.getImprovementType()
														if iImp != -1 and gc.getImprovementInfo(iImp).isImprovementBonusMakesValid(eBonus):
																bBonus2Missing = False
		if bBonus2Missing:
				return eBonus2

		return None


def onEmigrantBuilt(city, unit):
		#iPlayer = city.getOwner()
		#pPlayer = gc.getPlayer(iPlayer)
		pPlot = city.plot()
		iPop = city.getPopulation()
		# Einheit die richtige Kultur geben
		# iPlayerCulture = city.findHighestCulture() Klappt nicht, da Kultur des Stadtplots benoetigt wird
		# Muss selbst bestimmt werden, da plot.findHighestCultureTeam() das Team, aber nicht die Civ zurueckgibt
		iRange = gc.getMAX_PLAYERS()
		iPlayerCulture = -1
		iValueCulture = -1
		for i in range(iRange):
				if pPlot.getCulture(i) > iValueCulture:
						iValueCulture = pPlot.getCulture(i)
						iPlayerCulture = i
		# Sollte auf dem Plot keine Kultur sein (geht eigentlich nicht...), gehoert der Auswanderer zur Kultur des Besitzers
		if iValueCulture < 1:
				iPlayerCulture = unit.getOwner()
		CvUtil.addScriptData(unit, "p", iPlayerCulture)
		# Kultur von dem Stadtplot abziehen
		iCulture = pPlot.getCulture(iPlayerCulture) / iPop
		pPlot.changeCulture(iPlayerCulture, -iCulture, 1)
		# Pop senken, Nahrungslager leeren
		city.setFood(0)

		# Religion vergeben
		PAE_Unit.setUnitReligion(unit)

		if iPop > 1: # and pPlayer.isHuman():
				city.changePopulation(-1)

		doCheckCityState(city)
		# ***TEST***
		# CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Auswanderer gebaut. Pop",iPop)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		# CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",(city.getName(),city.getOwner())), None, 2, None, ColorTypes(10), 0, 0, False, False)


def doEmigrantSpawn(pCity):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		popCity = pCity.getPopulation()
		popNeu = max(1, popCity - 1)
		text = ""
		bRevoltDanger = False
		iChance = 4
		iCityUnhappy = pCity.unhappyLevel(0) - pCity.happyLevel()
		iTaxesLimit = getTaxesLimit(pPlayer)

		# Unhappiness per non state religion (by Dertuek)
		iHappNonState = pPlayer.getNonStateReligionHappiness()
		if iHappNonState < 0:
				iStateReligion = pPlayer.getStateReligion()
				iCurrentTurn = gc.getGame().getElapsedGameTurns()
				for iRel in range(gc.getNumReligionInfos()):
						if pCity.isHasReligion(iRel):
								if gc.getGame().getReligionGameTurnFounded(iRel) == iCurrentTurn and \
												iRel != iStateReligion and \
												pPlayer.hasHolyCity(iRel):
										# The player just has founded the religion and had no time to convert to it
										#  => Don't count the malus just this turn
										iCityUnhappy += iHappNonState

		iCityUnhealthy = pCity.badHealth(False) - pCity.goodHealth()
		if iCityUnhappy > 0 or iCityUnhealthy > 0:
				bRevoltDanger = True
				if iCityUnhealthy > 0:
						text = CyTranslator().getText("TXT_KEY_MESSAGE_CITY_EMIGRANTS_2", (pCity.getName(), popNeu, popCity))
				else:
						text = CyTranslator().getText("TXT_KEY_MESSAGE_CITY_EMIGRANTS", (pCity.getName(), popNeu, popCity))
				if iCityUnhappy < 0:
						iCityUnhappy = 0
				if iCityUnhealthy <= 0:
						iCityUnhealthy = 0
				iChance = (iCityUnhappy + iCityUnhealthy) * 4  # * popCity
		elif pPlayer.getAnarchyTurns() > 0:
				bRevoltDanger = True
				text = CyTranslator().getText("TXT_KEY_MESSAGE_CITY_EMIGRANTS_3", (pCity.getName(), popNeu, popCity))
		elif pPlayer.getStateReligion() != -1 and not pCity.isHasReligion(pPlayer.getStateReligion()):
				bRevoltDanger = True
				text = CyTranslator().getText("TXT_KEY_MESSAGE_CITY_EMIGRANTS_4", (pCity.getName(), popNeu, popCity))
		elif pPlayer.getCommercePercent(0) > iTaxesLimit:
				iChance = int((pPlayer.getCommercePercent(0) - iTaxesLimit) / 5)
				# Pro Happy Citizen 5% Nachlass
				iChance = iChance - pCity.happyLevel() + pCity.unhappyLevel(0)
				bRevoltDanger = iChance > 0
				text = CyTranslator().getText("TXT_KEY_MESSAGE_CITY_EMIGRANTS_5", (pCity.getName(), popNeu, popCity))

		if bRevoltDanger:
				if CvUtil.myRandom(100, "doEmigrantSpawn") < iChance:
						iUnitType = gc.getInfoTypeForString("UNIT_EMIGRANT")
						NewUnit = pPlayer.initUnit(iUnitType, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

						# Einheit die richtige Kultur geben
						iPlayerCulture = pCity.findHighestCulture()
						if iPlayerCulture == -1:
								iPlayerCulture = iPlayer
						CvUtil.addScriptData(NewUnit, "p", iPlayerCulture)
						# Kultur von der Stadt abziehen
						iCulture = pCity.getCulture(iPlayerCulture)
						pCity.changeCulture(iPlayerCulture, -(iCulture/5), 1)

						# Einheit eine Religion geben
						PAE_Unit.setUnitReligion(NewUnit)

						pCity.setPopulation(popNeu)
						doCheckCityState(pCity)

						if pPlayer.isHuman() and text != "":
								CyInterface().addMessage(iPlayer, True, 10, text, "AS2D_REVOLTSTART", InterfaceMessageTypes.MESSAGE_TYPE_INFO,
																				 "Art/Interface/Buttons/Techs/button_brandschatzen.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
						else:
								PAE_Sklaven.doAIReleaseSlaves(pCity)
				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Emigrant verlaesst Stadt (Zeile 3624)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)


def doLeprosy(pCity):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		bDecline = False
		if pCity.goodHealth() < pCity.badHealth(False):
				iChance = pCity.badHealth(False) - pCity.goodHealth()
				# PAE V: less chance for AI
				if not pPlayer.isHuman():
						iChance = iChance / 3

				if CvUtil.myRandom(100, "doLeprosy") < iChance:
						iOldPop = pCity.getPopulation()

						# Leprakolonie nimmt nur 1 POP
						iBuilding = gc.getInfoTypeForString('BUILDING_LEPRAKOLONIE')
						if pCity.isHasBuilding(iBuilding):
								iNewPop = max(1, iOldPop - 1)
								if pPlayer.isHuman():
										CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_LEBRA_1", (pCity.getName(), )), "AS2D_PLAGUE", 2, None, ColorTypes(13), pCity.getX(),  pCity.getY(), True, True)
						else:
								iRandPop = CvUtil.myRandom(int(round(pCity.getPopulation() / 2)), "doLeprosy2") + 1
								iNewPop = max(1, iOldPop - iRandPop)
								# City Revolt
								# pCity.setOccupationTimer(1)
								if pPlayer.isHuman():
										CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_LEBRA_2",
																																																(pCity.getName(), iNewPop, iOldPop)), "AS2D_PLAGUE", 2, None, ColorTypes(13), pCity.getX(),  pCity.getY(), True, True)

						pCity.setPopulation(iNewPop)
						bDecline = True

						if not pPlayer.isHuman():
								PAE_Sklaven.doAIReleaseSlaves(pCity)

						# ***TEST***
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Lepra (Zeile 3660)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		return bDecline


def doSpawnPest(pCity):
		if pCity is None or pCity.isNone():
				return False

		iChance = pCity.badHealth(False) - pCity.goodHealth()
		if iChance > 0:
				iPlayer = pCity.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				# PAE V: less chance for AI
				if not pPlayer.isHuman():
						iChance = iChance / 3

				if CvUtil.myRandom(100, "doSpawnPest") < iChance:
						iThisTeam = pPlayer.getTeam()
						pTeam = gc.getTeam(iThisTeam)

						#iMedicine1 = gc.getInfoTypeForString("TECH_MEDICINE1")
						#iMedicine2 = gc.getInfoTypeForString("TECH_MEDICINE2")
						#iMedicine3 = gc.getInfoTypeForString("TECH_MEDICINE3")
						#iMedicine4 = gc.getInfoTypeForString("TECH_HEILKUNDE")

						# City Revolt
						#if team.isHasTech(iMedicine1) or  team.isHasTech(iMedicine2) or  team.isHasTech(iMedicine3) or  team.isHasTech(iMedicine4): pCity.setOccupationTimer(2)
						# else: pCity.setOccupationTimer(3)
						# pCity.setOccupationTimer(1)

						# message for all
						iRange = gc.getMAX_PLAYERS()
						for iPlayer2 in range(iRange):
								pSecondPlayer = gc.getPlayer(iPlayer2)
								if pSecondPlayer.isHuman():
										iSecTeam = pSecondPlayer.getTeam()
										if pTeam.isHasMet(iSecTeam):
												CyInterface().addMessage(iPlayer2, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_GLOBAL", (pCity.getName(), 0)),
																								 "AS2D_PLAGUE", 2, 'Art/Interface/Buttons/Actions/button_skull.dds', ColorTypes(13), pCity.getX(),  pCity.getY(), True, True)

						if pPlayer.isHuman():
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_GLOBAL", (pCity.getName(), 0)),
																				 "AS2D_PLAGUE", 2, 'Art/Interface/Buttons/Actions/button_skull.dds', ColorTypes(13), pCity.getX(),  pCity.getY(), True, True)
						# end message

						# Plague building gets added into city
						iBuildingPlague = gc.getInfoTypeForString("BUILDING_PLAGUE")
						pCity.setNumRealBuilding(iBuildingPlague, 1)
						return True

						# ***TEST***
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Pest (Zeile 3701)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		return False


def doPlagueEffects(pCity):
		iBuildingPlague = gc.getInfoTypeForString('BUILDING_PLAGUE')
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		#iCulture = pCity.getBuildingCommerceByBuilding(2, iBuildingPlague)
		iCulture = pCity.getCulture(iPlayer)
		iX = pCity.getX()
		iY = pCity.getY()
		# Calculation var
		iHappiness = pCity.getBuildingHappiness(iBuildingPlague)

		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Culture",iCulture)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Happiness",iHappiness)), None, 2, None, ColorTypes(10), 0, 0, False, False)

		# Plots rundherum mit SeuchenFeature belasten
		if iHappiness == -5:
				feat_seuche = gc.getInfoTypeForString('FEATURE_SEUCHE')
				for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
						loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
						if loopPlot is not None and not loopPlot.isNone():
								if not loopPlot.isWater() and not loopPlot.isPeak() and loopPlot.getFeatureType() == -1:
										loopPlot.setFeatureType(feat_seuche, 0)

		# Downgrade Improvements
		if iHappiness == -4 or iHappiness == -2:
				for iI in range(gc.getNUM_CITY_PLOTS()):
						loopPlot = pCity.getCityIndexPlot(iI)
						if loopPlot is not None and not loopPlot.isNone():
								improv1 = gc.getInfoTypeForString('IMPROVEMENT_COTTAGE')
								improv2 = gc.getInfoTypeForString('IMPROVEMENT_HAMLET')
								improv3 = gc.getInfoTypeForString('IMPROVEMENT_VILLAGE')
								improv4 = gc.getInfoTypeForString('IMPROVEMENT_TOWN')
								iImprovement = loopPlot.getImprovementType()
								# 50% chance of downgrading
								iRand = CvUtil.myRandom(2, "doPlagueEffects")
								if iRand == 1:
										if iImprovement == improv2:
												loopPlot.setImprovementType(improv1)
										elif iImprovement == improv3:
												loopPlot.setImprovementType(improv2)
										elif iImprovement == improv4:
												loopPlot.setImprovementType(improv3)

		# decline City pop
		# iThisTeam = pPlayer.getTeam()
		# team = gc.getTeam(iThisTeam)

		#iMedicine1 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_MEDICINE1')
		#iMedicine2 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_MEDICINE2')
		#iMedicine3 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_MEDICINE3')
		#iMedicine4 = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_HEILKUNDE')

		# Change City Pop
		iOldPop = pCity.getPopulation()
		# there is no medicine against plague :)
		# if team.isHasTech(iMedicine1) or  team.isHasTech(iMedicine2) or  team.isHasTech(iMedicine3) or  team.isHasTech(iMedicine4):
		# bis zu -2 pro turn
		iPopChange = 1 + CvUtil.myRandom(2, "doPlagueEffects2")

		# Slaves and Glads
		eSpecialistGlad = gc.getInfoTypeForString("SPECIALIST_GLADIATOR")
		eSpecialistHouse = gc.getInfoTypeForString("SPECIALIST_SLAVE")
		eSpecialistFood = gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD")
		eSpecialistProd = gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD")

		iCityGlads = pCity.getFreeSpecialistCount(eSpecialistGlad)
		iCitySlavesHaus = pCity.getFreeSpecialistCount(eSpecialistHouse)
		iCitySlavesFood = pCity.getFreeSpecialistCount(eSpecialistFood)
		iCitySlavesProd = pCity.getFreeSpecialistCount(eSpecialistProd)

		# Pop
		iNewPop = max(1, iOldPop - iPopChange)

		# Message new Pop
		if pPlayer.isHuman():
				CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST", (pCity.getName(), iNewPop, iOldPop)), None, 2, None, ColorTypes(13), 0, 0, False, False)

		pCity.setPopulation(iNewPop)
		# end decline city pop

		# Sklaven sterben
		# Prio: Haus (min 1 bleibt), Food, Glads, Prod
		iSlaves = iCityGlads + iCitySlavesHaus + iCitySlavesFood + iCitySlavesProd
		while iSlaves > 0 and iPopChange > 0:
				if iCitySlavesHaus > 1:
						pCity.changeFreeSpecialistCount(eSpecialistHouse, -1)
						iCitySlavesHaus -= 1
						if pPlayer.isHuman():
								CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_HAUS", (pCity.getName(),)), None, 2, None, ColorTypes(7), 0, 0, False, False)
				elif iCitySlavesFood > 0:
						pCity.changeFreeSpecialistCount(eSpecialistFood, -1)
						iCitySlavesFood -= 1
						if pPlayer.isHuman():
								CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_FOOD", (pCity.getName(),)), None, 2, None, ColorTypes(7), 0, 0, False, False)
				elif iCityGlads > 0:
						pCity.changeFreeSpecialistCount(eSpecialistGlad, -1)
						iCityGlads -= 1
						if pPlayer.isHuman():
								CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_GLAD", (pCity.getName(),)), None, 2, None, ColorTypes(7), 0, 0, False, False)
				elif iCitySlavesProd > 0:
						pCity.changeFreeSpecialistCount(eSpecialistProd, -1)
						iCitySlavesProd -= 1
						if pPlayer.isHuman():
								CyInterface().addMessage(pCity.getOwner(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_PROD", (pCity.getName(),)), None, 2, None, ColorTypes(7), 0, 0, False, False)
				iSlaves -= 1
				iPopChange -= 1

		# Hurt and kill units
		lMessageOwners = []
		for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
				loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
				if loopPlot is not None and not loopPlot.isNone():
						iRange = loopPlot.getNumUnits()
						for iUnit in range(iRange):
								iRand = CvUtil.myRandom(30, "doPlagueEffects3") + 15
								pLoopUnit = loopPlot.getUnit(iUnit)
								if pLoopUnit is not None:
										if pLoopUnit.getDamage() + iRand < 100:
												pLoopUnit.changeDamage(iRand, False)
										sOwner = pLoopUnit.getOwner()
										psOwner = gc.getPlayer(sOwner)
										if pLoopUnit.getDamage() > 95:
												if psOwner is not None and psOwner.isHuman():
														CyInterface().addMessage(sOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_KILL_UNIT", (pLoopUnit.getName(), pCity.getName())),
																										 None, 2, 'Art/Interface/Buttons/Actions/button_skull.dds', ColorTypes(12), loopPlot.getX(), loopPlot.getY(), True, True)
												# pLoopUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
												pLoopUnit.kill(True, -1)  # RAMK_CTD
										if psOwner is not None and psOwner.isHuman():
												if sOwner not in lMessageOwners:
														lMessageOwners.append(sOwner)
														CyInterface().addMessage(sOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_2", (pCity.getName(), 0)),
																										 None, 2, 'Art/Interface/Buttons/Actions/button_skull.dds', ColorTypes(12), iX, iY, True, True)

		# Change City Culture
		iCultureNew = max(0, iCulture - 50)
		pCity.setCulture(iPlayer, iCultureNew, 1)

		# Calculation
		if iHappiness >= -1:
				# Building erneut initialisieren. CIV BUG.
				pCity.setBuildingHappyChange(gc.getBuildingInfo(iBuildingPlague).getBuildingClassType(), 0)
				# Building entfernen
				pCity.setNumRealBuilding(iBuildingPlague, 0)
				# Message
				if pPlayer.isHuman():
						CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_PEST_DONE", (pCity.getName(), iNewPop, iOldPop)),
																		 "AS2D_WELOVEKING", 2, 'Art/Interface/Buttons/Actions/button_skull.dds', ColorTypes(8), pCity.getX(),  pCity.getY(), True, True)

		else:
				CvUtil.changeBuildingHappyChange(pCity, iBuildingPlague, +1)
				# # zum Gebaeude +1 Happiness addieren (-5,-4,..) - funkt leider nicht mit nur einer Zeile?!- Civ BUG?
				# if iHappiness == -5: pCity.setBuildingHappyChange (gc.getBuildingInfo(iBuildingPlague).getBuildingClassType(), +1)
				# if iHappiness == -4: pCity.setBuildingHappyChange (gc.getBuildingInfo(iBuildingPlague).getBuildingClassType(), +2)
				# if iHappiness == -3: pCity.setBuildingHappyChange (gc.getBuildingInfo(iBuildingPlague).getBuildingClassType(), +3)
				# if iHappiness == -2: pCity.setBuildingHappyChange (gc.getBuildingInfo(iBuildingPlague).getBuildingClassType(), +4)
				# if iHappiness == -1: pCity.setBuildingHappyChange (gc.getBuildingInfo(iBuildingPlague).getBuildingClassType(), +5)
				# if iHappiness < -5:
				# pCity.setBuildingHappyChange (gc.getBuildingInfo(iBuildingPlague).getBuildingClassType(), 0)
				# pCity.setNumRealBuilding(iBuildingPlague,0)
				# pCity.setNumRealBuilding(iBuildingPlague,1)

		# spread plague 10%
		if CvUtil.myRandom(10, "spread Plague") == 1:
				doSpreadPlague(pCity)


def doRevoltShrink(pCity):
		if pCity and not pCity.isNone():
				if pCity.getPopulation() > 1:
						if CvUtil.myRandom(4, "doRevoltShrink") == 1:
								pCity.changePopulation(-1)
								iPlayer = pCity.getOwner()
								pPlayer = gc.getPlayer(iPlayer)
								if pPlayer.isHuman():
										CyInterface().addMessage(iPlayer, False, 25, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_REVOLT_SHRINK", (pCity.getName(),)), "AS2D_REVOLTSTART",
																						 InterfaceMessageTypes.MESSAGE_TYPE_INFO, "Art/Interface/Buttons/Techs/button_brandschatzen.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
								# ***TEST***
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Stadtpop sinkt wegen Revolte (Zeile 4126)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
								return True
		return False


def doPartisans(pCity, iPreviousOwner):
		# Seek Plots
		rebelPlotArray = []
		PartisanPlot2 = []
		iX = pCity.getX()
		iY = pCity.getY()
		for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
				loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
				if loopPlot is not None and not loopPlot.isNone() and not loopPlot.isUnit():
						if not loopPlot.isWater() and not loopPlot.isImpassable() and not loopPlot.isCity():
								if loopPlot.isHills():
										rebelPlotArray.append(loopPlot)
								else:
										PartisanPlot2.append(loopPlot)
		if not rebelPlotArray:
				rebelPlotArray = PartisanPlot2

		# Set Partisans
		if rebelPlotArray:
				pPreviousOwner = gc.getPlayer(iPreviousOwner)
				iThisTeam = pPreviousOwner.getTeam()
				team = gc.getTeam(iThisTeam)
				if team.isHasTech(gc.getInfoTypeForString("TECH_BEWAFFNUNG4")) and pCity.canTrain(gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), 0, 0):
						iUnitType = gc.getInfoTypeForString("UNIT_SCHILDTRAEGER")
				elif team.isHasTech(gc.getInfoTypeForString("TECH_BEWAFFNUNG2")) and pCity.canTrain(gc.getInfoTypeForString("UNIT_AXEMAN"), 0, 0):
						iUnitType = gc.getInfoTypeForString("UNIT_AXEMAN")
				elif team.isHasTech(gc.getInfoTypeForString("TECH_BEWAFFNUNG")):
						iUnitType = gc.getInfoTypeForString("UNIT_AXEWARRIOR")
				else:
						iUnitType = gc.getInfoTypeForString("UNIT_WARRIOR")

				# Number of Partisans
				iAnzahl = CvUtil.myRandom(pCity.getPopulation()/2, "doPartisans") + 1
				for _ in range(iAnzahl):
						pPlot = rebelPlotArray[CvUtil.myRandom(len(rebelPlotArray), "doPartisansPlot")]
						pUnit = pPreviousOwner.initUnit(iUnitType, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						iDamage = CvUtil.myRandom(50, "doPartisansDamage")
						pUnit.setDamage(iDamage, iPreviousOwner)

				# PAE V: Reservisten
				iAnzahl = pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_RESERVIST"))
				pCity.setFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_RESERVIST"), 0)
				for _ in range(iAnzahl):
						pPlot = rebelPlotArray[CvUtil.myRandom(len(rebelPlotArray), "doPartisansReservists")]
						pUnit = pPreviousOwner.initUnit(iUnitType, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						iDamage = CvUtil.myRandom(25, "doPartisansReservistsDamage")
						pUnit.setDamage(iDamage, iPreviousOwner)
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT2"), True)
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT3"), True)
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT4"), True)

				#iOwner = pCity.findHighestCulture()
#        if iPreviousOwner != -1 and iNewOwner != -1:
#          if not pPreviousOwner.isBarbarian() and pPreviousOwner.getNumCities() > 0:
#            if gc.getTeam(pPreviousOwner.getTeam()).isAtWar(gc.getPlayer(iNewOwner).getTeam()):
#              if gc.getNumEventTriggerInfos() > 0: # prevents mods that don't have events from getting an error
#                iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_PARTISANS')
#                if iEvent != -1 and gc.getGame().isEventActive(iEvent) and pPreviousOwner.getEventTriggerWeight(iEvent) >= 0:
#                  triggerData = pPreviousOwner.initTriggeredData(iEvent, True, -1, pCity.getX(), pCity.getY(), iPreviousOwner, pCity.getID(), -1, -1, -1, -1)
# --- Ende Partisans -------------------------


def doCaptureSlaves(pCity, iNewOwner, iPreviousOwner):
		pPlayer = gc.getPlayer(iNewOwner)
		iTeam = pPlayer.getTeam()
		pTeam = gc.getTeam(iTeam)

		iTechEnslavement = gc.getInfoTypeForString("TECH_ENSLAVEMENT")
		if pTeam.isHasTech(iTechEnslavement):
				iSlaves = CvUtil.myRandom(pCity.getPopulation() - 1, "doCaptureSlaves") + 1

				# Trait Aggressive: Popverlust bleibt gleich / loss of pop remains the same
				iSetPop = max(1, pCity.getPopulation() - iSlaves)
				pCity.setPopulation(iSetPop)

				# Trait Aggressive: Slaves * 2
				if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_AGGRESSIVE")) or pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_EROBERER")):
						iSlaves *= 2

				iUnit = gc.getInfoTypeForString("UNIT_SLAVE")
				pPlot = pCity.plot()
				for _ in range(iSlaves):
						CvUtil.spawnUnit(iUnit, pPlot, pPlayer)

				if pPlayer.isHuman():
						if iSlaves == 1:
								CyInterface().addMessage(iNewOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_SLAVES_1", (0, 0)), None, 2, None, ColorTypes(8), 0, 0, False, False)
						else:
								CyInterface().addMessage(iNewOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_SLAVES_2", (iSlaves, 0)), None, 2, None, ColorTypes(8), 0, 0, False, False)
				if gc.getPlayer(iPreviousOwner).isHuman():
						if iSlaves == 1:
								CyInterface().addMessage(iPreviousOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_SLAVES_3", (pCity.getName(), 0)), None, 2, None, ColorTypes(7), 0, 0, False, False)
						else:
								CyInterface().addMessage(iPreviousOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_SLAVES_4", (pCity.getName(), iSlaves)), None, 2, None, ColorTypes(7), 0, 0, False, False)

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Stadt erobert (Zeile 3182)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

# Deportation von Stadteinwohnern (historisch: Assyrische Massendeportationen)


def doDeportation(pCity, iNewOwner, iPreviousOwner):
		pPlayer = gc.getPlayer(iNewOwner)
		# Einheit erstellen
		NewUnit = CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_EMIGRANT"), pCity.plot(), pPlayer)

		# Kultur vergeben
		iCulture = pCity.findHighestCulture()
		if iCulture == -1:
				iCulture = iPreviousOwner
		CvUtil.addScriptData(NewUnit, "p", iCulture)

		# Einheit eine Religion geben
		PAE_Unit.setUnitReligion(NewUnit)

		# Versorger erstellen 33.3%
		if CvUtil.myRandom(10, "PAE_City:doDeportation Create Suppy Wagon") < 3:
				NewUnit = CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"), pCity.plot(), pPlayer)
				PAE_Unit.initSupply(NewUnit)


def doSettledSlavesAndReservists(pCity):
		bRevolt = False
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		pTeam = gc.getTeam(pPlayer.getTeam())
		pCityPlot = pCity.plot()
		iCityPop = pCity.getPopulation()

		eSpecialistGlad = gc.getInfoTypeForString("SPECIALIST_GLADIATOR")
		eSpecialistHouse = gc.getInfoTypeForString("SPECIALIST_SLAVE")
		eSpecialistFood = gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD")
		eSpecialistProd = gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD")

		eSpecialistReserve = gc.getInfoTypeForString("SPECIALIST_RESERVIST")
		#eSpecialistFreeCitizen = gc.getInfoTypeForString("SPECIALIST_CITIZEN2")

		iCityGlads = pCity.getFreeSpecialistCount(eSpecialistGlad)
		iCitySlavesHaus = pCity.getFreeSpecialistCount(eSpecialistHouse)
		iCitySlavesFood = pCity.getFreeSpecialistCount(eSpecialistFood)
		iCitySlavesProd = pCity.getFreeSpecialistCount(eSpecialistProd)
		iCitySlaves = iCitySlavesHaus + iCitySlavesFood + iCitySlavesProd
		iCitySlaves2 = 0  # Unsettled Slaves in city

		iCityReservists = pCity.getFreeSpecialistCount(eSpecialistReserve)

		# Wenn es Sklaven gibt = verschiedene Sterbensarten
		if iCitySlaves > 0 or iCityReservists > 0:
				# Sklaventyp aussuchen, aber es soll max. immer nur 1 Typ pro Stadt draufgehn
				iTyp = -1

				# Haussklave 4%
				if iCitySlavesHaus > 0:
						iChance = 4
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_PATRONAT")):
								iChance = 2
						if CvUtil.myRandom(100, "iCitySlavesHaus") < iChance:
								iTyp = 2
				# Feldsklave 6%
				if iCitySlavesFood > 0 and iTyp == -1:
						iChance = 6
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_EISENPFLUG")):
								iChance = 3
						if CvUtil.myRandom(100, "iCitySlavesFood") < iChance:
								iTyp = 0
				# Bergwerkssklave 8%
				if iCitySlavesProd > 0 and iTyp == -1:
						iChance = 8
						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_MECHANIK")):
								iChance = 4
						if CvUtil.myRandom(100, "iCitySlavesProd") < iChance:
								iTyp = 1
				# Reservist 2%
				if iCityReservists > 0 and iTyp == -1:
						if CvUtil.myRandom(100, "iCityReservists") < 2:
								iTyp = 3

				# Reservisten
				if iTyp == 3:
						pCity.changeFreeSpecialistCount(eSpecialistReserve, -1)
						if pPlayer.isHuman():
								iRand = 1 + CvUtil.myRandom(9, "Reservisten")
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_DYING_RESERVIST_"+str(iRand), (pCity.getName(), "")), None, 2,
																				 ",Art/Interface/MainScreen/CityScreen/Great_Engineer.dds,Art/Interface/Buttons/Warlords_Atlas_2.dds,7,6", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
				# Sklavensterben
				elif iTyp != -1:
						# PAE V: stehende Sklaven werden zugewiesen
						bErsatz = False
						iRangePlotUnits = pCityPlot.getNumUnits()
						for iUnit in range(iRangePlotUnits):
								pLoopUnit = pCityPlot.getUnit(iUnit)
								if pLoopUnit.getOwner() == iPlayer and pLoopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SLAVE"):
										# pLoopUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
										pLoopUnit.kill(True, -1)  # RAMK_CTD
										bErsatz = True
										break

						# Feldsklaven
						if iTyp == 0:
								if not bErsatz:
										pCity.changeFreeSpecialistCount(eSpecialistFood, -1)
										iCitySlavesFood -= 1
								if pPlayer.isHuman():
										iRand = 1 + CvUtil.myRandom(16, "Feldsklaven")
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_SLAVES_FELD_"+str(iRand), (pCity.getName(), "")),
																						 None, 2, "Art/Interface/Buttons/Units/button_slave.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

						# Bergwerkssklaven
						elif iTyp == 1:
								if not bErsatz:
										pCity.changeFreeSpecialistCount(eSpecialistProd, -1)
										iCitySlavesProd -= 1
								if pPlayer.isHuman():
										iRand = 1 + CvUtil.myRandom(20, "Bergwerkssklaven")
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_SLAVES_MINE_"+str(iRand), (pCity.getName(), "")),
																						 None, 2, "Art/Interface/Buttons/Units/button_slave.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

						# Haussklaven
						elif iTyp == 2:
								# A) Standard Sklavensterben
								# B) Tech Patronat: Hausklaven werden freie Buerger
								iRand = 0
								# if pTeam.isHasTech(gc.getInfoTypeForString("TECH_PATRONAT")):
								#    iRand = 2

								# Dying
								if CvUtil.myRandom(iRand, "Haussklaven1") == 0:
										if not bErsatz:
												pCity.changeFreeSpecialistCount(eSpecialistHouse, -1)
												iCitySlavesHaus -= 1
										if pPlayer.isHuman():
												iRand = 1 + CvUtil.myRandom(14, "Haussklaven2")
												CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_SLAVES_HAUS_"+str(iRand), (pCity.getName(), "")),
																								 None, 2, "Art/Interface/Buttons/Units/button_slave.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
								# Patronat
								# else:
								#    bErsatz = False
								#    pCity.changeFreeSpecialistCount(eSpecialistHouse, -1)
								#    iCitySlavesHaus -= 1
								#    pCity.changeFreeSpecialistCount(eSpecialistFreeCitizen, +1)  # SPECIALIST_CITIZEN2
								#    if pPlayer.isHuman():
								#        iRand = 1 + CvUtil.myRandom(2, "Haussklaven3")
								#        CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_SLAVES_PATRONAT_"+str(iRand), (pCity.getName(), "")), None, 2, "Art/Interface/Buttons/Units/button_slave.dds", ColorTypes(8), pCity.getX(), pCity.getY(), True, True)

						if bErsatz:
								if pPlayer.isHuman():
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_SLAVES_ERSATZ", ("",)), None, 2,
																						 "Art/Interface/Buttons/Units/button_slave.dds", ColorTypes(8), pCity.getX(), pCity.getY(), True, True)
						else:
								# Gesamtsumme aendern
								iCitySlaves -= 1

		# Wenns mehr Sklaven als Einwohner gibt = Revolte
		if iCitySlaves + iCityGlads > iCityPop:
				# Calc factor
				iChance = (iCitySlaves + iCityGlads - iCityPop) * 10

				# rebel bonus when unhappy
				if pCity.happyLevel() < pCity.unhappyLevel(0):
						iChance += 25
				# Units that prevent a revolt
				iPromoHero = gc.getInfoTypeForString('PROMOTION_HERO')
				iRangePlotUnits = pCityPlot.getNumUnits()
				for iUnit in range(iRangePlotUnits):
						pLoopUnit = pCityPlot.getUnit(iUnit)
						if pLoopUnit.isHasPromotion(iPromoHero):
								iChance -= 25
						elif pLoopUnit.isMilitaryHappiness():
								iChance -= 2
						elif pLoopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SLAVE"):
								iCitySlaves2 += 1
								iChance += 2
				# Buildings that prevent a revolt
				iBuilding = gc.getInfoTypeForString('BUILDING_AMPHITHEATER')
				if pCity.isHasBuilding(iBuilding):
						iChance -= 5
				iBuilding = gc.getInfoTypeForString('BUILDING_CIRCUS')
				if pCity.isHasBuilding(iBuilding):
						iChance -= 5
				# Civics that promotes/prevents a revolt
				if pPlayer.isCivic(14):
						iChance += 5
				if pPlayer.isCivic(15):
						iChance += 5
				if pPlayer.isCivic(16) or pPlayer.isCivic(17):
						iChance -= 5

				if iChance > 0:
						iRand = CvUtil.myRandom(100, "SKLAVENAUFSTAND")
						# Lets rebell
						if iRand < iChance:
								if iPlayer == gc.getGame().getActivePlayer():
										CyAudioGame().Play2DSound('AS2D_REVOLTSTART')

								# Einen guenstigen Plot auswaehlen
								rebelPlotArray = []
								rebelPlotArrayB = []
								for i in range(3):
										for j in range(3):
												loopPlot = gc.getMap().plot(pCity.getX() + i - 1, pCity.getY() + j - 1)
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
										bRevolt = True
										# pruefen ob es einen Vorbesitzer fuer diese Stadt gibt
										iPreviousOwner = pCity.findHighestCulture()
										barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
										if iPlayer != iPreviousOwner and iPreviousOwner != -1:
												if gc.getTeam(pPlayer.getTeam()).isAtWar(gc.getPlayer(iPreviousOwner).getTeam()):
														barbPlayer = gc.getPlayer(iPreviousOwner)

										# Unsettled slaves
										iNumRebels2 = 0
										if iCitySlaves2 > 0:
												iNumRebels2 = CvUtil.myRandom(iCitySlaves2 - 1, "Unsettled slaves2") + 1
												iDone = 0
												iRangePlotUnits = pCityPlot.getNumUnits()
												for iUnit in range(iRangePlotUnits):
														pLoopUnit = pCityPlot.getUnit(iUnit)
														if iDone < iNumRebels2 and pLoopUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SLAVE"):
																# pLoopUnit.doCommand(CommandTypes.COMMAND_DELETE, -1, -1)
																pLoopUnit.kill(True, -1)  # RAMK_CTD
																iDone += 1

										iNumRebels = 0
										# SLAVE REVOLT (SKLAVENAUFSTAND)
										if iCitySlaves > iCityGlads and iCitySlaves > 0:
												iUnitType = PAE_Barbaren.getPartisan(pPlayer)

												# Settled slaves
												iNumRebels = CvUtil.myRandom(iCitySlaves - 1, "Settled slaves") + 1
												iNumRebTmp = iNumRebels
												# Zuerst Feldsklaven
												if iNumRebTmp >= iCitySlavesFood:
														pCity.setFreeSpecialistCount(eSpecialistFood, 0)
														iNumRebTmp -= iCitySlavesFood
												else:
														pCity.changeFreeSpecialistCount(eSpecialistFood, iNumRebTmp * (-1))
														iNumRebTmp = 0
												# Dann Bergwerkssklaven
												if iNumRebTmp >= iCitySlavesProd and iNumRebTmp > 0:
														pCity.setFreeSpecialistCount(eSpecialistProd, 0)
														iNumRebTmp -= iCitySlavesProd
												else:
														pCity.changeFreeSpecialistCount(eSpecialistProd, iNumRebTmp * (-1))
														iNumRebTmp = 0
												# Der Rest Haussklaven
												if iNumRebTmp >= iCitySlavesHaus and iNumRebTmp > 0:
														pCity.setFreeSpecialistCount(eSpecialistHouse, 0)
														# iNumRebTmp -= iCitySlavesHaus
												else:
														pCity.changeFreeSpecialistCount(eSpecialistHouse, iNumRebTmp * (-1))
														# iNumRebTmp = 0

										# GLADIATOR REVOLT (GLADIATORENAUFSTAND)
										elif iCityGlads > 0:
												iUnitType = gc.getInfoTypeForString("UNIT_GLADIATOR")
												# Settled gladiators
												iNumRebels = CvUtil.myRandom(iCityGlads - 1, "Settled gladiators")+1
												pCity.changeFreeSpecialistCount(eSpecialistGlad, iNumRebels * (-1))

										iNumRebels += iNumRebels2

										if iNumRebels:
												for _ in range(iNumRebels):
														iPlot = CvUtil.myRandom(len(rebelPlotArray), "rebelPlotArray")
														NewUnit = barbPlayer.initUnit(iUnitType, rebelPlotArray[iPlot].getX(), rebelPlotArray[iPlot].getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
														NewUnit.setImmobileTimer(1)
												# ***TEST***
												#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Rebell erstellt",iNumRebels)), None, 2, None, ColorTypes(10), 0, 0, False, False)

												# City Defender damage
												doCityRevolt(pCity, iNumRebels + 1)

												iRangeMaxPlayers = gc.getMAX_PLAYERS()
												for iLoopPlayer in range(iRangeMaxPlayers):
														pLoopPlayer = gc.getPlayer(iLoopPlayer)
														iLoopTeam = pLoopPlayer.getTeam()
														pLoopTeam = gc.getTeam(iLoopTeam)
														if pLoopTeam.isHasMet(pPlayer.getTeam()) and pLoopPlayer.isHuman():
																if iLoopPlayer == iPlayer:
																		iColor = 7
																else:
																		iColor = 10
																if iNumRebels == 1:
																		CyInterface().addMessage(iLoopPlayer, True, 8, CyTranslator().getText("TXT_KEY_REBELL_REVOLT_ONE", (pCity.getName(), pPlayer.getCivilizationAdjective(1), iNumRebels)),
																														 None, InterfaceMessageTypes.MESSAGE_TYPE_INFO, "Art/Interface/Buttons/Units/button_slave.dds", ColorTypes(iColor), pCity.getX(), pCity.getY(), True, True)
																else:
																		CyInterface().addMessage(iLoopPlayer, True, 8, CyTranslator().getText("TXT_KEY_REBELL_REVOLT", (pCity.getName(), pPlayer.getCivilizationAdjective(1), iNumRebels)),
																														 None, InterfaceMessageTypes.MESSAGE_TYPE_INFO, "Art/Interface/Buttons/Units/button_slave.dds", ColorTypes(iColor), pCity.getX(), pCity.getY(), True, True)

						# KI soll Stadtsklaven freistellen 1:4
						elif not pPlayer.isHuman():
								if CvUtil.myRandom(4, "Stadtsklaven freistellen") == 1:
										PAE_Sklaven.doAIReleaseSlaves(pCity)

		# Sklaven oder Gladiatoren: sobald das Christentum entdeckt wurde -> 2%
		iReligion = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
		if not bRevolt and PAE_Christen.canSpreadChristentumOverall():
				if pPlayer.getStateReligion() != iReligion:

						if pTeam.isHasTech(gc.getInfoTypeForString("TECH_HERESY")): 
							iChance = 1
						else: 
							iChance = 2
		
						iRand = CvUtil.myRandom(75, "ChristentumSklavenRevolte")
						if iRand < iChance:
								# City Defender damage
								doCityRevolt(pCity, 2)
								bRevolt = True
								# Message to players
								iRangeMaxPlayers = gc.getMAX_PLAYERS()
								for iLoopPlayer in range(iRangeMaxPlayers):
										pLoopPlayer = gc.getPlayer(iLoopPlayer)
										iLoopTeam = pLoopPlayer.getTeam()
										pLoopTeam = gc.getTeam(iLoopTeam)
										if pLoopTeam.isHasMet(pPlayer.getTeam()) and pLoopPlayer.isHuman():
												if iLoopPlayer == iPlayer:
														iColor = 7
												else:
														iColor = 10
												CyInterface().addMessage(iLoopPlayer, True, 8, CyTranslator().getText("TXT_KEY_REVOLT_CHRISTIANS", (pCity.getName(), pPlayer.getCivilizationAdjective(1))), None,
																								 InterfaceMessageTypes.MESSAGE_TYPE_INFO, "Art/Interface/Buttons/Actions/button_kreuz.dds", ColorTypes(iColor), pCity.getX(), pCity.getY(), True, True)

								# 1 settled Slave (Slave or gladiator) gets killed
								if iCitySlaves > 0 or iCityGlads > 0:
										bChristSlaves = False
										if iCitySlaves > 0 and iCityGlads > 0:
												iRand = CvUtil.myRandom(2, "1 settled Slave (Slave or gladiator) gets killed")
												bChristSlaves = (iRand == 0)  # 0 = Slaves, 1 = Glads
										else:
												bChristSlaves = (iCitySlaves > 0)  # either slaves or glads

										if bChristSlaves:
												if iCitySlavesHaus > 0 and iCitySlavesFood > 0 and iCitySlavesProd > 0:
														iRand = CvUtil.myRandom(3, "bChristSlaves")
														if iRand == 1:
																pCity.changeFreeSpecialistCount(eSpecialistFood, -1)
														elif iRand == 2:
																pCity.changeFreeSpecialistCount(eSpecialistProd, -1)
														else:
																pCity.changeFreeSpecialistCount(eSpecialistHouse, -1)
												elif iCitySlavesHaus > 0 and iCitySlavesFood > 0:
														iRand = CvUtil.myRandom(2, "bChristSlaves2")
														if iRand == 1:
																pCity.changeFreeSpecialistCount(eSpecialistFood, -1)
														else:
																pCity.changeFreeSpecialistCount(eSpecialistHouse, -1)
												elif iCitySlavesHaus > 0 and iCitySlavesProd > 0:
														iRand = CvUtil.myRandom(2, "bChristSlaves3")
														if iRand == 1:
																pCity.changeFreeSpecialistCount(eSpecialistProd, -1)
														else:
																pCity.changeFreeSpecialistCount(eSpecialistHouse, -1)
												elif iCitySlavesFood > 0 and iCitySlavesProd > 0:
														iRand = CvUtil.myRandom(2, "bChristSlaves4")
														if iRand == 1:
																pCity.changeFreeSpecialistCount(eSpecialistFood, -1)
														else:
																pCity.changeFreeSpecialistCount(eSpecialistProd, -1)
												elif iCitySlavesFood > 0:
														pCity.changeFreeSpecialistCount(eSpecialistFood, -1)
												elif iCitySlavesProd > 0:
														pCity.changeFreeSpecialistCount(eSpecialistProd, -1)
												else:
														pCity.changeFreeSpecialistCount(eSpecialistHouse, -1)

												if pPlayer.isHuman():
														CyInterface().addMessage(iPlayer, True, 8, CyTranslator().getText("TXT_KEY_REVOLT_CHRISTIANS_1_SLAVE", (pCity.getName(), )),
																										 None, 2, "Art/Interface/Buttons/Actions/button_kreuz.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
										else:
												pCity.changeFreeSpecialistCount(eSpecialistGlad, -1)
												if pPlayer.isHuman():
														CyInterface().addMessage(iPlayer, True, 8, CyTranslator().getText("TXT_KEY_REVOLT_CHRISTIANS_1_GLAD", (pCity.getName(), )),
																										 None, 2, "Art/Interface/Buttons/Actions/button_kreuz.dds", ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

		# Christentum kommt in die Stadt 5%
		if iCitySlaves > 0 and not bRevolt:
				iReligion = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
				if PAE_Christen.canSpreadChristentumOverall():
						iRand = CvUtil.myRandom(20, "RELIGION_CHRISTIANITY")
						if iRand == 1:
								if not pCity.isHasReligion(iReligion):
										pCity.setHasReligion(iReligion, 1, 1, 0)
										if pPlayer.isHuman():
												CyInterface().addMessage(iPlayer, True, 8, CyTranslator().getText("TXT_KEY_SLAVES_SPREAD_CHRISTIANITY", (pCity.getName(), )),
																								 None, 2, "Art/Interface/Buttons/Actions/button_kreuz.dds", ColorTypes(13), pCity.getX(), pCity.getY(), True, True)


def doMissionaryForCivs(iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		pCity = None
		(loopCity, pIter) = pPlayer.firstCity(False)
		while loopCity:
				# find first valid city
				if not loopCity.isNone() and loopCity.getOwner() == pPlayer.getID():
						pCity = loopCity
						break
				(loopCity, pIter) = pPlayer.nextCity(pIter, False)
		if pCity:
				# # -- Nordischer Missionar fuer Germanen/Vandalen
				# if gc.getGame().getGameTurnYear() == -2250:
				# Civ = gc.getInfoTypeForString("CIVILIZATION_GERMANEN")
				# iRel = gc.getInfoTypeForString("RELIGION_NORDIC")
				# #if gc.getGame().isReligionFounded(iRel):
				# if pPlayer.getCivilizationType() == Civ and pPlayer.getStateReligion() != iRel:
				# iUnitType = gc.getInfoTypeForString("UNIT_NORDIC_MISSIONARY")
				# pPlayer.initUnit(iUnitType, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
				# if (pPlayer.isHuman()):
				# popupInfo = CyPopupInfo()
				# popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				# popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_GALLIEN_MISSIONAR",("", )))
				# popupInfo.addPopup(iPlayer)

				# -- Griechischer Missionar fuer Rom
				if gc.getGame().getGameTurnYear() == -1200:
						iRel = gc.getInfoTypeForString("RELIGION_GREEK")
						if gc.getGame().isReligionFounded(iRel):
								if pPlayer.getStateReligion() != iRel:
										CivArray = [gc.getInfoTypeForString("CIVILIZATION_ROME"),gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS")]
										if pPlayer.getCivilizationType() in CivArray:
												iUnitType = gc.getInfoTypeForString("UNIT_GREEK_MISSIONARY")
												pPlayer.initUnit(iUnitType, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
												if pPlayer.isHuman():
														# Dies soll doppelte Popups in PB-Spielen vermeiden.
														if iPlayer == gc.getGame().getActivePlayer():
																popupInfo = CyPopupInfo()
																popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
																popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_ROM_MISSIONAR", ("", )))
																popupInfo.addPopup(iPlayer)

				# #-- Aegyptischer Missionar fuer Nubien
				# if gc.getGame().getGameTurnYear() == -3000:
						# Civ = gc.getInfoTypeForString("CIVILIZATION_NUBIA")
						# iRel = gc.getInfoTypeForString("RELIGION_EGYPT")
						# #if gc.getGame().isReligionFounded(iRel):
						# if pPlayer.getCivilizationType() == Civ and pPlayer.getStateReligion() != iRel:
								# iUnitType = gc.getInfoTypeForString("UNIT_EGYPT_MISSIONARY")
								# pPlayer.initUnit(iUnitType, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
								# if pPlayer.isHuman():
										# popupInfo = CyPopupInfo()
										# popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
										# popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_EGYPT_MISSIONAR",("", )))
										# popupInfo.addPopup(iPlayer)


def catchGreatPeople(pCity, iNewOwner, iPreviousOwner, bAssimilation):
		"""# --- gets captured: 50 % | can flee: 40 % | get killed: 10 %"""
		pNewOwner = gc.getPlayer(iNewOwner)
		pPreviousOwner = gc.getPlayer(iPreviousOwner)
		pCityPlot = pCity.plot()
		lUnits = [
				[gc.getInfoTypeForString("UNIT_PROPHET"), 3, 3, 3],
				[gc.getInfoTypeForString("UNIT_ARTIST"), 3, 3, 3],
				[gc.getInfoTypeForString("UNIT_SCIENTIST"), 3, 3, 3],
				[gc.getInfoTypeForString("UNIT_MERCHANT"), 3, 3, 3],
				[gc.getInfoTypeForString("UNIT_ENGINEER"), 3, 3, 4],
				[gc.getInfoTypeForString("UNIT_GREAT_GENERAL"), 11, 3, 10],
				[gc.getInfoTypeForString("UNIT_GREAT_SPY"), 4, 3, 4],
		]
		numGPTypes = len(lUnits)
		if bAssimilation:
				#lNumGP = [0] * numGPTypes
				return
		else:
				lNumGP = [
						pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST")),
						pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_ARTIST")),
						pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_SCIENTIST")),
						pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_MERCHANT")),
						pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_ENGINEER")),
						pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL")),
						pCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GREAT_SPY"))
				]
				# guenstigen Plot aussuchen
				# mit pCityPlot.getNearestLandPlot() ist es sonst immer der gleiche
				fleePlotArray = []
				iX = pCity.getX()
				iY = pCity.getY()
				for iI in range(DirectionTypes.NUM_DIRECTION_TYPES):
						loopPlot = plotDirection(iX, iY, DirectionTypes(iI))
						if loopPlot is not None and not loopPlot.isNone() and not loopPlot.isCity():
								if not loopPlot.isPeak() and not loopPlot.isWater():
										if loopPlot.getNumUnits() > 0:
												iRange = loopPlot.getNumUnits()
												for n in range(iRange):
														if loopPlot.getUnit(n).getOwner() == iPreviousOwner:
																fleePlotArray.append(loopPlot)
																break
										else:
												fleePlotArray.append(loopPlot)
				if not fleePlotArray:
						fleePlotArray.append(pCityPlot.getNearestLandPlot())

		bText = pNewOwner.isHuman()
		iNumFleePlots = len(fleePlotArray)
		bAlive = pPreviousOwner.isAlive()
		for i in range(numGPTypes):
				iCityGP = lNumGP[i]
				lUnit = lUnits[i]
				iNewUnit = lUnit[0]
				for _ in range(iCityGP):
						iRand = CvUtil.myRandom(10, "catchGreatPeople")
						if iRand < 5:
								CvUtil.spawnUnit(iNewUnit, pCityPlot, pNewOwner)
								if bText:
										iRand = 1 + CvUtil.myRandom(lUnit[1], "TXT_KEY_MESSAGE_CATCH_GP")
										text = CyTranslator().getText("TXT_KEY_MESSAGE_CATCH_GP"+str(i+1)+"_"+str(iRand), (0, 0))
										CyInterface().addMessage(iNewOwner, True, 10, text, None, 2, None, ColorTypes(14), 0, 0, False, False)
						elif iRand < 9 and bAlive and iNumFleePlots != 0:
								iJump2Plot = CvUtil.myRandom(iNumFleePlots, "catchGreatPeopleFleePlot")
								CvUtil.spawnUnit(iNewUnit, fleePlotArray[iJump2Plot], pPreviousOwner)
								if bText:
										iRand = 1 + CvUtil.myRandom(lUnit[2], "TXT_KEY_MESSAGE_FLEE_GP")
										text = CyTranslator().getText("TXT_KEY_MESSAGE_FLEE_GP"+str(i+1)+"_"+str(iRand), (0, 0))
										CyInterface().addMessage(iNewOwner, True, 10, text, None, 2, None, ColorTypes(7), 0, 0, False, False)
						elif bText:
								iRand = 1 + CvUtil.myRandom(lUnit[3], "TXT_KEY_MESSAGE_UNCATCH_GP")
								text = CyTranslator().getText("TXT_KEY_MESSAGE_UNCATCH_GP"+str(i+1)+"_"+str(iRand), (0, 0))
								CyInterface().addMessage(iNewOwner, True, 10, text, None, 2, None, ColorTypes(7), 0, 0, False, False)


def correctCityBuildings(pCity, pPlayer, pPreviousOwner):
		# Provinzpalast und Praefectur muss raus, Bischofssitz kann bleiben
		# wuerd es nicht reichen, die Eroberungswahrscheinlichkeit auf 0 zu stellen? -> nicht bei Renegade
		iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")
		if pCity.isHasBuilding(iBuilding):
				pCity.setNumRealBuilding(iBuilding, 0)
		iBuilding = gc.getInfoTypeForString("BUILDING_PRAEFECTUR")
		if pCity.isHasBuilding(iBuilding):
				pCity.setNumRealBuilding(iBuilding, 0)
		# Spezialgebaeude muessen raus, weil nicht die Building_X erobert werden, sondern die BuildingClass_X !!!
		for i in range(9):
				iBuilding = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationBuildings(gc.getInfoTypeForString("BUILDINGCLASS_SPECIAL"+str(i+1)))
				if iBuilding is not None and iBuilding != -1:
						if pCity.isHasBuilding(iBuilding):
								pCity.setNumRealBuilding(iBuilding, 0)
		# Palisade - Stadtmauer - Hohe/Breite Mauern
		iBuildingPalisade = gc.getInfoTypeForString("BUILDING_PALISADE")
		# prereq: BUILDINGCLASS_PALISADE
		iBuildingWalls1 = gc.getInfoTypeForString("BUILDING_WALLS")
		iBuildingWalls2 = gc.getInfoTypeForString("BUILDING_OPPIDUM")
		# prereq: BUILDINGCLASS_WALLS
		iBuildingHighWalls1 = gc.getInfoTypeForString("BUILDING_HIGH_WALLS")
		iBuildingHighWalls2 = gc.getInfoTypeForString("BUILDING_CELTIC_DUN")
		iBuildingHighWalls3 = gc.getInfoTypeForString("BUILDING_HIGH_WALLS_GRECO")
		if pCity.isHasBuilding(iBuildingHighWalls1) or pCity.isHasBuilding(iBuildingHighWalls2) or pCity.isHasBuilding(iBuildingHighWalls3):
				if not pCity.isHasBuilding(iBuildingWalls1) and not pCity.isHasBuilding(iBuildingWalls2):
						iBuilding = gc.getCivilizationInfo(pPreviousOwner.getCivilizationType()).getCivilizationBuildings(gc.getInfoTypeForString("BUILDINGCLASS_WALLS"))
						pCity.setNumRealBuilding(iBuilding, 1)
		if pCity.isHasBuilding(iBuildingWalls1) or pCity.isHasBuilding(iBuildingWalls2):
				if not pCity.isHasBuilding(iBuildingPalisade):
						pCity.setNumRealBuilding(iBuildingPalisade, 1)

		# Handelsstrasse (wird bei onCityAcquired leider entfernt)
		bSetTradeRoad = False
		iTradeRoad = gc.getInfoTypeForString("ROUTE_TRADE_ROAD")
		iBuilding = gc.getInfoTypeForString("BUILDING_HANDELSZENTRUM")
		if pCity.isHasBuilding(iBuilding):
				bSetTradeRoad = True
		else:
				iX = pCity.plot().getX()
				iY = pCity.plot().getY()
				for i in range(3):
						for j in range(3):
								loopPlot = gc.getMap().plot(iX + i - 1, iY + j - 1)
								if not loopPlot.isNone():
										if loopPlot.getRouteType() == iTradeRoad:
												bSetTradeRoad = True
												break
						if bSetTradeRoad:
								break
		if bSetTradeRoad:
				pCity.plot().setRouteType(iTradeRoad)


def doFreeTechMissionary(iTechType, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)

		# Religionen
		lTechs = {
				gc.getInfoTypeForString("TECH_RELIGION_NORDIC"): gc.getInfoTypeForString("UNIT_NORDIC_MISSIONARY"),
				gc.getInfoTypeForString("TECH_RELIGION_CELTIC"): gc.getInfoTypeForString("UNIT_CELTIC_MISSIONARY"),
				gc.getInfoTypeForString("TECH_RELIGION_SUMER"): gc.getInfoTypeForString("UNIT_SUMER_MISSIONARY"),
				gc.getInfoTypeForString("TECH_RELIGION_GREEK"): gc.getInfoTypeForString("UNIT_GREEK_MISSIONARY"),
				gc.getInfoTypeForString("TECH_RELIGION_EGYPT"): gc.getInfoTypeForString("UNIT_EGYPT_MISSIONARY"),
				gc.getInfoTypeForString("TECH_RELIGION_PHOEN"): gc.getInfoTypeForString("UNIT_PHOEN_MISSIONARY"),
				gc.getInfoTypeForString("TECH_RELIGION_HINDU"): gc.getInfoTypeForString("UNIT_HINDU_MISSIONARY"),
				gc.getInfoTypeForString("TECH_RELIGION_ROME"): gc.getInfoTypeForString("UNIT_ROME_MISSIONARY"),
				gc.getInfoTypeForString("TECH_DUALISMUS"): gc.getInfoTypeForString("UNIT_ZORO_MISSIONARY"),
				gc.getInfoTypeForString("TECH_FRUCHTBARKEIT"): gc.getInfoTypeForString("UNIT_EXECUTIVE_2"),
				gc.getInfoTypeForString("TECH_SENSE"): gc.getInfoTypeForString("UNIT_EXECUTIVE_3"),
				gc.getInfoTypeForString("TECH_GLADIATOR"): gc.getInfoTypeForString("UNIT_EXECUTIVE_5"),
				#gc.getInfoTypeForString("TECH_COLONIZATION"): gc.getInfoTypeForString("UNIT_SETTLER"),
		}

		# PAE VII: also for Team MP Games
		iTeam = pPlayer.getTeam()
		iRange = gc.getMAX_PLAYERS()
		for i in range(iRange):
			pPlayer = gc.getPlayer(i)
			iOtherTeam = pPlayer.getTeam()
			if iTeam == iOtherTeam:

				# Einheit erstellen
				try:
						iUnit = lTechs[iTechType]
						# Zufallsstadt auswaehlen
						lCities = []
						(loopCity, pIter) = pPlayer.firstCity(False)
						while loopCity:
								if not loopCity.isNone() and loopCity.getOwner() == iPlayer:  # only valid cities
										lCities.append(loopCity)
								(loopCity, pIter) = pPlayer.nextCity(pIter, False)

						if lCities:
								iRandCity = lCities[CvUtil.myRandom(len(lCities), "doFreeTechMissionary")]
								if iUnit == gc.getInfoTypeForString("UNIT_SETTLER"): 
										iUnitAIType = UnitAITypes.UNITAI_SETTLE
								else: 
										iUnitAIType = UnitAITypes.UNITAI_MISSIONARY
								NewUnit = pPlayer.initUnit(iUnit, iRandCity.getX(), iRandCity.getY(), iUnitAIType, DirectionTypes.DIRECTION_SOUTH)

								# Matriarchist
								if iTechType == gc.getInfoTypeForString("TECH_FRUCHTBARKEIT"):
										# PAE 6.15: eine zweite Einheit erstellen
										NewUnit2 = pPlayer.initUnit(iUnit, iRandCity.getX(), iRandCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)

										# Verschiedene Gottesanbeter
										lCivs = {
												gc.getInfoTypeForString("CIVILIZATION_CELT"): "TXT_KEY_UNIT_MATRIACHAT_CELTS",
												gc.getInfoTypeForString("CIVILIZATION_GERMANEN"): "TXT_KEY_UNIT_MATRIACHAT_GERMAN",
												gc.getInfoTypeForString("CIVILIZATION_ROME"): "TXT_KEY_UNIT_MATRIACHAT_ROME",
												gc.getInfoTypeForString("CIVILIZATION_GREECE"): "TXT_KEY_UNIT_MATRIACHAT_GREEK",
												gc.getInfoTypeForString("CIVILIZATION_ATHENS"): "TXT_KEY_UNIT_MATRIACHAT_GREEK",
												gc.getInfoTypeForString("CIVILIZATION_THEBAI"): "TXT_KEY_UNIT_MATRIACHAT_GREEK",
												gc.getInfoTypeForString("CIVILIZATION_SPARTA"): "TXT_KEY_UNIT_MATRIACHAT_GREEK",
												gc.getInfoTypeForString("CIVILIZATION_EGYPT"): "TXT_KEY_UNIT_MATRIACHAT_EGYPT",
												gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"): "TXT_KEY_UNIT_MATRIACHAT_PHOEN",
												gc.getInfoTypeForString("CIVILIZATION_PHON"): "TXT_KEY_UNIT_MATRIACHAT_PHOEN",
												gc.getInfoTypeForString("CIVILIZATION_ILLYRIA"): "TXT_KEY_UNIT_MATRIACHAT_ILLYRIA",
												gc.getInfoTypeForString("CIVILIZATION_BABYLON"): "TXT_KEY_UNIT_MATRIACHAT_BABYLON",
												gc.getInfoTypeForString("CIVILIZATION_SUMERIA"): "TXT_KEY_UNIT_MATRIACHAT_SUMER",
												gc.getInfoTypeForString("CIVILIZATION_HETHIT"): "TXT_KEY_UNIT_MATRIACHAT_HITTI",
												gc.getInfoTypeForString("CIVILIZATION_PERSIA"): "TXT_KEY_UNIT_MATRIACHAT_PERSIA",
												gc.getInfoTypeForString("CIVILIZATION_BERBER"): "TXT_KEY_UNIT_MATRIACHAT_BERBER",
												gc.getInfoTypeForString("CIVILIZATION_NUMIDIA"): "TXT_KEY_UNIT_MATRIACHAT_BERBER",
												gc.getInfoTypeForString("CIVILIZATION_IBERER"): "TXT_KEY_UNIT_MATRIACHAT_IBERIA",
												gc.getInfoTypeForString("CIVILIZATION_DAKER"): "TXT_KEY_UNIT_MATRIACHAT_DACIA",
												gc.getInfoTypeForString("CIVILIZATION_SKYTHEN"): "TXT_KEY_UNIT_MATRIACHAT_SCYTHS",
										}
										# Verschiedene Gottesanbeter
										try:
												text = CyTranslator().getText(lCivs[pPlayer.getCivilizationType()], ("",))
												text = text + " " + CyTranslator().getText("TXT_KEY_UNIT_KULT_FOLLOWER", ("",))
												NewUnit.setName(text)
												NewUnit2.setName(text)
										except KeyError:
												pass
										

								# ***TEST***
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Matriachist bekommen (Zeile 2848)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

								# Kybele/Cybele
								elif iTechType == gc.getInfoTypeForString("TECH_SENSE"):
										# PAE 6.15: eine zweite Einheit erstellen
										NewUnit2 = pPlayer.initUnit(iUnit, iRandCity.getX(), iRandCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)

								# Heroenkultist
								elif iTechType == gc.getInfoTypeForString("TECH_GLADIATOR"):
										# PAE 6.15: eine zweite Einheit erstellen
										NewUnit2 = pPlayer.initUnit(iUnit, iRandCity.getX(), iRandCity.getY(), UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)

										lCivs = {
												gc.getInfoTypeForString("CIVILIZATION_CELT"): "TXT_KEY_UNIT_HEROEN_CELTS",
												gc.getInfoTypeForString("CIVILIZATION_GERMANEN"): "TXT_KEY_UNIT_HEROEN_GERMAN",
												gc.getInfoTypeForString("CIVILIZATION_ROME"): "TXT_KEY_UNIT_HEROEN_ROME",
												gc.getInfoTypeForString("CIVILIZATION_GREECE"): "TXT_KEY_UNIT_HEROEN_ROME",
												gc.getInfoTypeForString("CIVILIZATION_ATHENS"): "TXT_KEY_UNIT_HEROEN_ROME",
												gc.getInfoTypeForString("CIVILIZATION_THEBAI"): "TXT_KEY_UNIT_HEROEN_ROME",
												gc.getInfoTypeForString("CIVILIZATION_SPARTA"): "TXT_KEY_UNIT_HEROEN_ROME",
												gc.getInfoTypeForString("CIVILIZATION_EGYPT"): "TXT_KEY_UNIT_HEROEN_EGYPT",
												gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"): "TXT_KEY_UNIT_HEROEN_PHOEN",
												gc.getInfoTypeForString("CIVILIZATION_PHON"): "TXT_KEY_UNIT_HEROEN_PHOEN",
												gc.getInfoTypeForString("CIVILIZATION_ILLYRIA"): "TXT_KEY_UNIT_HEROEN_PHOEN",
												gc.getInfoTypeForString("CIVILIZATION_BABYLON"): "TXT_KEY_UNIT_HEROEN_BABYLON",
												gc.getInfoTypeForString("CIVILIZATION_SUMERIA"): "TXT_KEY_UNIT_HEROEN_SUMER",
												gc.getInfoTypeForString("CIVILIZATION_HETHIT"): "TXT_KEY_UNIT_HEROEN_HITTI",
												gc.getInfoTypeForString("CIVILIZATION_PERSIA"): "TXT_KEY_UNIT_HEROEN_PERSIA",
										}
										# Verschiedene Gottesanbeter
										try:
												text = CyTranslator().getText(lCivs[pPlayer.getCivilizationType()], ("",))
												text = text + " " + CyTranslator().getText("TXT_KEY_UNIT_KULT_FOLLOWER", ("",))
												NewUnit.setName(text)
												NewUnit2.setName(text)
										except KeyError:
												pass

				except KeyError:
						pass


def doFreeTechSettler(iTechType, pPlayer):
		lSettlerCivs = [
				gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"),
				gc.getInfoTypeForString("CIVILIZATION_PHON"),
				gc.getInfoTypeForString("CIVILIZATION_GREECE"),
				gc.getInfoTypeForString("CIVILIZATION_ATHENS"),
				gc.getInfoTypeForString("CIVILIZATION_THEBAI"),
				gc.getInfoTypeForString("CIVILIZATION_SPARTA"),
				gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"),
				gc.getInfoTypeForString("CIVILIZATION_PERSIA"),
				gc.getInfoTypeForString("CIVILIZATION_BABYLON"),
				gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"),
				gc.getInfoTypeForString("CIVILIZATION_ISRAEL"),
				gc.getInfoTypeForString("CIVILIZATION_LYDIA"),
				gc.getInfoTypeForString("CIVILIZATION_INDIA"),
				gc.getInfoTypeForString("CIVILIZATION_ROME")
		]
		lSettlerTechs = [
				gc.getInfoTypeForString("TECH_GEOMETRIE"),
				gc.getInfoTypeForString("TECH_SCHIFFSBAU"),
				gc.getInfoTypeForString("TECH_DUALISMUS"),
				gc.getInfoTypeForString("TECH_RELIGION_CELTIC"),
				gc.getInfoTypeForString("TECH_RELIGION_NORDIC"),
				gc.getInfoTypeForString("TECH_RELIGION_ROME"),
				gc.getInfoTypeForString("TECH_PERSIAN_ROAD")
		]

		# PAE VII: also for Team MP Games
		iTeam = pPlayer.getTeam()
		iRange = gc.getMAX_PLAYERS()
		for i in range(iRange):
			pPlayer = gc.getPlayer(i)
			iOtherTeam = pPlayer.getTeam()
			if iTeam == iOtherTeam:

				if iTechType in lSettlerTechs or (iTechType == gc.getInfoTypeForString("TECH_COLONIZATION2") and pPlayer.getCivilizationType() in lSettlerCivs):
						# Einheit erstellen
						pCapital = pPlayer.getCapitalCity()
						if pCapital is not None and not pCapital.isNone():
								CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_SETTLER"), pCapital.plot(), pPlayer)


def getTechOnConquer(pCity, iPreviousOwner, iNewOwner):
		pPlayer = gc.getPlayer(iNewOwner)
		pPreviousOwner = gc.getPlayer(iPreviousOwner)
		pTeamOld = gc.getTeam(pPreviousOwner.getTeam())
		pTeamNew = gc.getTeam(pPlayer.getTeam())

		bGetTech = False
		if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_ARCHIVE")) or pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_LIBRARY")):
				bGetTech = True
		iRand = CvUtil.myRandom(3, "getTechOnConquer")
		if iRand == 1 or bGetTech:
				bGetTech = False  # falls es keine Tech gibt, dann Forschungsbonus

				TechArray = []
				for i in range(gc.getNumTechInfos()):
						if pTeamOld.isHasTech(i) and not pTeamNew.isHasTech(i):
								if gc.getTechInfo(i) is not None and gc.getTechInfo(i).isTrade():
										TechArray.append(i)
				if TechArray:
						bGetTech = True
						iTechRand = CvUtil.myRandom(len(TechArray), "getTechOnConquer2")
						iTech = TechArray[iTechRand]
						if pPlayer.getCurrentResearch() == iTech:
								pTeamNew.setResearchProgress(iTech, gc.getTechInfo(iTech).getResearchCost()-1, iNewOwner)
						pTeamNew.setHasTech(iTech, 1, iNewOwner, 0, 1)
						if pPlayer.isHuman():
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_POPUP_GETTING_TECH", (gc.getTechInfo(iTech).getDescription(), )))
								popupInfo.addPopup(iNewOwner)
						else:
								pPlayer.clearResearchQueue()
						# ***TEST***
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Tech erhalten (Zeile 3465)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

		# Forschungsbonus auf derzeitige Forschung
		if not bGetTech:
				iTechOld = pPreviousOwner.getCurrentResearch()
				iTechNew = pPlayer.getCurrentResearch()

				#iEraPercent = gc.getEraInfo(gc.getTechInfo(iTechNew).getEra()).getResearchPercent()

				# Beim Gewinner: Ein Drittel der Zeit verkuerzen
				# Beim Verlierer: Ein Viertel der Zeit verlaengern
				# Forschungkosten != reale Kosten (+% in Era und Schwierigkeitsgrad)
				if iTechNew != -1:
						iProgress = int(gc.getTechInfo(iTechNew).getResearchCost() / 4) + pCity.getPopulation() * 10
						# Halber Wert bei unterentwickelter CIV
						if pPreviousOwner.getTechScore() < pPlayer.getTechScore():
								iProgress = iProgress / 2

						# No auto-grant, so set to 1 less of full amount => stimmt nicht, weil bei Cost nicht +% von Era und Schw.grad miteinberechnet wird
						# if pTeamNew.getResearchProgress(iTechNew) + iProgress >= gc.getTechInfo(iTechNew).getResearchCost():
						#  iProgress = pTeamNew.getResearchProgress(iTechNew) + iProgress - gc.getTechInfo(iTechNew).getResearchCost() - 1
						pTeamNew.changeResearchProgress(iTechNew, iProgress, iNewOwner)
						if pPlayer.isHuman():
								CyInterface().addMessage(iNewOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_CONQUER_RESEARCH_WINNER", (iProgress,)), None, 2, None, ColorTypes(8), 0, 0, False, False)

				if iTechOld != -1:
						iProgress = int(gc.getTechInfo(iTechOld).getResearchCost() / 4) + pCity.getPopulation() * 10
						iProgress = min(iProgress, pTeamOld.getResearchProgress(iTechOld))
						# Halber Wert bei unterentwickelter CIV
						if pPreviousOwner.getTechScore() < pPlayer.getTechScore():
								iProgress = iProgress / 2
						pTeamOld.changeResearchProgress(iTechOld, -iProgress, iPreviousOwner)
						if pPreviousOwner.isHuman():
								CyInterface().addMessage(iPreviousOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_CONQUER_RESEARCH_LOSER", (iProgress,)), None, 2, None, ColorTypes(7), 0, 0, False, False)


def getGoldkarren(pCity, pPlayer):
		iPop = int(pCity.getPopulation())
		if iPop == 1:
				iBeute = 1
		else:
				iBeute = iPop * 2 - 1
		iBeute = min(10,iBeute) # maximal 10 Goldkarren
		if iBeute > 0:
				for _ in range(iBeute):
						CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_GOLDKARREN"), pCity.plot(), pPlayer)


def doRefugeeToNeighborCity(pCity, iPreviousOwner, iNewOwner):
		# --- Bevoelkerungszuwachs bei Nachbarstaedten (50% Chance pro Stadt fuer + 1 Pop)
		# --- PAE V Patch4: ab Pop 3 (sonst exploit)
		iX = pCity.getX()
		iY = pCity.getY()
		for x in range(-5, 6):
				for y in range(-5, 6):
						loopPlot = plotXY(iX, iY, x, y)
						if loopPlot is not None and not loopPlot.isNone():
								if loopPlot.isCity():
										loopCity = loopPlot.getPlotCity()
										iLoopOwner = loopCity.getOwner()
										if iLoopOwner != -1 and iLoopOwner != iNewOwner and iLoopOwner != gc.getBARBARIAN_PLAYER():
												iRand = CvUtil.myRandom(2, "doRefugeeToNeighborCity")
												if iRand == 1:
														loopCity.changePopulation(1)
														if gc.getPlayer(iLoopOwner).isHuman():
																CyInterface().addMessage(iLoopOwner, True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_CITY_GETS_POP", (pCity.getName(), loopCity.getName())),
																												 None, 2, "Art/Interface/Buttons/Units/button_emigrant.dds", ColorTypes(13), loopPlot.getX(), loopPlot.getY(), True, True)
														# Kultur & Religion
														if iPreviousOwner != gc.getBARBARIAN_PLAYER():
																# Kultur
																iCulture = pCity.getCulture(iLoopOwner)
																iPop = loopCity.getPopulation()
																if iCulture > 1 and iPop > 0:
																		iChangeCulture = iCulture / iPop
																		loopCity.changeCulture(iPreviousOwner, iChangeCulture, 0)
																# Religion (ab PAE VII)
																iReligion = getCityReligion(pCity)
																if iReligion != -1:
																	if not loopCity.isHasReligion(iReligion):
																		loopCity.setHasReligion(iReligion, 1, 1, 0)

														# PAE Provinzcheck
														doCheckCityState(loopCity)
														# ***TEST***
														#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Stadtpop gewachsen durch Krieg (Zeile 3493)",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)


def removeSwamp(pCity, sText):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		bFeatSwamp = False
		terrain_swamp = gc.getInfoTypeForString("TERRAIN_SWAMP")
		terrain_grass = gc.getInfoTypeForString("TERRAIN_GRASS")
		iX = pCity.getX()
		iY = pCity.getY()
		for x in range(-1, 2):
				for y in range(-1, 2):
						loopPlot = plotXY(iX, iY, x, y)
						if loopPlot is not None and not loopPlot.isNone():
								if loopPlot.getTerrainType() == terrain_swamp:
										loopPlot.setTerrainType(terrain_grass, 1, 1)
										loopPlot.setImprovementType(-1)
										bFeatSwamp = True
		if bFeatSwamp and pPlayer.isHuman():
				CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText(sText, (pCity.getName(),)), None, 2, None, ColorTypes(14), iX, iY, False, False)

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Sumpf wird entfernt (Zeile 2232)",1)), None, 2, None, ColorTypes(10), iX, iY, False, False)

# Bei fortgeschrittenen Spielen soll der Palast in der ersten Stadt autom. erstellt werden
def doCheckCapital(pCity):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.getCurrentEra() > 0:
				pCapital = pPlayer.getCapitalCity()
				if pCapital.isNone():  # or pCapital is None or pCapital == "None":
						# if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_LEADERSHIP")):
						pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_PALACE"), 1)


def doMessageWonderCapture(pCity):
		iOwner = pCity.getOwner()
		if pCity.getNumWorldWonders() > 0:
				for i in range(gc.getNumBuildingInfos()):
						eLoopBuilding = gc.getBuildingInfo(i)
						if pCity.isHasBuilding(i):
								eBuildingClass = gc.getBuildingClassInfo(eLoopBuilding.getBuildingClassType())
								if eBuildingClass.getMaxGlobalInstances() == 1:
										pPlayer = gc.getPlayer(iOwner)
										for iLoopPlayer in range(gc.getMAX_PLAYERS()):
												pLoopPlayer = gc.getPlayer(iLoopPlayer)
												pLoopTeam = gc.getTeam(pLoopPlayer.getTeam())
												if pLoopTeam.isHasMet(pPlayer.getTeam()) and pLoopPlayer.isHuman():
														if iLoopPlayer == iOwner:
																CyInterface().addMessage(iLoopPlayer, False, 10, CyTranslator().getText("TXT_KEY_WONDER_CAPTURE_YOU", (pPlayer.getName(),
																																																																			 eLoopBuilding.getDescription())), '', 0, eLoopBuilding.getButton(), ColorTypes(8), pCity.getX(), pCity.getY(), True, True)
														else:
																CyInterface().addMessage(iLoopPlayer, False, 10, CyTranslator().getText("TXT_KEY_WONDER_CAPTURE", (pPlayer.getName(), eLoopBuilding.getDescription())),
																												 '', 0, eLoopBuilding.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)


def isHasHeldendenkmal(pCity):
		if pCity and not pCity.isNone():
				for iBuilding in L.LHeldendenkmal:
						if pCity.isHasBuilding(iBuilding):
								return True
		return False


def getHeldendenkmalList(pCity):
		lBuildings = []
		for iBuilding in L.LHeldendenkmal:
				if pCity.isHasBuilding(iBuilding):
						lBuildings.append(iBuilding)
		return lBuildings

# rename cities (called from EventManager onCityBuilt)
def doCheckCityName(pCity):
		# init
		Filename = ""
		# Szenarien
		sScenarioName = CvUtil.getScriptData(CyMap().plot(0, 0), ["S", "t"])
		if sScenarioName == "RiseOfGreece":
				Filename = "Cities_RiseOfGreece.txt"
		elif sScenarioName == "BarbaricumRiseOfGreekPoleis":
				Filename = "Cities_BarbaricumRiseOfGreece.txt"
		elif sScenarioName == "EuropeMini":
				Filename = "Cities_Europe_Mini.txt"
		elif sScenarioName == "EuropeLarge" or sScenarioName == "SchmelzEuro":
				Filename = "Cities_Europe_Large.txt"
		elif sScenarioName == "CivIIIRiseOfRome":
				Filename = "Cities_CivIIIRiseOfRome.txt"

		if Filename != "":
				# init
				# thisCityName = pCity.getName()
				thisCityX = pCity.getX()
				thisCityY = pCity.getY()
				CityNamesFile = open(os.path.join("Mods", PAEMod, "Assets", "XML","Misc",Filename))
				for CurString in CityNamesFile.readlines():
						if "#" in CurString:
								continue
						if "x=" in CurString or "X=" in CurString:
								xRange = getRangeCut(CurString[2:])
						elif "y=" in CurString or "Y=" in CurString:
								yRange = getRangeCut(CurString[2:])
						elif "name=" in CurString or "Name=" in CurString:
								cityName = CurString[5:].strip()

								if "TXT_KEY" in cityName:
										cityName = CyTranslator().getText(cityName, ())

								# ***TEST***
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("City name: " + cityName,0)), None, 2, None, ColorTypes(10), 0, 0, False, False)
								# for i in xRange:
								#  CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("X",i)), None, 2, None, ColorTypes(10), 0, 0, False, False)
								# for i in yRange:
								#  CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Y",i)), None, 2, None, ColorTypes(10), 0, 0, False, False)

								if thisCityX in xRange and thisCityY in yRange:
										bRename = True
										# check cities
										iNumPlayers = gc.getMAX_PLAYERS()
										for iPlayer in range(iNumPlayers):
												pPlayer = gc.getPlayer(iPlayer)
												iNumCities = pPlayer.getNumCities()
												for iCity in range(iNumCities):
														if pPlayer.getCity(iCity).getName() == cityName:
																bRename = False
																break  # for iCity
												if not bRename:
														break  # for iPlayer

										# rename city
										if bRename:
												pCity.setName(cityName, 0)
												break  # for CurString
				CityNamesFile.close()


def getRangeCut(string):
		string = str(string)
		string = string.strip()
		if "-" not in string:
				return [int(string)]
		else:
				for i in range(len(string)):
						if string[i] == "-":
								iPos = i
								break
				iBegin = int(string[:iPos])
				iEnd = string[iPos+1:]
				iDiff = int(iEnd) - int(iBegin)
				if iDiff < 0:
						iDiff *= -1
				xyRange = []
				xyRange.append(iBegin)
				for i in range(iDiff):
						iBegin += 1
						xyRange.append(iBegin)
				return xyRange

# PAE Stadtstatus
# 0: Siedlung
# 1: Dorf
# 2: Stadt
# 3: Provinzstadt
# 4: Metropole
def getCityStatus(pCity, iPlayer, iCity, bReturnButton):
		if pCity == None:
				pCity = gc.getPlayer(iPlayer).getCity(iCity)
		if pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_METROPOLE")):
				if bReturnButton:
						return gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_METROPOLE")).getButton()
				else:
						return 4
		elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZ")):
				if bReturnButton:
						return gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_PROVINZ")).getButton()
				else:
						return 3
		elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_STADT")):
				if bReturnButton:
						return gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_STADT")).getButton()
				else:
						return 2
		elif pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_KOLONIE")):
				if bReturnButton:
						return gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_KOLONIE")).getButton()
				else:
						return 1

		if bReturnButton:
				return gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_SIEDLUNG")).getButton()
		else:
				return 0

# City Civil War
# Return True: auch wenn Bürgerkrieg gerade im Gang ist oder soeben beendet wird
def doCheckCivilWar(pCity):
		# BTS Bug 10.2023: wo zufällig eine Stadt ohne Namen und falscher ID geschickt wird (im WB wird sie mit Namen und anderer ID angezeigt)
		# getName() check verhindert somit einen python Fehler (c++ exception) auf großen Karten
		if pCity is None or pCity.isNone() or pCity.getName() == "":
				return False
		if not pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")):
				return False
		# check General oder Rhetoriker
		if doCityCheckRevoltEnd(pCity):
				return True

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("CIVIL WAR",pCity.getX())), None, 2, None, ColorTypes(10), 0, 0, False, False)
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",(pCity.getName(),pCity.getY())), None, 2, None, ColorTypes(10), 0, 0, False, False)

		# Inits
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		# pPlot = pCity.plot()
		iPop = pCity.getPopulation()
		bHuman = pPlayer.isHuman()

		# alle Einheiten verletzen
		lUnits = doCivilWarHarmUnits(pCity)
		iMilitaryUnits = len(lUnits)

		# in capital, units count double. Maybe check for GovernmentCenter?
		iUnitsExtraCalc = 0
		if pCity.isCapital() or pCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_PROVINZPALAST")):
				iUnitsExtraCalc = iMilitaryUnits

		iChance = CvUtil.myRandom(100, "iRandCityCivilWarChances")

		# Chance, dass der Civil War endet: HI 1:20, KI 1:5
		# End of Civil War
		if iPop <= iMilitaryUnits + iUnitsExtraCalc or iChance < 5 or not bHuman and iChance < 20:
				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("End Civil War",0)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR"), 0)
				# Der Bürgerkrieg in %s wurde beendet.
				if pPlayer.isHuman():
						CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_1", (pCity.getName(),)), "AS2D_WELOVEKING", 2,
																		 gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")).getButton(), ColorTypes(8), pCity.getX(), pCity.getY(), True, True)
						# popupInfo = CyPopupInfo()
						# popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						# popupInfo.setText(CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_1", (pCity.getName(),)))
						# popupInfo.addPopup(iPlayer)
				return True

		# In %s tobt immer noch ein Bürgerkrieg! Es steht/stehen x Einheit/en gegen y Bevölkerung!
		if pPlayer.isHuman():
				CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_6", (pCity.getName(), iMilitaryUnits, iPop)), "AS2D_REVOLTSTART",
																 2, gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

		# Chance, dass diese Runde nix passiert: HI 25%, KI 50%
		if iChance < 25 or bHuman and iChance < 50:

				iRand = CvUtil.myRandom(iPop + iMilitaryUnits, "iRandCityCivilWarUnitsVsPop")

				# Die Einheiten gewinnen gegen Pop
				if iRand > iMilitaryUnits:
						if iPop > 1:
								pCity.changePopulation(-1)
						# Es wurden etliche Bürger in %s niedergemetzelt.
						if pPlayer.isHuman():
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_2", (pCity.getName(),)), None, 2,
																				 gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
						# ***TEST***
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Civil War -POP",pCity.getX())), None, 2, None, ColorTypes(10), 0, 0, False, False)
				# es wird eine Einheit gekillt
				elif iMilitaryUnits > 0:

						lHarmedUnits = []
						for loopUnit in lUnits:
								if loopUnit.getDamage() > 74:
										lHarmedUnits.append(loopUnit)

						if lHarmedUnits:

								# kill heavy injured unit
								iRand = CvUtil.myRandom(len(lHarmedUnits), "iRandCityCivilWarUnitLost")

								lHarmedUnits[iRand].kill(True, -1)
								iMilitaryUnits -= 1
								# Der Mob in %s konnte eine Einheit töten.
								if pPlayer.isHuman():
										CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_3", (pCity.getName(),)), None, 2,
																						 gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
										popupInfo = CyPopupInfo()
										popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
										popupInfo.setText(CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_3", (pCity.getName(),)))
										popupInfo.addPopup(iPlayer)
								# ***TEST***
								#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Civil War -UNIT",pCity.getX())), None, 2, None, ColorTypes(10), 0, 0, False, False)

				# Stadt wird barbarisch, wenn keine Einheiten mehr drin sind
				if iMilitaryUnits <= 0:
						pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR"), 0)
						#doRenegadeCity(pCity, gc.getBARBARIAN_PLAYER(), None)
						# pPlayer.acquireCity (CyCity pCity, BOOL bConquest, BOOL bTrade)
						gc.getPlayer(gc.getBARBARIAN_PLAYER()).acquireCity(pCity, False, True)
						# Ihr habt die Stadt %s verloren.
						if pPlayer.isHuman():
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_4", (pCity.getName(),)), "AS2D_REVOLTSTART", 2,
																				 gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_4", (pCity.getName(),)))
								popupInfo.addPopup(iPlayer)
						# ***TEST***
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("BarbarCity",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		return True

def doStartCivilWar(pCity, iChance):
		if pCity is None or pCity.isNone():
				return

		if CvUtil.myRandom(100, "iRandStartCityCivilWar") < iChance:
				iPlayer = pCity.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Start Civil War",pCity.getPopulation())), None, 2, None, ColorTypes(10), 0, 0, False, False)
				pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR"), 1)
				# Ein Bürgerkrieg ist in %s1 ausgebrochen!
				if pPlayer.isHuman():
						CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_5", (pCity.getName(),)), "AS2D_REVOLTSTART", 2,
																		 gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_5", (pCity.getName(),)))
						popupInfo.addPopup(iPlayer)

				# Es gibt Städte, die haben Units > Pop. Das wäre sonst ohne Auswirkung.
				# A: Einheiten verletzen
				# B: 50:50 Pop -1
				doCivilWarHarmUnits(pCity)

				# Die Einheiten gewinnen gegen Pop
				if CvUtil.myRandom(2, "iRandCityCivilWarPop-1") == 1:
						if pCity.getPopulation() > 1:
								pCity.changePopulation(-1)
						# Es wurden etliche Bürger in %s niedergemetzelt.
						if pPlayer.isHuman():
								CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_INFO_CIVIL_WAR_2", (pCity.getName(),)), None, 2,
																				 gc.getBuildingInfo(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")).getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
						# ***TEST***
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Civil War -POP",pCity.getX())), None, 2, None, ColorTypes(10), 0, 0, False, False)


def doCivilWarHarmUnits(pCity):
		if pCity is None or pCity.isNone():
				return
		iPlayer = pCity.getOwner()
		pPlot = pCity.plot()
		lUnits = []
		# Einheiten verletzen
		for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getOwner() == iPlayer and pUnit.isMilitaryHappiness():
						lUnits.append(pUnit)

						iPrevDamage = pUnit.getDamage()
						if iPrevDamage >= 90:
								continue

						iDamage = 20 + CvUtil.myRandom(20, "iRandCityCivilWarUnitDamage")
						if iPrevDamage + iDamage >= 90:
								pUnit.setDamage(90, iPlayer)
						else:
								pUnit.changeDamage(iDamage, False)

		return lUnits

# Project : Panhellenion
# Alle Städte bekommen den Hellenismus Kult (inkl. Vasallen)
def doPanhellenismus(iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iCorp = gc.getInfoTypeForString("CORPORATION_7")
		iRange = pPlayer.getNumCities()
		for ii in range(iRange):
				pCity = pPlayer.getCity(ii)
				if pCity and not pCity.isNone():
						if not pCity.isHasCorporation(iCorp):
								pCity.setHasCorporation(iCorp, 1, 0, 1)

		iHegemonTeam = pPlayer.getTeam()
		# pHegemonTeam = gc.getTeam(iHegemonTeam)
		iRange = gc.getMAX_PLAYERS()
		for ii in range(iRange):
				pLoopPlayer = gc.getPlayer(ii)
				if pLoopPlayer.isAlive():
						iTeam = pLoopPlayer.getTeam()
						pTeam = gc.getTeam(iTeam)
						if pTeam.isVassal(iHegemonTeam):
								iRange = pLoopPlayer.getNumCities()
								for jj in range(iRange):
										pCity = pLoopPlayer.getCity(jj)
										if pCity and not pCity.isNone():
												if not pCity.isHasCorporation(iCorp):
														pCity.setHasCorporation(iCorp, 1, 0, 0)

# Reliquie wird erzeugt
def getHolyRelic(pCity, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString("TECH_MARTYRIUM")):
				iBuilding = gc.getInfoTypeForString("BUILDING_MARTYRION")
				for iReligion in L.LMonoReligions:

						if pPlayer.getStateReligion() == iReligion and pCity.isHasReligion(iReligion):

								bRelic = False
								if pCity.isHasBuilding(iBuilding):
										pCity.setNumRealBuilding(iBuilding, 0)
										bRelic = True
								elif CvUtil.myRandom(10, "iRandCityRelic") == 1:
										bRelic = True

								if bRelic:
										CvUtil.spawnUnit(gc.getInfoTypeForString("UNIT_RELIC"), pCity.plot(), pPlayer)
										if pPlayer.isHuman():
												CyInterface().addMessage(iPlayer, True, 10, CyTranslator().getText("TXT_KEY_INFO_RELIC", (pCity.getName(),)), None, 2,
																								 gc.getUnitInfo(gc.getInfoTypeForString("UNIT_RELIC")).getButton(), ColorTypes(8), pCity.getX(), pCity.getY(), True, True)

# onCityRazed: Missionar erstellen
def getCityMissionar(pCity, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		iReligion = pPlayer.getStateReligion()
		if iReligion > -1 and pCity.isHasReligion(iReligion):
				for iUnit in range(gc.getNumUnitInfos()):
						if gc.getUnitInfo(iUnit).getPrereqReligion() == iReligion and "MISSIONARY" in gc.getUnitInfo(iUnit).getTextKey():
								CvUtil.spawnUnit(iUnit, pCity.plot(), pPlayer)
								break


def isCityState(iPlayer):
		# city states / Stadtstaaten
		return gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(gc.getInfoTypeForString("TECH_CITY_STATE"))

# in EventManager
# onCityAcquired(pCity, True)
# onCityDoTurn(pCity, False)
def doCheckDyingGeneral(pCity, bOnCityAcquired):
		eBuildingStadt = gc.getInfoTypeForString("BUILDING_STADT")
		if pCity.isHasBuilding(eBuildingStadt):
				eBuildingClass = gc.getBuildingInfo(eBuildingStadt).getBuildingClassType()
				if bOnCityAcquired:
						pCity.setBuildingHappyChange(eBuildingClass, 0)
						return
				iHappy = pCity.getBuildingHappyChange(eBuildingClass)
				if iHappy != 0:
						if CvUtil.myRandom(20, "iRandCityRelic") == 1:
								if iHappy < 0: iHappy += 1
								else: iHappy -= 1
								pCity.setBuildingHappyChange(eBuildingClass, iHappy)

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

		LReligions = [
				gc.getInfoTypeForString("RELIGION_JUDAISM"),
				gc.getInfoTypeForString("RELIGION_CHRISTIANITY"),
				gc.getInfoTypeForString("RELIGION_ISLAM")
		]
		LText = []
		bRefuse = False
		for i in LReligions:
				if pCity.isHasReligion(i) and pPlayer.getStateReligion() != i:
					bRefuse = True
					if i == gc.getInfoTypeForString("RELIGION_JUDAISM"): LText.append("TXT_RELIGION_UNIT_BUILT_INFO_1")
					elif i == gc.getInfoTypeForString("RELIGION_CHRISTIANITY"): LText.append("TXT_RELIGION_UNIT_BUILT_INFO_2")
					elif i == gc.getInfoTypeForString("RELIGION_ISLAM"): LText.append("TXT_RELIGION_UNIT_BUILT_INFO_3")

		if bRefuse and CvUtil.myRandom(5, "iRandReligionUnitBuiltRefuse") == 1:
				iRandText = CvUtil.myRandom(len(LText), "iRandReligionUnitBuiltRefuseText")
				pUnit.kill(True, -1)
				if pPlayer.isHuman():
						szText = u"%s: " % (pCity.getName()) + CyTranslator().getText(LText[iRandText], ())
						CyInterface().addMessage(iPlayer, True, 10, szText, None, 2, pUnit.getButton(), ColorTypes(7), pCity.getX(), pCity.getY(), True, True)

def getTaxesLimit(pPlayer):
		if (pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_DEMOCRACY")) or
				pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_ARISTOKRATIE")) or
				pPlayer.isCivic(gc.getInfoTypeForString("CIVIC_IMPERATOR"))
		):
				return 50
		else:
				return 75

def getCityReligion(pCity):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iPlayerReligion = -1
		lReligions = []
		iStateReligion = pPlayer.getStateReligion()
		iRange = gc.getNumReligionInfos()
		for iRel in range(iRange):
			if pCity.isHasReligion(iRel):
				if iRel == iStateReligion:
					iPlayerReligion = iRel
					break
				lReligions.append(iRel)

		if iPlayerReligion == -1:
			if len(lReligions):
				iRand = CvUtil.myRandom(len(lReligions), "setUnitReligion")
				iPlayerReligion = lReligions[iRand]
			# Das nicht, sonst haben die Auswanderer eroberter (barbarischer) Städte automatisch die Staatsreligion des Eroberers
			#else:
			#	iPlayerReligion = iStateReligion
		return iPlayerReligion
