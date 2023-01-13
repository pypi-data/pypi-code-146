# !/usr/bin/python3
# -*- coding: utf-8 -*-
from pybpodgui_api.models.session.session_io import SessionIO


class SessionCom(SessionIO):
    """

    **Properties**

        status
            :class:`int`

            Holds setup status

    **Methods**

    """

    #### SESSION STATUS CONSTANTS ####
    STATUS_READY = 0
    STATUS_SESSION_RUNNING = 1  # The session is running

    def __init__(self, setup):
        super(SessionCom, self).__init__(setup)
        self.status = self.STATUS_READY

    @property
    def status(self):
        """
        Get and set the session status

        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

        if value == self.STATUS_READY:
            self.setup.status = self.setup.STATUS_READY
        elif value == self.STATUS_SESSION_RUNNING:
            self.setup.status = self.setup.STATUS_RUNNING_TASK
