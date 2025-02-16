# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
# Created by Pie, Austria
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
																FontTypes, CyGame, CyMap,
																WidgetTypes, PanelStyles, PopupStates,
																CyInterface, NotifyCode, CyMessageControl,
																CyGInterfaceScreen, CyCamera)
import CvUtil
# import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvTradeRouteAdvisor2:

		def __init__(self):
				self.SCREEN_NAME = "TradeRouteAdvisor2"
				self.DEBUG_DROPDOWN_ID = "TradeRouteAdvisor2DropdownWidget"
				self.WIDGET_ID = "TradeRouteAdvisor2Widget"
				self.WIDGET_HEADER = "TradeRouteAdvisor2WidgetHeader"
				self.EXIT_ID = "TradeRouteAdvisor2ExitWidget"
				self.BACKGROUND_ID = "TradeRouteAdvisor2Background"
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
				return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.TRADEROUTE_ADVISOR2)

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
				screen.setLabel(self.WIDGET_HEADER, "Background", u"<font=4b>" + localText.getText("TXT_KEY_TRADE_ROUTE2_ADVISOR_SCREEN", ()).upper() + u"</font>",
												CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# draw the contents
				self.drawContents()

				self.refreshScreen()

		def drawContents(self):

				screen = self.getScreen()
				self.deleteAllWidgets()

				BUTTON_SIZE = 48

				# +++ 1 +++ Units with trade routes
				lTradeUnitsLand = [
						gc.getInfoTypeForString("UNIT_TRADE_MERCHANT_MAN"),
						gc.getInfoTypeForString("UNIT_TRADE_MERCHANT"),
						gc.getInfoTypeForString("UNIT_CARAVAN")
				]
				lTradeUnitsSea = [
						gc.getInfoTypeForString("UNIT_TRADE_MERCHANTMAN"),
						gc.getInfoTypeForString("UNIT_GAULOS"),
						gc.getInfoTypeForString("UNIT_CARVEL_TRADE")
				]

				list1 = []
				list2 = []
				list3 = []
				list4 = []

				pPlayer = gc.getPlayer(CyGame().getActivePlayer())
				(unit, pIter) = pPlayer.firstUnit(False)
				while unit:
						if unit.getUnitType() in lTradeUnitsLand:
								# Mit Auftrag
								if int(CvUtil.getScriptData(unit, ["autA"], 0)):
										list1.append(unit)
								# Ohne Auftrag
								else:
										list3.append(unit)
						elif unit.getUnitType() in lTradeUnitsSea:
								# Mit Auftrag
								if int(CvUtil.getScriptData(unit, ["autA"], 0)):
										list2.append(unit)
								# Ohne Auftrag
								else:
										list4.append(unit)

						(unit, pIter) = pPlayer.nextUnit(pIter, False)

				# Sortierte Liste: Zeige zuerst Landeinheiten, danach Schiffe (zuerst mit Auftag, danach ohne)
				lHandelseinheiten = list1 + list2 + list3 + list4

				iY = 80
				i = 0

				iRange = len(lHandelseinheiten)
				if iRange == 0:
						szText = localText.getText("TXT_KEY_TRADE_ADVISOR_INFO2", ())
						screen.setLabel("Label1_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 100, iY+20, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				else:
						for j in range(iRange):
								pUnit = lHandelseinheiten[j]
								bTradeRouteActive = int(CvUtil.getScriptData(pUnit, ["autA"], 0))

								screen.addPanel("PanelBG_"+str(i), u"", u"", True, False, 40, iY, 935, 51, PanelStyles.PANEL_STYLE_MAIN_BLACK25)
								iY += 4

								# Button unit
								screen.setImageButton("L1_"+str(i), pUnit.getButton(), 50, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, 1, pUnit.getID())

								# Unit name
								szText = pUnit.getName()
								screen.setLabel("L2_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 100, iY+5, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

								# Unit load
								szText = localText.getText("TXT_UNIT_INFO_BAR_5", ()) + u" "
								iValue1 = CvUtil.getScriptData(pUnit, ["b"], -1)
								if iValue1 != -1:
										sBonusDesc = gc.getBonusInfo(iValue1).getDescription()
										iBonusChar = gc.getBonusInfo(iValue1).getChar()
										szText += localText.getText("TXT_UNIT_INFO_BAR_4", (iBonusChar, sBonusDesc))
								else:
										szText += localText.getText("TXT_KEY_NO_BONUS_STORED", ())

								screen.setLabel("L3_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 100, iY+24, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

								# City 1
								if bTradeRouteActive:
										iCityX = int(CvUtil.getScriptData(pUnit, ["autX1"], -1))
										iCityY = int(CvUtil.getScriptData(pUnit, ["autY1"], -1))
										tmpPlot = CyMap().plot(iCityX, iCityY)
										if tmpPlot and not tmpPlot.isNone() and tmpPlot.isCity():
												szText = tmpPlot.getPlotCity().getName()
												if tmpPlot.getOwner() == CyGame().getActivePlayer():
														iTmpX = 470
												else:
														iTmpX = 500
												screen.setLabel("L4_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, iTmpX, iY+5, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
										if tmpPlot.getOwner() != -1:
												iCiv = gc.getPlayer(tmpPlot.getOwner()).getCivilizationType()
												# Flagge
												if tmpPlot.getOwner() == CyGame().getActivePlayer():
														screen.addFlagWidgetGFC("L5_"+str(i), 480, iY, 24, 54, tmpPlot.getOwner(), WidgetTypes.WIDGET_FLAG, tmpPlot.getOwner(), -1)
												# Civ-Button
												else:
														screen.setImageButton("L5_"+str(i), gc.getCivilizationInfo(iCiv).getButton(), 476, iY+24, 24, 24, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, -1)
												szText = gc.getPlayer(tmpPlot.getOwner()).getCivilizationDescription(0)
												screen.setLabel("L6_"+str(i), "Background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY,
																				470, iY+28, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, -1)

										# Button Bonus 1
										iBonus = CvUtil.getScriptData(pUnit, ["autB1"], -1)
										if iBonus != -1:
												screen.setImageButton("L7_"+str(i), gc.getBonusInfo(iBonus).getButton(), 510, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1)

								# Buttons Arrow to left
								screen.setImageButton("L8_"+str(i), "Art/Interface/Buttons/arrow_left.tga", 580, iY+9, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1)

								# Promotion Escort / Begleitschutz
								iPromo = gc.getInfoTypeForString("PROMOTION_SCHUTZ")
								if pUnit.isHasPromotion(iPromo):
										screen.setImageButton("L14_"+str(i), gc.getPromotionInfo(iPromo).getButton(), 615, iY+9, 32, 32, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPromo, -1)

								# Button Arrow to right
								screen.setImageButton("L9_"+str(i), "Art/Interface/Buttons/arrow_right.tga", 650, iY+9, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1)


								# City 2
								if bTradeRouteActive:
										iCityX = int(CvUtil.getScriptData(pUnit, ["autX2"], -1))
										iCityY = int(CvUtil.getScriptData(pUnit, ["autY2"], -1))
								
										# Button Bonus 2
										iBonus = CvUtil.getScriptData(pUnit, ["autB2"], -1)
										if iBonus != -1:
												screen.setImageButton("L10_"+str(i), gc.getBonusInfo(iBonus).getButton(), 700, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1)

										tmpPlot = CyMap().plot(iCityX, iCityY)
										if tmpPlot and not tmpPlot.isNone() and tmpPlot.isCity():
												szText = tmpPlot.getPlotCity().getName()
												if tmpPlot.getOwner() == CyGame().getActivePlayer():
														iTmpX = 790
												else:
														iTmpX = 760
												screen.setLabel("L11_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iTmpX, iY+5, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
										if tmpPlot.getOwner() != -1:
												iCiv = gc.getPlayer(tmpPlot.getOwner()).getCivilizationType()
												# Flagge
												if tmpPlot.getOwner() == CyGame().getActivePlayer():
														screen.addFlagWidgetGFC("L12_"+str(i), 756, iY, 24, 54, tmpPlot.getOwner(), WidgetTypes.WIDGET_FLAG, tmpPlot.getOwner(), -1)
												# Civ-Button
												else:
														screen.setImageButton("L12_"+str(i), gc.getCivilizationInfo(iCiv).getButton(), 760, iY+24, 24, 24, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, -1)
												szText = gc.getPlayer(tmpPlot.getOwner()).getCivilizationDescription(0)
												screen.setLabel("L13_"+str(i), "Background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
																				790, iY+28, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, -1)


								if bTradeRouteActive:
										# Cancel Button
										screen.setImageButton("L15_"+str(i), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_AUTO_STOP").getPath(),
																					900, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, 748, pUnit.getID())
								else:
										szText = localText.getText("TXT_KEY_TRADE_ADVISOR_INFO3", ())
										screen.setLabel("L6_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, 900+BUTTON_SIZE, iY+14, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

								# ----
								i += 1
								iY += 60

		def refreshScreen(self):
				self.deleteAllWidgets()
				return 0

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
				if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
						if inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData2() != -1:
								pPlayer = gc.getPlayer(CyGame().getActivePlayer())
								pUnit = pPlayer.getUnit(inputClass.getData2())
								if inputClass.getData1() == 1:
										CyCamera().JustLookAtPlot(pUnit.plot())
										CyInterface().selectUnit(pUnit, True, True, True)
										self.hideScreen()
								elif inputClass.getData1() == 748:
										CyMessageControl().sendModNetMessage(748, -1, -1, CyGame().getActivePlayer(), inputClass.getData2())
										CyCamera().JustLookAtPlot(pUnit.plot())
										CyInterface().selectUnit(pUnit, True, True, True)
										self.hideScreen()
				return 0

		def update(self, fDelta):
				return

		def hideScreen(self):
				screen = self.getScreen()
				screen.hideScreen()
