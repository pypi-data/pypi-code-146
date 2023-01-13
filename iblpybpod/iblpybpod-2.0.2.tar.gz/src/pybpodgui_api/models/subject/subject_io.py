# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging
import pybpodgui_api
from .subject_com import SubjectCom

from sca.formats import json

logger = logging.getLogger(__name__)


class SubjectIO(SubjectCom):
    """

    """

    def __init__(self, project):
        super().__init__(project)

        self.data = None

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def save(self):
        """
        Save subject data on filesystem.

        :ivar str project_path: Project path.
        :return: Dictionary containing the setup info to save.
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping subject without name")
            return None
        else:
            if not os.path.exists(self.path):
                os.makedirs(self.path)

            if self.data:
                data = self.data
            else:
                data = json.scadict(
                    uuid4_id=self.uuid4,
                    software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                    def_url='http://pybpod.readthedocs.org',
                    def_text='This file contains information about a subject used on PyBpod GUI.'
                )

            data['setup'] = str(self.setup.uuid4 if self.setup else None)

            config_path = os.path.join(self.path, self.name+'.json')
            with open(config_path, 'w') as fstream:
                json.dump(data, fstream)

    def toJSON(self):
        data = json.scadict(
                    uuid4_id=self.uuid4,
                    software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                    def_url='http://pybpod.readthedocs.org',
                    def_text='This file contains information about a subject used on PyBpod GUI.',
                )
        data['name'] = self.name
        data['setup'] = str(self.setup.uuid4 if self.setup else None)
        data['uuid4'] = self.uuid4

        return json.dumps(data)

    def load(self, path):
        """
        Load subject data from filesystem

        :ivar str subject_path: Path of the subject
        :ivar dict data: data object that contains all subject info
        """
        self.name = os.path.basename(path)

        try:
            with open(os.path.join(self.path, self.name+'.json'), 'r') as stream:
                self.data = data = json.load(stream)
            self.uuid4 = data.uuid4 if data.uuid4 else self.uuid4

            self._setup_id = self.data.get('setup', None)
        except:
            raise Exception('There was an error loading the configuration file for the subject [{name}]. File not found.'.format(name=self.name))

    def post_load(self):
        self.setup = self.project.find_setup_by_id(self._setup_id) if hasattr(self, "_setup_id") else None

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'setup': str(self.setup.uuid4 if self.setup else None)})
        return data
