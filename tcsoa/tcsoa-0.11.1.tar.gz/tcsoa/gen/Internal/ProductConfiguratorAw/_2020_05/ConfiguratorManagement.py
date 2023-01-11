from __future__ import annotations

from tcsoa.gen.BusinessObjects import WorkspaceObject, Cfg0ConfiguratorPerspective
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChildNode(TcBaseObj):
    """
    ChildNode is a ViewModelObject that represents the child for a given parent object. It encapsulates a model object
    in server side. This object can represent configurator objects like Cfg0AbsFeature, Cfg0AbsFeatureFamily,
    Cfg0AbsProductLine, and Cfg0AbsProductModel.
    
    :var parentNode: Parent node in tree for this child node.
    :var node: The ViewModelObject to be rendered.
    """
    parentNode: ViewModelObjectNode = None
    node: ViewModelObjectNode = None


@dataclass
class GetConfiguratorDataHierarchyIn(TcBaseObj):
    """
    The structure containing parameters to fetch the children for given parent Business Object.
    
    :var configPerspective: The configurator perspective. When this operation is invoked first time, this parameter
    would be null. First call returns this parameter and caller must hold to that parameter for passing through
    subsequent calls.
    :var parent: The parent object for which configurator data to be retrieved
    :var sortCriteria: Criteria to be used to sort the filtered results.
    :var requestInfo: Map (string/string) of configuration parameters.
    
    Allowed key | values are: 
    
    "RequestType" key provides information about the data that needs to be displayed to be handled for this service
    operation call.
    "RequestType" | "Products", product Line Hierarchy is displayed. "RequestType" | "Features", variability data is
    displayed. 
    
    "Expand" key provides the information of level of expansion for a given object.   
    "Expand" | "0", complete hierarchy is displayed. 
    "Expand" | "1", only one level of hierarchy is displayed. 
    Default value of "Expand" is "0". 
    
    "View" key provides information about the type of view. 
    "View" | "Tree", information is provided in hierarchical format. 
    Default value of "View" is "Tree". Key and Value in map are case sensitive. This parameter can be used in future to
    support different types of Views e.g. "List".
    
    "configSettings" key stores configuration information in JSON string which will be used to retrieve content
    "configSettings" JSON string supports following keys:
    "pca0RevisionRule": contains the Revision Rule name based on recent configurator perspective settings.
    "pca0Effectivity": contains the Effectivity expression string based on recent configurator perspective settings.
    "pca0RuleDate": contains the Rule Date based on recent configurator perspective settings.
    """
    configPerspective: Cfg0ConfiguratorPerspective = None
    parent: WorkspaceObject = None
    sortCriteria: SortCriteria = None
    requestInfo: StringMap2 = None


@dataclass
class GetConfiguratorDataHierarchyResp(TcBaseObj):
    """
    The output containing the available variability for the input list of variant option vaue selections.
    
    :var configPerspective: The configurator perspective containing all information about the current Configurator
    Context, revision rule and effectivity. All further communications with the server to retrieve variant
    configuration data must use this object.
    :var parent: The parent object for which configurator data to be retrieved.
    :var childrenNode: Teamcenter WorkspaceObject that was searched for and to be rendered in the view.
    :var serviceData: Contains the list of errors that might have occurred as part of the service invocation.
    :var responseInfo: Map (string/string) of configuration parameters.
    
    Keys supported: 
    "configSettings": contains the configuration settings for perspective object. This is JSON string.
    "configSettings" JSON string supports following keys:
    "pca0RevisionRule": contains the updated Revision Rule string based on recent configurator perspective object.
    "pca0Effectivity": contains Effectivity expression string based on recent configurator perspective object.
    "pca0RuleDate": contains Rule Date based on recent configurator perspective object.
    
    "pca0ConfigPerspective": contains latest updated Configurator Perspective properties.
    """
    configPerspective: Cfg0ConfiguratorPerspective = None
    parent: WorkspaceObject = None
    childrenNode: List[ChildNode] = ()
    serviceData: ServiceData = None
    responseInfo: StringMap2 = None


@dataclass
class SortCriteria(TcBaseObj):
    """
    Specifies the criteria to use to sort the results that are retrieved. It provides the field to sort and the
    direction to sort it in.
    
    :var fieldName: The name of the field to perform the sorting. This has to be the name of a property of an
    Configurator object on which sorting to be performed.
    :var sortDirection: The direction in which the sorting needs to be perfomed. It could be ascending or descending.
    Valid values are: "ASC" and "DESC".
    """
    fieldName: str = ''
    sortDirection: str = ''


@dataclass
class ViewModelObjectNode(TcBaseObj):
    """
    Service operation output structure to store the Teamcenter WorkspaceObject and its associated View model properties
    to be displayed in the view.
    
    :var wsObject: WorkspaceObject representing the node.
    :var nodeProperties: A list of ViewModelObjectProperty for the node.
    """
    wsObject: WorkspaceObject = None
    nodeProperties: List[ViewModelObjectProperty] = ()


@dataclass
class ViewModelObjectProperty(TcBaseObj):
    """
    Properties of the viewmodel object.
    
    :var propertyName: Property name.
    :var nodePropertyInfo: Map of (string, string) child node property and value.
    Valid keys: "isArray", "isEnabled", "isEditable"
    Valid Values: "true", "false".
    :var values: Real value for the property, the values are converted to strings for other value types such as date,
    double, Boolean or referenced objects.
    :var displayValues: Display values for the property.
    :var srcobjLsd: Last saved date of source object.
    """
    propertyName: str = ''
    nodePropertyInfo: PropertyInfoMap = None
    values: List[str] = ()
    displayValues: List[str] = ()
    srcobjLsd: datetime = None


"""
Map of string and list of strings.
"""
PropertyInfoMap = Dict[str, str]


"""
Map of string key and string as value.
"""
StringMap2 = Dict[str, str]
