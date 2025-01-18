# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
# Changes by Pie for PAE V
from CvPythonExtensions import (CyGlobalContext, CyArtFileMgr, CyTranslator,
																CyGInterfaceScreen, PopupStates, FontTypes,
																WidgetTypes, PanelStyles, CyGameTextMgr,
																CivilopediaPageTypes, TableStyles)
import string
import CvUtil
# import ScreenInput
import CvScreenEnums
import CvPediaScreen  # base class
import CvPediaTech
import CvPediaUnit
import CvPediaBuilding
import CvPediaPromotion
import CvPediaUnitChart
import CvPediaBonus
import CvPediaTerrain
import CvPediaFeature
import CvPediaImprovement
import CvPediaCivic
import CvPediaCivilization
import CvPediaLeader
import CvPediaSpecialist
import CvPediaHistory
import CvPediaProject
import CvPediaReligion
import CvPediaCorporation

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvPediaMain(CvPediaScreen.CvPediaScreen):
		"Civilopedia Main Screen"

		def __init__(self):

				self.PEDIA_MAIN_SCREEN_NAME = "PediaMainScreen"
				self.INTERFACE_ART_INFO = "SCREEN_BG_OPAQUE"

				self.WIDGET_ID = "PediaMainWidget"
				self.EXIT_ID = "PediaMainExitWidget"
				self.BACKGROUND_ID = "PediaMainBackground"
				self.TOP_PANEL_ID = "PediaMainTopPanel"
				self.BOTTOM_PANEL_ID = "PediaMainBottomPanel"
				self.BACK_ID = "PediaMainBack"
				self.NEXT_ID = "PediaMainForward"
				self.TOP_ID = "PediaMainTop"
				self.LIST_ID = "PediaMainList"
				self.UPGRADES_GRAPH_ID = "PediaMainUpgradesGraph"

				self.X_SCREEN = 500
				self.Y_SCREEN = 396
				self.W_SCREEN = 1024
				self.H_SCREEN = 768
				self.Y_TITLE = 8
				self.DY_TEXT = 45

				self.X_EXIT = 994
				self.Y_EXIT = 730

				self.X_BACK = 50
				self.Y_BACK = 730

				self.X_FORWARD = 200
				self.Y_FORWARD = 730

				self.X_MENU = 450
				self.Y_MENU = 730

				self.BUTTON_SIZE = 64
				self.BUTTON_COLUMNS = 9

				self.X_ITEMS_PANE = 10  # 30
				self.Y_ITEMS_PANE = 57  # 80
				self.H_ITEMS_PANE = 650  # 610
				self.W_ITEMS_PANE = 780  # 740
				self.ITEMS_MARGIN = 18
				self.ITEMS_SEPARATION = 2

				self.X_LINKS = 797
				self.Y_LINKS = 51
				self.H_LINKS = 300
				self.W_LINKS = 225

				self.H_LINKS_FULL_H = 650

				self.nWidgetCount = 0

				# screen instances
				self.pediaTechScreen = CvPediaTech.CvPediaTech(self)
				self.pediaUnitScreen = CvPediaUnit.CvPediaUnit(self)
				self.pediaBuildingScreen = CvPediaBuilding.CvPediaBuilding(self)
				self.pediaPromotionScreen = CvPediaPromotion.CvPediaPromotion(self)
				self.pediaUnitChart = CvPediaUnitChart.CvPediaUnitChart(self)
				self.pediaBonus = CvPediaBonus.CvPediaBonus(self)
				self.pediaTerrain = CvPediaTerrain.CvPediaTerrain(self)
				self.pediaFeature = CvPediaFeature.CvPediaFeature(self)
				self.pediaImprovement = CvPediaImprovement.CvPediaImprovement(self)
				self.pediaCivic = CvPediaCivic.CvPediaCivic(self)
				self.pediaCivilization = CvPediaCivilization.CvPediaCivilization(self)
				self.pediaLeader = CvPediaLeader.CvPediaLeader(self)
				self.pediaSpecialist = CvPediaSpecialist.CvPediaSpecialist(self)
				self.pediaProjectScreen = CvPediaProject.CvPediaProject(self)
				self.pediaReligion = CvPediaReligion.CvPediaReligion(self)
				self.pediaCorporation = CvPediaCorporation.CvPediaCorporation(self)
				self.pediaHistorical = CvPediaHistory.CvPediaHistory(self)

				# used for navigating "forward" and "back" in civilopedia
				self.pediaHistory = []
				self.pediaFuture = []

				self.listCategories = []

				self.iCategory = -1
				self.iLastScreen = -1
				self.iActivePlayer = -1

				self.mapCategories = {
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH: self.placeTechs,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT: self.placeUnits,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING: self.placeBuildings,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_WONDER: self.placeWonders,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN: self.placeTerrains,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE: self.placeFeatures,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS: self.placeBoni,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT: self.placeImprovements,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST: self.placeSpecialists,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION: self.placePromotions,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP: self.placeUnitGroups,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV: self.placeCivs,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER: self.placeLeaders,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION: self.placeReligions,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_CORPORATION: self.placeCorporations,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC: self.placeCivics,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT: self.placeProjects,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT: self.placeConcepts,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW: self.placeNewConcepts,
						CivilopediaPageTypes.CIVILOPEDIA_PAGE_HINTS: self.placeHints,
						20: self.placeTraits,
						21: self.placeFormations,
						22: self.placeVeterans,
						23: self.placeRanks,
						#24: self.placeSpecialBuildings,
						24: self.placeNationalBuildings,
						25: self.placeTimelineUnits
				}

		def getScreen(self):
				return CyGInterfaceScreen(self.PEDIA_MAIN_SCREEN_NAME, CvScreenEnums.PEDIA_MAIN)

		def setPediaCommonWidgets(self):
				self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
				self.BACK_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_BACK", ()).upper() + "</font>"
				self.FORWARD_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_FORWARD", ()).upper() + "</font>"
				self.MENU_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_TOP", ()).upper() + "</font>"

				# PAE check
				#self.MENU_TEXT = self.MENU_TEXT + u" " + str(self.iLastScreen) + u" / " + str(self.iCategory)

				self.szCategoryTech = localText.getText("TXT_KEY_PEDIA_CATEGORY_TECH", ())
				self.szCategoryUnit = localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ())
				self.szCategoryBuilding = localText.getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ())
				self.szCategoryWonder = localText.getText("TXT_KEY_CONCEPT_WONDERS", ())
				self.szCategoryBonus = localText.getText("TXT_KEY_PEDIA_CATEGORY_BONUS", ())
				self.szCategoryTerrain = localText.getText("TXT_KEY_PEDIA_CATEGORY_TERRAIN", ())
				self.szCategoryFeature = localText.getText("TXT_KEY_PEDIA_CATEGORY_FEATURE", ())
				self.szCategoryImprovement = localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ())
				self.szCategorySpecialist = localText.getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST", ())
				self.szCategoryPromotion = localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ())
				self.szCategoryUnitCombat = localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ())
				self.szCategoryCiv = localText.getText("TXT_KEY_PEDIA_CATEGORY_CIV", ())
				self.szCategoryLeader = localText.getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ())
				self.szCategoryReligion = localText.getText("TXT_KEY_PEDIA_CATEGORY_RELIGION", ())
				self.szCategoryCorporation = localText.getText("TXT_KEY_CONCEPT_CORPORATIONS", ())
				self.szCategoryCivic = localText.getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ())
				self.szCategoryProject = localText.getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ())
				self.szCategoryConcept = localText.getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT_PAE", ())
				self.szCategoryConceptNew = localText.getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT_NEW", ())

				# PAE
				self.szCategoryHints = localText.getText("TXT_KEY_PEDIA_CATEGORY_HINTS", ())
				self.szCategoryRank = localText.getText("TXT_KEY_PEDIA_CATEGORY_RANKS", ())
				self.szCategoryForm = localText.getText("TXT_KEY_PEDIA_CATEGORY_FORMATIONS", ())
				self.szCategorySpecialUnits = localText.getText("TXT_KEY_PEDIA_CATEGORY_SPECIAL_UNITS", ())
				self.szCategoryNationalBuildings = localText.getText("TXT_KEY_PEDIA_CATEGORY_NATIONAL_WONDERS", ())
				self.szCategorySpecialBuildings = localText.getText("TXT_KEY_PEDIA_CATEGORY_SPECIAL_BUILDINGS", ())
				self.szCategoryVeterans = localText.getText("TXT_KEY_PEDIA_CATEGORY_VETERANS", ())
				self.szCategoryTraits = localText.getText("TXT_KEY_PEDIA_CATEGORY_TRAITS", ())
				self.szCategoryTimelineUnits = localText.getText("TXT_KEY_PEDIA_CATEGORY_TIMELINE_UNITS", ())

				self.listCategories = [self.szCategoryTech,
															 self.szCategoryUnit,
															 self.szCategoryBuilding,
															 self.szCategoryWonder,
															 self.szCategoryTerrain,
															 self.szCategoryFeature,
															 self.szCategoryBonus,
															 self.szCategoryImprovement,
															 self.szCategorySpecialist,
															 self.szCategoryPromotion,
															 self.szCategoryUnitCombat,
															 self.szCategoryCiv,
															 self.szCategoryLeader,
															 self.szCategoryReligion,
															 self.szCategoryCorporation,
															 self.szCategoryCivic,
															 self.szCategoryProject,
															 self.szCategoryConcept,
															 self.szCategoryConceptNew,
															 self.szCategoryHints,
															 self.szCategoryTraits,
															 self.szCategoryForm,
															 self.szCategoryVeterans,
															 self.szCategoryRank,
															 #self.szCategorySpecialBuildings,
															 self.szCategoryNationalBuildings,
															 self.szCategoryTimelineUnits
															 ]

				# Create a new screen
				screen = self.getScreen()
				screen.setRenderInterfaceOnly(True)
				screen.setScreenGroup(1)
				screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

				# Set background
				screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.addPanel(self.TOP_PANEL_ID, u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR)
				screen.addPanel(self.BOTTOM_PANEL_ID, u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR)
				screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

				# Exit button
				screen.setText(self.EXIT_ID, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

				# Back
				screen.setText(self.BACK_ID, "Background", self.BACK_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_BACK, self.Y_BACK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_BACK, 1, -1)

				# Forward
				screen.setText(self.NEXT_ID, "Background", self.FORWARD_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_FORWARD, self.Y_FORWARD, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_FORWARD, 1, -1)

				# Can't find out: first click (f12) doesn't create a full height bar

				# List of items on the right
				# PAE different Link menu height
				#lPediaLinksExtra = [0,1,2,3,20]
				#lPediaScreenExtra = [200,201,202]
				# if self.iLastScreen != CvScreenEnums.PEDIA_MAIN:
				##  screen.addListBoxGFC(self.LIST_ID, "", self.X_LINKS, self.Y_LINKS, self.W_LINKS, self.H_LINKS_FULL_H, TableStyles.TABLE_STYLE_STANDARD)
				# if self.iCategory in lPediaLinksExtra and self.iLastScreen not in lPediaScreenExtra and self.iLastScreen > -1:
				#  screen.addListBoxGFC(self.LIST_ID, "", self.X_LINKS, self.Y_LINKS, self.W_LINKS, self.H_LINKS, TableStyles.TABLE_STYLE_STANDARD)
				# elif self.iCategory == -1 and self.iLastScreen == -1 or self.iLastScreen in lPediaScreenExtra:
				#  screen.addListBoxGFC(self.LIST_ID, "", self.X_LINKS, self.Y_LINKS, self.W_LINKS, self.H_LINKS, TableStyles.TABLE_STYLE_STANDARD)
				# else:
				#  screen.addListBoxGFC(self.LIST_ID, "", self.X_LINKS, self.Y_LINKS, self.W_LINKS, self.H_LINKS_FULL_H, TableStyles.TABLE_STYLE_STANDARD)

				screen.addListBoxGFC(self.LIST_ID, "", self.X_LINKS, self.Y_LINKS, self.W_LINKS, self.H_LINKS_FULL_H, TableStyles.TABLE_STYLE_STANDARD)

				screen.enableSelect(self.LIST_ID, True)
				screen.setStyle(self.LIST_ID, "Table_StandardCiv_Style")

		# Screen construction function
		def showScreen(self, iCategory):
				self.iCategory = iCategory

				self.deleteAllWidgets()

				screen = self.getScreen()

				bNotActive = (not screen.isActive())
				if bNotActive or self.iLastScreen != CvScreenEnums.PEDIA_MAIN:
						self.setPediaCommonWidgets()

				# Header...                                                               + " "+str(self.iLastScreen)+" "+str(self.iCategory)
				szHeader = u"<font=4b>" + localText.getText("TXT_KEY_WIDGET_HELP", ()).upper() + u"</font>"
				szHeaderId = self.getNextWidgetName()
				screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, -1, -1)

				self.panelName = self.getNextWidgetName()
				screen.addPanel(self.panelName, "", "", False, False,
																				self.X_ITEMS_PANE, self.Y_ITEMS_PANE, self.W_ITEMS_PANE, self.H_ITEMS_PANE, PanelStyles.PANEL_STYLE_BLUE50)

				if self.iLastScreen != CvScreenEnums.PEDIA_MAIN or bNotActive:
						self.placeLinks(True)
						self.iLastScreen = CvScreenEnums.PEDIA_MAIN
				else:
						self.placeLinks(False)

				if self.mapCategories.has_key(iCategory):
						self.mapCategories.get(iCategory)()

		def placeTechs(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumTechInfos(), gc.getTechInfo)

				nColumns = 4
				nEntries = len(list) + 26  # 26 wegen Alphabet
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				A = ""
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows

						# Buchstabe
						B = item[0][:1]
						if A == "" or A != B and not B.isdigit():
								A = B
								if not iColumn:
										screen.appendTableRow(tableName)
								screen.setTableText(tableName, iColumn, iRow, u"<font=2>[" + A + u"]</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
								iCounter += 1
								iRow += 1

						if not iColumn:
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getTechInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeUnits(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumUnitInfos(), gc.getUnitInfo)
				#list = self.pediaUnitScreen.getUnitSortedList(0)

				if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
						listCopy = list[:]
						for item in listCopy:
								if not gc.getGame().isUnitEverActive(item[1]):
										list.remove(item)

				nColumns = 4
				nEntries = len(list) + 26  # 26 wegen Alphabet
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				A = ""
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						szButton = gc.getUnitInfo(item[1]).getButton()
						if self.iActivePlayer != -1:
								szButton = gc.getPlayer(self.iActivePlayer).getUnitButton(item[1])
						# Buchstabe
						B = item[0][:1]
						if A != B:
								A = B
								if not iColumn:
										screen.appendTableRow(tableName)
								screen.setTableText(tableName, iColumn, iRow, u"<font=2>[" + A + u"]</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
								iCounter += 1
								iRow += 1
						# Unitname
						if not iColumn:
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", szButton, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeSpecialUnits(self):
				screen = self.getScreen()

				# Create and place a tech pane
				#list = self.getSortedList( gc.getNumUnitInfos(), gc.getUnitInfo )
				list = self.pediaUnitScreen.getUnitSortedList(1)

				if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
						listCopy = list[:]
						for item in listCopy:
								if not gc.getGame().isUnitEverActive(item[1]):
										list.remove(item)

				nColumns = 4
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						if item[1] > 0:
								iRow = iCounter % nRows
								iColumn = iCounter // nRows
								if iRow >= iNumRows:
										iNumRows += 1
										screen.appendTableRow(tableName)
								szButton = gc.getUnitInfo(item[1]).getButton()
								if self.iActivePlayer != -1:
										szButton = gc.getPlayer(self.iActivePlayer).getUnitButton(item[1])
								screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", szButton, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
								iCounter += 1

		def placeBuildings(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.pediaBuildingScreen.getBuildingSortedList(0) # PAE
				#list = self.pediaBuildingScreen.getBuildingSortedList(False) # BTS

				if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
						listCopy = list[:]
						for item in listCopy:
								if not gc.getGame().isBuildingEverActive(item[1]):
										list.remove(item)

				nColumns = 4
				nEntries = len(list) + 26  # 26 wegen Alphabet
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				A = ""
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows

						# Buchstabe
						B = item[0][:1]
						if A != B:
								A = B
								if not iColumn:
										screen.appendTableRow(tableName)
								screen.setTableText(tableName, iColumn, iRow, u"<font=2>[" + A + u"]</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
								iCounter += 1
								iRow += 1

						if not iColumn:
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBuildingInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1


		def placeSpecialBuildings(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.pediaBuildingScreen.getBuildingSortedList(3)

				if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
						listCopy = list[:]
						for item in listCopy:
								if not gc.getGame().isBuildingEverActive(item[1]):
										list.remove(item)

				nColumns = 3
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBuildingInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1


		def placeWonders(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.pediaBuildingScreen.getBuildingSortedList(1) # PAE
				#list = self.pediaBuildingScreen.getBuildingSortedList(True) # BTS

				nColumns = 3
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBuildingInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1


		def placeNationalBuildings(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.pediaBuildingScreen.getBuildingSortedList(2)

				nColumns = 3
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBuildingInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1


		def placeBoni(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumBonusInfos(), gc.getBonusInfo)

				nColumns = 3
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getBonusInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeImprovements(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumImprovementInfos(), gc.getImprovementInfo)

				nColumns = 3
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getImprovementInfo(item[1]
																																																										).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placePromotions(self):
				screen = self.getScreen()

				# PAE : normale Promotions
				list = self.pediaPromotionScreen.getPromoSortedList(0)

				nColumns = 4
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				i = 0
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getPromotionInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeFormations(self):
				screen = self.getScreen()

				# PAE : Formationen
				list = self.pediaPromotionScreen.getPromoSortedList(1)

				nColumns = 3
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getPromotionInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeRanks(self):
				screen = self.getScreen()

				# PAE : Rangsystem
				list = self.pediaPromotionScreen.getPromoSortedList(2)

				# Alte Ansicht
				"""
				nColumns = 2
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
								nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
								screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
								iRow = iCounter % nRows
								iColumn = iCounter // nRows
								if iRow >= iNumRows:
												iNumRows += 1
												screen.appendTableRow(tableName)
								screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getPromotionInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
								iCounter += 1
				"""

				# Neue Ansicht
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, 3, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, 30, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.setTableColumnHeader(tableName, 0, "", self.W_ITEMS_PANE/3+80)
				screen.setTableColumnHeader(tableName, 1, "", self.W_ITEMS_PANE/3-40)
				screen.setTableColumnHeader(tableName, 2, "", self.W_ITEMS_PANE/3-40)
				# Columns-Ueberschriften
				screen.appendTableRow(tableName)
				screen.setTableText(tableName, 0, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY_RANKS", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 1, 0, localText.getText("TXT_KEY_WB_UNITS", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 2, 0, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				# Tabelle
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, 3, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+35, self.W_ITEMS_PANE, self.H_ITEMS_PANE-35, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				screen.setTableColumnHeader(tableName, 0, "", self.W_ITEMS_PANE/3+80)
				screen.setTableColumnHeader(tableName, 1, "", self.W_ITEMS_PANE/3-40)
				screen.setTableColumnHeader(tableName, 2, "", self.W_ITEMS_PANE/3-40)

				CivList = []

				iRow = 0
				for item in list:
						screen.appendTableRow(tableName)

						iCiv = -1
						bMelee = False
						bMounted = False
						lUnits = []
						iTech = -1
						if item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ROM_1"):
								lUnits = [gc.getInfoTypeForString("UNIT_LEGION"), gc.getInfoTypeForString("UNIT_LEGION2"), gc.getInfoTypeForString("UNIT_AUXILIAR_ROME")]
								iCiv = gc.getInfoTypeForString("CIVILIZATION_ROME")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ROM_5"):
								lUnits = [gc.getInfoTypeForString("UNIT_LEGION_OPTIO"), gc.getInfoTypeForString("UNIT_LEGION_OPTIO2")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ROM_8"):
								lUnits = [gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"), gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ROM_12"):
								lUnits = [gc.getInfoTypeForString("UNIT_LEGION_TRIBUN")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_1"):
								lUnits = [gc.getInfoTypeForString("UNIT_EQUITES"), gc.getInfoTypeForString("UNIT_HORSEMAN_EQUITES2")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_3"):
								lUnits = [gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_5"):
								lUnits = [gc.getInfoTypeForString("UNIT_LEGION_TRIBUN")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_1"):
								lUnits = [gc.getInfoTypeForString("UNIT_ROME_COMITATENSES")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_6"):
								lUnits = [gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_11"):
								lUnits = [gc.getInfoTypeForString("UNIT_ROME_COMITATENSES3"), gc.getInfoTypeForString("UNIT_ROME_SCHOLAE")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_GREEK_1"):
								lUnits = [gc.getInfoTypeForString("UNIT_HOPLIT")]
								iCiv = gc.getInfoTypeForString("CIVILIZATION_GREECE")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_GREEK_5"):
								lUnits = [gc.getInfoTypeForString("UNIT_HOPLIT_2")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_GREEK_8"):
								lUnits = [gc.getInfoTypeForString("UNIT_ELITE_HOPLIT")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_GREEK_11"):
								lUnits = [gc.getInfoTypeForString("UNIT_GREEK_STRATEGOS")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_1"):
								lUnits = [gc.getInfoTypeForString("UNIT_SPARTA_1")]
								iCiv = gc.getInfoTypeForString("CIVILIZATION_SPARTA")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_5"):
								lUnits = [gc.getInfoTypeForString("UNIT_SPARTA_2")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_8"):
								lUnits = [gc.getInfoTypeForString("UNIT_SPARTA_3")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_1"):
								bMelee = True
								iTech = gc.getInfoTypeForString("TECH_PHALANX2")
								iCiv = gc.getInfoTypeForString("CIVILIZATION_MACEDONIA")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_5"):
								lUnits = [gc.getInfoTypeForString("UNIT_PEZHETAIROI2")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_8"):
								lUnits = [gc.getInfoTypeForString("UNIT_PEZHETAIROI3")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_10"):
								lUnits = [gc.getInfoTypeForString("UNIT_PEZHETAIROI4")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_1"):
								lUnits = [gc.getInfoTypeForString("UNIT_HOPLIT_PERSIA"), gc.getInfoTypeForString("UNIT_SPEARMAN_PERSIA"), gc.getInfoTypeForString("UNIT_UNSTERBLICH")]
								iCiv = gc.getInfoTypeForString("CIVILIZATION_PERSIA")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_6"):
								lUnits = [gc.getInfoTypeForString("UNIT_APFELTRAEGER")]
								iTech = gc.getInfoTypeForString("TECH_LINOTHORAX")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_8"):
								lUnits = [gc.getInfoTypeForString("UNIT_PERSIA_AZADAN")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_1"):
								lUnits = [gc.getInfoTypeForString("UNIT_HORSEMAN_PERSIA")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_6"):
								lUnits = [gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE1")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_8"):
								lUnits = [gc.getInfoTypeForString("UNIT_CATAPHRACT_PERSIA")]
								iTech = gc.getInfoTypeForString("TECH_HORSE_ARMOR")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_12"):
								lUnits = [gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE2")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_1"):
								bMelee = True
								iTech = gc.getInfoTypeForString("TECH_BEWAFFNUNG3")
								iCiv = gc.getInfoTypeForString("CIVILIZATION_EGYPT")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_6"):
								lUnits = [gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_10"):
								lUnits = [gc.getInfoTypeForString("UNIT_WAR_CHARIOT")]
								iTech = gc.getInfoTypeForString("TECH_THE_WHEEL3")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_1"):
								lUnits = [gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT")]
								iCiv = gc.getInfoTypeForString("CIVILIZATION_CARTHAGE")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_3"):
								lUnits = [gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2")]
								iTech = gc.getInfoTypeForString("TECH_KETTENPANZER")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_5"):
								lUnits = [gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_1"):
								bMelee = True
								iTech = gc.getInfoTypeForString("TECH_BUERGERSOLDATEN")
								iCiv = gc.getInfoTypeForString("CIVILIZATION_ASSYRIA")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_4"):
								lUnits = [gc.getInfoTypeForString("UNIT_ASSUR_RANG1")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_7"):
								lUnits = [gc.getInfoTypeForString("UNIT_ASSUR_RANG2")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_11"):
								lUnits = [gc.getInfoTypeForString("UNIT_ASSUR_RANG3")]
								iTech = gc.getInfoTypeForString("TECH_THE_WHEEL3")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_SUMER_1"):
								bMelee = True
								iTech = gc.getInfoTypeForString("TECH_BUERGERSOLDATEN")
								iCiv = gc.getInfoTypeForString("CIVILIZATION_SUMERIA")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_SUMER_5"):
								lUnits = [gc.getInfoTypeForString("UNIT_SUMER_RANG1")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_SUMER_10"):
								lUnits = [gc.getInfoTypeForString("UNIT_SUMER_RANG2")]
								iTech = gc.getInfoTypeForString("TECH_THE_WHEEL3")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_GER_1"):
								bMelee = True
								iTech = gc.getInfoTypeForString("TECH_KRIEGERETHOS")
								iCiv = gc.getInfoTypeForString("CIVILIZATION_GERMANEN")
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_GER_3"):
								lUnits = [gc.getInfoTypeForString("UNIT_STAMMESFUERST")]
						elif item[1] == gc.getInfoTypeForString("PROMOTION_RANG_HUN"):
								bMounted = True
								iTech = gc.getInfoTypeForString("TECH_KRIEGERETHOS")
								iCiv = gc.getInfoTypeForString("CIVILIZATION_HUNNEN")

						# CIV
						if iCiv != -1:
								CivList.append(iCiv)
								screen.appendTableRow(tableName)
								screen.setTableText(tableName, 1, iRow+1, u"<font=4>%s</font>" % gc.getCivilizationInfo(iCiv).getDescription().upper(), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
								screen.appendTableRow(tableName)
								screen.appendTableRow(tableName)
								iRow += 3

						# Rank
						screen.setTableText(tableName, 0, iRow, u"<font=3>" + item[0] + u"</font>", gc.getPromotionInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)

						# Tech
						if iTech != -1:
								screen.setTableText(tableName, 2, iRow, gc.getTechInfo(iTech).getDescription(), gc.getTechInfo(iTech).getButton(),
																		WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, iTech, 1, CvUtil.FONT_LEFT_JUSTIFY)

						# Units
						if bMelee:
								screen.setTableText(tableName, 1, iRow, localText.getText("TXT_KEY_PEDIA_ALL_MELEE", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						elif bMounted:
								screen.setTableText(tableName, 1, iRow, localText.getText("TXT_KEY_UNITCOMBAT_MOUNTED", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						elif len(lUnits):
								i = 0
								for iUnit in lUnits:
										if i > 0:
												screen.appendTableRow(tableName)
										screen.setTableText(tableName, 1, iRow+i, gc.getUnitInfo(iUnit).getDescription(), gc.getUnitInfo(iUnit).getButton(),
																				WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, CvUtil.FONT_LEFT_JUSTIFY)
										i += 1

						iRow += max(1, len(lUnits))

		def placeUnitGroups(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumUnitCombatInfos(), gc.getUnitCombatInfo)

				nColumns = 2
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getUnitCombatInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeCivs(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumCivilizationInfos(), gc.getCivilizationInfo)

				if gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
						listCopy = list[:]
						for item in listCopy:
								if not gc.getGame().isCivEverActive(item[1]):
										list.remove(item)

				nColumns = 3
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if (gc.getCivilizationInfo(item[1]).isPlayable()):
								if iRow >= iNumRows:
										iNumRows += 1
										screen.appendTableRow(tableName)
								screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getCivilizationInfo(item[1]
																																																												 ).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
								iCounter += 1

		def placeLeaders(self):
				screen = self.getScreen()

				""" Alte original Ansicht
				# Create and place a tech pane
				list = self.getSortedList( gc.getNumLeaderHeadInfos(), gc.getLeaderHeadInfo )
				listCopy = list[:]
				for item in listCopy:
						if item[1] == gc.getDefineINT("BARBARIAN_LEADER"):
								list.remove(item)
						elif gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
								if not gc.getGame().isLeaderEverActive(item[1]):
										list.remove(item)

				nColumns = 3
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)

						iNumCivs = 0
						iLeaderCiv = -1
						for iCiv in range(gc.getNumCivilizationInfos()):
								civ = gc.getCivilizationInfo(iCiv)
								if civ.isLeaders(item[1]):
										iNumCivs += 1
										iLeaderCiv = iCiv

						if iNumCivs != 1:
								iLeaderCiv = -1

						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getLeaderHeadInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, item[1], iLeaderCiv, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1
				"""

				nColumns = 3

				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, 30, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)
				# Columns-Ueberschriften
				screen.appendTableRow(tableName)
				screen.setTableText(tableName, 0, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY_CIV", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 1, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 2, 0, localText.getText("TXT_KEY_PEDIA_TRAITS", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				iRow = 0
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+35, self.W_ITEMS_PANE, self.H_ITEMS_PANE-35, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				for iCiv in range(gc.getNumCivilizationInfos()):
						if iCiv == gc.getBARBARIAN_PLAYER():
								continue
						bParagraph = True
						for iLeader in range(gc.getNumLeaderHeadInfos()):
								if not gc.getCivilizationInfo(iCiv).isLeaders(iLeader):
										continue
								elif iLeader == gc.getDefineINT("BARBARIAN_LEADER"):
										continue
								elif gc.getDefineINT("CIVILOPEDIA_SHOW_ACTIVE_CIVS_ONLY") and gc.getGame().isFinalInitialized():
										if not gc.getGame().isLeaderEverActive(iLeader):
												continue

								# Paragraph/Abstand
								if iCiv > 0 and bParagraph:
										screen.appendTableRow(tableName)
										iRow += 1
										bParagraph = False

								screen.appendTableRow(tableName)
								# Civ
								screen.setTableText(tableName, 0, iRow, gc.getCivilizationInfo(iCiv).getDescription(), gc.getCivilizationInfo(
										iCiv).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, 1, CvUtil.FONT_LEFT_JUSTIFY)
								# Leader
								screen.setTableText(tableName, 1, iRow, gc.getLeaderHeadInfo(iLeader).getDescription(), gc.getLeaderHeadInfo(
										iLeader).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, iCiv, CvUtil.FONT_LEFT_JUSTIFY)
								# Traits (Ansicht nur fuer 2 Traits programmiert)
								szText = ""
								for iTrait in range(gc.getNumTraitInfos()):
										if gc.getLeaderHeadInfo(iLeader).hasTrait(iTrait):
												if szText == "":
														szText = u"( %s /" % gc.getTraitInfo(iTrait).getDescription()
												else:
														szText += u" %s )" % gc.getTraitInfo(iTrait).getDescription()
														break
								screen.setTableText(tableName, 2, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

								iRow += 1

		def placeReligions(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumReligionInfos(), gc.getReligionInfo)

				nColumns = 1
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getReligionInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeCorporations(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumCorporationInfos(), gc.getCorporationInfo)

				nColumns = 1
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getCorporationInfo(item[1]
																																																										).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeCivics(self):
				screen = self.getScreen()

				""" Alte Originalansicht
					# Create and place a tech pane
					list = self.getSortedList( gc.getNumCivicInfos(), gc.getCivicInfo )

					nColumns = 3
					nEntries = len(list)
					nRows = nEntries // nColumns
					if (nEntries % nColumns):
									nRows += 1
					tableName = self.getNextWidgetName()
					screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
					screen.enableSelect(tableName, False)
					for i in range(nColumns):
									screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

					iCounter = 0
					iNumRows = 0
					for item in list:
									iRow = iCounter % nRows
									iColumn = iCounter // nRows
									if iRow >= iNumRows:
													iNumRows += 1
													screen.appendTableRow(tableName)
									screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getCivicInfo(item[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
									iCounter += 1
				"""

				nColumns = 5

				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, 30, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.setTableColumnHeader(tableName, 0, "", 80)
				screen.setTableColumnHeader(tableName, 1, "", 110)
				screen.setTableColumnHeader(tableName, 2, "", 190)
				screen.setTableColumnHeader(tableName, 3, "", 190)
				screen.setTableColumnHeader(tableName, 4, "", 210)
				# Columns-Ueberschriften
				screen.appendTableRow(tableName)
				screen.setTableText(tableName, 0, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 1, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY_ANARCHY", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_CENTER_JUSTIFY)
				screen.setTableText(tableName, 2, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 3, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 4, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY_UPKEEP", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				iRow = 0
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+35, self.W_ITEMS_PANE, self.H_ITEMS_PANE-35, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				screen.setTableColumnHeader(tableName, 0, "", 80)
				screen.setTableColumnHeader(tableName, 1, "", 110)
				screen.setTableColumnHeader(tableName, 2, "", 190)
				screen.setTableColumnHeader(tableName, 3, "", 190)
				screen.setTableColumnHeader(tableName, 4, "", 210)

				for iCivicOption in range(gc.getNumCivicOptionInfos()):
						bParagraph = True
						for iCivic in range(gc.getNumCivicInfos()):
								if gc.getCivicInfo(iCivic).getCivicOptionType() != iCivicOption:
										continue

								# Paragraph/Abstand
								if iCivicOption > 0 and bParagraph:
										screen.appendTableRow(tableName)
										iRow += 1
										bParagraph = False

								screen.appendTableRow(tableName)
								# Civic Option
								screen.setTableText(tableName, 0, iRow, gc.getCivicOptionInfo(iCivicOption).getDescription(), "", WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1, CvUtil.FONT_LEFT_JUSTIFY)
								# Anarchy length
								screen.setTableText(tableName, 1, iRow, str(gc.getCivicInfo(iCivic).getAnarchyLength()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
								# Civic
								screen.setTableText(tableName, 2, iRow, gc.getCivicInfo(iCivic).getDescription(), gc.getCivicInfo(
										iCivic).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1, CvUtil.FONT_LEFT_JUSTIFY)
								# Tech
								szText = ""
								iTech = gc.getCivicInfo(iCivic).getTechPrereq()
								if iTech > -1:
										screen.setTableText(tableName, 3, iRow, gc.getTechInfo(iTech).getDescription(), gc.getTechInfo(
												iTech).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, CvUtil.FONT_LEFT_JUSTIFY)
								# Upkeep
								pUpkeepInfo = gc.getUpkeepInfo(gc.getCivicInfo(iCivic).getUpkeep())
								if pUpkeepInfo:
										szText = pUpkeepInfo.getDescription()
								else:
										szText = localText.getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
								screen.setTableText(tableName, 4, iRow, szText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

								iRow += 1

		def placeProjects(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.pediaProjectScreen.getProjectSortedList()

				nColumns = 1
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iRow = iCounter % nRows
						iColumn = iCounter // nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getProjectInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeTerrains(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumTerrainInfos(), gc.getTerrainInfo)

				nColumns = 1
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iColumn = iCounter // nRows
						iRow = iCounter % nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getTerrainInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeFeatures(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumFeatureInfos(), gc.getFeatureInfo)

				nColumns = 2
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iColumn = iCounter // nRows
						iRow = iCounter % nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getFeatureInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeConcepts(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumConceptInfos(), gc.getConceptInfo)

				nColumns = 3
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iColumn = iCounter // nRows
						iRow = iCounter % nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getConceptInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, item[1], CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeNewConcepts(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumNewConceptInfos(), gc.getNewConceptInfo)

				nColumns = 2
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iColumn = iCounter // nRows
						iRow = iCounter % nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getNewConceptInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_DESCRIPTION, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, item[1], CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeSpecialists(self):
				screen = self.getScreen()

				# Create and place a tech pane
				list = self.getSortedList(gc.getNumSpecialistInfos(), gc.getSpecialistInfo)

				nColumns = 2
				nEntries = len(list)
				nRows = nEntries // nColumns
				if (nEntries % nColumns):
						nRows += 1
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				iCounter = 0
				iNumRows = 0
				for item in list:
						iColumn = iCounter // nRows
						iRow = iCounter % nRows
						if iRow >= iNumRows:
								iNumRows += 1
								screen.appendTableRow(tableName)
						screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", gc.getSpecialistInfo(item[1]).getButton(),
																WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
						iCounter += 1

		def placeHints(self):
				screen = self.getScreen()

				self.szAreaId = self.getNextWidgetName()
				screen.addListBoxGFC(self.szAreaId, "",
														 self.X_ITEMS_PANE, self.Y_ITEMS_PANE, self.W_ITEMS_PANE, self.H_ITEMS_PANE, TableStyles.TABLE_STYLE_STANDARD)

				szHintsText = CyGameTextMgr().buildHintsList()
				hintText = string.split(szHintsText, "\n")
				for hint in hintText:
						if len(hint) != 0:
								screen.appendListBoxStringNoUpdate(self.szAreaId, hint, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				screen.updateListBox(self.szAreaId)

		# Staatsoberhaupt-Merkmale

		def placeTraits(self):
				screen = self.getScreen()

				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, 1, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, 30, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.setTableText(tableName, 0, 0, localText.getText("TXT_KEY_PEDIA_TRAITS", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				lTraits = []
				szSpecialText = ""
				iT1 = -1
				iT2 = -1
				for iLeader in range(gc.getNumLeaderHeadInfos()):
						iT1 = -1
						# bChecked = False
						for iTrait in range(gc.getNumTraitInfos()):
								if gc.getLeaderHeadInfo(iLeader).hasTrait(iTrait):
										if iT1 == -1:
												iT1 = iTrait
										else:
												iT2 = iTrait
												break

						if iT1 not in lTraits and iT2 not in lTraits:
								lTraits.append(iT1)
								lTraits.append(iT2)
								szSpecialText += CyGameTextMgr().parseLeaderTraits(iLeader, -1, False, True)

				szSpecialText = szSpecialText[1:]
				screen.addMultilineText(self.getNextWidgetName(), szSpecialText,
																self.X_ITEMS_PANE+5, self.Y_ITEMS_PANE+35, self.W_ITEMS_PANE, self.H_ITEMS_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		def placeVeterans(self):
				screen = self.getScreen()

				nColumns = 4

				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, 30, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)
				# Columns-Ueberschriften
				screen.appendTableRow(tableName)
				screen.setTableText(tableName, 0, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY_CIV", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 1, 0, localText.getText("TXT_KEY_WB_UNIT", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 2, 0, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 3, 0, localText.getText("TXT_KEY_PEDIA_UPGRADE", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				iRow = 0
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+35, self.W_ITEMS_PANE, self.H_ITEMS_PANE-35, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				# lUnits = Civ, Unit or UnitType, UpgradeUnit, Promotion
				# UnitType: -1 = Alle Einheiten, -2 = Berittene Einheiten
				# Die Original-Liste ist in PAE_Lists (RangPromoUp)
				# Hier ist eine erweiterte Liste inkl. UNIT_PRAETORIANs für die Pedia
				iRome = gc.getInfoTypeForString("CIVILIZATION_ROME")
				LRankUnits = [
						(iRome, gc.getInfoTypeForString("UNIT_ARCHER_ROME"), gc.getInfoTypeForString("UNIT_ARCHER_LEGION"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_ARCHER_LEGION"), gc.getInfoTypeForString("UNIT_HORSE_ARCHER_ROMAN"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_HASTA"), gc.getInfoTypeForString("UNIT_CELERES"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_PRINCIPES"), gc.getInfoTypeForString("UNIT_TRIARII"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_HASTATI"), gc.getInfoTypeForString("UNIT_TRIARII"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_PILUMNI"), gc.getInfoTypeForString("UNIT_TRIARII"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_TRIARII"), gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION"), gc.getInfoTypeForString("UNIT_LEGION_OPTIO"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_OPTIO"), gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_7")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"), gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_11")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION"), gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_OPTIO"), gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_CENTURIO"), gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION2"), gc.getInfoTypeForString("UNIT_LEGION_OPTIO2"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_OPTIO2"), gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_7")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"), gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_11")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION2"), gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_OPTIO2"), gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_CENTURIO2"), gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(iRome, gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("UNIT_PRAETORIAN2"), gc.getInfoTypeForString("PROMOTION_COMBAT1")),
						(iRome, gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("UNIT_ROME_COHORTES_URBANAE"), gc.getInfoTypeForString("PROMOTION_COMBAT1")),
						(iRome, gc.getInfoTypeForString("UNIT_PRAETORIAN"), gc.getInfoTypeForString("UNIT_HORSEMAN_EQUITES2"), gc.getInfoTypeForString("PROMOTION_COMBAT1")),
						(iRome, gc.getInfoTypeForString("UNIT_LEGION_EVOCAT"), gc.getInfoTypeForString("UNIT_PRAETORIAN3"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_PRAETORIAN2"), gc.getInfoTypeForString("UNIT_PRAETORIAN3"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COHORTES_URBANAE"), gc.getInfoTypeForString("UNIT_PRAETORIAN3"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_EQUITES"), gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_3")),
						(iRome, gc.getInfoTypeForString("UNIT_EQUITES"), gc.getInfoTypeForString("UNIT_PRAETORIAN_RIDER"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_HORSEMAN_EQUITES2"), gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_3")),
						(iRome, gc.getInfoTypeForString("UNIT_HORSEMAN_DECURIO"), gc.getInfoTypeForString("UNIT_LEGION_TRIBUN"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_EQUES_5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_LIMITANEI"), gc.getInfoTypeForString("UNIT_ROME_LIMITANEI_GARDE"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COMITATENSES"), gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2"), gc.getInfoTypeForString("UNIT_ROME_COMITATENSES3"), gc.getInfoTypeForString("PROMOTION_RANG_ROM_LATE_10")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COMITATENSES2"), gc.getInfoTypeForString("UNIT_ROME_PALATINI"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_COMITATENSES3"), gc.getInfoTypeForString("UNIT_ROME_PALATINI"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_ROME_PALATINI"), gc.getInfoTypeForString("UNIT_ROME_SCHOLAE"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_CLIBANARII_ROME"), gc.getInfoTypeForString("UNIT_ROME_SCHOLAE"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(iRome, gc.getInfoTypeForString("UNIT_CATAPHRACT_ROME"), gc.getInfoTypeForString("UNIT_ROME_SCHOLAE"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_HOPLIT"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_HOPLIT"), gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_HOPLIT_SPARTA"), gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_HOPLIT"), gc.getInfoTypeForString("UNIT_HOPLIT_2"), gc.getInfoTypeForString("PROMOTION_RANG_GREEK_4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), gc.getInfoTypeForString("UNIT_HOPLIT_2"), gc.getInfoTypeForString("PROMOTION_RANG_GREEK_4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_HOPLIT_2"), gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"), gc.getInfoTypeForString("PROMOTION_RANG_GREEK_7")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_ELITE_HOPLIT"), gc.getInfoTypeForString("UNIT_GREEK_STRATEGOS"), gc.getInfoTypeForString("PROMOTION_RANG_GREEK_10")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK"), gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK2"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_GREECE"), -2, gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_SPARTA"), gc.getInfoTypeForString("UNIT_HOPLIT"), gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_SPARTA"), gc.getInfoTypeForString("UNIT_HOPLIT_SPARTA"), gc.getInfoTypeForString("UNIT_HOPLIT_KALOS"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_SPARTA"), -1, gc.getInfoTypeForString("UNIT_SPARTA_1"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_SPARTA"), gc.getInfoTypeForString("UNIT_SPARTA_1"), gc.getInfoTypeForString("UNIT_SPARTA_2"), gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_4")),
						(gc.getInfoTypeForString("CIVILIZATION_SPARTA"), gc.getInfoTypeForString("UNIT_SPARTA_2"), gc.getInfoTypeForString("UNIT_SPARTA_3"), gc.getInfoTypeForString("PROMOTION_RANG_SPARTA_7")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK"), gc.getInfoTypeForString("UNIT_ARCHER_REFLEX_GREEK2"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_HYPASPIST"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_HYPASPIST"), gc.getInfoTypeForString("UNIT_HYPASPIST2"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_7")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_HYPASPIST2"), gc.getInfoTypeForString("UNIT_HYPASPIST3"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_9")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_PEZHETAIROI2"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_PEZHETAIROI"), gc.getInfoTypeForString("UNIT_PEZHETAIROI2"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_PEZHETAIROI2"), gc.getInfoTypeForString("UNIT_PEZHETAIROI3"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_7")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_PEZHETAIROI3"), gc.getInfoTypeForString("UNIT_PEZHETAIROI4"), gc.getInfoTypeForString("PROMOTION_RANG_MACEDON_9")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON"), gc.getInfoTypeForString("UNIT_COMPANION_CAVALRY"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_COMPANION_CAVALRY"), gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON3"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON3"), gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON4"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_MACEDONIA"), gc.getInfoTypeForString("UNIT_HORSEMAN_MACEDON4"), gc.getInfoTypeForString("UNIT_GREEK_HIPPARCH"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_UNSTERBLICH"), gc.getInfoTypeForString("UNIT_UNSTERBLICH_2"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), -1, gc.getInfoTypeForString("UNIT_APFELTRAEGER"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_5")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_APFELTRAEGER"), gc.getInfoTypeForString("UNIT_UNSTERBLICH_2"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_7")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_APFELTRAEGER"), gc.getInfoTypeForString("UNIT_PERSIA_AZADAN"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_10")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_UNSTERBLICH_2"), gc.getInfoTypeForString("UNIT_PERSIA_AZADAN"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA_10")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_HORSEMAN_PERSIA"), gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE1"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_5")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE1"), gc.getInfoTypeForString("UNIT_CATAPHRACT_PERSIA"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_7")),
						(gc.getInfoTypeForString("CIVILIZATION_PERSIA"), gc.getInfoTypeForString("UNIT_CATAPHRACT_PERSIA"), gc.getInfoTypeForString("UNIT_HORSE_PERSIA_NOBLE2"), gc.getInfoTypeForString("PROMOTION_RANG_PERSIA2_11")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_EGYPT"), -1, gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_EGYPT"), gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"), gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"), gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_5")),
						(gc.getInfoTypeForString("CIVILIZATION_EGYPT"), gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"), gc.getInfoTypeForString("UNIT_WAR_CHARIOT"), gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_10")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_NUBIA"), -1, gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_NUBIA"), gc.getInfoTypeForString("UNIT_EGYPT_CHEPESCH"), gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"), gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_5")),
						(gc.getInfoTypeForString("CIVILIZATION_NUBIA"), gc.getInfoTypeForString("UNIT_STATTHALTER_EGYPT"), gc.getInfoTypeForString("UNIT_WAR_CHARIOT"), gc.getInfoTypeForString("PROMOTION_RANG_EGYPT_10")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_2")),
						(gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_2")),
						(gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_4")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_PHON"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_PHON"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_PHON"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_SWORD"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_2")),
						(gc.getInfoTypeForString("CIVILIZATION_PHON"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_2")),
						(gc.getInfoTypeForString("CIVILIZATION_PHON"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_HOPLIT2"), gc.getInfoTypeForString("UNIT_CARTH_SACRED_BAND_OFFICER"), gc.getInfoTypeForString("PROMOTION_RANG_CARTHAGE_4")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"), -1, gc.getInfoTypeForString("UNIT_ASSUR_RANG1"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_3")),
						(gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"), gc.getInfoTypeForString("UNIT_ASSUR_RANG2"), gc.getInfoTypeForString("UNIT_ASSUR_RANG3"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_6")),
						(gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"), gc.getInfoTypeForString("UNIT_ASSUR_RANG3"), gc.getInfoTypeForString("UNIT_ELITE_ASSUR"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_10")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_BABYLON"), -1, gc.getInfoTypeForString("UNIT_ASSUR_RANG1"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_3")),
						(gc.getInfoTypeForString("CIVILIZATION_BABYLON"), gc.getInfoTypeForString("UNIT_ASSUR_RANG2"), gc.getInfoTypeForString("UNIT_ASSUR_RANG3"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_6")),
						(gc.getInfoTypeForString("CIVILIZATION_BABYLON"), gc.getInfoTypeForString("UNIT_ASSUR_RANG3"), gc.getInfoTypeForString("UNIT_ELITE_ASSUR"), gc.getInfoTypeForString("PROMOTION_RANG_ASSUR_10")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_SUMERIA"), -1, gc.getInfoTypeForString("UNIT_ELITE_SUMER"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_SUMERIA"), -1, gc.getInfoTypeForString("UNIT_SUMER_RANG1"), gc.getInfoTypeForString("PROMOTION_RANG_SUMER_4")),
						(gc.getInfoTypeForString("CIVILIZATION_SUMERIA"), gc.getInfoTypeForString("UNIT_SUMER_RANG1"), gc.getInfoTypeForString("UNIT_SUMER_RANG2"), gc.getInfoTypeForString("PROMOTION_RANG_SUMER_9")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_ISRAEL"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_MACCABEE"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_INDIA"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_RADSCHA"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_INDIA"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_INDIAN_NAYAR"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_DAKER"), gc.getInfoTypeForString("UNIT_SCHILDTRAEGER"), gc.getInfoTypeForString("UNIT_FUERST_DAKER"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_GERMANEN"), -1, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_GERMANEN"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_GERMAN_HARIER"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_GERMANEN"), gc.getInfoTypeForString("UNIT_AXEMAN2"), gc.getInfoTypeForString("UNIT_BERSERKER_GERMAN"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_CELT"), -1, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_GALLIEN"), -1, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_VANDALS"), -1, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(gc.getInfoTypeForString("CIVILIZATION_BRITEN"), gc.getInfoTypeForString("UNIT_SPEARMAN"), gc.getInfoTypeForString("UNIT_CELTIC_FIANNA"), gc.getInfoTypeForString("PROMOTION_COMBAT4")),
						(gc.getInfoTypeForString("CIVILIZATION_BRITEN"), -1, gc.getInfoTypeForString("UNIT_STAMMESFUERST"), gc.getInfoTypeForString("PROMOTION_COMBAT5")),
						(-1,0,0,0),
						(gc.getInfoTypeForString("CIVILIZATION_HUNNEN"), gc.getInfoTypeForString("UNIT_MONGOL_KESHIK"), gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN_HUN"), gc.getInfoTypeForString("PROMOTION_COMBAT5"))
				]

				for unit in LRankUnits:
						screen.appendTableRow(tableName)

						# Leere Zeile
						if unit[0] == -1:
								screen.setTableText(tableName, 0, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText(tableName, 1, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText(tableName, 2, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								screen.setTableText(tableName, 3, iRow, "", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						else:
							# Civ
							screen.setTableText(tableName, 0, iRow, gc.getCivilizationInfo(unit[0]).getDescription(), gc.getCivilizationInfo(
									unit[0]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, unit[0], 1, CvUtil.FONT_LEFT_JUSTIFY)

							# Unit
							if unit[1] == -1:
									screen.setTableText(tableName, 1, iRow, localText.getText("TXT_KEY_PEDIA_ALL_MELEE", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							elif unit[1] == -2:
									screen.setTableText(tableName, 1, iRow, localText.getText("TXT_KEY_UNITCOMBAT_MOUNTED", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							else:
									screen.setTableText(tableName, 1, iRow, gc.getUnitInfo(unit[1]).getDescription(), gc.getUnitInfo(
											unit[1]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, unit[1], 1, CvUtil.FONT_LEFT_JUSTIFY)

							# Bedingung
							if unit[3] != -1:
									screen.setTableText(tableName, 2, iRow, gc.getPromotionInfo(unit[3]).getDescription(), gc.getPromotionInfo(
											unit[3]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, unit[3], 1, CvUtil.FONT_LEFT_JUSTIFY)

							# Upgrade
							if unit[2] != -1:
									screen.setTableText(tableName, 3, iRow, gc.getUnitInfo(unit[2]).getDescription(), gc.getUnitInfo(
											unit[2]).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, unit[2], 1, CvUtil.FONT_LEFT_JUSTIFY)

						iRow += 1

		def placeTimelineUnits(self):
				screen = self.getScreen()

				nColumns = 3

				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+5, self.W_ITEMS_PANE, 30, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)
				# Columns-Ueberschriften
				screen.appendTableRow(tableName)
				screen.setTableText(tableName, 0, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 1, 0, localText.getText("TXT_KEY_WB_UNIT", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, 2, 0, localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ()), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

				iRow = 0
				tableName = self.getNextWidgetName()
				screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+35, self.W_ITEMS_PANE, self.H_ITEMS_PANE-35, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				screen.enableSelect(tableName, False)
				for i in range(nColumns):
						screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

				for iEra in range(gc.getNumEraInfos()):
						if iEra > 5:
								break
						lTechs = []
						iTech = 0
						for iTech in range(gc.getNumTechInfos()):
								if gc.getTechInfo(iTech).getEra() == iEra:
										lTechs.append(iTech)

						if len(lTechs):

								# Era-Description
								screen.appendTableRow(tableName)
								screen.appendTableRow(tableName)
								screen.setTableText(tableName, 1, iRow+1, u"<font=4>%s</font>" % gc.getEraInfo(iEra).getDescription(), "", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_CENTER_JUSTIFY)
								screen.appendTableRow(tableName)
								iRow += 3

								iUnit = 0
								for iUnit in range(gc.getNumUnitInfos()):
										iTech = gc.getUnitInfo(iUnit).getPrereqAndTech()
										if iUnit != -1 and iTech in lTechs:
												iUnitCombat = gc.getUnitInfo(iUnit).getUnitCombatType()
												screen.appendTableRow(tableName)
												# Tech
												if iTech != -1:
														screen.setTableText(tableName, 0, iRow, gc.getTechInfo(iTech).getDescription(), gc.getTechInfo(
																iTech).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, CvUtil.FONT_LEFT_JUSTIFY)
												# Unit
												screen.setTableText(tableName, 1, iRow, gc.getUnitInfo(iUnit).getDescription(), gc.getUnitInfo(
														iUnit).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUnit, 1, CvUtil.FONT_LEFT_JUSTIFY)
												# Combat type
												if iUnitCombat != -1:
														screen.setTableText(tableName, 2, iRow, gc.getUnitCombatInfo(iUnitCombat).getDescription(), gc.getUnitCombatInfo(
																iUnitCombat).getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iUnitCombat, 1, CvUtil.FONT_LEFT_JUSTIFY)
												iRow += 1

		def placeLinks(self, bRedraw):

				screen = self.getScreen()

				if bRedraw:
						screen.clearListBoxGFC(self.LIST_ID)

				i = 0
				for szCategory in self.listCategories:
						if bRedraw:
								screen.appendListBoxStringNoUpdate(self.LIST_ID, szCategory, WidgetTypes.WIDGET_PEDIA_MAIN, i, 0, CvUtil.FONT_LEFT_JUSTIFY)
						i += 1

				if bRedraw:
						screen.updateListBox(self.LIST_ID)

				screen.setSelectedListBoxStringGFC(self.LIST_ID, self.iCategory)

		# returns a unique ID for a widget in this screen
		def getNextWidgetName(self):
				szName = self.WIDGET_ID + str(self.nWidgetCount)
				self.nWidgetCount += 1
				return szName

		def pediaJump(self, iScreen, iEntry, bRemoveFwdList):

				if (iEntry < 0):
						return

				self.iActivePlayer = gc.getGame().getActivePlayer()

				self.pediaHistory.append((iScreen, iEntry))
				if (bRemoveFwdList):
						self.pediaFuture = []

				if (iScreen == CvScreenEnums.PEDIA_MAIN):
						self.showScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_TECH):
						self.pediaTechScreen.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_UNIT):
						self.pediaUnitScreen.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_BUILDING):
						self.pediaBuildingScreen.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_PROMOTION):
						self.pediaPromotionScreen.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_UNIT_CHART):
						self.pediaUnitChart.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_BONUS):
						self.pediaBonus.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_TERRAIN):
						self.pediaTerrain.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_FEATURE):
						self.pediaFeature.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_IMPROVEMENT):
						self.pediaImprovement.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_CIVIC):
						self.pediaCivic.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_CIVILIZATION):
						self.pediaCivilization.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_LEADER):
						self.pediaLeader.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_SPECIALIST):
						self.pediaSpecialist.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_PROJECT):
						self.pediaProjectScreen.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_RELIGION):
						self.pediaReligion.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_CORPORATION):
						self.pediaCorporation.interfaceScreen(iEntry)
				elif (iScreen == CvScreenEnums.PEDIA_HISTORY):
						self.pediaHistorical.interfaceScreen(iEntry)

		def back(self):
				if (len(self.pediaHistory) > 1):
						self.pediaFuture.append(self.pediaHistory.pop())
						current = self.pediaHistory.pop()
						self.pediaJump(current[0], current[1], False)
				return 1

		def forward(self):
				if (self.pediaFuture):
						current = self.pediaFuture.pop()
						self.pediaJump(current[0], current[1], False)
				return 1

		def pediaShow(self):
				if (not self.pediaHistory):
						self.pediaHistory.append((CvScreenEnums.PEDIA_MAIN, 0))

				current = self.pediaHistory.pop()

				# erase history so it doesn't grow too large during the game
				self.pediaFuture = []
				self.pediaHistory = []

				# jump to the last screen that was up
				self.pediaJump(current[0], current[1], False)

		def link(self, szLink):
				if (szLink == "PEDIA_MAIN_TECH"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH), True)
				if (szLink == "PEDIA_MAIN_UNIT"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT), True)
				if (szLink == "PEDIA_MAIN_BUILDING"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING), True)
				if (szLink == "PEDIA_MAIN_TERRAIN"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN), True)
				if (szLink == "PEDIA_MAIN_FEATURE"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE), True)
				if (szLink == "PEDIA_MAIN_BONUS"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS), True)
				if (szLink == "PEDIA_MAIN_IMPROVEMENT"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT), True)
				if (szLink == "PEDIA_MAIN_SPECIALIST"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST), True)
				if (szLink == "PEDIA_MAIN_PROMOTION"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION), True)
				if (szLink == "PEDIA_MAIN_UNIT_GROUP"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP), True)
				if (szLink == "PEDIA_MAIN_CIV"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV), True)
				if (szLink == "PEDIA_MAIN_LEADER"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER), True)
				if (szLink == "PEDIA_MAIN_RELIGION"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION), True)
				if (szLink == "PEDIA_MAIN_CORPORATION"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CORPORATION), True)
				if (szLink == "PEDIA_MAIN_CIVIC"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC), True)
				if (szLink == "PEDIA_MAIN_PROJECT"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT), True)
				if (szLink == "PEDIA_MAIN_CONCEPT"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT), True)
				if (szLink == "PEDIA_MAIN_CONCEPT_NEW"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW), True)
				if (szLink == "PEDIA_MAIN_HINTS"):
						return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_HINTS), True)

				for i in range(gc.getNumConceptInfos()):
						if (gc.getConceptInfo(i).isMatchForLink(szLink, False)):
								iEntryId = self.pediaHistorical.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, i)
								return self.pediaJump(CvScreenEnums.PEDIA_HISTORY, iEntryId, True)
				for i in range(gc.getNumNewConceptInfos()):
						if (gc.getNewConceptInfo(i).isMatchForLink(szLink, False)):
								iEntryId = self.pediaHistorical.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW, i)
								return self.pediaJump(CvScreenEnums.PEDIA_HISTORY, iEntryId, True)
				for i in range(gc.getNumTechInfos()):
						if (gc.getTechInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_TECH, i, True)
				for i in range(gc.getNumUnitInfos()):
						if (gc.getUnitInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_UNIT, i, True)
				for i in range(gc.getNumCorporationInfos()):
						if (gc.getCorporationInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_CORPORATION, i, True)
				for i in range(gc.getNumBuildingInfos()):
						if (gc.getBuildingInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_BUILDING, i, True)
				for i in range(gc.getNumPromotionInfos()):
						if (gc.getPromotionInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_PROMOTION, i, True)
				for i in range(gc.getNumUnitCombatInfos()):
						if (gc.getUnitCombatInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_UNIT_CHART, i, True)
				for i in range(gc.getNumBonusInfos()):
						if (gc.getBonusInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_BONUS, i, True)
				for i in range(gc.getNumTerrainInfos()):
						if (gc.getTerrainInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_TERRAIN, i, True)
				for i in range(gc.getNumFeatureInfos()):
						if (gc.getFeatureInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_FEATURE, i, True)
				for i in range(gc.getNumImprovementInfos()):
						if (gc.getImprovementInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_IMPROVEMENT, i, True)
				for i in range(gc.getNumCivicInfos()):
						if (gc.getCivicInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_CIVIC, i, True)
				for i in range(gc.getNumCivilizationInfos()):
						if (gc.getCivilizationInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_CIVILIZATION, i, True)
				for i in range(gc.getNumLeaderHeadInfos()):
						if (gc.getLeaderHeadInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_LEADER, i, True)
				for i in range(gc.getNumSpecialistInfos()):
						if (gc.getSpecialistInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_SPECIALIST, i, True)
				for i in range(gc.getNumProjectInfos()):
						if (gc.getProjectInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_PROJECT, i, True)
				for i in range(gc.getNumReligionInfos()):
						if (gc.getReligionInfo(i).isMatchForLink(szLink, False)):
								return self.pediaJump(CvScreenEnums.PEDIA_RELIGION, i, True)

		def deleteAllWidgets(self):
				screen = self.getScreen()
				iNumWidgets = self.nWidgetCount
				self.nWidgetCount = 0
				for i in range(iNumWidgets):
						screen.deleteWidget(self.getNextWidgetName())
				self.nWidgetCount = 0

		# Will handle the input for this screen...

		def handleInput(self, inputClass):
				# redirect to proper screen if necessary
				if (self.iLastScreen == CvScreenEnums.PEDIA_UNIT):
						return self.pediaUnitScreen.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_TECH):
						return self.pediaTechScreen.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_BUILDING):
						return self.pediaBuildingScreen.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_PROMOTION):
						return self.pediaPromotionScreen.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_UNIT_CHART):
						return self.pediaUnitChart.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_BONUS):
						return self.pediaBonus.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_TERRAIN):
						return self.pediaTerrain.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_FEATURE):
						return self.pediaFeature.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_IMPROVEMENT):
						return self.pediaImprovement.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_CIVIC):
						return self.pediaCivic.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_CIVILIZATION):
						return self.pediaCivilization.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_LEADER):
						return self.pediaLeader.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_SPECIALIST):
						return self.pediaSpecialist.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_PROJECT):
						return self.pediaProjectScreen.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_RELIGION):
						return self.pediaReligion.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_CORPORATION):
						return self.pediaCorporation.handleInput(inputClass)
				if (self.iLastScreen == CvScreenEnums.PEDIA_HISTORY):
						return self.pediaHistorical.handleInput(inputClass)

				return 0
