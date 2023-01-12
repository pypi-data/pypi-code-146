from __future__ import annotations

from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SupportedHandlerArgumentsInfoOutput(TcBaseObj):
    """
    SupportedHandlerArgumentsInfoOutput structure represents handler Data with dynamic hints.
    
    :var clientId: A unique string used to identify return data elements.
    :var handlerData: Handler Data with dynamic hints (as a JSON string). The following hints are included:
    &bull;    Mandatory Arguments
    &bull;    Optional arguments.
    &bull;    Mutex arguments.
    &bull;    Dependent arguments.
    &bull;    Nullable arguments.
    &bull;    Required one of arguments.
    &bull;    And argument values which allow only particular set of values for ex: list of object types, status,
    relations and LOVs.
    :var additionalData: This is a map that will point to a list of strings. It can be used incase there is a need to
    send any additional data.
    """
    clientId: str = ''
    handlerData: str = ''
    additionalData: HandlerKeyValuePair = None


@dataclass
class SupportedHandlerArgumentsInput(TcBaseObj):
    """
    SupportedHandlerArgumentsInput stucture represent the input handler name and clientId.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements.
    :var handlerName: Name of the handler.
    :var additionalData: This is a map that will point to a list of strings. It can be used incase there is a need to
    send any additional data as input to this operation.
    """
    clientId: str = ''
    handlerName: str = ''
    additionalData: HandlerKeyValuePair = None


@dataclass
class SupportedHandlerArgumentsReponse(TcBaseObj):
    """
    SupportedHandlerArgumentsReponse represents list of SupportedHandlerArgumentsInfoOutput which contains information
    about handlerData and clientId.
    
    :var output: List of SupportedHandlerArgumentsInfoOutput structure which contains handler data info.
    """
    output: List[SupportedHandlerArgumentsInfoOutput] = ()


"""
Structure for passing handler data in form of key and values.
"""
HandlerKeyValuePair = Dict[str, List[str]]
