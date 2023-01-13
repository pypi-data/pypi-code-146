# !/usr/bin/python3
# -*- coding: utf-8 -*-

from pybpodgui_plugin.models.setup.setup_dockwindow import SetupDockWindow


class SetupCom(SetupDockWindow):
    """
    Define board actions that are triggered by setup.

    .. seealso::
        This class heavy relies on the corresponding API module.

        :py:class:`pybpodgui_api.models.setup.setup_com.SetupCom`

    **Methods**

    """

    def stop_task(self):
        """
        Stop task by calling API.

        Also, update UI by calling :py:meth:`pybpodgui_plugin.models.setup.setup_uibuisy.SetupUIBusy.update_ui`.
        """
        super(SetupCom, self).stop_task()
        self.update_ui()

    def kill_task(self):
        """
        Kill the task by calling
        """
        super(SetupCom, self).kill_task()
        self.update_ui()
