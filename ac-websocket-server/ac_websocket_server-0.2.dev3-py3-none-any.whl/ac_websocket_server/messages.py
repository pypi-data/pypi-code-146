'''Assetto Corsa WebSockets Server Messages'''

from dataclasses import dataclass
from enum import Enum
from typing import Union

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DriverInfo:
    '''Represents a driver.'''
    name: str = ''
    host: str = ''
    port: int = 0
    car: str = ''
    guid: str = ''
    ballast: int = 0
    msg: str = ''


@dataclass_json
@dataclass
class ServerInfo:
    '''Represents version information for a server.'''

    version: str = ''
    timestamp: str = ''
    track: str = ''
    cars: str = ''
    msg: str = ''


@dataclass_json
@dataclass
class SessionInfo:
    '''Represents an individual session in the AC game server'''

    type: str = ''
    laps: int = 0
    time: int = 0
    msg: str = ''


class MessageType(Enum):
    '''Allowable message types'''

    DRIVER_INFO = 'DriverInfo'
    SERVER_INFO = 'ServerInfo'
    SESSION_INFO = 'SessionInfo'


MessageBody = Union[DriverInfo, ServerInfo, SessionInfo]


@dataclass_json
@dataclass
class Message:
    '''Basic message structure'''
    type: MessageType
    body: MessageBody
