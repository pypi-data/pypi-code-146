#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
import logging
import os

import dxpy
import requests

from soyuz.data.storages import DNAnexusStorage, ExodusStorage
from soyuz.dx.variables import Type, Property
from soyuz import __version__ as version
from soyuz.utils import UploaderException


class Record(object):
    __metaclass__ = ABCMeta

    def __init__(self, storage, basedir, name):
        self.storage = storage
        self.__id = None
        self.__details = None
        self.__tags = None
        self.__types = None
        self.__properties = None
        self.__record = None
        self.__basedir = basedir
        self.__name = name

    @abstractmethod
    def get_id(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def get_details(self):
        raise NotImplementedError()

    @abstractmethod
    def add_tags(self, tags):
        raise NotImplementedError()

    @abstractmethod
    def set_details(self, details):
        raise NotImplementedError()

    @abstractmethod
    def get_properties(self):
        raise NotImplementedError()

    @abstractmethod
    def set_properties(self, properties):
        raise NotImplementedError()

    @abstractmethod
    def add_property(self, key, value):
        raise NotImplementedError()


class DNAnexusRecord(Record):
    def __init__(self, storage, basedir, name):
        super(DNAnexusRecord, self).__init__(storage, basedir, name)
        self.__record = dxpy.new_dxrecord(types=[Type.UPLOAD_SENTINEL],
                                          folder=os.path.join(basedir, name).replace("\\", "/"),
                                          name="{}_upload_sentinel".format(name),
                                          properties={Property.RUN_FOLDER: name,
                                                      Property.VERSION: version},
                                          parents=True)

    def get_id(self):
        return self.__record.get_id()

    def close(self):
        return self.__record.close()

    def get_details(self):
        return self.__record.get_details()

    def set_details(self, details):
        return self.__record.set_details(details)

    def get_properties(self):
        return self.__record.get_properties()

    def set_properties(self, properties):
        return self.__record.set_properties(properties)

    def add_property(self, key, value):
        properties = self.__record.get_properties()
        properties[key] = value
        self.set_properties(properties)

    def add_tags(self, tags):
        return self.__record.add_tags(tags)


class ExodusRecord(Record):
    def __init__(self, storage, basedir, name):
        super(ExodusRecord, self).__init__(storage, basedir, name)
        self.__id = None
        self.__record = None
        self.__name = name
        self.__basedir = basedir
        self.__details = {}
        self.__properties = {Property.RUN_FOLDER: self.__name, Property.VERSION: version}
        self.__tags = []
        self.__types = []
        self.__base_headers = self.storage.base_headers
        self.exodus_url = self.storage.exodus_url
        self.exodus_username = self.storage.exodus_username
        self.exodus_password = self.storage.exodus_password

    def close(self):
        data = {'name': self.__name,
                'folder': os.path.join(self.__basedir, self.__name).replace("\\", "/"),
                'types': [Type.UPLOAD_SENTINEL],
                'properties': self.__properties,
                'tags': self.__tags,
                'details': self.__details
                }
        response = requests.post(os.path.join(self.exodus_url, "2.0/data/records/new"),
                                 json=data,
                                 auth=(self.exodus_username, self.exodus_password),
                                 headers=self.__base_headers)
        response.raise_for_status()
        data = response.json()
        self.__id = data['link']
        logging.info("Successfully created: {}".format(os.path.join(self.__basedir, self.__name)))
        return self.get_id()

    def get_id(self):
        return self.__id

    def get_details(self):
        return self.__details

    def set_details(self, details):
        self.__details = details

    def add_tags(self, tags):
        self.__tags.extend(tags)
        self.__tags = list(set(self.__tags))

    def get_properties(self):
        return self.__properties

    def set_properties(self, properties):
        self.__properties = dict(properties)

    def add_property(self, key, value):
        self.__properties[key] = value


class RecordFactory(object):
    @staticmethod
    def create(storage, basedir, name):
        if isinstance(storage, DNAnexusStorage):
            return DNAnexusRecord(storage, basedir, name)
        if isinstance(storage, ExodusStorage):
            return ExodusRecord(storage, basedir, name)
        raise UploaderException("Storage with name {} was not found".format(name))
