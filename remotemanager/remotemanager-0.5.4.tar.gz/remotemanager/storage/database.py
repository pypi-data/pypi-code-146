import functools
import logging
import operator
import warnings

import yaml

from remotemanager.utils import get_version, ensure_filetype, \
    recursive_dict_update
from remotemanager.utils.version import Version


class Database:
    """
    Database file handler for use in the Dataset.

    .. warning::
        Interacting with this object directly could cause unstable behaviour.
        It is best to allow Dataset to handle the Database

    Args:
        file (str):
            filename to write to
    """

    _versionkey = '~database-version~'

    def __init__(self,
                 file):

        file = ensure_filetype(file, 'yaml')

        self._logger = logging.getLogger(__name__ + '.Database')

        self._path = file
        self._storage = self._read()
        self._tree = None

    def _read(self) -> dict:
        """
        Wipes the tree cache and reads from the database file, creating it if
        it does not already exist.
        """
        self._tree = None  # wipe tree cache
        self._logger.info(f'reading {self._path}')
        try:
            with open(self._path, 'r') as o:
                data = yaml.safe_load(o)
        except FileNotFoundError:
            self._logger.warning('file not found, creating')
            data = {Database._versionkey: get_version()}
            self._write(data)

        try:
            version = data.pop(Database._versionkey)
        except KeyError:
            version = "0.0.0"

        self._logger.info(f'database file version: {version}')

        if Version(version) < get_version():
            msg = f'database file (version {version}) is less than ' \
                  f'current remotemanager install version'
            warnings.warn(msg)
            self._logger.warning(msg)

        return data

    def _write(self, data: dict):
        """
        Clears the tree cache and writes to the file

        Args:
            data (dict):
                writes `data` to the database file
        """
        self._tree = None  # wipe tree cache

        data[Database._versionkey] = get_version()

        with open(self._path, 'w+') as o:
            yaml.dump(data, o)

    def read(self):
        """
        Read the database file
        """
        self._storage = self._read()

    def write(self):
        """
        Write the database to file
        """
        self._write(self._storage)

    def update(self, payload):
        """
        Update the database with payload (dict)

        Args:
            payload (dict):
                Dictionary to recursively update with. Usually called with the
                output of object.pack()
        """

        self._logger.info('updating stored info')

        self._storage = recursive_dict_update(self._storage, payload)
        self.write()

    @property
    def path(self):
        """
        Path to current database file
        """
        return self._path

    @property
    def tree(self) -> list:
        """
        Returns a list of path-like strings for the stored database dict

        Returns (list):
            List of path-like strings
        """
        if self._tree is not None:
            return self._tree
        self._tree = self.climb(self._storage)
        return self._tree

    def climb(self,
              data: dict,
              branch: list = None) -> list:
        """
        "climb" a dictionary tree, returning a list of path-like strings for
        each element

        .. note::
            This method is intended for use within the `tree` property, and
            could cause unintended behaviour if called directly, though will
            allow you to produce a `tree` like list for any dictionary. Use
            with caution.

        Args:
            data (dict):
                dictionary to treat
            branch (list):
                current branch, used for recursion

        Returns (list):
            list of path-like strings
        """

        if branch is None:
            branch = []

        joinchar = '/'

        ret = []

        if len(data) == 0:
            ret.append(joinchar.join(branch))

        for key in data:
            tmp = []
            if isinstance(data[key], dict):
                tmp.append(key)
                ret += self.climb(data[key], branch + tmp)
            else:
                ret.append(joinchar.join(branch + [key]))
        return ret

    def find(self,
             key: str):
        """
        Find the first instance of key within the database tree

        Args:
            key (str):
                key (uuid) to look for

        Returns:
            database tree below key
        """

        def get_minimum_path(p, k):
            fullpath = p.split('/')
            return fullpath[:fullpath.index(k)+1]

        target = []
        for path in self.tree:
            if key in path:
                target = get_minimum_path(path, key)
                break
        data = chain_get(self._storage, target)

        return data


def chain_get(d: dict,
              keys: str):
    """
    Get item from a nested dict using a list of keys

    Args:
        d (dict):
            nested dict to query
        keys (list):
            list of keys to use

    Returns:
        item from nested dict `d` at [list, of, keys]
    """
    return functools.reduce(operator.getitem, keys, d)
