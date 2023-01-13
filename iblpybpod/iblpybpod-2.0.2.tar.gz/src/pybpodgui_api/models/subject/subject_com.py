import logging

from pybpodgui_api.exceptions.wrong_subject_error import WrongSubjectConfigured
from .subject_base import SubjectBase

logger = logging.getLogger(__name__)


class SubjectCom(SubjectBase):

    def can_run_task(self):
        # if already running we should stop it (the run button changes to stop when pressed)
        if self.setup.status == self.setup.STATUS_RUNNING_TASK:
            self.setup.stop_task()
            self.setup.status = self.setup.STATUS_READY
            return False

        if self.setup is None or self.setup == 0:
            raise Exception('Please select a setup before proceeding.')

        if not (len(self.setup.subjects) == 1 and self in self.setup.subjects):
            raise WrongSubjectConfigured('The subject is not properly configured in the selected setup.')

        return True

    def run_task(self):
        if self.can_run_task():
            self.setup.run_task()
