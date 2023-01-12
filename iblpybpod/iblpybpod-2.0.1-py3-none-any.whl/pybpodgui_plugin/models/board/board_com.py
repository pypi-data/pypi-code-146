# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pybpodgui_api.models.setup import Setup

from pybpodgui_plugin.models.board.board_window import BoardWindow
from AnyQt.QtCore import QTimer

logger = logging.getLogger(__name__)


class BoardCom(BoardWindow):
    """
    Board communication logic. Define here actions that can be triggered on board.

    .. seealso::
        This class heavy relies on the corresponding API module.

        :py:class:`pybpodgui_api.models.board.board_com.BoardCom`

    **Methods**

    """

    def __init__(self, project=None):
        BoardWindow.__init__(self, project)

        self._timer = QTimer()
        self._timer.timeout.connect(self.run_task_handler)

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def log2board(self, data):
        if hasattr(self, '_log') and self._log.visible:
            self._log += data

    def run_task(self, session, board_task, workspace_path, detached=False):
        """
        Bases: :meth:`pybpodgui_api.models.board.board_com.BoardCom.run_task`

        Start running task on board by invoking API

        :param session:
        :param board_task: board and task object
        :return: True if no problems occur, False otherwise.
        """
        flag = None
        self._enable_btn_flag = True
        self._tmp_setup = session.setup
        try:
            flag = super(BoardCom, self).run_task(session, board_task, workspace_path, detached)
        except Exception:
            board_task.setup.status = Setup.STATUS_READY
            self.status = self.STATUS_READY
            raise

        return flag

    def start_run_task_handler(self):
        super(BoardCom, self).start_run_task_handler()
        self._timer.start(500)

    def end_run_task_handler(self):
        super(BoardCom, self).end_run_task_handler()
        self.run_task_handler(False)
