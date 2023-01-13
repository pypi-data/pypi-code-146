# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging
import pybpodgui_api
from pybpodgui_api.models.board.board_base import BoardBase
from sca.formats import json


logger = logging.getLogger(__name__)


class BoardIO(BoardBase):
    """

    """

    def __init__(self, project):
        super(BoardIO, self).__init__(project)

        self.data = None

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'serial_port': self.serial_port})

        return data

    def save(self):
        """
        Save experiment data on filesystem.

        :ivar dict parent_path: Project path.
        :return: Dictionary containing the board info to save. If None is returned, it means that ther was a failure.
        :rtype: dict
        """
        if not self.name:
            logger.warning("Skipping board without name")
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
                    def_text='This file contains the configuration of Bpod board.'
                )
            data['serial-port'] = self.serial_port
            data['enabled-bncports'] = self.enabled_bncports
            data['enabled-wiredports'] = self.enabled_wiredports
            data['enabled-behaviorports'] = self.enabled_behaviorports
            data['net-port'] = self.net_port

            config_path = os.path.join(self.path, self.name+'.json')
            with open(config_path, 'w') as fstream:
                json.dump(data, fstream)

    def load(self, path):
        """
        Load board data from filesystem

        :ivar str board_path: Path of the board
        :ivar dict data: data object that contains all board info
        """
        self.name = os.path.basename(path)
        with open(os.path.join(self.path, self.name+'.json'), 'r') as stream:
            self.data = data = json.load(stream)

        self.uuid4 = data.uuid4 if data.uuid4 else self.uuid4
        self.serial_port = data.get('serial-port', data.get('serial_port', None))
        self.enabled_bncports = data.get('enabled-bncports', None)
        self.enabled_wiredports = data.get('enabled-wiredports', None)
        self.enabled_behaviorports = data.get('enabled-behaviorports', None)
        self.net_port = data.get('net-port', None)

    def __generate_boards_path(self, project_path):
        return os.path.join(project_path, 'boards')

    def __generate_board_path(self, boards_path):
        return os.path.join(boards_path, self.name)
