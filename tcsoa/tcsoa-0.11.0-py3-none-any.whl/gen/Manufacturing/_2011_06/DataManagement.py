from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2009_10.DataManagement import CreateInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OpenContextInfo(TcBaseObj):
    """
    Contains information on an opened context
    
    :var context: The opened context (The top line of the created window)
    :var object: The object which was passed to the method as input if this context was opened directly. If this
    context was opened as an outcome of another context or if CC was opened then this will be NULL
    :var views: A vector with the top lines of the opened views (OG windows)
    :var structureContext: The structure context containing this context. This is relevant only in case the context to
    open is a CC or SC object
    """
    context: BusinessObject = None
    object: BusinessObject = None
    views: List[BusinessObject] = ()
    structureContext: BusinessObject = None


@dataclass
class OpenContextInput(TcBaseObj):
    """
    Input for openContexts operation
    
    :var object: The object to open
    :var openViews: Defines whether to open all connected views
    :var openAssociatedContexts: Defines whether to open also associated contexts
    :var contextSettings: Defines additional context settings such as configuration (revision rule, variant rule, IC),
    show-unconfigured options, Product Configurator context flag, etc.
    """
    object: BusinessObject = None
    openViews: bool = False
    openAssociatedContexts: bool = False
    contextSettings: CreateInput = None


@dataclass
class OpenContextsResponse(TcBaseObj):
    """
    Response object for openContexts operation
    
    :var output: A vector with information of the method output
    :var serviceData: The operation ServiceData
    """
    output: List[ContextGroup] = ()
    serviceData: ServiceData = None


@dataclass
class OpenViewsResponse(TcBaseObj):
    """
    Response object for openViews operation
    
    :var views: A vector with the opened views (the top lines of the created OG windows)
    :var serviceData: The operation ServiceData
    """
    views: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class ContextGroup(TcBaseObj):
    """
    A group of contexts opened by openContexts operation
    
    :var contexts: A vector with information on each opened context in the group
    :var collaborationContext: The container of the context group (CC). This is relevant only in case the context to
    open is a CC object
    """
    contexts: List[OpenContextInfo] = ()
    collaborationContext: BusinessObject = None
