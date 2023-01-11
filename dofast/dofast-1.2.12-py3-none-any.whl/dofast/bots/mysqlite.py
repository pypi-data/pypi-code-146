#!/usr/bin/env python
import datetime
import sqlite3

class Message(object):

    def __init__(self, db_file='botmsg.db'):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS botmsg (
            id INTEGER PRIMARY KEY,
            date TEXT,
            msg TEXT)''')

    def add(self, message: str):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.cursor.execute('''INSERT INTO botmsg (date, msg) VALUES (?, ?)''',
                            (date, message))
        self.conn.commit()

    def get(self, date: str):
        self.cursor.execute('''SELECT msg FROM botmsg WHERE date = ?''',
                            (date, ))
        return self.cursor.fetchone()[0]


