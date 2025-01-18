# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
																FontTypes, CivilopediaPageTypes, YieldTypes,
																WidgetTypes, PanelStyles, TableStyles,
																CyGameTextMgr, GenericButtonSizes)
import CvUtil
# import ScreenInput
import CvScreenEnums
import string

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvPediaBonus:
		"Civilopedia Screen for Bonus Resources"

		def __init__(self, main):
				self.iBonus = -1
				self.top = main

				self.X_BONUS_PANE = 10
				self.Y_BONUS_PANE = 57
				self.W_BONUS_PANE = 433
				self.H_BONUS_PANE = 165

				self.X_BONUS_ANIMATION = 460
				self.Y_BONUS_ANIMATION = 65
				self.W_BONUS_ANIMATION = 311
				self.H_BONUS_ANIMATION = 156
				self.X_ROTATION_BONUS_ANIMATION = -20
				self.Z_ROTATION_BONUS_ANIMATION = 30
				self.SCALE_ANIMATION = 0.8

				self.X_ICON = 53
				self.Y_ICON = 90
				self.W_ICON = 100
				self.H_ICON = 100
				self.ICON_SIZE = 64

				self.X_STATS_PANE = 185
				self.Y_STATS_PANE = 90  # 128
				self.W_STATS_PANE = 240
				self.H_STATS_PANE = 200

				# iWidthBuffer = 20
				# iHeightBuffer = 0

				self.X_IMPROVEMENTS_PANE = 10
				self.Y_IMPROVEMENTS_PANE = 237
				self.W_IMPROVEMENTS_PANE = 305
				self.H_IMPROVEMENTS_PANE = 110

				self.X_EFFECTS_PANE = 330
				self.Y_EFFECTS_PANE = 237
				self.W_EFFECTS_PANE = 443
				self.H_EFFECTS_PANE = 110

				self.X_REQUIRES = 10
				self.Y_REQUIRES = 354
				self.W_REQUIRES = 305
				self.H_REQUIRES = 110

				self.X_HISTORY_PANE = 330
				self.Y_HISTORY_PANE = 354
				self.W_HISTORY_PANE = 443
				self.H_HISTORY_PANE = 255

				self.X_BUILDINGS = 10
				self.Y_BUILDINGS = 471
				self.W_BUILDINGS = 305
				self.H_BUILDINGS = 110

				self.X_ALLOWS_PANE = 10
				self.Y_ALLOWS_PANE = 597
				self.W_ALLOWS_PANE = 763
				self.H_ALLOWS_PANE = 110

		# Screen construction function
		def interfaceScreen(self, iBonus):

				self.iBonus = iBonus

				self.top.deleteAllWidgets()

				screen = self.top.getScreen()

				bNotActive = (not screen.isActive())
				if bNotActive:
						self.top.setPediaCommonWidgets()

				# Header...
				szHeader = u"<font=4b>" + gc.getBonusInfo(self.iBonus).getDescription().upper() + u"</font>"
				szHeaderId = self.top.getNextWidgetName()
				screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0,
												FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS, iBonus)

				# Top
				screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU,
											 self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS, -1)

				if self.top.iLastScreen != CvScreenEnums.PEDIA_BONUS or bNotActive:
						self.placeLinks(True)
						self.top.iLastScreen = CvScreenEnums.PEDIA_BONUS
				else:
						self.placeLinks(False)

				# Icon
				screen.addPanel(self.top.getNextWidgetName(), "", "", False, False,
												self.X_BONUS_PANE, self.Y_BONUS_PANE, self.W_BONUS_PANE, self.H_BONUS_PANE, PanelStyles.PANEL_STYLE_BLUE50)
				screen.addPanel(self.top.getNextWidgetName(), "", "", False, False,
												self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
				screen.addDDSGFC(self.top.getNextWidgetName(), gc.getBonusInfo(self.iBonus).getButton(),
												 self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Bonus animation
				screen.addBonusGraphicGFC(self.top.getNextWidgetName(), self.iBonus,
																	self.X_BONUS_ANIMATION, self.Y_BONUS_ANIMATION, self.W_BONUS_ANIMATION, self.H_BONUS_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_BONUS_ANIMATION, self.Z_ROTATION_BONUS_ANIMATION, self.SCALE_ANIMATION, True)

				self.placeStats()

				# PAE
				# list = [
				#     gc.getInfoTypeForString("BONUSCLASS_GRAIN"),
				#     gc.getInfoTypeForString("BONUSCLASS_LIVESTOCK"),
				#     gc.getInfoTypeForString("BONUSCLASS_PLANTATION"),
				#     gc.getInfoTypeForString("BONUSCLASS_MISC"),
				#     gc.getInfoTypeForString("BONUSCLASS_RARITY"),
				#     gc.getInfoTypeForString("BONUSCLASS_GENERAL"),
				#     gc.getInfoTypeForString("BONUSCLASS_MERCENARY"),
				#     gc.getInfoTypeForString("BONUSCLASS_LUXURY")
				# ]
				# if gc.getBonusInfo(self.iBonus).getBonusClassType() in list:
				self.placeTerrain()
				# ----

				self.placeYield()

				self.placeRequires()

				self.placeBuildings()
				self.placeAllows()

				self.placeSpecial()

				self.placeHistory()

				return

		def placeStats(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()

				screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
				screen.enableSelect(panelName, False)

				szYield = ""
				for k in range(YieldTypes.NUM_YIELD_TYPES):
						iYieldChange = gc.getBonusInfo(self.iBonus).getYieldChange(k)
						if (iYieldChange != 0):
								if (iYieldChange > 0):
										sign = "+"
								else:
										sign = ""

								#szYield = (u"%s: %s%i " % (gc.getYieldInfo(k).getDescription(), sign, iYieldChange))
								# PAE:
								if szYield != "":
										szYield += u", "
								szYield += u"%s%i %c" % (sign, iYieldChange, gc.getYieldInfo(k).getChar())
				if szYield != "":
						#screen.appendListBoxString(panelName, u"<font=4>" + szYield.upper() + (u"%c" % gc.getYieldInfo(k).getChar()) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
						screen.appendListBoxString(panelName, u"<font=4>" + szYield + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		# PAE
		def placeTerrain(self):

				screen = self.top.getScreen()
				x = 0
				y = 30
				a = 0
				# Terrain
				for iI in range(gc.getNumTerrainInfos()):
						if not gc.getTerrainInfo(iI).isGraphicalOnly():
								if gc.getBonusInfo(self.iBonus).isTerrain(iI):
										screen.addDDSGFC(self.top.getNextWidgetName(), gc.getTerrainInfo(iI).getButton(),
																		 self.X_STATS_PANE + x, self.Y_STATS_PANE + y, 48, 48, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, iI, -1)
										x += 52
										a += 1

				# Feature
				for iI in range(gc.getNumFeatureInfos()):
						if not gc.getFeatureInfo(iI).isGraphicalOnly():
								if gc.getBonusInfo(self.iBonus).isFeature(iI):
										if a >= 5:
												x = 0
												y = 80
												a = 0
										screen.addDDSGFC(self.top.getNextWidgetName(), gc.getFeatureInfo(iI).getButton(),
																		 self.X_STATS_PANE + x, self.Y_STATS_PANE + y, 48, 48, WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, iI, -1)
										x += 52
				# Feature + Terrain
				bPlus = True
				for iI in range(gc.getNumTerrainInfos()):
						if not gc.getTerrainInfo(iI).isGraphicalOnly():
								if gc.getBonusInfo(self.iBonus).isFeatureTerrain(iI) and not gc.getBonusInfo(self.iBonus).isTerrain(iI):
										if bPlus:
												screen.addMultilineText(self.top.getNextWidgetName(), u"<font=10>+</font>",
																								self.X_STATS_PANE + x, self.Y_STATS_PANE + 40, 30, 30, WidgetTypes.WIDGET_PYTHON, -1, -1, 0)
												bPlus = False
												x += 20
										screen.addDDSGFC(self.top.getNextWidgetName(), gc.getTerrainInfo(iI).getButton(),
																		 self.X_STATS_PANE + x, self.Y_STATS_PANE + y, 48, 48, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, iI, -1)
										x += 52

				# Oliven
				if self.iBonus == gc.getInfoTypeForString("BONUS_OLIVES"):
						iI = gc.getInfoTypeForString("TERRAIN_COAST")
						screen.addDDSGFC(self.top.getNextWidgetName(), gc.getTerrainInfo(iI).getButton(),
														 self.X_STATS_PANE + x, self.Y_STATS_PANE + y, 48, 48, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, iI, -1)

		def placeYield(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), "", True, True,
												self.X_IMPROVEMENTS_PANE, self.Y_IMPROVEMENTS_PANE, self.W_IMPROVEMENTS_PANE, self.H_IMPROVEMENTS_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				# bonusInfo = gc.getBonusInfo(self.iBonus)

				for j in range(gc.getNumImprovementInfos()):
						bFirst = True
						szYield = u""
						bEffect = False
						for k in range(YieldTypes.NUM_YIELD_TYPES):
								iYieldChange = gc.getImprovementInfo(j).getImprovementBonusYield(self.iBonus, k)
								# PAE: and Bonus makes valid
								if iYieldChange != 0 or gc.getImprovementInfo(j).isImprovementBonusMakesValid(self.iBonus):
										bEffect = True
										iYieldChange += gc.getImprovementInfo(j).getYieldChange(k)

										if (bFirst):
												bFirst = False
										else:
												szYield += ", "

										if (iYieldChange > 0):
												sign = "+"
										else:
												sign = ""

										szYield += (u"%s%i%c" % (sign, iYieldChange, gc.getYieldInfo(k).getChar()))
						if (bEffect):
								childPanelName = self.top.getNextWidgetName()
								screen.attachPanel(panelName, childPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)

								screen.attachLabel(childPanelName, "", "  ")
								screen.attachImageButton(childPanelName, "", gc.getImprovementInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, j, 1, False)
								screen.attachLabel(childPanelName, "", szYield)

		def placeSpecial(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_EFFECTS", ()), "", True, False,
												self.X_EFFECTS_PANE, self.Y_EFFECTS_PANE, self.W_EFFECTS_PANE, self.H_EFFECTS_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				listName = self.top.getNextWidgetName()
				screen.attachListBoxGFC(panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY)
				screen.enableSelect(listName, False)

				szSpecialText = CyGameTextMgr().getBonusHelp(self.iBonus, True)
				splitText = string.split(szSpecialText, "\n")
				for special in splitText:
						if len(special) != 0:
								screen.appendListBoxString(listName, special, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		def placeRequires(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True,
												self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50)

				screen.attachLabel(panelName, "", "  ")

				iTech = gc.getBonusInfo(self.iBonus).getTechReveal()
				if (iTech > -1):
						screen.attachImageButton(panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)
						screen.attachLabel(panelName, "", u"(" + localText.getText("TXT_KEY_PEDIA_BONUS_APPEARANCE", ()) + u")")
				iTech = gc.getBonusInfo(self.iBonus).getTechCityTrade()
				if (iTech > -1):
						screen.attachImageButton(panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False)
						screen.attachLabel(panelName, "", u"(" + localText.getText("TXT_KEY_PEDIA_BONUS_TRADE", ()) + u")")

		def placeHistory(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True,
												self.X_HISTORY_PANE, self.Y_HISTORY_PANE, self.W_HISTORY_PANE, self.H_HISTORY_PANE,
												PanelStyles.PANEL_STYLE_BLUE50)

				screen.attachLabel(panelName, "", "  ")

				textName = self.top.getNextWidgetName()
				screen.addMultilineText(textName, gc.getBonusInfo(self.iBonus).getCivilopedia(), self.X_HISTORY_PANE + 15, self.Y_HISTORY_PANE + 40,
																self.W_HISTORY_PANE - (15 * 2), self.H_HISTORY_PANE - (15 * 2) - 25, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		def placeBuildings(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()), "", False, True,
												self.X_BUILDINGS, self.Y_BUILDINGS, self.W_BUILDINGS, self.H_BUILDINGS, PanelStyles.PANEL_STYLE_BLUE50)

				screen.attachLabel(panelName, "", "  ")

				for iBuilding in range(gc.getNumBuildingInfos()):
						pBuildingInfo = gc.getBuildingInfo(iBuilding)
						# BTS Standard
						if pBuildingInfo.getFreeBonus() == self.iBonus:
								screen.attachImageButton(panelName, "", pBuildingInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False)

						# PAE: Buildings that give yield Bonus for that resource
						for iYield in range(3):
								if pBuildingInfo.getBonusYieldModifier(self.iBonus, iYield):
										screen.attachImageButton(panelName, "", pBuildingInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False)

						# PAE: Buildings that give health or happiness change
						if pBuildingInfo.getBonusHealthChanges(self.iBonus) or pBuildingInfo.getBonusHappinessChanges(self.iBonus):
								screen.attachImageButton(panelName, "", pBuildingInfo.getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False)

		def placeAllows(self):

				screen = self.top.getScreen()

				panelName = self.top.getNextWidgetName()
				screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_ALLOWS", ()), "", False, True,
												self.X_ALLOWS_PANE, self.Y_ALLOWS_PANE, self.W_ALLOWS_PANE, self.H_ALLOWS_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				screen.attachLabel(panelName, "", "  ")

				# add unit buttons
				for eLoopUnit in range(gc.getNumUnitInfos()):
						bFound = False
						if (eLoopUnit >= 0):
								if (gc.getUnitInfo(eLoopUnit).getPrereqAndBonus() == self.iBonus):
										bFound = True
								else:
										j = 0
										while (not bFound and j < gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
												if (gc.getUnitInfo(eLoopUnit).getPrereqOrBonuses(j) == self.iBonus):
														bFound = True
												j += 1
						if bFound:
								szButton = gc.getUnitInfo(eLoopUnit).getButton()
								if self.top.iActivePlayer != -1:
										szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(eLoopUnit)
								screen.attachImageButton(panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False)

				for eLoopBuilding in range(gc.getNumBuildingInfos()):
						bFound = False
						if (gc.getBuildingInfo(eLoopBuilding).getPrereqAndBonus() == self.iBonus):
								bFound = True
						else:
								j = 0
								while (not bFound and j < gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
										if (gc.getBuildingInfo(eLoopBuilding).getPrereqOrBonuses(j) == self.iBonus):
												bFound = True
										j += 1
						if bFound:
								screen.attachImageButton(panelName, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
																				 WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False)

				# PAE Kulte
				for eLoopBuilding in range(gc.getNumCorporationInfos()):
						bFound = False
						j = 0
						while (not bFound and j < gc. getNUM_CORPORATION_PREREQ_BONUSES()):
								if (gc.getCorporationInfo(eLoopBuilding).getPrereqBonus(j) == self.iBonus):
										bFound = True
								j += 1
						if bFound:
								screen.attachImageButton(panelName, "", gc.getCorporationInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
																				 WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, eLoopBuilding, 1, False)

		def placeLinks(self, bRedraw):

				screen = self.top.getScreen()

				if bRedraw:
						screen.clearListBoxGFC(self.top.LIST_ID)

				# sort resources alphabetically
				rowListName = [(0, 0)]*gc.getNumBonusInfos()
				for j in range(gc.getNumBonusInfos()):
						rowListName[j] = (gc.getBonusInfo(j).getDescription(), j)
				rowListName.sort()

				iSelected = 0
				i = 0
				for iI in range(gc.getNumBonusInfos()):
						if (not gc.getBonusInfo(rowListName[iI][1]).isGraphicalOnly()):
								if bRedraw:
										screen.appendListBoxString(self.top.LIST_ID, rowListName[iI][0], WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, rowListName[iI][1], 0, CvUtil.FONT_LEFT_JUSTIFY)
								if rowListName[iI][1] == self.iBonus:
										iSelected = i
								i += 1

				screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

		# Will handle the input for this screen...
		def handleInput(self, inputClass):
				return 0
