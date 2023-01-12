# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf

from AnyQt.QtGui import QIcon
from AnyQt import QtCore


from pybpodgui_plugin.models.setup.setup_window import SetupWindow


logger = logging.getLogger(__name__)


class SetupTreeNode(SetupWindow):
    """
    Extends setup window to show up in the project tree section.
    Define here actions related to the setup tree node.

    **Properties**

        name
            Handles setup tree node name.

        tree
            Returns project tree.

    **Methods**

    """

    def __init__(self, experiment):
        SetupWindow.__init__(self, experiment)

        self.__running_icon = QIcon(conf.PLAY_SMALL_ICON)

        self.create_treenode(self.tree)

    def create_treenode(self, tree):
        """
        Creates node for this setup under the corresponding experiment parent node.

        This methods is called when the setup is first created.

        The following actions get assigned to node:
            * *Remove*: :meth:`SetupTreeNode.remove`.

        Sets key events:
            * :meth:`SetupTreeNode.node_key_pressed_event`


        :param tree: the project tree
        :type tree: pyforms.controls.ControlTree
        :return: new created node
        :return type: QTreeWidgetItem
        """

        self.node = tree.create_child(self.name, self.experiment.node, icon=QIcon(conf.BOX_SMALL_ICON))
        self.node.key_pressed_event = self.node_key_pressed_event
        self.node.window = self
        # self.node.setExpanded(True)

        tree.add_popup_menu_option('Remove', self.remove, item=self.node, icon=QIcon(conf.REMOVE_SMALL_ICON))
        return self.node

    def remove(self):
        """
        Remove setup from project and remove node from tree.

        .. seealso::
            * Setup removal (dock window): :py:meth:`pybpodgui_plugin.models.setup.setup_dockwindow.SetupDockWindow.remove`.
            * Setup removal (API): :meth:`pybpodgui_api.models.board.setup_base.SetupBase.remove`.
        """

        for index in range(len(self.sessions) - 1, -1, -1):
            self.sessions[index].remove()
        self.experiment -= self
        self.experiment.node.removeChild(self.node)

    def node_key_pressed_event(self, event):
        """
        Sets key events for:
            * Remove setup: :class:`SetupTreeNode.remove`

        :param event: key event
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.remove()

    @property
    def name(self):
        if hasattr(self, 'node'):
            return str(self.node.text(0))
        else:
            return SetupWindow.name.fget(self)

    @name.setter
    def name(self, value):
        SetupWindow.name.fset(self, value)
        if hasattr(self, 'node'):
            self.node.setText(0, value)

    @property
    def tree(self):
        return self.experiment.tree
