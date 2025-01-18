# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
																FontTypes, NotifyCode, WidgetTypes, PanelStyles,
																CyInterface, InterfaceDirtyBits, CyGame, CyCamera,
																CyGInterfaceScreen, CommerceTypes, CyMessageControl,
																PopupStates, ButtonPopupTypes, CyPopupInfo,
																ButtonStyles, FontSymbols, ControlTypes,
																YieldTypes, TableStyles, ChatTargetTypes)
import CvUtil
# import ScreenInput
import CvScreenEnums
import PAE_Cultivation
import PAE_Vassal
#import PAE_Lists as L <= geht hier nicht ;(

# TODO remove
# DEBUG code for Python 3 linter
# unicode = str
# xrange = range

# IMPORTANT INFORMATION
#
# All widget names MUST be unique when creating screens.  If you create
# a widget named 'Hello', and then try to create another named 'Hello', it
# will modify the first hello.
#
# Also, when attaching widgets, 'Background' is a reserve word meant for
# the background widget.  Do NOT use 'Background' to name any widget, but
# when attaching to the background, please use the 'Background' keyword.
#  Thanks to Lee Reeves, AKA Taelis on civfanatics.com
#  Thanks to Solver

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvDomesticAdvisor:
		"Domestic Advisor Screen"

		def __init__(self):
				self.listSelectedCities = []

				self.WIDGET_ID = "DomesticScreenWidget"
				self.nWidgetCount = 0
				self.iActiveTab = 1

		# Screen construction function

		def interfaceScreen(self):

				player = gc.getPlayer(gc.getGame().getActivePlayer())

				# Create a new screen, called DomesticAdvisor, using the file CvDomesticAdvisor.py for input
				screen = self.getScreen()

				self.nScreenWidth = screen.getXResolution() - 30
				self.nScreenHeight = screen.getYResolution() - 210
				self.nTableWidth = self.nScreenWidth - 85  # 35
				if self.iActiveTab in [2,4,5]:
						self.nTableHeight = self.nScreenHeight - 125
				else:
						self.nTableHeight = self.nScreenHeight - 85
				self.nNormalizedTableWidth = 970

				self.nFirstSpecialistX = 30
				self.nSpecialistY = self.nScreenHeight - 55
				self.nSpecialistWidth = 32
				self.nSpecialistLength = 32
				self.nSpecialistDistance = 100

				# Offset from Specialist Image/Size for the Specialist Plus/Minus buttons
				self.nPlusOffsetX = -4
				self.nMinusOffsetX = 16
				self.nPlusOffsetY = self.nMinusOffsetY = 30
				self.nPlusHeight = 20
				self.nPlusWidth = self.nMinusWidth = self.nMinusHeight = 20

				# Offset from Specialist Image for the Specialist Text
				self.nSpecTextOffsetX = 40
				self.nSpecTextOffsetY = 10

				screen.setRenderInterfaceOnly(True)
				screen.setDimensions(15, 50, self.nScreenWidth, self.nScreenHeight)  # 15, 100
				screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

				# Here we set the background widget and exit button, and we show the screen
				screen.addPanel("DomesticAdvisorBG", u"", u"", True, False, 0, 0, self.nScreenWidth, self.nScreenHeight, PanelStyles.PANEL_STYLE_MAIN)
				screen.setText("DomesticExit", "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY,
											 self.nScreenWidth - 25, self.nScreenHeight - 45, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
				# PB Mod Unpause MOD
				if CyGame().isPitboss():
						screen.setText("DomesticUnpause", "Background", localText.getText("TXT_KEY_MOD_UNPAUSE", ()).upper(), CvUtil.FONT_LEFT_JUSTIFY, 25, self.nScreenHeight - 45, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 301311, 2013 )

				# PAE: Page 2 for Slave Buildings
				# PAE: Page 3 for Cultivation
				# PAE: Page 4 for Specialists
				# PAE: Page 5 for Great Generals
				self.Y_TAB1 = 135
				self.Y_TAB2 = 205
				self.Y_TAB3 = 275
				self.Y_TAB4 = 345
				self.Y_TAB5 = 415
				self.Y_TAB6 = 485
				self.X_TABS = 40
				self.TEXT_TAB1 = u"<font=1>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_TAB1", ()) + u"</font>"
				self.TEXT_TAB2 = u"<font=1>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_TAB2", ()) + u"</font>"
				self.TEXT_TAB3 = u"<font=1>" + localText.getText("TXT_KEY_TECH_KULTIVIERUNG", ()) + u"</font>"
				self.TEXT_TAB4 = u"<font=1>" + localText.getText("TXT_KEY_LABEL_SPECIALISTS", ()) + u"</font>"
				self.TEXT_TAB5 = u"<font=1>" + localText.getText("TXT_KEY_LABEL_GENERALS", ()) + u"</font>"
				self.TEXT_TAB6 = u"<font=1>" + localText.getText("TXT_KEY_LABEL_BUILDING_PROMO", ()) + u"</font>"
				self.TEXT_TAB1_YELLOW = u"<font=1>" + localText.getColorText("TXT_KEY_DOMESTIC_ADVISOR_TAB1", (), gc.getInfoTypeForString("COLOR_YELLOW")) + u"</font>"
				self.TEXT_TAB2_YELLOW = u"<font=1>" + localText.getColorText("TXT_KEY_DOMESTIC_ADVISOR_TAB2", (), gc.getInfoTypeForString("COLOR_YELLOW")) + u"</font>"
				self.TEXT_TAB3_YELLOW = u"<font=1>" + localText.getColorText("TXT_KEY_TECH_KULTIVIERUNG", (), gc.getInfoTypeForString("COLOR_YELLOW")) + u"</font>"
				self.TEXT_TAB4_YELLOW = u"<font=1>" + localText.getColorText("TXT_KEY_LABEL_SPECIALISTS", (), gc.getInfoTypeForString("COLOR_YELLOW")) + u"</font>"
				self.TEXT_TAB5_YELLOW = u"<font=1>" + localText.getColorText("TXT_KEY_LABEL_GENERALS", (), gc.getInfoTypeForString("COLOR_YELLOW")) + u"</font>"
				self.TEXT_TAB6_YELLOW = u"<font=1>" + localText.getColorText("TXT_KEY_LABEL_BUILDING_PROMO", (), gc.getInfoTypeForString("COLOR_YELLOW")) + u"</font>"

				self.deleteAllWidgets()

				self.szTab1a = self.getNextWidgetName()
				self.szTab1b = self.getNextWidgetName()
				self.szTab2a = self.getNextWidgetName()
				self.szTab2b = self.getNextWidgetName()
				self.szTab3a = self.getNextWidgetName()
				self.szTab3b = self.getNextWidgetName()
				self.szTab4a = self.getNextWidgetName()
				self.szTab4b = self.getNextWidgetName()
				self.szTab5a = self.getNextWidgetName()
				self.szTab5b = self.getNextWidgetName()
				self.szTab6a = self.getNextWidgetName()
				self.szTab6b = self.getNextWidgetName()
				screen.setImageButton(self.szTab1a, "Art/Interface/Buttons/Actions/button_emigrant.dds", 18, 90, 46, 46, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButton(self.szTab2a, gc.getSpecialistInfo(gc.getInfoTypeForString("SPECIALIST_SLAVE")).getButton(), 18, 160, 46, 46, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButton(self.szTab3a, "Art/Interface/Buttons/Actions/button_bonusverbreitung.dds", 18, 230, 46, 46, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButton(self.szTab4a, gc.getSpecialistInfo(gc.getInfoTypeForString("SPECIALIST_ENGINEER")).getButton(), 18, 300, 46, 46, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButton(self.szTab5a, gc.getSpecialistInfo(gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL")).getButton(), 18, 370, 46, 46, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setImageButton(self.szTab6a, gc.getPromotionInfo(gc.getInfoTypeForString("PROMOTION_COMBAT5")).getButton(), 18, 440, 46, 46, WidgetTypes.WIDGET_GENERAL, -1, -1)
				# Draw Tab buttons and tabs
				if (self.iActiveTab == 1):
						screen.setText(self.szTab1b, "", self.TEXT_TAB1_YELLOW, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB1, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab2b, "", self.TEXT_TAB2, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab3b, "", self.TEXT_TAB3, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab4b, "", self.TEXT_TAB4, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB4, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab5b, "", self.TEXT_TAB5, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB5, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab6b, "", self.TEXT_TAB6, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB6, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				elif (self.iActiveTab == 2):
						screen.setText(self.szTab1b, "", self.TEXT_TAB1, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB1, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab2b, "", self.TEXT_TAB2_YELLOW, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab3b, "", self.TEXT_TAB3, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab4b, "", self.TEXT_TAB4, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB4, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab5b, "", self.TEXT_TAB5, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB5, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab6b, "", self.TEXT_TAB6, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB6, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				elif (self.iActiveTab == 3):
						screen.setText(self.szTab1b, "", self.TEXT_TAB1, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB1, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab2b, "", self.TEXT_TAB2, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab3b, "", self.TEXT_TAB3_YELLOW, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab4b, "", self.TEXT_TAB4, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB4, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab5b, "", self.TEXT_TAB5, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB5, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab6b, "", self.TEXT_TAB6, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB6, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				elif (self.iActiveTab == 4):
						screen.setText(self.szTab1b, "", self.TEXT_TAB1, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB1, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab2b, "", self.TEXT_TAB2, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab3b, "", self.TEXT_TAB3, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab4b, "", self.TEXT_TAB4_YELLOW, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB4, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab5b, "", self.TEXT_TAB5, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB5, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab6b, "", self.TEXT_TAB6, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB6, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				elif (self.iActiveTab == 5):
						screen.setText(self.szTab1b, "", self.TEXT_TAB1, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB1, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab2b, "", self.TEXT_TAB2, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab3b, "", self.TEXT_TAB3, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab4b, "", self.TEXT_TAB4, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB4, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab5b, "", self.TEXT_TAB5_YELLOW, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB5, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab6b, "", self.TEXT_TAB6, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB6, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				elif (self.iActiveTab == 6):
						screen.setText(self.szTab1b, "", self.TEXT_TAB1, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB1, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab2b, "", self.TEXT_TAB2, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB2, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab3b, "", self.TEXT_TAB3, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab4b, "", self.TEXT_TAB4, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB4, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab5b, "", self.TEXT_TAB5, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB5, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.setText(self.szTab6b, "", self.TEXT_TAB6_YELLOW, CvUtil.FONT_CENTER_JUSTIFY, self.X_TABS, self.Y_TAB6, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				bCanLiberate = False
				(loopCity, iter) = player.firstCity(False)
				while(loopCity):
						# if not loopCity.isNone() and loopCity.getOwner() == player.getID(): #only valid cities
						if loopCity.getLiberationPlayer(False) != -1:
								bCanLiberate = True
								break
						(loopCity, iter) = player.nextCity(iter, False)

				if (bCanLiberate or player.canSplitEmpire()):
						screen.setImageButton("DomesticSplit", "", self.nScreenWidth - 180, self.nScreenHeight - 45, 28, 28,
																	WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FREE_COLONY).getActionInfoIndex(), -1)
						screen.setStyle("DomesticSplit", "Button_HUDAdvisorVictory_Style")

				# Erase the flag?
				CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, True)

				# Draw the city list
				self.drawContents()

		# Function to draw the contents of the cityList passed in
		def drawContents(self):

				# Get the screen and the player
				screen = self.getScreen()
				player = gc.getPlayer(CyGame().getActivePlayer())

				screen.moveToFront("Background")

				# Build the table
				if (self.iActiveTab == 6):
						screen.addTableControlGFC("CityListBackground", 12, 78, 61, self.nTableWidth, self.nTableHeight - 50, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				elif (self.iActiveTab == 5):
						screen.addTableControlGFC("CityListBackground", 12, 78, 61, self.nTableWidth, self.nTableHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				elif (self.iActiveTab == 4):
						screen.addTableControlGFC("CityListBackground", gc.getNumSpecialistInfos()+3, 78, 61, self.nTableWidth, self.nTableHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				elif (self.iActiveTab == 3):
						screen.addTableControlGFC("CityListBackground", len(self.getBonuses())+2, 78, 21, self.nTableWidth, self.nTableHeight - 25, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				elif (self.iActiveTab == 2):
						screen.addTableControlGFC("CityListBackground", 18, 78, 61, self.nTableWidth, self.nTableHeight - 25, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				else:
						screen.addTableControlGFC("CityListBackground", 21, 78, 21, self.nTableWidth, self.nTableHeight, True, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect("CityListBackground", True)
				screen.enableSort("CityListBackground")
				screen.setStyle("CityListBackground", "Table_StandardCiv_Style")

				# Loop through the cities
				i = 0
				(loopCity, iter) = player.firstCity(False)
				while loopCity:
						# if not loopCity.isNone() and loopCity.getOwner() == player.getID(): #only valid cities
						screen.appendTableRow("CityListBackground")
						if (loopCity.getName() in self.listSelectedCities):
								screen.selectRow("CityListBackground", i, True)
						if (self.iActiveTab == 6):
								self.updateTable6(loopCity, i)
						elif (self.iActiveTab == 5):
								self.updateTable5(loopCity, i)
						elif (self.iActiveTab == 4):
								self.updateTable4(loopCity, i)
						elif (self.iActiveTab == 3):
								self.updateTable3(loopCity, i)
						elif (self.iActiveTab == 2):
								self.updateTable2(loopCity, i)
						else:
								self.updateTable(loopCity, i)
						i += 1
						(loopCity, iter) = player.nextCity(iter, False)

				if (self.iActiveTab == 6):
						self.drawHeaders6()
				elif (self.iActiveTab == 5):
						self.drawHeaders5()
				elif (self.iActiveTab == 4):
						self.drawHeaders4()
				elif (self.iActiveTab == 3):
						self.drawHeaders3()
				elif (self.iActiveTab == 2):
						self.drawHeaders2()
				else:
						self.drawHeaders()

				self.drawSpecialists()

				screen.moveToBack("DomesticAdvisorBG")

				self.updateAppropriateCitySelection()

				CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)

		# ################### PAGE 1 ###################################

		def drawHeaders(self):

				# Get the screen and the player
				screen = self.getScreen()

				iPlayer = CyGame().getActivePlayer()
				pTeam = gc.getTeam(gc.getPlayer(iPlayer).getTeam())

				# PAE Untere Buttons
				if pTeam.isHasTech(gc.getInfoTypeForString("TECH_SOELDNERTUM")):
								screen.setImageButton(self.getNextWidgetName(), "Art/Interface/Buttons/Actions/button_action_mercenary_assign.dds", 80, self.nScreenHeight - 60, 46, 46, WidgetTypes.WIDGET_GENERAL, 709, -1)

				if pTeam.isHasTech(gc.getInfoTypeForString("TECH_VASALLENTUM")):
						if len(PAE_Vassal.getVassals(iPlayer)):
								screen.setImageButton(self.getNextWidgetName(), "Art/Interface/Buttons/Civics/civic_buerger.dds", 140, self.nScreenHeight - 60, 46, 46, WidgetTypes.WIDGET_GENERAL, 764, 764)

				# Zoom to City
				screen.setTableColumnHeader("CityListBackground", 0, "", (20 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Name Column
				screen.setTableColumnHeader("CityListBackground", 1, "<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()) + "</font>", (120 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Population Column
				# BTS: localText.getText("TXT_KEY_POPULATION", ())
				screen.setTableColumnHeader("CityListBackground", 2, "<font=2>" + u"%c" % CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR) + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Cultivation status
				screen.setTableColumnHeader("CityListBackground", 3, "<font=2>" + (u"%c" % gc.getBonusInfo(gc.getInfoTypeForString("BONUS_COW")).getChar()) +
																		"</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Settled Slaves Column
				screen.setTableColumnHeader("CityListBackground", 4, "<font=2>" + (u"%c" % gc.getBonusInfo(gc.getInfoTypeForString("BONUS_SLAVES")).getChar()) +
																		"</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Settled Glads Column
				screen.setTableColumnHeader("CityListBackground", 5, "<font=2>" + u"%c" % gc.getBonusInfo(gc.getInfoTypeForString("BONUS_BRONZE")
																																																	).getChar() + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Happiness Column
				screen.setTableColumnHeader("CityListBackground", 6, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)) + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Health Column
				screen.setTableColumnHeader("CityListBackground", 7, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)) + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Food Column
				screen.setTableColumnHeader("CityListBackground", 8, "<font=2>" + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()) + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Production Column
				screen.setTableColumnHeader("CityListBackground", 9, "<font=2>" + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()) +
																		"</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Gold Column
				screen.setTableColumnHeader("CityListBackground", 10, "<font=2>" + (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()) +
																		"</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Maintenance Column
				screen.setTableColumnHeader("CityListBackground", 11, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.BAD_GOLD_CHAR)) + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Research Column
				szText = u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
				screen.setTableColumnHeader("CityListBackground", 12, "<font=2>" + szText, (40 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Espionage Column
				szText = u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
				screen.setTableColumnHeader("CityListBackground", 13, "<font=2>" + szText, (40 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Culture Column
				screen.setTableColumnHeader("CityListBackground", 14, "<font=2>" + (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()) +
																		"</font>", (60 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Trade Column
				screen.setTableColumnHeader("CityListBackground", 15, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.TRADE_CHAR)) + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Great Person Column
				screen.setTableColumnHeader("CityListBackground", 16, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR)) +
																		"</font>", (70 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Garrison Column
				screen.setTableColumnHeader("CityListBackground", 17, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR)) + "</font>", (35 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Production Column
				screen.setTableColumnHeader("CityListBackground", 18, "<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_PRODUCING", ()) +
																		"</font>", (105 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Liberate Column
				screen.setTableColumnHeader("CityListBackground", 19, "", (25 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Stop Growth Column
				screen.setTableColumnHeader("CityListBackground", 20, "<font=2>" + localText.getText("TXT_KEY_DOM_ADVISOR_GROWTH1", ()) + "</font>", (90 * self.nTableWidth) / self.nNormalizedTableWidth)

		def updateTable(self, pLoopCity, i):

				screen = self.getScreen()

				# City status (button)
				buttonCityStatus = self.getButtonCityStatus(pLoopCity)

				# BTS: buttonCityStatus = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath()
				screen.setTableText("CityListBackground", 0, i, "", buttonCityStatus, WidgetTypes.WIDGET_ZOOM_CITY, pLoopCity.getOwner(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)

				# City Name
				szName = self.getCityName(pLoopCity)
				screen.setTableText("CityListBackground", 1, i, szName, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Population
				screen.setTableInt("CityListBackground", 2, i, unicode(pLoopCity.getPopulation()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Cultivation status
				iAnz1 = PAE_Cultivation.getCityCultivatedBonuses(pLoopCity,0)
				iAnz2 = PAE_Cultivation.getCityCultivationAmount(pLoopCity,0)
				text = u"%d/%d" % (iAnz1, iAnz2) # Limit bei CityStatus
				if iAnz1 < iAnz2: text = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + text + localText.getText("TXT_KEY_COLOR_REVERT", ())
				#text = u"%d" % PAE_Cultivation.getCityCultivatedBonuses(pLoopCity, -1)
				screen.setTableInt("CityListBackground", 3, i, text, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Settled Slaves
				iCitySlaves1 = pLoopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"))
				iCitySlaves2 = pLoopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD"))
				iCitySlaves3 = pLoopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD"))
				text = u"%d/%d/%d" % (iCitySlaves1, iCitySlaves2, iCitySlaves3)
				screen.setTableInt("CityListBackground", 4, i, text, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Settled Gladiators
				iCityGlads = pLoopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GLADIATOR"))
				screen.setTableInt("CityListBackground", 5, i, unicode(iCityGlads), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Happiness
				iNetHappy = pLoopCity.happyLevel() - pLoopCity.unhappyLevel(0)
				szText = unicode(iNetHappy)
				if iNetHappy > 0:
						szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
				elif iNetHappy < 0:
						szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
				screen.setTableInt("CityListBackground", 6, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Health
				iNetHealth = pLoopCity.goodHealth() - pLoopCity.badHealth(0)
				szText = unicode(iNetHealth)
				if iNetHealth > 0:
						szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
				elif iNetHealth < 0:
						szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
				screen.setTableInt("CityListBackground", 7, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Food status
				iNetFood = pLoopCity.foodDifference(True)

				# PAE city supply
				#pCityPlot = gc.getMap().plot( pLoopCity.getX(), pLoopCity.getY() )
				#iCityMaintainUnits = (pCityPlot.getNumDefenders(pLoopCity.getOwner()) - (pLoopCity.getPopulation() * 2)) / 2
				#if iCityMaintainUnits > 0: iNetFood -= iCityMaintainUnits

				szText = unicode(iNetFood)
				if iNetFood > 0:
						szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
				elif iNetFood < 0:
						szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
				screen.setTableInt("CityListBackground", 8, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Production status
				screen.setTableInt("CityListBackground", 9, i, unicode(pLoopCity.getYieldRate(YieldTypes.YIELD_PRODUCTION)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Gold and Maintainance
				iGold = pLoopCity.getCommerceRate(CommerceTypes.COMMERCE_GOLD)
				iMaintenance = pLoopCity.getMaintenance()

				# Gold status
				if iGold > iMaintenance:
						szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + unicode(iGold-iMaintenance) + localText.getText("TXT_KEY_COLOR_REVERT", ())
				else:
						szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + unicode(iGold-iMaintenance) + localText.getText("TXT_KEY_COLOR_REVERT", ())
				screen.setTableInt("CityListBackground", 10, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Maintenance
				if iMaintenance > iGold:
						szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + unicode(iMaintenance) + localText.getText("TXT_KEY_COLOR_REVERT", ())
				else:
						szText = unicode(iMaintenance)
				screen.setTableInt("CityListBackground", 11, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Science rate
				screen.setTableInt("CityListBackground", 12, i, unicode(pLoopCity.getCommerceRate(CommerceTypes.COMMERCE_RESEARCH)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Espionage rate
				screen.setTableInt("CityListBackground", 13, i, unicode(pLoopCity.getCommerceRate(CommerceTypes.COMMERCE_ESPIONAGE)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Culture status
				szCulture = unicode(pLoopCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE))
				iCultureTimes100 = pLoopCity.getCultureTimes100(CyGame().getActivePlayer())
				iCultureRateTimes100 = pLoopCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
				if iCultureRateTimes100 > 0:
						iCultureLeftTimes100 = 100 * pLoopCity.getCultureThreshold() - iCultureTimes100
						if iCultureLeftTimes100 > 0:
								szCulture += u" (" + unicode((iCultureLeftTimes100 + iCultureRateTimes100 - 1) / iCultureRateTimes100) + u")"

				screen.setTableInt("CityListBackground", 14, i, szCulture, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Trade
				screen.setTableInt("CityListBackground", 15, i, unicode(pLoopCity.getTradeYield(YieldTypes.YIELD_COMMERCE)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Great Person
				iGreatPersonRate = pLoopCity.getGreatPeopleRate()
				szGreatPerson = unicode(iGreatPersonRate)
				if iGreatPersonRate > 0:
						iGPPLeft = gc.getPlayer(gc.getGame().getActivePlayer()).greatPeopleThreshold(False) - pLoopCity.getGreatPeopleProgress()
						if iGPPLeft > 0:
								iTurnsLeft = iGPPLeft / pLoopCity.getGreatPeopleRate()
								if iTurnsLeft * pLoopCity.getGreatPeopleRate() < iGPPLeft:
										iTurnsLeft += 1
								szGreatPerson += u" (" + unicode(iTurnsLeft) + u")"

				screen.setTableInt("CityListBackground", 16, i, szGreatPerson, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Garrison
				screen.setTableInt("CityListBackground", 17, i, unicode(pLoopCity.plot().getNumDefenders(pLoopCity.getOwner())), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Producing
				screen.setTableText("CityListBackground", 18, i, pLoopCity.getProductionName() + " (" + str(pLoopCity.getGeneralProductionTurnsLeft()) + ")",
														"", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				szText = u""
				# Capital
				if pLoopCity.isCapital():
						szText += u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)
				# Provincial Palace
				if pLoopCity.isGovernmentCenter():
						szText += u"%c" % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR)
				# City riot / civil war
				if pLoopCity.getOccupationTimer():
						szText += u"%c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)
				# Liberation
				if pLoopCity.getLiberationPlayer(False) != -1:
						szText += u"%c" % CyGame().getSymbolID(FontSymbols.MAP_CHAR)
				# Olympic Games
				if pLoopCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_OLYMPIONIKE")):
						szText += u"%c" % gc.getReligionInfo(gc.getInfoTypeForString("RELIGION_GREEK")).getChar()
				# Thing meetings
				if pLoopCity.isHasBuilding(gc.getInfoTypeForString("BUILDING_THING_CITY")):
						szText += u"%c" % gc.getReligionInfo(gc.getInfoTypeForString("RELIGION_NORDIC")).getChar()

				screen.setTableText("CityListBackground", 19, i, szText, "", WidgetTypes.WIDGET_GENERAL, 749, 20, CvUtil.FONT_LEFT_JUSTIFY)

				# PAE: City Growth (Stadtwachstum): aktiv/active or inaktiv/inactive
				if (pLoopCity.AI_isEmphasize(5)):
						szText = localText.getText("TXT_KEY_DOM_ADVISOR_GROWTH2", ())
						szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
				else:
						szText = localText.getText("TXT_KEY_DOM_ADVISOR_GROWTH3", ())
						szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + szText + localText.getText("TXT_KEY_COLOR_REVERT", ())
						if pLoopCity.foodDifference(True) <= 0:
								szText += u" (0)"
						else:
								szText += u" (%d)" % int(float(pLoopCity.growthThreshold()) / float(pLoopCity.foodDifference(True)))

				screen.setTableText("CityListBackground", 20, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

		# ################### PAGE 2 ###### Slave Buildings ##########

		def drawHeaders2(self):

				ButtonSize = 46
				ButtonY = 12
				ButtonX = (260 * self.nTableWidth) / self.nNormalizedTableWidth
				MarginX = (56 * self.nTableWidth) / self.nNormalizedTableWidth
				ColWidth = (56 * self.nTableWidth) / self.nNormalizedTableWidth
				
				player = gc.getPlayer(gc.getGame().getActivePlayer())
				pTeam = gc.getTeam(player.getTeam())

				# Get the screen and the player
				screen = self.getScreen()

				# OBEN (header)
				szText = localText.getText("TXT_KEY_DOMESTIC_ADVISOR_AVAILABLE_SLAVES", (player.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_SLAVE")), ))
				screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
						80, 30, 0, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1)

				# UNTEN (bottom)
				#Sterberate
				screen.setText(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_STERBERATE_SLAVES", ()).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
						80, self.nScreenHeight - 65, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVILOPEDIA).getActionInfoIndex(), -1)

				# Haussklaven
				iChance = 4
				if pTeam.isHasTech(gc.getInfoTypeForString("TECH_PATRONAT")): iChance = 2
				szText = u"<font=3>" + localText.getText("TXT_KEY_UNIT_SLAVE_HAUS", ()) + (u": %s%%</font>" % str(iChance))
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 200, self.nScreenHeight - 85, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				screen.addPanel(self.getNextWidgetName(), u"", u"", True, False, 200, self.nScreenHeight-66, 220, 56, PanelStyles.PANEL_STYLE_MAIN_BLACK25)
				szText = u"<font=2>" + localText.getText("TXT_KEY_WORLD_STANDARD", ()) + u": 4%</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 200, self.nScreenHeight - 60, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=2>" + localText.getText("TXT_KEY_TRADE_TECH", ()) + u" " + localText.getText("TXT_KEY_TECH_PATRONAT", ()) + u": -2%</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 200, self.nScreenHeight - 44, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1)

				# Feldsklaven
				iChance = 6
				if pTeam.isHasTech(gc.getInfoTypeForString("TECH_EISENPFLUG")): iChance = 3
				szText = u"<font=3>" + localText.getText("TXT_KEY_UNIT_SLAVE_FOOD", ()) + (u": %s%%</font>" % str(iChance))
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 430, self.nScreenHeight - 85, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1)

				screen.addPanel(self.getNextWidgetName(), u"", u"", True, False, 430, self.nScreenHeight-66, 220, 56, PanelStyles.PANEL_STYLE_MAIN_BLACK25)
				szText = u"<font=2>" + localText.getText("TXT_KEY_WORLD_STANDARD", ()) + u": 6%</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 430, self.nScreenHeight - 60, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=2>" + localText.getText("TXT_KEY_TRADE_TECH", ()) + u" " + localText.getText("TXT_KEY_TECH_EISENPFLUG", ()) + u": -3%</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 430, self.nScreenHeight - 44, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1)

				# Bergwerksklaven
				iChance = 8
				if pTeam.isHasTech(gc.getInfoTypeForString("TECH_MECHANIK")): iChance = 4
				szText = u"<font=3>" + localText.getText("TXT_KEY_UNIT_SLAVE_PROD", ()) + (u": %s%%</font>" % str(iChance))
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 660, self.nScreenHeight - 85, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1)

				screen.addPanel(self.getNextWidgetName(), u"", u"", True, False, 660, self.nScreenHeight-66, 220, 56, PanelStyles.PANEL_STYLE_MAIN_BLACK25)
				szText = u"<font=2>" + localText.getText("TXT_KEY_WORLD_STANDARD", ()) + u": 8%</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 660, self.nScreenHeight - 60, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=2>" + localText.getText("TXT_KEY_TRADE_TECH", ()) + u" " + localText.getText("TXT_KEY_TECH_MECHANIK", ()) + u": -4%</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 660, self.nScreenHeight - 44, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1)

				# Gebäudesklaven
				iChance = 6
				if pTeam.isHasTech(gc.getInfoTypeForString("TECH_MEDICINE3")): iChance -= 2
				if pTeam.isHasTech(gc.getInfoTypeForString("TECH_ANATOMIE")): iChance -= 2
				szText = u"<font=3>" + localText.getText("TXT_KEY_UNIT_SLAVE_BUILDING", ()) + (u": %s%%</font>" % str(iChance))
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 890, self.nScreenHeight - 85, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1)

				screen.addPanel(self.getNextWidgetName(), u"", u"", True, False, 890, self.nScreenHeight-66, 220, 56, PanelStyles.PANEL_STYLE_MAIN_BLACK25)
				szText = u"<font=2>" + localText.getText("TXT_KEY_WORLD_STANDARD", ()) + u": 6%</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 890, self.nScreenHeight - 60, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=2>" + localText.getText("TXT_KEY_TRADE_TECH", ()) + u" " + localText.getText("TXT_KEY_TECH_MEDICINE3", ()) + u": -2%</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 890, self.nScreenHeight - 44, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1)
				szText = u"<font=2>" + localText.getText("TXT_KEY_TRADE_TECH", ()) + u" " + localText.getText("TXT_KEY_TECH_ANATOMIE", ()) + u": -2%</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 890, self.nScreenHeight - 28, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1)


				# Zoom to City
				screen.setTableColumnHeader("CityListBackground", 0, "", (20 * self.nTableWidth) / self.nNormalizedTableWidth)

				# City name
				screen.setTableColumnHeader("CityListBackground", 1, "<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()) + "</font>", (120 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Population
				screen.setTableColumnHeader("CityListBackground", 2, "<font=2>" + u"%c" % CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR) + "</font>", ColWidth)

				# Field slaves
				iData = gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD")
				screen.setImageButton(self.getNextWidgetName(), gc.getSpecialistInfo(iData).getButton(), ButtonX, ButtonY, ButtonSize, ButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, iData, 1)
				screen.setTableColumnHeader("CityListBackground", 3, "<font=2>" + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()) + "</font>", ColWidth)

				# Mine slaves
				iData = gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD")
				screen.setImageButton(self.getNextWidgetName(), gc.getSpecialistInfo(iData).getButton(), ButtonX+MarginX*1,
															ButtonY, ButtonSize, ButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, iData, 2)
				screen.setTableColumnHeader("CityListBackground", 4, "<font=2>" + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()) + "</font>", ColWidth)

				# House slaves
				iData = gc.getInfoTypeForString("SPECIALIST_SLAVE")
				screen.setImageButton(self.getNextWidgetName(), gc.getSpecialistInfo(iData).getButton(), ButtonX+MarginX*2,
															ButtonY, ButtonSize, ButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 5, "<font=2>" + (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar()) + "</font>", ColWidth)

				# Gladiators
				iData = gc.getInfoTypeForString("SPECIALIST_GLADIATOR")
				screen.setImageButton(self.getNextWidgetName(), gc.getSpecialistInfo(iData).getButton(), ButtonX+MarginX*3,
															ButtonY, ButtonSize, ButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 6, "<font=2>" + u"%c" % gc.getBonusInfo(gc.getInfoTypeForString("BONUS_BRONZE")).getChar() + "</font>", ColWidth)

				# Slave market
				iData = gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")
				screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*4, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 7, "<font=2>" + (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()) + "</font>", ColWidth)

				# Gladiatorenschule
				iData = gc.getInfoTypeForString("BUILDING_GLADIATORENSCHULE")
				screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*5, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 8, "<font=2>" + (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()) + "</font>", ColWidth)

				# Brotmanufaktur
				iData = gc.getInfoTypeForString("BUILDING_BROTMANUFAKTUR")
				screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*6, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 9, "<font=2>" + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()) + "</font>", ColWidth)

				# Manufaktur
				iData = gc.getInfoTypeForString("BUILDING_CORP3")
				screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*7, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 10, "<font=2>" + (u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()) + "</font>", ColWidth)

				# School
				iData = gc.getInfoTypeForString("BUILDING_SCHULE")
				screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*8, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 11, "<font=2>" + (u"+2%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar()) + "</font>", ColWidth)

				# Library
				iData = gc.getInfoTypeForString("BUILDING_LIBRARY")
				screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*9, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 12, "<font=2>" + (u"+2%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar()) + "</font>", ColWidth)

				# Fire station
				iData = gc.getInfoTypeForString("BUILDING_FEUERWEHR")
				screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*10, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 13, "<font=2>" + (u"%c" % CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)) + "</font>", ColWidth)

				# Bordell
				iData = gc.getInfoTypeForString("BUILDING_BORDELL")
				screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*11, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 14, "<font=2>" + (u"+2%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()) + "</font>", ColWidth)

				# Theatre
				iData = gc.getInfoTypeForString("BUILDING_THEATER")
				screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*12, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 15, "<font=2>" + (u"+2%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()) + "</font>", ColWidth)

				# Temple slaves
				iData = gc.getInfoTypeForString("SPECIALBUILDING_TEMPLE")
				screen.setImageButton(self.getNextWidgetName(), gc.getSpecialBuildingInfo(iData).getButton(), ButtonX+MarginX*13, ButtonY, 46, 46, WidgetTypes.WIDGET_HELP_SPECIAL_BUILDING, -1, iData)
				# Trait Creative: 3 Kultur pro Sklave / 3 culture per slave
				if gc.getPlayer(CyGame().getActivePlayer()).hasTrait(gc.getInfoTypeForString("TRAIT_CREATIVE")):
						screen.setTableColumnHeader("CityListBackground", 16, "<font=2>" + (u"+3%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()) + "</font>", ColWidth)
				else:
						screen.setTableColumnHeader("CityListBackground", 16, "<font=2>" + (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()) + "</font>", ColWidth)

				# Palace slaves
				iData = gc.getInfoTypeForString("BUILDING_PALACE")
				screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*14, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
				screen.setTableColumnHeader("CityListBackground", 17, "<font=2>" + (u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()) + "</font>", ColWidth)

		def updateTable2(self, pLoopCity, i):

				screen = self.getScreen()

				# City status (button)
				buttonCityStatus = self.getButtonCityStatus(pLoopCity)

				# BTS: buttonCityStatus = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath()
				screen.setTableText("CityListBackground", 0, i, "", buttonCityStatus, WidgetTypes.WIDGET_ZOOM_CITY, pLoopCity.getOwner(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)

				# City Name
				szName = self.getCityName(pLoopCity)
				screen.setTableText("CityListBackground", 1, i, szName, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Population
				iPop = pLoopCity.getPopulation()
				screen.setTableInt("CityListBackground", 2, i, unicode(iPop), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Settled Slaves
				iCityGlads = pLoopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_GLADIATOR"))
				iCitySlaves1 = pLoopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE"))
				iCitySlaves2 = pLoopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_FOOD"))
				iCitySlaves3 = pLoopCity.getFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SLAVE_PROD"))

				iSumSlaves = iCityGlads + iCitySlaves1 + iCitySlaves2 + iCitySlaves3

				if iPop < iSumSlaves:
						szColor = localText.getText("TXT_KEY_COLOR_NEGATIVE", ())
				else:
						szColor = localText.getText("TXT_KEY_COLOR_POSITIVE", ())

				# Field slaves
				if iCitySlaves2:
						szText = u"%d" % iCitySlaves2
				else:
						szText = szColor + u"%d" % (iCitySlaves2) + localText.getText("TXT_KEY_COLOR_REVERT", ())
				screen.setTableInt("CityListBackground", 3, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				# Mine slaves
				if iCitySlaves3:
						szText = u"%d" % iCitySlaves3
				else:
						szText = szColor + u"%d" % (iCitySlaves3) + localText.getText("TXT_KEY_COLOR_REVERT", ())
				screen.setTableInt("CityListBackground", 4, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				# House slaves
				if iCitySlaves1:
						szText = u"%d" % iCitySlaves1
				else:
						szText = szColor + u"%d" % (iCitySlaves1) + localText.getText("TXT_KEY_COLOR_REVERT", ())
				screen.setTableInt("CityListBackground", 5, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				# Gladiators
				if iCityGlads:
						szText = u"%d" % iCityGlads
				else:
						szText = szColor + u"%d" % (iCityGlads) + localText.getText("TXT_KEY_COLOR_REVERT", ())
				screen.setTableInt("CityListBackground", 6, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Slave market
				if pLoopCity.getNumRealBuilding(gc.getInfoTypeForString("BUILDING_SKLAVENMARKT")):
						szText = u"1"
				elif pLoopCity.getNumRealBuilding(gc.getInfoTypeForString("BUILDING_STADT")):
						szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + u"0" + localText.getText("TXT_KEY_COLOR_REVERT", ())
				else:
						szText = u""
				screen.setTableInt("CityListBackground", 7, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Gladiatorenschule
				if pLoopCity.getNumRealBuilding(gc.getInfoTypeForString("BUILDING_GLADIATORENSCHULE")):
						szText = u"1"
				elif pLoopCity.getNumRealBuilding(gc.getInfoTypeForString("BUILDING_STADT")):
						szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + u"0" + localText.getText("TXT_KEY_COLOR_REVERT", ())
				else:
						szText = u""
				screen.setTableInt("CityListBackground", 8, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Brotmanufaktur
				eBuilding = gc.getInfoTypeForString("BUILDING_BROTMANUFAKTUR")
				szText = self.getTable2Value(pLoopCity, eBuilding, 3)
				screen.setTableInt("CityListBackground", 9, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Manufaktur
				eBuilding = gc.getInfoTypeForString("BUILDING_CORP3")
				szText = self.getTable2Value(pLoopCity, eBuilding, 5)
				screen.setTableInt("CityListBackground", 10, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# School
				eBuilding = gc.getInfoTypeForString("BUILDING_SCHULE")
				szText = self.getTable2Value(pLoopCity, eBuilding, 5)
				screen.setTableInt("CityListBackground", 11, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Library
				eBuilding = gc.getInfoTypeForString("BUILDING_LIBRARY")
				szText = self.getTable2Value(pLoopCity, eBuilding, 5)
				screen.setTableInt("CityListBackground", 12, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Fire station
				eBuilding = gc.getInfoTypeForString("BUILDING_FEUERWEHR")
				szText = self.getTable2Value(pLoopCity, eBuilding, 3)
				screen.setTableInt("CityListBackground", 13, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Bordell
				eBuilding = gc.getInfoTypeForString("BUILDING_BORDELL")
				szText = self.getTable2Value(pLoopCity, eBuilding, 5)
				screen.setTableInt("CityListBackground", 14, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Theatre
				eBuilding = gc.getInfoTypeForString("BUILDING_THEATER")
				szText = self.getTable2Value(pLoopCity, eBuilding, 5)
				screen.setTableInt("CityListBackground", 15, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Temple slaves
				eBuilding = gc.getInfoTypeForString("SPECIALBUILDING_TEMPLE")
				iCulture = 0
				bTemple = False
				# Trait Creative: 3 Kultur pro Sklave / 3 culture per slave
				if gc.getPlayer(pLoopCity.getOwner()).hasTrait(gc.getInfoTypeForString("TRAIT_CREATIVE")):
						iCultureSlave = 3
				else:
						iCultureSlave = 1
				Temples = self.getTemples()
				for iTemple in Temples:
						if pLoopCity.getNumRealBuilding(iTemple):
								bTemple = True
								eBuildingClass = gc.getBuildingInfo(iTemple).getBuildingClassType()
								iTempleCulture = pLoopCity.getBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_CULTURE)
								if iTempleCulture > 2:
										iCulture += (pLoopCity.getBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_CULTURE) - 2) / iCultureSlave

				if iCulture:
						szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + (u"%d" % iCulture) + localText.getText("TXT_KEY_COLOR_REVERT", ())
				elif bTemple:
						szText = localText.getText("TXT_KEY_COLOR_GRAY", ()) + u"0" + localText.getText("TXT_KEY_COLOR_REVERT", ())
				else:
						szText = u""
				screen.setTableInt("CityListBackground", 16, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Palace slaves
				eBuilding = gc.getInfoTypeForString("BUILDING_PALACE")
				if pLoopCity.getNumRealBuilding(eBuilding):
						eBuildingClass = gc.getBuildingInfo(eBuilding).getBuildingClassType()
						iCulture = pLoopCity.getBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_CULTURE)
						if iCulture > 4:
								szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + (u"%d" % (iCulture-4)) + localText.getText("TXT_KEY_COLOR_REVERT", ())
						else:
								szText = localText.getText("TXT_KEY_COLOR_GRAY", ()) + u"0" + localText.getText("TXT_KEY_COLOR_REVERT", ())
				else:
						szText = u""
				screen.setTableInt("CityListBackground", 17, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		def getTable2Value(self, pLoopCity, eBuilding, iMax):

				if pLoopCity.getNumRealBuilding(eBuilding):
						eBuildingClass = gc.getBuildingInfo(eBuilding).getBuildingClassType()
						iValue = 0
						if eBuilding == gc.getInfoTypeForString("BUILDING_BROTMANUFAKTUR"):
								iValue = pLoopCity.getBuildingYieldChange(eBuildingClass, YieldTypes.YIELD_FOOD)
						elif eBuilding == gc.getInfoTypeForString("BUILDING_CORP3"):
								iValue = pLoopCity.getBuildingYieldChange(eBuildingClass, YieldTypes.YIELD_PRODUCTION)
						elif eBuilding == gc.getInfoTypeForString("BUILDING_LIBRARY"):
								iValue = pLoopCity.getBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_RESEARCH) / 2
						elif eBuilding == gc.getInfoTypeForString("BUILDING_SCHULE"):
								iValue = pLoopCity.getBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_RESEARCH) / 2
						elif eBuilding == gc.getInfoTypeForString("BUILDING_FEUERWEHR"):
								iValue = pLoopCity.getBuildingHappyChange(eBuildingClass)
						elif eBuilding == gc.getInfoTypeForString("BUILDING_BORDELL"):
								iValue = pLoopCity.getBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_CULTURE) / 2
						elif eBuilding == gc.getInfoTypeForString("BUILDING_THEATER"):
								iValue = pLoopCity.getBuildingCommerceChange(eBuildingClass, CommerceTypes.COMMERCE_CULTURE) / 2

						if iValue == iMax:
								return u"%d/%d" % (iValue, iMax)
						else:
								return localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + (u"%d/%d" % (iValue, iMax)) + localText.getText("TXT_KEY_COLOR_REVERT", ())

				elif pLoopCity.canConstruct(eBuilding, False, False, False):
						return localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + (u"0/%d" % iMax) + localText.getText("TXT_KEY_COLOR_REVERT", ())
				else:
						# return u"0/%d" % iMax
						return u""

		def getTemples(self):
				Temples = [
						gc.getInfoTypeForString("BUILDING_ZORO_TEMPLE"),
						gc.getInfoTypeForString("BUILDING_PHOEN_TEMPLE"),
						gc.getInfoTypeForString("BUILDING_SUMER_TEMPLE"),
						gc.getInfoTypeForString("BUILDING_ROME_TEMPLE"),
						gc.getInfoTypeForString("BUILDING_GREEK_TEMPLE"),
						gc.getInfoTypeForString("BUILDING_CELTIC_TEMPLE"),
						gc.getInfoTypeForString("BUILDING_EGYPT_TEMPLE"),
						gc.getInfoTypeForString("BUILDING_NORDIC_TEMPLE")
				]
				return Temples

		# ################### PAGE 3 ##### Cultivation ###########

		def drawHeaders3(self):

				ColWidth = (50 * self.nTableWidth) / self.nNormalizedTableWidth

				# Get the screen and the player
				screen = self.getScreen()

				# Zoom to City
				screen.setTableColumnHeader("CityListBackground", 0, "", (20 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Name Column
				screen.setTableColumnHeader("CityListBackground", 1, "<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()) + "</font>", (120 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Cultivation status
				j = 0
				List = self.getBonuses()
				for eBonus in List:
						screen.setTableColumnHeader("CityListBackground", 2+j, "<font=2>" + (u"%c" % gc.getBonusInfo(eBonus).getChar()) + "</font>", ColWidth)
						j += 1

				#TXT_KEY_DOMESTIC_ADVISOR_LEGENDE = "Legende"
				#TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_1 = "Weiß: [COLOR_BUILDING_TEXT]Die Ressource ist bei der Stadt verbreitet[COLOR_REVERT]"
				#TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_2 = "[COLOR_BUILDING_TEXT]Grau: Die Ressource kann derzeit nicht verbreitet werden[COLOR_REVERT]"
				#TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_3 = "[COLOR_POSITIVE_TEXT]Grün[COLOR_REVERT]: [COLOR_BUILDING_TEXT]Die Ressource kann verbreitet werden und ist im Handelsnetz verfügbar[COLOR_REVERT]"
				#TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_4 = "[COLOR_NEGATIVE_TEXT]Rot[COLOR_REVERT]: [COLOR_BUILDING_TEXT]Die Ressource kann verbreitet werden, ist aber nicht im Handelsnetz verfügbar[COLOR_REVERT]"
				#TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_5 = "[COLOR_HIGHLIGHT_TEXT]x/y[COLOR_REVERT]: [COLOR_BUILDING_TEXT]Diese Ressourcen sind voneinander abhängig. Es können maximal y dieser Ressourcen um die Stadt verbreitet werden (je nach Stadtgröße: 3,6,12,20).[COLOR_REVERT]"
				#TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_6 = "[COLOR_HIGHLIGHT_TEXT]Kein Wert[COLOR_REVERT]: [COLOR_BUILDING_TEXT]Die Ressource kann überhaupt nicht verbreitet werden (kein geeignetes Terrain)[COLOR_REVERT]"

				# UNTEN (Bottom)
				# Legende
				screen.setText(self.getNextWidgetName(), "Background", u"<font=3>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_LEGENDE", ()).upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
						80, self.nScreenHeight - 85, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVILOPEDIA).getActionInfoIndex(), -1)

				screen.addPanel(self.getNextWidgetName(), u"", u"", True, False, 180, self.nScreenHeight-86, self.nScreenWidth-400, 76, PanelStyles.PANEL_STYLE_MAIN_BLACK25)
				szText = u"<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_1", ()) + u"</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 190, self.nScreenHeight - 80, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_2", ()) + u"</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 190, self.nScreenHeight - 64, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_3", ()) + u"</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 660, self.nScreenHeight - 80, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_4", ()) + u"</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 660, self.nScreenHeight - 64, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_5", ()) + u"</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 190, self.nScreenHeight - 48, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szText = u"<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_LEGENDE_6", ()) + u"</font>"
				screen.setText(self.getNextWidgetName(), "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 190, self.nScreenHeight - 32, -0.1, FontTypes.MENU_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)


		def updateTable3(self, pLoopCity, i):

				screen = self.getScreen()

				# City status (button)
				buttonCityStatus = self.getButtonCityStatus(pLoopCity)

				# BTS: buttonCityStatus = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath()
				screen.setTableText("CityListBackground", 0, i, "", buttonCityStatus, WidgetTypes.WIDGET_ZOOM_CITY, pLoopCity.getOwner(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)

				# City Name
				szName = self.getCityName(pLoopCity)
				screen.setTableText("CityListBackground", 1, i, szName, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				BonusClasses = [
						gc.getInfoTypeForString("BONUSCLASS_GRAIN"),
						gc.getInfoTypeForString("BONUSCLASS_LIVESTOCK")
				]
				j = 0
				List = self.getBonuses()
				for eBonus in List:
						iAnz = PAE_Cultivation.isCityHasBonus(pLoopCity, eBonus)
						# Getreide und Vieh
						if gc.getBonusInfo(eBonus).getBonusClassType() in BonusClasses:
								#PossiblePlots = PAE_Cultivation.getCityCultivatablePlots(pLoopCity, eBonus)
								#iMax = PAE_Cultivation.getCityCultivationAmount(pLoopCity,0)

								# PAE VII: Anzeige nur 1x Bonus pro Stadt
								if iAnz:
										szText = u"%d/%d" % (iAnz,1)
								elif PAE_Cultivation._isCityCultivationPossible(pLoopCity, 0):
										if gc.getPlayer(pLoopCity.getOwner()).hasBonus(eBonus):
												szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + u"%d/%d" % (0,1) + localText.getText("TXT_KEY_COLOR_REVERT", ())
										else:
												szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + u"%d/%d" % (0,1) + localText.getText("TXT_KEY_COLOR_REVERT", ())
								else:
										szText = localText.getText("TXT_KEY_COLOR_GRAY", ()) + u"%d/%d" % (0,1) + localText.getText("TXT_KEY_COLOR_REVERT", ())

								# PAE VI: Anzeige Anzahl/Max
								"""
								if PAE_Cultivation._isCityCultivationPossible(pLoopCity, 0):
										iMax = min(iMax, len(PossiblePlots))
										if iAnz == 0 and iMax == 0:
												szText = localText.getText("TXT_KEY_COLOR_GRAY", ()) + (u"%d/%d" % (iAnz,iMax)) + localText.getText("TXT_KEY_COLOR_REVERT", ())
										elif iAnz >= iMax:
												szText = u"%d/%d" % (iAnz,1)
										else:
												if gc.getPlayer(pLoopCity.getOwner()).hasBonus(eBonus):
														szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + (u"%d/%d" % (iAnz,iMax)) + localText.getText("TXT_KEY_COLOR_REVERT", ())
												else:
														szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + (u"%d/%d" % (iAnz,iMax)) + localText.getText("TXT_KEY_COLOR_REVERT", ())
								elif iAnz:
										szText = u"%d/%d" % (iAnz,iMax)
								else:
										szText = localText.getText("TXT_KEY_COLOR_GRAY", ()) + (u"%d/%d" % (iAnz,iMax)) + localText.getText("TXT_KEY_COLOR_REVERT", ())
								"""

						# der Rest
						elif iAnz:
								szText = u"%d" % iAnz
						else:
								PossiblePlots = PAE_Cultivation.getCityCultivatablePlots(pLoopCity, eBonus)
								if PossiblePlots:
										if gc.getPlayer(pLoopCity.getOwner()).hasBonus(eBonus):
												szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + u"0" + localText.getText("TXT_KEY_COLOR_REVERT", ())
										else:
												szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + u"0" + localText.getText("TXT_KEY_COLOR_REVERT", ())
								else:
										szText = u""

						screen.setTableInt("CityListBackground", 2+j, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						j += 1

		def getBonuses(self):
				BonusClasses = [
						gc.getInfoTypeForString("BONUSCLASS_GRAIN"),
						gc.getInfoTypeForString("BONUSCLASS_LIVESTOCK"),
						gc.getInfoTypeForString("BONUSCLASS_PLANTATION")
				]
				Bonuses = []
				Bonuses.append(gc.getInfoTypeForString("BONUS_HORSE"))
				Bonuses.append(gc.getInfoTypeForString("BONUS_CAMEL"))
				for eBonus in range(gc.getNumBonusInfos()):
						if gc.getBonusInfo(eBonus).getBonusClassType() in BonusClasses:
								Bonuses.append(eBonus)
				Bonuses.append(gc.getInfoTypeForString("BONUS_CRAB"))
				Bonuses.append(gc.getInfoTypeForString("BONUS_CLAM"))
				return Bonuses

		# ################### PAGE 4 ####### Specialists #############

		def drawHeaders4(self):

				ButtonSize = 46
				ButtonY = 12
				ButtonX = (236 * self.nTableWidth) / self.nNormalizedTableWidth
				MarginX = (40 * self.nTableWidth) / self.nNormalizedTableWidth
				ColWidth = (40 * self.nTableWidth) / self.nNormalizedTableWidth

				# Get the screen and the player
				screen = self.getScreen()

				# Zoom to City
				screen.setTableColumnHeader("CityListBackground", 0, "", (20 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Name Column
				screen.setTableColumnHeader("CityListBackground", 1, "<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()) + "</font>", (120 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Population Column
				screen.setTableColumnHeader("CityListBackground", 2, "<font=2>" + u"%c" % CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR) + "</font>", ColWidth)

				# Specialists
				for iData in range(gc.getNumSpecialistInfos()):
						# if (gc.getSpecialistInfo(iData).isVisible()):
						screen.setImageButton(self.getNextWidgetName(), gc.getSpecialistInfo(iData).getButton(), ButtonX+MarginX*iData,
																	ButtonY, ButtonSize, ButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, iData, 1)
						szText = u""
						for i in range(YieldTypes.NUM_YIELD_TYPES):
								iNum = gc.getSpecialistInfo(iData).getYieldChange(i)
								if iNum:
										if iNum > 1:
												szText += u"%d%c" % (iNum, gc.getYieldInfo(i).getChar())
										else:
												szText += u"%c" % (gc.getYieldInfo(i).getChar())
						for i in range(CommerceTypes.NUM_COMMERCE_TYPES):
								iNum = gc.getSpecialistInfo(iData).getCommerceChange(i)
								if iNum:
										if iNum > 1:
												szText += u"%d%c" % (iNum, gc.getCommerceInfo(i).getChar())
										else:
												szText += u"%c" % (gc.getCommerceInfo(i).getChar())
						if gc.getSpecialistInfo(iData).getExperience():
								szText += u"%c" % gc.getBonusInfo(gc.getInfoTypeForString("BONUS_BRONZE")).getChar()

						screen.setTableColumnHeader("CityListBackground", 3+iData, "<font=2>" + szText + "</font>", ColWidth)

		def updateTable4(self, pLoopCity, i):

				screen = self.getScreen()

				# City status (button)
				buttonCityStatus = self.getButtonCityStatus(pLoopCity)

				# BTS: buttonCityStatus = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath()
				screen.setTableText("CityListBackground", 0, i, "", buttonCityStatus, WidgetTypes.WIDGET_ZOOM_CITY, pLoopCity.getOwner(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)

				# City Name
				szName = self.getCityName(pLoopCity)
				screen.setTableText("CityListBackground", 1, i, szName, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Population
				screen.setTableInt("CityListBackground", 2, i, unicode(pLoopCity.getPopulation()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Specialists
				for iData in range(gc.getNumSpecialistInfos()):
						iMax = pLoopCity.getMaxSpecialistCount(iData)
						if pLoopCity.getFreeSpecialistCount(iData):
								szText = u"%d" % (pLoopCity.getSpecialistCount(iData) + pLoopCity.getFreeSpecialistCount(iData))
						elif iMax == 0:
								szText = localText.getText("TXT_KEY_COLOR_GRAY", ()) + u"0/0" + localText.getText("TXT_KEY_COLOR_REVERT", ())
						else:
								szText = u"%d/%d" % (pLoopCity.getSpecialistCount(iData) + pLoopCity.getFreeSpecialistCount(iData), iMax)
						screen.setTableInt("CityListBackground", 3+iData, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)


		# ################### PAGE 5 ###### Great Generals ############

		def drawHeaders5(self):

				ButtonSize = 46
				ButtonY = 12
				ButtonX = (263 * self.nTableWidth) / self.nNormalizedTableWidth
				MarginX = (56 * self.nTableWidth) / self.nNormalizedTableWidth
				ColWidth = (56 * self.nTableWidth) / self.nNormalizedTableWidth
				
				player = gc.getPlayer(gc.getGame().getActivePlayer())

				# Get the screen and the player
				screen = self.getScreen()

				szText = localText.getText("TXT_KEY_DOMESTIC_ADVISOR_AVAILABLE_GENERALS", (player.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_GREAT_GENERAL")), ))
				screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
						80, 30, 0, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1)

				# Zoom to City
				screen.setTableColumnHeader("CityListBackground", 0, "", (20 * self.nTableWidth) / self.nNormalizedTableWidth)

				# City name
				screen.setTableColumnHeader("CityListBackground", 1, "<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()) + "</font>", (120 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Population
				screen.setTableColumnHeader("CityListBackground", 2, "<font=2>" + u"%c" % CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR) + "</font>", ColWidth)

				# Buildings
				List = [
						gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationBuildings(gc.getInfoTypeForString("BUILDINGCLASS_HEROIC_EPIC")),
						gc.getInfoTypeForString("BUILDING_MILITARY_ACADEMY"),
						gc.getInfoTypeForString("BUILDING_SIEGESSTELE"),
						gc.getInfoTypeForString("BUILDING_SIEGESTEMPEL"),
						gc.getInfoTypeForString("BUILDING_SIEGESSTATUE"),
						gc.getInfoTypeForString("BUILDING_SIEGESSAEULE"),
						gc.getInfoTypeForString("BUILDING_ELEPHANTMONUMENT"),
						gc.getInfoTypeForString("BUILDING_TRIUMPH"),
						gc.getInfoTypeForString("BUILDING_ROMAN_SHRINE")
				]
				n = 0
				for iData in List:
						eBuildingClass = gc.getBuildingInfo(iData).getBuildingClassType()
						screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*n, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
						szText = u"<font=2>"
						if gc.getBuildingInfo(iData).getHappiness():
								szText += (u"+%d%c" % (gc.getBuildingInfo(iData).getHappiness(), CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)))
						if gc.getBuildingInfo(iData).getObsoleteSafeCommerceChange(CommerceTypes.COMMERCE_CULTURE):
								szText += (u"+%d%c" % (gc.getBuildingInfo(iData).getObsoleteSafeCommerceChange(CommerceTypes.COMMERCE_CULTURE), gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar()))
						szText += "</font>"
						screen.setTableColumnHeader("CityListBackground", 3+n, szText, ColWidth)
						n += 1

				Units = []
				(loopUnit, iter) = player.firstUnit(False)
				while(loopUnit):
						if loopUnit.getUnitClassType() == gc.getInfoTypeForString("UNITCLASS_GREAT_GENERAL"):
								Units.append(loopUnit)
						(loopUnit, iter) = player.nextUnit(iter, False)

				# PAE Untere Buttons (UNITS)
				n = 60
				iRange = min(len(Units),10)
				for i in range(iRange):
						screen.setImageButton(self.getNextWidgetName(), Units[i].getButton(), 80 + n*i, self.nScreenHeight - 60, 46, 46, WidgetTypes.WIDGET_GENERAL, 1, Units[i].getID())


		def updateTable5(self, pLoopCity, i):

				screen = self.getScreen()
				player = gc.getPlayer(gc.getGame().getActivePlayer())

				# City status (button)
				buttonCityStatus = self.getButtonCityStatus(pLoopCity)

				# BTS: buttonCityStatus = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath()
				screen.setTableText("CityListBackground", 0, i, "", buttonCityStatus, WidgetTypes.WIDGET_ZOOM_CITY, pLoopCity.getOwner(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)

				# City Name
				szName = self.getCityName(pLoopCity)
				screen.setTableText("CityListBackground", 1, i, szName, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Population
				iPop = pLoopCity.getPopulation()
				screen.setTableInt("CityListBackground", 2, i, unicode(iPop), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Buildings
				List = [
						gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationBuildings(gc.getInfoTypeForString("BUILDINGCLASS_HEROIC_EPIC")),
						gc.getInfoTypeForString("BUILDING_MILITARY_ACADEMY"),
						gc.getInfoTypeForString("BUILDING_SIEGESSTELE"),
						gc.getInfoTypeForString("BUILDING_SIEGESTEMPEL"),
						gc.getInfoTypeForString("BUILDING_SIEGESSTATUE"),
						gc.getInfoTypeForString("BUILDING_SIEGESSAEULE"),
						gc.getInfoTypeForString("BUILDING_ELEPHANTMONUMENT"),
						gc.getInfoTypeForString("BUILDING_TRIUMPH"),
						gc.getInfoTypeForString("BUILDING_ROMAN_SHRINE")
				]
				n = 0
				for iData in List:
						if pLoopCity.getNumRealBuilding(iData):
								szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + u"1" + localText.getText("TXT_KEY_COLOR_REVERT", ())
						elif iData == gc.getInfoTypeForString("BUILDING_SIEGESSTELE") or iData == gc.getInfoTypeForString("BUILDING_SIEGESTEMPEL"):
								szText = u""
						elif pLoopCity.canConstruct(iData,0,0,1):
								szText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + u"0" + localText.getText("TXT_KEY_COLOR_REVERT", ())
						else:
								szText = u""
						screen.setTableInt("CityListBackground", 3+n, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
						n += 1


		# ################### PAGE 6 ###################################

		def drawHeaders6(self):

				# Get the screen and the player
				screen = self.getScreen()

				ButtonSize = 46
				ButtonY = 12
				ButtonX = (263 * self.nTableWidth) / self.nNormalizedTableWidth
				MarginX = (56 * self.nTableWidth) / self.nNormalizedTableWidth
				ColWidth = (56 * self.nTableWidth) / self.nNormalizedTableWidth
				
				player = gc.getPlayer(gc.getGame().getActivePlayer())

				# Available Building Promo Units
				LPromos = [
						gc.getInfoTypeForString("PROMOTION_CITY_GARRISON5"),
						gc.getInfoTypeForString("PROMOTION_CITY_RAIDER5"),
						gc.getInfoTypeForString("PROMOTION_GUERILLA5"),
						gc.getInfoTypeForString("PROMOTION_PILLAGE5"),
						gc.getInfoTypeForString("PROMOTION_JUNGLE5"),
						gc.getInfoTypeForString("PROMOTION_SUMPF5"),
						gc.getInfoTypeForString("PROMOTION_WOODSMAN5"),
						gc.getInfoTypeForString("PROMOTION_DESERT5"),
						gc.getInfoTypeForString("PROMOTION_NAVIGATION4")
				]
				Units = []
				iAnz = 0
				(loopUnit, iter) = player.firstUnit(False)
				while(loopUnit):
						for iPromo in LPromos:
								if loopUnit.isHasPromotion(iPromo):
										iAnz += 1
										Units.append(loopUnit)
										break
						(loopUnit, iter) = player.nextUnit(iter, False)

				# PAE Untere Buttons (UNITS)
				n = 60
				iRange = min(len(Units),10)
				for i in range(iRange):
						screen.setImageButton(self.getNextWidgetName(), Units[i].getButton(), 300 + n*i, self.nScreenHeight - 60, 46, 46, WidgetTypes.WIDGET_GENERAL, 1, Units[i].getID())

				szText = localText.getText("TXT_KEY_AVAILABLE_BUILDING_PROMO_UNITS", (iAnz, ))
				screen.setLabel(self.getNextWidgetName(), "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY,
						80, self.nScreenHeight - 60, 0, FontTypes.MENU_FONT, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1)

				# Zoom to City
				screen.setTableColumnHeader("CityListBackground", 0, "", (20 * self.nTableWidth) / self.nNormalizedTableWidth)

				# City name
				screen.setTableColumnHeader("CityListBackground", 1, "<font=2>" + localText.getText("TXT_KEY_DOMESTIC_ADVISOR_NAME", ()) + "</font>", (120 * self.nTableWidth) / self.nNormalizedTableWidth)

				# Population
				screen.setTableColumnHeader("CityListBackground", 2, "<font=2>" + u"%c" % CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR) + "</font>", ColWidth)

				# Buildings
				List = [
						gc.getInfoTypeForString("BUILDING_PROMO_CITY_D"),
						gc.getInfoTypeForString("BUILDING_PROMO_CITY_A"),
						gc.getInfoTypeForString("BUILDING_PROMO_HILLS"),
						gc.getInfoTypeForString("BUILDING_PROMO_PILLAGE"),
						gc.getInfoTypeForString("BUILDING_PROMO_JUNGLE"),
						gc.getInfoTypeForString("BUILDING_PROMO_SWAMP"),
						gc.getInfoTypeForString("BUILDING_PROMO_FOREST"),
						gc.getInfoTypeForString("BUILDING_PROMO_DESERT"),
						gc.getInfoTypeForString("BUILDING_PROMO_NAVI")
				]
				n = 0
				for iData in List:
						eBuildingClass = gc.getBuildingInfo(iData).getBuildingClassType()
						screen.setImageButton(self.getNextWidgetName(), gc.getBuildingInfo(iData).getButton(), ButtonX+MarginX*n, ButtonY, 46, 46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iData, -1)
						szText = u""
						screen.setTableColumnHeader("CityListBackground", 3+n, szText, ColWidth)
						n += 1


		def updateTable6(self, pLoopCity, i):

				screen = self.getScreen()
				player = gc.getPlayer(gc.getGame().getActivePlayer())

				# City status (button)
				buttonCityStatus = self.getButtonCityStatus(pLoopCity)

				# BTS: buttonCityStatus = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CITYSELECTION").getPath()
				screen.setTableText("CityListBackground", 0, i, "", buttonCityStatus, WidgetTypes.WIDGET_ZOOM_CITY, pLoopCity.getOwner(), pLoopCity.getID(), CvUtil.FONT_LEFT_JUSTIFY)

				# City Name
				szName = self.getCityName(pLoopCity)
				screen.setTableText("CityListBackground", 1, i, szName, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Population
				iPop = pLoopCity.getPopulation()
				screen.setTableInt("CityListBackground", 2, i, unicode(iPop), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				# Buildings
				List = [
						gc.getInfoTypeForString("BUILDING_PROMO_CITY_D"),
						gc.getInfoTypeForString("BUILDING_PROMO_CITY_A"),
						gc.getInfoTypeForString("BUILDING_PROMO_HILLS"),
						gc.getInfoTypeForString("BUILDING_PROMO_PILLAGE"),
						gc.getInfoTypeForString("BUILDING_PROMO_JUNGLE"),
						gc.getInfoTypeForString("BUILDING_PROMO_SWAMP"),
						gc.getInfoTypeForString("BUILDING_PROMO_FOREST"),
						gc.getInfoTypeForString("BUILDING_PROMO_DESERT"),
						gc.getInfoTypeForString("BUILDING_PROMO_NAVI")
				]
				n = 0
				for iData in List:
						if pLoopCity.getNumRealBuilding(iData):
								szText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + u"1" + localText.getText("TXT_KEY_COLOR_REVERT", ())
						else:
								szText = localText.getText("TXT_KEY_COLOR_GRAY", ()) + u"0" + localText.getText("TXT_KEY_COLOR_REVERT", ())
						screen.setTableInt("CityListBackground", 3+n, i, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
						n += 1


		# ################### END PAGES ###################################


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
				# City name: font-color: white (normal), red (riot/civil war)
				if pLoopCity.getNumRealBuilding(gc.getInfoTypeForString("BUILDING_CIVIL_WAR")) or pLoopCity.getOccupationTimer():
						szName = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + pLoopCity.getName() + localText.getText("TXT_KEY_COLOR_REVERT", ())
						szName += u"%c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)
				else:
						szName = pLoopCity.getName()

				# Symbol: Stern: Capital (gold) or provincial palace (silver)
				if pLoopCity.isCapital():
						szName += u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)
				elif pLoopCity.isGovernmentCenter():
						szName += u"%c" % CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR)

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

		# Draw the specialist and their increase and decrease buttons
		def drawSpecialists(self):
				screen = self.getScreen()

				for i in range(gc.getNumSpecialistInfos()):
						if (gc.getSpecialistInfo(i).isVisible()):
								szName = "SpecialistImage" + str(i)
								screen.setImageButton(szName, gc.getSpecialistInfo(i).getTexture(), self.nFirstSpecialistX + (self.nSpecialistDistance * i),
																			self.nSpecialistY, self.nSpecialistWidth, self.nSpecialistLength, WidgetTypes.WIDGET_CITIZEN, i, -1)
								screen.hide(szName)

								szName = "SpecialistPlus" + str(i)
								screen.setButtonGFC(szName, u"", "", self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nPlusOffsetX, self.nSpecialistY + self.nPlusOffsetY,
																		self.nPlusWidth, self.nPlusHeight, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS)
								screen.hide(szName)

								szName = "SpecialistMinus" + str(i)
								screen.setButtonGFC(szName, u"", "", self.nFirstSpecialistX + (self.nSpecialistDistance * i) + self.nMinusOffsetX, self.nSpecialistY + self.nMinusOffsetY,
																		self.nMinusWidth, self.nMinusHeight, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS)
								screen.hide(szName)

								szName = "SpecialistText" + str(i)
								screen.setLabel(szName, "Background", "", CvUtil.FONT_LEFT_JUSTIFY, self.nFirstSpecialistX + (self.nSpecialistDistance * i) +
																self.nSpecTextOffsetX, self.nSpecialistY + self.nSpecTextOffsetY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
								screen.hide(szName)

		def hideSpecialists(self):
				screen = self.getScreen()
				for i in range(gc.getNumSpecialistInfos()):
						if (gc.getSpecialistInfo(i).isVisible()):
								screen.hide("SpecialistImage" + str(i))
								screen.hide("SpecialistPlus" + str(i))
								screen.hide("SpecialistMinus" + str(i))
								screen.hide("SpecialistText" + str(i))

		def updateSpecialists(self):
				""" Function which shows the specialists."""
				screen = self.getScreen()

				if (CyInterface().isOneCitySelected()):

						city = CyInterface().getHeadSelectedCity()
						nPopulation = city.getPopulation()
						nFreeSpecial = city.totalFreeSpecialists()

						for i in range(gc.getNumSpecialistInfos()):
								if (gc.getSpecialistInfo(i).isVisible()):
										szName = "SpecialistImage" + str(i)
										screen.show(szName)

										szName = "SpecialistText" + str(i)
										screen.setLabel(szName, "Background", str(city.getSpecialistCount(i)) + "/" + str(city.getMaxSpecialistCount(i)), CvUtil.FONT_LEFT_JUSTIFY, self.nFirstSpecialistX +
																		(self.nSpecialistDistance * i) + self.nSpecTextOffsetX, self.nSpecialistY + self.nSpecTextOffsetY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
										screen.show(szName)

										# If the specialist is valid and we can increase it
										szName = "SpecialistPlus" + str(i)
										if (city.isSpecialistValid(i, 1) and (city.getForceSpecialistCount(i) < (nPopulation + nFreeSpecial))):
												screen.show(szName)
										else:
												screen.hide(szName)

										# if we HAVE specialists already and they're not forced.
										szName = "SpecialistMinus" + str(i)
										if (city.getSpecialistCount(i) > 0 or city.getForceSpecialistCount(i) > 0):
												screen.show(szName)
										else:
												screen.hide(szName)
				else:
						self.hideSpecialists()

		# Will handle the input for this screen...
		def handleInput(self, inputClass):
				' Calls function mapped in DomesticAdvisorInputMap'
				# only get from the map if it has the key

				if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
						if (inputClass.getMouseX() == 0):
								screen = self.getScreen()
								screen.hideScreen()

								CyInterface().selectCity(gc.getPlayer(inputClass.getData1()).getCity(inputClass.getData2()), True)

								popupInfo = CyPopupInfo()
								popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
								popupInfo.setText(u"showDomesticAdvisor")
								popupInfo.addPopup(inputClass.getData1())
						else:
								
								if (self.iActiveTab == 1 or self.iActiveTab == 4):
										# BTS standard
										self.updateAppropriateCitySelection()
										self.updateSpecialists()
								else:
										# PAE: got to city on map
										screen = self.getScreen()
										screen.hideScreen()
										self.updateAppropriateCitySelection()
										CyCamera().JustLookAtPlot(CyInterface().getHeadSelectedCity().plot())


				elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):

						szWidgetName = inputClass.getFunctionName() + str(inputClass.getID())

						if (inputClass.getFunctionName() == "DomesticSplit"):
								screen = self.getScreen()
								screen.hideScreen()
						elif (szWidgetName == self.szTab1a or szWidgetName == self.szTab1b):
								self.iActiveTab = 1
								self.interfaceScreen()
						elif (szWidgetName == self.szTab2a or szWidgetName == self.szTab2b):
								self.iActiveTab = 2
								self.interfaceScreen()
						elif (szWidgetName == self.szTab3a or szWidgetName == self.szTab3b):
								self.iActiveTab = 3
								self.interfaceScreen()
						elif (szWidgetName == self.szTab4a or szWidgetName == self.szTab4b):
								self.iActiveTab = 4
								self.interfaceScreen()
						elif (szWidgetName == self.szTab5a or szWidgetName == self.szTab5b):
								self.iActiveTab = 5
								self.interfaceScreen()
						elif (szWidgetName == self.szTab6a or szWidgetName == self.szTab6b):
								self.iActiveTab = 6
								self.interfaceScreen()
						elif inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL:
								if inputClass.getData1() == 764:
										CyMessageControl().sendModNetMessage(764, CyGame().getActivePlayer(), -1, -1, -1)
										self.getScreen().hideScreen()
								elif inputClass.getData1() == 709:
										CyMessageControl().sendModNetMessage(709, -1, -1, -1, CyGame().getActivePlayer())
										self.getScreen().hideScreen()
								elif inputClass.getData1() == 1 and inputClass.getData2() != -1:
										pPlayer = gc.getPlayer(CyGame().getActivePlayer())
										pUnit = pPlayer.getUnit(inputClass.getData2())
										CyCamera().JustLookAtPlot(pUnit.plot())
										CyInterface().selectUnit(pUnit, True, True, True)
										self.getScreen().hideScreen()
						 
						#PB Mod - Remove Pause
						if inputClass.getData1() == 301311:
							if gc.getGame().isPaused() and not CyGame().isPitbossHost():
								# Cause crash on PB server is host os is Linux
								#gc.sendPause(-1)
								# Workaround.
								gc.sendChat("RemovePause", ChatTargetTypes.CHATTARGET_ALL)
								screen = CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
								screen.hideScreen()
						
						

				return 0

		def updateAppropriateCitySelection(self):
				nCities = gc.getPlayer(gc.getGame().getActivePlayer()).getNumCities()
				screen = self.getScreen()
				screen.updateAppropriateCitySelection("CityListBackground", nCities, 1)
				self.listSelectedCities = []
				for i in range(nCities):
						if screen.isRowSelected("CityListBackground", i):
								self.listSelectedCities.append(screen.getTableText("CityListBackground", 2, i))

		def update(self, fDelta):
				if (CyInterface().isDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT) == True):
						CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, False)

						screen = self.getScreen() #noqa
						player = gc.getPlayer(CyGame().getActivePlayer())

						i = 0
						(loopCity, iter) = player.firstCity(False)
						while loopCity:
								# if not loopCity.isNone() and loopCity.getOwner() == player.getID(): #only valid cities
								if (self.iActiveTab == 6):
										self.updateTable6(loopCity, i)
								elif (self.iActiveTab == 5):
										self.updateTable5(loopCity, i)
								elif (self.iActiveTab == 4):
										self.updateTable4(loopCity, i)
								elif (self.iActiveTab == 3):
										self.updateTable3(loopCity, i)
								elif (self.iActiveTab == 2):
										self.updateTable2(loopCity, i)
								else:
										self.updateTable(loopCity, i)
								i += 1
								(loopCity, iter) = player.nextCity(iter, False)

						self.updateSpecialists()

		def getScreen(self):
				return CyGInterfaceScreen("DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR)

		def getNextWidgetName(self):
				szName = self.WIDGET_ID + str(self.nWidgetCount)
				self.nWidgetCount += 1
				return szName

		def deleteAllWidgets(self, iNumPermanentWidgets=0):
				screen = self.getScreen()
				i = self.nWidgetCount - 1
				while (i >= iNumPermanentWidgets):
						self.nWidgetCount = i
						screen.deleteWidget(self.getNextWidgetName())
						i -= 1
				self.nWidgetCount = iNumPermanentWidgets

				return
