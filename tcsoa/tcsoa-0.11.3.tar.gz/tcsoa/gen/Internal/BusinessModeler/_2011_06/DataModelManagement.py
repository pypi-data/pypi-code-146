from __future__ import annotations

from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ServerCacheResponse(TcBaseObj):
    """
    ServerCacheResponse structure represents the error code that could occur during the creation or deletion of the
    Metadata cache and corresponding log file tickets.
    
    :var errorCode: Error code for the cache creation process. It is the error code returned by the server if there is
    any error during cache generation or deletion.
    :var logFileTickets: Log file tickets corresponding to each log file generated. These are the FMS file tickets that
    BMIDE uses to retrieve the log files to be displayed to the BMIDE user.
    """
    errorCode: int = 0
    logFileTickets: List[str] = ()
