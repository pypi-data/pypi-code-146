# !/usr/bin/python3
# -*- coding: utf-8 -*-

import traceback
import logging
import os
import subprocess
import io
import sys
import json
import pandas as pd

from confapp import conf
from pathlib import Path

from pybpodapi.session import Session
from pybpodapi.utils import date_parser
from pybpodgui_api.models.board.board_io import BoardIO

from sca.formats.csv import CSV_DELIMITER, CSV_QUOTECHAR, CSV_QUOTING
import csv

from .non_blockingcsvreader import NonBlockingCSVReader
from .non_blockingstreamreader import NonBlockingStreamReader

logger = logging.getLogger(__name__)


class BoardCom(BoardIO):
    #### SETUP STATUS ####
    STATUS_READY = 0
    STATUS_RUNNING_TASK = 1  # The board is busy running a task

    INFO_CREATOR_NAME = 'CREATOR-NAME'
    INFO_PROJECT_NAME = 'PROJECT-NAME'
    INFO_EXPERIMENT_NAME = 'EXPERIMENT-NAME'
    INFO_BOARD_NAME = 'BOARD-NAME'
    INFO_SETUP_NAME = 'SETUP-NAME'
    INFO_SUBJECT_NAME = 'SUBJECT-NAME'
    INFO_BPODGUI_VERSION = 'BPOD-GUI-VERSION'

    def __init__(self, project):
        BoardIO.__init__(self, project)
        self.status = BoardCom.STATUS_READY

    ##########################################################################
    ####### PROPERTIES #######################################################
    ##########################################################################

    @property
    def status(self):
        """
        Get and set the board status

        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

        # in case a session is running update the status of this sessions
        if not hasattr(self, '_running_session'):
            return

        session = self._running_session
        if value == self.STATUS_READY:
            session.status = session.STATUS_READY
        elif value == self.STATUS_RUNNING_TASK:
            session.status = session.STATUS_SESSION_RUNNING

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def pause_trial(self):
        if hasattr(self, 'proc'):
            self.proc.stdin.write("pause-trial\r\n".encode())
            self.proc.stdin.flush()

    def resume_trial(self):
        if hasattr(self, 'proc'):
            self.proc.stdin.write("resume-trial\r\n".encode())
            self.proc.stdin.flush()

    def stop_trial(self):
        if hasattr(self, 'proc'):
            self.proc.stdin.write("stop-trial\r\n".encode())
            self.proc.stdin.flush()

    def stop_task(self):
        if hasattr(self, 'proc'):
            self.proc.stdin.write("close\r\n".encode())
            self.proc.stdin.flush()
    
    def kill_task(self):
        if hasattr(self, 'proc'):
            self.proc.stdin.write("kill\r\n".encode())
            self.proc.stdin.flush()

    def log2board(self, data):
        """
        Function used to update the board log
        """
        pass

    def freegui(self):
        """
        Function used to release the processing to update the GUI events
        """
        pass

    def run_task(self, session, board_task, workspace_path, detached=False):
        """
        Run a task.

        :ivar Session session: Session to record the data.
        :ivar BoardTask board_task: Configuration to run session.
        :ivar str workspace_path: Not used. To be removed in the future.
        """
        session.subjects = [str([s.name, str(s.uuid4)]) for s in board_task.setup.subjects]

        xt_user = ''
        xt_subject = ''
        if hasattr(conf, 'PYBPOD_EXTRA_INFO'):
            if 'Users' in conf.PYBPOD_EXTRA_INFO:
                xt_user = session.user.toJSON()
            if 'Subjects' in conf.PYBPOD_EXTRA_INFO:
                xt_subject = []
                for sbj in board_task.setup.subjects:
                    xt_subject.append(sbj.toJSON())

        self._running_detached = detached
        self._running_boardtask = board_task
        self._running_task = board_task.task
        self._running_session = session

        board = board_task.board

        # create the session path
        Path(session.path).mkdir(parents=True, exist_ok=True)

        # load bpod configuration template
        template = os.path.join(os.path.dirname(__file__), 'run_settings_template.py')
        bpod_settings = open(template, 'r').read().format(
            serialport=board.serial_port,
            bnp_ports=('BPOD_BNC_PORTS_ENABLED = {0}'.format(board.enabled_bncports) if board.enabled_bncports else ''),
            wired_ports=('BPOD_WIRED_PORTS_ENABLED = {0}'.format(board.enabled_wiredports) if board.enabled_wiredports else ''),
            behavior_ports=('BPOD_BEHAVIOR_PORTS_ENABLED = {0}'.format(board.enabled_behaviorports) if board.enabled_behaviorports else ''),
            session_name=session.name,
            netport=board_task.board.net_port,
            stream2stdout=not detached,
            project=session.project.name,
            experiment=session.setup.experiment.name,
            board=board_task.board.name,
            setup=session.setup.name,
            session=session.name,
            protocolname=board_task.task.name,
            session_path=os.path.abspath(session.path).encode('unicode_escape').decode(),
            subjects=','.join(list(map(lambda x: '"'+str(x)+'"', session.subjects))),
            user=json.dumps([session.user.name, str(session.user.uuid4), session.user.connection] if session.user.uuid4 else None),
            subject_extra=','.join(list(map(lambda x: '"'+str(x)+'"', xt_subject))),
            user_extra=xt_user,
            variables_names=','.join(["'"+var.name+"'" for var in board_task.variables]),
            bpod_firmware_version=conf.TARGET_BPOD_FIRMWARE_VERSION
        )

        for var in board_task.variables:
            bpod_settings += "\n"+str(var)

        # create the bpod configuration file in the session folder
        settings_path = os.path.join(self._running_session.path, 'user_settings.py')
        with open(settings_path, 'w') as out:
            out.write(bpod_settings)

        # create the bpod configuration file in the session folder
        init_path = os.path.join(self._running_session.path, '__init__.py')
        with open(init_path, 'w') as out:
            pass

        ## Execute the PRE commands ###################################
        for cmd in board_task.task.commands:
            if cmd.when == 0:
                try:
                    cmd.execute(session=session)
                except Exception as err:
                    traceback.print_exc()
                    self.alert(str(err), "Unexpected error when executing a pre-command.")
        ###############################################################

        task = board_task.task

        self.start_run_task_handler()

        enviroment = os.environ.copy()
        enviroment['PYTHONPATH'] = os.pathsep.join([os.path.abspath(self._running_session.path)]+sys.path)

        if detached:
            self.proc = subprocess.Popen(
                ['python', os.path.abspath(task.filepath)],
                stdin=subprocess.PIPE,
                cwd=self._running_session.path,
                env=enviroment
            )
        else:
            session.data = pd.DataFrame(columns=['TYPE', 'PC-TIME', 'BPOD-INITIAL-TIME', 'BPOD-FINAL-TIME', 'MSG', '+INFO'])

            self.proc = subprocess.Popen(
                ['python', os.path.abspath(task.filepath)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self._running_session.path,
                env=enviroment
            )
            self.csvreader = NonBlockingCSVReader(
                csv.reader(io.TextIOWrapper(self.proc.stdout, encoding='utf-8'),
                           delimiter=CSV_DELIMITER,
                           quotechar=CSV_QUOTECHAR,
                           quoting=CSV_QUOTING)
            )
            self.stderrstream = NonBlockingStreamReader(self.proc.stderr)

    def run_task_handler(self, flag=True):

        if not self._running_detached:
            row = self.csvreader.readline()
            data = ''
            while row is not None:
                if row is None:
                    break
                if len(row) == 6:
                    self._running_session.data.loc[len(self._running_session.data)] = row

                if self._running_session.uuid4 is None and len(row) == 2 and row[0] == '__UUID4__':
                    self._running_session.uuid4 = row[1]

                if len(row) > 0:
                    data += str(row)+'\n'

                self.freegui()
                row = self.csvreader.readline()

            if len(data) > 0:
                self.log2board(data)

            errline = self.stderrstream.readline()
            if errline is not None:
                self.log2board(errline)

        if flag and self.proc.poll() is not None:
            self.end_run_task_handler()

    def start_run_task_handler(self):
        self.status = self.STATUS_RUNNING_TASK

    def stop_thread(self):
        pass

    def end_run_task_handler(self):
        self.stop_thread()

        if not self._running_detached:
            # in case it is running detached
            errline = self.stderrstream.readline()
            if errline is not None:
                self.log2board(errline)

        # del self.proc

        session = self._running_session

        filepath = os.path.join(session.path, session.name+'.csv')
        session.filepath = filepath if os.path.exists(filepath) else None

        ## Execute the POST commands ##################################
        for cmd in self._running_task.commands:
            if cmd.when == 1:
                try:
                    cmd.execute(session=session)
                except Exception as err:
                    traceback.print_exc()
                    self.alert(str(err), "Unexpected error when executing the post-command")

        ###############################################################

        self.status = self.STATUS_READY

        if self._running_detached:
            session.load_contents()

        if session.data is not None:
            res = session.data.query("MSG=='{0}'".format(Session.INFO_SESSION_ENDED))
            for index, row in res.iterrows():
                session.ended = date_parser.parse(row['+INFO'])

            board_task = self._running_boardtask

            if board_task.update_variables:
                for var in board_task.variables:
                    res = session.data.query("TYPE=='VAL' and MSG=='{0}'".format(var.name))
                    for index, row in res.tail(1).iterrows():
                        value = row['+INFO']
                        if var.datatype == 'string':
                            var.value = value
                        else:
                            value.isdigit()
                            var.datatype == float(value)
