# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf

from AnyQt.QtGui import QIcon
from AnyQt import QtCore

from pybpodgui_plugin.models.board.board_com import BoardCom

logger = logging.getLogger(__name__)


class BoardTreeNode(BoardCom):
    """
    Extends board window to show up in the project tree section.
    Define here actions related to the board tree node.

    **Properties**

        name
            Handles board tree node name.

        tree
            Returns project tree.

    **Methods**

    """

    def __init__(self, project):
        BoardCom.__init__(self, project)
        self.create_treenode(self.tree)

    def create_treenode(self, tree):
        """
        Creates node for this board under the parent "Boards" node.

        This methods is called when the board is first created.

        The following actions get assigned to node:
            * *Remove*: :meth:`BoardTreeNode.remove`.

        Sets key events:
            * :meth:`BoardTreeNode.node_key_pressed_event`


        :param tree: the project tree
        :type tree: pyforms.controls.ControlTree
        :return: new created node
        :return type: QTreeWidgetItem
        """
        self.node = tree.create_child(self.name, self.project.boards_node, icon=QIcon(conf.BOARD_SMALL_ICON))
        self.node.key_pressed_event = self.node_key_pressed_event
        self.node.double_clicked_event = self.node_double_clicked_event
        self.node.window = self
        self.node.setExpanded(True)

        tree.add_popup_menu_option('Remove', self.remove, item=self.node, icon=QIcon(conf.REMOVE_SMALL_ICON))
        return self.node

    def remove(self):
        """

        Remove board from project and remove node from tree.

        .. seealso::
            * Board removal (dock window): :py:meth:`pybpodgui_plugin.models.board.board_dockwindow.BoardDockWindow.remove`.
            * Board removal (API): :meth:`pybpodgui_api.models.board.board_base.BoardBase.remove`.
            * Remove board from project: :meth:`pybpodgui_api.models.project.project_base.ProjectBase.__sub__`.

        """
        self.project -= self
        self.project.boards_node.removeChild(self.node)

    def node_key_pressed_event(self, event):
        """
        Sets key events for:
            * Remove board: :meth:`BoardTreeNode.remove`

        :param event: key event
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.remove()

    def node_double_clicked_event(self):
        """
        Open board console window when tree node is double clicked.
        """
        self.open_log_window()

    @property
    def name(self):
        if hasattr(self, 'node'):
            return str(self.node.text(0))
        else:
            return BoardCom.name.fget(self)

    @name.setter
    def name(self, value):
        BoardCom.name.fset(self, value)
        if hasattr(self, 'node'):
            self.node.setText(0, value)

    @property
    def tree(self):
        return self.project.tree
