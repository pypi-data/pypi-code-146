#!/usr/bin/env python3
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

from trosnoth.const import ACHIEVEMENT_TACTICAL, BOT_GOAL_KILL_THINGS
from trosnoth.levels.base import Level, play_level
from trosnoth.levels.maps import LargeRingsMap, SmallRingMap, SmallStackMap
from trosnoth.messages import AwardPlayerCoinMsg
from trosnoth.triggers.coins import SlowlyIncrementLivePlayerCoinsTrigger
from trosnoth.triggers.deathmatch import (
    AddLimitedBotsTrigger, PlayerLifeScoreTrigger,
    PlayerKillScoreTrigger,
)


MIN_HUNTERS = 4
MAX_HUNTERS = 12
BONUS_COINS_FOR_WINNER = 500


class HuntedLevel(Level):
    levelName = 'Hunted'
    default_duration = 6 * 60
    map_selection = (
        LargeRingsMap(),
        SmallRingMap(),
        SmallStackMap(),
    )
    level_code = 'hunted'

    def __init__(self, *args, **kwargs):
        super(HuntedLevel, self).__init__(*args, **kwargs)
        self.duration = self.level_options.get_duration(self)
        self.blue_team = self.red_team = None

    def get_team_to_join(self, preferred_team, user, nick, bot):
        return self.red_team

    def pre_sync_setup(self):
        self.blue_team, self.red_team = self.pre_sync_create_teams(
            [
                ('Hunters', ()),
                ('Hunted', self.world.players),
            ]
        )
        self.level_options.apply_map_layout(self)
        self.world.uiOptions.team_ids_humans_can_join = [b'B']

    async def run(self):
        try:
            self.red_team.abilities.set(aggression=False)

            for player in self.world.players:
                if not player.bot:
                    room = self.world.select_good_respawn_zone_for_team(self.red_team)
                    self.world.magically_move_player_now(player, room.centre, alive=True)


            SlowlyIncrementLivePlayerCoinsTrigger(self).activate()
            scoreTrigger = PlayerLifeScoreTrigger(
                self, teams={self.red_team}).activate()
            PlayerKillScoreTrigger(self, dieScore=0).activate()
            botTrigger = AddLimitedBotsTrigger(level=self, max_bots=MAX_HUNTERS,
                min_bots=MIN_HUNTERS, bot_kind='terminator', bot_nick='Terminator',
                bot_team=self.blue_team, increase_with_enemies=True).activate()
            self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
            self.setUserInfo('Hunted', (
                '* Die as few times as possible',
                '* Players score points for every second they are alive',
            ), BOT_GOAL_KILL_THINGS)
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
            maxScore = max(playerScores.values())
            winners = [
                p for p, score in list(playerScores.items())
                if score == maxScore and p.team == self.red_team]

            self.set_winners(winners)
            for winner in winners:
                self.world.sendServerCommand(
                    AwardPlayerCoinMsg(winner.id, BONUS_COINS_FOR_WINNER))

            await self.world.sleep_future(3)
        finally:
            self.red_team.abilities.set(aggression=True)


if __name__ == '__main__':
    play_level(HuntedLevel(), bot_count=1)
