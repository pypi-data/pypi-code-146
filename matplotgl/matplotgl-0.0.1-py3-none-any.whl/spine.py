from .utils import make_sprite, value_to_string

import ipywidgets as ipw
from matplotlib import ticker
import numpy as np
import pythreejs as p3


class Spine(ipw.HTML):

    def __init__(self,
                 kind,
                 transform,
                 ticks=True,
                 color='black',
                 tick_size=0.02):

        self._kind = kind
        self._ticks = ticks
        self.transform = transform
        # self.low = 0
        # self.high = 1
        self.tick_size = tick_size
        self.ticker = ticker.AutoLocator()

        self.geometry = p3.BufferGeometry(
            attributes={
                'position': p3.BufferAttribute(array=np.zeros((5, 3))),
            })
        self.material = p3.LineBasicMaterial(color=color, linewidth=1)
        self.sprites = None

        self.make_line()

        self.line = p3.Line(geometry=self.geometry, material=self.material)

        super().__init__()
        self.add(self.line)

    def make_line(self):
        if self._ticks:
            ticks = self.ticker.tick_values(self.transform.low,
                                            self.transform.high)
            x = [1 if self._kind == 'right' else 0]
            y = [1 if self._kind == 'top' else 0]
            sprites = []
            f = 3
            for tick in ticks:
                if self.transform.low <= tick <= self.transform.high:
                    t = self.transform(tick)
                    if self._kind == 'left':
                        x += [0, -self.tick_size, 0]
                        y += [t, t, t]
                        s = [-f * self.tick_size, t, 0]
                    elif self._kind == 'right':
                        x += [1, 1 + self.tick_size, 1]
                        y += [t, t, t]
                        s = [1 + f * self.tick_size, t, 0]
                    elif self._kind == 'bottom':
                        x += [t, t, t]
                        y += [0, -self.tick_size, 0]
                        s = [t, -f * self.tick_size, 0]
                    elif self._kind == 'top':
                        x += [t, t, t]
                        y += [1, 1 + self.tick_size, 1]
                        s = [t, 1 + f * self.tick_size, 0]
                    sprites.append(
                        make_sprite(value_to_string(tick),
                                    position=s,
                                    size=0.05))
            x += [0 if self._kind == 'left' else 1]
            y += [0 if self._kind == 'bottom' else 1]
            if self.sprites is not None:
                self.remove(self.sprites)
            self.sprites = p3.Group()
            self.sprites.add(sprites)
            self.add(self.sprites)
        else:
            if self._kind == 'left':
                x = [0, 0]
                y = [0, 1]
            elif self._kind == 'right':
                x = [1, 1]
                y = [0, 1]
            elif self._kind == 'bottom':
                x = [0, 1]
                y = [0, 0]
            elif self._kind == 'top':
                x = [0, 1]
                y = [1, 1]
        self.geometry.attributes['position'].array = np.array(
            [x, y, np.zeros_like(x)], dtype='float32').T
        # if self._ticks:

    def set_transform(self, transform):
        self.transform = transform
        self.make_line()
