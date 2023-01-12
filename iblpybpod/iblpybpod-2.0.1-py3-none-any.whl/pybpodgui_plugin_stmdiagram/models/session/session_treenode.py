# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf

from AnyQt.QtGui import QIcon

from pyforms.controls import ControlTree

from pybpodgui_plugin_stmdiagram.stmdiagram_window import StmDiagramWindow

logger = logging.getLogger(__name__)


class SessionTreeNode(object):

    def create_treenode(self, tree):
        """

        :param ControlTree tree: project tree

        :return: this session tree node
        """
        node = super().create_treenode(tree)
        self.stmdiagram_action = tree.add_popup_menu_option(
            'STM Diagram',
            self.__open_stmdiagram_plugin,
            item=self.node,
            icon=QIcon(conf.TIMELINE_PLUGIN_ICON)
        )
        return node

    def __open_stmdiagram_plugin(self):

        self.load_contents()

        if not hasattr(self, 'stmdiagram_win'):
            self.stmdiagram_win = StmDiagramWindow(self)
            self.stmdiagram_win.show()
            self.stmdiagram_win.subwindow.resize(*conf.TIMELINE_PLUGIN_WINDOW_SIZE)
        else:
            self.stmdiagram_win.show()

        self.stmdiagram_action.setEnabled(False)

    def remove(self):
        if hasattr(self, 'stmdiagram_win'):
            self.mainwindow.mdi_area -= self.stmdiagram_win
        super().remove()

    @property
    def name(self):
        return super(SessionTreeNode, self.__class__).name.fget(self)

    @name.setter
    def name(self, value):
        super(SessionTreeNode, self.__class__).name.fset(self, value)
        if hasattr(self, 'stmdiagram_win'):
            self.stmdiagram_win.title = value
