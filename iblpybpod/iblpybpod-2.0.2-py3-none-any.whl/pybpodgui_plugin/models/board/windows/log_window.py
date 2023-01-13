#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from AnyQt.QtGui import QIcon
from confapp import conf
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlButton
from pyforms.controls import ControlCheckBox
from pyforms.controls import ControlTextArea

logger = logging.getLogger(__name__)


class LogWindow(BaseWidget):
    def __init__(self, board):
        BaseWidget.__init__(self, board.name)
        self.board = board
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.setWindowIcon(QIcon(conf.BOARD_SMALL_ICON))
        self._autoscroll_checkbox = ControlCheckBox('Auto-scroll', default=True, changed_event=self.__auto_scroll_evt)
        self._clear_btn = ControlButton('Clear', default=self.__clear_log_evt)
        self._log = ControlTextArea(readonly=True, autoscroll=False)

        self.formset = [(' ', '_autoscroll_checkbox', '_clear_btn'), '_log']

    def __add__(self, data):
        self._log += data
        return self

    def show(self):
        # Prevent the call to be recursive because of the mdi_area
        if hasattr(self, '_show_called'):
            BaseWidget.show(self)
            return
        self._show_called = True
        self.mainwindow.mdi_area += self
        del self._show_called

    def beforeClose(self):
        return False

    def __auto_scroll_evt(self):
        self._log.autoscroll = self._autoscroll_checkbox.value

    def __clear_log_evt(self):
        self._log.value = ''

    @property
    def title(self):
        return BaseWidget.title.fget(self)

    @title.setter
    def title(self, value):
        BaseWidget.title.fset(self, "{0} log".format(value))

    @property
    def mainwindow(self):
        return self.board.mainwindow
