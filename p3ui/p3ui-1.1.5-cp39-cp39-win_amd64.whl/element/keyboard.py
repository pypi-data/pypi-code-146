import asyncio
import inspect
from collections import deque

from .numpad import NumPad
from ..native import *


class Keyboard(ChildWindow):
    class Event:
        """ each key input event may consist of key down/up and an optional character with modifiers"""

        def __init__(self, key, character, modifiers=[]):
            self.key = key
            self.character = character
            self.modifiers = modifiers

    @staticmethod
    def is_editable(node):
        if node is None:
            return False
        it = node
        while it:
            if isinstance(it, Window):
                break
            if isinstance(it, NumPad):
                return False
            it = it.parent
        return isinstance(node, InputText)

    def __init__(self, user_interface, item_size=2.5, spacing=0.25, unit=em):
        self._enabled = True
        self.user_interface = user_interface
        self.item_size, self.spacing, self.unit = item_size, spacing, unit

        s = item_size | unit
        space = spacing | unit
        s2 = (item_size * 2 + spacing) | unit

        self.input_target_node = None
        self._input_task = None
        self._input = []
        self._events = list()
        self._change_listener = []

        self._shift_key_pressed = False

        def make_button(label, key=None, character=None, height=(s, 0, 0), width=(s, 0, 0), on_click=None):
            if on_click is None:
                on_click = lambda: self.push_event(Keyboard.Event(
                    key=key,
                    character=character)
                )
            return Button(
                label=label,
                width=width,
                height=height,
                on_click=on_click
            )

        def make_abc_button(label, key):
            def push_event():
                self.push_event(Keyboard.Event(
                    key=key,
                    character=label.upper() if self._shift_key_pressed else label.lower(),
                    modifiers=[Key_ModShift] if self._shift_key_pressed else []
                ))
                if self._shift_key_pressed:
                    self.toggle_shift()

            button = Button(
                label=label,
                width=(s, 0, 0),
                height=(s, 0, 0),
                on_click=push_event
            )

            def on_change():
                if self._shift_key_pressed:
                    button.label = label.upper()
                else:
                    button.label = label.lower()

            self._change_listener.append(on_change)
            return button

        number_row = Row(
            justify_content=Justification.Start,
            padding=(0 | em, 0 | em),
            spacing=space,
            align_items=Alignment.Stretch,
            children=[
                make_button(label='_', character='_'),
                make_button(label='1', key=Key_1, character='1'),
                make_button(label='2', key=Key_2, character='2'),
                make_button(label='3', key=Key_3, character='3'),
                make_button(label='4', key=Key_4, character='4'),
                make_button(label='5', key=Key_5, character='5'),
                make_button(label='6', key=Key_6, character='6'),
                make_button(label='7', key=Key_7, character='7'),
                make_button(label='8', key=Key_8, character='8'),
                make_button(label='9', key=Key_9, character='9'),
                make_button(label='0', key=Key_0, character='0'),
                make_button(label='<', key=Key_Backspace, width=(s2, 0, 0))
            ]
        )
        row1 = Row(
            justify_content=Justification.Start,
            padding=(0 | em, 0 | em),
            spacing=space,
            align_items=Alignment.Stretch,
            children=[
                make_button(label='@', character='@'),
                make_abc_button(label='q', key=Key_Q),
                make_abc_button(label='w', key=Key_W),
                make_abc_button(label='e', key=Key_E),
                make_abc_button(label='r', key=Key_R),
                make_abc_button(label='t', key=Key_T),
                make_abc_button(label='z', key=Key_Z),
                make_abc_button(label='u', key=Key_U),
                make_abc_button(label='i', key=Key_I),
                make_abc_button(label='o', key=Key_O),
                make_abc_button(label='p', key=Key_P),
                make_button(label='!', key=Key_1, character='!'),
                make_button(label='?', key=None, character='?')
            ]
        )
        row2 = Row(
            justify_content=Justification.Start,
            padding=(0 | em, 0 | em),
            spacing=space,
            align_items=Alignment.Stretch,
            children=[
                make_button(label='Abc', key=Key_LeftShift, character=None, width=(s2, 0, 0),
                            on_click=self.toggle_shift),
                make_abc_button(label='a', key=Key_A),
                make_abc_button(label='s', key=Key_S),
                make_abc_button(label='d', key=Key_D),
                make_abc_button(label='f', key=Key_F),
                make_abc_button(label='g', key=Key_G),
                make_abc_button(label='h', key=Key_H),
                make_abc_button(label='j', key=Key_J),
                make_abc_button(label='k', key=Key_K),
                make_abc_button(label='l', key=Key_L),
                make_button(label='<', key=Key_LeftArrow),
                make_button(label='>', key=Key_RightArrow),
            ]
        )
        row3 = Row(
            justify_content=Justification.Start,
            padding=(0 | em, 0 | em),
            spacing=space,
            align_items=Alignment.Stretch,
            children=[
                make_button(label='space', key=Key_Space, character=' ', width=(s2, 0, 0)),
                make_abc_button(label='y', key=Key_Y),
                make_abc_button(label='x', key=Key_X),
                make_abc_button(label='c', key=Key_C),
                make_abc_button(label='v', key=Key_V),
                make_abc_button(label='b', key=Key_B),
                make_abc_button(label='n', key=Key_N),
                make_abc_button(label='m', key=Key_M),
                make_button(label=',', key=Key_Comma, character=','),
                make_button(label='.', key=Key_Period, character='.'),
                make_button(label='enter', key=Key_Enter, width=(s2, 0, 0)),
            ]
        )
        super().__init__(
            label='Keyboard',
            visible=False,
            on_close=self.close,
            resizeable=False,
            on_resize=self.center_widget,
            content=Column(
                padding=(0.5 | em, 0.5 | em),
                height=(auto, 0, 0),
                align_items=Alignment.Stretch,
                spacing=space,
                children=[number_row, row1, row2, row3]
            ))
        user_interface.add(self)

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        if not value:
            self.close()

    def toggle_shift(self):
        self._shift_key_pressed = not self._shift_key_pressed
        [listener() for listener in self._change_listener]

    def push_event(self, event):
        self._events.append(event)
        if not self._input_task:
            self._input_task = asyncio.get_event_loop().create_task(self._process_event())
        self.input_target_node.focus()

    async def _process_event(self):
        while True:
            #
            # the input needs 2 frames, one for activation, second for the input queue?
            if self.input_target_node == self.user_interface.active_node:
                counter += 1
            else:
                counter = 0
            if counter > 1:
                break
            await asyncio.sleep(0)
        try:
            #
            # this works in "no time" since v. 1.88, else we'd need a sleep(0)
            for e in self._events:
                if e.key is not None:
                    self.user_interface.add_key_event(e.key, True, None)
                if e.character is not None:
                    self.user_interface.add_input_character(ord(e.character))
                if e.key is not None:
                    self.user_interface.add_key_event(e.key, False, None)
        finally:
            self._events = []
            self._input_task = None

    @staticmethod
    def create(user_interface):
        self = Keyboard(user_interface)

        #
        #
        super_on_changed = user_interface.on_active_node_changed

        async def on_active_node_changed():
            if not self.enabled:
                return
            if super_on_changed:
                await super_on_changed()
            if Keyboard.is_editable(user_interface.active_node):
                if user_interface.active_node != self.input_target_node:
                    self.visible = True
                    self.opacity = 0.
                    self.input_target_node = user_interface.active_node
                    #
                    # keyboard have to be visible before we can focus and move it
                    await asyncio.sleep(0)
                    self.input_target_node.focus()
                    self.center_widget(self.size)
                    return
            #
            # the focus flag can only be obtained while the window is visible (invisible->unfocused)
            if not self.visible:
                return
            if self.focused:
                return
            #
            # in between there may be one frame with an unfocused window
            await asyncio.sleep(0)
            if not self.focused and not Keyboard.is_editable(user_interface.active_node):
                self.input_target_node = None
                self.close()

        user_interface.on_active_node_changed = on_active_node_changed
        return self

    def center_widget(self, s):
        ps = self.user_interface.size
        rx = ps[0] - s[0]
        ry = ps[1] - s[1]
        self.left = rx / 2 | px
        self.top = ry - 50 | px
        self.opacity = 1.

    def close(self):
        self.visible = False
        self.input_target_node = None
