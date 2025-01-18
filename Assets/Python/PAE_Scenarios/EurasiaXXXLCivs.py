# Scenario brettschmitt's XXXL

# Imports
from CvPythonExtensions import (CyGlobalContext, UnitAITypes, DirectionTypes, CommerceTypes)
# import CvEventInterface
import CvUtil
# import PyHelpers

# Defines
gc = CyGlobalContext()


def onGameStart():

		eBuilding = gc.getInfoTypeForString("BUILDING_PALACE")
		eBuildingClass = gc.getBuildingInfo(eBuilding).getBuildingClassType()
		# evtl. auch einfach:
		#eBuildingClass = gc.getInfoTypeForString("BUILDINGCLASS_PALACE")
		eTechJagd = gc.getInfoTypeForString("TECH_HUNTING")
		eTechFischen = gc.getInfoTypeForString("TECH_FISHING")
		eUnitHunter = gc.getInfoTypeForString("UNIT_HUNTER")
		eUnitBoot = gc.getInfoTypeForString("UNIT_WORKBOAT")

		for iPlayer in range(gc.getMAX_PLAYERS()):

				iResearchBoost = 0
				pPlayer = gc.getPlayer(iPlayer)
				# iCiv = pPlayer.getCivilizationType()
				pTeam = gc.getTeam(pPlayer.getTeam())

				pCity = pPlayer.getCity(0)
				if pCity and not pPlayer.isHuman():

						# Rom
						if iPlayer == 20:
								# Palace
								if CvUtil.myRandom(10, "StartBoost") < 3:
										iResearchBoost = 3
								else:
										iResearchBoost = 6

								# Jagd
								if CvUtil.myRandom(10, "GiveStartTech") < 6:
										# pTeam.setHasTech(TechType eIndex, BOOL bNewValue, PlayerType ePlayer, BOOL bFirst, BOOL bAnnounce)
										pTeam.setHasTech(eTechJagd, 1, iPlayer, 0, 1)
										if CvUtil.myRandom(10, "CreateUnit") < 3:
												pPlayer.initUnit(eUnitHunter, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

						# Karthago
						elif iPlayer == 19:
								# Palace
								if CvUtil.myRandom(10, "StartBoost") < 3:
										iResearchBoost = 6
								else:
										iResearchBoost = 3

								# Fischen
								if CvUtil.myRandom(10, "GiveStartTech") < 6:
										pTeam.setHasTech(eTechFischen, 1, iPlayer, 0, 1)

								# Jagd
								if CvUtil.myRandom(10, "GiveStartTech") < 6:
										pTeam.setHasTech(eTechJagd, 1, iPlayer, 0, 1)
										if CvUtil.myRandom(10, "CreateUnit") < 3:
												pPlayer.initUnit(eUnitHunter, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

						# Persien
						elif iPlayer == 42:
								# Palace
								iRand = CvUtil.myRandom(10, "StartBoost")
								if iRand < 3:
										iResearchBoost = 3
								else:
										iResearchBoost = 6

								# Fischen
								if CvUtil.myRandom(10, "GiveStartTech") < 8:
										pTeam.setHasTech(eTechFischen, 1, iPlayer, 0, 1)

								# Jagd
								if CvUtil.myRandom(10, "GiveStartTech") < 6:
										pTeam.setHasTech(eTechJagd, 1, iPlayer, 0, 1)
										if CvUtil.myRandom(10, "CreateUnit") < 3:
												pPlayer.initUnit(eUnitHunter, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

						# Griechenland
						elif iPlayer == 25:
								# Palace
								if CvUtil.myRandom(10, "StartBoost") < 5:
										iResearchBoost = 3
								else:
										iResearchBoost = 6

								# Fischen
								if CvUtil.myRandom(10, "GiveStartTech") < 8:
										pTeam.setHasTech(eTechFischen, 1, iPlayer, 0, 1)
										if CvUtil.myRandom(10, "CreateUnit") < 6:
												pPlayer.initUnit(eUnitBoot, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

						# alle anderen Spieler: 30% Chance +3 Forschung im Palast
						elif CvUtil.myRandom(10, "StartBoost") < 3:
								iResearchBoost = 3

						if iResearchBoost:
								iResearch = pCity.getBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_RESEARCH) + iResearchBoost
								pCity.setBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_RESEARCH, iResearch)
