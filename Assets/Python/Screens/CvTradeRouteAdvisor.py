# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
# Created by Pie, Austria
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
																FontTypes, TableStyles,
																WidgetTypes, PanelStyles,
																CyGame, FontSymbols,
																CyGInterfaceScreen, PopupStates)
import CvUtil
# import ScreenInput
import CvScreenEnums
import PAE_Trade

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvTradeRouteAdvisor:

		def __init__(self):
				self.SCREEN_NAME = "TradeRouteAdvisor"
				self.DEBUG_DROPDOWN_ID = "TradeRouteAdvisorDropdownWidget"
				self.WIDGET_ID = "TradeRouteAdvisorWidget"
				self.WIDGET_HEADER = "TradeRouteAdvisorWidgetHeader"
				self.EXIT_ID = "TradeRouteAdvisorExitWidget"
				self.BACKGROUND_ID = "TradeRouteAdvisorBackground"
				self.X_SCREEN = 500
				self.Y_SCREEN = 396
				self.W_SCREEN = 1024
				self.H_SCREEN = 768
				self.Y_TITLE = 12
				self.Z_CONTROLS = -2.0

				self.X_EXIT = 994
				self.Y_EXIT = 726

				self.nWidgetCount = 0

				self.iTargetPlayer = -1
				self.iActiveCityID = -1
				self.iSelectedMission = -1

		def getScreen(self):
				return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.TRADEROUTE_ADVISOR)

		def interfaceScreen(self):

				self.iTargetPlayer = -1
				self.iActiveCityID = -1
				self.iSelectedMission = -1
				self.iActivePlayer = CyGame().getActivePlayer()

				screen = self.getScreen()
				if screen.isActive():
						return
				screen.setRenderInterfaceOnly(True)
				screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

				# Set the background and exit button, and show the screen
				screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

				screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addPanel("TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR)
				screen.addPanel("TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR)

				screen.showWindowBackground(False)
				screen.setText(self.EXIT_ID, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>",
											 CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

				# Header...
				screen.setLabel(self.WIDGET_HEADER, "Background", u"<font=4b>" + localText.getText("TXT_KEY_TRADE_ROUTE_ADVISOR_SCREEN", ()).upper() + u"</font>",
												CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# draw the contents
				self.drawContents()

				self.deleteAllWidgets()

		def drawContents(self):
				screen = self.getScreen()
				self.deleteAllWidgets()
				# addPanel: Vertical, scrollable, x ,y, width, height
				# +++ 1 +++ PANEL Requests: Trade Requests
				screen.addPanel("PanelRequests", u"", u"", True, False, 35, 75, 945, 266, PanelStyles.PANEL_STYLE_DAWNTOP)
				BUTTON_SIZE = 48
				iY = 30
				# Cities with Special bonus order
				bMessageNoCities = True
				i = 0
				for iPlayer in range(gc.getMAX_PLAYERS()):
						loopPlayer = gc.getPlayer(iPlayer)
						if loopPlayer.isAlive() and not loopPlayer.isHuman() and not loopPlayer.isBarbarian():
								(pCity, pIter) = loopPlayer.firstCity(False)
								while pCity:
										if not pCity.isNone() and pCity.getOwner() == loopPlayer.getID():  # only valid cities
												iTurn = int(CvUtil.getScriptData(pCity, ["tst"], -1)) - gc.getGame().getGameTurn()
												if iTurn != -1:
														i += 1
														pTeam = gc.getTeam(loopPlayer.getTeam())
														if pTeam.isHasMet(gc.getPlayer(gc.getGame().getActivePlayer()).getTeam()):
																iBonus = int(CvUtil.getScriptData(pCity, ["tsb"], -1))
																if iBonus != -1:
																		iCiv = loopPlayer.getCivilizationType()
																		iLeader = loopPlayer.getLeaderType()
																		iPop = pCity.getPopulation()
																		bMessageNoCities = False
																		iX = 50
																		iY += 60
																		# Button Bonus
																		screen.setImageButton("Label_1_"+str(i), gc.getBonusInfo(iBonus).getButton(), iX, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1)
																		iX += 60
																		# Text City name
																		szText = pCity.getName()
																		screen.setLabel("Label_2_"+str(i), "Background", u"<font=4>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
																										iX, iY + 2, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
																		# Text CIV Name
																		szText = loopPlayer.getCivilizationDescription(0)
																		screen.setLabel("Label_CivName_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
																										iX, iY + 25, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
																		iX += 325
																		# Text City Population
																		szText = localText.getText("POP:", ()) + u" %d" % (iPop)
																		screen.setLabel("Label_3_"+str(i), "Background", u"<font=4>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY,
																										iX, iY + 10, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
																		iX += 10
																		# Button Civ
																		screen.setImageButton("Label_4_"+str(i), gc.getCivilizationInfo(iCiv).getButton(), iX, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, -1)
																		iX += 60
																		# Button Leader
																		screen.setImageButton("Label_5_"+str(i), gc.getLeaderHeadInfo(iLeader).getButton(), iX, iY,
																													BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, iCiv)
																		iX += 60
																		# Text Open Borders
																		szText = localText.getText("TXT_KEY_MISC_OPEN_BORDERS", ()) + u": "
																		if pTeam.isOpenBorders(CyGame().getActiveTeam()):
																				szText += localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + localText.getText("TXT_KEY_POPUP_YES", ()) + localText.getText("TXT_KEY_COLOR_REVERT", ())
																		else:
																				szText += localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + localText.getText("TXT_KEY_POPUP_NO", ()) + localText.getText("TXT_KEY_COLOR_REVERT", ())
																		screen.setLabel("Label_6_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
																										iX, iY+4, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

																		# AI Attitudes - KI Haltung
																		iAtt = loopPlayer.AI_getAttitude(gc.getGame().getActivePlayer())
																		lAttText = ["TXT_KEY_ATTITUDE_FURIOUS", "TXT_KEY_ATTITUDE_ANNOYED", "TXT_KEY_ATTITUDE_CAUTIOUS", "TXT_KEY_ATTITUDE_PLEASED", "TXT_KEY_ATTITUDE_FRIENDLY"]
																		# Text Attitude
																		szText = localText.getText("TXT_KEY_ATTITUDE", ()) + u": %c" % (CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 4 + iAtt) + localText.getText(lAttText[iAtt], ())
																		screen.setLabel("Label_7_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
																										iX, iY+24, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
																		iX += 200

																		# Text Required Bonus
																		szText = localText.getText("TXT_KEY_TRADE_ADVISOR_1", ()) + u": " + gc.getBonusInfo(iBonus).getDescription()
																		screen.setLabel("Label_8_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
																										iX, iY+4, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
																		# Text Remaining Turns
																		szText = localText.getText("TXT_KEY_TRADE_ADVISOR_2", ()) + u": %d" % (iTurn)
																		screen.setLabel("Label_9_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
																										iX, iY+24, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
										(pCity, pIter) = loopPlayer.nextCity(pIter, False)

				if bMessageNoCities:
						szText = localText.getText("TXT_KEY_TRADE_ADVISOR_INFO", ())
						screen.setLabel("Label1_0", "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 100, iY+80, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# +++ 2 +++ PANEL 1-4: Goods (Bonus resources)
				screen.addPanel("Panel1", u"", u"", True, False,  35, 344, 225, 50, PanelStyles.PANEL_STYLE_DAWNTOP)
				screen.addPanel("Panel2", u"", u"", True, False, 275, 344, 225, 50, PanelStyles.PANEL_STYLE_DAWNTOP)
				screen.addPanel("Panel3", u"", u"", True, False, 515, 344, 225, 50, PanelStyles.PANEL_STYLE_DAWNTOP)
				screen.addPanel("Panel4", u"", u"", True, False, 755, 344, 225, 50, PanelStyles.PANEL_STYLE_DAWNTOP)

				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_TITLE_PANEL1", ()).upper() + u"</font>"
				screen.setLabel("TitelPanel1", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 45, 350, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_TITLE_PANEL2", ()).upper() + u"</font>"
				screen.setLabel("TitelPanel2", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 285, 350, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_TITLE_PANEL3", ()).upper() + u"</font>"
				screen.setLabel("TitelPanel3", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 525, 350, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_TITLE_PANEL4", ()).upper() + u"</font>"
				screen.setLabel("TitelPanel4", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 765, 350, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_WERT_PANEL1", ()) + u"</font>"
				screen.setLabel("WertPanel1", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 45, 368, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_WERT_PANEL2", ()) + u"</font>"
				screen.setLabel("WertPanel2", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 285, 368, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_WERT_PANEL3", ()) + u"</font>"
				screen.setLabel("WertPanel3", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 525, 368, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_WERT_PANEL4", ()) + u"</font>"
				screen.setLabel("WertPanel4", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 765, 368, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Tabellen
				screen.addTableControlGFC("Table1", 1,  40, 400, 215, 210, False, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.addTableControlGFC("Table2", 1, 280, 400, 215, 210, False, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.addTableControlGFC("Table3", 1, 520, 400, 215, 210, False, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.addTableControlGFC("Table4", 1, 760, 400, 215, 210, False, True, 24, 24, TableStyles.TABLE_STYLE_STANDARD)

				# Add bonus to tables
				pPlayer = gc.getPlayer(self.iActivePlayer)
				iCol1 = 0
				iCol2 = 0
				iCol3 = 0
				iCol4 = 0
				iNumBonus = gc.getNumBonusInfos()
				for iLoop in range(iNumBonus):
						szName = gc.getBonusInfo(iLoop).getDescription()
						szButton = gc.getBonusInfo(iLoop).getButton()
						iBonusClassType = gc.getBonusInfo(iLoop).getBonusClassType()
						# iBonusTechReveal = gc.getBonusInfo(iLoop).getTechReveal()
						#bShow = False
						# if gc.getTeam(pPlayer.getTeam()).isHasTech(iBonusTechReveal):
						bShow = True
						# BonusclassTypes PAE:
						# 0: BONUSCLASS_GENERAL
						# 1: BONUSCLASS_GRAIN
						# 2: BONUSCLASS_LIVESTOCK
						# 3: BONUSCLASS_MERCENARY
						# 4: BONUSCLASS_LUXURY
						# 5: BONUSCLASS_WONDER
						# 6: BONUSCLASS_MISC
						# 7: BONUSCLASS_RARITY
						# 8: BONUSCLASS_PLANTATION
						if bShow:
								if iBonusClassType == 7:
										screen.appendTableRow("Table1")
										screen.setTableText("Table1", 0, iCol1, szName, szButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
										iCol1 += 1
								elif iBonusClassType == 4:
										screen.appendTableRow("Table2")
										screen.setTableText("Table2", 0, iCol2, szName, szButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
										iCol2 += 1
								elif iBonusClassType == 0 or iBonusClassType == 5:
										screen.appendTableRow("Table3")
										screen.setTableText("Table3", 0, iCol3, szName, szButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
										iCol3 += 1
								elif iBonusClassType == 1 or iBonusClassType == 2 or iBonusClassType == 8:
										screen.appendTableRow("Table4")
										screen.setTableText("Table4", 0, iCol4, szName, szButton, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
										iCol4 += 1

				# +++ 3 +++ PANEL Bottom: Formeln

				screen.addPanel("PanelBottom", u"", u"", True, False, 40, self.H_SCREEN-151, 935, 96, PanelStyles.PANEL_STYLE_MAIN_BLACK25)

				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_BOTTOM1", ()) + u"</font>"
				screen.setLabel("TextBottom1", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 50, self.H_SCREEN-140, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_BOTTOM2", ()) + u"</font>"
				screen.setLabel("TextBottom2", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 50, self.H_SCREEN-120, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				szText = u"<font=3>" + localText.getText(
						"TXT_KEY_TRADE_ADVISOR_BOTTOM3", (
								PAE_Trade.getPossibleTradeUnits(pPlayer),
								PAE_Trade.getCountTradePosts(pPlayer),
								PAE_Trade.getCountTradeTraits(pPlayer),
								PAE_Trade.getCountTradeCivic(pPlayer),
								PAE_Trade.getCountTradeTechs(pPlayer),
								PAE_Trade.getMaxTradeUnits()
						)
				) + u"</font>"
				screen.setLabel("TextBottom3", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 50, self.H_SCREEN-98, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				iAnz1 = pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString("UNITCLASS_TRADE_MERCHANT_MAN"))
				#iAnz1 = pPlayer.getUnitClassCountPlusMaking(gc.getUnitInfo(gc.getInfoTypeForString("UNIT_TRADE_MERCHANT_MAN")).getUnitClassType())
				iAnz2 = pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString("UNITCLASS_TRADE_MERCHANT"))
				iAnz3 = pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString("UNITCLASS_CARAVAN"))
				iAnz4 = pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString("UNITCLASS_TRADE_MERCHANTMAN"))
				iAnz4 += pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString("UNITCLASS_CARVEL_TRADE"))
				szText = u"<font=3>" + localText.getText("TXT_KEY_TRADE_ADVISOR_BOTTOM4", (PAE_Trade.getCountTradeUnits(pPlayer),iAnz1,iAnz2,iAnz3,iAnz4)) + u"</font>"
				screen.setLabel("TextBottom4", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 50, self.H_SCREEN-78, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# returns a unique ID for a widget in this screen
		def getNextWidgetName(self):
				szName = self.WIDGET_ID + str(self.nWidgetCount)
				self.nWidgetCount += 1
				return szName

		def deleteAllWidgets(self):
				screen = self.getScreen()
				i = self.nWidgetCount - 1
				while i >= 0:
						self.nWidgetCount = i
						screen.deleteWidget(self.getNextWidgetName())
						i -= 1
				self.nWidgetCount = 0

		# Will handle the input for this screen...
		def handleInput(self, inputClass):
				return 0

		def update(self, fDelta):
				return
