# Trosnoth (Ubertweak Platform Game)
# Copyright (C) Joshua D Bartlett
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import asyncio
from configparser import ConfigParser

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QTableWidgetItem

from trosnoth import data
from trosnoth.const import BOT_DIFFICULTY_EASY, BOT_DIFFICULTY_HARD, DEFAULT_BOT_DIFFICULTY
from trosnoth.gui.app import UserClosedPygameWindow
from trosnoth.levels.base import LevelOptions
from trosnoth.model.map import ZoneLayout, ZoneStep
from trosnoth.run.solotest import launch_solo_game_async, SoloGameClosed
from trosnoth.triggers.deathmatch import make_small_circles_layout
from trosnoth.utils.utils import (
    UIScreenRunner, format_numbers,
)
from trosnoth.welcome.nonqt import async_callback, run_callback_in_async_loop

TUTORIALS_PROGRESS_FILE = data.user_path / 'tutorials.ini'
COMPLETED_KEY = 'completed'
BEST_SCORE_KEY = 'best_score'

scenarios = []


class TutorialsScreen:
    def __init__(self, parent):
        self.async_manager = parent.async_manager   # Allows async callbacks

        self.parent = parent
        self.screen_runner = UIScreenRunner()
        self.window = window = parent.window
        self.main_stack = window.findChild(QWidget, 'main_stack')
        self.tutorials_page = window.findChild(QWidget, 'tutorials_page')

        self.tutorials_table = None
        self.tick_font = None
        self.progress = None

        window.findChild(QWidget, 'tutorials_back_button').clicked.connect(
            run_callback_in_async_loop(self.back_clicked))
        window.findChild(QWidget, 'tutorials_play_button').clicked.connect(
            run_callback_in_async_loop(self.play_scenario))

        self.hard_mode_checkbox = window.findChild(QWidget, 'hard_mode_checkbox')
        self.tutorials_table = window.findChild(QWidget, 'tutorials_table')
        self.tutorials_table.horizontalHeader().sectionResized.connect(
            run_callback_in_async_loop(self.table_section_resized))
        self.tutorials_table.cellDoubleClicked.connect(
            run_callback_in_async_loop(self.play_scenario))

        self.tutorials_table.setColumnWidth(0, 75)
        self.tutorials_table.setColumnWidth(1, 250)

        title_font = QFont(self.tutorials_table.item(0, 1).font())
        title_font.setPixelSize(20)
        description_font = QFont(self.tutorials_table.item(0, 2).font())
        description_font.setPixelSize(16)
        self.tick_font = QFont(self.tutorials_table.item(0, 2).font())
        self.tick_font.setPixelSize(40)

        self.tutorials_table.setRowCount(len(scenarios))
        for i, scenario in enumerate(scenarios):
            item = QTableWidgetItem(scenario.name)
            item.setFont(title_font)
            self.tutorials_table.setItem(i, 1, item)
            item = QTableWidgetItem(scenario.description)
            item.setFont(description_font)
            self.tutorials_table.setItem(i, 2, item)

        # For some reason, calling resizeRowsToContents right here adds
        # padding to the cells, but using call_soon() does not, and is
        # therefore consistent with what happens on section resize.
        asyncio.get_event_loop().call_soon(self.table_section_resized)

    def update_progress_indicators(self):
        self.reload_progress()
        best_option_selected = False
        for i, scenario in enumerate(scenarios):
            if self.is_scenario_completed(scenario):
                item = QTableWidgetItem('✓')
                item.setFont(self.tick_font)
                self.tutorials_table.setItem(i, 0, item)
            elif not best_option_selected:
                best_option_selected = True
                self.tutorials_table.setCurrentCell(i, 1)

        if not best_option_selected:
            # Select the first scenario in the list if all are completed
            self.tutorials_table.setCurrentCell(0, 1)

    async def run(self):
        previous_page_widget = self.main_stack.currentWidget()
        try:
            self.update_progress_indicators()
            self.main_stack.setCurrentWidget(self.tutorials_page)
            return await self.screen_runner.run()
        finally:
            self.main_stack.setCurrentWidget(previous_page_widget)

    def back_clicked(self):
        self.screen_runner.done(None)

    def reload_progress(self):
        self.progress = ConfigParser(interpolation=None)
        for scenario in scenarios:
            self.progress.add_section(scenario().get_section_name())
        self.progress.read(TUTORIALS_PROGRESS_FILE)

    def is_scenario_completed(self, scenario):
        return self.progress[scenario().get_section_name()].getboolean(COMPLETED_KEY, False)

    def get_scenario_best_score(self, scenario):
        return self.progress[scenario().get_section_name()].getfloat(BEST_SCORE_KEY, fallback=None)

    @async_callback
    async def play_scenario(self, *args):
        current_row = self.tutorials_table.currentRow()
        scenario = scenarios[current_row]
        previous_best_score = self.get_scenario_best_score(scenario)
        hard_mode = self.hard_mode_checkbox.isChecked()

        if scenario.intro and not self.is_scenario_completed(scenario):
            ok = await self.parent.message_viewer.run(scenario.intro)
            if not ok:
                return

        play_again = True
        while play_again:
            try:
                succeeded, score = await scenario().run(hard_mode=hard_mode)
            except (UserClosedPygameWindow, SoloGameClosed):
                break

            if not succeeded:
                play_again = await self.display_play_again_window(
                    scenario.name, previous_best_score, None)
                continue

            if score is None:
                self.scenario_now_completed(current_row, None)
                break

            best_score = score if previous_best_score is None else max(previous_best_score, score)
            self.scenario_now_completed(current_row, best_score)

            play_again = await self.display_play_again_window(
                scenario.name, previous_best_score, score)
            previous_best_score = best_score

    def scenario_now_completed(self, row_index, best_score=None):
        scenario = scenarios[row_index]

        self.reload_progress()
        section_name = scenario().get_section_name()
        self.progress[section_name][COMPLETED_KEY] = '1'
        if best_score is not None:
            self.progress[section_name][BEST_SCORE_KEY] = str(best_score)

        with open(TUTORIALS_PROGRESS_FILE, 'w') as f:
            self.progress.write(f)

        item = QTableWidgetItem('✓')
        item.setFont(self.tick_font)
        self.tutorials_table.setItem(row_index, 0, item)

    def table_section_resized(self, *args):
        PADDING = 20
        self.tutorials_table.resizeRowsToContents()
        for i in range(self.tutorials_table.rowCount()):
            self.tutorials_table.setRowHeight(i, self.tutorials_table.rowHeight(i) + PADDING)

    async def display_play_again_window(self, level_name, best_score, this_score):
        '''
        :param level_name: the name of the scenario
        :param best_score: None if there is no previous best score
        :param this_score: None if level was failed, otherwise best score
        '''
        if this_score is None:
            # Scenario failed
            if best_score is None:
                message = 'Scenario failed.'
            else:
                best_string, = format_numbers([best_score])
                message = f'Scenario failed.\n\nHigh score: {best_string}'
        elif best_score is None:
            this_string, = format_numbers([this_score])
            message = f'Scenario complete.\n\nScore: {this_string}\nOld high score: —'
        else:
            this_string, best_string = format_numbers([this_score, best_score])
            if this_score > best_score:
                message = (
                    f'Congratulations! You got a new high score!\n\n'
                    f'Score: {this_string}\nOld high score: {best_string}'
                )
            elif this_score == best_score:
                message = (
                    f'Congratulations! You equalled your high score.\n\n'
                    f'Score: {this_string}\nHigh score: {best_string}'
                )
            else:
                message = f'Scenario complete.\n\nScore: {this_string}\nHigh score: {best_string}'

        message += f'\n\nPlay {level_name} again?'
        result = await self.parent.message_viewer.run(message, ok_text='play again')
        return result


class TutorialScenario:
    name = NotImplemented
    description = NotImplemented
    section_name = None
    intro = None

    def get_section_name(self):
        if self.section_name is None:
            return type(self).__name__

    async def run(self, hard_mode=False):
        '''
        :return: (completed, score)
        '''
        raise NotImplementedError()


@scenarios.append
class CatPigeon(TutorialScenario):
    name = 'Cat among pigeons'
    description = 'Get used to the game controls while shooting bots who don’t shoot back.'
    intro = (
        'Default controls:\n\n'

        'W, A, S, D ~ move player\n'
        'Left mouse ~ shoot\n'
        'Right mouse ~ grappling hook\n\n'

        'Controls can be configured in settings.\n\n'

        'In this scenario, enemy bots will not attack you. Shoot as many of them as you can in '
        'the time limit.'
    )

    async def run(self, hard_mode=False):
        from trosnoth.levels.catpigeon import CatPigeonLevel

        return await launch_solo_game_async(
            game_prefix='Cat among pigeons',
            level=CatPigeonLevel(
                level_options=LevelOptions(duration=120), map_builder=self.build_map),
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else DEFAULT_BOT_DIFFICULTY,
        )

    def build_map(self):
        zones = ZoneLayout()

        zones.setZoneOwner(zones.firstLocation, 0, dark=True)
        zones.connectZone(zones.firstLocation, ZoneStep.SOUTH, ownerIndex=1, dark=False)

        return zones.createMapLayout(autoOwner=False)


@scenarios.append
class OrbChase(TutorialScenario):
    name = 'Orb chase'
    description = 'Improve your map navigation speed as you try to reach the target orb.'
    intro = (
        'Every time your player touches a red orb in this scenario, you gain one point and a '
        'different orb becomes red.\n\n'

        'Look at the minimap to work out the best route to the red orb.\n\n'

        'You begin this scenario as a ghost. Move the ghost using the mouse. To respawn, move to '
        'a blue room and left click the mouse.\n\n'
    )

    async def run(self, hard_mode=False):
        from trosnoth.levels.orbchase import OrbChaseLevel

        return await launch_solo_game_async(
            game_prefix='Orb chase',
            level=OrbChaseLevel(level_options=LevelOptions(duration=180)),
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else DEFAULT_BOT_DIFFICULTY,
        )


@scenarios.append
class OneOnOneFreeForAll(TutorialScenario):
    name = '1v1 free-for-all'
    description = 'Practise dogfighting with one enemy bot.'
    intro = (
        'In this scenario you will fight against a single enemy bot.\n\n'

        'The winner is the player with the most kills when the timer runs out.\n\n'

        'Every kill earns you money. You can use your money to buy items and weapons. Press tab '
        'to select an item, then press space bar to use it.'
    )

    async def run(self, hard_mode=False):
        from trosnoth.levels.freeforall import FreeForAllLevel

        return await launch_solo_game_async(
            game_prefix='1v1 free-for-all',
            level=FreeForAllLevel(
                level_options=LevelOptions(duration=3 * 60),
                add_one_bot=False, map_builder=make_small_circles_layout),
            bot_count=1,
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else BOT_DIFFICULTY_EASY,
        )


@scenarios.append
class OneOnOneTrosnothMatch(TutorialScenario):
    name = '1v1 Trosnoth match'
    description = 'Play a Trosnoth match against a single bot. Capture all orbs to win.'
    intro = (
        'The aim of Trosnoth is to capture all enemy rooms.\n\n'

        'To capture a room, touch the orb at the room centre. If the enemy bot is defending the '
        'room, you will need to kill it or chase it away first.\n\n'

        'You can only capture a room that is next to territory you own.'
    )

    async def run(self, hard_mode=False):
        from trosnoth.levels.solo import SoloRulesGame

        return await launch_solo_game_async(
            game_prefix='1v1 Trosnoth',
            level=SoloRulesGame(include_rabbit_hunt=False),
            bot_count=1,
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else DEFAULT_BOT_DIFFICULTY,
        )


@scenarios.append
class ThreeOnThreeTrosnothMatch(TutorialScenario):
    name = '3v3 Trosnoth match'
    description = 'You and 2 bots play Trosnoth against 3 bots.'
    intro = (
        'This is a tournament-style 3v3 Trosnoth match, with bots on both teams.\n\n'

        'You can only capture a room if there are more attackers than defenders alive in the '
        'room. E.g.:\n'
        '2 attackers vs. 1 defender = can capture\n'
        '1 attacker vs. 1 defender = cannot capture\n\n'

        'If a team’s territory is divided in two, the team loses the smaller section.'
    )

    async def run(self, hard_mode=False):
        from trosnoth.levels.standard import StandardRandomLevel

        return await launch_solo_game_async(
            game_prefix='3v3 Trosnoth',
            level=StandardRandomLevel(include_rabbit_hunt=False),
            bot_count=5,
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else DEFAULT_BOT_DIFFICULTY,
        )


@scenarios.append
class FreeForAll(TutorialScenario):
    name = 'Four player free-for-all'
    description = 'Practise dogfighting in a 3-bot free-for-all.'

    async def run(self, hard_mode=False):
        from trosnoth.levels.freeforall import FreeForAllLevel

        return await launch_solo_game_async(
            game_prefix='Free-for-all',
            level=FreeForAllLevel(level_options=LevelOptions(duration=300), add_one_bot=False),
            bot_count=3,
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else DEFAULT_BOT_DIFFICULTY,
        )


@scenarios.append
class LastStandTrosnothMatch(TutorialScenario):
    name = '3v3 Last stand'
    description = 'Try to win from a losing position.'
    intro = (
        'This is a tournament-style 3v3 Trosnoth match, with bots on both teams.\n\n'

        'However, your team begins the scenario with only 1 or 2 rooms remaining.'
    )

    async def run(self, hard_mode=False):
        from trosnoth.levels.laststand import LastStandLevel

        return await launch_solo_game_async(
            game_prefix='3v3 Last stand',
            level=LastStandLevel(include_rabbit_hunt=False),
            bot_count=5,
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else DEFAULT_BOT_DIFFICULTY,
        )


@scenarios.append
class NonViolentTrosnoth(TutorialScenario):
    name = 'Non-violent Trosnoth'
    description = 'Learn to position your player by playing a Trosnoth match where nobody can ' \
                  'shoot.'
    intro = (
        'This is a regular Trosnoth match, except nobody can fire shots.\n\n'

        'To prevent a room from being captured, you simply need to keep enough defenders in the '
        'room. To capture a room, you need to target a room that is not well defended.\n\n'

        'Pay close attention to the minimap so you will know when to defend and which room to '
        'attack.'
    )

    async def run(self, hard_mode=False):
        from trosnoth.levels.positioningdrill import PositioningDrillLevel

        return await launch_solo_game_async(
            game_prefix='Non-violent',
            level=PositioningDrillLevel(include_rabbit_hunt=False),
            bot_count=5,
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else DEFAULT_BOT_DIFFICULTY,
        )


@scenarios.append
class PacifistChallenge(TutorialScenario):
    name = 'Pacifist Challenge'
    description = 'Try to win a 3v3 Trosnoth match without firing a single shot.'
    intro = (
        'This is a regular Trosnoth 3v3 match, with a twist.\n\n'

        'In this scenario, everyone can fire shots except you.\n\n'

        'Good luck!'
    )

    async def run(self, hard_mode=False):
        from trosnoth.levels.pacifistdrill import HumansArePacifistsLevel
        return await launch_solo_game_async(
            game_prefix='Pacifist Challenge',
            level=HumansArePacifistsLevel(include_rabbit_hunt=False),
            bot_count=5,
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else DEFAULT_BOT_DIFFICULTY,
        )


@scenarios.append
class WingmanChallenge2v2(TutorialScenario):
    name = '2v2 Wingman Challenge'
    description = 'Try to win a 2v2 Trosnoth match without capturing any orbs.'
    intro = (
        'In this 2v2 Trosnoth match, bots can capture rooms but you can’t.\n\n'

        'You’ll need to focus on defending and supporting your team mate.\n\n'

        'Good luck!'
    )

    async def run(self, hard_mode=False):
        from trosnoth.levels.wingmandrill import HumansAreWingmenLevel
        return await launch_solo_game_async(
            game_prefix='2v2 Wingman Challenge',
            level=HumansAreWingmenLevel(include_rabbit_hunt=False),
            bot_count=3,
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else DEFAULT_BOT_DIFFICULTY,
        )


@scenarios.append
class WingmanChallenge(TutorialScenario):
    name = '3v3 Wingman Challenge'
    description = 'Try to win a 3v3 Trosnoth match without capturing any orbs.'
    intro = (
        'In this 3v3 Trosnoth match, bots can capture rooms but you can’t.\n\n'

        'You’ll need to focus on defending and supporting your team mates.\n\n'

        'Good luck!'
    )

    async def run(self, hard_mode=False):
        from trosnoth.levels.wingmandrill import HumansAreWingmenLevel
        return await launch_solo_game_async(
            game_prefix='3v3 Wingman Challenge',
            level=HumansAreWingmenLevel(
                include_rabbit_hunt=False, level_options=LevelOptions(map_index=1)),
            bot_count=5,
            bot_difficulty=BOT_DIFFICULTY_HARD if hard_mode else DEFAULT_BOT_DIFFICULTY,
        )
