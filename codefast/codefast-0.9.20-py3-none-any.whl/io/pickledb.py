#!/usr/bin/env python
import atexit
import os
import pickle
import time
from logging import warning
from typing import Any, Dict, List, Optional, Set, Tuple, Union

try:
    import expiringdict
except ImportError:
    print('install expiringdict ...')
    os.system('pip install expiringdict')


class PickleDB(object):
    """ simple key-value database implementation using expiringdict
    """

    def __init__(self,
                 db_file: str = '/tmp/pickle.db',
                 max_len: int = 100000,
                 max_age_seconds: int = 86400 * 30,
                 delay_write: bool = True) -> None:
        '''
        Args:
            delay_write(bool): if True, then data will only persist to disk at most once
            per second, which will save time when dumping data frequently for a long period of time.

            max_len(int): max length of the database. If max length is too large, the write speed will 
            be painfully slow. Based on our experience, max_len <= 800000 will be a good choice.
        '''
        if max_len > 800000:
            warning(
                'max_len {} is too large, the performance will be affected.'.
                format(max_len))
        self.db_file = db_file
        self.max_len = max_len
        self.max_age_seconds = max_age_seconds
        self.delay_write = delay_write
        self.db = expiringdict.ExpiringDict(max_len, max_age_seconds)
        self._persist_time = expiringdict.ExpiringDict(
            max_len, max_age_seconds)
        if os.path.exists(db_file):
            self.db.update(pickle.load(open(db_file, 'rb')))
        atexit.register(self.safe_exit)
    
    def set(self, key: str, value: str) -> bool:
        """ set key-value
        """
        self.db[key] = value
        if self.delay_write:
            now_second = int(time.time())
            if now_second not in self._persist_time:
                self._persist_time[now_second] = 1
            else:
                return True
        pickle.dump(self.db, open(self.db_file, 'wb'))

    def get(self, key: str) -> Union[str, None]:
        return self.db.get(key, None)

    def exists(self, key: str) -> bool:
        return key in self.db

    def keys(self) -> List[str]:
        return self.db.keys()

    def values(self) -> List[str]:
        return self.db.values()

    def pop(self, key: str) -> str:
        """ pop key-value
        """
        return self.db.pop(key)

    def rpush(self, list_name: str, value: str) -> None:
        self.db.setdefault(list_name, []).append(value)

    def lpush(self, list_name: str, value: str) -> None:
        self.db.setdefault(list_name, []).insert(0, value)

    def blpop(self, list_name: str, timeout: int = 30) -> Tuple[str, Union[str, None]]:
        """ always return a tuple. 
        """
        while timeout > 0:
            if list_name in self.db and len(self.db[list_name]) > 0:
                return list_name, self.db[list_name].pop(0)
            time.sleep(1)
            timeout -= 1
        return list_name, None

    def __getitem__(self, key: str) -> Union[str, None]:
        return self.db.get(key, None)

    def __setitem__(self, key: str, value: str) -> None:
        self.set(key, value)

    def items(self) -> List[Tuple[str, str]]:
        return self.db.items()

    def delete(self, key: str) -> None:
        self.db.pop(key)

    def __len__(self) -> int:
        return len(self.db)

    def __repr__(self) -> str:
        return f'PickleDB(db_file={self.db_file}, max_len={self.max_len}, max_age_seconds={self.max_age_seconds})'

    def __iter__(self) -> List[str]:
        return self.db.__iter__()

    def safe_exit(self):
        """ save data when exit
        """
        pickle.dump(self.db, open(self.db_file, 'wb'))

    def to_dict(self)->Dict:
        """Export content of the database as a normal dict."""
        return dict(self.db)
