# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import shutil
import pybpodgui_api
from pybpodgui_api.models.setup.setup_base import SetupBase

from sca.formats import json

logger = logging.getLogger(__name__)


class SetupBaseIO(SetupBase):

    def __init__(self, experiment):
        super(SetupBaseIO, self).__init__(experiment)

        # initial name. Used to track if the name was updated
        self.initial_name = None
        self.data = None

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'board_uuid4': str(self.board.uuid4 if self.board else None)})
        data.update({'task': str(self.task.uuid4 if self.task else None)})
        self.board_task.collect_data(data)

        data.update({'sessions': []})

        for session in self.sessions:
            data['sessions'].append(session.collect_data({}))

        return data

    def save(self):
        """
        Save setup data on filesystem.

        :ivar str parent_path: Experiment path.  
        :return: Dictionary containing the setup info to save.  
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping setup without name")
        else:

            if self.initial_name is not None:
                initial_path = os.path.join(self.experiment.path, 'setups', self.initial_name)

                if initial_path != self.path:
                    shutil.move(initial_path, self.path)
                    current_filepath = os.path.join(self.path, self.initial_name+'.json')
                    future_filepath = os.path.join(self.path, self.name+'.json')
                    shutil.move(current_filepath, future_filepath)

            if not os.path.exists(self.path):
                os.makedirs(self.path)

            # save sessions
            for session in self.sessions:
                session.save()

            self.project.remove_non_existing_repositories(
                os.path.join(self.path, 'sessions'),
                [session.name for session in self.sessions]
            )

            if self.data:
                data = self.data
            else:
                data = json.scadict(
                    uuid4_id=self.uuid4,
                    software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                    def_url='http://pybpod.readthedocs.org',
                    def_text='This file contains information about a PyBpod experiment setup.'
                )
            data['board'] = self.board.name if self.board else None
            data['task'] = self.task.name if self.task else None
            data['subjects'] = [subject.name for subject in self.subjects]
            data['detached'] = self.detached

            # collect board_task data
            for key, value in self.board_task.save().items():
                data[key] = value

            if self.board:
                data.add_external_ref(self.board.uuid4)

            for subject in self.subjects:
                data.add_external_ref(subject.uuid4)

            config_path = os.path.join(self.path, self.name+'.json')
            with open(config_path, 'w') as fstream:
                json.dump(data, fstream)

            self.initial_name = self.name

    def load(self, path):
        """
        Load setup data from filesystem

        :ivar str setup_path: Path of the setup
        :ivar dict data: data object that contains all setup info
        """
        self.name = os.path.basename(path)
        with open(os.path.join(self.path, self.name+'.json'), 'r') as stream:
            self.data = data = json.load(stream)
        self.uuid4 = data.uuid4 if data.uuid4 else self.uuid4

        self.initial_name = self.name
        self.board = data.get('board', None)
        self.task = data.get('task', None)

        self.detached = data.get('detached', False)
        self.board_task.load(data)

        for subject_name in data.get('subjects', []):
            self += self.project.find_subject(subject_name)

        sessionspath = os.path.join(self.path, 'sessions')
        if os.path.exists(sessionspath):
            for name in sorted(os.listdir(sessionspath)):
                if os.path.isfile(os.path.join(sessionspath, name)):
                    continue
                session = self.create_session()
                session.load(os.path.join(sessionspath, name))

        self._sessions = sorted(self.sessions, key=lambda x: x.started, reverse=True)
