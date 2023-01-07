#!/usr/bin/env python

'''Assetto Corsa Websockets App Objects'''

import tkinter as tk
from tkinter import ttk

APP_TITLE = 'ACWS Client'
BUTTON_X = 10
COLUMN_X = 50
CONSOLE_X = 86
CONSOLE_Y = 15
ENTRY_X = 40
FRAME_X = 800
FRAME_Y = 100
LABEL_X = 8
PAD_X = 10
PAD_Y = 5

ENABLE_VISIBLE_SCROLLBAR = False


class GriddedButton(ttk.Button):
    '''Button in a grid'''

    def __init__(self, parent, grid_row: int, grid_col: int,
                 width: int = BUTTON_X, **kwargs):

        super().__init__(parent, width=width, **kwargs)

        self.grid_propagate(False)
        self.grid(row=grid_row, column=grid_col, padx=PAD_X, pady=PAD_Y)


class GriddedEntry(ttk.Entry):
    '''Entry in a grid'''

    def __init__(self, parent, grid_row: int, grid_col: int,
                 width: int = ENTRY_X, **kwargs):

        super().__init__(parent, width=width, **kwargs)

        self.grid_propagate(False)
        self.grid(row=grid_row, column=grid_col, padx=PAD_X, pady=PAD_Y)


class GriddedFrame(tk.Frame):
    '''Frame inside a Grid'''

    def __init__(self, grid_row: int, grid_col: int,
                 height_by: float = 1, width_by: float = 1, **kwargs):

        super().__init__(height=FRAME_Y * height_by,
                         width=FRAME_X * width_by, **kwargs)

        self.grid_propagate(False)
        self.grid(row=grid_row, column=grid_col, padx=PAD_X, pady=PAD_Y)

    def configure_columns(self, *weights):
        '''Helper function to configure column weights'''
        i = 0
        for weight in weights:
            self.columnconfigure(i, weight=weight)
            i += 1

    def configure_rows(self, *weights):
        '''Helper function to configure row weights'''
        i = 0
        for weight in weights:
            self.rowconfigure(i, weights=weight)
            i += 1


class GriddedLabel(ttk.Label):
    '''Label inside a Grid'''

    def __init__(self, parent, grid_row: int, grid_col: int, width: int = LABEL_X, **kwargs):

        super().__init__(parent, width=width, **kwargs)

        self.grid_propagate(False)
        self.grid(row=grid_row, column=grid_col, padx=PAD_X, pady=PAD_Y)


class GriddedListbox(tk.Listbox):
    '''Listbox in a grid'''

    def __init__(self, parent, grid_row: int, grid_col: int,
                 grid_span: int = 1, **kwargs):

        super().__init__(parent, height=CONSOLE_Y, width=CONSOLE_X, **kwargs)

        self.grid(row=grid_row, column=grid_col,
                  columnspan=grid_span, padx=PAD_X, pady=PAD_Y)

        scrollbar = tk.Scrollbar(parent)

        if ENABLE_VISIBLE_SCROLLBAR:
            scrollbar.grid(row=grid_row,
                           column=grid_col + grid_span + 1,
                           padx=PAD_X, pady=PAD_Y)
            scrollbar.config(command=self.yview)

        self.config(yscrollcommand=scrollbar.set)


class GriddedTreeview(ttk.Treeview):
    '''Treeview in a grid'''

    def __init__(self, parent, grid_row: int, grid_col: int,
                 grid_span: int = 1, **kwargs):

        super().__init__(parent, height=CONSOLE_Y - 2, show='headings', **kwargs)

        self.grid(row=grid_row, column=grid_col,
                  columnspan=grid_span, padx=PAD_X, pady=PAD_Y)

        self._columns = ()

        scrollbar = tk.Scrollbar(parent)
        self.config(yscrollcommand=scrollbar.set)

    def add_columns(self, *cols):
        '''Add all columns to the tree'''

        self['columns'] = cols
        for col in cols:
            self.column(col, anchor=tk.W)
            self.heading(col, text=col, anchor=tk.W)

    def set_widths(self, *widths):
        '''Set column widths'''

        i = 0
        for width in widths:
            self.column(i, minwidth=width, width=width)
            i += 1


class TrafficLight():
    '''Tk based traffic light'''

    def __init__(self, parent, row: int, column: int):
        self.colour = 'red'
        self.canvas = tk.Canvas(parent, width=20, height=20)
        self.canvas.grid(row=row, column=column, padx=PAD_X, pady=PAD_Y)
        self.light = self.canvas.create_oval(5, 5, 20, 20, fill=self.colour)

    def gray(self):
        self.canvas.itemconfigure(self.light, fill='darkgray')

    def green(self):
        self.canvas.itemconfigure(self.light, fill='green')

    def red(self):
        self.canvas.itemconfigure(self.light, fill='red')
