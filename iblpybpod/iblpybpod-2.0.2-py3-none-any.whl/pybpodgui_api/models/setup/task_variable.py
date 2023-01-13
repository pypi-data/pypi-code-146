# !/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class TaskVariable(object):
    def __init__(self, board_task, name=None, value=None, datatype='string'):
        self.board_task = board_task
        self.name = name
        self.value = value
        self.datatype = datatype

        board_task += self

    def __str__(self):
        return "{name} = {value}".format(
            name=self.name,
            value=("'"+self.value+"'") if self.datatype == 'string' else self.value
        )

    @property
    def name(self):
        """
        Get and set variable name

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def datatype(self):
        """
        Get and set variable data type. It can be from type 'number' or 'string'

        :rtype: str
        """
        return self._datatype

    @datatype.setter
    def datatype(self, value):
        self._datatype = value

    def collect_data(self, data):
        data.update({'name': str(self.name)})
        data.update({'value': self.value})
        data.update({'datatype': str(self.datatype)})
        return data

    def save(self):
        """
        Save variable data on filesystem.

        :ivar str setup_path: Setup path.
        :return: Dictionary containing the variable info to save.
        :rtype: dict
        """
        data2save = {}
        data2save.update({'name': str(self.name)})
        data2save.update({'value': self.value})
        data2save.update({'datatype': str(self.datatype)})
        return data2save

    def load(self, data):
        """
        Load variable data from filesystem

        :ivar dict data: data object that contains all task variable info
        """
        self.name = data['name']
        self.value = data['value']
        self.datatype = data['datatype']
