#!/usr/bin/env python
import hashlib
import os
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

from codefast.io.file import FileIO as fio


class osdb(object):
    """ simple key-value database implementation using expiringdict
    """

    def __init__(self, db_file: str = '/tmp/osdb'):
        '''
        Args:
            ...
        '''
        self.db_file = db_file
        self.key_path = os.path.join(self.db_file, 'keys')
        self.value_path = os.path.join(self.db_file, 'values')
        fio.rm(db_file)  # in case file with same name exists
        fio.rm(self.key_path)
        fio.rm(self.value_path)

        if not fio.exists(db_file):
            fio.mkdir(self.db_file)
        if not fio.exists(self.key_path):
            fio.mkdir(self.key_path)
        if not fio.exists(self.value_path):
            fio.mkdir(self.value_path)

    def kpath(self, key: str) -> str:
        return os.path.join(self.key_path,
                            hashlib.md5(str(key).encode()).hexdigest())

    def vpath(self, key: str) -> str:
        return os.path.join(self.value_path,
                            hashlib.md5(str(key).encode()).hexdigest())

    def set(self, key: str, value: str):
        with open(self.vpath(key), 'w') as f:
            f.write(str(value))

        with open(self.kpath(key), 'w') as f:
            f.write(str(key))

    def get(self, key: str) -> Union[str, None]:
        try:
            return fio.reads(self.vpath(key))
        except:
            return None

    def exists(self, key: str) -> bool:
        return fio.exists(self.kpath(key))

    def keys(self) -> Iterator[str]:
        try:
            for k in fio.walk(self.key_path):
                yield fio.reads(k).strip()
        except:
            yield from []

    def values(self) -> Iterator[str]:
        for k in fio.walk(self.value_path):
            yield fio.reads(k)

    def pop(self, key: str) -> str:
        """ pop key-value
        """
        value = self.get(key)
        fio.rm(self.kpath(key))
        fio.rm(self.vpath(key))
        return value

    def poplist(self, keylist: List[str]) -> str:
        """ pop key list
        """
        pass
        # values = []
        # for k in keylist:
        #     values.append(self.get(k))
        #     fio.rm(self.kpath(k))
        # keyset = set(keylist)
        # keys = [k for k in self.keys() if k not in keyset]
        # fio.write('\n'.join(keys), self.key_path)
        # return values
    def smembers(self, set_name: str) -> Set[str]:
        if self.exists(set_name):
            self.cutline = '-$-' * 10
            return set(self.get(set_name).split(self.cutline))
        else:
            return set()

    def sadd(self, set_name: str, value: str) -> None:
        """ add value to set"""
        if not self.exists(set_name):
            self.set(set_name, value)
        else:
            self.cutline = '-$-' * 10
            self.set(set_name, self.get(set_name) + self.cutline + value)

    def sdel(self, set_name: str, value: str) -> None:
        """ delete value from set
        """
        if self.exists(set_name):
            self.cutline = '-$-' * 10
            values = self.get(set_name).split(self.cutline)
            values = [v for v in values if v != value]
            self.set(set_name, self.cutline.join(values))

    def rpush(self, list_name: str, value: str) -> None:
        raise NotImplementedError

    def lpush(self, list_name: str, value: str) -> None:
        raise NotImplementedError

    def blpop(self,
              list_name: str,
              timeout: int = 30) -> Tuple[str, Union[str, None]]:
        """ always return a tuple. 
        """
        raise NotImplementedError

    def __getitem__(self, key: str) -> Union[str, None]:
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> None:
        self.set(key, value)

    def delete(self, key: str) -> None:
        return self.pop(key)

    def __len__(self) -> int:
        return len([k for k in self.keys()])

    def __repr__(self) -> str:
        return 'osdb(%s)' % self.db_file
