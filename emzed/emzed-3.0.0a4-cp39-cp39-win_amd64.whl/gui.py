#! /usr/bin/env python
# Copyright 2020 Uwe Schmitt <uwe.schmitt@id.ethz.ch>

try:
    import emzed_gui

    has_emzed_gui = True
    __dir__ = emzed_gui.__dir__
except ImportError:
    has_emzed_gui = False

    def __dir__():
        return []


def __getattr__(name):
    if not has_emzed_gui:
        raise AttributeError("please install emzed3_gui to access emzed.gui")

    return getattr(emzed_gui, name)
