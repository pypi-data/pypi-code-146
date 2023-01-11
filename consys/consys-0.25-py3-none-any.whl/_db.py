"""
Database
"""

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def get_db(host, name, login=None, password=None):
    """ Initialize the database """

    params = {
        'host': host,
        'port': 27017,
    }

    if login and password:
        params['username'] = login
        params['password'] = password
        params['authSource'] = 'admin'
        params['authMechanism'] = 'SCRAM-SHA-1'

    return MongoClient(**params)[name]


__all__ = (
    'get_db',
    'DuplicateKeyError',
)
