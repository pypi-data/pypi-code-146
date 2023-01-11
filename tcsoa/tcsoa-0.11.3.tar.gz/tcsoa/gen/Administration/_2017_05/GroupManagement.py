from __future__ import annotations

from tcsoa.gen.BusinessObjects import Group, ImanVolume
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AddChildGroupsToGroupStructure(TcBaseObj):
    """
    Groups to be added to a parent Group.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var groupsToAdd: A list of existing Group objects to be added to the parent Group as child groups.
    :var groupsToCreateAndAdd: A list of CreateAndAddChildGrpsToGrpStructure objects for Group. A new Group will be
    created for each input in the list and added to the parent Group.
    :var parentGroup: The parent Group the child groups are to be added to.
    """
    clientId: str = ''
    groupsToAdd: List[Group] = ()
    groupsToCreateAndAdd: List[CreateAndAddChildGrpsToGrpStructure] = ()
    parentGroup: Group = None


@dataclass
class CreateAndAddChildGrpsToGrpStructure(TcBaseObj):
    """
    Group to be created.
    
    :var name: Name of the Group to be created.
    :var description: Description of the Group.
    :var privilege: Indicates whether members of the Group will get administrative privileges.
    If true, all members of this Group will have system administration privilege; otherwise members will not have
    administration privilege.
    :var localVolume: Default local volume for the Group, local volume refers to a physical location with same site as
    Group where the Teamcenter files are stored. This temporary local volume allows the file to be stored locally
    before it is automatically transferred to the final destination in the background. Once the file is stored in the
    default local volume, the user can continue working without having to wait for the upload to take place.
    :var security: Specifies the project level security settings of Group. Valid values are "Internal" or "External".
    The internal/external Security setting allows or restricts access to data. For example, members of external groups
    can only access data in their group.
    :var volume: The location where the Teamcenter files to be stored by the users of this Group.
    """
    name: str = ''
    description: str = ''
    privilege: bool = False
    localVolume: ImanVolume = None
    security: str = ''
    volume: ImanVolume = None
