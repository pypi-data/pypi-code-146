from __future__ import annotations

from enum import Enum
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LoggerLevel(TcBaseObj):
    """
    Logger name and logging priority level of each of the loggers.
    
    :var loggerName: Name of the logger
    :var priority: Logging priority level of the logger
    """
    loggerName: str = ''
    priority: LogLevel = None


@dataclass
class LoggerLevelResponse(TcBaseObj):
    """
    Logger name and current log level of each of the loggers
    
    :var loggerList: List of loggers, and the corresponding log level
    """
    loggerList: List[LoggerLevel] = ()


@dataclass
class ModuleStatus(TcBaseObj):
    """
    Set the journaling status for the module with the given name
    
    :var status: true if module needs to be turned on for journaling.
    :var moduleName: Name of the journaling module
    """
    status: bool = False
    moduleName: str = ''


@dataclass
class ModuleStatusResponse(TcBaseObj):
    """
    Get module name and the current status of the module.
    
    :var moduleList: Vector of module name and status.
    """
    moduleList: List[ModuleStatus] = ()


@dataclass
class ReturnStatus(TcBaseObj):
    """
    Returns status of checking, journaling, statistics, TAO level, and SQL logging.
    
    :var checkingStatus: Checking level, returns integer, 0, 1, or 2.  The checking level is used in low level  libsyss
    framework code, to control the extent of runtime diagnostic checking.
    - 0 production mode
    - 1 checking on
    - 2 extensive checking.
    
    
    :var journalStatus: True if entries are being written to the journal file,  false otherwise.
    :var statisticsStatus: True if summary statistics are collected, false otherwise.True if summary statistics are
    collected, false otherwise.
    :var taoStatus: An integer 0 through 10 representing the TAO (CORBA server) log level.
    :var sqlLogStatus: A structure holding the various SQL Logging settings.
    """
    checkingStatus: int = 0
    journalStatus: bool = False
    statisticsStatus: bool = False
    taoStatus: int = 0
    sqlLogStatus: SQLLogInfo = None


@dataclass
class SQLLogInfo(TcBaseObj):
    """
    A structure containing SQL logging option settings.
    
    :var debugState: True if SQL debug information is written to the syslog file, false otherwise.  This must be true
    for the other SQL debug settings to take effect.
    :var showBindVariables: True if SQL bind variables and their values are shown, false otherwise.
    :var profile: True if SQL profiling information is shown, false otherwise.
    :var toJournal: True if the SQL debug information is written to the journal file as well as to the syslog.  False
    if the SQL debug information is written only to the syslog file.
    :var timing: True if SQL statement timing information is shown, false otherwise.
    """
    debugState: bool = False
    showBindVariables: bool = False
    profile: bool = False
    toJournal: bool = False
    timing: bool = False


@dataclass
class SQLLogInfoResponse(TcBaseObj):
    """
    Current status of SQL logging settings.
    
    :var sqlLogInfo: A structure containing SQL logging settings.
    """
    sqlLogInfo: SQLLogInfo = None


@dataclass
class TAOLogLevelResponse(TcBaseObj):
    """
    Structure holding the TAO log level.
    
    :var level: The current TAO log level.
    """
    level: int = 0


@dataclass
class CheckingLevelResponse(TcBaseObj):
    """
    Checking level
    
    :var level: Checking level 0, 1, or 2.
    """
    level: int = 0


class LogLevel(Enum):
    """
    Enumerated list of logger priority levels
    """
    LOG_FATAL = 'LOG_FATAL'
    LOG_ERROR = 'LOG_ERROR'
    LOG_WARN = 'LOG_WARN'
    LOG_INFO = 'LOG_INFO'
    LOG_DEBUG = 'LOG_DEBUG'
    LOG_TRACE = 'LOG_TRACE'
    LOG_DEFAULT = 'LOG_DEFAULT'
