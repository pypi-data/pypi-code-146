import asyncio
from collections import deque

from ..native import *

import inspect


class NumPad(ChildWindow):
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
        return hasattr(node, 'value') and not isinstance(node, InputText)

    def __init__(self, user_interface, item_size=2.5, spacing=0.25, unit=em):
        self.user_interface = user_interface
        self.item_size, self.spacing, self.unit = item_size, spacing, unit

        s = item_size | unit
        space = spacing | unit
        s2 = (item_size * 2 + spacing) | unit

        self.input_target_node = None
        self._input_task = None
        self._input = []
        self._events = deque()
        self._enabled = True

        def make_button(label, key=None, character=None, height=(s, 0, 0), width=(s, 0, 0), on_click=None):
            if on_click is None:
                on_click = lambda: self.push_event(NumPad.Event(
                    key=key,
                    character=character)
                )
            return Button(
                label=label,
                width=width,
                height=height,
                on_click=on_click
            )

        self.input = InputText(width=(item_size * 3 + 2 * spacing | unit, 0, 0))

        row1 = Row(
            justify_content=Justification.Start,
            padding=(0 | em, 0 | em),
            spacing=space,
            align_items=Alignment.Stretch,
            children=[
                make_button(label='7', key=Key_7, character='7'),
                make_button(label='8', key=Key_8, character='8'),
                make_button(label='9', key=Key_9, character='9'),
                make_button(label='*', character='*'),
                make_button(label='/', character='/'),
                make_button(label='<', key=Key_Backspace, width=(s2, 0, 0))
            ]
        )
        row2 = Row(
            justify_content=Justification.Start,
            padding=(0 | em, 0 | em),
            spacing=space,
            align_items=Alignment.Stretch,
            children=[
                make_button(label='4', key=Key_5, character='4'),
                make_button(label='5', key=Key_6, character='5'),
                make_button(label='6', key=Key_7, character='6'),
                make_button(label='+', character='+'),
                make_button(label='-', character='-'),
                make_button(label='<', key=Key_LeftArrow),
                make_button(label='>', key=Key_RightArrow)
            ]
        )
        row3 = Row(
            justify_content=Justification.Start,
            padding=(0 | em, 0 | em),
            spacing=space,
            align_items=Alignment.Stretch,
            children=[
                make_button(label='1', key=Key_1, character='1'),
                make_button(label='2', key=Key_2, character='2'),
                make_button(label='3', key=Key_3, character='3'),
                make_button(label='(', character='('),
                make_button(label=')', character=')')
            ]
        )
        row4 = Row(
            justify_content=Justification.Start,
            padding=(0 | em, 0 | em),
            spacing=space,
            align_items=Alignment.Stretch,
            children=[
                make_button(label='0', key=Key_0, character='0', width=(s2, 0, 0)),
                make_button(label='.', key=Key_Period, character='.'),
                make_button(label='space', key=Key_Space, character=' ', width=(s2, 0, 0))
            ]
        )
        super().__init__(
            label='NumPad',
            visible=False,
            on_close=self.close,
            resizeable=False,
            on_resize=self.center_widget,
            content=Column(
                padding=(0.5 | em, 0.5 | em),
                height=(auto, 0, 0),
                align_items=Alignment.Stretch,
                spacing=space,
                children=[
                    self.input,
                    row1,
                    row2,
                    Row(
                        padding=(0 | em, 0 | em),
                        spacing=space,
                        children=[
                            Column(
                                padding=(0 | em, 0 | em),
                                spacing=space,
                                children=[
                                    row3,
                                    row4
                                ]
                            ),
                            make_button(label='enter', key=Key_Enter, width=(s2, 0, 0), height=(s2, 0, 0),
                                        on_click=self.enter)
                        ]
                    )

                ]
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

    async def enter(self):
        try:
            v = self.input.value
            if len(v) == 0:
                return
            self.input_target_node.value = eval(v)
            if self.input_target_node.on_change:
                if inspect.iscoroutinefunction(self.input_target_node.on_change):
                    await self.input_target_node.on_change(self.input_target_node.value)
                else:
                    self.input_target_node.on_change(self.input_target_node.value)
            self.close()
        except:
            pass
        finally:
            pass

    def push_event(self, event):
        self._events.append(event)
        if not self._input_task:
            self._input_task = asyncio.get_event_loop().create_task(self._process_event())
        self.input.focus()

    async def _process_event(self):
        while True:
            #
            # the input needs 2 frames, one for activation, second for the input queue?
            if self.input == self.user_interface.active_node:
                counter += 1
            else:
                counter = 0
            if counter > 1:
                break
            await asyncio.sleep(0)
        #
        # this works in "no time" since v. 1.88, else we'd need a sleep(0)
        for e in self._events:
            if e.key is not None:
                self.user_interface.add_key_event(e.key, True, None)
            if e.character is not None:
                self.user_interface.add_input_character(ord(e.character))
            if e.key is not None:
                self.user_interface.add_key_event(e.key, False, None)
        self._events = []
        self._input_task = None

    @staticmethod
    def create(user_interface):
        self = NumPad(user_interface)

        #
        #
        super_on_changed = user_interface.on_active_node_changed

        async def on_active_node_changed():
            if not self.enabled:
                return
            if super_on_changed:
                await super_on_changed()
            active_node = user_interface.active_node
            i = 0
            #
            # must be active for 5 frames
            while i < 5:
                await asyncio.sleep(0)
                if active_node != user_interface.active_node:
                    return
                i += 1
                #
                # reset counter on mouse action
                if self.user_interface.mouse_state.left_button_down:
                    i = 0
            if NumPad.is_editable(user_interface.active_node):
                if user_interface.active_node != self.input_target_node:
                    self.visible = True
                    self.opacity = 0.
                    self.input_target_node = user_interface.active_node
                    self.input.value = str(self.input_target_node.value)
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
            if not self.focused and not NumPad.is_editable(user_interface.active_node):
                self.close()

        #
        #
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
