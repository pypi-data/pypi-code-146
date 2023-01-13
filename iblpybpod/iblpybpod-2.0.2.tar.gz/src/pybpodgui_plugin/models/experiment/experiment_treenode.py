# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf

from AnyQt.QtGui import QIcon
from AnyQt import QtCore

from pybpodgui_plugin.models.setup import Setup
from pybpodgui_plugin.models.experiment.experiment_window import ExperimentWindow

logger = logging.getLogger(__name__)


class ExperimentTreeNode(ExperimentWindow):
    """
    Extends experiment window to show up in the project tree section.
    Define here actions related to the experiment tree node.

    **Properties**

        name
            Handles experiment tree node name.

        tree
            Returns project tree.

    **Methods**

    """

    def __init__(self, project):
        # type: (project) -> None
        """

        :param project: project where this experiment belongs
        :type project: pybpodgui_plugin.models.project.Project
        """
        ExperimentWindow.__init__(self, project)

        self.__running_icon = QIcon(conf.PLAY_SMALL_ICON)

        self.create_treenode(self.tree)

    def create_treenode(self, tree):
        """
        Creates node for this experiment under the parent "Experiments" node.

        This methods is called when the experiment is first created.

        The following actions get assigned to node:
            * *Add setup*: :class:`ExperimentTreeNode._ExperimentTreeNode__add_setup`.
            * *Remove*: :class:`ExperimentTreeNode.remove`.

        Sets key events:
            * :class:`ExperimentTreeNode.node_key_pressed_event`


        :param tree: the project tree
        :type tree: pyforms.controls.ControlTree
        :return: new created node
        :return type: QTreeWidgetItem
        """
        self.node = tree.create_child(self.name, self.project.experiments_node,
                                      icon=QIcon(conf.EXPERIMENT_SMALL_ICON))
        self.node.key_pressed_event = self.node_key_pressed_event
        self.node.window = self
        self.node.setExpanded(True)

        tree.add_popup_menu_option('Add setup', self.__add_setup, item=self.node,
                                   icon=QIcon(conf.ADD_SMALL_ICON))
        tree.add_popup_menu_option('Remove', self.remove, item=self.node, icon=QIcon(conf.REMOVE_SMALL_ICON))

        return self.node

    def __add_setup(self):
        """
        Bind events for adding new setup (a.k.a setup). Invokes :class:`ExperimentTreeNode.create_setup`.

        """
        setup = self.create_setup()
        setup.focus_name()

    def create_setup(self):
        """
        Invoke setup (a.k.a setup) creation and focus GUI on the new node.

        :return: the setup just created.
        :return type: Setup

        .. seealso::
            Setup: :class:`pybpodgui_plugin.models.setup.setup_window.SetupWindow`.

        """
        setup = Setup(self)
        self.tree.setCurrentItem(setup.node)
        return setup

    def remove(self):
        """
        Iterates over all setups (a.k.a. setup) and remove them.
        Finally, removes experiment node from project tree and remove experiment from project.

        .. seealso::
            * Experiment removal (API): :class:`pybpodgui_api.models.experiment.experiment_base.ExperimentBase.remove`.
            * Experiment Dock window: :class:`pybpodgui_plugin.models.experiment.experiment_dockwindow.ExperimentDockWindow`.
            * Remove experiment from project: :class:`pybpodgui_api.models.project.project_base.ProjectBase.__sub__`.
        """
        for index in range(len(self.setups) - 1, -1, -1):
            self.setups[index].remove()

        self.project -= self
        self.project.experiments_node.removeChild(self.node)

    def node_key_pressed_event(self, event):
        """
        Sets key events for:
            * Remove experiment: :class:`ExperimentTreeNode.remove`

        :param event: key event
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.remove()

    @property
    def name(self):
        if hasattr(self, 'node'):
            return str(self.node.text(0))
        else:
            return ExperimentWindow.name.fget(self)

    @name.setter
    def name(self, value):
        ExperimentWindow.name.fset(self, value)
        if hasattr(self, 'node'): self.node.setText(0, value)

    @property
    def tree(self):
        return self.project.tree
