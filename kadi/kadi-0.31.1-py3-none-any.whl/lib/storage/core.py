# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from abc import ABC
from abc import abstractmethod

from flask import current_app


class BaseStorage(ABC):
    """Base class for all storage providers.

    :param storage_type: The unique type of the storage.
    :param storage_name: (optional) A user-readable name of the storage. Defaults to the
        given storage type.
    :param max_size: (optional) The maximum file size for the storage to accept when
        saving files.
    """

    # pylint: disable=missing-function-docstring

    def __init__(self, storage_type, storage_name=None, max_size=None):
        self.max_size = max_size
        self._storage_type = storage_type
        self._storage_name = storage_name if storage_name is not None else storage_type

    @property
    def storage_type(self):
        return self._storage_type

    @property
    def storage_name(self):
        return self._storage_name

    @abstractmethod
    def exists(self, filepath):
        pass

    @abstractmethod
    def open(self, filepath, mode="rb", encoding=None):
        pass

    @abstractmethod
    def close(self, file):
        pass

    @abstractmethod
    def save(self, dst, file_or_src, append=False):
        pass

    @abstractmethod
    def move(self, src, dst):
        pass

    @abstractmethod
    def delete(self, filepath):
        pass

    @abstractmethod
    def ensure_filepath_exists(self, filepath):
        pass

    @abstractmethod
    def get_mimetype(self, filepath):
        pass

    @abstractmethod
    def get_size(self, filepath):
        pass

    @abstractmethod
    def validate_size(self, filepath, size, op="=="):
        pass

    @abstractmethod
    def get_checksum(self, filepath):
        pass

    @abstractmethod
    def validate_checksum(self, filepath, expected, actual=None):
        pass

    @abstractmethod
    def create_filepath(self, file_identifier):
        pass


def get_storages():
    """Get all registered storages.

    :return: The storages.
    """
    return current_app.config["STORAGES"]


def get_storage(storage_type):
    """Get a registered storage for a given storage type.

    :param storage_type: The storage type.
    :return: The storage or ``None`` if no storage could be found.
    """
    return current_app.config["STORAGES"].get(storage_type)
