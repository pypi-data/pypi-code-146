import logging
from confapp import conf

from AnyQt.QtGui import QIcon
from AnyQt import QtCore

from pybpodgui_plugin.models.user.user_window import UserWindow

logger = logging.getLogger(__name__)


class UserTreeNode(UserWindow):
    def __init__(self, _project):
        UserWindow.__init__(self, _project)
        self.project = _project
        self.create_treenode(self.tree)

    def create_treenode(self, tree):
        self.node = tree.create_child(self._name, self.project.users_node, icon=QIcon(conf.PERSON_SMALL_ICON))
        self.node.key_pressed_event = self.node_key_pressed_event
        # print(self.node)
        self.node.window = self
        self.node.double_clicked_event = self.node_double_clicked_event

        tree.add_popup_menu_option('Remove', self.remove, item=self.node, icon=QIcon(conf.REMOVE_SMALL_ICON))
        return self.node

    def node_double_clicked_event(self):
        self.connection = 'local'
        self.project.loggeduser = self

    def remove(self):
        self.project.user_removed(self)
        self.project -= self
        self.project.users_node.removeChild(self.node)

    def node_key_pressed_event(self, event):
        """
        Sets key events for:
            * Remove board: :meth:`BoardTreeNode.remove`

        :param event: key event
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.remove()

    @property
    def name(self):
        if hasattr(self, 'node'):
            return str(self.node.text(0))
        else:
            return UserWindow.name.fget(self)

    @name.setter
    def name(self, value):
        UserWindow.name.fset(self, value)
        if hasattr(self, 'node'):
            self.node.setText(0, value)

    @property
    def tree(self):
        return self.project.tree
