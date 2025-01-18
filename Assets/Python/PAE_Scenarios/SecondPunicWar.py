# Scenario SecondPunicWar by Barcas

# Imports
from CvPythonExtensions import (CyGlobalContext, CyPopupInfo, CyTranslator,
																ButtonPopupTypes, CyMap, UnitAITypes,
																CyInterface, DirectionTypes, CyCamera)
# import CvEventInterface
import CvUtil
# import PyHelpers
import PAE_City

# Defines
gc = CyGlobalContext()
iRome = 0
iCarthago = 1

# Kriegserklärung FIRST TURN
def onEndGameTurn(iGameTurn):

		# Beginn Runde 1 (218 v.Chr.) Kriegserklärung Team 0 (Rom) an Team 1 (Karthago)
		if iGameTurn == 12:

				# ewiger Krieg
				#gc.getTeam(gc.getPlayer(0).getTeam()).setPermanentWarPeace(gc.getPlayer(1).getTeam(), False)
				gc.getTeam(gc.getPlayer(iRome).getTeam()).declareWar(gc.getPlayer(iCarthago).getTeam(), False, 5)
				gc.getPlayer(iRome).AI_setAttitudeExtra(iCarthago, -50)
				gc.getPlayer(iCarthago).AI_setAttitudeExtra(iRome, -50)
				# gc.getTeam(gc.getPlayer(0).getTeam()).setWarWeariness(gc.getPlayer(1).getTeam(),30)
				# gc.getTeam(gc.getPlayer(1).getTeam()).setWarWeariness(gc.getPlayer(0).getTeam(),30)

				# Meldung an die Spieler
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_1", ("",)))
				popupInfo.addPopup(gc.getGame().getActivePlayer())

		# Konsul Lucius Postumius Albinus fällt im Kampf gegen Boier
		if iGameTurn == 40:
				iBoier = 7
				if not gc.getTeam(gc.getPlayer(iBoier).getTeam()).isAtWar(gc.getPlayer(iRome).getTeam()):
						gc.getTeam(gc.getPlayer(iBoier).getTeam()).declareWar(gc.getPlayer(iRome).getTeam(), False, 5)

				gc.getPlayer(iRome).AI_setAttitudeExtra(iBoier, -30)
				gc.getPlayer(iBoier).AI_setAttitudeExtra(iRome, -30)

				# Meldung an die Spieler
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_7", ("",)))
				popupInfo.addPopup(gc.getGame().getActivePlayer())

		# Massinissa verbündet sich mit Karthago
		# Civ Ost-Numider (Massinissa) wird Vasall von Karthago
		# Bedingung: Ost-Numider ist noch nicht Vasall
		if iGameTurn == 45:
				iMassinissa = 3
				iTeamCarthago = gc.getPlayer(iCarthago).getTeam()
				iTeamNumidien = gc.getPlayer(iMassinissa).getTeam()
				pTeamNumidien = gc.getTeam(iTeamNumidien)
				if not pTeamNumidien.isVassal(iTeamCarthago):

						gc.getTeam(iTeamCarthago).assignVassal(iTeamNumidien, 0)  # Vassal, but no surrender

						# Meldung an die Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_8", ("",)))
						popupInfo.addPopup(gc.getGame().getActivePlayer())

		# 214 v.Chr.: Syrakus erklärt Rom den Krieg
		if iGameTurn == 65:
				iSyracus = 21
				if not gc.getTeam(gc.getPlayer(iSyracus).getTeam()).isAtWar(gc.getPlayer(iRome).getTeam()):
						gc.getTeam(gc.getPlayer(iSyracus).getTeam()).declareWar(gc.getPlayer(iRome).getTeam(), False, 5)

						# Meldung an die Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_11", ("",)))
						popupInfo.addPopup(gc.getGame().getActivePlayer())

		# Syphax verbündet sich mit Rom
		# Civ West-Numider (Syphax) wird Vasall von Rom
		# Bedingung: West-Numider ist noch nicht Vasall von Rom
		if iGameTurn == 145:
				iSyphax = 2
				iTeamRome = gc.getPlayer(iRome).getTeam()
				iTeamNumidien = gc.getPlayer(iSyphax).getTeam()
				pTeamNumidien = gc.getTeam(iTeamNumidien)
				if not pTeamNumidien.isVassal(iTeamRome):

						gc.getTeam(iTeamRome).assignVassal(iTeamNumidien, 0)  # Vassal, but no surrender

						# Meldung an die Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_16", ("",)))
						popupInfo.addPopup(gc.getGame().getActivePlayer())

		# Syphax läuft zu Karthago über
		# Civ West-Numider (Syphax) wird Vasall von Karthago
		# Bedingung: West-Numider ist noch nicht Vasall von Karthago
		if iGameTurn == 174:
				iSyphax = 2
				iTeamCarthago = gc.getPlayer(iCarthago).getTeam()
				iTeamNumidien = gc.getPlayer(iSyphax).getTeam()
				pTeamNumidien = gc.getTeam(iTeamNumidien)
				if not pTeamNumidien.isVassal(iTeamCarthago):

						gc.getTeam(iTeamCarthago).assignVassal(iTeamNumidien, 0)  # Vassal, but no surrender

						# Meldung an die Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_18", ("",)))
						popupInfo.addPopup(gc.getGame().getActivePlayer())

		# Massinissa läuft zu Rom über
		# Civ Ost-Numider (Massinissa) wird Vasall von Rom
		# Bedingung: Ost-Numider ist noch nicht Vasall von Rom
		if iGameTurn == 145:
				iMassinissa = 3
				iTeamRome = gc.getPlayer(iRome).getTeam()
				iTeamNumidien = gc.getPlayer(iMassinissa).getTeam()
				pTeamNumidien = gc.getTeam(iTeamNumidien)
				if not pTeamNumidien.isVassal(iTeamRome):

						gc.getTeam(iTeamRome).assignVassal(iTeamNumidien, 0)  # Vassal, but no surrender

						# Meldung an die Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_19", ("",)))
						popupInfo.addPopup(gc.getGame().getActivePlayer())


def onEndPlayerTurn(iPlayer, iGameTurn):

		# Kelten erheben sich in der Po-Ebene
		if iGameTurn == 13:
				if iPlayer == iRome and gc.getPlayer(iPlayer).isHuman():

						# 1. barb. Einheiten bei Placentia
						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(47, 66),
								CyMap().plot(48, 66),
								CyMap().plot(49, 66)
						]
						Landungsplot = getRandomPlot(lPlots)

						# Einheiten erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_CELTIC_GALLIC_WARRIOR"),
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER"),
								gc.getInfoTypeForString("UNIT_HORSEMAN_CELTIC")
						]
						for i in LNewUnits:
								pUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						# Ping
						CyInterface().doPing(Landungsplot.getX(), Landungsplot.getY(), iPlayer)

						# 2. barb. Einheiten bei Ravenna
						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(53, 67),
								CyMap().plot(53, 57),
								CyMap().plot(53, 65)
						]
						Landungsplot = getRandomPlot(lPlots)

						# Einheiten erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_CELTIC_GALLIC_WARRIOR"),
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER"),
								gc.getInfoTypeForString("UNIT_HORSEMAN_CELTIC")
						]
						for i in LNewUnits:
								pUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						# Ping
						CyInterface().doPing(Landungsplot.getX(), Landungsplot.getY(), iPlayer)

						# Meldung an den Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_2", ("",)))
						popupInfo.addPopup(iPlayer)

		# 2. Schlacht von Lilybaeum, Angriff Karthago auf Sizilien
		if iGameTurn == 19:
				if iPlayer == iRome and gc.getPlayer(iPlayer).isHuman():

						# Plot für die Schiffe
						lPlots = [
								CyMap().plot(51, 45),
								CyMap().plot(51, 46),
								CyMap().plot(51, 47)
						]
						Schiffsplot = getRandomPlot(lPlots)


						# Meldung an den Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_3", ("",)))
						popupInfo.addPopup(iPlayer)
						CyCamera().JustLookAtPlot(Schiffsplot)
						
						# Karthago Gold geben, damit die KI die Schiffe nicht gleich auflöst
						gc.getPlayer(iCarthago).changeGold(300)

						# Schiffe erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_QUADRIREME")
						]
						for i in LNewUnits:
								for _ in range(4):
										pUnit = gc.getPlayer(iCarthago).initUnit(i, Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT2"), True)


		# Schlacht von Cissa, Römer landen in Iberien
		if iGameTurn == 23:
				if iPlayer == iCarthago and gc.getPlayer(iPlayer).isHuman():

						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(19, 52),
								CyMap().plot(19, 53),
								CyMap().plot(20, 53)
						]
						Landungsplot = getRandomPlot(lPlots)
						# Plot für die Schiffe
						lPlots = [
								CyMap().plot(20, 52),
								CyMap().plot(21, 52),
								CyMap().plot(21, 53)
						]
						Schiffsplot = getRandomPlot(lPlots)

						# Schiffe erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_QUADRIREME"),
								gc.getInfoTypeForString("UNIT_TRIREME")
						]
						for i in LNewUnits:
								for _ in range(2):
										pUnit = gc.getPlayer(iRome).initUnit(i, Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS1"), True)

						# Einheiten erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_TRIARII"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME")
						]
						for i in LNewUnits:
								pUnit = gc.getPlayer(iRome).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						# Meldung an den Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_4", ("",)))
						popupInfo.addPopup(iPlayer)
						CyCamera().JustLookAtPlot(Landungsplot)

		# Rom erobert Sagunt (Plot: 20,50)
		if iGameTurn == 30:
				if iPlayer == iCarthago and gc.getPlayer(iPlayer).isHuman() and CyMap().plot(20, 50).getOwner() == iCarthago:

						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(19, 51),
								CyMap().plot(20, 49)
						]
						Landungsplot = getRandomPlot(lPlots)
						# Plot für die Schiffe
						lPlots = [
								CyMap().plot(20, 49),
								CyMap().plot(20, 50),
								CyMap().plot(20, 51)
						]
						Schiffsplot = getRandomPlot(lPlots)

						# Schiffe erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_QUADRIREME"),
								gc.getInfoTypeForString("UNIT_TRIREME")
						]
						for i in LNewUnits:
								for _ in range(2):
										pUnit = gc.getPlayer(iRome).initUnit(i, Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS1"), True)

						# Einheiten erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_TRIARII"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME")
						]
						for i in LNewUnits:
								pUnit = gc.getPlayer(iRome).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						# Meldung an den Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_5", ("",)))
						popupInfo.addPopup(iPlayer)
						CyCamera().JustLookAtPlot(Landungsplot)

		# iberische Städte rebellieren gegen Karthago
		# barb. Einheiten in Iberien
		if iGameTurn == 38:
				if iPlayer == iCarthago and gc.getPlayer(iPlayer).isHuman():

						LNewUnits = [
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER_IBERIA"),
								gc.getInfoTypeForString("UNIT_SPEARMAN"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_CELTIBERIAN_CAVALRY")
						]

						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(14, 50),
								CyMap().plot(14, 51),
								CyMap().plot(14, 52)
						]
						Landungsplot = getRandomPlot(lPlots)
						for i in LNewUnits:
								pUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(8, 43),
								CyMap().plot(9, 42),
								CyMap().plot(9, 43)
						]
						Landungsplot = getRandomPlot(lPlots)
						for i in LNewUnits:
								pUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						# Meldung an den Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_6", ("",)))
						popupInfo.addPopup(iPlayer)
						CyCamera().JustLookAtPlot(Landungsplot)

		# Capua verbündet sich mit Hannibal
		# Capua wird barbarisch (Plot: 58, 58)
		# Bedinung: Capua = römisch + Rom u. Karthago im Krieg
		if iGameTurn == 50:
				if iPlayer == iRome and gc.getPlayer(iPlayer).isHuman():
						pPlot = CyMap().plot(58, 58)
						if pPlot.getOwner() == iRome and gc.getTeam(gc.getPlayer(iCarthago).getTeam()).isAtWar(gc.getPlayer(iRome).getTeam()):

								# Stadt wird barbarisch + Einheiten
								PAE_City.doRenegadeCity(pPlot.getPlotCity(), gc.getBARBARIAN_PLAYER(), None)

								LNewUnits = [
										gc.getInfoTypeForString("UNIT_REBELL"),
										gc.getInfoTypeForString("UNIT_REFLEX_ARCHER"),
										gc.getInfoTypeForString("UNIT_SAMNIT")
								]
								for i in LNewUnits:
										pUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(i, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CITY_GARRISON1"), True)

								# Meldung an den Spieler
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_9", ("",)))
								popupInfo.addPopup(iPlayer)
								CyCamera().JustLookAtPlot(pPlot)

		# Schlacht von Cornus, Punier landen auf Sardinien
		if iGameTurn == 56:
				if iPlayer == iRome and gc.getPlayer(iPlayer).isHuman():

						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(44, 52),
								CyMap().plot(45, 51),
								CyMap().plot(45, 52)
						]
						Landungsplot = getRandomPlot(lPlots)
						# Plot für die Schiffe
						lPlots = [
								CyMap().plot(43, 51),
								CyMap().plot(43, 52),
								CyMap().plot(43, 53)
						]
						Schiffsplot = getRandomPlot(lPlots)

						# Schiffe erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_QUADRIREME"),
								gc.getInfoTypeForString("UNIT_TRIREME")
						]
						for i in LNewUnits:
								for _ in range(2):
										pUnit = gc.getPlayer(iCarthago).initUnit(i, Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT2"), True)

						# Einheiten erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER"),
								gc.getInfoTypeForString("UNIT_SPEARMAN_CARTHAGE"),
								gc.getInfoTypeForString("UNIT_SPEARMAN_CARTHAGE"),
								gc.getInfoTypeForString("UNIT_REBELL"),
								gc.getInfoTypeForString("UNIT_REBELL"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER")
						]
						for i in LNewUnits:
								pUnit = gc.getPlayer(iCarthago).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						# Meldung an den Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_10", ("",)))
						popupInfo.addPopup(iPlayer)
						CyCamera().JustLookAtPlot(Landungsplot)

		# Massinissa schickt Truppen nach Iberien
		# ost-num. Truppen in Karthago-Nova
		# Bedingung: Ost-Numider Vasall von Karthago + Rom und Karthago im Krieg
		if iGameTurn == 85:
				if iPlayer == iCarthago or iPlayer == iRome:
						iMessana = 3
						iTeamCarthago = gc.getPlayer(iCarthago).getTeam()
						iTeamMessana = gc.getPlayer(iMessana).getTeam()
						pTeamMessana = gc.getTeam(iTeamMessana)
						if pTeamMessana.isVassal(iTeamCarthago) and gc.getTeam(iTeamCarthago).isAtWar(gc.getPlayer(iRome).getTeam()):

								# Plot für die Einheiten
								Landungsplot = CyMap().plot(19, 46)

								if iPlayer == iCarthago:
										# Einheiten erstellen
										LNewUnits = [
												gc.getInfoTypeForString("UNIT_HORSEMAN_NUMIDIA")
										]

										for i in LNewUnits:
												for _ in range(4):
														pUnit = gc.getPlayer(iMessana).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
														pUnit.setExperience(2, -1)

								# Meldung an den Spieler
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_12", ("",)))
								popupInfo.addPopup(iPlayer)
								CyCamera().JustLookAtPlot(Landungsplot)

		# Hannibal erobert Tarent
		# Tarent wird barbarisch
		# Bedinung: Tarent = römisch + Rom u. Karthago im Krieg
		if iGameTurn == 90:
				if iPlayer == iRome:
						pPlot = CyMap().plot(62, 53)
						if pPlot.getOwner() == iRome and gc.getTeam(gc.getPlayer(iRome).getTeam()).isAtWar(gc.getPlayer(iCarthago).getTeam()):

								# Stadt wird barbarisch + Einheiten
								PAE_City.doRenegadeCity(pPlot.getPlotCity(), gc.getBARBARIAN_PLAYER(), None)

								LNewUnits = [
										gc.getInfoTypeForString("UNIT_REBELL"),
										gc.getInfoTypeForString("UNIT_REFLEX_ARCHER"),
										gc.getInfoTypeForString("UNIT_HOPLIT")
								]
								for i in LNewUnits:
										pUnit = gc.getPlayer(gc.getBARBARIAN_PLAYER()).initUnit(i, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CITY_GARRISON1"), True)

								# Meldung an den Spieler
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_13", ("",)))
								popupInfo.addPopup(iPlayer)
								CyCamera().JustLookAtPlot(pPlot)

		# Unruhen in Rom
		if iGameTurn == 110:
				if iPlayer == iRome:
						pCity = gc.getPlayer(iPlayer).getCapitalCity()

						PAE_City.doCityRevolt(pCity, 4)

						# Meldung an den Spieler
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_14", ("",)))
						popupInfo.addPopup(iPlayer)
						CyCamera().JustLookAtPlot(pCity.plot())

		# Schlacht von Neu-Karthago, Römer greifen Stadt an
		# röm. Schiffe + Einheiten bei Neu-Karthago (Plot: 19,46)
		# Bedingung: Neu-Karthago = karth. + Rom und Karthago im Krieg
		if iGameTurn == 125:
				if iPlayer == iCarthago:
						pPlot = CyMap().plot(19, 46)  # TXT_KEY_CITY_NAME_CARTHAGO_NOVO
						if pPlot.getOwner() == iCarthago and gc.getTeam(gc.getPlayer(iCarthago).getTeam()).isAtWar(gc.getPlayer(iRome).getTeam()):

								# Plot für die Landungseinheiten
								lPlots = [
										CyMap().plot(18, 45),
										CyMap().plot(19, 45),
										CyMap().plot(19, 47)
								]
								Landungsplot = getRandomPlot(lPlots)
								# Plot für die Schiffe
								lPlots = [
										CyMap().plot(20, 45),
										CyMap().plot(20, 46),
										CyMap().plot(20, 47)
								]
								Schiffsplot = getRandomPlot(lPlots)

								# Schiffe erstellen
								LNewUnits = [
										gc.getInfoTypeForString("UNIT_QUADRIREME"),
										gc.getInfoTypeForString("UNIT_TRIREME")
								]
								for i in LNewUnits:
										for _ in range(2):
												pUnit = gc.getPlayer(iRome).initUnit(i, Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
												pUnit.setExperience(2, -1)
												pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
												pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS1"), True)

								# Einheiten erstellen
								LNewUnits = [
										gc.getInfoTypeForString("UNIT_TRIARII"),
										gc.getInfoTypeForString("UNIT_PRINCIPES"),
										gc.getInfoTypeForString("UNIT_PRINCIPES"),
										gc.getInfoTypeForString("UNIT_HASTATI"),
										gc.getInfoTypeForString("UNIT_HASTATI"),
										gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
										gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME")
								]
								for i in LNewUnits:
										pUnit = gc.getPlayer(iRome).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)

								pUnit = gc.getPlayer(iRome).initUnit(gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"), Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
								pUnit.setName("Publius Cornelius Scipio")

								# Meldung an den Spieler
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_15", ("",)))
								popupInfo.addPopup(iPlayer)
								CyCamera().JustLookAtPlot(Landungsplot)

		# Schlacht am Metaurus (Ost-Italien) Hasdrubal Barca
		# karthag. Einheiten in Italien
		# Stadt (Ariminum) = römisch + Rom und Karthago im Krieg
		if iGameTurn == 150:
				if iPlayer == iRome:
						pPlot = CyMap().plot(54, 62)  # Florentia
						if pPlot.getOwner() == iRome and gc.getTeam(gc.getPlayer(iRome).getTeam()).isAtWar(gc.getPlayer(iCarthago).getTeam()):

								# Plot für die Landungseinheiten
								lPlots = [
										CyMap().plot(55, 64),
										CyMap().plot(54, 64),
										CyMap().plot(55, 63)
								]
								Landungsplot = getRandomPlot(lPlots)

								# Einheiten erstellen
								LNewUnits = [
										gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER"),
										gc.getInfoTypeForString("UNIT_SPEARMAN_CARTHAGE"),
										gc.getInfoTypeForString("UNIT_SPEARMAN_CARTHAGE"),
										gc.getInfoTypeForString("UNIT_SCHILDTRAEGER_IBERIA"),
										gc.getInfoTypeForString("UNIT_SCHILDTRAEGER_IBERIA"),
										gc.getInfoTypeForString("UNIT_CELTIC_GALLIC_WARRIOR"),
										gc.getInfoTypeForString("UNIT_CELTIC_GALLIC_WARRIOR")
								]

								for i in LNewUnits:
										pUnit = gc.getPlayer(iCarthago).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT2"), True)

								pUnit = gc.getPlayer(iCarthago).initUnit(gc.getInfoTypeForString("UNIT_MOUNTED_SACRED_BAND_CARTHAGE"),
																												 Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT2"), True)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADER"), True)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_LEADERSHIP"), True)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_FLANKING1"), True)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_FORM_FLANKENSCHUTZ"), True)
								pUnit.setName("Hasdrubal Barca")

								# Meldung an den Spieler
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_17", ("",)))
								popupInfo.addPopup(iPlayer)
								CyCamera().JustLookAtPlot(Landungsplot)

		# Rom landet in Afrika bei Utica
		if iGameTurn == 183:
				if iPlayer == iCarthago and not gc.getPlayer(iRome).isHuman():
						if gc.getTeam(gc.getPlayer(iCarthago).getTeam()).isAtWar(gc.getPlayer(iRome).getTeam()):

								# Plot für die Landungseinheiten
								lPlots = [
										CyMap().plot(40, 40),
										CyMap().plot(41, 40),
										CyMap().plot(41, 41)
								]
								Landungsplot = getRandomPlot(lPlots)
								# Plot für die Schiffe
								lPlots = [
										CyMap().plot(40, 42),
										CyMap().plot(41, 42),
										CyMap().plot(42, 42)
								]
								Schiffsplot = getRandomPlot(lPlots)

								# Schiffe erstellen
								LNewUnits = [
										gc.getInfoTypeForString("UNIT_QUADRIREME"),
										gc.getInfoTypeForString("UNIT_TRIREME")
								]
								for i in LNewUnits:
										for _ in range(2):
												pUnit = gc.getPlayer(iRome).initUnit(i, Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
												pUnit.setExperience(2, -1)
												pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
												pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS1"), True)

								# Einheiten erstellen
								LNewUnits = [
										gc.getInfoTypeForString("UNIT_TRIARII"),
										gc.getInfoTypeForString("UNIT_PRINCIPES"),
										gc.getInfoTypeForString("UNIT_PRINCIPES"),
										gc.getInfoTypeForString("UNIT_HASTATI"),
										gc.getInfoTypeForString("UNIT_HASTATI"),
										gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
										gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME")
								]
								for i in LNewUnits:
										pUnit = gc.getPlayer(iRome).initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)

								# Meldung an den Spieler
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_2NDPUNICWAR_20", ("",)))
								popupInfo.addPopup(iPlayer)
								CyCamera().JustLookAtPlot(Landungsplot)


def onCityAcquired(pCity, iNewOwner):
		iCivRome = 0  # Capital: Rome
		iCivCarthage = 1  # Capital: Carthage
		sData = CvUtil.getScriptData(pCity.plot(), ["t"])
		if sData == "Rome" and iNewOwner == iCivCarthage or sData == "Carthage" and iNewOwner == iCivRome:

				# PAE Movie
				if gc.getPlayer(iNewOwner).isHuman():
						if iNewOwner == iCivRome:
								iMovie = 1
						else:
								iMovie = 2
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
						popupInfo.setData1(iMovie)  # dynamicID in CvWonderMovieScreen
						popupInfo.setData2(0)  # fix pCity.getID()
						popupInfo.setData3(3)  # fix PAE Movie ID for victory movies
						popupInfo.setText(u"showWonderMovie")
						popupInfo.addPopup(iNewOwner)

				gc.getGame().setWinner(gc.getPlayer(iNewOwner).getTeam(), 2)


def getRandomPlot(lPlots):

		# Zufallsplot vorher auswählen, falls überall Einheiten drauf stehn -> jumpToNearestValidPlot
		iRand = CvUtil.myRandom(len(lPlots), "")
		Notfallsplot = lPlots[iRand]

		# Einen Plot aus den vorgegebenen Plots raussuchen, wo keine Einheiten drauf stehen
		lNewPlots = []
		for p in lPlots:
				if p.getNumUnits() == 0:
						lNewPlots.append(p)

		if len(lNewPlots) == 0:
				for i in range(Notfallsplot.getNumUnits()):
						Notfallsplot.getUnit(i).jumpToNearestValidPlot()
						return Notfallsplot
		else:
				iRand = CvUtil.myRandom(len(lNewPlots), "")
				return lNewPlots[iRand]
