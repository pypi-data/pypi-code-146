# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import pybpodgui_api
from sca.formats import json
from pybpodgui_api.models.task.task_base import TaskBase

logger = logging.getLogger(__name__)


class TaskIO(TaskBase):
    """
    Task I/O operations
    """

    def __init__(self, project=None):
        super(TaskIO, self).__init__(project)

        self.data = None

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def save(self):
        """
        Save setup data on filesystem.

        :ivar str project_path: Project path.
        :ivar dict data: Dictionary where to save the data to.
        :return: Dictionary containing the task info to save.
        :rtype: dict
        """

        if (self.path and not os.path.exists(self.path)) or not self.path:
            self.make_path()

        if (self.filepath and not os.path.exists(self.filepath)) or not self.filepath:
            self.filepath = self.make_emptyfile()

        """
        current_path     = os.path.dirname(self.filepath)
        current_filename = os.path.basename(self.filepath)
        future_path      = self.path

        if current_path!=future_path:
            shutil.move( current_path, future_path )
            current_filepath = os.path.join(future_path, current_filename)
            future_filepath  = os.path.join(future_path, self.name+'.py')
            shutil.move( current_filepath, future_filepath )
        """

        if self.data:
            data = self.data
        else:
            data = json.scadict(
                uuid4_id=self.uuid4,
                software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                def_url='http://pybpod.readthedocs.org',
                def_text='This file contains information about a PyBpod protocol.'
            )
        data['name'] = self.name
        data['trigger-softcodes'] = self.trigger_softcodes
        data['commands'] = [cmd.save() for cmd in self.commands]

        config_path = os.path.join(self.path, self.name+'.json')
        with open(config_path, 'w') as fstream:
            json.dump(data, fstream)

    def load(self, path):
        """
        Load setup data from filesystem

        :ivar str task_path: Path of the task
        :ivar dict data: data object that contains all task info
        """
        self.name = os.path.basename(path)

        config_path = os.path.join(self.path, self.name+'.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as stream:
                self.data = data = json.load(stream)
                self.uuid4 = data.uuid4 if data.uuid4 else self.uuid4
                self.filepath = os.path.join(self.path, self.name+'.py')
        else:
            self.data = data = {}

        self.trigger_softcodes = data.get('trigger-softcodes', None)

        for cmddata in data.get('commands', []):
            cmd = getattr(self, cmddata['type'])()
            cmd.load(cmddata)

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'trigger_softcodes': self.trigger_softcodes})

        data.update({'commands': []})

        for cmd in self.commands:
            data['commands'].append(cmd.collect_data({}))

        return data
