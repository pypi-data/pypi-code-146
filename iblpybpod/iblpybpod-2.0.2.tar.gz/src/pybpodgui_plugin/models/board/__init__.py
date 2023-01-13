# !/usr/bin/python3
# -*- coding: utf-8 -*-

from confapp import conf

from pybpodgui_plugin.models.board.board_uibusy import BoardUIBusy

Board = type(
    'Board',
    tuple(conf.GENERIC_EDITOR_PLUGINS_FINDER.find_class('models.board.Board') + [BoardUIBusy]),
    {}
)
