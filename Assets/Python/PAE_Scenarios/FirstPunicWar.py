# Scenario FirstPunicWar by Keinpferd

# Imports
from CvPythonExtensions import (CyGlobalContext, DirectionTypes, UnitAITypes,
																CyMap, CyPopupInfo, ButtonPopupTypes,
																CyTranslator, CyInterface, ColorTypes, CyCamera)
# import CvEventInterface
import CvUtil
# import PyHelpers
# import CvCameraControls
import PAE_Unit
import PAE_City

# Defines
gc = CyGlobalContext()


def onEndPlayerTurn(iPlayer, iGameTurn):

		iCivRome = 0
		iCivCarthage = 1
		iCivMessana = 4
		iCivSyrakus = 12

		# Runde 1: In der ersten Runde soll sich Messana an Rom als Vasall anbieten
		if iGameTurn == 0:

				if iPlayer == iCivMessana:

						iTeamRome = gc.getPlayer(iCivRome).getTeam()
						iTeamMessana = gc.getPlayer(iCivMessana).getTeam()
						pTeamMessana = gc.getTeam(iTeamMessana)
						if not pTeamMessana.isVassal(iTeamRome):

								gc.getTeam(iTeamRome).assignVassal(iTeamMessana, 0)  # Vassal, but no surrender

								# Meldungen an die Spieler
								iRange = gc.getMAX_PLAYERS()
								for iLoopPlayer in range(iRange):
										pPlayer = gc.getPlayer(iLoopPlayer)
										if pPlayer.isHuman():
												# Meldung Karthago Human
												if iLoopPlayer == iCivCarthage:
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSANA_PLAYER_CARTHAGE", ("",)))
														popupInfo.addPopup(iLoopPlayer)
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(CyTranslator().getText("TXT_KEY_WAR_PLAYER_CARTHAGE", ("",)))
														popupInfo.addPopup(iLoopPlayer)
												elif iLoopPlayer == iCivRome:
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSANA_PLAYER_ALL", ("",)))
														popupInfo.addPopup(iLoopPlayer)
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(CyTranslator().getText("TXT_KEY_WAR_PLAYER_ROME", ("",)))
														popupInfo.addPopup(iLoopPlayer)
												# Meldung an alle Humans
												else:
														popupInfo = CyPopupInfo()
														popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
														popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSANA_PLAYER_ALL", ("",)))
														popupInfo.addPopup(iLoopPlayer)

		# Runde 2: 264BC Im Kampf um die Vorherrschaft auf Sizilien gerät Syrakus zwischen die Fronten von Rom und Karthago.
		# HI Syrakus
		# Bedingung Syrakus mit Rom im Krieg
		elif iGameTurn == 2:
				pPlot = CyMap().plot(86, 36)
				pSyrakus = gc.getPlayer(iCivSyrakus)
				if iPlayer == iCivSyrakus and pSyrakus.isHuman() and gc.getTeam(iCivSyrakus).isAtWar(iCivRome):
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"),
								gc.getInfoTypeForString("UNIT_HOPLIT"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_MACEDON"),
								gc.getInfoTypeForString("UNIT_AUXILIAR_HORSE")
						]
						for i in LNewUnits:
								for _ in range(3):
										pUnit = pSyrakus.initUnit(i, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)

						pUnit = pSyrakus.initUnit(gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						PAE_Unit.initSupply(pUnit)

						# Meldung
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN2", ("",)))
						popupInfo.addPopup(iPlayer)
						CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN2", ("", )), None, 2,
																		 "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(2), pPlot.getX(), pPlot.getY(), True, True)
						CyInterface().doPing(pPlot.getX(), pPlot.getY(), iPlayer)
						CyCamera().JustLookAtPlot(pPlot)

		# Runde 3: Im Kampf gegen Rom sendet unser makedonischer Freund Alexander II Männer und Schiffe für den Freiheitskampf der Griechen auf Sizilien.
		# HI Syrakus
		elif iGameTurn == 3:
				pSyrakus = gc.getPlayer(iCivSyrakus)
				if iPlayer == iCivSyrakus and pSyrakus.isHuman():
						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(84, 37),
								CyMap().plot(84, 38)
						]
						Landungsplot = getRandomPlot(lPlots)

						# Plot für die Schiffe
						lPlots = [
								CyMap().plot(85, 38)
						]
						Schiffsplot = getRandomPlot(lPlots)

						# Einheiten erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"),
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"),
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"),
								gc.getInfoTypeForString("UNIT_PEZHETAIROI"),
								gc.getInfoTypeForString("UNIT_PEZHETAIROI"),
								gc.getInfoTypeForString("UNIT_PEZHETAIROI"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_MACEDON"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_MACEDON"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_MACEDON"),
								gc.getInfoTypeForString("UNIT_AUXILIAR_HORSE")
						]
						for i in LNewUnits:
								pUnit = pSyrakus.initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						# Schiffe erstellen
						for _ in range(3):
								pUnit = pSyrakus.initUnit(gc.getInfoTypeForString("UNIT_TRIREME"), Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTHWEST)
								pUnit.setExperience(2, -1)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
								pUnit.finishMoves()

						# Meldung
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN3", ("",)))
						popupInfo.addPopup(iPlayer)
						CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN3", ("", )), None, 2,
																		 "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(2), Landungsplot.getX(), Landungsplot.getY(), True, True)
						CyCamera().JustLookAtPlot(Landungsplot)

		# Im Jahr 261 BC beschließt der Senat von Rom den Bau einer Kriegsflotte auf Basis eines gekenterten punischen Schiffes.
		# Mit Hilfe von Enterbrücken und größeren Schiffsbesatzungen erringen die Römer einen spektakulären Seesieg am Kap Economus (256 BC)."
		elif iGameTurn == 50 and (iPlayer == iCivRome or iPlayer == iCivCarthage):
				pPlot = CyMap().plot(59, 57)  # City: Antium

				if iPlayer == iCivRome and pPlot.getOwner() == iCivRome:
						pRome = gc.getPlayer(iCivRome)
						# Einheiten erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_QUADRIREME"),
								gc.getInfoTypeForString("UNIT_QUINQUEREME")
						]
						for i in LNewUnits:
								for _ in range(4):
										pUnit = pRome.initUnit(i, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS1"), True)

				if gc.getPlayer(iPlayer).isHuman():
						# Meldung
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN50", ("",)))
						popupInfo.addPopup(iPlayer)
						CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN50", ("", )), None, 2,
																		 "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(2), pPlot.getX(), pPlot.getY(), True, True)
						CyCamera().JustLookAtPlot(pPlot)

		# Konsul Lucius Cornelius Scipio landet 259 BC auf Korsika und Sardinien. Er kann die Inseln jedoch nicht dauerhaft besetzen.
		elif iGameTurn == 65 and iPlayer == iCivCarthage:
				if gc.getPlayer(iPlayer).isHuman():
						pRome = gc.getPlayer(iCivRome)

						# Landung der Römer auf Korsika
						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(46, 49),
								CyMap().plot(46, 48),
								CyMap().plot(46, 47)
						]
						Landungsplot = getRandomPlot(lPlots)

						# Plot für die Schiffe
						lPlots = [
								CyMap().plot(47, 49),
								CyMap().plot(49, 47),
								CyMap().plot(47, 47)
						]
						Schiffsplot = getRandomPlot(lPlots)

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
								pUnit = pRome.initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						# Schiffe erstellen
						for _ in range(2):
								pUnit = pRome.initUnit(gc.getInfoTypeForString("UNIT_QUADRIREME"), Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTHWEST)
								pUnit.setExperience(2, -1)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS1"), True)

						# Ping
						CyInterface().doPing(Landungsplot.getX(), Landungsplot.getY(), iPlayer)

						# Landung der Römer auf Sizilien
						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(48, 44),
								CyMap().plot(48, 45),
								CyMap().plot(49, 44),
								CyMap().plot(47, 45)
						]
						Landungsplot = getRandomPlot(lPlots)

						# Plot für die Schiffe
						lPlots = [
								CyMap().plot(49, 45),
								CyMap().plot(49, 46),
								CyMap().plot(48, 46),
								CyMap().plot(47, 46)
						]
						Schiffsplot = getRandomPlot(lPlots)

						# Einheiten erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_TRIARII"),
								gc.getInfoTypeForString("UNIT_TRIARII"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_EQUITES"),
								gc.getInfoTypeForString("UNIT_EQUITES"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM")
						]
						for i in LNewUnits:
								pUnit = pRome.initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						pUnit = pRome.initUnit(gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"), Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						PAE_Unit.initSupply(pUnit)

						pUnit = pRome.initUnit(gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"), Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pUnit.setExperience(2, -1)
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
						pUnit.setName("Lucius Cornelius Scipio")

						# Schiffe erstellen
						for _ in range(5):
								pUnit = pRome.initUnit(gc.getInfoTypeForString("UNIT_QUADRIREME"), Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTHWEST)
								pUnit.setExperience(2, -1)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS1"), True)

						# Ping
						CyInterface().doPing(Landungsplot.getX(), Landungsplot.getY(), iPlayer)

						pPlot = Landungsplot
						# Meldung
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN65", ("",)))
						popupInfo.addPopup(iPlayer)
						CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN65", ("", )), None, 2,
																		 "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(2), pPlot.getX(), pPlot.getY(), True, True)
						CyCamera().JustLookAtPlot(pPlot)

		# Numideraufstand
		# Die Schwäche von Karthago ausnutzend, erheben sich die lokalen Numiderstämme zu einem Aufstand um die Vorherrschaft der Punier abzuschütteln.
		elif iGameTurn == 75 and iPlayer == iCivCarthage:
				if gc.getPlayer(iPlayer).isHuman():
						pBarbs = gc.getPlayer(gc.getBARBARIAN_PLAYER())
						# 4x Rebellen
						for i in range(4):
								if i == 0:
										lPlots = [
												CyMap().plot(71, 13),
												CyMap().plot(71, 12),
												CyMap().plot(70, 12),
												CyMap().plot(70, 13)
										]
								elif i == 1:
										lPlots = [
												CyMap().plot(65, 15),
												CyMap().plot(66, 15),
												CyMap().plot(65, 14),
												CyMap().plot(64, 13)
										]
								elif i == 2:
										lPlots = [
												CyMap().plot(54, 14),
												CyMap().plot(54, 15),
												CyMap().plot(53, 13)
										]
								elif i == 3:
										lPlots = [
												CyMap().plot(35, 4),
												CyMap().plot(36, 4),
												CyMap().plot(37, 4),
												CyMap().plot(38, 4)
										]
								pPlot = getRandomPlot(lPlots)
								# Einheiten erstellen
								LNewUnits = [
										gc.getInfoTypeForString("UNIT_HORSEMAN_NUMIDIA"),
										gc.getInfoTypeForString("UNIT_KRUMMSAEBEL"),
										gc.getInfoTypeForString("UNIT_SKIRMISHER"),
										gc.getInfoTypeForString("UNIT_REBELL")
								]
								for i in LNewUnits:
										pUnit = pBarbs.initUnit(i, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)

						# Meldung
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN75", ("",)))
						popupInfo.addPopup(iPlayer)
						CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN75", ("", )), None, 2,
																		 "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(2), pPlot.getX(), pPlot.getY(), True, True)
						CyCamera().JustLookAtPlot(pPlot)

		# Landung von Regulus in Nordafrika  (2 Legionen)
		# Im Jahr 256 BC landet der Konsul Marcus Atilius Regulus bei Aspis in Nordafrika und bedroht Karthago direkt.
		# Mit Hilfe des Söldnerführers Xanthippos gelingt es den Puniern die römische Invasion zurück zu schlagen (Schlacht von Tunis 255 BC).
		elif iGameTurn == 110 and iPlayer == iCivCarthage:
				if gc.getPlayer(iPlayer).isHuman():
						pRome = gc.getPlayer(iCivRome)

						# Landung der Römer vor Karthago
						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(72, 22),
								CyMap().plot(73, 22),
								CyMap().plot(72, 23)
						]
						Landungsplot = getRandomPlot(lPlots)

						# Plot für die Schiffe
						lPlots = [
								CyMap().plot(73, 23),
								CyMap().plot(72, 24),
								CyMap().plot(71, 24)
						]
						Schiffsplot = getRandomPlot(lPlots)

						# Einheiten erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_TRIARII"),
								gc.getInfoTypeForString("UNIT_TRIARII"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_PRINCIPES"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_HASTATI"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER_ROME"),
								gc.getInfoTypeForString("UNIT_EQUITES"),
								gc.getInfoTypeForString("UNIT_EQUITES"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM")
						]
						for i in LNewUnits:
								pUnit = pRome.initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						pUnit = pRome.initUnit(gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"), Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						PAE_Unit.initSupply(pUnit)

						pUnit = pRome.initUnit(gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"), Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pUnit.setExperience(2, -1)
						pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
						pUnit.setName("Marcus Atilius Regulus")

						# Schiffe erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_TRIREME"),
								gc.getInfoTypeForString("UNIT_BIREME"),
								gc.getInfoTypeForString("UNIT_QUINQUEREME")
						]
						for i in LNewUnits:
								for _ in range(2):
										pUnit = pRome.initUnit(i, Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS1"), True)

						pPlot = Landungsplot
						# Meldung
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN110", ("",)))
						popupInfo.addPopup(iPlayer)
						CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN110", ("", )), None,
																		 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(2), pPlot.getX(), pPlot.getY(), True, True)
						CyCamera().JustLookAtPlot(pPlot)

		# Landung der Punier bei Agrigent
		# Bedingung: Agrigent = Römisch
		# Im Jahr 251 BC gelingt Karthago die Rückeroberung von Agrigent
		elif iGameTurn == 160 and iPlayer == iCivRome:
				pPlot = CyMap().plot(77, 36)  # City: Agrigentum
				if pPlot.getOwner() == iCivRome and gc.getPlayer(iPlayer).isHuman():
						pCarthage = gc.getPlayer(iCivCarthage)

						# Landung der Karthager vor Agrigentum
						# Plot für die Landungseinheiten
						lPlots = [
								CyMap().plot(76, 36),
								CyMap().plot(76, 35),
								CyMap().plot(78, 35),
								CyMap().plot(78, 36)
						]
						Landungsplot = getRandomPlot(lPlots)

						# Plot für die Schiffe
						lPlots = [
								CyMap().plot(77, 35),
								CyMap().plot(76, 34),
								CyMap().plot(77, 34),
								CyMap().plot(78, 34)
						]
						Schiffsplot = getRandomPlot(lPlots)

						# Einheiten erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD"),
								gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD"),
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER_IBERIA"),
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER_IBERIA"),
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER_IBERIA"),
								gc.getInfoTypeForString("UNIT_SCHILDTRAEGER_IBERIA"),
								gc.getInfoTypeForString("UNIT_SPEARMAN_CARTHAGE"),
								gc.getInfoTypeForString("UNIT_SPEARMAN_CARTHAGE"),
								gc.getInfoTypeForString("UNIT_SPEARMAN_CARTHAGE"),
								gc.getInfoTypeForString("UNIT_SPEARMAN_CARTHAGE"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER"),
								gc.getInfoTypeForString("UNIT_SKIRMISHER"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM"),
								gc.getInfoTypeForString("UNIT_BATTERING_RAM")
						]
						for i in LNewUnits:
								pUnit = pCarthage.initUnit(i, Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)

						pUnit = pCarthage.initUnit(gc.getInfoTypeForString("UNIT_SUPPLY_WAGON"), Landungsplot.getX(), Landungsplot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						PAE_Unit.initSupply(pUnit)

						# Schiffe erstellen
						LNewUnits = [
								gc.getInfoTypeForString("UNIT_QUINQUEREME"),
								gc.getInfoTypeForString("UNIT_QUADRIREME"),
								gc.getInfoTypeForString("UNIT_TRIREME")
						]
						for i in LNewUnits:
								for _ in range(2):
										pUnit = pCarthage.initUnit(i, Schiffsplot.getX(), Schiffsplot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)
										pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)

						pPlot = Landungsplot
						# Meldung
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN160", ("",)))
						popupInfo.addPopup(iPlayer)
						CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN160", ("", )), None,
																		 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(2), pPlot.getX(), pPlot.getY(), True, True)
						CyCamera().JustLookAtPlot(pPlot)

		# Privater Kaperkrieg vor den Küsten Karthagos
		# Nach der verlorenen Seeschlacht von Drepana 249 v.Chr und schweren Verlusten in Stürmen (Kamarina, 255 v.Chr.) stellt Rom sein Flottenprogramm ein,
		# ermuntert aber wohlhabende Römer zu privaten Kaperfahrten vor den Küsten der Punier.
		elif iGameTurn == 185 and iPlayer == iCivCarthage:
				if gc.getPlayer(iPlayer).isHuman():
						pRome = gc.getPlayer(iCivRome)

						# Fixe Plots für die Piraten
						lPlots = [
								CyMap().plot(43, 44),
								CyMap().plot(54, 31),
								CyMap().plot(82, 28),
								CyMap().plot(73, 17),
								CyMap().plot(66, 24),
								CyMap().plot(62, 23),
								CyMap().plot(58, 21),
								CyMap().plot(63, 24)
						]
						# 8 röm. Piraten-Trieren vor Nordafrika und Sardinien
						for p in lPlots:
								for i in range(p.getNumUnits()):
										p.getUnit(i).jumpToNearestValidPlot()
								pUnit = pRome.initUnit(gc.getInfoTypeForString("UNIT_PIRAT_TRIREME"), p.getX(), p.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)
								pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)

						# Meldung
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN185", ("",)))
						popupInfo.addPopup(iPlayer)

		# Plünderung der ital. Südküste
		# Nachdem der Krieg zu Land und zur See stagniert, unternimmt die punische Flotte Plünderungszüge an der italienischen Südküste.
		elif iGameTurn == 195 and iPlayer == iCivRome:
				pPlot = CyMap().plot(77, 36)  # City: Agrigentum
				if pPlot.getOwner() == iCivRome and gc.getPlayer(iPlayer).isHuman():
						pCarthage = gc.getPlayer(iCivCarthage)

						# Fixe Plots für die Schiffe
						lPlots = [
								CyMap().plot(87, 45),
								CyMap().plot(84, 58),
								CyMap().plot(81, 61),
								CyMap().plot(77, 54),
								CyMap().plot(69, 56),
								CyMap().plot(75, 68)
						]
						# 6 karth. Triere inkl. 3 Einheiten vor Süditalien
						for p in lPlots:
								for i in range(p.getNumUnits()):
										p.getUnit(i).jumpToNearestValidPlot()
								pShip = pCarthage.initUnit(gc.getInfoTypeForString("UNIT_TRIREME"), p.getX(), p.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
								pShip.setExperience(2, -1)
								pUnit = pCarthage.initUnit(gc.getInfoTypeForString("UNIT_SCHILDTRAEGER_IBERIA"), p.getX(), p.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)
								pUnit.setTransportUnit(pShip)
								pUnit = pCarthage.initUnit(gc.getInfoTypeForString("UNIT_SPEARMAN_CARTHAGE"), p.getX(), p.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)
								pUnit.setTransportUnit(pShip)
								pUnit = pCarthage.initUnit(gc.getInfoTypeForString("UNIT_SKIRMISHER"), p.getX(), p.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
								pUnit.setExperience(2, -1)
								pUnit.setTransportUnit(pShip)

						# Meldung
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN195", ("",)))
						popupInfo.addPopup(iPlayer)

		# Flottenbau, Bed. Antium = röm.
		# In einem letzten Kraftakt baut Rom eine neue Kriegsflotte um den Konflikt nach 23 Jahren endlich zu beenden.
		# Nach dem römischen Seesieg bei den Ägadischen Inseln (241 BC) muß Karthago um Frieden bitten.
		elif iGameTurn == 265 and (iPlayer == iCivRome or iPlayer == iCivCarthage):
				pPlot = CyMap().plot(59, 57)  # City: Antium
				if pPlot.getOwner() == iCivRome:
						if iPlayer == iCivRome:
								# Schiffe erstellen
								LNewUnits = [
										gc.getInfoTypeForString("UNIT_QUINQUEREME"),
										gc.getInfoTypeForString("UNIT_QUADRIREME")
								]
								for i in LNewUnits:
										for _ in range(3):
												pUnit = pCarthage.initUnit(i, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ASSAULT_SEA, DirectionTypes.DIRECTION_SOUTH)
												pUnit.setExperience(2, -1)
												pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMBAT1"), True)
												pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CORVUS1"), True)

						# Meldung
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN265", ("",)))
						popupInfo.addPopup(iPlayer)
						CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN265", ("", )), None,
																		 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(2), pPlot.getX(), pPlot.getY(), True, True)
						CyCamera().JustLookAtPlot(pPlot)

		# Die Stadt Falerii rebelliert gegen Rom
		# Bedingung: Falerii = Römisch
		# Die Einwohner von der ehemals etruskischen Stadt Falerii erheben sich im Jahr 240 BC gegen die römische Vorherrschaft
		elif iGameTurn == 280 and iPlayer == iCivRome:
				pPlot = CyMap().plot(54, 61)  # City: Faleria
				if pPlot.getOwner() == iCivRome and gc.getPlayer(iPlayer).isHuman():
						if pPlot.isCity():

								# Stadt wird barbarisch + Einheiten (4-6)
								PAE_City.doRenegadeCity(pPlot.getPlotCity(), gc.getBARBARIAN_PLAYER(), None)

								pBarbs = gc.getPlayer(gc.getBARBARIAN_PLAYER())

								LNewUnits = [
										gc.getInfoTypeForString("UNIT_REBELL"),
										gc.getInfoTypeForString("UNIT_REFLEX_ARCHER"),
										gc.getInfoTypeForString("UNIT_CELERES")
								]

								# Fix die obigen Einheiten
								for i in LNewUnits:
										pUnit = pBarbs.initUnit(i, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)

								# zusätzliche Einheiten insg. 4-6
								iNum = 1 + CvUtil.myRandom(3, "")
								for _ in range(iNum):
										iRand = CvUtil.myRandom(len(LNewUnits), "")
										pUnit = pBarbs.initUnit(LNewUnits[iRand], pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
										pUnit.setExperience(2, -1)

								# Meldung
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN280", ("",)))
								popupInfo.addPopup(iPlayer)
								CyInterface().addMessage(iPlayer, True, 12, CyTranslator().getText("TXT_KEY_MESSAGE_1STPUNICWAR_TURN280", ("", )), None,
																				 2, "Art/Interface/Buttons/General/button_alert_new.dds", ColorTypes(2), pPlot.getX(), pPlot.getY(), True, True)
								CyCamera().JustLookAtPlot(pPlot)


def onCombatResult(pWinner, pLoser):
		if pLoser.getUnitType() == gc.getInfoTypeForString("UNIT_QUADRIREME"):
				if gc.getPlayer(pWinner.getOwner()).getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ROME"):
						iTech = gc.getInfoTypeForString("TECH_WARSHIPS")
						iTeam = gc.getPlayer(pWinner.getOwner()).getTeam()
						pTeam = gc.getTeam(iTeam)
						if not pTeam.isHasTech(iTech):
								pTeam.setHasTech(iTech, 1, pWinner.getOwner(), 0, 1)


def onCityAcquired(pCity, iNewOwner):
		iCivRome = 0  # Capital: Rome
		# iCivCarthage = 1  # Capital: Carthage
		sData = CvUtil.getScriptData(pCity.plot(), ["t"])
		if sData == "Rome" and iNewOwner != iCivRome or sData == "Carthage" and iNewOwner == iCivRome:

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
