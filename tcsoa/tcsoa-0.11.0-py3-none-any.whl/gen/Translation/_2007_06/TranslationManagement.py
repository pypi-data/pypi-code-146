from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateTranslationRequestArgs(TcBaseObj):
    """
    The CreateTranslationRequestArgs struct is used to pass in multiple sets of data
    to be used in a single call.  These structs are passed in the collection of
    input arguments to the function createTranslationRequest.
    
    :var primaryObjects: The primary objects for the request.  This usually
    refers to a dataset to translate but can be any component.
    :var secondaryObjects: The secondary objects for the request.  This usually
    refers to the Item Revision containing the primary objects.
    :var priority: The priority to assign to the request.
    :var providerName: The provider name to process the request.
    :var translatorName: The translator from the above provider to translate the request.
    :var trigger: The trigger is a string that identifies who/where created this request.
    :var translatorArgs: The translator arguments to pass to the translator.  These are name
    value pairs like: NAME=FENDER.
    """
    primaryObjects: List[BusinessObject] = ()
    secondaryObjects: List[BusinessObject] = ()
    priority: int = 0
    providerName: str = ''
    translatorName: str = ''
    trigger: str = ''
    translatorArgs: List[str] = ()


@dataclass
class CreateTranslationRequestResponse(TcBaseObj):
    """
    The CreateTranslationRequestResponse struct contains the requests that were created
    as a result of the inputs specified in the CreateTranslationRequestArgs struct above.
    
    :var requestsCreated: The Translation Request objects created.
    :var svcData: The Service Data.
    """
    requestsCreated: List[BusinessObject] = ()
    svcData: ServiceData = None
