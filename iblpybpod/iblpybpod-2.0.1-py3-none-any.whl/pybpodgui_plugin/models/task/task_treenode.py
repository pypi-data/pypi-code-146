# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf


from AnyQt.QtWidgets import QApplication
from AnyQt.QtGui import QIcon
from AnyQt import QtCore

from pybpodgui_plugin.models.task.task_window import TaskWindow

logger = logging.getLogger(__name__)


class TaskTreeNode(TaskWindow):
    """
    Extends task window to show up in the project tree section.
    Define here actions related to the task tree node.

    **Properties**

        name
            Handles task tree node name.

        tree
            Returns project tree.

    **Methods**

    """

    def __init__(self, project):
        TaskWindow.__init__(self, project)

        self.create_treenode(self.tree)

    def create_treenode(self, tree):
        """
        Creates node for this task under the parent "Tasks" node.

        This methods is called when the task is first created.

        The following actions get assigned to node:
            * *Remove*: :meth:`TaskTreeNode.remove`.

        Sets key events:
            * :meth:`TaskTreeNode.node_key_pressed_event`


        :param tree: the project tree
        :type tree: pyforms.controls.ControlTree
        :return: new created node
        :return type: QtGui.QTreeWidgetItem
        """
        self.node = tree.create_child(self.name, self.project.tasks_node, icon=QIcon(conf.TASK_SMALL_ICON))
        self.node.key_pressed_event = self.node_key_pressed_event
        self.node.double_clicked_event = self.node_double_clicked_event
        self.node.window = self
        self.node.setExpanded(True)

        tree.add_popup_menu_option('Remove', self.remove, item=self.node, icon=QIcon(conf.REMOVE_SMALL_ICON))
        return self.node

    def node_key_pressed_event(self, event):
        """
        Sets key events for:
            * Remove task: :meth:`TaskTreeNode.remove`
            * Edit task code: :py:meth:`pybpodgui_plugin.models.task.task_dockwindow.TaskDockWindow.edit_btn_evt`

        :param event: key event
        """
        modifiers = QApplication.keyboardModifiers()

        if event.key() == QtCore.Qt.Key_O and modifiers == QtCore.Qt.ControlModifier:
            self.edit_btn_evt()
        elif event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            self.edit_btn_evt()
        elif event.key() == QtCore.Qt.Key_Delete:
            self.remove()

    def node_double_clicked_event(self):
        """
        Fires event :py:meth:`pybpodgui_plugin.models.task.task_dockwindow.TaskDockWindow.edit_btn_evt` when tree node
        is double clicked.
        """
        self.edit_btn_evt()

    def remove(self):
        """

        Remove task from project and remove node from tree.

        .. seealso::
            * Task removal (dock window): :py:meth:`pybpodgui_plugin.models.task.task_dockwindow.TaskDockWindow.remove`.
            * Task removal (API): :meth:`pybpodgui_api.models.board.board_base.TaskBase.remove`.
            * Remove task from project: :meth:`pybpodgui_api.models.project.project_base.ProjectBase.__sub__`.

        """
        self.project -= self
        self.project.tasks_node.removeChild(self.node)

    @property
    def name(self):
        return TaskWindow.name.fget(self)

    @name.setter
    def name(self, value):
        TaskWindow.name.fset(self, value)
        if hasattr(self, 'node'):
            self.node.setText(0, value)
        if hasattr(self, '_code_editor'):
            self._code_editor.title = value
            self._code_editor.refresh_directory()

    @property
    def tree(self):
        return self.project.tree
