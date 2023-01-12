from .connection import Connection
from .exceptions import Error, ConnectionError, TimeoutError
from .principalserver import PrincipalServer, Region
from .server import Server

"""
pyvpsq.

Simple Python library for querying Valve's principal servers.
"""

__version__ = '0.1.0'
__author__ = 'cetteup'
__credits__ = [
    'https://github.com/ValvePython/steam',
    'https://developer.valvesoftware.com/wiki/Master_Server_Query_Protocol'
]
__all__ = ['Connection', 'PrincipalServer', 'Server', 'Region', 'Error', 'ConnectionError', 'TimeoutError']
