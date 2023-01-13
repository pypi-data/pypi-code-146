import logging
from pybpodgui_plugin.models.user.user_treenode import UserTreeNode

logger = logging.getLogger(__name__)


class UserDockWindow(UserTreeNode):

    def show(self):
        self.mainWindow.details.value = self
        super(UserDockWindow, self).show()

    def focus_name(self):
        self._namebox.form.lineEdit.setFocus()

    def remove(self):
        """

        Prompts user to confirm user removal and closes mdi windows associated with this user.

        .. seealso::
            This method extends user tree node :py:meth:`pybpodgui_plugin.models.user.user_treenode.UserTreeNode.remove`.

        """
        reply = self.question('User "{0}" will be deleted. Are you sure?'.format(self.name), 'Warning')
        if reply == 'yes':
            if hasattr(self, '_code_editor'):
                self.mainwindow.mdi_area -= self._code_editor
            super(UserDockWindow, self).remove()

    def close(self):
        self.mainWindow.details.value = None
        super(UserDockWindow, self).close()

    @property
    def mainWindow(self):
        return self.project.mainwindow
