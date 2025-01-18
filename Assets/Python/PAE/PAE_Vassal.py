# Imports
from CvPythonExtensions import (CyGlobalContext, CyPopupInfo, ButtonPopupTypes,
																CyTranslator, CyMessageControl, CyAudioGame,
																CyCamera, CyInterface, UnitAITypes, ColorTypes,
																DirectionTypes)
# import CvEventInterface
import CvUtil
import PAE_City
import PAE_Unit

# Defines
gc = CyGlobalContext()


def onCityAcquired(pCity, iNewOwner, iPreviousOwner):
		pWinner = gc.getPlayer(iNewOwner)
		iWinnerTeam = pWinner.getTeam()
		pWinnerTeam = gc.getTeam(iWinnerTeam)

		# Der Gewinner muss die TECH Vassallentum erforscht haben
		iTechVasallentum = gc.getInfoTypeForString("TECH_VASALLENTUM")
		if pWinnerTeam.isHasTech(iTechVasallentum) and iNewOwner != gc.getBARBARIAN_PLAYER():

				pLoser = gc.getPlayer(iPreviousOwner)
				iLoserTeam = pLoser.getTeam()
				pLoserTeam = gc.getTeam(iLoserTeam)
				iLoserPowerWithVassals = pLoserTeam.getPower(True)  # mit Vasallen
				iWinnerPower = pWinnerTeam.getPower(True)  # mit Vasallen

				# ***TEST***
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Winner Power",iWinnerPower)), None, 2, None, ColorTypes(10), 0, 0, False, False)
				#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Loser Power",iLoserPowerWithVassals)), None, 2, None, ColorTypes(10), 0, 0, False, False)

				# Hegemon verliert eine Stadt, Vasallen werden gecheckt
				iRange = gc.getMAX_PLAYERS()
				for iVassal in range(iRange):
						pPlayer = gc.getPlayer(iVassal)
						if pPlayer.isAlive():
								iTeam = pPlayer.getTeam()
								pTeam = gc.getTeam(iTeam)
								if pTeam.isVassal(iLoserTeam):
										iVassalPower = pTeam.getPower(True)

										iLoserPower = iLoserPowerWithVassals - iVassalPower

										# ***TEST***
										#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Hegemon Power",iLoserPower)), None, 2, None, ColorTypes(10), 0, 0, False, False)
										#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Vasall Power",iVassalPower)), None, 2, None, ColorTypes(10), 0, 0, False, False)

										# Wenn Vasall gemeinsam mit dem Feind staerker als Hegemon ist
										# weiters trotzdem loyal zum Hegemon 1:3
										if iVassalPower + iWinnerPower > iLoserPower and (CvUtil.myRandom(30, "weiters trotzdem loyal zum Hegemon") + pPlayer.AI_getAttitude(iPreviousOwner) - pPlayer.AI_getAttitude(iNewOwner)) < 10:

												# ***TEST***
												#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Vassal interaction",1)), None, 2, None, ColorTypes(10), 0, 0, False, False)

												# Initials
												iWinnerGold = pWinner.getGold()

												# 1/3 Gold, aber mind. > 300
												if iVassalPower > iLoserPower - iLoserPower/3 + 1:
														fGold = 0.33
														iMinGold = 300

												# 1/2 Gold, aber mind. > 400
												elif iVassalPower > iLoserPower / 2:
														fGold = 0.5
														iMinGold = 400

												# 2/3 Gold, aber mind. > 500
												else:
														fGold = 0.66
														iMinGold = 500

												# HI Vassal
												# ------------------------------
												if pPlayer.isHuman():
														# Wir sind staerker als der Hegemon
														if iVassalPower > iLoserPower:
																popupInfo = CyPopupInfo()
																popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
																popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_09", (pLoser.getCivilizationShortDescription(0),
																									pWinner.getCivilizationShortDescription(0), pPlayer.getCivilizationAdjective(3))))
																popupInfo.setData1(iNewOwner)
																popupInfo.setData2(iPreviousOwner)
																popupInfo.setData3(iVassal)
																popupInfo.setOnClickedPythonCallback("popupVassal09")  # EntryPoints/CvScreenInterface und CvGameUtils / 688
																popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_09_YES",
																													(pLoser.getCivilizationShortDescription(0), pWinner.getCivilizationShortDescription(0))), "")
																popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_09_NO",
																													(pLoser.getCivilizationShortDescription(0), pWinner.getCivilizationShortDescription(0))), "")
																popupInfo.addPopup(iVassal)

														# Gemeinsam sind wir staerker als der Hegemon
														# HI-HI-Interaktion
														elif pWinner.isHuman() and iWinnerGold >= iMinGold:
																iBribe = int(iWinnerGold * fGold)
																if iMinGold > iBribe:
																		iBribe = iMinGold

																popupInfo = CyPopupInfo()
																popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
																if pCity == None:
																		popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_14", (
																											pPlayer.getCivilizationAdjective(3), gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDescription())))
																else:
																		popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_10", (pCity.getName(),
																											pPlayer.getCivilizationAdjective(3), gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDescription())))
																popupInfo.setData1(iNewOwner)
																popupInfo.setData2(iPreviousOwner)
																popupInfo.setData3(iVassal)
																popupInfo.setFlags(iBribe)
																popupInfo.setOnClickedPythonCallback("popupVassal10")  # EntryPoints/CvScreenInterface und CvGameUtils / 689
																popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_10_YES", (gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDescription(), iBribe)), "")
																popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_10_NO", (gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDescription(),)), "")
																popupInfo.addPopup(iNewOwner)

														# HI-KI Interaktion
														elif iWinnerGold >= iMinGold:
																iBribe = int(iWinnerGold * fGold)
																if iMinGold > iBribe:
																		iBribe = iMinGold

																# KI bietet zu 50% ein Angebot an
																if CvUtil.myRandom(2, "KI bietet zu 50% ein Angebot an") < 1:
																		popupInfo = CyPopupInfo()
																		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
																		popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_11", (gc.getLeaderHeadInfo(
																				pWinner.getLeaderType()).getDescription(), iBribe, pWinner.getCivilizationShortDescription(0))))
																		popupInfo.setData1(iNewOwner)
																		popupInfo.setData2(iPreviousOwner)
																		popupInfo.setData3(iVassal)
																		popupInfo.setFlags(iBribe)
																		popupInfo.setOnClickedPythonCallback("popupVassal11")  # EntryPoints/CvScreenInterface und CvGameUtils / 690
																		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_11_YES", (gc.getLeaderHeadInfo(
																				pLoser.getLeaderType()).getDescription(), gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription())), "")
																		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_11_NO", ()), "")
																		iRand = 1 + CvUtil.myRandom(9, "TXT_KEY_POPUP_VASSAL_KILL_")
																		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_KILL_"+str(iRand), (gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(),)), "")
																		popupInfo.addPopup(iVassal)

																# Winner hat kein Interesse
																# Vasall darf entscheiden, ob er Krieg erklaert
																else:
																		popupInfo = CyPopupInfo()
																		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
																		popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_12", (gc.getLeaderHeadInfo(
																				pWinner.getLeaderType()).getDescription(), pWinner.getCivilizationAdjective(2))))
																		popupInfo.setData1(iNewOwner)
																		popupInfo.setData2(iPreviousOwner)
																		popupInfo.setData3(iVassal)
																		popupInfo.setOnClickedPythonCallback("popupVassal12")  # EntryPoints/CvScreenInterface und CvGameUtils / 691
																		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_12_YES", (gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription(),)), "")
																		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_12_NO", ()), "")
																		popupInfo.addPopup(iVassal)

														# Winner hat kein Gold
														# Vasall darf entscheiden, ob er Krieg erklaert
														else:
																popupInfo = CyPopupInfo()
																popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
																popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_13", (gc.getLeaderHeadInfo(
																		pWinner.getLeaderType()).getDescription(), pWinner.getCivilizationAdjective(2))))
																popupInfo.setData1(iNewOwner)
																popupInfo.setData2(iPreviousOwner)
																popupInfo.setData3(iVassal)
																popupInfo.setOnClickedPythonCallback("popupVassal12")  # EntryPoints/CvScreenInterface und CvGameUtils / 691
																popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_12_YES", (gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription(),)), "")
																popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_12_NO", ()), "")
																popupInfo.addPopup(iVassal)

												# ------------------------------

												# HI Winner
												# ----------------------------
												elif pWinner.isHuman():
														iBribe = int(iWinnerGold * fGold)
														if iMinGold > iBribe:
																iBribe = iMinGold

														if iWinnerGold >= iBribe:
																popupInfo = CyPopupInfo()
																popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
																popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_08", (pPlayer.getCivilizationShortDescription(0),
																									gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription(), iBribe)))
																popupInfo.setData1(iNewOwner)
																popupInfo.setData2(iPreviousOwner)
																popupInfo.setData3(iVassal)
																popupInfo.setFlags(iBribe)
																popupInfo.setOnClickedPythonCallback("popupVassal08")  # EntryPoints/CvScreenInterface und CvGameUtils / 687
																popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_08_YES", (pLoser.getCivilizationShortDescription(0), iBribe)), "")
																popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_08_NO", ()), "")
																popupInfo.addPopup(iNewOwner)

												# KI Vassal
												# ------------------------------
												else:
														bDeclareWar = False
														if iVassalPower > iLoserPower:
																# 2/3 Chance, dass Vasall dem Hegemon Krieg erklaert
																if CvUtil.myRandom(3, "2/3 Chance, dass Vasall dem Hegemon Krieg erklaert") < 2:
																		bDeclareWar = True

														# KI-KI-Interaktion
														# Winner hat mehr als das erforderte Gold, Akzeptanz: Winner: 50%, Loser: 100%
														if not bDeclareWar and iMinGold <= iWinnerGold * fGold:
																if CvUtil.myRandom(2, "Winner hat mehr als das erforderte Gold") < 1:
																		bDeclareWar = True
																		pPlayer.changeGold(int(iWinnerGold * fGold))
																		pWinner.changeGold(int(iWinnerGold * fGold) * (-1))

														# Winner hat das mindest geforderte Gold, Akzeptanz: Winner: 100%, Loser: 50%
														if not bDeclareWar and iWinnerGold >= iMinGold:
																if CvUtil.myRandom(2, "Winner hat das mindest geforderte Gold") < 1:
																		bDeclareWar = True
																		pPlayer.changeGold(iMinGold)
																		pWinner.changeGold(iMinGold * (-1))

														if bDeclareWar:
																VassalUnsetHegemon(iVassal)
																pTeam.declareWar(iLoserTeam, 0, 4)
																if pWinner.isHuman():
																		popupInfo = CyPopupInfo()
																		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
																		popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_09_1", (pLoser.getCivilizationAdjective(3),
																											gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDescription(),)))
																		popupInfo.addPopup(iNewOwner)

				# Hegemon verliert Stadt Ende -----

				# ------------
				# Wenn man selbst eine Stadt verliert
				# Loser und Winner-Werte von oben
				# ------------

				# -------------------------------
				# Wird der Verlierer zum Vasall ?
				iMinimumCities = 5
				if pLoser.hasTrait(gc.getInfoTypeForString("TRAIT_AGGRESSIVE")):
						iMinimumCities = 3

				if pLoser.getNumCities() > 1:
					if not pWinnerTeam.isAVassal() and iNewOwner != gc.getBARBARIAN_PLAYER() and iPreviousOwner != gc.getBARBARIAN_PLAYER() and \
					(iLoserPowerWithVassals < iWinnerPower and pLoser.getNumCities() <= iMinimumCities or iLoserPowerWithVassals * 2 < iWinnerPower):

							# Abfrage ob man als Gewinner den Schwaecheren zum Vasall nimmt
							# HI-HI
							# pCity darf None sein
							if pWinner.isHuman() and pLoser.isHuman():
									VassalHItoHI(iNewOwner, iPreviousOwner, pCity)

							# KI bietet der HI Vasallenstatus an, 120% - 20% pro Stadt
							elif pWinner.isHuman():
									if 12 - pLoser.getNumCities() * 2 > CvUtil.myRandom(10, "KI bietet der HI Vasallenstatus an"):
											iGold = pLoser.getGold() / 2 + CvUtil.myRandom(pLoser.getGold() / 2, "iGold KI Vasall")
											iGold = int(iGold)
											popupInfo = CyPopupInfo()
											popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
											popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_01", (gc.getLeaderHeadInfo(
													pLoser.getLeaderType()).getDescription(), pLoser.getCivilizationShortDescription(0), iGold)))
											popupInfo.setData1(iNewOwner)
											popupInfo.setData2(iPreviousOwner)
											popupInfo.setData3(iGold)
											popupInfo.setFlags(0)  # to Loser
											popupInfo.setOnClickedPythonCallback("popupVassal01")  # EntryPoints/CvScreenInterface und CvGameUtils / 671
											popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_01_YES", ()), "")
											popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_01_NO", ()), "")
											iRand = 1 + CvUtil.myRandom(9, "TXT_KEY_POPUP_VASSAL_KILL_")
											popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_KILL_"+str(iRand), (gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription(),)), "")
											popupInfo.addPopup(iNewOwner)

					# HI: Abfrage ob HI als Verlierer Vasall werden will
					elif not pWinnerTeam.isAVassal() and pLoser.isHuman() and iLoserPowerWithVassals <= iWinnerPower*1.2:
							iGold = pLoser.getGold() / 2 + CvUtil.myRandom(pLoser.getGold() / 2, "iGold HI Vasall")
							iGold = int(iGold)
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							if pCity == None:
									popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_15", (gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(), iGold)))
							else:
									popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_02", (pCity.getName(), gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(), iGold)))
							popupInfo.setData1(iNewOwner)
							popupInfo.setData2(iPreviousOwner)
							popupInfo.setData3(iGold)
							popupInfo.setFlags(1)  # to Winner
							popupInfo.setOnClickedPythonCallback("popupVassal01")  # EntryPoints/CvScreenInterface und CvGameUtils / 671
							popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_02_YES", (gc.getLeaderHeadInfo(
									pWinner.getLeaderType()).getDescription(), pWinner.getCivilizationShortDescription(0))), "")
							popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_01_NO", ()), "")
							iRand = 1 + CvUtil.myRandom(9, "TXT_KEY_POPUP_VASSAL_KILL_")
							popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_KILL_"+str(iRand), (gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(),)), "")
							popupInfo.addPopup(iPreviousOwner)

	# KI-KI Vasall, 120% - 10% pro Stadt
	# PAE V Patch 4: deaktiviert
	# else:
	#   if 12 - pLoser.getNumCities() > CvUtil.myRandom(10, "KI-KI Vasall"):
	#     pWinnerTeam.assignVassal (iLoserTeam, 1) # surrender
	#     VassalHegemonGetsVassal(iPreviousOwner) # Hegemon verliert seine Vasallen
	#     iGold = pLoser.getGold() / 2 + CvUtil.myRandom(pLoser.getGold() / 2, "iGold KI-KI Vasall")
	#     pWinner.changeGold(iGold)
	#     pLoser.changeGold(iGold * (-1))

# Vasall soll seinen Hegemon verlieren


def VassalUnsetHegemon(iVassal):
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("TEST",iVassal)), None, 2, None, ColorTypes(10), 0, 0, False, False)
		pVassal = gc.getPlayer(iVassal)
		iVassalTeam = pVassal.getTeam()
		pVassalTeam = gc.getTeam(iVassalTeam)
		iRange = gc.getMAX_PLAYERS()
		for i in range(iRange):
				pPlayer = gc.getPlayer(i)
				if pPlayer.isAlive():
						iTeam = pPlayer.getTeam()
						pTeam = gc.getTeam(iTeam)
						if pVassalTeam.isVassal(iTeam):
								pTeam.freeVassal(iVassalTeam)
								pVassalTeam.setVassal(iTeam, 0, 0)  # komischerweise gehts nur so


# Hegemon verliert seine Vasallen
def VassalHegemonGetsVassal(iHegemon):
		pHegemon = gc.getPlayer(iHegemon)
		iHegemonTeam = pHegemon.getTeam()
		pHegemonTeam = gc.getTeam(iHegemonTeam)
		iRange = gc.getMAX_PLAYERS()
		for i in range(iRange):
				pPlayer = gc.getPlayer(i)
				if pPlayer.isAlive():
						iTeam = pPlayer.getTeam()
						pTeam = gc.getTeam(iTeam)
						if pTeam.isVassal(iHegemonTeam):
								#pHegemonTeam.setVassal(iTeam, 0, 0)
								pHegemonTeam.freeVassal(iTeam)
								pTeam.setVassal(iHegemonTeam, 0, 0)  # siehe VassalUnset (=ungetestet)


def VassalHItoHI(iNewOwner, iPreviousOwner, pCity):
		pLoser = gc.getPlayer(iPreviousOwner)
		iLoserTeam = pLoser.getTeam()
		pLoserTeam = gc.getTeam(iLoserTeam)
		iLoserPower = pLoserTeam.getPower(False)  # ohne Vasallen
		iLoserPowerWithVassals = pLoserTeam.getPower(True)  # mit Vasallen
		pWinner = gc.getPlayer(iNewOwner)
		iWinnerTeam = pWinner.getTeam()
		pWinnerTeam = gc.getTeam(iWinnerTeam)
		iWinnerPower = pWinnerTeam.getPower(True)  # mit Vasallen
		# HI-HI Interaktion
		# 1) Der Loser darf beginnen und sich als Vasall vorschlagen
		# 1a) Wenn negativ, dann soll Winner eine Meldung bekommen und dem Loser einen Vorschlag unterbreiten => 2
		# 1b) Der Winner darf entscheiden, ob der Vorschlag angenommen wird
		# 2) Der Loser darf entscheiden, ob er mit dem Angebot des Winners Vasall wird
		iGold1 = CvUtil.myRandom(pLoser.getGold() / 2, "iGold1 HI-HI Interaktion")
		if iGold1 < pLoser.getGold() / 4:
				iGold1 = pLoser.getGold() / 4
		iGold2 = iGold1 * 2
		iGold1 = int(iGold1)
		iGold2 = int(iGold2)
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		if iLoserPower < iWinnerPower / 2:
				szBuffer = "TXT_KEY_POPUP_VASSAL_03_A"
		elif iLoserPower < iWinnerPower - iWinnerPower / 3:
				# Gemeinsam mit unseren Vasallen
				if iLoserPower < iLoserPowerWithVassals:
						szBuffer = "TXT_KEY_POPUP_VASSAL_03_C"
				else:
						szBuffer = "TXT_KEY_POPUP_VASSAL_03_B"
		else:
				szBuffer = "TXT_KEY_POPUP_VASSAL_03_D"

		if pCity is None:
				CityName = ""
				szBuffer = "TXT_KEY_POPUP_VASSAL_03_E"
		else:
				CityName = pCity.getName()
		popupInfo.setText(CyTranslator().getText(szBuffer, (CityName, pWinner.getCivilizationAdjective(2), pWinner.getCivilizationShortDescription(0))))
		popupInfo.setData1(iNewOwner)
		popupInfo.setData2(iPreviousOwner)
		popupInfo.setData3(iGold1)
		popupInfo.setFlags(iGold2)
		popupInfo.setOnClickedPythonCallback("popupVassal03")  # EntryPoints/CvScreenInterface und CvGameUtils / 682
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_03_1", (pWinner.getCivilizationShortDescription(0), iGold1)), "")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_03_2", (pWinner.getCivilizationShortDescription(0), iGold2)), "")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_03_NO", ()), "")
		popupInfo.addPopup(iPreviousOwner)


def onModNetMessage(iData1, iData2, iData3, iData4, iData5):
	# iLoser gets Vassal of iWinner with 1/2 Gold of iLoser
		if iData1 == 671:
				do671(iData2, iData3, iData4, iData5)

		# HI-HI Interaktion Start ++++++++++++++++++++++++++++++
		# 1) Der Loser darf beginnen und sich als Vasall vorschlagen
		# 1a) Wenn negativ, dann soll Winner eine Meldung bekommen und dem Loser einen Vorschlag unterbreiten => 2
		# 1b) Der Winner darf entscheiden, ob der Vorschlag angenommen wird
		# 2) Der Loser darf entscheiden, ob er mit dem Angebot des Winners Vasall wird
		# = Net-ID , iWinner , iLoser, iGold1
		elif iData1 == 682:
				do682(iData2, iData3, iData4)

		# 1a => 2
		elif iData1 == 683:
				do683(iData2, iData3, iData4)

		# 2 => Loser entscheidet: YES: Loser wird Vasall, NO: Winner bekommt Meldung
		elif iData1 == 684:
				do684(iData2, iData3, iData4)

		# 1b Winner entscheidet: YES: Loser wird Vasall, NO: Loser bekommt Meldung
		elif iData1 == 685:
				do685(iData2, iData3, iData4)

		# Es wird nochmal entschieden
		elif iData1 == 686:
				# zur Loserauswahl
				if iData4 == 0:
						# iWinner , iLoser, pCity
						VassalHItoHI(iData2, iData3, None)
				# zur Winnerauswahl
				else:
						CyMessageControl().sendModNetMessage(682, iData1, iData2, -1, 0)

		# HI-HI Interaktion Ende +++++++++++++++++++++++++++++++++

		# Winner greift einen Hegemon an und bekommt ein positives Kriegsangebot von einem seiner Vasallen
		# Message-ID / HI - Winner / KI-Loser (Hegemon) / KI-Vasall / Bestechungsgeld
		elif iData1 == 687:
				do687(iData2, iData3, iData4, iData5)

		# HI ist Vasall eines Hegemons, der soeben eine Stadt verloren hat
		# iData5: 0=Krieg gegen Hegemon, 1=treu
		elif iData1 == 688:
				do688(iData2, iData3, iData4, iData5)

		# 1. Schritt HI-Winner und HI-Vasall
		elif iData1 == 689:
				do689(iData2, iData3, iData4, iData5)

		# HI Vasall: Kriegserklaerung an Hegemon oder Botschafterkill
		elif iData1 == 690:
				do690(iData2, iData3, iData4, iData5)

		# HI Vasall erklaert eigenmaechtig Krieg gegen Hegemon
		elif iData1 == 691:
				do691(iData2, iData3, iData4)

		# ------------------------------------------------------------

		# Vassallen entfernen oder Städte schenken (Button in der Hauptstadt)
		elif iData1 == 764:
				# iData1, iData2, ... , iData5
				# First:  764, iPlayer, -1, -1, -1
				# Second: 764, iPlayer, iVasall, iButtonID, -1
				pPlayer = gc.getPlayer(iData2)

				# Vasallen auflisten und Vasall auswählen
				if iData3 == -1:
						# Dies soll doppelte Popups in PB-Spielen vermeiden.
						if iData2 == gc.getGame().getActivePlayer():
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASALLEN_0", ()))
								popupInfo.setData1(iData2)  # iPlayer
								popupInfo.setOnClickedPythonCallback("popupVasallen")

								lVassals = getVassals(iData2)
								for iVassal in lVassals:
										iCities = gc.getPlayer(iVassal).getNumCities()
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASALLEN_1", (gc.getPlayer(iVassal).getCivilizationShortDescriptionKey(), iCities)),
																							gc.getCivilizationInfo(gc.getPlayer(iVassal).getCivilizationType()).getButton())

								# Cancel button
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ("", )), "Art/Interface/Buttons/Actions/Cancel.dds")
								popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
								popupInfo.addPopup(iData2)

				# Vasall: Entlassen oder eine Stadt schenken, wo eigene Kultur < 50%
				else:

						if iData4 == -1:
								# Dies soll doppelte Popups in PB-Spielen vermeiden.
								if iData2 == gc.getGame().getActivePlayer():

										lVassals = getVassals(iData2)

										popupInfo = CyPopupInfo()
										popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
										popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASALLEN_2", (gc.getPlayer(lVassals[iData3]).getCivilizationShortDescriptionKey(),)))
										popupInfo.setData1(iData2)  # iPlayer
										popupInfo.setData2(lVassals[iData3])  # iVasall
										popupInfo.setOnClickedPythonCallback("popupVasallen")

										# Button 0: Vasall freigeben
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASALLEN_3", ()), "Art/Interface/Buttons/Civics/civic_buerger.dds")

										# Vasall eine Stadt schenken
										lCities = getCitiesOfLowCultureLevel(iData2)
										for iCity in lCities:
												pCity = gc.getPlayer(iData2).getCity(iCity)
												iCulture = pCity.plot().calculateTeamCulturePercent(pPlayer.getTeam())
												popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASALLEN_4", (pCity.getName(), iCulture)), PAE_City.getCityStatus(None, iData2, iCity, True))

										# Cancel button
										popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ACTION_CANCEL", ("", )), "Art/Interface/Buttons/Actions/Cancel.dds")
										popupInfo.setFlags(popupInfo.getNumPythonButtons()-1)
										popupInfo.addPopup(iData2)

						# Vasall freilassen
						elif iData4 == 0:
								#lVassals = getVassals(iData2)
								VassalUnsetHegemon(iData3)
								gc.getPlayer(iData3).AI_changeAttitudeExtra(iData2, 2)

								if iData2 == gc.getGame().getActivePlayer():
										CyAudioGame().Play2DSound("AS2D_WELOVEKING")
						# Stadt schenken
						elif iData4 < iData5:
								lCities = getCitiesOfLowCultureLevel(iData2)
								pCity = pPlayer.getCity(lCities[iData4-1])  # iData4 - 1, weil buttonId 0 die Freilassung ist
								pPlot = pCity.plot()
								doGiveCity2Vassal(pCity, iData3)
								gc.getPlayer(iData3).AI_changeAttitudeExtra(iData2, 1)

								if iData2 == gc.getGame().getActivePlayer():
										CyCamera().JustLookAtPlot(pPlot)
										CyAudioGame().Play2DSound("AS2D_WELOVEKING")


def do671(iWinner, iLoser, iGold, iData5):

		pWinner = gc.getPlayer(iWinner)
		pLoser = gc.getPlayer(iLoser)
		iWinnerTeam = pWinner.getTeam()
		pWinnerTeam = gc.getTeam(iWinnerTeam)
		iLoserTeam = pLoser.getTeam()
		pLoserTeam = gc.getTeam(iLoserTeam)

		# Botschafter Kill
		# Verschlechterung der Beziehungen um -1
		# Verbesserung der Beziehungen mit jenen, die mit diesem im Krieg sind um +1
		if iGold == -1:
				# Verlierer bekommt Absage
				if iData5 == 0:
						# Verlierer bekommt -1 zum Gewinner
						pLoser.AI_changeAttitudeExtra(iWinner, -1)
						# Alle, die mit dem Verlierer im Krieg sind, bekommen zum Gewinner +1
						# ausser die Vasallen des Gewinners
						iRange = gc.getMAX_PLAYERS()
						for i in range(iRange):
								if gc.getPlayer(i).isAlive():
										iTeam = gc.getPlayer(i).getTeam()
										if pLoserTeam.isAtWar(iTeam) and not gc.getTeam(iTeam).isVassal(iWinnerTeam):
												gc.getPlayer(i).AI_changeAttitudeExtra(iWinner, 1)

				# Gewinner bekommt Absage

				else:
						# Gewinner bekommt -1 zum Verlierer
						pWinner.AI_changeAttitudeExtra(iLoser, -1)
						# Alle, die mit dem Gewinner im Krieg sind, bekommen zum Verlierer +1
						# ausser die Vasallen des Verlierers
						iRange = gc.getMAX_PLAYERS()
						for i in range(iRange):
								if gc.getPlayer(i).isAlive():
										iTeam = gc.getPlayer(i).getTeam()
										if pWinnerTeam.isAtWar(iTeam) and not gc.getTeam(iTeam).isVassal(iLoserTeam):
												gc.getPlayer(i).AI_changeAttitudeExtra(iLoser, 1)

		else:
				if pLoserTeam.isAVassal():
						VassalUnsetHegemon(iLoser)  # Vasall verliert seinen Hegemon
				VassalHegemonGetsVassal(iLoser)  # Hegemon verliert seine Vasallen
				pWinnerTeam.assignVassal(iLoserTeam, 1)  # surrender
				pWinner.changeGold(iGold)
				pLoser.changeGold(iGold * (-1))
				if iWinner == gc.getGame().getActivePlayer():
						CyAudioGame().Play2DSound('AS2D_COINS')
				# Open borders
				doOpenBorders2Vassal(iWinner, iLoser)


def do682(iWinner, iLoser, iGold):
		pWinner = gc.getPlayer(iWinner)
		pLoser = gc.getPlayer(iLoser)
		# iWinnerTeam = pWinner.getTeam()
		# pWinnerTeam = gc.getTeam(iWinnerTeam)
		# iLoserTeam = pLoser.getTeam()
		# pLoserTeam = gc.getTeam(iLoserTeam)

		# Loser moechte nix zu tun haben = 1a
		# Winner bietet Hegemonschaft an
		if iGold == -1:
				iGold1 = CvUtil.myRandom(pWinner.getGold() / 4, "iGold1 Winner bietet Hegemonschaft an")
				if iGold1 < pWinner.getGold() / 8:
						iGold1 = pWinner.getGold() / 8 + iGold1
				iGold2 = iGold1 * 2
				iGold1 = int(iGold1)
				iGold2 = int(iGold2)
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_04", (gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription(), pLoser.getCivilizationShortDescription(0))))
				popupInfo.setData1(iWinner)
				popupInfo.setData2(iLoser)
				popupInfo.setData3(iGold1)
				popupInfo.setFlags(iGold2)
				popupInfo.setOnClickedPythonCallback("popupVassal04")  # EntryPoints/CvScreenInterface und CvGameUtils / 683
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_04_1", (iGold1, pWinner.getCivilizationAdjective(2))), "")
				if iGold2 > 0:
						popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_04_2", (iGold2, pWinner.getCivilizationAdjective(2))), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_04_NO", ()), "")
				popupInfo.addPopup(iWinner)
		# Loser schlagt vor, Winner entscheidet = 1b
		else:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_06", (gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription(), pLoser.getCivilizationShortDescription(0), iGold)))
				popupInfo.setData1(iWinner)
				popupInfo.setData2(iLoser)
				popupInfo.setData3(iGold)
				popupInfo.setOnClickedPythonCallback("popupVassal06")  # EntryPoints/CvScreenInterface und CvGameUtils / 685
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_06_YES", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_06_NO", ()), "")
				iRand = 1 + CvUtil.myRandom(9, "TXT_KEY_POPUP_VASSAL_KILL_")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_KILL_"+str(iRand), (gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription(),)), "")
				popupInfo.addPopup(iWinner)


def do683(iWinner, iLoser, iData4):
		pWinner = gc.getPlayer(iWinner)
		# pLoser = gc.getPlayer(iLoser)
		# iWinnerTeam = pWinner.getTeam()
		# pWinnerTeam = gc.getTeam(iWinnerTeam)
		# iLoserTeam = pLoser.getTeam()
		# pLoserTeam = gc.getTeam(iLoserTeam)

		# Winner bietet Hegemonschaft an
		# Loser entscheidet
		if iData4 >= 0:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_05", (gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(), pWinner.getCivilizationShortDescription(0), iData4)))
				popupInfo.setData1(iWinner)
				popupInfo.setData2(iLoser)
				popupInfo.setData3(iData4)
				popupInfo.setOnClickedPythonCallback("popupVassal05")  # EntryPoints/CvScreenInterface und CvGameUtils / 684
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_05_YES", (gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(),)), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_05_NO", (iData4,)), "")
				iRand = 1 + CvUtil.myRandom(9, "TXT_KEY_POPUP_VASSAL_KILL_")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_KILL_"+str(iRand), (gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(),)), "")
				popupInfo.addPopup(iLoser)


def do684(iWinner, iLoser, iGold):
		pWinner = gc.getPlayer(iWinner)
		pLoser = gc.getPlayer(iLoser)
		iWinnerTeam = pWinner.getTeam()
		pWinnerTeam = gc.getTeam(iWinnerTeam)
		iLoserTeam = pLoser.getTeam()
		pLoserTeam = gc.getTeam(iLoserTeam)

		# Winner bietet Hegemonschaft an
		# Loser nicht einverstanden
		if iGold == 0:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_07", (gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription(), pLoser.getCivilizationShortDescription(0))))
				popupInfo.setData1(iWinner)
				popupInfo.setData2(iLoser)
				popupInfo.setData3(1)  # zur Winnerauswahl
				popupInfo.setOnClickedPythonCallback("popupVassal07")  # EntryPoints/CvScreenInterface und CvGameUtils / 686 / 1
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_07_YES", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_07_NO", ()), "")
				popupInfo.addPopup(iWinner)

		# Botschafter vom Winner wird gekillt
		elif iGold == -1:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)  # Vorsicht Text PopUp only!
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_05_1", (gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription(), pLoser.getCivilizationShortDescription(0))))
				popupInfo.addPopup(iLoser)

				# Verschlechterung der Beziehungen des Gewinners zum Verlierer -1
				pWinner.AI_changeAttitudeExtra(iLoser, -1)
				# Alle, die mit dem Gewinner im Krieg sind, bekommen zum Verlierer +1
				# ausser die Vasallen des Verlierers
				iRange = gc.getMAX_PLAYERS()
				for i in range(iRange):
						if gc.getPlayer(i).isAlive():
								iTeam = gc.getPlayer(i).getTeam()
								if pWinnerTeam.isAtWar(iTeam) and not gc.getTeam(iTeam).isVassal(pLoserTeam.getID()):
										gc.getPlayer(i).AI_changeAttitudeExtra(iLoser, 1)

		else:
				if pLoserTeam.isAVassal():
						VassalUnsetHegemon(iLoser)  # Vasall verliert seinen Hegemon
				VassalHegemonGetsVassal(iLoser)  # Hegemon verliert seine Vasallen
				pWinnerTeam.assignVassal(iLoserTeam, 1)  # surrender
				pLoser.changeGold(iGold)
				pWinner.changeGold(iGold * (-1))
				if iLoser == gc.getGame().getActivePlayer():
						CyAudioGame().Play2DSound('AS2D_COINS')
				# Open borders
				doOpenBorders2Vassal(iWinner, iLoser)


def do685(iWinner, iLoser, iGold):
		pWinner = gc.getPlayer(iWinner)
		pLoser = gc.getPlayer(iLoser)
		iWinnerTeam = pWinner.getTeam()
		pWinnerTeam = gc.getTeam(iWinnerTeam)
		iLoserTeam = pLoser.getTeam()
		pLoserTeam = gc.getTeam(iLoserTeam)

		# Winner bietet Hegemonschaft an
		# Loser entscheidet

		# Winner lehnt ab, nochmal entscheiden?
		if iGold == 0:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_07", (gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(), pWinner.getCivilizationShortDescription(0))))
				popupInfo.setData1(iWinner)
				popupInfo.setData2(iLoser)
				popupInfo.setData3(0)  # zur Loserauswahl
				popupInfo.setOnClickedPythonCallback("popupVassal07")  # EntryPoints/CvScreenInterface und CvGameUtils / 686 / 0
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_07_YES", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_07_NO", ()), "")
				popupInfo.addPopup(iLoser)

		# Botschafter vom Loser wird gekillt
		elif iGold == -1:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)  # Vorsicht Text PopUp only!
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_05_1", (gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(), pWinner.getCivilizationShortDescription(0))))
				popupInfo.addPopup(iLoser)
				# Verschlechterung der Beziehungen vom Verlierer zum Gewinner -1
				pLoser.AI_changeAttitudeExtra(iWinner, -1)
				# Alle, die mit dem Verlierer im Krieg sind, bekommen zum Gewinner +1
				# ausser die Vasallen des Gewinners
				iRange = gc.getMAX_PLAYERS()
				for i in range(iRange):
						if gc.getPlayer(i).isAlive():
								iTeam = gc.getPlayer(i).getTeam()
								if pLoserTeam.isAtWar(iTeam) and not gc.getTeam(iTeam).isVassal(pWinnerTeam.getID()):
										gc.getPlayer(i).AI_changeAttitudeExtra(iWinner, 1)

		# Vasall werden
		else:
				if pLoserTeam.isAVassal():
						VassalUnsetHegemon(iLoser)  # Vasall verliert seinen Hegemon
				VassalHegemonGetsVassal(iLoser)  # Hegemon verliert seine Vasallen
				pWinnerTeam.assignVassal(iLoserTeam, 1)  # surrender
				pWinner.changeGold(iGold)
				pLoser.changeGold(iGold * (-1))
				if iWinner == gc.getGame().getActivePlayer():
						CyAudioGame().Play2DSound('AS2D_COINS')
				# Open borders
				doOpenBorders2Vassal(iWinner, iLoser)


def do687(iWinner, iLoser, iVassal, iGold):
		pWinner = gc.getPlayer(iWinner)
		pLoser = gc.getPlayer(iLoser)
		pVassal = gc.getPlayer(iVassal)

		#iWinnerTeam = pWinner.getTeam()
		#pWinnerTeam = gc.getTeam(iWinnerTeam)
		iLoserTeam = pLoser.getTeam()
		# pLoserTeam = gc.getTeam(iLoserTeam)
		iVassalTeam = pVassal.getTeam()
		pVassalTeam = gc.getTeam(iVassalTeam)

		# Vasall vom Hegemon loesen
		VassalUnsetHegemon(iVassal)

		# Dann mit allen Frieden schliessen
		iRange = gc.getMAX_PLAYERS()
		for i in range(iRange):
				if gc.getPlayer(i).isAlive():
						iTeam = gc.getPlayer(i).getTeam()
						if pVassalTeam.isAtWar(iTeam) and i != gc.getBARBARIAN_PLAYER():
								gc.getTeam(iTeam).makePeace(iVassalTeam)

		# Danach dem alten Hegemon Krieg erklaeren
		pVassalTeam.declareWar(iLoserTeam, 0, 4)
		pVassal.changeGold(iGold)
		pWinner.changeGold(iGold * (-1))
		if iVassal == gc.getGame().getActivePlayer():
				CyAudioGame().Play2DSound('AS2D_COINS')


def do688(iWinner, iLoser, iVassal, iFlag):
		pWinner = gc.getPlayer(iWinner)
		pLoser = gc.getPlayer(iLoser)
		pVassal = gc.getPlayer(iVassal)
		#iWinnerTeam = pWinner.getTeam()
		#pWinnerTeam = gc.getTeam(iWinnerTeam)
		iLoserTeam = pLoser.getTeam()
		#pLoserTeam = gc.getTeam(iLoserTeam)

		if iFlag == 0:
				gc.getTeam(pVassal.getTeam()).declareWar(iLoserTeam, 0, 4)
				# Beziehungsstatus aendern
				pLoser.AI_changeAttitudeExtra(iVassal, -2)
				pWinner.AI_changeAttitudeExtra(iVassal, 2)
				if pWinner.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_09_1", (pVassal.getCivilizationAdjective(3), gc.getLeaderHeadInfo(pVassal.getLeaderType()).getDescription(),)))
						popupInfo.addPopup(iWinner)
				if pLoser.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_09_2", (pVassal.getCivilizationAdjective(4), gc.getLeaderHeadInfo(pVassal.getLeaderType()).getDescription(),)))
						popupInfo.addPopup(iLoser)
		else:
				# Beziehungsstatus aendern
				pLoser.AI_changeAttitudeExtra(iVassal, 3)
				pWinner.AI_changeAttitudeExtra(iVassal, -1)
				if pWinner.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_09_3", (pVassal.getCivilizationAdjective(3), gc.getLeaderHeadInfo(pVassal.getLeaderType()).getDescription(),)))
						popupInfo.addPopup(iWinner)
				if pLoser.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_09_4", (pVassal.getCivilizationAdjective(3), gc.getLeaderHeadInfo(pVassal.getLeaderType()).getDescription(),)))
						popupInfo.addPopup(iLoser)


def do689(iWinner, iLoser, iVassal, iGold):
		pWinner = gc.getPlayer(iWinner)
		pLoser = gc.getPlayer(iLoser)
		# pVassal = gc.getPlayer(iVassal)
		#iWinnerTeam = pWinner.getTeam()
		#pWinnerTeam = gc.getTeam(iWinnerTeam)
		# iLoserTeam = pLoser.getTeam()
		#pLoserTeam = gc.getTeam(iLoserTeam)

		# Winner bietet dem Vasall ein Angebot an (iData5 = Gold)
		if iGold > 0:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_11", (gc.getLeaderHeadInfo(pWinner.getLeaderType()
																																																	).getDescription(), iGold, gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription())))
				popupInfo.setData1(iWinner)
				popupInfo.setData2(iLoser)
				popupInfo.setData3(iVassal)
				popupInfo.setFlags(iGold)
				popupInfo.setOnClickedPythonCallback("popupVassal11")  # EntryPoints/CvScreenInterface und CvGameUtils / 690
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_11_YES", (gc.getLeaderHeadInfo(
						pLoser.getLeaderType()).getDescription(), gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription())), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_11_NO", ()), "")
				iRand = 1 + CvUtil.myRandom(9, "TXT_KEY_POPUP_VASSAL_KILL_")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_KILL_"+str(iRand), (gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(),)), "")
				popupInfo.addPopup(iVassal)

		# Winner hat kein Interesse
		# Vasall darf entscheiden, ob er Krieg erklaert
		else:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_12", (gc.getLeaderHeadInfo(pWinner.getLeaderType()).getDescription(), pWinner.getCivilizationAdjective(2))))
				popupInfo.setData1(iWinner)
				popupInfo.setData2(iLoser)
				popupInfo.setData3(iVassal)
				popupInfo.setOnClickedPythonCallback("popupVassal12")  # EntryPoints/CvScreenInterface und CvGameUtils / 691
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_12_YES", (gc.getLeaderHeadInfo(pLoser.getLeaderType()).getDescription(),)), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_12_NO", ()), "")
				popupInfo.addPopup(iVassal)


def do690(iWinner, iLoser, iVassal, iGold):
		pWinner = gc.getPlayer(iWinner)
		pLoser = gc.getPlayer(iLoser)
		pVassal = gc.getPlayer(iVassal)
		#iWinnerTeam = pWinner.getTeam()
		#pWinnerTeam = gc.getTeam(iWinnerTeam)
		iLoserTeam = pLoser.getTeam()
		# pLoserTeam = gc.getTeam(iLoserTeam)

		# Botschafter-Kill
		if iGold == -1:
				pWinner.AI_changeAttitudeExtra(iVassal, -1)
				if pWinner.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)  # Vorsicht Text PopUp only!
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_05_1", (gc.getLeaderHeadInfo(pVassal.getLeaderType()).getDescription(), pVassal.getCivilizationShortDescription(0))))
						popupInfo.addPopup(iWinner)

		# Angebot angenommen mit Kriegserklaerung
		else:
				# Zuerst mit allen Frieden schliessen
				iVassalTeam = pVassal.getTeam()
				pVassalTeam = gc.getTeam(iVassalTeam)
				iRange = gc.getMAX_PLAYERS()
				for i in range(iRange):
						if gc.getPlayer(i).isAlive():
								iTeam = gc.getPlayer(i).getTeam()
								if pVassalTeam.isAtWar(iTeam) and i != gc.getBARBARIAN_PLAYER():
										gc.getTeam(iTeam).makePeace(iVassalTeam)

				# Vom Hegemon loesen
				VassalUnsetHegemon(iLoserTeam)

				# Danach Krieg erklaeren
				gc.getTeam(pVassal.getTeam()).declareWar(iLoserTeam, 0, 4)
				pVassal.changeGold(iGold)
				pWinner.changeGold(iGold * (-1))
				if iVassal == gc.getGame().getActivePlayer():
						CyAudioGame().Play2DSound('AS2D_COINS')

				if pWinner.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_11_1", (pVassal.getCivilizationAdjective(3), gc.getLeaderHeadInfo(pVassal.getLeaderType()).getDescription())))
						popupInfo.addPopup(iWinner)


def do691(iWinner, iLoser, iVassal):
		pWinner = gc.getPlayer(iWinner)
		pLoser = gc.getPlayer(iLoser)
		pVassal = gc.getPlayer(iVassal)
		#iWinnerTeam = pWinner.getTeam()
		#pWinnerTeam = gc.getTeam(iWinnerTeam)
		iLoserTeam = pLoser.getTeam()
		# pLoserTeam = gc.getTeam(iLoserTeam)

		# Vom Hegemon loesen
		VassalUnsetHegemon(iLoserTeam)
		gc.getTeam(pVassal.getTeam()).declareWar(iLoserTeam, 0, 4)

		if pWinner.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_12_1", (pVassal.getCivilizationAdjective(3), gc.getLeaderHeadInfo(pVassal.getLeaderType()).getDescription())))
				popupInfo.addPopup(iWinner)

# 702 , iHegemon (HI) , iVassal, iTech , iTechCost
# Yes  : iTech und iTechCost = -1 (+1 Beziehung)
# Money: iTech und iTechCost
# NO:  : iTech = -1
def do702(iHegemon, iVassal, iTech, iTechCost):
		pHegemon = gc.getPlayer(iHegemon)
		pVassal = gc.getPlayer(iVassal)
		iVassalTeam = pVassal.getTeam()
		pVassalTeam = gc.getTeam(iVassalTeam)

		# Yes
		if iTech > -1 and iTechCost == -1:
				pVassalTeam.setHasTech(iTech, 1, iVassal, 0, 1)
				if pVassal.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_GETTING_TECH", (gc.getTechInfo(iTech).getDescription(),)))
						popupInfo.addPopup(iVassal)
				else:
						pVassal.AI_changeAttitudeExtra(iHegemon, 1)
						if iHegemon == gc.getGame().getActivePlayer():
								CyInterface().addMessage(iHegemon, True, 10, CyTranslator().getText("TXT_KEY_POPUP_VASSAL_TECH_THX", (gc.getTechInfo(iTech).getDescription(),)), None, 2, None, ColorTypes(8), 0, 0, False, False)

		# Money
		elif iTech > -1:
				if pVassal.getGold() >= iTechCost:
						# HI - HI Konfrontation
						if pVassal.isHuman():
								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
								popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_TECH_2", (gc.getTechInfo(iTech).getDescription(), iTechCost)))
								popupInfo.setData1(iHegemon)
								popupInfo.setData2(iVassal)
								popupInfo.setData3(iTech)
								popupInfo.setFlags(iTechCost)
								popupInfo.setOnClickedPythonCallback("popupVassalTech2")  # EntryPoints/CvScreenInterface und CvGameUtils / 702
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_TECH_2_YES", ("", iTechCost)), "")
								popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_TECH_2_NO", ("",)), "")
								popupInfo.addPopup(iVassal)
						else:
								pVassalTeam.setHasTech(iTech, 1, iVassal, 0, 1)
								pVassal.changeGold(-iTechCost)
								pHegemon.changeGold(iTechCost)
								if iHegemon == gc.getGame().getActivePlayer():
										CyAudioGame().Play2DSound('AS2D_COINS')

								# Tech cost check
								# the more CIVs do have this tech, the cheaper
								iFaktor = gc.getGame().countKnownTechNumTeams(iTech)
								if iFaktor < 2:
										iFaktor = 2
								iTechCostRegular = gc.getTechInfo(iTech).getResearchCost() / iFaktor
								if iTechCost < iTechCostRegular and iHegemon == gc.getGame().getActivePlayer():
										CyInterface().addMessage(iHegemon, True, 10, CyTranslator().getText("TXT_KEY_POPUP_VASSAL_TECH_THX", (gc.getTechInfo(iTech).getDescription(),)), None, 2, None, ColorTypes(8), 0, 0, False, False)
								else:
										pVassal.AI_changeAttitudeExtra(iHegemon, -1)
				else:
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_TECH_HAS_NO_MONEY", (gc.getTechInfo(iTech).getDescription(), iTechCost)))
						popupInfo.addPopup(iHegemon)

		# No
		elif not pVassal.isHuman():
				pVassal.AI_changeAttitudeExtra(iHegemon, -2)

# 703 , iHegemon (HI) , iVassal (HI), iTech , iTechCost
# Yes  : iTech und iTechCost
# NO:  : iTechCost = -1


def do703(iHegemon, iVassal, iTech, iTechCost):
		pHegemon = gc.getPlayer(iHegemon)
		pVassal = gc.getPlayer(iVassal)
		iVassalTeam = pVassal.getTeam()
		pVassalTeam = gc.getTeam(iVassalTeam)

		if iTechCost == -1:
				CyInterface().addMessage(iHegemon, True, 10, CyTranslator().getText("TXT_KEY_POPUP_VASSAL_TECH_2_DECLINE", ("",)), None, 2, None, ColorTypes(8), 0, 0, False, False)
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_TECH_2_DECLINE", ("", )))
				popupInfo.addPopup(iHegemon)
		else:
				pVassalTeam.setHasTech(iTech, 1, iVassal, 0, 1)
				pVassal.changeGold(-iTechCost)
				pHegemon.changeGold(iTechCost)
				if iHegemon == gc.getGame().getActivePlayer():
						CyAudioGame().Play2DSound('AS2D_COINS')
				# Meldungen
				CyInterface().addMessage(iHegemon, True, 10, CyTranslator().getText("TXT_KEY_POPUP_VASSAL_TECH_THX", (gc.getTechInfo(iTech).getDescription(),)), None, 2, None, ColorTypes(8), 0, 0, False, False)
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_VASSAL_GETTING_TECH", (gc.getTechInfo(iTech).getDescription(),)))
				popupInfo.addPopup(iVassal)

# Get List of Hegemon's vassals


def getVassals(iHegemon):
		pHegemon = gc.getPlayer(iHegemon)
		iHegemonTeam = pHegemon.getTeam()

		lVassals = []
		iRange = gc.getMAX_PLAYERS()
		for iPlayer in range(iRange):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer is not None and not pPlayer.isNone() and pPlayer.isAlive():
						iTeam = pPlayer.getTeam()
						pTeam = gc.getTeam(iTeam)
						if pTeam.isVassal(iHegemonTeam):
								lVassals.append(iPlayer)
		return lVassals

# Get List of a player's cities with less owned culture


def getCitiesOfLowCultureLevel(iPlayer):
		pPlayer = gc.getPlayer(iPlayer)

		lCities = []
		iNumCities = pPlayer.getNumCities()
		for iCity in range(iNumCities):
				pCity = pPlayer.getCity(iCity)
				if not pCity.isNone():
						iCulture = pCity.plot().calculateTeamCulturePercent(pPlayer.getTeam())
						if iCulture < 51:
								lCities.append(iCity)

		return lCities


# ueberlaufende Stadt / City renegade
# When Unit gets attacked: LoserUnitID (must not get killed automatically) , no unit = None
def doGiveCity2Vassal(pCity, iNewOwner):

		# ***TEST***
		#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Give City 2 Vassal",iNewOwner)), None, 2, None, ColorTypes(10), 0, 0, False, False)

		if iNewOwner == -1:
				iNewOwner = gc.getBARBARIAN_PLAYER()
		if pCity.getOwner() == iNewOwner:
				return

		pNewOwner = gc.getPlayer(iNewOwner)

		iX = pCity.getX()
		iY = pCity.getY()
		pPlot = pCity.plot()
		iOldOwner = pCity.getOwner()

		# AI Attitude dadurch aufbessern
		pNewOwner.AI_changeAttitudeExtra(iOldOwner, +1)

		# Einheiten auslesen bevor die Stadt ueberlaeuft
		UnitArray = []
		iRange = pPlot.getNumUnits()
		for iUnit in range(iRange):
				pLoopUnit = pPlot.getUnit(iUnit)
				if not pLoopUnit.isDead():
						if pLoopUnit.getOwner() == iOldOwner:
								if pLoopUnit.isCargo():
										pLoopUnit.setTransportUnit(None)  # Fehlerquelle
								UnitArray.append(pLoopUnit)

		# Stadt laeuft automatisch ueber (CyCity pCity, BOOL bConquest, BOOL bTrade)
		pNewOwner.acquireCity(pCity, 0, 1)

		# Einheiten generieren
		for pLoopUnit in UnitArray:
				if pLoopUnit is None or pLoopUnit.isNone():
						# TEST
						#CyInterface().addMessage(gc.getGame().getActivePlayer(), True, 10, CyTranslator().getText("TXT_KEY_MESSAGE_TEST",("Test 1 - Unit none",iOldOwner)), None, 2, None, ColorTypes(10), 0, 0, False, False)
						continue

				iUnitType = pLoopUnit.getUnitType()
				# iUnitAIType = pLoopUnit.getUnitAIType() # Fehlerquelle
				iUnitAIType = -1
				iUnitCombatType = pLoopUnit.getUnitCombatType()

				# UnitAIType -1 (NO_UNITAI) -> UNITAI_UNKNOWN = 0 , ATTACK = 4, City Defense = 10
				if iUnitAIType in [-1, 0]:
						if iUnitType == gc.getInfoTypeForString('UNIT_FREED_SLAVE'):
								iUnitAIType = 20  # UNITAI_ENGINEER
						elif iUnitType == gc.getInfoTypeForString('UNIT_TRADE_MERCHANT'):
								iUnitAIType = 19  # UNITAI_MERCHANT
						elif iUnitType == gc.getInfoTypeForString('UNIT_TRADE_MERCHANTMAN'):
								iUnitAIType = 19
						else:
								iUnitAIType = -1

				# Slaves will be freed, nur wenn dessen Besitzer neu ist
				if iUnitType == gc.getInfoTypeForString('UNIT_SLAVE'):
						iUnitType = gc.getInfoTypeForString('UNIT_FREED_SLAVE')
						NewUnit = pNewOwner.initUnit(iUnitType, iX, iY, UnitAITypes.UNITAI_ENGINEER, DirectionTypes.DIRECTION_SOUTH)
						PAE_Unit.copyName(NewUnit, iUnitType, pLoopUnit.getName())
				# Emigrant und dessen Kultur
				elif iUnitType == gc.getInfoTypeForString('UNIT_EMIGRANT'):
						NewUnit = pNewOwner.initUnit(iUnitType, iX, iY, UnitAITypes.UNITAI_SETTLE, DirectionTypes.DIRECTION_SOUTH)
						CvUtil.addScriptData(NewUnit, "p", iOldOwner)
						PAE_Unit.copyName(NewUnit, iUnitType, pLoopUnit.getName())
				elif iUnitType != -1:
						NewUnit = pNewOwner.initUnit(iUnitType, iX, iY, UnitAITypes(iUnitAIType), DirectionTypes.DIRECTION_SOUTH)
						PAE_Unit.copyName(NewUnit, iUnitType, pLoopUnit.getName())
						if iUnitCombatType != -1:
								PAE_Unit.initUnitFromUnit(pLoopUnit, NewUnit)
								NewUnit.setDamage(pLoopUnit.getDamage(), -1)

				if pLoopUnit:
						pLoopUnit.kill(True, -1)

		if iNewOwner == gc.getBARBARIAN_PLAYER():
				iPartisan = gc.getInfoTypeForString("UNIT_FREEDOM_FIGHTER")
				pNewOwner.initUnit(iPartisan, iX, iY, UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
				pNewOwner.initUnit(iPartisan, iX, iY, UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
				pNewOwner.initUnit(iPartisan, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		# Pointer anpassen
		if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				if pCity and not pCity.isNone():
						# Stadtgroesse kontrollieren
						if pCity.getPopulation() < 1:
								pCity.setPopulation(1)
						# Kolonie/Provinz checken
						PAE_City.doCheckCityState(pCity)


# ein Spieler, der zu einem Vasall wird, soll OpenBorders zu seinem Hegemon bekommen
# ebenfalls auch bei den Vasallen dieses Hegemons
def doOpenBorders2Vassal(iWinner, iLoser):
		pWinner = gc.getPlayer(iWinner)
		pLoser = gc.getPlayer(iLoser)
		iWinnerTeam = pWinner.getTeam()
		# pWinnerTeam = gc.getTeam(iWinnerTeam)
		iLoserTeam = pLoser.getTeam()
		pLoserTeam = gc.getTeam(iLoserTeam)

		# OpenBorders zum Hegemon
		pLoserTeam.signOpenBorders(iWinnerTeam)

		# OpenBorders zu den Vasallen des Hegemons
		iRange = gc.getMAX_PLAYERS()
		for i in range(iRange):
				pPlayer = gc.getPlayer(i)
				if pPlayer.isAlive():
						iTeam = pPlayer.getTeam()
						pTeam = gc.getTeam(iTeam)
						if pTeam.isVassal(iWinnerTeam):
								pLoserTeam.signOpenBorders(iTeam)
