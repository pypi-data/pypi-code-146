import sys
import time
import random
import re
import signal

# Problematic imports - start
import keyboard
import pyautogui
import pyperclip
# Problematic imports - end

import klsframe.gui.guiLayout as guiLayout


# --------------------------------------------------------------------------
# BASIC API CALLS
# --------------------------------------------------------------------------

def click(x=None, y=None, button='left', clicks=1, interval=0.0):
    """
    Moves to (x, y) and clicks the specified button ``clicks`` times
    :param x:
    :param y:
    :param button:
    :param clicks:
    :param interval:
    :return:
    """
    pyautogui.click(x=x, y=y, button=button, clicks=clicks, interval=interval)


def click_on(elem: guiLayout.GUIComponent, button='left', clicks=1):
    pt = elem.get_point(position='center')
    click_at(pt, button=button, clicks=clicks)


def click_at(point: guiLayout.Point, button='left', clicks=1):
    click(x=point.x, y=point.y, button=button, clicks=clicks)


def move(x, y, duration=0.0):
    pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeOutQuad)


def move_to(self, point: guiLayout.Point):
    pyautogui.moveTo(point.x, point.y, duration=self.speed_profile, tween=pyautogui.easeOutQuad)


def write(msg, interval=0.0):
    """
    Tries to write wherever the cursor is placed

    Arguments
        msg. String to be written. Can contain special characters (\n, \t...)
        If msg is a list of strings, then each element of the list will be written in a new line
    """
    if type(msg) is str:
        pyautogui.write(message=msg, interval=interval)
    elif type(msg) is list:
        for m in msg:
            pyautogui.write(message=f'{m}\n', interval=interval)
    else:
        raise TypeError('Invalid type for msg in write()')


def press(*args, interval=0.0):
    """
    Combination of pyautogui.press and pyautogui.hotkey
    press('ctrl', 'c') = press(*['ctrl', 'c']) = press('ctrl+c')
    You can pass a list of key-actions that will be executed in order, for example: 'ctrl+c', 'ctrl+v'
    Arguments (2 types)
        string
             'a' -> single press
             'a+b+c' -> hotkey (use \\ to escape +, like 3\\+2 = 5)
        tuple
            ('c', 2) -> {'key': 'c', 'presses': 2}
            ('ctrl+t', 2) -> {'key': 'ctrl+t', 'presses': 2}
    """
    for arg in args:
        if type(arg) is tuple:
            _key = arg[0]
            _presses = arg[1]
        elif type(arg) is str:
            _key = arg
            _presses = 1
        else:
            raise TypeError('Invalid args type in press() ')

        if _key.find('+') != -1 and re.search('^\\w+(\\+\\w+)+', arg) is not None:
            for _i in range(0, _presses):
                pyautogui.hotkey(*_key.split('+'))
        else:
            pyautogui.press(keys=_key, presses=_presses, interval=interval)


def scroll(value, direction='vertical', x=None, y=None):
    """
    pyautogui.scroll(10)   # scroll up 10 "clicks"
    pyautogui.scroll(-10)  # scroll down 10 "clicks"
    pyautogui.scroll(10, x=100, y=100)  # move mouse cursor to 100, 200, then scroll up 10 "clicks"

    ONLY in OS X and Linux platforms
    pyautogui.hscroll(10)   # scroll right 10 "clicks"
    pyautogui.hscroll(-10)   # scroll left 10 "clicks"
    """
    _allowed_directions = ['vertical', 'horizontal']
    _allowed_values = range(-10000, 10001)
    if direction not in _allowed_directions:
        raise ValueError(f"Error. Invalid value for direction ({direction})")
    elif direction == 'horizontal' and sys.platform.find('win') != -1:
        raise ValueError(f"Error. Horizontal scrolling not supported on Windows platform")
    elif value not in _allowed_values:
        raise ValueError(f"Error. Invalid scroll value. Valid range [-100, 100]")

    if direction == 'vertical':
        vt_scroll(clicks=value, x=x, y=y)
    elif direction == 'horizontal':
        hz_scroll(clicks=value, x=y, y=y)
    else:
        raise ValueError('Unexpected value for argument "direction"')


def hz_scroll(clicks, x=None, y=None):
    if x is not None and y is not None:
        if guiLayout.safe_coordinates(x, y):
            pyautogui.hscroll(clicks=clicks, x=x, y=y)
        else:
            raise ValueError(f"Error. Coordinates ({x}, {y}) out of range")
    else:
        pyautogui.hscroll(clicks=clicks)


def vt_scroll(clicks, x=None, y=None):
    if x is not None and y is not None:
        if guiLayout.safe_coordinates(x, y):
            pyautogui.vscroll(clicks=clicks, x=x, y=y)
        else:
            raise ValueError(f"Error. Coordinates ({x}, {y}) out of range")
    else:
        pyautogui.vscroll(clicks=clicks)


def pause(seconds):
    time.sleep(seconds)


# --------------------------------------------------------------------------
# ADVANCED FUNCTIONS
# --------------------------------------------------------------------------

def keep_awake(minutes=None):
    screen = pyautogui.size()
    safe_threshold = 25
    delay = 2
    if minutes is None:
        stop_condition = lambda: True
    elif isinstance(minutes, int) and 1 <= minutes < 1440:  # Between 1 minute and 1 day
        _end = time.time() + minutes * 60
        stop_condition = lambda: time.time() <= _end
    else:
        raise ValueError("Value provided for the parameter 'minutes' is out of range [1, 1440]")
    while stop_condition():
        # TODO: use my own click function
        pyautogui.moveTo(
            x=random.randint(safe_threshold, screen.width - safe_threshold),
            y=random.randint(safe_threshold, screen.height - safe_threshold))
        if random.randint(0, 3) == 1:  # 25% chances
            pyautogui.press('f5')
            time.sleep(delay)
            pyautogui.press('esc')
            time.sleep(delay)
        else:
            time.sleep(delay)


def quick_action(action):
    # TODO: Implement quick actions
    quick_actions = {
        'next_window': lambda: pyautogui.hotkey(*['alt', 'tab']),
        'next_tab': lambda: pyautogui.hotkey(*['ctrl', 'tab']),
        'close_tab': lambda: pyautogui.hotkey(*['ctrl', 'w']),
        'win_explorer': lambda: pyautogui.hotkey(*['win', 'e']),
        'cut': {'hold': ['ctrl'], 'do': ['x']},
        'open-link-new-tab': {'hold': ['ctrl'], 'do': [{'button': 'left', 'presses': 1, 'x': -1, 'y': -1}]},
        'copy': ['ctrl', 'c'],
        'paste': ['ctrl', 'v'],
    }
    # These are predefined quick actions
    # (right) click
    # double (right) click
    # triple (right) click
    # left click
    # middle click
    __PREDEFINED_ACTIONS = [
        {
            'command': 'press',
            'target': (None, None),
            'value': ['ctrl', 'c'],
            'description': 'copy'
        }
    ]
    pass


def with_hold_do(holds=None, actions=None):
    """
    We can define here quick actions. For example 'ctrl-click', 'ctrl-cmd', 'shift-cmd'

    Arguments
        holds: e.g. 'ctrl', 'shift', 'alt', 'alt-gr', 'fn'...
        actions: a list of actions
            keys 'a', 'b', 'c'...
            clicks {'clicks': 1, button: 'left', 'x': x, 'y': y}
                If (x, y) == (-1, -1) click in the current position
    """
    if holds is None:
        holds = []
    if actions is None:
        actions = []
    with pyautogui.hold(holds):
        for act in actions:
            if type(act) is tuple and len(act) == 2:
                click(x=act[0], y=act[1])
            elif type(act) is dict:
                click(button=act['button'], clicks=act['clicks'], x=act['x'], y=act['y'])
            elif type(act) is str:
                write(act)
            else:
                raise ValueError(f'Invalid type {type(act)} for hold_and_do(). ')


def copy_text(x=None, y=None, remove_special_chars=False):
    # TODO: refactor
    if x is None or y is None:
        x = pyautogui.position()[0]
        y = pyautogui.position()[1]
    # move(x, y)
    pyautogui.click(x=x, y=y, button='left', clicks=3)
    with_hold_do(['ctrl'], ['c'])
    if remove_special_chars:
        return re.sub('[\t\n\r]+', '', get_clipboard()).strip()
    else:
        return get_clipboard().strip()


def get_clipboard():
    # https://stackoverflow.com/questions/101128/how-do-i-read-text-from-the-clipboard
    # return Tk().clipboard_get()
    return pyperclip.paste()


def set_clipboard(data):
    # https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard
    # TODO: fix. It does not work with Tkinter
    pyperclip.copy(str(data))


def get_coordinates():
    # TODO: Update according to the new class ScreenArea
    while True:
        elem_name = pyautogui.prompt('Place the cursor on the component and enter its name')
        if elem_name == '' or elem_name is None:
            break
        else:
            time.sleep(5)
            pos = pyautogui.position()
            print(f'{elem_name} = ({pos[0]}, {pos[1]})')


def find_window(target):
    for wd in pyautogui.getAllTitles():
        if re.search(target, wd) is not None:
            windows = pyautogui.getWindowsWithTitle(wd)
            if windows is None:
                raise FileNotFoundError(f"Window {target} not found. Is it open?")
            elif len(windows) != 1:
                raise ValueError(f"Ambiguous search. More than one window with name {target}")
            else:
                windows[0].activate()
                windows[0].maximize()
                return windows[0]
    raise FileNotFoundError(f"Window {target} not found. Is it open?")


# --------------------------------------------------------------------------
# CLASSES
# --------------------------------------------------------------------------

class Action:
    def __init__(self):
        self.command = ''  # click, move, write, press...
        self.target = ''  # (x,y)
        self.value = ''  # Additional args, e.g. [right, triple] -> click
        self.description = ''  # Optional short description of the action.


class Worker:
    __MAX_SPEED = 2.0
    __MIN_SPEED = 0.0

    def __init__(self, speed=None):
        _allowed = ["autobot", "millennial", "grandpa"]
        if re.match('[0-9]+(.[0-9])?', speed) is not None:
            speed = float(speed)
            if self.__MAX_SPEED < speed or speed < self.__MIN_SPEED:
                raise ValueError('Invalid speed range for the Worker')
        elif type(speed) is str:
            if speed in _allowed:
                speed = float(_allowed.index(speed))
            else:
                raise ValueError(f'Unknown Worker speed profile "{speed}". '
                                 f'Supported profiles (from slow to fast) are: {", ".join(_allowed)}')

        self.speed_profile = speed
        self._interval_delay = 0.0
        self.busy = False  # Indicate if the worker is currently executing a subroutine
        self.target_window = ''
        self.gui_layout = guiLayout.GUILayout()
        # STATS
        self.traveling_time = 0
        self.total_clicks = 0
        self.total_keys_pressed = 0

        self.update_speed_profile(0)
        keyboard.add_hotkey('ctrl+alt+add', lambda: self.update_speed_profile(0.5))
        keyboard.add_hotkey('ctrl+alt+subtract', lambda: self.update_speed_profile(-0.5))
        keyboard.add_hotkey('ctrl+alt+p', self.halt_resume_execution)

    def update_speed_profile(self, inc):
        if 0.0 <= self.speed_profile + float(inc) <= 2.0:
            self.speed_profile += float(inc)
            # TODO: this formula may be improved
            self._interval_delay = (0.05 + self.speed_profile / 10) * (self.speed_profile + 1)
            pyautogui.PAUSE = self.speed_profile
            print(f"[INFO] Speed profile updated (fastest <= current <= slowest): 0 <= {self.speed_profile} <= 2")
        elif self.speed_profile == 0.0:
            print('[WARN] Already using the slower speed profile')
        elif self.speed_profile == 2.0:
            print('[WARN] Already using the fastest speed profile')
        else:
            raise ValueError("Error. Speed profile out of bounds")

    def _pre_actions_checks(self):
        self.find_target_window()
        if not self.busy:
            exit(0)

    def is_target_window(self, alert=False):
        if re.search(self.target_window, pyautogui.getActiveWindow().title) is not None:
            return True
        else:
            if alert:
                res = pyautogui.confirm('WINDOW OUT OF SCOPE. Press enter to continue...')
                if res == 'Cancel':
                    print('[INFO] Operation cancelled by the user. Exiting...')
                    exit(0)
            return False

    def find_target_window(self):
        if self.is_target_window():
            pyautogui.getActiveWindow().maximize()
        else:
            find_window(self.target_window)

    def halt_resume_execution(self):
        self.busy = not self.busy
        # ret = pyautogui.confirm(title='Halt execution', text='Execution halted. Do you want to continue?')
        # if ret == 'OK':
        #     p.resume()
        #     return
        # elif ret == 'Cancel':
        #     p.terminate()
        #     sys.exit(0)
        # else:
        #     raise ValueError('Unexpected error in function halt()')
        signal.raise_signal(signal.SIGTERM)
        raise KeyboardInterrupt

    def execute(self, **kwargs):
        # TODO: wrapper for every action execution, so that if busy is set to false, it will stop immediately
        self._pre_actions_checks()
        while self.busy:
            pass

    def click(self, x=None, y=None, button='left', clicks=1):
        self.busy = True
        self._pre_actions_checks()
        click(x=x, y=y, button=button, clicks=clicks, interval=self._interval_delay)
        self.busy = False

    def move(self, x, y):
        self.busy = True
        self._pre_actions_checks()
        self.traveling_time += self.speed_profile
        move(x, y, self.speed_profile)
        self.busy = False

    def move_to(self, point: guiLayout.Point):
        self.busy = True
        self._pre_actions_checks()
        self.traveling_time += self.speed_profile
        pyautogui.moveTo(point.x, point.y, self.speed_profile, pyautogui.easeOutQuad)
        self.busy = False

    def write(self, msg):
        """
        Tries to write wherever the cursor is placed

        Arguments
            msg. String to be written. Can contain special characters (\n, \t...)
            If msg is a list of strings, then each element of the list will be written in a new line
        """
        self.busy = True
        self._pre_actions_checks()
        if type(msg) is str:
            write(msg=msg, interval=self._interval_delay / 2)
            self.total_keys_pressed += len(msg)
        elif type(msg) is list:
            for m in msg:
                write(msg=f'{m}\n', interval=self._interval_delay / 2)
                self.total_keys_pressed += len(m) + 1  # len(m) + \n
        else:
            raise TypeError('Invalid type for msg in write()')
        self.busy = False

    def press(self, *args):
        """
        press('ctrl', 'c') = press(*['ctrl', 'c']) = press('ctrl+c')
        You can pass a list of key-actions that will be executed in order, for example: 'ctrl+c', 'ctrl+v'
        Arguments (2 types)
            string
                 'a' -> single press
                 'a+b+c' -> hotkey (use \\ to escape +, like 3\\+2 = 5)
            tuple
                ('c', 2) -> {'key': 'c', 'presses': 2}
                ('ctrl+t', 2) -> {'key': 'ctrl+t', 'presses': 2}
        """
        self.busy = True
        self._pre_actions_checks()
        for arg in args:
            if type(arg) is tuple:
                _key = arg[0]
                _presses = arg[1]
            elif type(arg) is str:
                _key = arg
                _presses = 1
            else:
                raise TypeError('Invalid args type in press() ')

            if _key.find('+') != -1 and re.search('^\\w+(\\+\\w+)+', arg) is not None:
                for _i in range(0, _presses):
                    pyautogui.hotkey(*_key.split('+'))
                self.total_keys_pressed += len(_key.split('+')) * _presses
            else:
                pyautogui.press(keys=_key, presses=_presses, interval=self._interval_delay)
                self.total_keys_pressed += _presses
        self.busy = False

    def pause(self, seconds):
        self.traveling_time += seconds
        pause(seconds)

    # --------------------------------------------------------------------------
    # ADVANCED FUNCTIONS
    # --------------------------------------------------------------------------

    def keep_awake(self, minutes=None):
        self.busy = True
        if minutes is None:
            stop_condition = True
        elif isinstance(minutes, int) and 1 <= minutes < 1440:  # Between 1 minute and 1 day
            _end = time.time() + minutes * 60
            stop_condition = lambda: time.time() <= _end
        else:
            raise ValueError("Value provided for the parameter 'minutes' is out of range [1, 1440]")
        while stop_condition:
            move(x=self.gui_layout.screen_center()[0] + random.randint(-200, 200),
                 y=self.gui_layout.screen_center()[1] + random.randint(-200, 200))
            press('f5', 'esc')
            time.sleep(2)

    def quick_action(self, action):
        # TODO: Implement quick actions
        pass

    def with_hold_do(self, holds=None, actions=None):
        """
        We can define here quick actions. For example 'ctrl-click', 'ctrl-cmd', 'shift-cmd'

        Arguments
            holds: e.g. 'ctrl', 'shift', 'alt', 'alt-gr', 'fn'...
            actions: a list of actions
                keys 'a', 'b', 'c'...
                clicks {'clicks': 1, button: 'left', 'x': x, 'y': y}
                    If (x, y) == (-1, -1) click in the current position
        """
        self.busy = True
        self._pre_actions_checks()
        if holds is None:
            holds = []
        if actions is None:
            actions = []
        with pyautogui.hold(holds):
            for act in actions:
                if type(act) is tuple and len(act) == 2:
                    self.click(x=act[0], y=act[1])
                    self.total_clicks += 1
                elif type(act) is dict:
                    self.click(button=act['button'], clicks=act['clicks'], x=act['x'], y=act['y'])
                elif type(act) is str:
                    self.write(act)
                    self.total_keys_pressed += 1
                else:
                    raise ValueError(f'Invalid type {type(act)} for hold_and_do(). ')
                self.pause(self.speed_profile)
        self.busy = False


# -----------------------------------------------------------------------------------------------------------------
# ------------------------------------- MAIN-----------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    keep_awake(minutes=45)
    # w = Worker('millennial')
    # print(w.__dict__)
    # w.keep_awake(minutes=1)
    # exit(0)
