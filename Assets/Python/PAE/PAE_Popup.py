# Made by Pie for PAE, 11.10.2025

# Meldung mit PopUp
"""
	if pPlayer.isHuman():
		szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_HEAD", ("",))
		szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_BODY", ("",))
		PAE_Popup.PopUpDDS("Art/PAE/xy.dds",szTextHead,szTextBody,"CENTER")
"""

from CvPythonExtensions import (CyGInterfaceScreen, EventContextTypes)

import CvScreenEnums
import Popup as PyPopup

# PAE: PopUps mit dds-Bild
# am besten ein Bild mit width: 320px (wegen Abstand zum Scrollbalken), height ist egal
# alignment: CENTER, LEFT, RIGHT (default)
def PopUpDDS(ddsPIC, txtHEADER, txtBODY, alignment):
	screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
	if alignment == "CENTER":
		iX = screen.getXResolution() / 2 - 200
		iY = 40
	elif alignment == "LEFT":
		iX = 90
		iY = 90
	else: # (RIGHT)
		iX = screen.getXResolution() - 456
		iY = 90
	popupDDS = PyPopup.PyPopup(4000, EventContextTypes.EVENTCONTEXT_ALL) # 4000 = PopUpID
	#popupDDS.setSize(400,400) # (INT iXS, INT iYS) geht net
	popupDDS.setPosition(iX,iY)
	popupDDS.setHeaderString(txtHEADER)
	popupDDS.addDDS(ddsPIC, 0, 0, 256, 256) # (dds, x, y, width: 360 max, height)
	popupDDS.setBodyString(u"\n\n" + txtBODY)
	popupDDS.launch()
