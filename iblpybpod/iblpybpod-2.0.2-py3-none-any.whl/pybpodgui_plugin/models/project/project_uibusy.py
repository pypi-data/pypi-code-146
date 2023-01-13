# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf
from AnyQt.QtGui import QIcon
from pybpodgui_plugin.models.board import Board
from pybpodgui_plugin.models.project.project_dockwindow import ProjectDockWindow

logger = logging.getLogger(__name__)


class ProjectUIBusy(ProjectDockWindow):
    """

    """

    def update_ui(self):
        """
        Update user interface
        """
        busy_status = Board.STATUS_READY

        # This boolean makes it easy to disable run buttons on subjects
        sessionrunning = False

        logger.debug('Project [{0}] status:{1}'.format(self.name, busy_status))

        for board in self.boards:
            if board.status > Board.STATUS_READY:
                busy_status = board.status
                break

        if busy_status == Board.STATUS_READY:

            self.node.setIcon(0, QIcon(conf.PROJECT_SMALL_ICON))
            self.experiments_node.setIcon(0, QIcon(conf.EXPERIMENTS_SMALL_ICON))
            self.boards_node.setIcon(0, QIcon(conf.BOARDS_SMALL_ICON))
            self.subjects_node.setIcon(0, QIcon(conf.SUBJECTS_SMALL_ICON))

        elif busy_status in [Board.STATUS_RUNNING_TASK]:

            self.node.setIcon(0, QIcon(conf.PLAY_SMALL_ICON))
            self.experiments_node.setIcon(0, QIcon(conf.PLAY_SMALL_ICON))
            self.boards_node.setIcon(0, QIcon(conf.PLAY_SMALL_ICON))
            self.subjects_node.setIcon(0, QIcon(conf.PLAY_SMALL_ICON))
            # Flag this true so we can disable 'Run' buttons
            sessionrunning = True

        for exp in self.experiments:
            exp.update_ui()

        for board in self.boards:
            board.update_ui()

        for subj in self.subjects:
            subj.update_ui(sessionrunning)
