#!/usr/bin/python3
# -*- coding: utf-8 -*-


import logging
import os

import pyforms
from pyforms.basewidget import BaseWidget

logger = logging.getLogger(__name__)

try:
    from pyforms.controls import ControlCodeEditor
except:
    logger.error("Could not import ControlCodeEditor. Is QScintilla installed?")


class CodeEditor(BaseWidget):

    def __init__(self, board):
        BaseWidget.__init__(self, board.name)
        self.board = board
        self.layout().setContentsMargins(5, 5, 5, 5)

        self._code = ControlCodeEditor('Code', self.__get_code())

        self._code.changed_event = self.__code_changed_evt

    def __get_code(self):

        try:
            with open(self.board.hardware_file, "r") as file:
                return file.read()
        except:
            pass

        return ''

    def __code_changed_evt(self):
        hw_path = os.path.join(self.board.path, 'hardware.py')
        with open(hw_path, "w") as file:
            return file.write(self._code.value)

    def beforeClose(self):
        """
        Before closing window, ask user if she wants to save (if there are changes)
        """
        if self._code.is_modified:
            reply = self.question('Save the changes', 'Save the file')

            if reply == 'yes':
                self.__code_changed_evt()

        return False

    @property
    def title(self):
        return BaseWidget.title.fget(self)

    @title.setter
    def title(self, value):
        BaseWidget.title.fset(self, "{0} hardware editor".format(value))


# Execute the application
if __name__ == "__main__":
    pyforms.start_app(CodeEditor)
