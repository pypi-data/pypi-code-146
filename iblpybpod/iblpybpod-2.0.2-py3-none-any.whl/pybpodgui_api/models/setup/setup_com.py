# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from confapp import conf
from pybpodgui_api.exceptions.run_setup import RunSetupError
from pybpodgui_api.models.setup.setup_io import SetupBaseIO

logger = logging.getLogger(__name__)


class SetupCom(SetupBaseIO):
    """
    Define board actions that are triggered by setup.

    **Properties**

        status
            :class:`int`

            Holds setup status depending on board communication state.

    **Methods**

    """

    #### SETUP STATUS CONSTANTS ####
    STATUS_READY = 0
    STATUS_BOARD_LOCKED = 1  # The setup is free but the board is busy
    STATUS_RUNNING_TASK = 2  # The setup is busy running the task, but it cannot be stopped yet

    def __init__(self, experiment):
        super(SetupCom, self).__init__(experiment)
        self.status = self.STATUS_READY

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################
    def stop_trial(self):
        if self.status == self.STATUS_RUNNING_TASK:
            self.board.stop_trial()

    def stop_task(self):
        if self.status == self.STATUS_RUNNING_TASK:
            self.board.stop_task()

    def kill_task(self):
        if self.status == self.STATUS_RUNNING_TASK:
            self.board.kill_task()

    def pause_trial(self):
        if self.status == self.STATUS_RUNNING_TASK:
            self.board.pause_trial()

    def resume_trial(self):
        if self.status == self.STATUS_RUNNING_TASK:
            self.board.resume_trial()

    def run_task(self):
        """
        Run task on board.

        In order to run task, the project must be saved before.
        This method will restore task variables from session, create a new session
        and start the 'run task' operation by calling board function run_task.

        """
        if not self.can_run_task():
            return

        try:
            # update the status of the setup
            self.status = self.STATUS_RUNNING_TASK

            session = self.create_session()
            session.user = self.project.loggeduser

            self._run_flag = self.board.run_task(
                session,
                self.board_task,
                self.path,
                detached=self.detached
            )

            for s in self.subjects:
                s += session

            # we need this if we want to put the play button on the subject treenode's session correctly
            self.project.update_ui()

        except Exception as err:
            logger.error(str(err), exc_info=True)
            raise Exception("Unknown error found while running task. See log for more details.")

    def can_run_task(self):
        if not self.board or not self.task:
            logger.warning("Setup has no protocol assigned.")
            raise RunSetupError("Please assign a board and protocol first")
        if conf.PYBPODGUI_API_CHECK_SUBJECTS_ON_RUN and len(self.subjects) == 0:
            logger.warning("No Subjects selected")
            raise RunSetupError("Please add subjects to this experiment")
        if self.project.loggeduser is None:
            logger.warning("No User selected")
            raise RunSetupError("Please select an User. Please double click an User in the project tree to select it.")
        if not self.project.is_saved():
            # check conf property and save project automatically and return true
            if conf.PYBPODGUI_API_AUTO_SAVE_PROJECT_ON_RUN:
                logger.info("Auto saving project")
                print("Auto saving project")
                self.project.save()
                return True
            else:
                logger.warning("Run protocol cannot be executed because project is not saved.")
                raise RunSetupError("Project must be saved before run protocol")
        return True
