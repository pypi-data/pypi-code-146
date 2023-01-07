#!/usr/bin/env python3
# coding=utf-8
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

from trosnoth.const import (
    ACHIEVEMENT_TACTICAL, BOT_GOAL_KILL_THINGS, DEFAULT_TEAM_NAME_1,
    DEFAULT_TEAM_NAME_2,
)
from trosnoth.levels.base import Level, play_level
from trosnoth.levels.maps import (
    LargeRingsMap, SmallRingMap, SmallStackMap, LabyrinthMap,
    SmallMap, StandardMap, LargeMap, WideMap, FreeFlowMap,
)
from trosnoth.messages import AwardPlayerCoinMsg
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.coins import (
    SlowlyIncrementLivePlayerCoinsTrigger, AwardStartingCoinsTrigger,
)
from trosnoth.triggers.deathmatch import (
    PlayerKillScoreTrigger, AddOneBotTrigger,
)

BONUS_COINS_FOR_WINNER = 500


class FreeForAllLevel(Level):
    levelName = 'Free for All'
    default_duration = 6 * 60
    map_selection = (
        LargeRingsMap(),
        SmallRingMap(),
        SmallStackMap(),
        LabyrinthMap(),
        FreeFlowMap(),
        StandardMap(),
        SmallMap(),
        WideMap(),
        LargeMap(),
    )
    level_code = 'free4all'

    def __init__(self, map_builder=None, add_one_bot=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_one_bot = add_one_bot
        self.duration = self.level_options.get_duration(self)
        self.map_builder = map_builder

    def get_team_to_join(self, preferred_team, user, nick, bot):
        return None

    def pre_sync_setup(self):
        self.pre_sync_create_teams(
            [(DEFAULT_TEAM_NAME_1, ()), (DEFAULT_TEAM_NAME_2, ())],
            neutral_players=self.world.players)

        if self.map_builder is None:
            self.level_options.apply_map_layout(self)
        else:
            self.world.setLayout(self.map_builder())
        self.world.uiOptions.team_ids_humans_can_join = [NEUTRAL_TEAM_ID]

    async def run(self):
        SlowlyIncrementLivePlayerCoinsTrigger(self).activate()
        AwardStartingCoinsTrigger(self).activate()
        PlayerKillScoreTrigger(self, dieScore=-0.5).activate()
        if self.add_one_bot:
            AddOneBotTrigger(self).activate()
        self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
        self.setUserInfo('Free for All', (
            '* You gain 1 point per kill',
            '* You lose ½ point if you are killed',
            '* Kills earn you money',
            '* Use TAB to select an item to buy',
            '* Press SPACE to buy selected item',
        ), BOT_GOAL_KILL_THINGS)
        self.world.abilities.set(zoneCaps=False, balanceTeams=False)
        if self.duration:
            self.world.clock.startCountDown(self.duration)
        else:
            self.world.clock.stop()
        self.world.clock.propagateToClients()

        await self.world.clock.onZero.wait_future()

        # Game over!
        playerScores = self.world.scoreboard.playerScores
        max_score = max(playerScores.values())
        winners = [
            p for p, score in list(playerScores.items())
            if score == max_score]

        self.set_winners(winners)
        for winner in winners:
            self.world.sendServerCommand(
                AwardPlayerCoinMsg(winner.id, BONUS_COINS_FOR_WINNER))

        await self.world.sleep_future(3)

        return any(not p.bot for p in winners), max_score


if __name__ == '__main__':
    play_level(FreeForAllLevel(), bot_count=0)
