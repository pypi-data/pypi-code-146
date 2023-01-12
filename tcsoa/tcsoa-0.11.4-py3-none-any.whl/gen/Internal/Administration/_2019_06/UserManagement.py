from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, User
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetGroupRoleViewModelInput(TcBaseObj):
    """
    This structure holds the information about the user object that is used to construct ViewModelObject strucutres and
    information required to fetch correct page of data.
    
    :var userObject: Specifies the User object that will be used to construct list of ViewModelObjects. It can be any
    user if the current logged in user is DBA. For non-dba user it should only be current logged in user.
    :var startIndex: The start index represents the index starting from where the ViewModelObjects should be included
    in the response. And hence this must be a non-negative value. Otherwise all data will be returned and the data will
    not be paginated.
    :var pageSize: The maximum number of ViewModelObjects that should be included while returning the response.
    """
    userObject: User = None
    startIndex: int = 0
    pageSize: int = 0


@dataclass
class GetGroupRoleViewModelResponse(TcBaseObj):
    """
    The structure holds the information about view model objects. Each ViewModelObject structure represents a row
    displayed on the Active Workspace table widget.
    
    :var viewModelRows: A list of view models which can be used to display a row on active     workspace table widget.
    :var totalFound: Total number of nodes that are part of view.
    :var endIndex: Cursor end position for the results returned so far.
    :var serviceData: The service data object.
    """
    viewModelRows: List[ViewModelObject] = ()
    totalFound: int = 0
    endIndex: int = 0
    serviceData: ServiceData = None


@dataclass
class ViewModelObject(TcBaseObj):
    """
    Structure to store the Teamcenter Business object and its associated view model properties to be displayed as a row
    on the Active Workspace table widget.
    
    :var modelObject: Represents the underlying business object of the row.
    :var viewModelProperties: A list of ViewModelProperty structure.
    """
    modelObject: BusinessObject = None
    viewModelProperties: List[ViewModelProperty] = ()


@dataclass
class ViewModelProperty(TcBaseObj):
    """
    Structure to store properties to be displayed as a single cell in a row of Active Workspace table widget. This can
    also include the properties which directly does not belong to the model object.
    
    :var propInternalName: Real name of the property.
    :var propDisplayName: Display name of the property.
    :var propDBValue: Database value of the property.
    :var propUIValue: Value of the property which will be shown to user.
    :var propDataType: Data type of the property.
    :var isEditable: If true, the property is editable; otherwise false.
    :var hasLOV: If true, property has LOV attached; otherwise, false.
    :var isModifiable: If true, the property is modifiable; otherwise, not.
    :var propBO: Business object related to the property. For Example: If property is default_role then it will contain
    Role object. If property is group than it will contain group object.
    """
    propInternalName: str = ''
    propDisplayName: str = ''
    propDBValue: str = ''
    propUIValue: str = ''
    propDataType: str = ''
    isEditable: bool = False
    hasLOV: bool = False
    isModifiable: bool = False
    propBO: BusinessObject = None
