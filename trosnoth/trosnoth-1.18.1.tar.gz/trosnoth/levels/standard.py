#!/usr/bin/env python3
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

import asyncio
import logging

from trosnoth.const import (
    BOT_GOAL_CAPTURE_MAP, ACHIEVEMENT_AFTER_GAME, ACHIEVEMENT_TERRITORY,
    ACHIEVEMENT_TACTICAL, BONUS_COINS_FOR_RABBIT_SURVIVAL,
)
from trosnoth.levels.base import (
    Level, play_level, SELECTABLE_TEAMS,
    FORCE_RANDOM_TEAMS, HVM_TEAMS,
)
from trosnoth.levels.maps import StandardMap, SmallMap, WideMap, LargeMap
from trosnoth.messages import AwardPlayerCoinMsg
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.bots import BalanceTeamsTrigger
from trosnoth.triggers.coins import (
    SlowlyIncrementLivePlayerCoinsTrigger, AwardStartingCoinsTrigger,
)
from trosnoth.triggers.rabbits import RabbitHuntTrigger
from trosnoth.triggers.zonecaps import (
    StandardZoneCaptureTrigger, StandardGameVictoryTrigger,
    PlayerZoneScoreTrigger,
)
from trosnoth.utils.event import waitForEvents

log = logging.getLogger(__name__)


class StandardLevel(Level):
    '''
    The base class used for levels with standard joining rules and win
    conditions.
    '''
    keepPlayerScores = True
    allowAutoBalance = True
    levelName = 'Trosnoth Match'
    countdown_time = 10

    default_duration = 20 * 60
    team_selection = (
        SELECTABLE_TEAMS,
        FORCE_RANDOM_TEAMS,
        HVM_TEAMS,
    )
    map_selection = (
        StandardMap(),
        SmallMap(),
        WideMap(),
        LargeMap(),
    )
    coin_increment_factor = 1

    def __init__(self, *args, include_rabbit_hunt=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.a_human_player_won = False
        self.include_rabbit_hunt = include_rabbit_hunt

    def getDuration(self):
        return None

    def pre_sync_setup(self):
        super().pre_sync_setup()
        if self.level_options.get_team_option(self) == SELECTABLE_TEAMS:
            self.world.uiOptions.team_ids_humans_can_join = [b'A', b'B']
            self.world.uiOptions.team_ids_humans_can_switch_to = [b'A', b'B']
        else:
            self.world.uiOptions.team_ids_humans_can_join = [NEUTRAL_TEAM_ID]

    async def run(self):
        team_option = self.level_options.get_team_option(self)
        if team_option == HVM_TEAMS and not self.world.botManager:
            self.begin_hvm()

        SlowlyIncrementLivePlayerCoinsTrigger(self, factor=self.coin_increment_factor).activate()

        await self.pregameCountdownPhase()

        await self.mainGamePhase()

        self.gameOver()

        if self.include_rabbit_hunt:
            await self.rabbitHuntPhase()
        else:
            self.world.clock.pause()
            self.world.clock.propagateToClients()
            await self.world.sleep_future(5)
        self.world.scoreboard.setMode(players=False, teams=False)

        return self.a_human_player_won, None

    async def pregameCountdownPhase(self):
        startingCoinsTrigger = AwardStartingCoinsTrigger(self).activate()

        self.setUserInfo('Get Ready...', (
            '* Game will begin soon',
            '* Capture or neutralise all enemy zones',
            '* To capture a zone, touch the orb',
            "* If a team's territory is split, the smaller section is neutralised",
            '* Use TAB and SPACE to select and buy items',
        ), BOT_GOAL_CAPTURE_MAP)
        self.world.clock.startCountDown(self.countdown_time, flashBelow=0)
        self.world.clock.propagateToClients()

        self.world.pauseStats()
        self.world.abilities.set(respawn=False, leaveFriendlyZones=False)
        self.world.onChangeVoiceChatRooms(self.world.teams, self.world.players)
        await self.world.clock.onZero.wait_future()
        startingCoinsTrigger.deactivate()

    async def mainGamePhase(self):
        winTrigger = StandardGameVictoryTrigger(self).activate()
        if self.keepPlayerScores:
            PlayerZoneScoreTrigger(self).activate()

        balanceTeamsTrigger = None
        if self.should_balance_teams():
            balanceTeamsTrigger = BalanceTeamsTrigger(self).activate()

        zoneCapTrigger = StandardZoneCaptureTrigger(self).activate()

        self.world.setActiveAchievementCategories({
            ACHIEVEMENT_TERRITORY, ACHIEVEMENT_TACTICAL})
        self.setMainGameUserInfo()
        self.notifyAll('The game is now on!!')
        self.playSound('startGame.ogg')
        self.world.resumeStats()
        self.world.abilities.set(respawn=True, leaveFriendlyZones=True)

        duration = self.getDuration()
        if duration:
            self.world.clock.startCountDown(duration)
        else:
            self.world.clock.stop()
        self.world.clock.propagateToClients()

        event, args = await waitForEvents([
            self.world.clock.onZero, winTrigger.onVictory])

        winTrigger.deactivate()
        zoneCapTrigger.deactivate()
        if balanceTeamsTrigger:
            balanceTeamsTrigger.deactivate()

    def should_balance_teams(self):
        if not self.world.abilities.balanceTeams:
            return False
        if not self.allowAutoBalance:
            return False
        if self.world.no_auto_balance:
            return False
        if self.level_options.get_team_option(self) == HVM_TEAMS:
            return False

        if not self.world.game.serverInterface:
            return True
        difficulty = self.world.game.serverInterface.get_balance_bot_difficulty()
        if difficulty is None:
            return False
        return True

    def setMainGameUserInfo(self):
        self.setUserInfo('Trosnoth Match', (
            '* Capture or neutralise all enemy zones',
            '* To capture a zone, touch the orb',
            "* If a team's territory is split, the smaller section is neutralised",
            '* Use TAB and SPACE to select and buy items',
        ), BOT_GOAL_CAPTURE_MAP)

    def gameOver(self):
        self.world.setActiveAchievementCategories({ACHIEVEMENT_AFTER_GAME})
        self.world.abilities.set(zoneCaps=False)

        maxZones = max(t.numZonesOwned for t in self.world.teams)
        winners = [t for t in self.world.teams if t.numZonesOwned == maxZones]
        if len(winners) > 1:
            winners = []
            winner = None
        else:
            winner = winners[0]

        self.a_human_player_won = any(p.team in winners and not p.bot for p in self.world.players)

        self.set_winners(winners)
        self.world.onStandardGameFinished(winner)

    async def rabbitHuntPhase(self, finalSleepTime=3):
        rabbitHuntTrigger = RabbitHuntTrigger(self).activate()
        result = await rabbitHuntTrigger.onComplete.wait_future()
        for player in result['liveRabbits']:
            self.world.sendServerCommand(
                AwardPlayerCoinMsg(player.id, BONUS_COINS_FOR_RABBIT_SURVIVAL))
            self.world.game.achievementManager.triggerAchievement(
                player, b'rabbitSurvival')

        await self.world.sleep_future(finalSleepTime)


class StandardRandomLevel(StandardLevel):
    '''
    A standard Trosnoth level with no special events or triggers, played on
    a randomised map.
    '''

    level_code = 'standard'
    hvm_level_name = 'Humans v Machines'

    def __init__(self, map_=None, **kwargs):
        super().__init__(**kwargs)

        self.map = map_
        self.duration = self.level_options.get_duration(self)

    def pre_sync_setup(self):
        super().pre_sync_setup()
        if self.map is None:
            self.level_options.apply_map_layout(self)
        else:
            self.map.apply(self)

    def getDuration(self):
        return self.duration


if __name__ == '__main__':
    play_level(StandardRandomLevel(), bot_count=1)
