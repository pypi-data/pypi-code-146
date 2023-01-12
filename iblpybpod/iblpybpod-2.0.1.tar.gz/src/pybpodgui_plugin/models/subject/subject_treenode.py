# !/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import inspect
from confapp import conf

from AnyQt.QtGui import QIcon
from AnyQt import QtCore

from pybpodgui_plugin.models.subject.subject_window import SubjectWindow
from pybpodgui_plugin.models.session import Session

logger = logging.getLogger(__name__)


class SubjectTreeNode(SubjectWindow):
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
        SubjectWindow.__init__(self, project)
        self.__running_icon = QIcon(conf.PLAY_SMALL_ICON)
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
        self.node = tree.create_child(self.name, self.project.subjects_node, icon=QIcon(conf.SUBJECT_SMALL_ICON))
        self.node.key_pressed_event = self.node_key_pressed_event
        self.node.window = self
        self.node.setExpanded(True)

        tree.add_popup_menu_option('Remove', self.remove, item=self.node, icon=QIcon(conf.REMOVE_SMALL_ICON))
        return self.node

    def remove(self, silent=False):
        """

        Remove subject from project and remove node from tree.

        .. seealso::
            * Subject removal (dock window): :py:meth:`pybpodgui_plugin.models.subject.subject_dockwindow.SubjectDockWindow.remove`.
            * Subject removal (API): :meth:`pybpodgui_api.models.subject.subject_base.SubjectBase.remove`.
            * Remove board from project: :meth:`pybpodgui_api.models.project.project_base.ProjectBase.__sub__`.

        """
        self.project -= self
        self.project.subjects_node.removeChild(self.node)

    def node_key_pressed_event(self, event):
        """
        Sets key events for:
            * Remove board: :meth:`BoardTreeNode.remove`

        :param event: key event
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.remove()

    def create_sessiontreenode(self, session):
        node = self.tree.create_child(session.name, self.node)
        node.key_pressed_event = session.node_key_pressed_event
        node.double_clicked_event = session.node_double_clicked_event
        # This makes the sesison window appear correctly
        node.window = session.node.window
        session.subjects_nodes[id(self.node)] = node

        return node

    def __add__(self, session):
        if isinstance(session, Session):
            # add another node to the UI
            node = self.create_sessiontreenode(session)
            session.subjects_nodes[id(self.node)] = node
            self.tree.add_popup_menu_option('Remove', session.remove, item=node, icon=QIcon(conf.REMOVE_SMALL_ICON))
        return super(SubjectTreeNode, self).__add__(session)

    def __sub__(self, value):
        if isinstance(value, Session):
            self.node.removeChild(value.subjects_nodes[id(self.node)])
        return super(SubjectTreeNode, self).__sub__(value)

    @property
    def name(self):
        if hasattr(self, 'node'):
            return str(self.node.text(0))
        else:
            return SubjectWindow.name.fget(self)

    @name.setter
    def name(self, value):
        SubjectWindow.name.fset(self, value)
        if hasattr(self, 'node'):
            self.node.setText(0, value)

    @property
    def tree(self):
        return self.project.tree
