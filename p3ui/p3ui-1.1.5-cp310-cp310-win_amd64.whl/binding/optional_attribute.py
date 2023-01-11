from ..native import *
from .. import Icons
from p3ui.editor._config import active_color


class OptionalAttribute(Row):

    def __init__(self, target, attribute_name, children, default_to):
        self.target, self.attribute_name = target, attribute_name
        self._children = children
        self.default_value = default_to
        #
        # prevent automatic evaluation ..
        self._evals = [c.eval for c in children]
        #        for c in children:
        #            c.eval = lambda: None

        super().__init__(
            width=(1 | em, 1, 1),
            padding=(0 | px, 0 | px),
            spacing=0.125 | em,
            align_items=Alignment.Center,
            justify_content=Justification.Center,
            on_mouse_enter=lambda _: self.eval(),
            on_mouse_leave=lambda _: self.eval(),
            background_color=lambda: active_color if self.hover and self._text.visible else '#77777711',
            children=children + [
                text := Text(value='none'),
                Spacer(width=(0 | px, 0, 0), height=(2 | em, 0, 0)),
                button := Button(width=(auto, 0, 0), label=f'{Icons.Close}', on_click=self.set_none)
            ]
        )
        self._text = text
        self._button = button
        self._temp = None

    def set_none(self):
        setattr(self.target, self.attribute_name, None)
        self.eval()

    def _on_mouse_down(self, e):
        print('mouse down')
        setattr(self.target, self.attribute_name, self.default_value)
        self.eval()

    def eval(self):
        value = getattr(self.target, self.attribute_name)
        #
        # self.on_mouse_down have be set if and only if it is None.
        # else the strong handle in the user data may be reset and
        # in this case the mouse down fails.
        if self.on_mouse_down is None and value is None:
            self.on_mouse_down = self._on_mouse_down
        elif self.on_mouse_down is not None and value is not None:
            self.on_mouse_down = None
        #
        # show or hide children, based on the value state
        self._text.visible = value is None
        self._button.visible = value is not None
        for child in self._children:
            child.visible = value is not None
            if value is None:
                continue
        #
        # only evaluate children if value not set to none
        if value is not None:
            [e() for e in self._evals]
        super().eval()
