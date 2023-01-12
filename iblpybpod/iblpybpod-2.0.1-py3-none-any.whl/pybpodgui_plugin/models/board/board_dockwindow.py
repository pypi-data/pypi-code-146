# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pybpodgui_plugin.models.board.windows.code_editor import CodeEditor
from pybpodgui_plugin.models.board.board_treenode import BoardTreeNode
from pybpodgui_plugin.models.board.windows.log_window import LogWindow

logger = logging.getLogger(__name__)


class BoardDockWindow(BoardTreeNode):
    """
    Dock window settings.
    Define here behaviors associated with board details section.

    **Properties**

        mainwindow
            Returns project main window.

    **Methods**

    """

    def __init__(self, project):
        super(BoardDockWindow, self).__init__(project)

        self._log_btn.value = self.open_log_window

    def show(self):
        """
        Select this window as the main window on the details section.
        """
        self.mainwindow.details.value = self
        super(BoardDockWindow, self).show()

    def focus_name(self):
        """
        Sets interface focus on the board name text field
        """
        self._name.form.lineEdit.setFocus()

    def remove(self):
        """

        Prompts user to confirm board removal and closes mdi windows associated with this board.

        .. seealso::
            This method extends board tree node :py:meth:`pybpodgui_plugin.models.board.board_treenode.BoardTreeNode.remove`.

        """
        reply = self.question('Board "{0}" will be deleted. Are you sure?'.format(self.name), 'Warning')

        if reply == 'yes':
            self.mainwindow.details.value = None
            if hasattr(self, '_code_editor'):
                self.mainwindow.mdi_area -= self._code_editor
            if hasattr(self, '_log'):
                self.mainwindow.mdi_area -= self._log

            super(BoardDockWindow, self).remove()

    def open_log_window(self):
        """
        Open board console window on the mdi section.
        """
        if not hasattr(self, '_log'):
            self._log = LogWindow(self)
        self.mainwindow.mdi_area += self._log

    def __edit_framework_evt(self):
        """
        Open code editor window on the mdi section for the framework source code.
        """
        if not self.path:
            self.message(self, "Cannot edit the file yet.", "You need to save the project first.")
        else:
            if not hasattr(self, '_code_editor'):
                self._code_editor = CodeEditor(self)

            self.mainwindow.mdi_area += self._code_editor

    @property
    def mainwindow(self):
        return self.project.mainwindow

    @property
    def name(self):
        return BoardTreeNode.name.fget(self)

    @name.setter
    def name(self, value):
        BoardTreeNode.name.fset(self, value)
        if hasattr(self, '_log'):
            self._log.title = value
        if hasattr(self, '_code_editor'):
            self._code_editor.title = value
