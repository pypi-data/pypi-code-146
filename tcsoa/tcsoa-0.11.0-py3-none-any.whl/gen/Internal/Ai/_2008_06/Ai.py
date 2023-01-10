from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenerateMonolithicJtOptions(TcBaseObj):
    """
    Configuration structure.
    
    :var continueOnError: if 0 return on any error condition raised, 1 indicates to continue
    :var processIntermediateNodes: 0-no 1-replace 2-add
    :var remoteProcessing: false mean call API without TSTK, true-means use TSTK and return
    after waiting for number of seconds sepcified by waitSecondsAtServer for the translation to complete.
    In this case client must use EndGenerateMonolithicJt to see the status.
    :var waitSecondsAtServer: Used in case of TSTK.
    """
    continueOnError: int = 0
    processIntermediateNodes: int = 0
    remoteProcessing: bool = False
    waitSecondsAtServer: int = 0


@dataclass
class BeginGenerateMonolithicJtResponse(TcBaseObj):
    """
    BeginGenerateMonolithicJtResponse struct
    
    :var ticket: The transient file ticket to be used for downloading the generated monolithic jt file
    :var logFileticket: The transient file ticket to be used for downloading the generated log file
    :var request: If using TSTK, the Request object created for translation purposes
    :var currentState: If using TSTK the current state of the translation
    :var data: partial failures are returned - along with object ids for each plmxml data could not be generated.
    """
    ticket: str = ''
    logFileticket: str = ''
    request: BusinessObject = None
    currentState: str = ''
    data: ServiceData = None


@dataclass
class EndGenerateMonolithicJtResponse(TcBaseObj):
    """
    EndGenerateMonolithicJtResponse struct
    
    :var ticket: The transient file ticket to be used for downloading the generated monolithic jt file
    :var logFileticket: The transient file ticket to be used for downloading the generated log file
    :var currentState: If using TSTK the current state of the translation. Completed to mean - that the
    translation is done.
    :var data: data
    """
    ticket: str = ''
    logFileticket: str = ''
    currentState: str = ''
    data: ServiceData = None
