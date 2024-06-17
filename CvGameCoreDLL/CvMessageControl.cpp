#include "CvGameCoreDLL.h"
#include "CvMessageControl.h"
#include "CvMessageData.h"
#include "CvDLLUtilityIFaceBase.h"

CvMessageControl& CvMessageControl::getInstance()
{
	static CvMessageControl m_sInstance;
	return m_sInstance;
}

void CvMessageControl::sendExtendedGame()
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetExtendedGame(GC.getGameINLINE().getActivePlayerInternal()));
	}
}

void CvMessageControl::sendAutoMoves()
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetAutoMoves(GC.getGameINLINE().getActivePlayerInternal()));
	}
}

void CvMessageControl::sendTurnComplete()
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetTurnComplete(GC.getGameINLINE().getActivePlayerInternal()));
	}
}

// PBMod
void CvMessageControl::sendTurnCompleteAll()
{
	//Finish turn for all players
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive()){
			gDLL->sendMessageData(new CvNetTurnComplete((PlayerTypes)iI));
		}
	}
}

void CvMessageControl::sendTurnCompletePB(PlayerTypes ePlayer)
{
	if( GC.getGameINLINE().isPitboss() )
	{
		if (GET_PLAYER(ePlayer).isAlive())
		{
			gDLL->sendMessageData(new CvNetTurnComplete(ePlayer));
		}
	}
}

void CvMessageControl::sendTurnIncompletePB(PlayerTypes ePlayer)
{
	if( GC.getGameINLINE().isPitboss() )
	{
		if (GET_PLAYER(ePlayer).isAlive())
		{
			gDLL->sendMessageData(new CvNetTurnIncomplete(ePlayer));
		}
	}
}
// PBMod end

void CvMessageControl::sendPushOrder(int iCityID, OrderTypes eOrder, int iData, bool bAlt, bool bShift, bool bCtrl)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetPushOrder(GC.getGameINLINE().getActivePlayerInternal(), iCityID, eOrder, iData, bAlt, bShift, bCtrl));
	}
}

void CvMessageControl::sendPopOrder(int iCity, int iNum)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetPopOrder(GC.getGameINLINE().getActivePlayerInternal(), iCity, iNum));
	}
}

void CvMessageControl::sendDoTask(int iCity, TaskTypes eTask, int iData1, int iData2, bool bOption, bool bAlt, bool bShift, bool bCtrl)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetDoTask(GC.getGameINLINE().getActivePlayerInternal(), iCity, eTask, iData1, iData2, bOption, bAlt, bShift, bCtrl));
	}
}

void CvMessageControl::sendUpdateCivics(const std::vector<CivicTypes>& aeCivics)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetUpdateCivics(GC.getGameINLINE().getActivePlayerInternal(), aeCivics));
	}
}

void CvMessageControl::sendResearch(TechTypes eTech, int iDiscover, bool bShift)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetResearch(GC.getGameINLINE().getActivePlayerInternal(), eTech, iDiscover, bShift));
	}
}

void CvMessageControl::sendEspionageSpendingWeightChange(TeamTypes eTargetTeam, int iChange)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetEspionageChange(GC.getGameINLINE().getActivePlayerInternal(), eTargetTeam, iChange));
	}
}

void CvMessageControl::sendAdvancedStartAction(AdvancedStartActionTypes eAction, PlayerTypes ePlayer, int iX, int iY, int iData, bool bAdd)
{
	gDLL->sendMessageData(new CvNetAdvancedStartAction(eAction, ePlayer, iX, iY, iData, bAdd));
}

void CvMessageControl::sendModNetMessage(int iData1, int iData2, int iData3, int iData4, int iData5)
{
	gDLL->sendMessageData(new CvNetModNetMessage(iData1, iData2, iData3, iData4, iData5));
}

void CvMessageControl::sendConvert(ReligionTypes eReligion)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetConvert(GC.getGameINLINE().getActivePlayerInternal(), eReligion));
	}
}

void CvMessageControl::sendEmpireSplit(PlayerTypes ePlayer, int iAreaId)
{
	gDLL->sendMessageData(new CvNetEmpireSplit(ePlayer, iAreaId));
}

void CvMessageControl::sendFoundReligion(PlayerTypes ePlayer, ReligionTypes eReligion, ReligionTypes eSlotReligion)
{
	gDLL->sendMessageData(new CvNetFoundReligion(ePlayer, eReligion, eSlotReligion));
}

void CvMessageControl::sendLaunch(PlayerTypes ePlayer, VictoryTypes eVictory)
{
	gDLL->sendMessageData(new CvNetLaunchSpaceship(ePlayer, eVictory));
}

void CvMessageControl::sendEventTriggered(PlayerTypes ePlayer, EventTypes eEvent, int iEventTriggeredId)
{
	gDLL->sendMessageData(new CvNetEventTriggered(ePlayer, eEvent, iEventTriggeredId));
}

void CvMessageControl::sendJoinGroup(int iUnitID, int iHeadID)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetJoinGroup(GC.getGameINLINE().getActivePlayerInternal(), iUnitID, iHeadID));
	}
}

void CvMessageControl::sendPushMission(int iUnitID, MissionTypes eMission, int iData1, int iData2, int iFlags, bool bShift)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetPushMission(GC.getGameINLINE().getActivePlayerInternal(), iUnitID, eMission, iData1, iData2, iFlags, bShift));
	}
}

void CvMessageControl::sendAutoMission(int iUnitID)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetAutoMission(GC.getGameINLINE().getActivePlayerInternal(), iUnitID));
	}
}

void CvMessageControl::sendDoCommand(int iUnitID, CommandTypes eCommand, int iData1, int iData2, bool bAlt)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetDoCommand(GC.getGameINLINE().getActivePlayerInternal(), iUnitID, eCommand, iData1, iData2, bAlt));
	}
}

void CvMessageControl::sendPercentChange(CommerceTypes eCommerce, int iChange)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetPercentChange(GC.getGameINLINE().getActivePlayerInternal(), eCommerce, iChange));
	}
}

void CvMessageControl::sendChangeVassal(TeamTypes eMasterTeam, bool bVassal, bool bCapitulated)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetChangeVassal(GC.getGameINLINE().getActivePlayerInternal(), eMasterTeam, bVassal, bCapitulated));
	}
}

void CvMessageControl::sendChooseElection(int iSelection, int iVoteId)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetChooseElection(GC.getGameINLINE().getActivePlayerInternal(), iSelection, iVoteId));
	}
}

void CvMessageControl::sendDiploVote(int iVoteId, PlayerVoteTypes eChoice)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetDiploVote(GC.getGameINLINE().getActivePlayerInternal(), iVoteId, eChoice));
	}
}

void CvMessageControl::sendChangeWar(TeamTypes eRivalTeam, bool bWar)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetChangeWar(GC.getGameINLINE().getActivePlayerInternal(), eRivalTeam, bWar));
	}
}

void CvMessageControl::sendPing(int iX, int iY)
{
	if (NO_PLAYER != GC.getGameINLINE().getActivePlayerInternal())
	{
		gDLL->sendMessageData(new CvNetPing(GC.getGameINLINE().getActivePlayerInternal(), iX, iY));
	}
}


