import asyncio
import dataclasses
import logging
import random
from typing import Optional

from twisted.internet import defer

from trosnoth.const import (
    GAME_FULL_REASON, PRIVATE_CHAT, BOT_GOAL_NONE, DEFAULT_BOT_DIFFICULTY, DEFAULT_TEAM_NAME_1,
    DEFAULT_TEAM_NAME_2, BOT_GOAL_KILL_THINGS,
)
from trosnoth.levels.hvm import HumansVsMachinesBotManager
from trosnoth.levels.maps import MapAPI, DefaultLobbyMap
from trosnoth.messages import (
    ChatMsg, PlaySoundMsg, UpdateGameInfoMsg, ChatFromServerMsg,
    SetTeamNameMsg, RemovePlayerMsg, RemoveProjectileMsg, SetPlayerCoinsMsg,
)
from trosnoth.model.player import Player
from trosnoth.model.team import Team
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.lobby import (
    AddBotsForLobbyTrigger, MakeNewPlayersNeutralTrigger,
    StartGameWhenReadyTrigger,
)
from trosnoth.utils.aio import as_future

log = logging.getLogger(__name__)

SELECTABLE_TEAMS = 'Flexible teams'
FORCE_RANDOM_TEAMS = 'Random teams (no choice)'
HVM_TEAMS = 'Humans vs. Machines'


def preferred_team_otherwise_smallest(preferred_team, universe, include_bots=False):
    if preferred_team is not None:
        return preferred_team

    team_sizes = {t: 0 for t in universe.teams}
    for player in universe.players:
        if player.team in team_sizes and (include_bots or not player.bot):
            team_sizes[player.team] = team_sizes[player.team] + 1

    smallest_size = min(team_sizes.values())
    options = [t for t, v in team_sizes.items() if v == smallest_size]
    return random.choice(options)


class BotController:
    '''
    This class exists as an interface between the level and a PuppetBot. At
    the moment it just proxies orders through to the bot, but ultimately the
    bot will be running in a separate process.
    '''

    def __init__(self, agent):
        self.agent = agent
        self._bot = agent.ai
        self.onOrderFinished = self._bot.onOrderFinished

    @property
    def player(self):
        return self._bot.player

    def standStill(self):
        return self._bot.standStill()

    def moveToPoint(self, pos):
        return self._bot.moveToPoint(pos)

    def move_to_room(self, room):
        return self._bot.move_to_room(room)

    def move_to_orb(self, room):
        return self._bot.move_to_orb(room)

    def attackPlayer(self, player):
        return self._bot.attackPlayer(player)

    def followPlayer(self, player):
        return self._bot.followPlayer(player)

    def collectTrosball(self):
        return self._bot.collectTrosball()

    def respawn(self, zone=None):
        return self._bot.respawn(zone)

    def setAggression(self, aggression):
        return self._bot.setAggression(aggression)

    def set_dodges_bullets(self, dodges_bullets):
        return self._bot.set_dodges_bullets(dodges_bullets)

    def setUpgradePolicy(self, upgrade, coinBuffer=0, delay=0):
        return self._bot.setUpgradePolicy(upgrade, coinBuffer, delay)


@dataclasses.dataclass
class LevelOptions:
    team_option_index: int = 0
    map_index: int = 0
    duration: Optional[float] = None

    def get_duration(self, level):
        return self.duration if self.duration is not None else level.default_duration

    def get_team_option(self, level):
        return level.team_selection[self.team_option_index]

    def get_map(self, level) -> MapAPI:
        return level.map_selection[self.map_index]

    def apply_map_layout(self, level):
        return self.get_map(level).apply(level)


RESERVED_TEAM_NAMES = {'machines'}


def get_preferred_team_name(players, default=None):
    preferences = {}
    for p in players:
        if p.suggested_team_name and not p.bot:
            suggestion = p.suggested_team_name.strip()
            if suggestion.lower() in RESERVED_TEAM_NAMES:
                continue
            preferences[suggestion] = preferences.get(suggestion, 0) + 1

    if not preferences:
        return default

    return max(preferences, key=preferences.get)


def get_preferred_scenario(game, players):
    counts = {}
    for player in players:
        choice = player.suggested_scenario_class
        if choice is None:
            continue
        hvm = player.suggested_scenario_hvm
        counts[choice, hvm] = counts.get((choice, hvm), 0) + 1

    if counts:
        level_class, hvm = max(counts, key=counts.get)
    else:
        from trosnoth.levels.registry import scenario_options
        from trosnoth.levels.standard import StandardRandomLevel
        if random.random() >= .5:
            level_class = StandardRandomLevel
        else:
            level_class = random.choice(scenario_options)

        if HVM_TEAMS in level_class.team_selection:
            hvm = random.random() > .7
        else:
            hvm = False

    level_options = LevelOptions(
        duration=get_preferred_duration(game, players),
        map_index=get_preferred_map_index(level_class, players),
    )
    if hvm:
        level_options.team_option_index = level_class.team_selection.index(HVM_TEAMS)
    return level_class(level_options=level_options)


def get_preferred_duration(game, players):
    lobby_settings = game.lobbySettings
    forced_duration = lobby_settings.get_forced_duration() if lobby_settings else None
    if forced_duration:
        return forced_duration * 60

    counts = {}
    for player in players:
        duration = player.suggested_duration
        counts[duration] = counts.get(duration, 0) + 1

    if not counts:
        return None

    return max(counts, key=counts.get) or None


def get_preferred_map_index(level_class, players):
    index_by_code = {map_class.code: i for i, map_class in enumerate(level_class.map_selection)}
    counts = {}
    for player in players:
        if player.suggested_map in index_by_code:
            index = index_by_code[player.suggested_map]
            counts[index] = counts.get(index, 0) + 1

    if not counts:
        return 0
    return max(counts, key=counts.get)


HUMANS_TEAM_NAME = 'Humans'
MACHINES_TEAM_NAME = 'Machines'


class Level(object):
    '''
    Base class for all standard and custom levels. A level provides
    server-only instructions about how a particular game is set up and
    operates.

    NOTE that clients know nothing about what level is being used, so any
    events that affect world state need to be carried out through the
    message-passing API in order that clients stay in sync with the server.
    '''

    recordGame = True
    resetPlayerCoins = True
    levelName = None

    default_duration: float
    team_selection = ('Scenario default',)
    map_selection = (None,)

    # Any level that can be selected in-game or in the server web
    # interface must define a string level_code value.
    level_code = None

    # If hvm_level_name is set, it will show up in the level options
    # lists. If it's not set, Humans vs. Machines will not be avalaible
    # for this level kind.
    hvm_level_name = None

    coins_for_kills_factor = 1
    coins_for_caps_factor = 1
    respawn_time_factor = 1

    def __init__(self, *args, level_options=None, **kwargs):
        super(Level, self).__init__(*args, **kwargs)
        self.world = None
        self._winner = None
        self.activeTriggers = set()
        self.level_options = level_options or LevelOptions()

    def begin_hvm(self):
        if self.world.botManager:
            raise RuntimeError('Another BotManager is active')
        if self.world.teams[0].teamName == HUMANS_TEAM_NAME:
            reverse = False
        elif self.world.teams[0].teamName == MACHINES_TEAM_NAME:
            reverse = True
        else:
            reverse = random.randrange(2)
        self.world.botManager = HumansVsMachinesBotManager(self.world, reverse)
        self.world.botManager.startingSoon()

    def pre_sync_setup(self):
        '''
        Called before all world state is synced to clients. This is
        typically used to set up the map, team names, and sometimes team
        allocations.

        The default implementation selects teams based on the selected
        team options. If a scenario is going to generate teams in some
        other way, it should override this method. I.e., it should not call
        super().pre_sync_setup().
        '''
        team_option = self.level_options.get_team_option(self)
        if team_option == FORCE_RANDOM_TEAMS:
            self.pre_sync_randomise_teams()
        elif team_option == HVM_TEAMS:
            self.pre_sync_create_hvm_teams()
        else:
            self.pre_sync_create_preferred_teams()
        self.world.abilities.respawn_time_factor = self.respawn_time_factor

    async def run_lobby_period(self):
        '''
        When hosting a LAN game, this is called after the world state is
        synced to clients. It should take care of setting up and tearing
        down the lobby period, and should call wait_for_ready_players()
        or equivalent to wait until everyone selects ready.

        The default implementation will return all players to ghosts in
        their own territory before returning.
        '''
        self.setUserInfo('Waiting for players…', (
            '* Select "Ready" to start',
        ), BOT_GOAL_KILL_THINGS)
        await self.wait_for_ready_players()

        self.return_players_to_own_territory(alive=False)
        self.remove_all_projectiles()
        self.reset_coins_to_zero()

    def return_players_to_own_territory(self, alive=None):
        for p in self.world.players:
            pos = self.world.select_good_respawn_zone_for_team(p.team).centre
            self.world.magically_move_player_now(p, pos, alive=alive)

    def remove_all_projectiles(self):
        for projectile_id in list(self.world.projectile_by_id):
            self.world.sendServerCommand(RemoveProjectileMsg(projectile_id))

    def reset_coins_to_zero(self):
        for p in self.world.players:
            self.world.sendServerCommand(SetPlayerCoinsMsg(p.id, 0))

    async def wait_for_ready_players(self):
        with self.world.uiOptions.modify(showReadyStates=True), \
                self.world.abilities.modify(
                    leaveFriendlyZones=True, zoneCaps=False, renaming=True):
            while True:
                humans = [p for p in self.world.players if not p.bot]
                if humans and all(p.readyToStart for p in humans):
                    break

                await as_future(self.world.sleep(3))

    def pre_sync_create_teams(self, team_info, neutral_players=(), remove_others=True):
        '''
        Sets team names and players on teams.
        Only call this from pre_sync_setup() as it does not sync changes
        to clients.

        :param team_info: sequence of (team_name, players) for each team
        :param neutral_players: if provided, these players will become
            neutral
        :param remove_others: whether or not to remove players who are
            not mentioned in team_info or neutral_players (default True)
        :return: sequence of teams
        '''
        unseen_players = set(self.world.players)

        team_objects = self.world.teams
        for team, (team_name, players) in zip(team_objects, team_info):
            team.teamName = team_name
            for player in players:
                player.team = team
                unseen_players.discard(player)

        for player in neutral_players:
            player.team = None
            unseen_players.discard(player)

        if remove_others:
            for player in unseen_players:
                self.world.delPlayer(player)

        return self.world.teams

    def pre_sync_randomise_teams(self, set_team_names=True):
        players = list(self.world.players)
        random.shuffle(players)
        group1, group2 = players[:len(players) // 2], players[len(players) // 2:]

        if set_team_names:
            name1 = get_preferred_team_name(group1, DEFAULT_TEAM_NAME_1)
            name2 = get_preferred_team_name(group2, DEFAULT_TEAM_NAME_2)
            if name2 == name1:
                if name1 == DEFAULT_TEAM_NAME_2:
                    name1 = DEFAULT_TEAM_NAME_1
                else:
                    name2 = DEFAULT_TEAM_NAME_2
        else:
            name1 = self.world.teams[0].teamName
            name2 = self.world.teams[1].teamName

        self.pre_sync_create_teams([(name1, group1), (name2, group2)])

    def pre_sync_create_hvm_teams(self):
        config = [(HUMANS_TEAM_NAME, self.world.players), (MACHINES_TEAM_NAME, ())]
        random.shuffle(config)
        self.pre_sync_create_teams(config)

    def pre_sync_create_preferred_teams(self):
        name1 = get_preferred_team_name(self.world.players, DEFAULT_TEAM_NAME_1)
        name2 = get_preferred_team_name(
            (p for p in self.world.players if p.suggested_team_name != name1),
            DEFAULT_TEAM_NAME_1 if name1 == DEFAULT_TEAM_NAME_2 else DEFAULT_TEAM_NAME_2)

        players1 = set()
        players2 = set()
        others = []
        for p in self.world.players:
            if p.suggested_team_name == name1:
                players1.add(p)
            elif p.suggested_team_name == name2:
                players2.add(p)
            else:
                others.append(p)

        random.shuffle(others)
        while others:
            p = others.pop()
            if len(players1) < len(players2):
                players1.add(p)
            elif len(players2) < len(players1):
                players2.add(p)
            else:
                random.choice([players1, players2]).add(p)

        self.pre_sync_create_teams([(name1, players1), (name2, players2)])

    def tearDownLevel(self):
        '''
        Called when a new level is selected, or the server terminates. This
        could be used to tear down event handlers which have been set up.
        '''
        while self.activeTriggers:
            trigger = self.activeTriggers.pop()
            try:
                trigger.deactivate()
            except Exception:
                log.exception('Error tearing down %s', trigger)

    async def run(self):
        '''
        Called when the level starts. By this point the Game and World have
        been completely instantiated. When this coroutine returns without any
        errors, the level is deemed to be completed, and the server will
        return to the lobby.

        :return: (succeeded, score) for when used as a tutorial
        '''
        await asyncio.get_event_loop().create_future()

    def findReasonPlayerCannotJoin(self, game, team_id, user, bot):
        '''
        Checks whether or not another player with the given details can join
        the game. By default, this will respect game.maxTotalPlayers, and
        game.maxPerTeam.

        @param game: the LocalGame object of the current game
        @param team_id: the id of the team that the player will join if
            permitted (calculated from call to getIdOfTeamToJoin().
        @param user: the authentication server user object if this game is
            being run on an authentication server, or None otherwise.
        @param bot: whether or not the requested join is from a bot.

        @return: None if the player can join the game, or a reason constant
            otherwise (e.g. GAME_FULL_REASON, or UNAUTHORISED_REASON).
        '''
        if len(game.world.players) >= game.maxTotalPlayers:
            return GAME_FULL_REASON

        if team_id != NEUTRAL_TEAM_ID:
            if sum(1 for p in game.world.players if p.teamId == team_id) >= game.maxPerTeam:
                return GAME_FULL_REASON

        return None

    def get_team_to_join(self, preferred_team, user, nick, bot):
        '''
        When a player asks to join a game, this method is called to
        decide which team to put them on, assuming that they are allowed
        to join.

        :param preferred_team: the team that the player would like to
            join if possible, or None if the player does not care
        :param user: the authentication server user object if this game
            is being run on an authentication server, or None otherwise.
        :param nick: the player's nick
        :param bot: whether or not the requested join is from a bot.

        :return: a team
        '''

        # Default team selection defers to bot manager
        if self.world.botManager:
            return self.world.botManager.getTeamToJoin(preferred_team, bot)
        if self.level_options.get_team_option(self) == FORCE_RANDOM_TEAMS:
            preferred_team = None
        return preferred_team_otherwise_smallest(preferred_team, self.world, include_bots=bot)

    def getWinner(self):
        '''
        Called when the server is saving the stats record for this game.
        Should return the team that has won, or None if the game has drawn.
        If the game is still in progress the Level may return None, or may
        return who is currently in the lead: this will only ever be used if
        the stats are saved half-way through the game and not saved at the
        end (e.g. server crashed).
        '''
        return self._winner

    @defer.inlineCallbacks
    def addBot(self, team, nick, botName='puppet', difficulty=DEFAULT_BOT_DIFFICULTY):
        '''
        Utility function that adds a bot to the game, but bypasses the call
        to findReasonPlayerCannotJoin(), because it is this level that has
        requested the join. By default, creates a PuppetBot which does
        nothing until told.
        '''

        game = self.world.game
        agent = yield game.addBot(
            botName, team=team, fromLevel=True, nick=nick, difficulty=difficulty)
        if agent and agent.player is None:
            yield agent.onPlayerSet.wait()

        defer.returnValue(agent)

    async def addControllableBot(self, team, nick, difficulty=DEFAULT_BOT_DIFFICULTY):
        '''
        Adds a PuppetBot to the game, which does nothing until told.
        '''
        game = self.world.game
        agent = await as_future(game.addBot(
            'puppet', team=team, fromLevel=True, nick=nick, forceLocal=True,
            difficulty=difficulty))
        if agent.player is None:
            await agent.onPlayerSet.wait_future()
        return BotController(agent)

    async def waitForHumans(self, number):
        '''
        Utility function that waits until at least number human players have
        joined the game, then returns a collection of the human players in
        the game.
        '''
        while True:
            humans = [p for p in self.world.players if p.join_complete and not p.bot]
            if len(humans) >= number:
                return humans

            await self.world.onPlayerAdded.wait_future()

    def sendPrivateChat(self, fromPlayer, toPlayer, text):
        fromPlayer.agent.sendRequest(
            ChatMsg(PRIVATE_CHAT, toPlayer.id, text=text.encode()))

    def playSound(self, filename):
        '''
        Utility function to play a sound on all clients. The sound file must
        exist on the client system.
        '''
        self.world.sendServerCommand(PlaySoundMsg(filename.encode('utf-8')))

    def setUserInfo(self, user_title, user_info, bot_goal):
        '''
        Utility function to set the tip that all players get to tell them
        their current objectives. Note that this function sets this tip
        globally for all players.
        '''
        self.world.uiOptions.setDefaultUserInfo(user_title, user_info, bot_goal)
        self.world.uiOptions.set(crowd_kind=bot_goal)
        self.world.sendServerCommand(
            UpdateGameInfoMsg.build(user_title, user_info, bot_goal))

    def notifyAll(self, message, error=False):
        '''
        Sends a notification message to all players and observers.
        '''
        self.world.sendServerCommand(
            ChatFromServerMsg(text=message.encode('utf-8'), error=error))

    def set_winners(self, winners):
        '''
        Utility function that shows the game over banner and blows a whistle.
        '''
        self.playSound('game-over-whistle.ogg')

        if any(not isinstance(w, (Team, Player)) for w in winners):
            raise TypeError('Winners must be players or teams')
        winning_teams = [w for w in winners if isinstance(w, Team)]
        winning_players = [w for w in winners if isinstance(w, Player)]

        if len(winning_teams) == 1:
            self._winner = winning_teams[0]
        else:
            self._winner = None

        if winning_teams and not winning_players:
            winning_players = None
        if winning_players and not winning_teams:
            winning_teams = None

        self.world.uiOptions.set(winning_teams=winning_teams, winning_players=winning_players)

    def setTeamName(self, team, name):
        self.world.sendServerCommand(SetTeamNameMsg(team.id, name.encode()))


class LobbySettings(object):
    def getAutoStartCountDown(self) -> Optional[float]:
        '''
        :return: Number of seconds before game will automatically start,
            or None for no auto start.
        '''
        raise NotImplementedError(
            '{}.getAutoStartCountDown'.format(self.__class__.__name__))

    def get_forced_size(self):
        raise NotImplementedError('{}.get_forced_size'.format(type(self).__name__))

    def get_forced_duration(self):
        raise NotImplementedError('{}.get_forced_duration'.format(type(self).__name__))

    def get_require_everyone_ready(self):
        raise NotImplementedError(f'{type(self).__name__}.get_require_everyone_ready')


class ServerLobbySettings(LobbySettings):
    def __init__(self, arenaManager):
        super(ServerLobbySettings, self).__init__()
        self.arenaManager = arenaManager

    def getAutoStartCountDown(self):
        record = self.arenaManager.getArenaRecord()
        result = record.autoStartCountDown
        if result < 0:
            return None
        return result

    def get_require_everyone_ready(self):
        record = self.arenaManager.getArenaRecord()
        return record.require_everyone_ready

    def get_forced_duration(self):
        record = self.arenaManager.getArenaRecord()
        return record.force_duration

    def get_forced_size(self):
        record = self.arenaManager.getArenaRecord()
        half_width = record.force_half_width
        height = record.force_height
        if half_width is not None and height is not None:
            return half_width, height
        return None


class LocalLobbySettings(LobbySettings):
    def getAutoStartCountDown(self):
        return None

    def get_forced_duration(self):
        return None

    def get_forced_size(self):
        return None

    def get_require_everyone_ready(self):
        return False


class LobbyLevel(Level):
    recordGame = False
    resetPlayerCoins = False
    levelName = 'Lobby'
    default_duration = None

    def __init__(self, lobbySettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if lobbySettings is None:
            lobbySettings = LocalLobbySettings()
        self.lobbySettings = lobbySettings
        self.require_everyone_ready = False

    def pre_sync_setup(self):
        # Keep the existing map, but make all players neutral
        self.pre_sync_create_teams(
            [(DEFAULT_TEAM_NAME_1, ()), (DEFAULT_TEAM_NAME_2, ())],
            neutral_players=self.world.players,
        )
        self.world.uiOptions.team_ids_humans_can_join = [NEUTRAL_TEAM_ID]

    async def run(self):
        MakeNewPlayersNeutralTrigger(self).activate()
        if not self.world.isOnceOnly():
            self.world.uiOptions.set(
                showReadyStates=True,
                allow_scenario_voting=True,
                team_name_suggestions=True,
                team_ids_humans_can_join=[NEUTRAL_TEAM_ID],
            )
            AddBotsForLobbyTrigger(self).activate()
            StartGameWhenReadyTrigger(self).activate()
            autoStartTime = self.lobbySettings.getAutoStartCountDown()
            self.require_everyone_ready = self.lobbySettings.get_require_everyone_ready()

            title = 'Lobby'
            userInfo = (
                '* Free for all',
                '* A match will start when enough players select "ready"',
            )
        else:
            title = 'Game Over'
            userInfo = (
                'Use the menu in the bottom left to leave game',
            )
            autoStartTime = None
            self.require_everyone_ready = False
        self.setUserInfo(title, userInfo, BOT_GOAL_NONE)

        # When most levels start, the previous level's winners are
        # cleared, but LobbyLevel is special-cased so that winners can
        # be displayed a little longer. Clear them after 20 seconds.
        asyncio.get_running_loop().call_later(20, self.clear_winners)

        self.world.abilities.set(zoneCaps=False, renaming=True)
        self.world.onChangeVoiceChatRooms([], [])

        if autoStartTime is not None:
            self.world.clock.startCountDown(autoStartTime)
            self.world.clock.propagateToClients()
            await self.world.clock.onZero.wait_future()
            self.start_some_game_now()

        # Lobby never finishes until it is canceled because a new level is
        # started.
        await asyncio.get_event_loop().create_future()

    def clear_winners(self):
        if self.world.scenarioManager.level is self:
            self.world.uiOptions.set(freeze_winners=False)

    def start_new_game_if_ready(self):
        players = [p for p in self.world.players if not p.bot]
        if not players:
            return
        ready_players = [p for p in players if p.readyToStart]
        ratio = 1 if self.require_everyone_ready else 0.7
        if len(ready_players) < ratio * len(players):
            return

        # Remove players who are not ready
        for p in list(self.world.players):
            if p.bot or not p.readyToStart:
                self.world.sendServerCommand(RemovePlayerMsg(p.id))

        level = get_preferred_scenario(self.world.game, ready_players)
        self.world.scenarioManager.startLevel(level)

    def start_some_game_now(self):
        level = get_preferred_scenario(
            self.world.game, [p for p in self.world.players if not p.bot])
        self.world.scenarioManager.startLevel(level)


class StandardLobbyLevel(LobbyLevel):
    def pre_sync_setup(self):
        super().pre_sync_setup()
        DefaultLobbyMap().apply(self)


def play_level(level, withLogging=True, **kwargs):
    '''
    For testing new Levels - launches Trosnoth in single player mode with
    the given level.
    '''
    import sys
    from trosnoth.run.solotest import launch_solo_game
    from trosnoth.welcome.common import initialise_qt_application

    initialise_qt_application()

    if withLogging:
        from trosnoth.utils.utils import initLogging
        initLogging()

    if '--profile' in sys.argv[1:]:
        import cProfile
        from trosnoth.utils.profiling import KCacheGrindOutputter
        prof = cProfile.Profile()

        try:
            prof.runcall(launch_solo_game, level=level, **kwargs)
        except (SystemExit, asyncio.CancelledError):
            pass
        finally:
            kg = KCacheGrindOutputter(prof)
            with open('{}.log'.format(level.__class__.__name__), 'w') as f:
                kg.output(f)
    else:
        try:
            launch_solo_game(level=level, **kwargs)
        except asyncio.CancelledError:
            pass


def run_bot_match(
        level, ai_class1, ai_class2,
        difficulty1=DEFAULT_BOT_DIFFICULTY, difficulty2=DEFAULT_BOT_DIFFICULTY,
        team_size=3, with_logging=True,
        **kwargs):
    from trosnoth.run.solotest import launch_solo_game

    if with_logging:
        from trosnoth.utils.utils import initLogging
        initLogging()

    bot_teams = (
        [(ai_class1, difficulty1)] * team_size,
        [(ai_class2, difficulty2)] * team_size,
    )
    launch_solo_game(level=level, bots_only=True, add_bots=bot_teams, **kwargs)
