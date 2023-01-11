import asyncio

import p3ui
from p3ui.editor._config import active_color, list_background_color_even, list_background_color_odd
from p3ui.element.dialog import Dialog
from p3ui import *


class AddIconDialogItem(Row):

    def __init__(self):
        self.item = None
        self.dialog = dialog
        self.icon = None
        super().__init__(
            padding=(0.618 | em, 0.618 | em),
            content=Text(value=lambda: f'{model.item[0]} {model.item[1]}'),
            background_color=lambda: self.eval_background_color(),
            on_mouse_down=lambda e: AddIconDialog.Instance.select(self.icon),
            on_mouse_enter=lambda _: self.parent.parent.eval(),
            on_mouse_leave=lambda _: self.parent.parent.eval(),
        )

    def eval_background_color(self):
        if self.hover:
            return active_color
        elif model.index % 2 == 0:
            return list_background_color_even
        else:
            return list_background_color_odd

    def eval(self):
        self.icon = model.item[0]
        super().eval()


class AddIconDialog(Dialog):
    Instance = None
    Icons = p3ui.Icons

    def __init__(self):
        super().__init__(
            label='Select Icon',
            width=(40 | em, 0, 0),
            height=(30 | em, 0, 0),
            content=Column(
                children=[
                    Row(
                        height=(auto, 0, 0),
                        align_items=Alignment.Center,
                        children=[
                            Text(f'{Icons.Search}'),
                            input := InputText(on_change=self.eval)
                        ],
                        on_select=self.select
                    ),
                    icon_list := ScrolledColumn()
                ]
            )
        )
        self.input = input
        self._future: asyncio.Future = None

        self.repeater = Repeater(
            target_container=icon_list,
            delegate=AddIconDialogItem,
            model=self.list_icons
        )

    def list_icons(self):
        s = self.input.value.lower()
        for name in dir(AddIconDialog.Icons):
            if name.startswith('_'):
                continue
            if s in name.lower():
                yield getattr(AddIconDialog.Icons, name), name

    def select(self, item):
        self._future.set_result(item)
        print('selected', item)

    async def get(self):
        if self._future:
            self._future.set_result(None)
        self._future = asyncio.Future()
        """ get an icon .. """
        await self.show()
        result = await self._future
        self._future = None
        self.close()
        return result

    def close(self):
        if self._future is not None:
            self._future.set_result(None)
            self._future = None
        super().close()
