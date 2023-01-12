# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pybpodgui_plugin.models.setup.setup_treenode import SetupTreeNode

logger = logging.getLogger(__name__)


class SetupDockWindow(SetupTreeNode):
    """
    Dock window settings.
    Define here behaviors associated with board dock window.

    **Properties**

        mainwindow
            Returns project main window.

    **Methods**

    """
    MARKED_FOR_REMOVAL = False

    def __init__(self, experiment):
        super(SetupDockWindow, self).__init__(experiment)

    def show(self):
        """
        Select this window as the main window on the details section.
        Also reload boards list on combo box.
        """
        self.mainwindow.details.value = self
        self.reload_boards(current_selected_board=self.board)
        self.reload_tasks(current_selected_task=self.task)
        super(SetupDockWindow, self).show()

    def focus_name(self):
        """
        Sets interface focus on the board name text field
        """
        self._name.form.lineEdit.setFocus()

    def remove(self):
        """

        Prompts user to confirm setup removal.

        .. seealso::
            This method extends setup tree node :py:meth:`pybpodgui_plugin.models.setup.setup_treenode.SetupTreeNode.remove`.

        """
        if self.experiment.MARKED_FOR_REMOVAL:
            reply = 'yes'
        else:
            reply = self.question('Setup "{0}" and all the sessions will be deleted. Are you sure?'.format(self.name),
                                  "Warning")
        if reply == 'yes':
            self.MARKED_FOR_REMOVAL = True
            self.mainwindow.details.value = None
            super(SetupDockWindow, self).remove()

    @property
    def mainwindow(self):
        return self.experiment.mainwindow
