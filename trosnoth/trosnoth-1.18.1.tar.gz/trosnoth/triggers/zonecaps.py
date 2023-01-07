

import logging

from trosnoth.model.zonemechanics import ZoneCaptureCalculator
from trosnoth.triggers.base import Trigger
from trosnoth.utils.event import Event

log = logging.getLogger(__name__)


class StandardZoneCaptureTrigger(Trigger):
    '''
    When a player touches an orb, capture that orb according to the standard
    Trosnoth zone capture rules.
    '''

    zone_capture_calculator_factory = ZoneCaptureCalculator

    def doActivate(self):
        self.world.onUnitsAllAdvanced.addListener(self.unitsHaveAdvanced)

    def doDeactivate(self):
        self.world.onUnitsAllAdvanced.removeListener(self.unitsHaveAdvanced)

    def unitsHaveAdvanced(self):
        self.zone_capture_calculator_factory.apply_to_world(self.world)


class StandardGameVictoryTrigger(Trigger):
    def __init__(self, *args, **kwargs):
        super(StandardGameVictoryTrigger, self).__init__(*args, **kwargs)
        self.onVictory = Event(['team'])
        self.dirty = True

    def doActivate(self):
        self.world.onZoneTagged.addListener(self.gotZoneTag)
        self.world.onServerTickComplete.addListener(self.gotTickComplete)
        self.dirty = True

    def doDeactivate(self):
        self.world.onZoneTagged.removeListener(self.gotZoneTag)
        self.world.onServerTickComplete.removeListener(self.gotTickComplete)

    def gotZoneTag(self, *args, **kwargs):
        self.dirty = True

    def gotTickComplete(self, *args, **kwargs):
        if not self.dirty:
            return
        teams_with_rooms = {r.owner for r in self.world.rooms if r.owner is not None}

        if len(teams_with_rooms) == 1:
            self.onVictory(teams_with_rooms.pop())
        elif len(teams_with_rooms) == 0:
            self.onVictory(None)

        self.dirty = False


class PlayerZoneScoreTrigger(Trigger):
    '''
    When a zone is neutralised or captured, award leaderboard points to all
    players in the zone on that team.
    '''

    def doActivate(self):
        self.world.onZoneCaptureFinalised.addListener(self.gotZoneCap)
        self.world.scoreboard.setMode(players=True)

    def doDeactivate(self):
        self.world.onZoneCaptureFinalised.removeListener(self.gotZoneCap)
        if self.world.scoreboard:
            self.world.scoreboard.setMode(players=False)

    def gotZoneCap(self, captureInfo):
        if not captureInfo['attackers']:
            return

        score = captureInfo['points'] / len(captureInfo['attackers'])
        for p in captureInfo['attackers']:
            self.world.scoreboard.playerScored(p, score)

