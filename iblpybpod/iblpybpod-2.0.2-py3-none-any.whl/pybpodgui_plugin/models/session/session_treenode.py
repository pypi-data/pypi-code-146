# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf


from AnyQt.QtGui import QIcon
from AnyQt import QtCore

from pybpodgui_plugin.models.session.session_window import SessionWindow

logger = logging.getLogger(__name__)


class SessionTreeNode(SessionWindow):
    def __init__(self, setup):
        SessionWindow.__init__(self, setup)

        self.__running_icon = QIcon(conf.PLAY_SMALL_ICON)
        # this helps on cascade elimination of treenodes
        self.subjects_nodes = {}
        self.running = False
        self.create_treenode(self.tree)

    def create_treenode(self, tree):
        self.node = tree.create_child(self.name, self.setup.node)
        self.node.key_pressed_event = self.node_key_pressed_event
        self.node.double_clicked_event = self.node_double_clicked_event
        self.node.window = self
        self.node.setExpanded(True)

        tree.add_popup_menu_option('Remove', self.remove, item=self.node, icon=QIcon(conf.REMOVE_SMALL_ICON))

        return self.node

    def node_key_pressed_event(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.remove()

    def node_double_clicked_event(self):
        self.load_contents()

    @property
    def name(self):
        if hasattr(self, 'node'):
            return str(self.node.text(0))
        else:
            return SessionWindow.name.fget(self)

    @name.setter
    def name(self, value):
        SessionWindow.name.fset(self, value)
        if hasattr(self, 'node'):
            self.node.setText(0, value)

    @property
    def tree(self):
        return self.setup.tree

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def remove(self):
        if self.setup.MARKED_FOR_REMOVAL:
            reply = 'yes'
        else:
            reply = self.question('Delete session: ' + self.name + '?', 'Delete')

        if reply == 'yes':
            super(SessionTreeNode, self).remove()
            self.setup.node.removeChild(self.node)
