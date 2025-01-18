# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
																FontTypes, CivilopediaPageTypes,
																WidgetTypes, PanelStyles, YieldTypes,
																CyGameTextMgr, GenericButtonSizes)
import CvUtil
# import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvPediaImprovement:
		"Civilopedia Screen for tile Improvements"

		def __init__(self, main):
				self.iImprovement = -1
				self.top = main

				self.X_UPPER_PANE = 10
				self.Y_UPPER_PANE = 57
				self.W_UPPER_PANE = 433
				self.H_UPPER_PANE = 165

				self.X_IMPROVENEMT_ANIMATION = 473
				self.Y_IMPROVENEMT_ANIMATION = 65
				self.W_IMPROVENEMT_ANIMATION = 303
				self.H_IMPROVENEMT_ANIMATION = 156
				self.X_ROTATION_IMPROVENEMT_ANIMATION = -20
				self.Z_ROTATION_IMPROVENEMT_ANIMATION = 30
				self.SCALE_ANIMATION = 0.8

				self.X_ICON = 175
				self.Y_ICON = 90
				self.W_ICON = 100
				self.H_ICON = 100
				self.ICON_SIZE = 64

				self.X_IMPROVEMENTS_PANE = 10
				self.Y_IMPROVEMENTS_PANE = self.Y_UPPER_PANE + self.H_UPPER_PANE + 10
				self.W_IMPROVEMENTS_PANE = 500
				self.H_IMPROVEMENTS_PANE = 160

				self.X_BONUS_YIELDS_PANE = self.X_IMPROVEMENTS_PANE + self.W_IMPROVEMENTS_PANE + 25
				self.Y_BONUS_YIELDS_PANE = self.Y_UPPER_PANE + self.H_UPPER_PANE + 10
				self.W_BONUS_YIELDS_PANE = 236
				self.H_BONUS_YIELDS_PANE = 460

				self.X_REQUIRES = 10
				self.Y_REQUIRES = self.Y_IMPROVEMENTS_PANE + self.H_IMPROVEMENTS_PANE + 10
				self.W_REQUIRES = 500
				self.H_REQUIRES = 110

				self.X_EFFECTS = 10
				self.Y_EFFECTS = self.Y_REQUIRES + self.H_REQUIRES + 10
				self.W_EFFECTS = 500
				self.H_EFFECTS = 170

		# Screen construction function
		def interfaceScreen(self, iImprovement):
				# PAE
				global Latifundien
				Latifundien = [
						gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM1"),
						gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM2"),
						gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM3"),
						gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM4"),
						gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM5")
				]
				global LImprFortSentry
				LImprFortSentry = [
						gc.getInfoTypeForString("IMPROVEMENT_TURM"),
						gc.getInfoTypeForString("IMPROVEMENT_TURM2"),
						gc.getInfoTypeForString("IMPROVEMENT_FORT"),
						gc.getInfoTypeForString("IMPROVEMENT_FORT2"),
						gc.getInfoTypeForString("IMPROVEMENT_LIMES9"),
						gc.getInfoTypeForString("IMPROVEMENT_LIMES2_9"),
						gc.getInfoTypeForString("IMPROVEMENT_KASTELL")
				]

				self.iImprovement = iImprovement

				self.top.deleteAllWidgets()

				screen = self.top.getScreen()

				bNotActive = (not screen.isActive())
				if bNotActive:
						self.top.setPediaCommonWidgets()

				# Header...
				szHeader = u"<font=4b>" + gc.getImprovementInfo(self.iImprovement).getDescription().upper() + u"</font>"
				szHeaderId = self.top.getNextWidgetName()
				screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Top
				screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU,
											 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT, -1)

				if self.top.iLastScreen != CvScreenEnums.PEDIA_IMPROVEMENT or bNotActive:
						self.placeLinks(True)
						self.top.iLastScreen = CvScreenEnums.PEDIA_IMPROVEMENT
				else:
						self.placeLinks(False)

				# Icon
				screen.addPanel(self.top.getNextWidgetName(), "", "", False, False,
												self.X_UPPER_PANE, self.Y_UPPER_PANE, self.W_UPPER_PANE, self.H_UPPER_PANE, PanelStyles.PANEL_STYLE_BLUE50)
				screen.addPanel(self.top.getNextWidgetName(), "", "", False, False,
												self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
				screen.addDDSGFC(self.top.getNextWidgetName(), gc.getImprovementInfo(self.iImprovement).getButton(),
												 self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Bonus animation
				screen.addImprovementGraphicGFC(self.top.getNextWidgetName(), self.iImprovement, self.X_IMPROVENEMT_ANIMATION, self.Y_IMPROVENEMT_ANIMATION, self.W_IMPROVENEMT_ANIMATION,
																				self.H_IMPROVENEMT_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_IMPROVENEMT_ANIMATION, self.Z_ROTATION_IMPROVENEMT_ANIMATION, self.SCALE_ANIMATION, True)

				self.placeSpecial()

				self.placeBonusYield()

				self.placeYield()

				self.placeRequires()

		def placeYield(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), "", True, True,
												self.X_IMPROVEMENTS_PANE, self.Y_IMPROVEMENTS_PANE, self.W_IMPROVEMENTS_PANE, self.H_IMPROVEMENTS_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				# info = gc.getImprovementInfo(self.iImprovement)

				szYield = u""

				# Baukosten
				for k in range(gc.getNumBuildInfos()):
						if (gc.getBuildInfo(k).getImprovement() == self.iImprovement):
								szYield += (u"%s: -%i%c\n" % (gc.getBuildInfo(k).getText(), gc.getBuildInfo(k).getCost(), gc.getCommerceInfo(0).getChar()))

				# BTS Standard
				for k in range(YieldTypes.NUM_YIELD_TYPES):
						iYieldChange = gc.getImprovementInfo(self.iImprovement).getYieldChange(k)
						if (iYieldChange != 0):
								if (iYieldChange > 0):
										sign = "+"
								else:
										sign = ""

								szYield += (u"%s: %s%i%c\n" % (gc.getYieldInfo(k).getDescription(), sign, iYieldChange, gc.getYieldInfo(k).getChar()))

				for k in range(YieldTypes.NUM_YIELD_TYPES):
						iYieldChange = gc.getImprovementInfo(self.iImprovement).getIrrigatedYieldChange(k)
						if (iYieldChange != 0):
								szYield += localText.getText("TXT_KEY_PEDIA_IRRIGATED_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar())) + u"\n"

				for k in range(YieldTypes.NUM_YIELD_TYPES):
						iYieldChange = gc.getImprovementInfo(self.iImprovement).getHillsYieldChange(k)
						if (iYieldChange != 0):
								szYield += localText.getText("TXT_KEY_PEDIA_HILLS_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar())) + u"\n"

				for k in range(YieldTypes.NUM_YIELD_TYPES):
						iYieldChange = gc.getImprovementInfo(self.iImprovement).getRiverSideYieldChange(k)
						if (iYieldChange != 0):
								szYield += localText.getText("TXT_KEY_PEDIA_RIVER_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar())) + u"\n"

				for iTech in range(gc.getNumTechInfos()):
						for k in range(YieldTypes.NUM_YIELD_TYPES):
								iYieldChange = gc.getImprovementInfo(self.iImprovement).getTechYieldChanges(iTech, k)
								if (iYieldChange != 0):
										szYield += localText.getText("TXT_KEY_PEDIA_TECH_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar(), gc.getTechInfo(iTech).getTextKey())) + u"\n"

				for iCivic in range(gc.getNumCivicInfos()):
						for k in range(YieldTypes.NUM_YIELD_TYPES):
								iYieldChange = gc.getCivicInfo(iCivic).getImprovementYieldChanges(self.iImprovement, k)
								if (iYieldChange != 0):
										szYield += localText.getText("TXT_KEY_PEDIA_TECH_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange,
																								 gc.getYieldInfo(k).getChar(), gc.getCivicInfo(iCivic).getTextKey())) + u"\n"

				for iRoute in range(gc.getNumRouteInfos()):
						for k in range(YieldTypes.NUM_YIELD_TYPES):
								iYieldChange = gc.getImprovementInfo(self.iImprovement).getRouteYieldChanges(iRoute, k)
								if (iYieldChange != 0):
										szYield += localText.getText("TXT_KEY_PEDIA_ROUTE_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange,
																								 gc.getYieldInfo(k).getChar(), gc.getRouteInfo(iRoute).getTextKey())) + u"\n"

				listName = self.top.getNextWidgetName()
				screen.addMultilineText(listName, szYield, self.X_IMPROVEMENTS_PANE+5, self.Y_IMPROVEMENTS_PANE+30, self.W_IMPROVEMENTS_PANE -
																10, self.H_IMPROVEMENTS_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		def placeBonusYield(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_BONUS_YIELDS", ()), "", True, True,
												self.X_BONUS_YIELDS_PANE, self.Y_BONUS_YIELDS_PANE, self.W_BONUS_YIELDS_PANE, self.H_BONUS_YIELDS_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				info = gc.getImprovementInfo(self.iImprovement)

				for j in range(gc.getNumBonusInfos()):
						bFirst = True
						szYield = u""
						bEffect = False
						for k in range(YieldTypes.NUM_YIELD_TYPES):
								iYieldChange = info.getImprovementBonusYield(j, k)
								if (iYieldChange != 0):
										bEffect = True
										if (bFirst):
												bFirst = False
										else:
												szYield += u", "

										if (iYieldChange > 0):
												sign = u"+"
										else:
												sign = u""

										szYield += (u"%s%i%c" % (sign, iYieldChange, gc.getYieldInfo(k).getChar()))
						if (bEffect):
								childPanelName = self.top.getNextWidgetName()
								screen.attachPanel(panelName, childPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)

								screen.attachLabel(childPanelName, "", "  ")
								screen.attachImageButton(childPanelName, "", gc.getBonusInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, j, 1, False)
								screen.attachLabel(childPanelName, "", u"<font=4>" + szYield + u"</font>")

		def placeRequires(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True,
												self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50)

				screen.attachLabel(panelName, "", "  ")

				for iBuild in range(gc.getNumBuildInfos()):
						if (gc.getBuildInfo(iBuild).getImprovement() == self.iImprovement):
								iTech = gc.getBuildInfo(iBuild).getTechPrereq()
								if (iTech > -1):
										screen.attachImageButton(panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)

				# PAE Units that can build that
				if self.iImprovement in Latifundien:
						if self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM1"):
								iUnit = gc.getInfoTypeForString("UNIT_PRAETORIAN")
								screen.attachImageButton(panelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)
						else:
								iImp = gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM1")
								screen.attachImageButton(panelName, "", gc.getImprovementInfo(iImp).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iImp, 1, False)

								iUnit = gc.getInfoTypeForString("UNIT_SLAVE")

								childPanelName = self.top.getNextWidgetName()
								screen.attachPanel(panelName, childPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
								screen.attachLabel(childPanelName, "", u"<font=4>+</font>")
								screen.attachImageButton(childPanelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)

								if self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM3") or self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM4") or self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM5"):
										screen.attachLabel(childPanelName, "", u"<font=4>+</font>")
										screen.attachImageButton(childPanelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)

								if self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM4") or self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM5"):
										screen.attachLabel(childPanelName, "", u"<font=4>+</font>")
										screen.attachImageButton(childPanelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)

								if self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_LATIFUNDIUM5"):
										screen.attachLabel(childPanelName, "", u"<font=4>+</font>")
										screen.attachImageButton(childPanelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)

				elif self.iImprovement == gc.getInfoTypeForString("IMPROVEMENT_HANDELSPOSTEN"):
						iUnit = gc.getInfoTypeForString("UNIT_TRADE_MERCHANT")
						screen.attachImageButton(panelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)
						iUnit = gc.getInfoTypeForString("UNIT_CARAVAN")
						screen.attachImageButton(panelName, "", gc.getUnitInfo(iUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, False)

		def placeSpecial(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False,
												self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50)

				listName = self.top.getNextWidgetName()

				szSpecialText = CyGameTextMgr().getImprovementHelp(self.iImprovement, True)

				# PAE : isFreshWaterValid
				if gc.getImprovementInfo(self.iImprovement).isFreshWaterMakesValid():
						szSpecialText += u"\n" + localText.getText("TXT_KEY_INFO_FRESHWATERMAKESVALID", ())
				# PAE: Latifundien (Prätis bauen es, Sklaven beschleunigen es)
				if self.iImprovement in Latifundien:
						szSpecialText += u"\n" + localText.getText("TXT_KEY_INFO_IMPROVEMENT_LATIFUNDIEN", ())
				if self.iImprovement in LImprFortSentry:
						szSpecialText += u"\n" + localText.getText("TXT_KEY_INFO_IMPROVEMENT_SENTRY", ())

				# Text wird hier ausgegeben
				screen.addMultilineText(listName, szSpecialText, self.X_EFFECTS+5, self.Y_EFFECTS+35, self.W_EFFECTS-10, self.H_EFFECTS-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		def placeLinks(self, bRedraw):

				screen = self.top.getScreen()

				if bRedraw:
						screen.clearListBoxGFC(self.top.LIST_ID)

				# sort Improvements alphabetically
				rowListName = [(0, 0)]*gc.getNumImprovementInfos()
				for j in range(gc.getNumImprovementInfos()):
						rowListName[j] = (gc.getImprovementInfo(j).getDescription(), j)
				rowListName.sort()

				iSelected = 0
				i = 0
				for iI in range(gc.getNumImprovementInfos()):
						if (not gc.getImprovementInfo(rowListName[iI][1]).isGraphicalOnly()):
								if bRedraw:
										screen.appendListBoxString(self.top.LIST_ID, rowListName[iI][0], WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, rowListName[iI][1], 0, CvUtil.FONT_LEFT_JUSTIFY)
								if rowListName[iI][1] == self.iImprovement:
										iSelected = i
								i += 1

				screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

		# Will handle the input for this screen...
		def handleInput(self, inputClass):
				return 0
