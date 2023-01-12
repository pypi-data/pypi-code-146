# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf

from AnyQt.QtGui import QIcon

from pyforms.controls import ControlTree

from pybpodgui_plugin_timeline.trials_plot_window import TrialsPlotWindow

logger = logging.getLogger(__name__)


class SessionTreeNode(object):

    def create_treenode(self, tree):
        """

        :param ControlTree tree: project tree

        :return: this session tree node
        """
        node = super(SessionTreeNode, self).create_treenode(tree)
        self.trialsplot_action = tree.add_popup_menu_option(
            'Bars graph',
            self.__open_trials_plot_plugin,
            item=self.node,
            icon=QIcon(conf.TIMELINE_PLUGIN_ICON)
        )
        return node

    def __open_trials_plot_plugin(self):
        if not hasattr(self, 'trialsplot_win'):
            self.trialsplot_win = TrialsPlotWindow(self)
            self.trialsplot_win.show()
            self.trialsplot_win.subwindow.resize(
                *conf.TIMELINE_PLUGIN_WINDOW_SIZE)
        else:
            self.trialsplot_win.show()

        self.trialsplot_action.setEnabled(False)

    def remove(self):
        if hasattr(self, 'trialsplot_win'):
            self.mainwindow.mdi_area -= self.trialsplot_win
        super(SessionTreeNode, self).remove()

    @property
    def name(self):
        return super(SessionTreeNode, self.__class__).name.fget(self)

    @name.setter
    def name(self, value):
        super(SessionTreeNode, self.__class__).name.fset(self, value)
        if hasattr(self, 'trialsplot_win'):
            self.trialsplot_win.title = value
