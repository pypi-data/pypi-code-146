#!/usr/bin/env python
import os

import codefast as cf
from cryptography.fernet import Fernet

from .accounts import accounts, paths


class Attrs(object):
    pass


def get_key() -> str:
    for p in paths:
        if p.startswith('~'):
            p = os.path.expanduser(p)
        try:
            return cf.io.reads(p).strip().encode()
        except FileNotFoundError:
            pass
    raise Exception('Fernet key not found')


def init_accounts() -> Attrs:
    key = get_key()
    fernet = Fernet(key)

    for k, v in accounts.items():
        key = fernet.decrypt(k.encode()).decode()
        val = fernet.decrypt(v.encode()).decode()
        setattr(Attrs, key, val)
    cert = '/etc/ssl/cert.pem'
    Attrs.ssl_cert = cert if os.path.exists(cert) else Attrs.ssl_cert
    return Attrs


Accounts = init_accounts()
