# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from pybpodgui_plugin.models.subject.subject_treenode import SubjectTreeNode

logger = logging.getLogger(__name__)


class SubjectDockWindow(SubjectTreeNode):

    def post_load(self):
        self.reload_setups()
        super().post_load()

    def show(self):
        self.mainwindow.details.value = self
        super(SubjectDockWindow, self).show()

    def focus_name(self):
        """
        Sets interface focus on the board name text field
        """
        self._name.form.lineEdit.setFocus()

    def remove(self, silent=False):
        """

        Prompts user to confirm subject removal and closes mdi windows associated with this subject.

        .. seealso::
            This method extends subject tree node :py:meth:`pybpodgui_plugin.models.subject.subject_treenode.SubjectTreeNode.remove`.

        """
        reply = None
        if not silent:
            reply = self.question('Subject "{0}" will be deleted. Are you sure?'.format(self.name), 'Warning')
        if silent or (reply is not None and reply == 'yes'):
            if hasattr(self, '_code_editor'):
                self.mainwindow.mdi_area -= self._code_editor
            super(SubjectDockWindow, self).remove(silent)

    def close(self, silent=False):
        self.mainwindow.details.value = None
        super(SubjectDockWindow, self).close(silent)

    @property
    def mainwindow(self):
        return self.project.mainwindow
