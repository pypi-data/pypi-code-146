#!/usr/bin/env python3
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

from trosnoth.const import ACHIEVEMENT_TACTICAL, BOT_GOAL_HUNT_RABBITS
from trosnoth.levels.base import Level, play_level
from trosnoth.levels.maps import LargeRingsMap, SmallRingMap, SmallStackMap
from trosnoth.messages import AwardPlayerCoinMsg
from trosnoth.triggers.base import Trigger
from trosnoth.triggers.coins import SlowlyIncrementLivePlayerCoinsTrigger
from trosnoth.triggers.deathmatch import (
    PlayerKillScoreTrigger, AddLimitedBotsTrigger,
)


MIN_PIGEONS = 4
MAX_PIGEONS = 12
BONUS_COINS_FOR_WINNER = 500


class CatPigeonLevel(Level):
    levelName = 'Cat Among Pigeons'
    level_code = 'catpigeon'

    default_duration = 4 * 60
    map_selection = (
        LargeRingsMap(),
        SmallRingMap(),
        SmallStackMap(),
    )

    def __init__(self, map_builder=None, *args, **kwargs):
        super(CatPigeonLevel, self).__init__(*args, **kwargs)
        self.duration = self.level_options.get_duration(self)
        self.blue_team = self.red_team = None
        self.map_builder = map_builder

    def get_team_to_join(self, preferred_team, user, nick, bot):
        return self.blue_team

    def pre_sync_setup(self):
        self.blue_team, self.red_team = self.pre_sync_create_teams(
            [
                ('Cats', self.world.players),
                ('Pigeons', ()),
            ]
        )
        if self.map_builder:
            self.world.setLayout(self.map_builder())
        else:
            self.level_options.apply_map_layout(self)
        self.world.uiOptions.team_ids_humans_can_join = [b'A']

    async def run(self):
        SlowlyIncrementLivePlayerCoinsTrigger(self).activate()
        scoreTrigger = PlayerKillScoreTrigger(self).activate()
        RespawnOnJoinTrigger(self).activate()
        botTrigger = AddLimitedBotsTrigger(self, max_bots=MAX_PIGEONS, min_bots=MIN_PIGEONS,
            bot_kind='sirrobin', bot_nick='Pigeon', bot_team=self.red_team,
            increase_with_enemies=True).activate()
        self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
        self.setUserInfo('Cat Among Pigeons', (
            '* Kill as many enemy players as you can',
        ), BOT_GOAL_HUNT_RABBITS)
        self.world.abilities.set(zoneCaps=False, balanceTeams=False)
        if self.duration:
            self.world.clock.startCountDown(self.duration)
        else:
            self.world.clock.stop()
        self.world.clock.propagateToClients()

        await self.world.clock.onZero.wait_future()

        # Game over!
        self.world.finaliseStats()
        scoreTrigger.deactivate()
        botTrigger.deactivate()
        playerScores = self.world.scoreboard.playerScores
        max_score = max(playerScores.values())
        winners = [
            p for p, score in list(playerScores.items())
            if score == max_score and p.team == self.blue_team]

        self.set_winners(winners)
        for winner in winners:
            self.world.sendServerCommand(
                AwardPlayerCoinMsg(winner.id, BONUS_COINS_FOR_WINNER))

        await self.world.sleep_future(0.1)

        return True, max_score


class RespawnOnJoinTrigger(Trigger):
    def doActivate(self):
        self.world.onPlayerAdded.addListener(self.got_player_added)
        for player in self.world.players:
            self.got_player_added(player)

    def doDeactivate(self):
        self.world.onPlayerAdded.removeListener(self.got_player_added)

    def got_player_added(self, player, *args, **kwargs):
        if player.team == self.level.blue_team:
            central_room = self.world.rooms.get_at(self.world.map.centre)
            self.world.magically_move_player(player, central_room.orb_pos, alive=True)


if __name__ == '__main__':
    play_level(CatPigeonLevel(), bot_count=1)
