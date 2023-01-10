#!/usr/bin/env python
import time
from logging import warning
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import os
import json
from codefast.ds import fplist as lis


class SQLite(object):
    """ simple key-value database implementation using expiringdict
    """

    def __init__(self, config_file: str = '/data/psdbcloud.json'):
        '''
        '''
        if not os.path.exists(config_file):
            raise Exception('config file not found: %s' % config_file)
        config = json.load(open(config_file, 'r'))
        import pymysql
        self.conn = pymysql.connect(host=config["host"],
                                    user=config["user"],
                                    passwd=config["password"],
                                    db=config["db"],
                                    cursorclass=pymysql.cursors.DictCursor,
                                    ssl={"ca": "/etc/ssl/certs/ca-certificates.crt"})
        self.cur = self.conn.cursor()
        cmd = "CREATE TABLE IF NOT EXISTS `db`(`key` TEXT NOT NULL PRIMARY KEY, `value` TEXT NOT NULL, PRIMARY KEY (`key`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
        self.cur.execute(cmd)
        self.conn.commit()

    def clear(self):
        cmd = "TRUNCATE TABLE db"
        self.cur.execute(cmd)

    def set(self, key: str, value: str, eager_mode: bool = False) -> 'self':
        """ set key-value
        if eager_mode is set, then the database will be synced after each set.
        """
        self.pop(key)
        cmd = "INSERT IGNORE INTO db (`key`, `value`) VALUES (%s, %s)"
        self.cur.execute(cmd, (key, value))
        if eager_mode:
            self.sync()
        return self

    def sync(self) -> 'self':
        self.conn.commit()

    def get(self, key: str) -> Union[str, None]:
        cmd = "SELECT `value` FROM db WHERE `key` = %s"
        resp = self.cur.execute(cmd, (key,))
        resp = self.cur.fetchone()
        if resp:
            return resp['value']
        return None

    def sample(self, n: int) -> List[Tuple[str, str]]:
        cmd = "SELECT `key`, `value` FROM db ORDER BY RANDOM() LIMIT %s"
        resp = self.cur.execute(cmd, (n,))
        resp = self.cur.fetchall()
        return resp

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    def keys(self) -> List[str]:
        cmd = "SELECT `key` FROM db"
        self.cur.execute(cmd)
        resp = lis(self.cur.fetchall())
        return resp.each(lambda x: x[0]).data

    def values(self) -> List[str]:
        cmd = "SELECT `value` FROM db"
        self.cur.execute(cmd)
        resp = lis(self.cur.fetchall())
        return resp.each(lambda x: x[0]).data

    def pop(self, key: str) -> str:
        """ pop key-value
        """
        cmd = "DELETE FROM db WHERE `key` = %s"
        resp = self.cur.execute(cmd, (key,))
        resp = self.cur.fetchone()
        self.conn.commit()
        return resp['value'] if resp else None

    def __getitem__(self, key: str) -> Union[str, None]:
        return self.get(str(key))

    def __setitem__(self, key: str, value: str) -> None:
        self.set(str(key), str(value))

    def items(self) -> List[Dict[str, str]]:
        cmd = "SELECT `key`, `value` FROM db"
        self.cur.execute(cmd)
        return self.cur.fetchall()

    def delete(self, key: str) -> None:
        return self.pop(str(key))

    def __len__(self) -> int:
        cmd = "SELECT COUNT(*) as LEN FROM db"
        self.cur.execute(cmd)
        resp = self.cur.fetchone()
        return resp['LEN']

    def len(self) -> int:
        return len(self)

    def __repr__(self) -> str:
        return 'DBLite(%s)' % self.to_dict()

    def to_dict(self) -> Dict:
        """Export content of the database as a normal dict."""
        return dict(self.items())
