from typing import List

import numpy as np
import simplejson as json
from coinlib.drawable.DrawableComponent import DrawableComponent


class GridCol(DrawableComponent):
    _width: int = 6
    _childs: List[DrawableComponent] = []

    def __init__(self, width=6, childs=None):
        super(GridCol, self).__init__("GridCol")
        self._width = width
        self._childs = childs if childs is not None else []
        pass

    def plot(self, drawable: DrawableComponent):
        self._childs.append(drawable)


class GridRow(DrawableComponent):
    _columns: List[GridCol] = [GridCol()]

    def __init__(self, cols=[]):
        super(GridRow, self).__init__("GridRow")
        self._columns = cols
        pass

    def plotAt(self, col_index, drawable: DrawableComponent):
        self._columns[col_index].plot(drawable)

class WindowGrid(DrawableComponent):

    _rows: List[GridRow] = []

    def __init__(self, rows: List[GridRow] = [GridRow()]):
        super(WindowGrid, self).__init__("WindowGrid")
        self._rows = []
        for r in rows:
            cols = []
            for c in r:
                cols.append(GridCol(width=c))
            gr = GridRow(cols)
            self._rows.append(gr)
        pass

    def plotAt(self, element: DrawableComponent, row_index=0, col_index=0 ):

        row = self._rows[row_index]

        to_json = getattr(element, "to_json", None)
        if callable(to_json):
            element = element.to_json()

        row.plotAt(col_index, element)

        return True


class DrawableText(DrawableComponent):
    _color = None
    _fontSize = 12

    def __init__(self, text: str, fontSize=12, color="white", caption=None, unit=None):
        super(DrawableText, self).__init__("DrawableText")
        self._text = text
        self._unit = unit
        self._caption = caption
        self._fontSize = fontSize
        self._color = color
        pass


class DrawableTable(DrawableComponent):
    _rows = []
    _columns = []

    def __init__(self, rows=[], columns=[]):
        super(DrawableTable, self).__init__("DrawableTable")
        if isinstance(rows, np.ndarray):
            rows = rows.tolist()
        self._rows = rows
        if isinstance(columns, np.ndarray):
            columns = columns.tolist()
        self._columns = columns
        pass