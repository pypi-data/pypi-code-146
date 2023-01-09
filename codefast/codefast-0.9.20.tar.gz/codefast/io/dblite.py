#!/usr/bin/env python
import time
from logging import warning
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from codefast.ds import fplist as lis


class DBLite(object):
    """ simple key-value database implementation using expiringdict
    """

    def __init__(self,
                 db_file: str = '/tmp/dblite.db',
                 max_len: int = 100000):
        '''
        Args:
            max_len(int): max length of the database. 
        '''
        import sqlite3 
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cur = self.conn.cursor()
        cmd = "CREATE TABLE IF NOT EXISTS db (key TEXT PRIMARY KEY, value TEXT, date TEXT)"
        self.cur.execute(cmd)
        self.conn.commit()
        self.max_len = max_len

    def set(self, key: str, value: str, eager_mode: bool = True) -> 'self':
        """ set key-value
        if eager_mode is set, then the database will be synced after each set.
        """
        cmd = "INSERT OR REPLACE INTO db (key, value, date) VALUES (?, ?, ?)"
        self.cur.execute(cmd, (key, value, time.time()))
        if eager_mode:
            self.sync()
        return self

    def sync(self) -> 'self':
        cmd = 'DELETE FROM db WHERE date NOT IN (SELECT date FROM db ORDER BY date DESC LIMIT ?)'
        self.cur.execute(cmd, (self.max_len,))
        self.conn.commit()

    def get(self, key: str) -> Union[str, None]:
        cmd = "SELECT value FROM db WHERE key = ?"
        resp = self.cur.execute(cmd, (key,)).fetchone()
        if resp:
            return resp[0]
        return None

    def sample(self, n: int) -> List[Tuple[str, str]]:
        cmd = "SELECT key, value FROM db ORDER BY RANDOM() LIMIT ?"
        resp = self.cur.execute(cmd, (n,)).fetchall()
        return resp

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    def keys(self) -> List[str]:
        cmd = "SELECT key FROM db"
        resp = lis(self.cur.execute(cmd).fetchall())
        return resp.each(lambda x: x[0]).data

    def values(self) -> List[str]:
        cmd = "SELECT value FROM db"
        resp = lis(self.cur.execute(cmd).fetchall())
        return resp.each(lambda x: x[0]).data

    def pop(self, key: str) -> str:
        """ pop key-value
        """
        cmd = "DELETE FROM db WHERE key = ?"
        resp = self.cur.execute(cmd, (key,)).fetchone()
        self.conn.commit()
        return resp[0] if resp else None

    def __getitem__(self, key: str) -> Union[str, None]:
        return self.get(str(key))

    def __setitem__(self, key: str, value: str) -> None:
        self.set(str(key), str(value))

    def items(self) -> List[Tuple[str, str]]:
        cmd = "SELECT key, value FROM db"
        resp = lis(self.cur.execute(cmd).fetchall())
        return resp.each(lambda x: (x[0], x[1])).data

    def delete(self, key: str) -> None:
        return self.pop(str(key))

    def __len__(self) -> int:
        cmd = "SELECT COUNT(*) FROM db"
        resp = self.cur.execute(cmd).fetchone()
        return resp[0]

    def len(self) -> int:
        return len(self)

    def __repr__(self) -> str:
        return 'DBLite(%s)' % self.to_dict()

    def to_dict(self) -> Dict:
        """Export content of the database as a normal dict."""
        return dict(self.items())
