#!/usr/bin/env python3
import json
import sqlite3

import codefast as cf
import joblib
import nsq
import numpy as np
import pandas as pd
from rich import print

from bordercollie.auth import auth

dbfile = 'local/logs/log_{}.db'.format(cf.shell('hostname'))
print(dbfile)
db = sqlite3.connect(dbfile)
db.execute('create table if not exists log (md5 text primary key, msg text)')


def keep_newest(db_name: str):
    size = int(cf.shell('du -s {} | cut -f1'.format(db_name)))
    if size > 1000000:
        new_db_file = db_name + '.old'
        cf.shell('mv {} {}.'.format(db_name, new_db_file))


def persist_data(message):
    try:
        msg = json.loads(message.body)
    except json.decoder.JSONDecodeError as e:
        cf.warning({"msg": "json loads failed", "eroor": e})
        return True

    log = msg['log']
    md5 = cf.md5sum(log)
    db.execute(
        'insert into log (md5, msg) values (?, ?) on conflict (md5) do nothing',
        (md5, log))
    db.commit()
    # cf.info('data {} was persisted'.format(log))
    return True


if __name__ == '__main__':
    keep_newest(dbfile)

    r = nsq.Reader(message_handler=persist_data,
                   nsqd_tcp_addresses=['localhost:4150'],
                   topic='log',
                   channel='persist',
                   lookupd_poll_interval=3,
                   max_in_flight=10)
    nsq.run()
