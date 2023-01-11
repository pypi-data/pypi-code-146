import asyncio
from p3ui import *


class Dialog(ChildWindow):

    def __init__(self, **kwargs):
        super().__init__(moveable=False, visible=False, opacity=0., resizeable=False, **kwargs, on_close=self.close)

    def close(self):
        self.opacity = 0.
        self.visible = False

    async def show(self):
        self.visible = True
        await asyncio.sleep(0)
        pw, ph = self.parent.size
        w, h = self.size
        self.left = (pw - w) / 2 | px
        self.top = (ph - h) / 2 | px
        self.opacity = 0.95
