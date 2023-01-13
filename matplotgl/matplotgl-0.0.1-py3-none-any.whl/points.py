# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Matplotgl contributors (https://github.com/matplotgl)

import pythreejs as p3
from matplotlib import ticker
import numpy as np
from typing import List, Tuple


class Points:

    def __init__(self, ax, x, y, color='blue', zorder=0) -> None:

        self._ax = ax
        self._x = np.asarray(x)
        self._y = np.asarray(y)
        self._zorder = zorder
        self._geometry = p3.BufferGeometry(
            attributes={
                'position':
                p3.BufferAttribute(array=np.array([
                    self._x, self._y,
                    np.full_like(self._x, self._zorder - 50)
                ],
                                                  dtype='float32').T),
            })
        self._material = p3.PointsMaterial(color=color, size=3)
        self._points = p3.Points(geometry=self._geometry,
                                 material=self._material)

    def get_bbox(self):
        pad = 0.03
        xmin = self._x.min()
        xmax = self._x.max()
        padx = pad * (xmax - xmin)
        ymin = self._y.min()
        ymax = self._y.max()
        pady = pad * (ymax - ymin)
        return {
            'left': xmin - padx,
            'right': xmax + padx,
            'bottom': ymin - pady,
            'top': ymax + pady
        }

    def _apply_transform(self):
        self._geometry.attributes['position'].array = np.array(
            [
                self._ax._transformx(self._x),
                self._ax._transformy(self._y),
                np.full_like(self._x, self._zorder - 50)
            ],
            dtype='float32').T

    def get(self):
        return self._points

    def set_xdata(self, x):
        self._x = np.asarray(x)
        self._apply_transform()

    def set_ydata(self, y):
        self._y = np.asarray(y)
        self._apply_transform()

    def set_data(self, xy):
        self._x = np.asarray(xy[:, 0])
        self._y = np.asarray(xy[:, 1])
        self._apply_transform()
