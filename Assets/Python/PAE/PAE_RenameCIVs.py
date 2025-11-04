# Imports
from CvPythonExtensions import (CyGlobalContext, CyTranslator, CyGame, CyInterface, ColorTypes)
import CvUtil
import PAE_Popup

# Defines
gc = CyGlobalContext()

# ---------------------------------------------
# PAE 7.13 Rename CIVs (changePlayer,changeTeam,changeCiv,setPlayer,setTeam,setCiv)
# in Late Antiquity for Early Middle Ages
# ---------------------------------------------

#Britonen - Pikten (300-600, Coroticus) - Angelsachsen (ab 600, Alfred der Große(871-899))
#Parther - Alanen (ab 300, Goar)
#Perser - Sassaniden (Sasan, 300-700) - Kalifat der Abbasiden (ab 700, Abu l-Abbas as-Saffah)
#Phönizier - Ghassaniden (300, Arethas)

#Kelten - Bajuwaren (ab 400, 500 Garibald)
#Vandalen - Westgoten (ab 400, Alarich I)
#Dakien - Sarmaten (ab 400, Rausimod)
#Gallier oder Germanen: 
#A) wenn nur einer von beiden existiert: 
#Franken ab 400 (400 Childerich, 500 Chlodwig, ab 800 Karl der Große)
#B)
#Gallien: Merowinger Childerich I (400 bis 500) - Merowinger Chlodwig I (500-700)) - Karolinger Karl d.G. (700-800) - Westfranken (800-1000, Karl der Kahle)
#Germanen - Alemannen (400-800) - Ostfranken (800-1000, Ludwig der Deutsche)

#Skythen - Bulgaren (ab 500, Khan Asparuch)
#Etrusker - Langobarden (500 , Alboin)
#Rom - Ostgoten (500, Theoderich der Große) - Heiliges Römisches Reich (800-1800, Karolinger Otto der Große, 912-1024)

#Hunnen - Awaren (ab 600, Bajan Khagan) - Magyaren (ab 800, Arpad)
#Karthager - Umayyaden (600, Muawiya I.)
#Illyrer - Slawen (600, Dušan der Mächtige)
#Lyder - Turkmenen (600, Arkadag = "Beschützer")
#Sumer - Lachmiden (600, al-Mundhir III.)

#Araber = Sarazenen (ab 700, Menschen des Ostens, Abd ar-Rahman)
#Berber - Mauren (ab 700, Tariq ibn Ziyad)
#Iberer - Asturien (700, Pelayo)
#Assyrer - Kurden (700, Babak Khorramdin)
#Babylon - if Islam: Kalifat von [capital], ab 700

#Hethiter - Seldschuken (800, Suleiman ibn Kutalmis)

#---- if Christentum: Heiliges [civ_adj] Reich
#---- if Islam: Kalifat von [capital]
# ---------------------------------------------
#pPlayer.changeLeader(x) # change to XML leader
#pPlayer.changeCiv(x) # change to XML Civ
#pPlayer.setName(x) # Leader's name
#pPlayer.setCivName("AAA", "BBB", "CCC") # CivDesc, CivShortDesc, CivAdjective
# ----- bei Karten mit mehreren gleichen CIVs wird der Beste umbenannt -------
# Texte:
# Volk->Volk: TXT_KEY_MESSAGE_NEWTRIBES1-11
# Staat->Volk:  TXT_KEY_MESSAGE_NEWTRIBES12
# Volk->Staat:  TXT_KEY_MESSAGE_NEWTRIBES13
# Staat->Staat: TXT_KEY_MESSAGE_NEWTRIBES14
def doRenameCIVs():
	iGameYear = gc.getGame().getGameTurnYear()
	lPlayers = []

	# +++++++ iGameYear +++++++++++++++++++++++++++++++++++++++++++
	if iGameYear == 300:
		pNewPlayer1 = None
		iScoreBest1 = 0
		pNewPlayer2 = None
		iScoreBest2 = 0
		pNewPlayer3 = None
		iScoreBest3 = 0
		pNewPlayer4 = None
		iScoreBest4 = 0

		iRange = gc.getMAX_PLAYERS()
		for iPlayer in range(iRange):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer is not None and not pPlayer.isNone() and pPlayer.isAlive():
				if pPlayer.isHuman():
					lPlayers.append(iPlayer)
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_BRITEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest1:
						iScoreBest1 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer1 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_PARTHER"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest2:
						iScoreBest2 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer2 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_PHON"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest3:
						iScoreBest3 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer3 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_PERSIA"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest4:
						iScoreBest4 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer4 = pPlayer

		if pNewPlayer1 is not None:
			txtCivOld = pNewPlayer1.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_PICTS_DESC",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_PICTS_ADJECTIVE",())
			pNewPlayer1.setName("Coroticus")
			pNewPlayer1.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer2 is not None:
			txtCivOld = pNewPlayer2.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_ALANEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_ALANEN_ADJ",())
			pNewPlayer2.setName("Goar")
			pNewPlayer2.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer3 is not None:
			txtCivOld = pNewPlayer3.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_GHASSANIDEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_GHASSANIDEN_ADJ",())
			pNewPlayer3.setName("Arethas")
			pNewPlayer3.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer4 is not None:
			txtCivOld = pNewPlayer4.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_SASSANIDEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_SASSANIDEN_ADJ",())
			pNewPlayer4.setName("Sasan")
			pNewPlayer4.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)

		# Hauptmeldefenster
		if len(lPlayers):
			szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_HEAD", ("",))
			szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_BODY", ("",))
			PAE_Popup.PopUpDDS("Art/PAE/MigrationPeriod300.dds",szTextHead,szTextBody,"CENTER")


	# +++++++ iGameYear +++++++++++++++++++++++++++++++++++++++++++
	elif iGameYear == 400:
		pNewPlayer1 = None
		iScoreBest1 = 0
		pNewPlayer2 = None
		iScoreBest2 = 0
		pNewPlayer3 = None
		iScoreBest3 = 0
		pNewPlayer4 = None
		iScoreBest4 = 0
		pNewPlayer5 = None
		iScoreBest5 = 0
		bGermans = False
		bGallier = False

		iRange = gc.getMAX_PLAYERS()
		for iPlayer in range(iRange):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer is not None and not pPlayer.isNone() and pPlayer.isAlive():
				if pPlayer.isHuman():
					lPlayers.append(iPlayer)
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_CELT"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest1:
						iScoreBest1 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer1 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_VANDALS"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest2:
						iScoreBest2 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer2 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_DAKER"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest3:
						iScoreBest3 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer3 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GERMANEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest4:
						iScoreBest4 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer4 = pPlayer
						bGermans = True
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GALLIEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest5:
						iScoreBest5 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer5 = pPlayer
						bGallier = True

		if pNewPlayer1 is not None:
			txtCivOld = pNewPlayer1.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_BAJUWAREN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_BAJUWAREN_ADJ",())
			pNewPlayer1.setName(CyTranslator().getText("TXT_KEY_CIV_BAJUWAREN_LEADER",()))
			pNewPlayer1.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer2 is not None:
			txtCivOld = pNewPlayer2.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_WESTGOTEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_WESTGOTEN_ADJ",())
			pNewPlayer2.setName(CyTranslator().getText("TXT_KEY_CIV_WESTGOTEN_LEADER",()))
			pNewPlayer2.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer3 is not None:
			txtCivOld = pNewPlayer3.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CITY_NAME_B110",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_SARMATEN_ADJ",())
			pNewPlayer3.setName(CyTranslator().getText("TXT_KEY_CIV_SARMATEN_LEADER",()))
			pNewPlayer3.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer4 is not None:
			txtCivOld = pNewPlayer4.getCivilizationDescription(0)
			if bGallier:
				txtCivNew = CyTranslator().getText("TXT_KEY_CIV_ALEMANNEN_SHORT_DESC",())
				txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_ALEMANNEN_ADJECTIVE",())
				pNewPlayer4.setName(CyTranslator().getText("TXT_KEY_GREAT_PERSON_GEN_08",()))
				pNewPlayer4.setCivName(txtCivNew, txtCivNew, txtCivAdj)
				txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
				txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
				for i in lPlayers:
					CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
			else:
				txtCivNew = CyTranslator().getText("TXT_KEY_CIV_FRANKEN",())
				txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_FRANKEN_ADJ",())
				pNewPlayer4.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER1",()))
				pNewPlayer4.setCivName(txtCivNew, txtCivNew, txtCivAdj)
				txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
				txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
				for i in lPlayers:
					CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer5 is not None:
			txtCivOld = pNewPlayer5.getCivilizationDescription(0)
			if bGermans:
				txtCivNew = CyTranslator().getText("TXT_KEY_CIV_MEROWINGER",())
				txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_MEROWINGER_ADJ ",())
				pNewPlayer5.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER1",()))
				pNewPlayer5.setCivName(txtCivNew, txtCivNew, txtCivAdj)
				txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
				txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
				for i in lPlayers:
					CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
			else:
				txtCivNew = CyTranslator().getText("TXT_KEY_CIV_FRANKEN",())
				txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_FRANKEN_ADJ",())
				pNewPlayer5.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER1",()))
				pNewPlayer5.setCivName(txtCivNew, txtCivNew, txtCivAdj)
				txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
				txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
				for i in lPlayers:
					CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)

		# Hauptmeldefenster
		if len(lPlayers):
			szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_HEAD", ("",))
			szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_BODY", ("",))
			PAE_Popup.PopUpDDS("Art/PAE/MigrationPeriod400.dds",szTextHead,szTextBody,"CENTER")


	# +++++++ iGameYear +++++++++++++++++++++++++++++++++++++++++++
	elif iGameYear == 500:
		pNewPlayer1 = None
		iScoreBest1 = 0
		pNewPlayer2 = None
		iScoreBest2 = 0
		pNewPlayer3 = None
		iScoreBest3 = 0
		pNewPlayer4 = None
		iScoreBest4 = 0
		pNewPlayer5 = None
		iScoreBest5 = 0
		bGermans = False
		bGallier = False

		iRange = gc.getMAX_PLAYERS()
		for iPlayer in range(iRange):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer is not None and not pPlayer.isNone() and pPlayer.isAlive():
				if pPlayer.isHuman():
					lPlayers.append(iPlayer)
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_SKYTHEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest1:
						iScoreBest1 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer1 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ETRUSCANS"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest2:
						iScoreBest2 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer2 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ROME"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest3:
						iScoreBest3 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer3 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GERMANEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest4:
						iScoreBest4 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer4 = pPlayer
						bGermans = True
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GALLIEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest5:
						iScoreBest5 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer5 = pPlayer
						bGallier = True

		if pNewPlayer1 is not None:
			txtCivOld = pNewPlayer1.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_BULGAREN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_BULGAREN_ADJ",())
			pNewPlayer1.setName(CyTranslator().getText("TXT_KEY_CIV_BULGAREN_LEADER",()))
			pNewPlayer1.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer2 is not None:
			txtCivOld = pNewPlayer2.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_LANGOBARDEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_LANGOBARDEN_ADJ",())
			pNewPlayer2.setName(CyTranslator().getText("TXT_KEY_CIV_LANGOBARDEN_LEADER",()))
			pNewPlayer2.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer3 is not None:
			txtCivOld = pNewPlayer3.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CITY_NAME_B80",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_OSTGOTEN_ADJECTIVE",())
			pNewPlayer3.setName(CyTranslator().getText("TXT_KEY_LEADER_THEODERICH",()))
			pNewPlayer3.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer4 is not None:
			if not bGallier:
				pNewPlayer4.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER2",()))
		if pNewPlayer5 is not None:
				pNewPlayer5.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER2",()))

		# Hauptmeldefenster
		if len(lPlayers):
			szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_HEAD", ("",))
			szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_BODY", ("",))
			PAE_Popup.PopUpDDS("Art/PAE/MigrationPeriod500.dds",szTextHead,szTextBody,"CENTER")


	# +++++++ iGameYear +++++++++++++++++++++++++++++++++++++++++++
	elif iGameYear == 600:
		pNewPlayer1 = None
		iScoreBest1 = 0
		pNewPlayer2 = None
		iScoreBest2 = 0
		pNewPlayer3 = None
		iScoreBest3 = 0
		pNewPlayer4 = None
		iScoreBest4 = 0
		pNewPlayer5 = None
		iScoreBest5 = 0
		pNewPlayer6 = None
		iScoreBest6 = 0

		iRange = gc.getMAX_PLAYERS()
		for iPlayer in range(iRange):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer is not None and not pPlayer.isNone() and pPlayer.isAlive():
				if pPlayer.isHuman():
					lPlayers.append(iPlayer)
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_BRITEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest1:
						iScoreBest1 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer1 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_HUNNEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest2:
						iScoreBest2 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer2 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_CARTHAGE"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest3:
						iScoreBest3 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer3 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ILLYRIA"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest4:
						iScoreBest4 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer4 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_LYDIA"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest5:
						iScoreBest5 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer5 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_SUMERIA"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest6:
						iScoreBest6 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer6 = pPlayer

		if pNewPlayer1 is not None:
			txtCivOld = pNewPlayer1.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_ANGELSACHSEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_ANGELSACHSEN_ADJ",())
			pNewPlayer1.setName(CyTranslator().getText("TXT_KEY_CIV_ANGELSACHSEN_LEADER",()))
			pNewPlayer1.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer2 is not None:
			txtCivOld = pNewPlayer2.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CITY_NAME_B86",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_AWAREN_ADJ",())
			pNewPlayer2.setName("Bajan Khagan")
			pNewPlayer2.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer3 is not None:
			txtCivOld = pNewPlayer3.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_UMAYYADEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_UMAYYADEN_ADJ",())
			pNewPlayer3.setName("Muawiya I")
			pNewPlayer3.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer4 is not None:
			txtCivOld = pNewPlayer4.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_SLAWEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_SLAWEN_ADJ",())
			pNewPlayer4.setName(CyTranslator().getText("TXT_KEY_CIV_SLAWEN_LEADER",()))
			pNewPlayer4.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer5 is not None:
			txtCivOld = pNewPlayer5.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_TURKMENEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_TURKMENEN_ADJ",())
			pNewPlayer5.setName("Arkadag")
			pNewPlayer5.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer6 is not None:
			txtCivOld = pNewPlayer6.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_LACHMIDEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_LACHMIDEN_ADJ",())
			pNewPlayer6.setName("al-Mundhir III")
			pNewPlayer6.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)

		# Hauptmeldefenster
		if len(lPlayers):
			szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_HEAD", ("",))
			szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_BODY", ("",))
			PAE_Popup.PopUpDDS("Art/PAE/MigrationPeriod600.dds",szTextHead,szTextBody,"CENTER")


	# +++++++ iGameYear +++++++++++++++++++++++++++++++++++++++++++
	elif iGameYear == 700:
		pNewPlayer1 = None
		iScoreBest1 = 0
		pNewPlayer2 = None
		iScoreBest2 = 0
		pNewPlayer3 = None
		iScoreBest3 = 0
		pNewPlayer4 = None
		iScoreBest4 = 0
		pNewPlayer5 = None
		iScoreBest5 = 0
		pNewPlayer6 = None
		iScoreBest6 = 0
		bGermans = False

		iRange = gc.getMAX_PLAYERS()
		for iPlayer in range(iRange):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer is not None and not pPlayer.isNone() and pPlayer.isAlive():
				if pPlayer.isHuman():
					lPlayers.append(iPlayer)
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_PERSIA"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest1:
						iScoreBest1 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer1 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_BERBER"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest2:
						iScoreBest2 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer2 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_IBERER"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest3:
						iScoreBest3 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer3 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GERMANEN"):
						bGermans = True
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GALLIEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest4:
						iScoreBest4 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer4 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ASSYRIA"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest5:
						iScoreBest5 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer5 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_BABYLON"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest6:
						iScoreBest6 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer6 = pPlayer

		if pNewPlayer1 is not None:
			txtCivOld = pNewPlayer1.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_ABBASIDEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_ABBASIDEN_ADJ",())
			pNewPlayer1.setName("Abu l-Abbas as-Saffah")
			pNewPlayer1.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer2 is not None:
			txtCivOld = pNewPlayer2.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CITY_NAME_B90",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_MAUREN_ADJ",())
			pNewPlayer2.setName("Tariq ibn Ziyad")
			pNewPlayer2.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer3 is not None:
			txtCivOld = pNewPlayer3.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_SCEN_CIV_ASTURIEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_SCEN_CIV_ASTURIEN_ADJ",())
			pNewPlayer3.setName("Pelayo")
			pNewPlayer3.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer4 is not None:
			txtCivOld = pNewPlayer4.getCivilizationDescription(0)
			if bGermans:
				txtCivNew = CyTranslator().getText("TXT_KEY_CIV_KAROLINGER",())
				txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_KAROLINGER_ADJ",())
				pNewPlayer4.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER3",()))
				pNewPlayer4.setCivName(txtCivNew, txtCivNew, txtCivAdj)
				txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
				txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
				for i in lPlayers:
					CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer5 is not None:
			txtCivOld = pNewPlayer5.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_KURDEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_KURDEN_ADJ",())
			pNewPlayer5.setName("Babak Khorramdin")
			pNewPlayer5.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer6 is not None:
			txtCivOld = pNewPlayer6.getCivilizationDescription(0)
			if pNewPlayer6.getStateReligion() == gc.getInfoTypeForString("RELIGION_ISLAM"):
				txtCivNew = CyTranslator().getText("TXT_KEY_CIV_KALIFAT",()) + u" " + pNewPlayer6.getCapitalCity().getName()
				pNewPlayer6.setCivName(txtCivNew, txtCivNew, "")

		# Hauptmeldefenster
		if len(lPlayers):
			szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_HEAD", ("",))
			szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_BODY", ("",))
			PAE_Popup.PopUpDDS("Art/PAE/MigrationPeriod700.dds",szTextHead,szTextBody,"CENTER")


	# +++++++ iGameYear +++++++++++++++++++++++++++++++++++++++++++
	elif iGameYear == 800:
		pNewPlayer1 = None
		iScoreBest1 = 0
		pNewPlayer2 = None
		iScoreBest2 = 0
		pNewPlayer3 = None
		iScoreBest3 = 0
		pNewPlayer4 = None
		iScoreBest4 = 0
		pNewPlayer5 = None
		iScoreBest5 = 0
		bGermans = False
		bGallier = False

		iRange = gc.getMAX_PLAYERS()
		for iPlayer in range(iRange):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer is not None and not pPlayer.isNone() and pPlayer.isAlive():
				if pPlayer.isHuman():
					lPlayers.append(iPlayer)
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ROME"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest1:
						iScoreBest1 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer1 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_HUNNEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest2:
						iScoreBest2 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer2 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_HETHIT"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest3:
						iScoreBest3 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer3 = pPlayer
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GERMANEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest4:
						iScoreBest4 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer4 = pPlayer
						bGermans = True
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_GALLIEN"):
					if CyGame().getPlayerScore(iPlayer) > iScoreBest5:
						iScoreBest5 = CyGame().getPlayerScore(iPlayer)
						pNewPlayer5 = pPlayer
						bGallier = True

		if pNewPlayer1 is not None:
			txtCivOld = pNewPlayer1.getCivilizationDescription(0)
			if pNewPlayer1.getStateReligion() == gc.getInfoTypeForString("RELIGION_CHRISTIANITY"):
				txtCivNew = CyTranslator().getText("TXT_KEY_CIV_HOLY_ROMAN_DESC",())
				txtCivAdj  = gc.getPlayer(gc.getInfoTypeForString("CIVILIZATION_ROME")).getCivilizationAdjective(0)
				pNewPlayer1.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER6",()))
				pNewPlayer1.setCivName(txtCivNew, txtCivNew, txtCivAdj)
				txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
				txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
				for i in lPlayers:
					CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer2 is not None:
			txtCivOld = pNewPlayer2.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_MAGYAREN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_MAGYAREN_ADJ",())
			pNewPlayer2.setName("Arpad")
			pNewPlayer2.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer3 is not None:
			txtCivOld = pNewPlayer3.getCivilizationDescription(0)
			txtCivNew = CyTranslator().getText("TXT_KEY_CIV_SELDSCHUKEN",())
			txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_SELDSCHUKEN_ADJ",())
			pNewPlayer3.setName(CyTranslator().getText("TXT_KEY_CIV_SELDSCHUKEN_LEADER",()))
			pNewPlayer3.setCivName(txtCivNew, txtCivNew, txtCivAdj)
			txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
			txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
			for i in lPlayers:
				CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
		if pNewPlayer4 is not None:
			txtCivOld = pNewPlayer4.getCivilizationDescription(0)
			if bGallier:
				txtCivNew = CyTranslator().getText("TXT_KEY_CIV_FRANKEN_OST",())
				txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_FRANKEN_OST_ADJ",())
				pNewPlayer4.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER5",()))
				pNewPlayer4.setCivName(txtCivNew, txtCivNew, txtCivAdj)
				txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
				txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
				for i in lPlayers:
					CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
			else:
				pNewPlayer4.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER3",()))
		if pNewPlayer5 is not None:
			txtCivOld = pNewPlayer5.getCivilizationDescription(0)
			if bGermans:
				txtCivNew = CyTranslator().getText("TXT_KEY_CIV_FRANKEN_WEST",())
				txtCivAdj  = CyTranslator().getText("TXT_KEY_CIV_FRANKEN_WEST_ADJ",())
				pNewPlayer5.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER4",()))
				pNewPlayer5.setCivName(txtCivNew, txtCivNew, txtCivAdj)
				txt = "TXT_KEY_MESSAGE_NEWTRIBES" + str(CvUtil.myRandom(11, "MigrationPeriodText") + 1)
				txt = CyTranslator().getText("TXT_KEY_CONCEPT_NEWTRIBES", ()) + u" : " + CyTranslator().getText(txt, (txtCivOld,txtCivNew))
				for i in lPlayers:
					CyInterface().addMessage(i, True, 10, txt, None, 2, None, ColorTypes(2), 0, 0, False, False)
			else:
				pNewPlayer5.setName(CyTranslator().getText("TXT_KEY_CIV_FRANKEN_LEADER3",()))

		# Hauptmeldefenster
		if len(lPlayers):
			szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_HEAD", ("",))
			szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_NEWTRIBES_BODY", ("",))
			PAE_Popup.PopUpDDS("Art/PAE/MigrationPeriod800.dds",szTextHead,szTextBody,"CENTER")



