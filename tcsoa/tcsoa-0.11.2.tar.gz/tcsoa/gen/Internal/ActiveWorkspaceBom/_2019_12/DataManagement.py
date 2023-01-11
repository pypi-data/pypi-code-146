from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetViewModelForCreateInfo(TcBaseObj):
    """
    GetViewModelForCreateInfo represent the parameters required to load ViewModelObject and render 'Grid:Row' view in
    editable state, to author WorkspaceObject of given input businessObjectType.
    
    :var businessObjectType: Internal type name of the object to be created.
    :var propertyNames: A list of internal property names displayed in table, for which mapped properties of
    BusinessObject to be determined.
    :var parent: The parent object of type Awb0Element under which child node information to be retrieved. Supported
    types are: Awb0DesignElement a child type of Awb0Element.
    """
    businessObjectType: str = ''
    propertyNames: List[str] = ()
    parent: BusinessObject = None


@dataclass
class GetViewModelForCreateResponse(TcBaseObj):
    """
    GetViewModelForCreateResponse contains information required to create WorkspaceObject.
    
    :var viewModelCreateInObjsJsonStrings: The UI definition to render an editable row. Json strings that contains the
    ViewModelObject structures which provide information for the CreateInput object, returned as a part of ServiceData
    plain objects. This is like the viewModelObjectJsonString used in getDeclarativeStyleSheet2 and
    loadViewModelForEditing2 operation.
    :var columnPropToCreateInPropMap: A map (string, string) of property names on column and CreateInput property name
    pairs  of the input businessObjectType.
    :var createHtmlProviders: A list of html panel defined input businessObjectType create stylesheet definition.
    :var serviceData: ServiceData containing partial error if any.
    """
    viewModelCreateInObjsJsonStrings: List[str] = ()
    columnPropToCreateInPropMap: StringMap = None
    createHtmlProviders: List[str] = ()
    serviceData: ServiceData = None


"""
A map of displayed property names on column and corresponding CreateInput property name pairs (string, string).
"""
StringMap = Dict[str, str]
