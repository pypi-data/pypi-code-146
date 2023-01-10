from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, POM_object, Fnd0ChangeContext
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SetChangeContextResponse2(TcBaseObj):
    """
    The valid input contexts and the corresponding configured objects are added to configuredObjectsMap. If the input
    context is not a valid context for configuring objects, no value is added to configuredObjectsMap for this context,
    and a partial error is added for this context. If the context is valid, and an object is not valid for
    configuration in that context, a partial error is added for that object.
    
    :var serviceData: Contains any partial errors for the operation.
    :var configuredObjectsMap: A map (business object, list of ChangeContextStructOut) between a context and the list
    of configured objects.
    """
    serviceData: ServiceData = None
    configuredObjectsMap: ChangeContextMapOut = None


@dataclass
class ChangeContextStructIn(TcBaseObj):
    """
    Structure containing configuration mode and the list of input objects.
    
    :var changeConfigurationMode: Applicable only when a ChangeNotice  is provided as the input 
    context. Allowed values are "Latest" and "LatestCurrentChangeOnly".
    :var inputObjects: The objects to be configured for the input context.
    """
    changeConfigurationMode: str = ''
    inputObjects: List[POM_object] = ()


@dataclass
class ChangeContextStructOut(TcBaseObj):
    """
    Structure of the context used to configure objects and the list of configured objects.
    
    :var changeContext: A business object that contains the input context and the configuration mode used.
    :var configuredObjs: List of configured objects.
    """
    changeContext: Fnd0ChangeContext = None
    configuredObjs: List[POM_object] = ()


"""
A map between a context and a list of objects to be configured using this context. The context object can be null, in which case the corresponding list of objects will be configured for public. The context can also be a runtime business object which holds the context and the change configuration mode.
"""
ChangeContextMapIn = Dict[BusinessObject, ChangeContextStructIn]


"""
A map between a context and a structure containing the list of objects configured with the context. The context object can be null, in which case the corresponding list of objects will be configured for public context.
"""
ChangeContextMapOut = Dict[BusinessObject, ChangeContextStructOut]
