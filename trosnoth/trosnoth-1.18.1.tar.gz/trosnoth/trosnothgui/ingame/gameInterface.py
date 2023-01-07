from dataclasses import dataclass
from functools import partial
import logging
import random
from typing import Optional

import pygame
from twisted.internet import defer

from trosnoth.const import (
    TROSBALL_DEATH_HIT, OPEN_CHAT, PRIVATE_CHAT, TEAM_CHAT,
    NOT_ENOUGH_COINS_REASON, PLAYER_DEAD_REASON, CANNOT_REACTIVATE_REASON,
    GAME_NOT_STARTED_REASON, TOO_CLOSE_TO_EDGE_REASON, PLAYER_HAS_TROSBALL_REASON,
    TOO_CLOSE_TO_ORB_REASON, NOT_IN_DARK_ZONE_REASON, INVALID_UPGRADE_REASON,
    DISABLED_UPGRADE_REASON, ALREADY_ALIVE_REASON, BE_PATIENT_REASON,
    ENEMY_ZONE_REASON, FROZEN_ZONE_REASON, BOMBER_DEATH_HIT,
    ACTION_CLEAR_UPGRADE, GAME_FULL_REASON, NICK_USED_REASON, BAD_NICK_REASON, UNAUTHORISED_REASON,
    USER_IN_GAME_REASON, ALREADY_JOINED_REASON,
)
from trosnoth.gui.framework import framework, hotkey, console
from trosnoth.gui.framework.declarative import (
    DeclarativeElement, Text, Rectangle,
    ComplexDeclarativeThing,
)
from trosnoth.gui.framework.elements import (
    TextElement, SolidRect,
)
from trosnoth.gui.framework.collapsebox import CollapseBox
from trosnoth.gui import keyboard
from trosnoth.gui.common import (
    Region, Screen, Location, Canvas, PaddedRegion, ScaledScalar,
)

from trosnoth.gamerecording.achievementlist import availableAchievements

from trosnoth.model.agent import ConcreteAgent, LocalPlayerSmoother
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID, NO_PLAYER
from trosnoth.model.upgrades import Shoxwave

from trosnoth.trosnothgui.ingame import viewmanager
from trosnoth.trosnothgui.ingame.achievementdisplay import (
    AchievementDisplay, RecentAchievements,
)
from trosnoth.trosnothgui.ingame.crowdnoise import CrowdNoiseGenerator
from trosnoth.trosnothgui.ingame.replayInterface import ViewControlInterface
from trosnoth.trosnothgui.ingame.joincontroller import JoinGameController
from trosnoth.trosnothgui.ingame.detailsInterface import DetailsInterface, LogMessage
from trosnoth.trosnothgui.ingame.playerInterface import PlayerInterface

from trosnoth import keymap

from trosnoth.data import user, getPath

from trosnoth.utils import globaldebug
from trosnoth.utils.event import Event
from trosnoth.utils.twist import WeakLoopingCall

from trosnoth.messages import (
    ChatFromServerMsg, ChatMsg, PingMsg,
    ShotFiredMsg, RespawnMsg, CannotRespawnMsg, TickMsg,
    CannotJoinMsg, AddPlayerMsg, PlayerHasUpgradeMsg, RemovePlayerMsg,
    PlayerCoinsSpentMsg, CannotBuyUpgradeMsg, ConnectionLostMsg,
    AchievementUnlockedMsg, SetPlayerTeamMsg, PlaySoundMsg,
    FireShoxwaveMsg, AwardPlayerCoinMsg,
    PlayerHasTrosballMsg, SlowPingMsg, BuyAmmoMsg,
)
from trosnoth.utils.utils import console_locals

log = logging.getLogger(__name__)


class GameInterface(framework.CompoundElement, ConcreteAgent):
    '''Interface for when we are connected to a game.'''

    local_player_driver_class = LocalPlayerSmoother
    achievementDefs = availableAchievements

    def __init__(
            self, app, game, onDisconnectRequest=None,
            onConnectionLost=None, replay=False, authTag=0, spectate=False):
        super(GameInterface, self).__init__(app, game=game)
        self.localState.onShoxwave.addListener(self.localShoxwaveFired)
        self.localState.onGameInfoChanged.addListener(self.gameInfoChanged)
        self.world.onOpenChatReceived.addListener(self.openChat)
        self.world.onTeamChatReceived.addListener(self.teamChat)
        self.world.onReset.addListener(self.worldReset)
        self.world.onGrenadeExplosion.addListener(self.grenadeExploded)
        self.world.onTrosballExplosion.addListener(self.trosballExploded)
        self.world.onBomberExplosion.addListener(self.bomber_exploded)
        self.world.on_mine_explosion.addListener(self.mine_exploded)
        self.world.onZoneTagged.addListener(self.orb_tagged)
        self.world.uiOptions.onChange.addListener(self.uiOptionsChanged)
        self.world.elephant.on_transfer.addListener(self.elephant_transferred)
        self.world.juggernaut.on_transfer.addListener(self.juggernaut_transferred)
        self.timingsLoop = WeakLoopingCall(self, '_sendPing')
        self.crowd_noise = CrowdNoiseGenerator(app, self.world)

        self.current_boost_purchase = TeamBoostTransactionTracker(self)

        self.subscribedPlayers = set()
        self.recent_achievements = RecentAchievements()

        self.onDisconnectRequest = Event()
        if onDisconnectRequest is not None:
            self.onDisconnectRequest.addListener(onDisconnectRequest)

        self.onConnectionLost = Event()
        if onConnectionLost is not None:
            self.onConnectionLost.addListener(onConnectionLost)
        self.game = game

        self.keyMapping = keyboard.KeyboardMapping(keymap.default_game_keys)
        self.runningPlayerInterface = None
        self.updateKeyMapping()
        self.gameViewer = viewmanager.GameViewer(self.app, self, game, replay)
        if replay or spectate:
            self.joinController = None
        else:
            self.joinController = JoinGameController(self.app, self, self.game)
        self.detailsInterface = DetailsInterface(self.app, self)
        self.winnerMsg = WinnerMsg(app)
        self.timing_info = TimingInfo()
        self.gameInfoDisplay = GameInfoDisplay(
            app, self,
            Region(topleft=Screen(0.01, 0.05), size=Canvas(330, 200)))
        self.hotkeys = hotkey.Hotkeys(
            self.app, self.keyMapping, self.detailsInterface.doAction)
        self.terminal = None

        self.vcInterface = None
        if replay:
            self.vcInterface = ViewControlInterface(self.app, self)

        self.ready = False
        if self.joinController:
            defer.maybeDeferred(game.addAgent, self, authTag=authTag).addCallback(self.addedAgent)

        self.setElements()

        if spectate:
            self.spectate()

        self.timingsLoop.start(1, now=False)

    def _sendPing(self):
        for i in range(3):
            data = bytes([random.randrange(256)])
            if data not in self.localState.pings:
                self.sendRequest(PingMsg(data))
                break

        for i in range(3):
            data = bytes([random.randrange(256)])
            if data not in self.localState.slow_pings:
                self.sendRequest(SlowPingMsg(data))
                break

    def gameInfoChanged(self):
        self.gameInfoDisplay.refreshInfo()

    def addedAgent(self, result):
        self.ready = True
        if self.joinController:
            self.joinController.established_connection_to_game()

    def spectatorWantsToJoin(self):
        if self.runningPlayerInterface or not self.joinController:
            return
        self.joinController.spectator_requests_join()

    def sendRequest(self, msg):
        if not self.ready:
            # Not yet completely connected to game
            return
        super(GameInterface, self).sendRequest(msg)

    def worldReset(self, *args, **kwarsg):
        if self.ready and self.joinController:
            self.joinController.world_was_reset()
        self.gameViewer.reset()

    def updateKeyMapping(self):
        # Set up the keyboard mapping.
        try:
            # Try to load keyboard mappings from the user's personal settings.
            with open(getPath(user, 'keymap'), 'r') as f:
                config = f.read()
            self.keyMapping.load(config)
            if self.runningPlayerInterface:
                self.runningPlayerInterface.keyMappingUpdated()
        except IOError:
            pass

    @ConnectionLostMsg.handler
    def connectionLost(self, msg):
        self.cleanUp()
        if self.joinController:
            self.joinController.lost_connection_to_game()
        self.onConnectionLost.execute()

    def joined(self, player):
        '''Called when joining of game is successful.'''
        pygame.key.set_repeat()
        self.gameViewer.worldgui.overridePlayer(self.localState.player)
        self.runningPlayerInterface = pi = PlayerInterface(self.app, self)
        self.detailsInterface.setPlayer(pi.player)
        self.setElements()

        self.joinController.successfully_joined_game()
        self.gameViewer.leaderboard.update()

    def spectate(self):
        '''
        Called by join controller if user selects to only spectate.
        '''
        self.vcInterface = ViewControlInterface(self.app, self)
        self.setElements()

        # Regenerate leaderboard so names are clickable
        self.gameViewer.leaderboard.update()

        if self.joinController:
            self.joinController.now_spectating_game()

    def stop(self):
        super(GameInterface, self).stop()
        self.localState.onShoxwave.removeListener(self.localShoxwaveFired)
        self.localState.onGameInfoChanged.removeListener(self.gameInfoChanged)
        self.world.juggernaut.on_transfer.removeListener(self.juggernaut_transferred)
        self.world.elephant.on_transfer.removeListener(self.elephant_transferred)
        self.world.onOpenChatReceived.removeListener(self.openChat)
        self.world.onTeamChatReceived.removeListener(self.teamChat)
        self.world.onReset.removeListener(self.worldReset)
        self.world.onGrenadeExplosion.removeListener(self.grenadeExploded)
        self.world.onTrosballExplosion.removeListener(self.trosballExploded)
        self.world.onBomberExplosion.removeListener(self.bomber_exploded)
        self.world.on_mine_explosion.removeListener(self.mine_exploded)
        self.world.onZoneTagged.removeListener(self.orb_tagged)
        self.world.uiOptions.onChange.removeListener(self.uiOptionsChanged)
        self.timingsLoop.stop()
        self.gameViewer.stop()
        self.detailsInterface.stop()
        self.crowd_noise.stop()
        self.app.soundPlayer.stop_looping_sounds()
        if self.runningPlayerInterface is not None:
            self.runningPlayerInterface.stop()

    def setElements(self):
        spectate = replay = False
        if self.runningPlayerInterface:
            self.elements = [
                self.gameViewer, self.runningPlayerInterface,
                self.gameInfoDisplay, self.hotkeys, self.detailsInterface,
                DeclarativeElement(self.app, (0, 0.65), MaybeShowUpscaleMessage()),
                DeclarativeElement(self.app, (0, 0.725), AchievementDisplay(
                    self.recent_achievements, self.detailsInterface.player)),
                self.winnerMsg,
            ]
        else:
            self.elements = [
                self.gameViewer, self.gameInfoDisplay,
                self.hotkeys, self.detailsInterface,
                self.winnerMsg]
            if self.vcInterface is not None:
                self.elements.insert(2, self.vcInterface)

            if self.joinController:
                spectate = True
            else:
                replay = True

        self.elements.append(
            DeclarativeElement(self.app, (-0.4, 1), TimingDisplay(self, self.timing_info)))

        self.detailsInterface.menuManager.setMode(
            spectate=spectate, replay=replay)

    def is_spectating(self):
        '''
        :return: True for replays or observer mode.
        '''
        return not self.runningPlayerInterface

    def toggleTerminal(self):
        if self.terminal is None:
            locs = {'app': self.app}
            try:
                locs.update(console_locals.get())
            except LookupError:
                pass
            self.terminal = console.TrosnothInteractiveConsole(
                self.app,
                self.app.screenManager.fonts.consoleFont,
                Region(size=Screen(1, 0.4), bottomright=Screen(1, 1)),
                locals=locs)
            self.terminal.interact().addCallback(self._terminalQuit)

        from trosnoth.utils.utils import timeNow
        if self.terminal in self.elements:
            if timeNow() > self._termWaitTime:
                self.elements.remove(self.terminal)
        else:
            self._termWaitTime = timeNow() + 0.1
            self.elements.append(self.terminal)
            self.setFocus(self.terminal)

    def _terminalQuit(self, result):
        if self.terminal in self.elements:
            self.elements.remove(self.terminal)
        self.terminal = None

    def disconnect(self):
        self.cleanUp()
        self.onDisconnectRequest.execute()

    def joinGame(self, nick, head, team, timeout=10):
        if team is None:
            teamId = NEUTRAL_TEAM_ID
        else:
            teamId = team.id

        self.sendJoinRequest(teamId, nick, head)

    def setPlayer(self, player):
        if not player:
            self.gameViewer.worldgui.removeOverride()
            self.lostPlayer()

        super(GameInterface, self).setPlayer(player)

        if player:
            if __debug__ and globaldebug.enabled:
                globaldebug.localPlayerId = player.id

            self.joined(player)

    @CannotJoinMsg.handler
    def joinFailed(self, msg):
        args = {}
        if msg.reasonId == GAME_FULL_REASON:
            message = LogMessage.GAME_FULL
        elif msg.reasonId == NICK_USED_REASON:
            message = LogMessage.NICK_IN_USE
            self.joinController.user_should_try_a_different_name()
        elif msg.reasonId == BAD_NICK_REASON:
            message = LogMessage.BAD_NICK
            self.joinController.user_should_try_a_different_name()
        elif msg.reasonId == UNAUTHORISED_REASON:
            message = LogMessage.UNAUTHORISED
        elif msg.reasonId == USER_IN_GAME_REASON:
            message = LogMessage.ALREADY_JOINED
        elif msg.reasonId == ALREADY_JOINED_REASON:
            message = LogMessage.ALREADY_JOINED
        else:
            # Unknown reason.
            message = LogMessage.JOIN_FAILED
            args = dict(code=msg.reasonId)
            message = 'Join failed (%r)' % (msg.reasonId,)

        self.detailsInterface.new_message(message, **args)
        self.detailsInterface.newChat(message.format(**args), None)

    def cleanUp(self):
        if self.gameViewer.timerBar is not None:
            self.gameViewer.timerBar = None
        pygame.key.set_repeat(300, 30)

    def uiOptionsChanged(self):
        if self.world.uiOptions.freeze_winners:
            return
        winning_teams = self.world.uiOptions.winning_teams
        winning_players = self.world.uiOptions.winning_players
        if winning_teams is None and winning_players is None:
            self.winnerMsg.hide()
        elif winning_teams:
            colour = winning_teams[0].shade(0.5, 1)
            if len(winning_teams) == 1:
                self.winnerMsg.show('Winner: {}'.format(winning_teams[0].teamName), colour)
            else:
                self.winnerMsg.show(
                    'Winners: {}'.format(', '.join(t.teamName for t in winning_teams)), colour)
        elif winning_players:
            team = winning_players[0].team
            colour = team.shade(0.5, 1) if team else (128, 128, 128)
            if len(winning_players) == 1:
                self.winnerMsg.show('Winner: {}'.format(winning_players[0].nick), colour)
            else:
                self.winnerMsg.show(
                    'Winners: {}'.format(', '.join(p.nick for p in winning_players)), colour)
        else:
            self.winnerMsg.show('Game drawn', (128, 128, 128))

    @PlayerCoinsSpentMsg.handler
    def discard(self, msg):
        pass

    @AwardPlayerCoinMsg.handler
    def playerAwardedCoin(self, msg):
        if not self.localState.player:
            return
        if msg.sound and msg.playerId == self.localState.player.id:
            self.play_sound('gotCoin')

    def elephant_transferred(self, old_possessor, new_possessor):
        if new_possessor:
            self.detailsInterface.new_message(
                LogMessage.ELEPHANT_GAINED,
                player=new_possessor.nick,
                elephant=self.world.uiOptions.elephantName,
            )

    def juggernaut_transferred(self, old_possessor, new_possessor):
        if new_possessor:
            self.detailsInterface.new_message(
                LogMessage.NEW_JUGGERNAUT, player=new_possessor.nick)

    @PlayerHasTrosballMsg.handler
    def gotTrosball(self, msg, _lastTrosballPlayer=[None]):
        player = self.world.playerWithId.get(msg.playerId)

        if player != _lastTrosballPlayer[0]:
            _lastTrosballPlayer[0] = player
            if player is None:
                self.detailsInterface.new_message(LogMessage.TROSBALL_DROPPED)
            else:
                self.detailsInterface.new_message(LogMessage.TROBSALL_GAINED, player=player.nick)

    @AddPlayerMsg.handler
    def addPlayer(self, msg):
        player = self.world.getPlayer(msg.playerId)
        if player and player not in self.subscribedPlayers:
            self.subscribedPlayers.add(player)
            team_name = str(player.team) if player.team else self.world.rogueTeamName
            self.detailsInterface.new_message(
                LogMessage.PLAYER_JOINED, player=player.nick, team=team_name)
            player.onDied.addListener(partial(self.player_died, player))

    @SetPlayerTeamMsg.handler
    def changeTeam(self, msg):
        self.defaultHandler(msg)    # Make sure the local player changes team
        player = self.world.getPlayer(msg.playerId)
        if player:
            self.detailsInterface.new_message(
                LogMessage.PLAYER_JOINED,
                player=player.nick, team=self.world.getTeamName(msg.teamId))

    @RemovePlayerMsg.handler
    def handle_RemovePlayerMsg(self, msg):
        player = self.world.getPlayer(msg.playerId)
        if player:
            self.detailsInterface.new_message(LogMessage.PLAYER_LEFT, player=player.nick)
            self.subscribedPlayers.discard(player)

    def lostPlayer(self):
        if self.runningPlayerInterface:
            self.runningPlayerInterface.stop()
        self.runningPlayerInterface = None
        self.detailsInterface.setPlayer(None)
        self.setElements()

    @CannotBuyUpgradeMsg.handler
    def notEnoughCoins(self, msg):
        if msg.reasonId == NOT_ENOUGH_COINS_REASON:
            message = LogMessage.NOT_ENOUGH_COINS
        elif msg.reasonId == CANNOT_REACTIVATE_REASON:
            message = LogMessage.CANNOT_REACTIVATE
        elif msg.reasonId == PLAYER_DEAD_REASON:
            message = LogMessage.NO_UPGRADE_WHILE_DEAD
        elif msg.reasonId == GAME_NOT_STARTED_REASON:
            message = LogMessage.UPGRADES_DISABLED
        elif msg.reasonId == PLAYER_HAS_TROSBALL_REASON:
            message = LogMessage.TROSBALL_EXCLUDES_UPGRADES
        elif msg.reasonId == TOO_CLOSE_TO_EDGE_REASON:
            message = LogMessage.TOO_CLOSE_TO_EDGE
        elif msg.reasonId == TOO_CLOSE_TO_ORB_REASON:
            message = LogMessage.TOO_CLOSE_TO_ORB
        elif msg.reasonId == NOT_IN_DARK_ZONE_REASON:
            message = LogMessage.NOT_IN_DARK_ZONE
        elif msg.reasonId == INVALID_UPGRADE_REASON:
            message = LogMessage.UNRECOGNISED_UPGRADE
        elif msg.reasonId == DISABLED_UPGRADE_REASON:
            message = LogMessage.UPGRADE_DISABLED
        else:
            message = LogMessage.UPGRADE_UNAVAILABLE
        self.detailsInterface.new_message(message)
        self.defaultHandler(msg)

    @PlayerHasUpgradeMsg.handler
    def gotUpgrade(self, msg):
        player = self.world.getPlayer(msg.playerId)
        if player:
            self.detailsInterface.upgradeUsed(player, msg.upgradeType)
            upgradeClass = self.world.getUpgradeType(msg.upgradeType)
            existing = player.items.get(upgradeClass)
            if not existing:
                if (self.detailsInterface.player is None or
                        self.detailsInterface.player.isFriendsWith(player)):
                    self.play_sound('buyUpgrade')

        self.defaultHandler(msg)

    @ChatFromServerMsg.handler
    def gotChatFromServer(self, msg):
        self.detailsInterface.new_message(
            LogMessage.SERVER_CHAT, message=msg.text.decode('utf-8'))

    def orb_tagged(self, zone, player, previous_owner):
        zone_label = zone.defn.label

        if player is None:
            self.play_sound('orb-power-down', zone.orb_pos)
        else:
            nick = player.nick
            self.detailsInterface.new_message(LogMessage.CAPPED, player=nick, zone=zone_label)
            self.play_sound('orb-change' if previous_owner else 'orb-power-up', zone.orb_pos)

    def player_died(self, target, killer, death_type):
        if death_type == TROSBALL_DEATH_HIT:
            self.detailsInterface.new_message(LogMessage.TROSBALL_DEATH, player=target.nick)
        elif death_type == BOMBER_DEATH_HIT:
            self.detailsInterface.new_message(LogMessage.BOMBER_DEATH, player=target.nick)
            thisPlayer = self.detailsInterface.player
            if thisPlayer and target.id == thisPlayer.id:
                self.detailsInterface.doAction(ACTION_CLEAR_UPGRADE)
        else:
            self.play_sound('killed-by-shot', pos=target.pos)
            if killer is None:
                self.detailsInterface.new_message(LogMessage.PLAYER_DIED, target=target.nick)
            else:
                self.detailsInterface.new_message(
                    LogMessage.PLAYER_KILLED, killer=killer.nick, target=target.nick)

    @RespawnMsg.handler
    def playerRespawn(self, msg):
        if msg.phantom:
            if self.player and msg.playerId == self.player.id:
                self.detailsInterface.new_message(LogMessage.TEMPORAL_ANOMALY)
                self.gameViewer.worldgui.add_temporal_anomaly(self.player, self.localState.player)
            return
        player = self.world.getPlayer(msg.playerId)
        if player:
            self.detailsInterface.new_message(LogMessage.RESPAWNED, player=player.nick)

    @CannotRespawnMsg.handler
    def respawnFailed(self, msg):
        if msg.reasonId == GAME_NOT_STARTED_REASON:
            message = LogMessage.GAME_NOT_STARTED
        elif msg.reasonId == ALREADY_ALIVE_REASON:
            message = LogMessage.ALREADY_ALIVE
        elif msg.reasonId == BE_PATIENT_REASON:
            message = LogMessage.BE_PATIENT
        elif msg.reasonId == ENEMY_ZONE_REASON:
            message = LogMessage.MOVE_TO_FRIENDLY_ZONE
        elif msg.reasonId == FROZEN_ZONE_REASON:
            message = LogMessage.ZONE_FROZEN
        else:
            message = LogMessage.CANNOT_RESPAWN
        self.detailsInterface.new_message(message)

    def sendPrivateChat(self, player, targetId, text):
        self.sendRequest(ChatMsg(PRIVATE_CHAT, targetId, text=text.encode()))

    def sendTeamChat(self, player, text):
        self.sendRequest(
            ChatMsg(TEAM_CHAT, player.teamId, text=text.encode()))

    def sendPublicChat(self, player, text):
        self.sendRequest(ChatMsg(OPEN_CHAT, text=text.encode()))

    def openChat(self, text, sender):
        text = ': ' + text
        self.detailsInterface.newChat(text, sender)

    def teamChat(self, team, text, sender):
        player = self.detailsInterface.player
        if player and player.isFriendsWithTeam(team):
            text = ' (team): ' + text
            self.detailsInterface.newChat(text, sender)

    @AchievementUnlockedMsg.handler
    def achievementUnlocked(self, msg):
        self.recent_achievements.add(msg)
        player = self.world.getPlayer(msg.playerId)
        if not player:
            return

        achievementName = self.achievementDefs.getAchievementDetails(
            msg.achievementId)[0]
        self.detailsInterface.new_message(
            LogMessage.ACHIEVEMENT, player=player.nick, achievement=achievementName)

    @ShotFiredMsg.handler
    def shotFired(self, msg):
        self.defaultHandler(msg)
        try:
            shot = self.world.getShot(msg.shot_id)
        except KeyError:
            return

        self.play_sound(shot.gun_type.firing_sound, pos=shot.pos)

    def grenadeExploded(self, pos, radius):
        self.gameViewer.worldgui.addExplosion(pos)
        self.play_sound('explodeGrenade', pos=pos)

    def trosballExploded(self, player):
        self.gameViewer.worldgui.addTrosballExplosion(player.pos)
        self.play_sound('explodeGrenade', pos=player.pos)

    def bomber_exploded(self, player):
        self.gameViewer.worldgui.add_bomber_explosion(player)
        self.play_sound('bomber-explode', pos=player.pos)

    def shot_rebounded(self, pos):
        self.play_sound('shot-rebound', pos=pos)

    @FireShoxwaveMsg.handler
    def shoxwaveExplosion(self, msg):
        self.defaultHandler(msg)
        self.play_sound(Shoxwave.firing_sound, pos=(msg.xpos, msg.ypos))
        localPlayer = self.localState.player
        if localPlayer and msg.playerId == localPlayer.id:
            return
        self.gameViewer.worldgui.addShoxwaveExplosion((msg.xpos, msg.ypos))

    def localShoxwaveFired(self):
        localPlayer = self.localState.player
        self.gameViewer.worldgui.addShoxwaveExplosion(localPlayer.pos)

    def mine_exploded(self, pos):
        self.gameViewer.worldgui.add_mine_explosion(pos)
        self.play_sound('explodeGrenade', pos=pos)

    def play_sound(self, action, pos=None):
        self.app.soundPlayer.play(action, self.gameViewer.viewManager.getTargetPoint(), pos)

    @PlaySoundMsg.handler
    def playSoundFromServerCommand(self, msg):
        self.app.soundPlayer.playFromServerCommand(
            msg.filename.decode('utf-8'))

    @TickMsg.handler
    def handle_TickMsg(self, msg):
        super(GameInterface, self).handle_TickMsg(msg)
        self.timing_info.seen_tick()

        looping_sound_positions = {}
        for shot in self.world.shots:
            if sound_name := shot.gun_type.looping_sound:
                looping_sound_positions.setdefault(sound_name, []).append(shot.pos)
        self.app.soundPlayer.set_looping_sound_positions(
            self.gameViewer.viewManager.getTargetPoint(), looping_sound_positions)

        if __debug__ and globaldebug.enabled:
            globaldebug.tick_logger.game_interface_saw_tick(msg.tickId)
            if globaldebug.debug_key_screenshots and globaldebug.debugKey:
                log.error('Saving screenshot info…')
                import pprint
                with open('screenshots.txt', 'a') as f:
                    try:
                        from trosnoth.tools.screenshots import get_screenshot_data
                        pprint.pprint(get_screenshot_data(self), f)
                    except Exception:
                        log.exception('Error saving screenshot info')

    @BuyAmmoMsg.handler
    def handle_BuyAmmoMsg(self, msg):
        if self.player and self.player.id == msg.player_id:
            self.detailsInterface.player_bought_ammo(msg.gun_type)


@dataclass(frozen=True)
class MaybeShowUpscaleMessage(ComplexDeclarativeThing):
    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        display = frame.app.settings.display
        if display.upscale:
            return
        if display.size[1] < display.max_viewport_height * 1.06:
            return
        frame.add(UpscaleMessage())


@dataclass(frozen=True)
class UpscaleMessage(ComplexDeclarativeThing):
    def draw(self, frame, state):
        frame.add(Rectangle(
            width=600,
            height=50,
            colour=(208, 200, 192, 192),
        ))
        frame.add(Text(
            'For a better experience on ultra high definition displays,',
            height=20,
            font='Junction.ttf',
            text_colour=(0, 0, 0),
            max_width=580,
            align=Text.A_center,
        ), at=(0, 0))
        frame.add(Text(
            'consider enabling up-scaling in display settings',
            height=20,
            font='Junction.ttf',
            text_colour=(0, 0, 0),
            max_width=580,
            align=Text.A_center,
        ), at=(0, 20))


class TimingInfo():
    def __init__(self):
        self.frames_seen = 0
        self.ticks_seen = 0
        self.time_passed = 0.

    def reset(self):
        self.frames_seen = 0
        self.ticks_seen = 0
        self.time_passed = 0.

    def seen_tick(self):
        self.ticks_seen += 1

    def seen_frame(self, delta_t):
        self.time_passed += delta_t
        self.frames_seen += 1


class TeamBoostTransactionTracker:
    def __init__(self, interface):
        self.coins = 0
        self.interface = interface
        self.boost_class = None

    def start_boost_purchase(self, boost_class):
        self.boost_class = boost_class
        if self.interface.player.team.boosts.get(boost_class):
            self.coins = 50
        else:
            self.coins = boost_class.deposit_cost
        self.constrain_coins()

    def contribute(self, delta):
        self.coins += delta
        self.constrain_coins()

    def constrain_coins(self):
        boost = self.interface.player.team.boosts.get(self.boost_class)
        if boost:
            remaining = boost.remaining_cost
        else:
            remaining = self.boost_class.total_cost
        self.coins = min(self.coins, self.interface.player.coins, remaining)

    def get_total_contributed_coins(self):
        boost = self.interface.player.team.boosts.get(self.boost_class)
        self.constrain_coins()
        if boost:
            progress = boost.total_cost - boost.remaining_cost + self.coins
        else:
            progress = self.coins
        return progress

    def get_boost_progress_ratio(self):
        return self.get_total_contributed_coins() / self.boost_class.total_cost

    def complete_purchase(self):
        coins = self.coins
        self.interface.please_contribute_to_team_boost(self.boost_class, round(coins))

        self.coins = 0
        self.boost_class = None


@dataclass(frozen=True)
class TimingDisplay(ComplexDeclarativeThing):
    interface: GameInterface
    info: TimingInfo

    def build_state(self, renderer):
        return {'fps': None, 'tps': None}

    def draw(self, frame, state):
        if not frame.app.settings.display.show_timings:
            return
        self.info.seen_frame(frame.delta_t)
        if self.info.time_passed > 3:
            state['fps'] = self.info.frames_seen / self.info.time_passed
            state['tps'] = self.info.ticks_seen / self.info.time_passed
            self.info.reset()

        frame.add(TimingPanel(
            fps=state['fps'],
            tps=state['tps'],
            ping=self.interface.localState.lastPingTime,
            smooth=self.interface.localState.slow_ping_time,
            jitter=self.interface.app.jitterLogger.jitter,
        ))


@dataclass(frozen=True)
class TimingPanel(ComplexDeclarativeThing):
    fps: Optional[float]
    tps: Optional[float]
    ping: Optional[float]
    smooth: Optional[float]
    jitter: Optional[float]

    def draw(self, frame, state):
        lines = []
        if self.fps is not None:
            lines.append(f'FPS: {self.fps:.1f}')
        if self.tps is not None:
            lines.append(f'TPS: {self.tps:.1f}')
        if self.ping is not None:
            lines.append(f'Ping: {round(1000 * self.ping)} ms')
        if self.smooth is not None:
            lines.append(f'Smooth: {round(1000 * self.smooth)} ms')
        if self.jitter is not None:
            lines.append(f'Jitter: {round(1000 * self.jitter)} ms')

        height = 10 * len(lines) + 6
        frame.add(
            Rectangle(
                width=84,
                height=height,
                colour=(255, 255, 255, 128),
            ),
            at=(0, -height / 2)
        )

        y = 4 - height
        for line in lines:
            y += 10
            frame.add(
                Text(
                    line,
                    height=10,
                    font='Junction.ttf',
                    text_colour=(0, 0, 0),
                    max_width=80,
                    align=Text.A_left,
                ),
                at=(-40, y),
            )


class GameInfoDisplay(CollapseBox):
    def __init__(self, app, gameInterface, region):
        colours = app.theme.colours
        fonts = app.screenManager.fonts
        self.interface = gameInterface
        super(GameInfoDisplay, self).__init__(
            app,
            region=region,
            titleFont=fonts.gameInfoTitleFont,
            font=fonts.gameInfoFont,
            titleColour=colours.gameInfoTitle,
            hvrColour=colours.gameInfoHover,
            colour=colours.gameInfoColour,
            backColour=colours.gameInfoBackColour,
            title='',
        )
        self.refreshInfo()

    def refreshInfo(self):
        localState = self.interface.localState
        self.setInfo(localState.userInfo, localState.userTitle)

    def get_screenshot_scenario(self):
        local_state = self.interface.localState
        user_info = list(local_state.userInfo)
        if self.hidden:
            user_info = []
        if (user_title := local_state.userTitle) or user_info:
            return [user_title] + user_info
        return []

    def restore_screenshot_scenario(self, data):
        local_state = self.interface.localState
        local_state.userTitle = data[0] if data else ''
        local_state.userInfo = tuple(data[1:])

        self.refreshInfo()
        self.hidden = not local_state.userInfo

        # Skip any resize animation and just jump to the intended size
        self.rect.height = self.targetRect.height
        self.updateElements()


class WinnerMsg(framework.CompoundElement):
    def __init__(self, app):
        super(WinnerMsg, self).__init__(app)
        self.winnerMsg = TextElement(
            app, '', app.screenManager.fonts.winMessageFont,
            Location(Screen(0.5, 0.14), 'midtop'), (64, 64, 64))
        self.background = SolidRect(
            app, (128, 128, 128), 150,
            PaddedRegion(self.winnerMsg, ScaledScalar(15)))
        self.elements = []

    def show(self, text, colour):
        self.winnerMsg.setText(text)
        self.background.colour = colour
        self.background.border = colour
        self.background.refresh()
        self.elements = [self.background, self.winnerMsg]

    def hide(self):
        self.elements = []
