import json
import pprint
from datetime import datetime, timedelta
from .ddragon.factory import ddragon_factory
from munch import DefaultMunch
from .ddragon.maps import maps, Position
import math
from collections.abc import Iterable

"""
Instantiates Match class from match data
"""


class Match:
    def __init__(self, data, timeline=None, patch=None):
        if timeline is not None and 'gameMode' and 'gameType' in timeline["info"]:
            timeline = None
        self._data = data


        self.dataVersion = data["metadata"]["dataVersion"]
        try:
            self.gameVersion = data["info"]["gameVersion"]
            self.patch = ".".join(data["info"]["gameVersion"].split(".")[0:2])

            patch = self.patch

            for ver in ddragon_factory.versions():
                if ver.startswith(patch):
                    self.version = ver
        except:
            for ver in ddragon_factory.versions():
                #print(patch)
                if ver.startswith(patch):
                    self.gameVersion = ver
                    self.version = ver
                    self.patch = patch

        self.matchId = data["metadata"]["matchId"]
        self.participantsPuuids = data["metadata"]["participants"]

        self.gameCreation = datetime.fromtimestamp(data["info"]["gameCreation"] / 1000)
        self.gameDuration = timedelta(seconds=data["info"]["gameDuration"])
        if self.gameDuration > timedelta(hours=2):
            self.gameDuration = timedelta(milliseconds=data["info"]["gameDuration"])
        try:
            self.gameEndTimestamp = datetime.fromtimestamp(data["info"]["gameEndTimestamp"] / 1000)
        except KeyError:
            self.gameEndTimestamp = self.gameCreation + self.gameDuration + timedelta(seconds=300)
        try:
            self.gameId = data["info"]["gameId"]
        except KeyError:
            self.gameId = self.matchId

        self.gameMode = data["info"]["gameMode"]
        try:
            self.gameName = data["info"]["gameName"]
        except KeyError:
            self.gameName = ""
        try:
            self.gameEndTimestamp = datetime.fromtimestamp(data["info"]["gameEndTimestamp"] / 1000)
        except KeyError:
            self.gameStartTimestamp = self.gameCreation
        self.gameType = data["info"]["gameType"]
        self.platformId = data["info"]["platformId"]
        self.mapId = data["info"]["mapId"]
        if self.mapId == 0:
            self.mapId = 11
        self.queueId = data["info"]["queueId"]
        try:
            self.tournamentCode = data["info"]["tournamentCode"]
        except KeyError:
            self.tournamentCode = None


        try:
            self._participants = [Participant(data, self) for data in data["info"]["participants"]]
            self._teams = [Team(data, self) for data in data["info"]["teams"]]
            self.map = maps[self.mapId]

            if timeline is not None:
                # print("Included timeline")
                self.include_timeline(timeline)
            else:
                self.timeline = None

        except KeyError as e:
            #print(e)
            if str(e).replace("'","").isnumeric():
                #print("Wrong game version")
                supposed_version_index = ddragon_factory.versions().index(self.version)
                first_test = supposed_version_index + 2
                self.version = ddragon_factory.versions()[first_test]
                found = False
                while not found:
                    supposed_version_index = ddragon_factory.versions().index(self.version)
                    next_try = supposed_version_index - 1
                    ver = ddragon_factory.versions()[next_try]
                    #print("New version tried : ", ver)
                    self.gameVersion = ver
                    self.version = ver
                    self.patch = ".".join(self.gameVersion.split(".")[0:2])
                    try:
                        #pprint.pp(data["info"]["participants"][0])
                        self._participants = [Participant(data, self) for data in data["info"]["participants"]]
                        self._teams = [Team(data, self) for data in data["info"]["teams"]]

                        self.map = maps[self.mapId]

                        if timeline is not None:
                            self.include_timeline(timeline)
                        else:
                            self.timeline = None
                        found = True

                    except Exception as e:

                        if str(e).replace("'","").isnumeric():
                            pass
                            #print(self.gameId, self.version)
                            #print(repr(e))
                        else:
                            raise e
                        pass
                #print(self.version)
            else:
                raise e
        """
        print(self._participants[0].runes)
        if len(self._participants[0].runes) == 0:
            pprint.pp(data["info"]["participants"][0])
            print(data)
            print("No runes here",self.gameId)
        """

    def participants(self, fieldSearch=None, fieldValue=None):
        if fieldSearch == "participantId" and fieldValue == 0:
            return None
        if fieldSearch == "participantId" and fieldValue is not None:
            return self._participants[fieldValue - 1]

        if (fieldSearch is None) ^ (fieldValue is None):
            raise ValueError(
                "fieldSearch and fieldValue should both be None or valued, fieldSearch is {} and fieldValue is {}.".format(
                    fieldSearch, fieldValue
                )
            )
        if fieldSearch is not None:
            toRet = filter(lambda par: getattr(par, fieldSearch) == fieldValue, self._participants)
        else:
            toRet = self._participants
        return list(toRet)

    def teams(self, teamId=None):
        if teamId is None:
            try:
                return self._teams
            except AttributeError as e:
                pprint.pp(self._data)
                print(repr(e))
                raise e
        elif self._teams[0].teamId == teamId:
            return self._teams[0]
        elif self._teams[1].teamId == teamId:
            return self._teams[1]
        else:
            raise ValueError("{} is not a valid teamId".format(teamId))

    def include_timeline(self, timeline):
        self.timeline = Timeline(timeline, self)
        for participant in self._participants:
            participant.include_timeline(self.timeline)


class Participant:
    def __init__(self, data, match):
        try:
            self.assists = data["assists"]
            self.baronKills = data["baronKills"]
            self.bountyLevel = data["bountyLevel"]
            self.champExperience = data["champExperience"]
            self.champLevel = data["champLevel"]
            self.championId = data["championId"]

            self.champion = ddragon_factory.championFromId(data["championId"], match.version)

            self.championName = data["championName"]
            self.championTransform = data["championTransform"]
            self.consumablesPurchased = data["consumablesPurchased"]
            self.damageDealtToBuildings = data["damageDealtToBuildings"]
            self.damageDealtToObjectives = data["damageDealtToObjectives"]
            self.damageDealtToTurrets = data["damageDealtToTurrets"]
            self.damageSelfMitigated = data["damageSelfMitigated"]
            self.deaths = data["deaths"]
            self.detectorWardsPlaced = data["detectorWardsPlaced"]
            self.doubleKills = data["doubleKills"]
            self.firstBloodAssist = data["firstBloodAssist"]
            self.firstBloodKill = data["firstBloodKill"]
            self.firstTowerAssist = data["firstTowerAssist"]
            self.firstTowerKill = data["firstTowerKill"]
            self.gameEndedInEarlySurrender = data["gameEndedInEarlySurrender"]
            self.gameEndedInSurrender = data["gameEndedInSurrender"]
            self.goldEarned = data["goldEarned"]
            self.goldSpent = data["goldSpent"]
            self.individualPosition = data["individualPosition"]
            self.inhibitorKills = data["inhibitorKills"]
            self.inhibitorTakedowns = data["inhibitorTakedowns"]
            self.inhibitorsLost = data["inhibitorsLost"]

            self.item0 = ddragon_factory.itemFromId(data["item0"], match.version)
            self.item1 = ddragon_factory.itemFromId(data["item1"], match.version)
            self.item2 = ddragon_factory.itemFromId(data["item2"], match.version)
            self.item3 = ddragon_factory.itemFromId(data["item3"], match.version)
            self.item4 = ddragon_factory.itemFromId(data["item4"], match.version)
            self.item5 = ddragon_factory.itemFromId(data["item5"], match.version)
            self.item6 = ddragon_factory.itemFromId(data["item6"], match.version)

            self.itemsPurchased = data["itemsPurchased"]
            self.killingSprees = data["killingSprees"]
            self.kills = data["kills"]
            self.lane = data["lane"]
            self.largestCriticalStrike = data["largestCriticalStrike"]
            self.largestKillingSpree = data["largestKillingSpree"]
            self.largestMultiKill = data["largestMultiKill"]
            self.longestTimeSpentLiving = data["longestTimeSpentLiving"]
            self.magicDamageDealt = data["magicDamageDealt"]
            self.magicDamageDealtToChampions = data["magicDamageDealtToChampions"]
            self.magicDamageTaken = data["magicDamageTaken"]
            self.neutralMinionsKilled = data["neutralMinionsKilled"]
            self.nexusKills = data["nexusKills"]
            self.nexusTakedowns = data["nexusTakedowns"]
            self.nexusLost = data["nexusLost"]
            self.objectivesStolen = data["objectivesStolen"]
            self.objectivesStolenAssists = data["objectivesStolenAssists"]
            self.participantId = data["participantId"]
            self.pentaKills = data["pentaKills"]

            self.perks = data["perks"]
            self.statRunes = [ddragon_factory.runeFromId(data["perks"]["statPerks"][rid], match.version) for rid in
                              data["perks"]["statPerks"]]
            self.runes = [ddragon_factory.runeFromId(selection["perk"], match.version) for style in
                          data["perks"]["styles"] for selection in style["selections"]]
            self.mainTree = ddragon_factory.runeFromId(data["perks"]["styles"][0]["style"], match.version)
            try:
                self.secondaryTree = ddragon_factory.runeFromId(data["perks"]["styles"][1]["style"], match.version)
            except KeyError as e:
                if data["perks"]["styles"][1]["style"]==0:
                    self.secondaryTree = ddragon_factory.runeFromId((data["perks"]["styles"][1]["selections"][0]["perk"] // 100) * 100, match.version)
                else:
                    print(data["perks"]["styles"][1])
                    raise e


            self.physicalDamageDealt = data["physicalDamageDealt"]
            self.physicalDamageDealtToChampions = data["physicalDamageDealtToChampions"]
            self.physicalDamageTaken = data["physicalDamageTaken"]
            self.profileIcon = data["profileIcon"]
            self.puuid = data["puuid"]
            self.quadraKills = data["quadraKills"]
            self.riotIdName = data["riotIdName"]
            self.role = data["role"]
            self.sightWardsBoughtInGame = data["sightWardsBoughtInGame"]
            self.spell1Casts = data["spell1Casts"]
            self.spell2Casts = data["spell2Casts"]
            self.spell3Casts = data["spell3Casts"]
            self.spell4Casts = data["spell4Casts"]
            self.summoner1Casts = data["summoner1Casts"]
            self.summoner1Id = data["summoner1Id"]
            self.summoner2Casts = data["summoner2Casts"]
            self.summoner2Id = data["summoner2Id"]
            self.summonerId = data["summonerId"]
            self.summonerLevel = data["summonerLevel"]
            self.summonerName = data["summonerName"]
            self.teamEarlySurrendered = data["teamEarlySurrendered"]
            self.teamId = data["teamId"]
            self.teamPosition = self.teamPosition = \
                    [None, "TOP_LANE", "JUNGLE", "MID_LANE", "BOT_LANE", "UTILITY", "TOP_LANE", "JUNGLE", "MID_LANE",
                     "BOT_LANE", "UTILITY"][self.participantId]
            self.timeCCingOthers = data["timeCCingOthers"]
            self.timePlayed = data["timePlayed"]
            self.totalDamageDealt = data["totalDamageDealt"]
            self.totalDamageDealtToChampions = data["totalDamageDealtToChampions"]
            self.totalDamageShieldedOnTeammates = data["totalDamageShieldedOnTeammates"]
            self.totalDamageTaken = data["totalDamageTaken"]
            self.totalHeal = data["totalHeal"]
            self.totalHealsOnTeammates = data["totalHealsOnTeammates"]
            self.totalMinionsKilled = data["totalMinionsKilled"] + data["neutralMinionsKilled"]
            # if self.teamPosition == "JUNGLE":
            #     print("V5")
            #     print(self.totalMinionsKilled, data["totalMinionsKilled"], data["neutralMinionsKilled"])
            #     print(self.totalMinionsKilled / (match.gameDuration.seconds / 60))
            #     pprint.pp(data)
            self.totalTimeCCDealt = data["totalTimeCCDealt"]
            self.totalTimeSpentDead = data["totalTimeSpentDead"]
            self.totalUnitsHealed = data["totalUnitsHealed"]
            self.tripleKills = data["tripleKills"]
            self.trueDamageDealt = data["trueDamageDealt"]
            self.trueDamageDealtToChampions = data["trueDamageDealtToChampions"]
            self.trueDamageTaken = data["trueDamageTaken"]
            self.turretKills = data["turretKills"]
            self.turretTakedowns = data["turretTakedowns"]
            self.turretsLost = data["turretsLost"]
            self.unrealKills = data["unrealKills"]
            self.visionScore = data["visionScore"]
            self.visionWardsBoughtInGame = data["visionWardsBoughtInGame"]
            self.wardsKilled = data["wardsKilled"]
            self.wardsPlaced = data["wardsPlaced"]
            self.win = data["win"]
            self.isv4 = False
        except KeyError:
            try:
                self.isv4 = True
                datav4 = data["stats"]
                self.participantId = datav4["participantId"]
                self.assists = datav4["assists"]
                self.baronKills = None
                self.bountyLevel = None
                self.champExperience = None
                self.champLevel = datav4["champLevel"]
                self.championId = data["championId"]
                try:
                    self.champion = ddragon_factory.championFromId(data["championId"], match.version)
                except AttributeError:
                    raise AttributeError(match.gameVersion, match.patch, ddragon_factory.versions())
                self.championName = self.champion.id
                self.championTransform = {}
                self.consumablesPurchased = None
                self.damageDealtToBuildings = None
                self.damageDealtToObjectives = datav4["damageDealtToObjectives"]
                self.damageDealtToTurrets = datav4["damageDealtToTurrets"]
                self.damageSelfMitigated = datav4["damageSelfMitigated"]
                self.deaths = datav4["deaths"]
                self.detectorWardsPlaced = None
                self.doubleKills = datav4["doubleKills"]
                try:
                    self.firstBloodAssist = datav4["firstBloodAssist"]
                    self.firstBloodKill = datav4["firstBloodKill"]
                    self.firstTowerAssist = datav4["firstTowerAssist"]
                    self.firstTowerKill = datav4["firstTowerKill"]
                except KeyError:
                    self.firstBloodAssist = False
                    self.firstBloodKill = False
                    self.firstTowerAssist = False
                    self.firstTowerKill = False
                self.gameEndedInEarlySurrender = False
                self.gameEndedInSurrender = False
                self.goldEarned = datav4["goldEarned"]
                self.goldSpent = datav4["goldSpent"]
                self.individualPosition = \
                    [None, "TOP_LANE", "JUNGLE", "MID_LANE", "BOT_LANE", "UTILITY", "TOP_LANE", "JUNGLE", "MID_LANE",
                     "BOT_LANE", "UTILITY"][self.participantId]
                self.inhibitorKills = datav4["inhibitorKills"]
                self.inhibitorTakedowns = datav4["inhibitorKills"]
                self.inhibitorsLost = None

                self.item0 = ddragon_factory.itemFromId(datav4["item0"], match.version)
                self.item1 = ddragon_factory.itemFromId(datav4["item1"], match.version)
                self.item2 = ddragon_factory.itemFromId(datav4["item2"], match.version)
                self.item3 = ddragon_factory.itemFromId(datav4["item3"], match.version)
                self.item4 = ddragon_factory.itemFromId(datav4["item4"], match.version)
                self.item5 = ddragon_factory.itemFromId(datav4["item5"], match.version)
                self.item6 = ddragon_factory.itemFromId(datav4["item6"], match.version)

                self.itemsPurchased = None
                self.killingSprees = datav4["killingSprees"]
                self.kills = datav4["kills"]
                self.lane = data["timeline"]["lane"]
                self.largestCriticalStrike = datav4["largestCriticalStrike"]
                self.largestKillingSpree = datav4["largestKillingSpree"]
                self.largestMultiKill = datav4["largestMultiKill"]
                self.longestTimeSpentLiving = datav4["longestTimeSpentLiving"]
                self.magicDamageDealt = datav4["magicDamageDealt"]
                self.magicDamageDealtToChampions = datav4["magicDamageDealtToChampions"]
                self.magicDamageTaken = datav4["magicalDamageTaken"]
                self.neutralMinionsKilled = datav4["neutralMinionsKilled"]
                self.nexusKills = None
                self.nexusTakedowns = None
                self.nexusLost = int(not datav4["win"])
                self.objectivesStolen = None
                self.objectivesStolenAssists = None
                self.pentaKills = datav4["pentaKills"]

                self.perks = []
                try:
                    self.statRunes = [ddragon_factory.runeFromId(datav4["statPerk" + str(rid)], match.version) for rid in
                                      range(3)]
                except KeyError as e:
                    self.statRunes = []
                try:
                    self.runes = [ddragon_factory.runeFromId(datav4["perk" + str(rid)], match.version) for rid in range(6)]
                except Exception as e:
                    try:
                        self.runes = [ddragon_factory.runeFromId(rune["masteryId"], match.version) for rune in data["masteries"]]
                    except KeyError as e:
                        if str(e).replace("'","").isnumeric():
                            raise e
                        self.runes = []

                try:
                    self.mainTree = ddragon_factory.runeFromId(datav4["perkPrimaryStyle"], match.version)
                    self.secondaryTree = ddragon_factory.runeFromId(datav4["perkSubStyle"], match.version)
                except:
                    self.mainTree = DefaultMunch({"name":""})
                    self.secondaryTree = DefaultMunch({"name":""})

                self.physicalDamageDealt = datav4["physicalDamageDealt"]
                self.physicalDamageDealtToChampions = datav4["physicalDamageDealtToChampions"]
                self.physicalDamageTaken = datav4["physicalDamageTaken"]
                try:
                    self.profileIcon = match._data["info"]["participantIdentities"][self.participantId - 1]["player"][
                        "profileIcon"]
                except KeyError as e:
                    if e == "player":
                        print(match._data["info"]["participantIdentities"][self.participantId - 1])
                        self.profileIcon = None

                self.puuid = data["puuid"]
                self.quadraKills = datav4["quadraKills"]
                self.riotIdName = ''
                self.role = data["timeline"]["role"]
                self.sightWardsBoughtInGame = datav4["sightWardsBoughtInGame"]
                self.spell1Casts = None
                self.spell2Casts = None
                self.spell3Casts = None
                self.spell4Casts = None
                self.summoner1Casts = None
                self.summoner1Id = data["summoner1Id"]
                self.summoner2Casts = None
                self.summoner2Id = data["summoner2Id"]
                self.summonerId = None
                self.summonerLevel = None

                try:
                    self.summonerName = match._data["info"]["participantIdentities"][self.participantId - 1]["player"][
                        "summonerName"]
                except KeyError as e:
                    #pprint.pp(match._data["info"]["participantIdentities"][self.participantId - 1])
                    #print(e)
                    if str(e) == "player":
                        print(match._data["info"]["participantIdentities"][self.participantId - 1])
                        self.summonerName = None

                self.teamEarlySurrendered = None
                self.teamId = data["teamId"]
                self.teamPosition = \
                    [None, "TOP_LANE", "JUNGLE", "MID_LANE", "BOT_LANE", "UTILITY", "TOP_LANE", "JUNGLE", "MID_LANE",
                     "BOT_LANE", "UTILITY"][self.participantId]
                self.timeCCingOthers = datav4["timeCCingOthers"]
                self.timePlayed = match.gameDuration
                self.totalDamageDealt = datav4["totalDamageDealt"]
                self.totalDamageDealtToChampions = datav4["totalDamageDealtToChampions"]
                self.totalDamageShieldedOnTeammates = None
                self.totalDamageTaken = datav4["totalDamageTaken"]
                self.totalHeal = datav4["totalHeal"]
                if datav4['totalUnitsHealed'] == 1:
                    self.totalHealsOnTeammates = 0
                else:
                    self.totalHealsOnTeammates = datav4['totalHeal']
                self.totalMinionsKilled = datav4["totalMinionsKilled"] + datav4["neutralMinionsKilled"]
                # if self.teamPosition == "JUNGLE":
                #     print(self.totalMinionsKilled, datav4["totalMinionsKilled"], datav4["neutralMinionsKilled"])
                #     print(self.totalMinionsKilled / (match.gameDuration.seconds / 60))
                #     print(datav4)
                self.totalTimeCCDealt = datav4["timeCCingOthers"]
                self.totalTimeSpentDead = None
                self.totalUnitsHealed = datav4["totalUnitsHealed"]
                self.tripleKills = datav4["tripleKills"]
                self.trueDamageDealt = datav4["trueDamageDealt"]
                self.trueDamageDealtToChampions = datav4["trueDamageDealtToChampions"]
                self.trueDamageTaken = datav4["trueDamageTaken"]
                self.turretKills = datav4["turretKills"]
                self.turretTakedowns = datav4["turretKills"]
                self.turretsLost = None
                self.unrealKills = datav4["unrealKills"]
                self.visionScore = datav4["visionScore"]
                self.visionWardsBoughtInGame = datav4["visionWardsBoughtInGame"]
                self.wardsKilled = datav4["wardsKilled"]
                self.wardsPlaced = datav4["wardsPlaced"]
                self.win = datav4["win"]
            except KeyError as e:
                if str(e).replace("'","").isnumeric():
                    raise e
                raise KeyError(data)

        self.summoner_spell_d = ddragon_factory.summonerFromId(self.summoner1Id, match.version)
        self.summoner_spell_f = ddragon_factory.summonerFromId(self.summoner2Id, match.version)

        self._match = match
        self.events = []
        self.frames = []
        self._matchup = None

    def count_events(self, filterFunction):
        return len(list(filter(filterFunction, self.events)))

    def filter_events(self, filterFunction):
        toRet = list(filter(filterFunction, self.events))
        if len(toRet) == 0:
            for e in self.events:
                print(e.__dict__)
        return toRet

    def team(self):
        return self._match.teams(self.teamId)

    def include_timeline(self, timeline):
        self.events = []
        self.frames = []
        for event in timeline.events:
            if self in event.implicated_participants:
                self.events.append(event)

        for frame in timeline.frames:
            f = frame.participantFrames[str(self.participantId)]
            if f.kills == 0:
                f.kills =  self.count_events(lambda e: e.type == "CHAMPION_KILL" and e.killer == self and e.timestamp < timedelta(minutes=timeline.frames.index(frame)))
            if f.assists == 0:
                f.assists =  self.count_events(lambda e: e.type == "CHAMPION_KILL" and self in e.assistingParticipants and e.timestamp < timedelta(minutes=timeline.frames.index(frame)))
            if f.deaths is None:
                f.deaths = self.count_events(lambda e: e.type == "CHAMPION_KILL" and e.victim == self and e.timestamp < timedelta(minutes=timeline.frames.index(frame)))
            self.frames.append(f)

    def delta_timeline(self, deltaParticipant, damageStatsFields=None, otherFields=None):
        if len(self.events) == 0:
            return {field: [] for field in damageStatsFields + otherFields}
        toRet = {field: [] for field in damageStatsFields + otherFields}
        for i in range(len(self.frames)):
            if damageStatsFields is not None and "damageStats" in self.frames[i]:
                for field in damageStatsFields:
                    #print(self.frames[i])
                    v = self.frames[i]["damageStats"][field] - deltaParticipant.frames[i]["damageStats"][field]
                    toRet[field].append(v)
            if otherFields is not None:
                for field in otherFields:
                    try:
                        v = self.frames[i][field] - deltaParticipant.frames[i][field]
                    except TypeError:
                        print(self.frames[i], field)
                        v = None
                    toRet[field].append(v)
        return toRet

    def cumulative_events_timeline(self, event_types, event_fields=None, limit=math.inf, compare='before'):
        toRet = {event_type + str(event_fields): 0 for event_type in event_types}
        if compare == "before":
            for event in filter(lambda e: e.timestamp.total_seconds() * 1000 < limit, self.events):
                if event.type in event_types:
                    if event_fields is None:
                        if self in event.implicated_participants:
                            toRet[event.type] += 1
                    else:
                        for field in event_fields:
                            target = event.__getattribute__(field)
                            if not isinstance(target, Iterable):
                                target = [target]
                            if self in target:
                                toRet[event.type + str(event_fields)] += 1

        if compare == "after":
            for event in filter(lambda e: e.timestamp > limit, self.events):
                if event.type in event_types:
                    if event_fields is None:
                        if self in event.implicated_participants:
                            toRet[event.type] += 1
                    else:
                        for field in event_fields:
                            if self in event.__getattribute__(field):
                                toRet[event.type + field] += 1
        return toRet

    def build_order(self, intermediaryItems=()):
        build = []

        for event in filter(lambda e: e.type in ["ITEM_SOLD", "ITEM_PURCHASED", "ITEM_UNDO"], self.events):
            match event.type:
                case "ITEM_PURCHASED":
                    if event.item.gold.total > 1600:
                        build.append(event)
                    else:
                        if event.item in intermediaryItems or "Boots" in event.item.tags:
                            build.append(event)
                case "ITEM_SOLD":
                    for e in build:
                        if e.item.name == event.item.name:
                            build.remove(e)
                case "ITEM_UNDO":
                    for e in build:
                        if e.item.name == event.before.name:
                            build.remove(e)

        return build

    def lane_opponent(self, competitive=False):
        if self._matchup is not None:
            return self._matchup
        if not competitive:
            for participant in self._match.participants():
                if participant.teamPosition == self.teamPosition and self.participantId != participant.participantId:
                    self._matchup = participant
                    return participant
        lane_opp = {1: 6, 2: 7, 3: 8, 4: 9, 5: 10, 6: 1, 7: 2, 8: 3, 9: 4, 10: 5}
        return self._match.participants(fieldSearch="participantId", fieldValue=lane_opp[self.participantId])


class Team:
    def __init__(self, data, match):
        self.bans = data["bans"]
        try:
            self.objectives = data["objectives"]
        except KeyError:
            self.objectives = {
                'firstBlood': data["firstBlood"],
                'firstTower': data["firstTower"],
                'firstInhibitor': data["firstInhibitor"],
                'firstBaron': data["firstBaron"],
                'firstDragon': data["firstDragon"]
            }
            try:
                self.objectives['firstRiftHerald'] = data["firstRiftHerald"]
            except Exception as e:
                self.objectives['firstRiftHerald'] = False
        self.teamId = data["teamId"]
        if self.teamId == 100:
            self.side = "Blue"
        else:
            self.side = "Red"
        self.win = data["win"]
        self.participants = list(filter(lambda p: p.teamId == self.teamId, match.participants()))
        self.cumulated_stats_save = None
        self._match = match

    def cumulated_stats(self, fields=(), save=False) -> dict:
        toRet = {f: 0 for f in fields}
        for p in self.participants:
            for f in fields:
                toRet[f] += p.__getattribute__(f)
        if save:
            self.cumulated_stats_save = toRet
        return toRet

    def enemyTeam(self):
        for t in self._match.teams():
            if t != self:
                return t


async def getMatch(data, timeline=None):
    return Match(data, timeline)


class Timeline:
    def __init__(self, data, match : Match):
        self._data = data
        if 'json' in data["info"]:
            data["info"] = data["info"]["json"]
        self.matchId = data["metadata"]["matchId"]
        self.participantsPuuids = data["metadata"]["participants"]
        try:
            self.frameInterval = data["info"]["frameInterval"]
        except KeyError as e:
            if e == "frameInterval":
                self.frameInterval = 60000
        try:
            self.frames = [Frame(frame, match) for frame in data["info"]["frames"]]
        except Exception as e:
            pprint.pp(data["info"].keys())
            raise e
        self.events = [Event(eventData, match) for frame in data["info"]["frames"] for eventData in frame["events"]]
        self.match = match

    def count_events(self, filterFunction):
        return len(list(filter(filterFunction, self.events)))

    def filter_events(self, filterFunction):
        # print(self.match.gameDuration)
        # if len(list(filter(filterFunction, self.events))) == 0:
        #      print(self.match.gameDuration)
        #      for event in self.events:
        #          print(event.__dict__)
        return list(filter(filterFunction, self.events))


class Frame:
    def __init__(self, data, match : Match):
        try:
            self.participantFrames = {pid: DefaultMunch.fromDict(data["participantFrames"][pid]) for pid in
                                  data["participantFrames"]}
            for index, pframe in enumerate(self.participantFrames):
                pf = self.participantFrames[pframe]
                pf.position = Position(pf.position, match.map)
                try:
                    participant = match.participants(fieldSearch="participantId",fieldValue=pf.participantId)
                    if pf.kills == None:
                        pf.kills = participant.count_events(lambda e : e.killer == participant and e.gameTime < timedelta(minutes=index))
                    if pf.assists == None:
                        pf.assists = participant.count_events(lambda e : participant in e.assistingParticipants and e.gameTime < timedelta(minutes=index))
                    pf.totalMinionsKilled = pf.minionsKilled + pf.jungleMinionsKilled
                except TypeError as e:
                    raise e
        except TypeError:
            pprint.pp(data)
            self.participantFrames = None


spellKeys = {1: "A", 2: "W", 3: "E", 4: "R"}


class Event:
    def __init__(self, eventData, match):
        self.type = eventData["type"]
        self.timestamp = timedelta(milliseconds=eventData["timestamp"])
        self.implicated_participants = []
        if "bounty" in eventData:
            self.bounty = eventData["bounty"]

        match self.type:
            case "ITEM_PURCHASED":
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.item = ddragon_factory.itemFromId(eventData["itemId"], match.version)
                self.implicated_participants = [self.participant]
            case "ITEM_UNDO":
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.before = ddragon_factory.itemFromId(eventData["beforeId"], match.version)
                self.after = eventData["afterId"]
                try:
                    self.goldGain = eventData["goldGain"]
                except KeyError:
                    self.goldGain = 0
                self.implicated_participants = [self.participant]
            case "SKILL_LEVEL_UP":
                self.levelUpType = eventData["levelUpType"]
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.skillSlot = eventData["skillSlot"]
                self.spellKey = spellKeys[self.skillSlot]
                self.spell = lambda: self.participant.champion.spells[self.skillSlot - 1]

                self.implicated_participants = [self.participant]
            case "WARD_PLACED":
                self.creator = match.participants(fieldSearch="participantId", fieldValue=eventData["creatorId"])
                self.ward_type = eventData["wardType"]
                self.implicated_participants = [self.creator]
            case "ITEM_DESTROYED":
                self.item = ddragon_factory.itemFromId(eventData["itemId"], match.version)
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.implicated_participants = [self.participant]
            case "LEVEL_UP":
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.level = eventData["level"]
                self.implicated_participants = [self.participant]
            case "CHAMPION_KILL":
                try:
                    self.assistingParticipants = [match.participants(fieldSearch="participantId", fieldValue=assistId)
                                                  for
                                                  assistId in eventData["assistingParticipantIds"]]
                except KeyError:
                    self.assistingParticipants = []
                try:
                    self.bounty = eventData["bounty"]
                    self.killStreakLength = eventData["killStreakLength"]
                except KeyError:
                    self.bounty = None
                    self.killStreakLength = None
                self.killer = match.participants(fieldSearch="participantId", fieldValue=eventData["killerId"])
                self.position = Position(eventData["position"], match.map)
                self.victim = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["victimId"]
                )
                try:
                    self.victimDamageDealt = [DeathRecapElement(element, match, dmg_from=self.victim) for element in
                                              eventData["victimDamageDealt"]]
                except KeyError:
                    self.victimDamageDealt = []
                try:
                    self.victimDamageReceived = [DeathRecapElement(element, match, dmg_to=self.victim) for element in
                                                 eventData["victimDamageReceived"]]
                except KeyError:
                    self.victimDamageReceived = []
                self.implicated_participants = [self.victim, self.killer] + self.assistingParticipants

            case "CHAMPION_SPECIAL_KILL":
                self.killType = eventData["killType"]
                self.killer = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["killerId"]
                )
                self.position = Position(eventData["position"], match.map)
                self.position = Position(eventData["position"], match.map)
                self.implicated_participants = [self.killer]

            case "ELITE_MONSTER_KILL":
                self.killer = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["killerId"]
                )
                if self.killer is not None:
                    try:
                        self.team = match.teams(teamId=eventData["killerTeamId"])
                    except KeyError:
                        self.team = self.killer.team()

                self.monsterType = eventData["monsterType"]
                if self.monsterType == "DRAGON":
                    try:
                        self.monsterSubType = eventData["monsterSubType"]
                    except KeyError:
                        self.monsterSubType = ""
                try:
                    self.assistingParticipants = eventData["assistingParticipantIds"]
                except KeyError:
                    self.assistingParticipants = []
                self.position = Position(eventData["position"], match.map)
                self.implicated_participants = [self.killer] + self.assistingParticipants

            case "ITEM_SOLD":
                self.item = ddragon_factory.itemFromId(eventData["itemId"], match.version)
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.implicated_participants = [self.participant]

            case "PAUSE_END":
                self.realTimestamp = datetime.fromtimestamp(eventData["realTimestamp"] / 1000)
            case "PAUSE_START":
                self.realTimestamp = datetime.fromtimestamp(eventData["realTimestamp"] / 1000)

            case "TURRET_PLATE_DESTROYED":
                if eventData["killerId"] != 0:
                    self.killer = match.participants(
                        fieldSearch="participantId", fieldValue=eventData["killerId"]
                    )
                else:
                    self.killer = None
                try:
                    self.assistingParticipants = eventData["assistingParticipantIds"]
                except KeyError:
                    self.assistingParticipants = []
                self.laneType = eventData["laneType"]
                self.team = match.teams(teamId=eventData["teamId"])
                self.position = Position(eventData["position"], match.map)
                self.implicated_participants = [self.killer] + self.assistingParticipants

            case "BUILDING_KILL":
                try:
                    self.assistingParticipants = eventData["assistingParticipantIds"]
                except KeyError:
                    self.assistingParticipants = []
                self.buildingType = eventData["buildingType"]
                if self.buildingType == "TOWER_BUILDING":
                    self.towerType = eventData["towerType"]
                if eventData["killerId"] != 0:
                    self.killer = match.participants(
                        fieldSearch="participantId", fieldValue=eventData["killerId"]
                    )
                else:
                    self.killer = None
                self.laneType = eventData["laneType"]
                self.position = Position(eventData["position"], match.map)
                self.team = match.teams(teamId=eventData["teamId"])
                self.implicated_participants = [self.killer] + self.assistingParticipants

            case "GAME_END":
                self.gameId = eventData["gameId"]
                self.realTimestamp = eventData["realTimestamp"]
                self.gameId = eventData["gameId"]
                self.gameId = eventData["gameId"]
                self.gameId = eventData["gameId"]

            case "WARD_KILL":
                self.killer = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["killerId"]
                )
                self.ward_type = eventData["wardType"]
                self.implicated_participants = [self.killer]

            case "DRAGON_SOUL_GIVEN":
                self.name = eventData["name"]
                self.team = match.teams(teamId=eventData["teamId"])
            case "OBJECTIVE_BOUNTY_PRESTART":
                self.team = match.teams(teamId=eventData["teamId"])
                self.actualStartTime = eventData["actualStartTime"]
            case "CHAMPION_TRANSFORM":
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.transformType = eventData["transformType"]
                self.implicated_participants = [self.participant]
            case "OBJECTIVE_BOUNTY_FINISH":
                self.team = match.teams(teamId=eventData["teamId"])

            case _:
                pprint.pp(eventData)
                raise ValueError("{} event type not handled".format(self.type))


class DeathRecapElement:
    def __init__(self, data, match, dmg_from=None, dmg_to=None):
        self.basic = data["basic"]
        self.magicDamage = data["magicDamage"]
        self.physicalDamage = data["physicalDamage"]
        self.trueDamage = data["trueDamage"]
        if dmg_to is None:
            self.dmg_from = dmg_from
            self.to = match.participants(
                fieldSearch="participantId", fieldValue=data["participantId"]
            )
        else:
            self.to = dmg_to
            if data["participantId"] != 0:
                self.dmg_from = match.participants(
                    fieldSearch="participantId", fieldValue=data["participantId"]
                )
            else:
                self.dmg_from = None

        self.spellName = data["spellName"]
        self.spellSlot = data["spellSlot"]
        self.type = data["type"]
