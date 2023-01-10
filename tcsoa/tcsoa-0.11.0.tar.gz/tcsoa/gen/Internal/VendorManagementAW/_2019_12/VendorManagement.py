from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AssignPartnerContractInput(TcBaseObj):
    """
    selected WorkspaceObject,partner contract to assign, preferred status.
    
    :var partnerContract: Vm0PrtnrContractRevision to assign.
    :var preferredStatus: Preferred status for partner contract in the context of an object. Valid values are given in
    LOV preference, "Vm0PrtnrContractAssignmentStatus".
    :var selectedObject: Selected WorkspaceObject to assign partner contract.
    """
    partnerContract: ItemRevision = None
    preferredStatus: str = ''
    selectedObject: WorkspaceObject = None


@dataclass
class ViewModelObject(TcBaseObj):
    """
    Structure to store the Teamcenter BusinessObject and its associated view model properties to be displayed as a
    single row in the table.
    
    :var modelObject: Represents the underlying business object of the row. The object can be WorkspaceObject.
    :var viewModelProperties: A list of ViewModelProperty structures.
    """
    modelObject: BusinessObject = None
    viewModelProperties: List[ViewModelProperty] = ()


@dataclass
class ViewModelProperty(TcBaseObj):
    """
    Structure to store the properties of logical business object to be displayed as a single cell in the row of table.
    Properties which do not exist directly on the business object, only those properties will be created.
    
    :var propInternalName: Real name of the property.
    :var propDisplayName: Display name of the property.
    :var propDBValue: Database value of the property.
    :var propUIValue: Value of the property which will be shown to user.
    :var propDataType: Data type of the property. Supported values are: "string", "int", "boolean", "short", "float",
    "double".
    :var isEditable: If property is editable then "true", otherwise "false".
    :var hasLOV: If true, property has LOV attached; otherwise, false.
    :var propParentBO: The business object which has this property.
    """
    propInternalName: str = ''
    propDisplayName: str = ''
    propDBValue: str = ''
    propUIValue: str = ''
    propDataType: str = ''
    isEditable: bool = False
    hasLOV: bool = False
    propParentBO: BusinessObject = None


@dataclass
class ViewModelRowsResponse(TcBaseObj):
    """
    The structure holds information of the view model objects. Each ViewModelObject structure represents a row
    displayed on table.
    
    :var viewModelRows: List of view model rows for each displayed node in a table.
    :var serviceData: The service data object.
    """
    viewModelRows: List[ViewModelObject] = ()
    serviceData: ServiceData = None


@dataclass
class ColumnInfo(TcBaseObj):
    """
    1.1.1.4    ColumnInfo
    
    :var propInternalName: Internal name of the column.
    :var propDisplayName: Display name of the column.
    :var objectTypeName: The business object type (ItemRevision and its subtypes) of the property associated with
    column.
    :var columnWidth: Width of the column in pixels.
    :var isDisplayed: If column needs to be displayed or not.
    """
    propInternalName: str = ''
    propDisplayName: str = ''
    objectTypeName: str = ''
    columnWidth: int = 0
    isDisplayed: bool = False


@dataclass
class ColumnInfoInput(TcBaseObj):
    """
    Type of table and WorkspaceObject object.
    
    :var tableType: Type of table to render. Supported table type is "PartnersStructure".
    :var inputObject: WorkspaceObject business object.
    """
    tableType: str = ''
    inputObject: WorkspaceObject = None


@dataclass
class ColumnInfoResponse(TcBaseObj):
    """
    This operation returns the information of the columns for a table which is rendered as a part of tree table for
    given type of structure and business object.
    
    The column information returned as part of this operation includes display name, internal name, object type,  width
    and a flag to indicate if column needs to be displayed or not.
    
    :var columnInfo: A list containing the columns for a table with other attributes of the column.
    :var serviceData: Service data object associated with the operation
    """
    columnInfo: List[ColumnInfo] = ()
    serviceData: ServiceData = None


@dataclass
class RemovePartnerContractInput(TcBaseObj):
    """
    The structure contains -
    1. WorkspaceObject from which the Partner Contract is to be removed. This could be an ItemRevision or a structure
    context.
    2. Partner Contract which is to be removed from the input WorkspaceObject.
    
    :var objectForContractRemoval: The WorkspaceObject from which the Partner Contract is to be removed.
    :var partnerContract: The Vm0PrtnrContractRevision object which is to be removed.
    """
    objectForContractRemoval: WorkspaceObject = None
    partnerContract: ItemRevision = None
