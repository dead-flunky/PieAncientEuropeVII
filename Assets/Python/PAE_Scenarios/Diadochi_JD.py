# Scenario JohnDay

# Imports
from CvPythonExtensions import CyGlobalContext
# import CvUtil

# Defines
gc = CyGlobalContext()


def onGameStart():
		# Fuer John: Immer Krieg zwischen bestimmten Civs
		lCivsAlwaysWar = [11, 18, 19, 20, 25, 26, 27, 28, 29, 40, 41, 47]
		for iPlayer1 in lCivsAlwaysWar:
				for iPlayer2 in lCivsAlwaysWar:
						iTeam1 = gc.getPlayer(iPlayer1).getTeam()
						iTeam2 = gc.getPlayer(iPlayer2).getTeam()
						pTeam1 = gc.getTeam(iTeam1)
						# pTeam2 = gc.getTeam(iTeam2)
						if iTeam1 != iTeam2:
								if not pTeam1.isAtWar(iTeam2):
										pTeam1.declareWar(iTeam2, False, 4)
								pTeam1.setPermanentWarPeace(iTeam2, True)
		# --------------


def onBeginPlayerTurn(iGameTurn, iPlayer):
		pass


def onCityAcquired(iPreviousOwner, iNewOwner, pCity, bConquest, bTrade):
		pass


def onEndGameTurn(iGameTurn):
		pass
