from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OccurenceInfo(TcBaseObj):
    """
    The structure contains information that represents occurrence.
    
    :var occThreadsChain: The uid strings of occurrence threads tha represent occurrences in the tree.
    :var stockAbleOccThread: The stock able occurrence - highest occurence level for setting IDIC. This parameter is
    optional and is used for perfomance reason - minimize the number of object to set IDIC. If stock able occurrence is
    received, IDIC is created for this occurence and remaining occurrence thread chain is concatenated with IDIC and
    returned to the client.
    :var clientID: A unique string supplied by the caller. This ID is used to identify return data elements.
    """
    occThreadsChain: List[str] = ()
    stockAbleOccThread: str = ''
    clientID: str = ''


@dataclass
class OccurrenceIDIC(TcBaseObj):
    """
    The structure contains IDIC uid string of occurrence.
    
    :var returnID: The new created IDIC. If stockAbleOccThread is received, the server returns a new IDIC for the stock
    able occurrence , concatenated with the remaining occurrence thread IDs in the following way:
    returnID = IDIC_of_stockAbleOcc/cloneStableID_of_occthread1/cloneStableID_of_occthread2/cloneStableID_of_occthread3
    :var clientID: A unique string supplied by the caller. This ID is used to identify return data elements.
    """
    returnID: str = ''
    clientID: str = ''


@dataclass
class PostAssignIDICInput(TcBaseObj):
    """
    The structure contains input parameters: PMI context and occurrences from this context.
    
    :var context: The BOMView of the context that contains received occurrences.
    :var occurrences: The list with occurrences.
    """
    context: BusinessObject = None
    occurrences: List[OccurenceInfo] = ()


@dataclass
class PostAssignIDICResponse(TcBaseObj):
    """
    The stucture contains the return parameters: the new created IDICs and  service data with errors
    
    :var occurrenceIDICs: The list of structures with created IDIC.
    :var serviceData: Holds partial errors.
    """
    occurrenceIDICs: List[OccurrenceIDIC] = ()
    serviceData: ServiceData = None
