# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
# Created by Pie, Austria
from CvPythonExtensions import (
		CyGlobalContext, CyArtFileMgr, CyTranslator, ButtonStyles,
		FontTypes, FontSymbols, CyGame, CyMap, InterfaceDirtyBits,
		WidgetTypes, PanelStyles, PopupStates, ActivationTypes,
		CyInterface, NotifyCode, CyMessageControl,
		CyCamera)
import CvUtil
if not CvUtil.isPitbossHost():
    	from CvPythonExtensions import CyGInterfaceScreen

# import ScreenInput
import CvScreenEnums
import PAE_Trade

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

				self.iActiveTab = 1
				self.Tab1 = "TAB1"
				self.Tab2 = "TAB2"

				# for TAB 2
				self.X_LEADERS = 20
				self.Y_LEADERS = 60
				self.W_LEADERS = 985
				self.H_LEADERS = 100
				self.LEADER_BUTTON_SIZE = 64
				self.LEADER_MARGIN = 12
				self.X_CITIES = 10
				self.Y_CITIES = 158
				self.W_CITIES = 985
				self.H_CITIES = 556

				self.LEADER_COLUMNS = int(self.W_LEADERS / (self.LEADER_BUTTON_SIZE + self.LEADER_MARGIN))
				self.iShiftKeyDown = 0

				self.iActivePlayer = CyGame().getActivePlayer()

		def getScreen(self):
				return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.TRADEROUTE_ADVISOR2)

		def interfaceScreen(self):

				screen = self.getScreen()

				# Set the background and exit button, and show the screen
				screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

				screen.setRenderInterfaceOnly(True)
				screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

				screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addPanel("TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR)
				screen.addPanel("TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR)

				screen.showWindowBackground(False)
				screen.setText(self.EXIT_ID, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>",
											 CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

				# Header...
				screen.setLabel(self.WIDGET_HEADER, "Background", u"<font=4b>" + localText.getText("TXT_KEY_TRADE_ROUTE2_ADVISOR_SCREEN", ()).upper() + u"</font>",
												CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Bottom: TAB links
				xTAB = 50
				yTAB = 726
				TEXT_TAB1 = u"<font=4>" + localText.getText("TXT_KEY_TRADE_ROUTE_ADVISOR2_TAB1", ()).upper() + "</font>"
				TEXT_TAB1_YELLOW = u"<font=4>" + localText.getColorText("TXT_KEY_TRADE_ROUTE_ADVISOR2_TAB1", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>"
				TEXT_TAB2 = u"<font=4>" + localText.getText("TXT_KEY_TRADE_ROUTE_ADVISOR2_TAB2", ()).upper() + "</font>"
				TEXT_TAB2_YELLOW = u"<font=4>" + localText.getColorText("TXT_KEY_TRADE_ROUTE_ADVISOR2_TAB2", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>"

				if (self.iActiveTab == 2):
						screen.setText(self.Tab1, "", TEXT_TAB1, CvUtil.FONT_LEFT_JUSTIFY, xTAB, yTAB, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.Tab2, "", TEXT_TAB2_YELLOW, CvUtil.FONT_LEFT_JUSTIFY, xTAB+220, yTAB, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				else:
						screen.setText(self.Tab1, "", TEXT_TAB1_YELLOW, CvUtil.FONT_LEFT_JUSTIFY, xTAB, yTAB, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.Tab2, "", TEXT_TAB2, CvUtil.FONT_LEFT_JUSTIFY, xTAB+220, yTAB, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# draw the contents
				self.drawContents()


		def drawContents(self):

				if (self.iActiveTab == 2):
						self.drawTAB2()
				else:
						self.drawTAB1()


		##################### FIRST PAGE ###############################
		def drawTAB1(self):

				screen = self.getScreen()

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
								City1 = None
								City2 = None
								pUnit = lHandelseinheiten[j]
								bTradeRouteActive = int(CvUtil.getScriptData(pUnit, ["autA"], 0))

								screen.addPanel("PanelBG_"+str(i), u"", u"", True, False, 40, iY, 935, 51, PanelStyles.PANEL_STYLE_MAIN_BLACK25)
								iY += 4

								# Button unit
								screen.setImageButton("L1_"+str(i), pUnit.getButton(), 50, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, 1, pUnit.getID())

								# Unit name
								szText = pUnit.getName()
								screen.setLabel("L2_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 100, iY+5, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, 1, pUnit.getID())

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
												City1 = tmpPlot.getPlotCity()
												szText = City1.getName()
												if tmpPlot.getOwner() == CyGame().getActivePlayer():
														iTmpX = 490
												else:
														iTmpX = 520
												screen.setLabel("L4_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, iTmpX, iY+5, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
										if tmpPlot.getOwner() != -1:
												iCiv = gc.getPlayer(tmpPlot.getOwner()).getCivilizationType()
												# Flagge
												if tmpPlot.getOwner() == CyGame().getActivePlayer():
														screen.addFlagWidgetGFC("L5_"+str(i), 500, iY, 24, 54, tmpPlot.getOwner(), WidgetTypes.WIDGET_FLAG, tmpPlot.getOwner(), -1)
												# Civ-Button
												else:
														screen.setImageButton("L5_"+str(i), gc.getCivilizationInfo(iCiv).getButton(), 496, iY+24, 24, 24, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, -1)
												szText = gc.getPlayer(tmpPlot.getOwner()).getCivilizationDescription(0)
												screen.setLabel("L6_"+str(i), "Background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY,
																				490, iY+28, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, -1)

										# Button Bonus 1
										iBonus1 = CvUtil.getScriptData(pUnit, ["autB1"], -1)
										if iBonus1 != -1:
												screen.setImageButton("L7_"+str(i), gc.getBonusInfo(iBonus1).getButton(), 530, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus1, -1)


								szArrowLeft = "Art/Interface/Buttons/button_arrow_left4.dds"
								szArrowRight = "Art/Interface/Buttons/button_arrow_right4.dds"
								# Unit comes from...
								if bTradeRouteActive:
									iFromX = CvUtil.getScriptData(pUnit, ["x"], -1)
									iFromY = CvUtil.getScriptData(pUnit, ["y"], -1)
									if iFromX == iCityX and iFromY == iCityY:
										szArrowRight = "Art/Interface/Buttons/button_arrow_right3.dds"
									else:
										szArrowLeft = "Art/Interface/Buttons/button_arrow_left3.dds"

								# Buttons Arrow to left
								screen.setImageButton("L8_"+str(i), szArrowLeft, 600, iY+9, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1)

								# Promotion Escort / Begleitschutz
								iPromo = gc.getInfoTypeForString("PROMOTION_SCHUTZ")
								if pUnit.isHasPromotion(iPromo):
										screen.setImageButton("L14_"+str(i), gc.getPromotionInfo(iPromo).getButton(), 635, iY+9, 32, 32, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, iPromo, -1)

								# Button Arrow to right
								screen.setImageButton("L9_"+str(i), szArrowRight, 670, iY+9, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1)


								# City 2
								if bTradeRouteActive:
										iCityX = int(CvUtil.getScriptData(pUnit, ["autX2"], -1))
										iCityY = int(CvUtil.getScriptData(pUnit, ["autY2"], -1))
								
										# Button Bonus 2
										iBonus2 = CvUtil.getScriptData(pUnit, ["autB2"], -1)
										if iBonus2 != -1:
												screen.setImageButton("L10_"+str(i), gc.getBonusInfo(iBonus2).getButton(), 720, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus2, -1)

										tmpPlot = CyMap().plot(iCityX, iCityY)
										if tmpPlot and not tmpPlot.isNone() and tmpPlot.isCity():
												City2 = tmpPlot.getPlotCity()
												szText = City2.getName()
												if tmpPlot.getOwner() == CyGame().getActivePlayer():
														iTmpX = 810
												else:
														iTmpX = 780
												screen.setLabel("L11_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iTmpX, iY+5, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
										if tmpPlot.getOwner() != -1:
												iCiv = gc.getPlayer(tmpPlot.getOwner()).getCivilizationType()
												# Flagge
												if tmpPlot.getOwner() == CyGame().getActivePlayer():
														screen.addFlagWidgetGFC("L12_"+str(i), 776, iY, 24, 54, tmpPlot.getOwner(), WidgetTypes.WIDGET_FLAG, tmpPlot.getOwner(), -1)
												# Civ-Button
												else:
														screen.setImageButton("L12_"+str(i), gc.getCivilizationInfo(iCiv).getButton(), 780, iY+24, 24, 24, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, -1)
												szText = gc.getPlayer(tmpPlot.getOwner()).getCivilizationDescription(0)
												screen.setLabel("L13_"+str(i), "Background", u"<font=2>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
																				810, iY+28, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, -1)

										# Profit ausrechnen
										iProfit1 = PAE_Trade.calcBonusProfit(City1, City2, iBonus1, pUnit) # Bonus 1
										iProfit2 = PAE_Trade.calcBonusProfit(City2, City1, iBonus2, pUnit) # möglicher Bonus hier
										iProfit = iProfit1 + iProfit2
										szText = localText.getText("TXT_KEY_TRADE_ADVISOR_INFO4", (iProfit,))
										screen.setLabel("L16_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, 350, iY+24, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

								if bTradeRouteActive:
										# Cancel Button
										screen.setImageButton("L15_"+str(i), ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_AUTO_STOP").getPath(),
																					920, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, 748, pUnit.getID())
								else:
										szText = localText.getText("TXT_KEY_TRADE_ADVISOR_INFO3", ())
										screen.setLabel("L6_"+str(i), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, 920+BUTTON_SIZE, iY+14, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

								# ----
								i += 1
								iY += 60


		##################### SECOND PAGE (idea by Rob Anybody) ###############################
		def drawTAB2(self):

				# Danke Ramk!
				if (self.iActivePlayer < 0): self.iActivePlayer = CyGame().getActivePlayer()

				screen = self.getScreen()

				# area for leaders
				screen.addPanel("LeaderPanel", "", "", False, True, self.X_LEADERS, self.Y_LEADERS, self.W_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_DAWNTOP)

				# scroll panel for leaders
				screen.addScrollPanel("ScrollPanelLeaders", u"", self.X_LEADERS, self.Y_LEADERS-16, self.W_LEADERS, self.H_LEADERS-10, PanelStyles.PANEL_STYLE_EXTERNAL)
				screen.setActivation("ScrollPanelLeaders", ActivationTypes.ACTIVATE_NORMAL)

				# area for city buttons
				screen.addPanel("CityPanel", "", "", True, True, self.X_CITIES, self.Y_CITIES, self.W_CITIES, self.H_CITIES, PanelStyles.PANEL_STYLE_MAIN_BLACK25)

				# Leaders Tab
				self.drawLeaders()

				# Cities Tab
				self.drawCities(self.iActivePlayer)

		def drawLeaders(self):

				screen = self.getScreen()
				listLeaders = []
				for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						player = gc.getPlayer(iLoopPlayer)
						if player.isBarbarian(): continue
						if (player.isAlive() and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam()) or gc.getGame().isDebugMode())):
								listLeaders.append(iLoopPlayer)

				# loop through all players and display leaderheads
				iIndex = -1
				for iLoopPlayer in listLeaders:
						iIndex += 1
						x = self.X_LEADERS + iIndex * (self.LEADER_BUTTON_SIZE + self.LEADER_MARGIN)
						screen.addCheckBoxGFCAt("ScrollPanelLeaders", "Leader"+str(iLoopPlayer), gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton(), "",
						x, 20, self.LEADER_BUTTON_SIZE, self.LEADER_BUTTON_SIZE, WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer, -1, ButtonStyles.BUTTON_STYLE_LABEL, False)

		def drawCities(self, iPlayer):

				self.deleteAllWidgets()
				screen = self.getScreen()

				player = gc.getPlayer(iPlayer)
				iTeam = gc.getPlayer(self.iActivePlayer).getTeam()
				BUTTON_SIZE = 48
				iY = self.Y_CITIES
				i = 0

				# scroll panel for cities
				screen.addScrollPanel("ScrollPanelCities", u"", self.X_CITIES, self.Y_CITIES+4, self.W_CITIES, self.H_CITIES-40, PanelStyles.PANEL_STYLE_EXTERNAL)
				screen.setActivation("ScrollPanelCities", ActivationTypes.ACTIVATE_NORMAL)

				pCapital = False
				lCities = []
				(loopCity, pIter) = player.firstCity(False)
				if loopCity is not None and not loopCity.isNone():
					while loopCity:
						if not loopCity.isNone() and loopCity.getOwner() == iPlayer:
							if loopCity.isRevealed(iTeam, 0):
								if loopCity.isCapital():
									pCapital = (loopCity.getName(),loopCity.getID())
								else:
									lCities.append((loopCity.getName(),loopCity.getID()))
						(loopCity, pIter) = player.nextCity(pIter, False)

				lCities.sort()
				if pCapital: lCities.insert(0,pCapital)

				for lCity in lCities:
					loopCity = player.getCity(lCity[1])

					iX = self.X_CITIES
					iY = 0+i*54


					# Symbol: Stern: Capital (gold) or provincial palace (silver)
					if loopCity.isCapital():
						screen.setLabelAt(self.getNextWidgetName(), "ScrollPanelCities", u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR),
						CvUtil.FONT_LEFT_JUSTIFY, iX+2, iY+4, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					elif loopCity.isGovernmentCenter():
						screen.setLabelAt(self.getNextWidgetName(), "ScrollPanelCities", u"%c" % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR),
						CvUtil.FONT_LEFT_JUSTIFY, iX+2, iY+4, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

					# Hafenstadt (Icons)
					if loopCity.isCoastal(4):
						screen.addDDSGFCAt(self.getNextWidgetName(), "ScrollPanelCities", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TRADE_ICON_ANKER").getPath(),
						iX, iY+20, 22, 22, WidgetTypes.WIDGET_GENERAL, -1, -1, False)


					# City status (button)
					buttonCityStatus = self.getButtonCityStatus(loopCity)
					screen.addCheckBoxGFCAt("ScrollPanelCities", self.getNextWidgetName(), buttonCityStatus, "",
					iX+22, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, iPlayer, loopCity.getID(), ButtonStyles.BUTTON_STYLE_LABEL, False)


					iX += 22 + BUTTON_SIZE + 4
					# City name
					szText = self.getCityName(loopCity)
					screen.setLabelAt(self.getNextWidgetName(), "ScrollPanelCities", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iX, iY+2, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

					# City properties
					szText = self.getCityProperties(loopCity)
					screen.setLabelAt(self.getNextWidgetName(), "ScrollPanelCities", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iX, iY+22, 0.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)


					iX += 110
					# Button Muster für Bonusresis
					lGoods = PAE_Trade.getCitySaleableGoods(loopCity, self.iActivePlayer)
					if len(lGoods):
						for iBonus in lGoods:
							iX += BUTTON_SIZE + 2
							screen.addDDSGFCAt(self.getNextWidgetName(), "ScrollPanelCities", gc.getBonusInfo(iBonus).getButton(), iX, iY, BUTTON_SIZE, BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1, False)


					i += 1
					iY += 60


		def getButtonCityStatus(self, pLoopCity):
				iBuildingSiedlung = gc.getInfoTypeForString("BUILDING_SIEDLUNG")
				iBuildingKolonie = gc.getInfoTypeForString("BUILDING_KOLONIE")
				iBuildingCity = gc.getInfoTypeForString("BUILDING_STADT")
				iBuildingProvinz = gc.getInfoTypeForString("BUILDING_PROVINZ")
				iBuildingMetropole = gc.getInfoTypeForString("BUILDING_METROPOLE")
				iCivilWar = gc.getInfoTypeForString("BUILDING_CIVIL_WAR")
				if pLoopCity.getNumRealBuilding(iBuildingMetropole):
						if pLoopCity.getOccupationTimer() or pLoopCity.getNumRealBuilding(iCivilWar):
							return "Art/Interface/Buttons/General/button_riot_city_stufe5.dds"
						else:
							return gc.getBuildingInfo(iBuildingMetropole).getButton()
				elif pLoopCity.getNumRealBuilding(iBuildingProvinz):
						if pLoopCity.getOccupationTimer() or pLoopCity.getNumRealBuilding(iCivilWar):
							return "Art/Interface/Buttons/General/button_riot_city_stufe4.dds"
						else:
							return gc.getBuildingInfo(iBuildingProvinz).getButton()
				elif pLoopCity.getNumRealBuilding(iBuildingCity):
						if pLoopCity.getOccupationTimer() or pLoopCity.getNumRealBuilding(iCivilWar):
							return "Art/Interface/Buttons/General/button_riot_city_stufe3.dds"
						else:
							return gc.getBuildingInfo(iBuildingCity).getButton()
				elif pLoopCity.getNumRealBuilding(iBuildingKolonie):
						if pLoopCity.getOccupationTimer() or pLoopCity.getNumRealBuilding(iCivilWar):
							return "Art/Interface/Buttons/General/button_riot_city_stufe2.dds"
						else:
							return gc.getBuildingInfo(iBuildingKolonie).getButton()
				else:
						if pLoopCity.getOccupationTimer() or pLoopCity.getNumRealBuilding(iCivilWar):
							return "Art/Interface/Buttons/General/button_riot_city_stufe1.dds"
						else:
							return gc.getBuildingInfo(iBuildingSiedlung).getButton()

		def getCityName(self, pLoopCity):
				szName = u""

				# City name: font-color: white (normal), red (riot/civil war)
				if pLoopCity.getNumRealBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")) or pLoopCity.getOccupationTimer():
						szName += localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + pLoopCity.getName() + localText.getText("TXT_KEY_COLOR_REVERT", ())
				else:
						szName += pLoopCity.getName()

				return szName

		def getCityProperties(self, pLoopCity):
				szName = u""

				# City name: font-color: white (normal), red (riot/civil war)
				if pLoopCity.getNumRealBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")) or pLoopCity.getOccupationTimer():
						szName += u"%c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)

				# Symbol: Religion
				for iReligion in range(gc.getNumReligionInfos()):
						if pLoopCity.isHasReligion(iReligion):
								if pLoopCity.isHolyCityByType(iReligion):
										szName += u"%c" % gc.getReligionInfo(iReligion).getHolyCityChar()
								else:
										szName += u"%c" % gc.getReligionInfo(iReligion).getChar()

				# Symbol: Kult
				for iCorporation in range(gc.getNumCorporationInfos()):
						if pLoopCity.isHeadquartersByType(iCorporation):
								szName += u"%c" % gc.getCorporationInfo(iCorporation).getHeadquarterChar()
						elif pLoopCity.isActiveCorporation(iCorporation):
								szName += u"%c" % gc.getCorporationInfo(iCorporation).getChar()

				return szName

		# ---- END SECOND PAGE ------------------



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
						if inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL:

								szWidgetName = inputClass.getFunctionName() + str(inputClass.getID())

								if (szWidgetName == self.Tab1):
										self.iActiveTab = 1
										self.interfaceScreen()
								elif (szWidgetName == self.Tab2):
										self.iActiveTab = 2
										self.interfaceScreen()

								elif self.iActiveTab == 1 and inputClass.getData2() != -1:
										pPlayer = gc.getPlayer(CyGame().getActivePlayer())
										pUnit = pPlayer.getUnit(inputClass.getData2())
										if inputClass.getData1() == 1:
												CyCamera().JustLookAtPlot(pUnit.plot())
												CyInterface().selectUnit(pUnit, True, True, True)
												self.hideScreen()
												return
										elif inputClass.getData1() == 748:
												CyMessageControl().sendModNetMessage(748, -1, -1, CyGame().getActivePlayer(), inputClass.getData2())
												CyCamera().JustLookAtPlot(pUnit.plot())
												CyInterface().selectUnit(pUnit, True, True, True)
												self.hideScreen()
												return

								elif self.iActiveTab == 2 and inputClass.getData1() != -1 and inputClass.getData2() != -1:
										pPlayer = gc.getPlayer(inputClass.getData1())
										pCity = pPlayer.getCity(inputClass.getData2())
										CyCamera().JustLookAtPlot(pCity.plot())
										self.hideScreen()
										return

						elif inputClass.getButtonType() == WidgetTypes. WIDGET_LEADERHEAD:
								if self.iActiveTab == 2:
										self.drawCities(inputClass.getData1())
										return

#				elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
#						if (inputClass.getData() == int(InputTypes.KB_LSHIFT) or inputClass.getData() == int(InputTypes.KB_RSHIFT)):
#								self.iShiftKeyDown = inputClass.getID()

				return 0

		def update(self, fDelta):
				return

		def hideScreen(self):
				screen = self.getScreen()
				screen.hideScreen()
