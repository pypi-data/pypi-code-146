from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetSubTypeHierarchicalTreeInput(TcBaseObj):
    """
    The main input here is the internal name of given type.
    
    :var typeInternalName: Internal name of type being requested.
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    """
    typeInternalName: str = ''
    clientId: str = ''


@dataclass
class GetSubTypeHierarchicalTreeResponse(TcBaseObj):
    """
    Holds linked type hierarchical tree data for requested types.  The structured trees start from given input types
    and consist of all level sub types.
    
    :var treeRootNodes: Root nodes of type hierachical trees. Each root node holds internal name and display name of
    given input type as well as its all immidiate sub types ordered by display name. Each immidiate sub type node holds
    its immidiate sub types ordered by display name.
    :var serviceData: Returned service data.
    """
    treeRootNodes: List[TypeHierarchicalTreeNode] = ()
    serviceData: ServiceData = None


@dataclass
class TypeHierarchicalTreeNode(TcBaseObj):
    """
    Holds internal name and display name of type as well as its all immidiate sub types ordered by display name.
    
    :var typeInternalName: Internal name of type.
    :var typeDisplayName: Display name of type.
    :var subTypes: Immidiate sub types ordered by display name.
    """
    typeInternalName: str = ''
    typeDisplayName: str = ''
    subTypes: List[TypeHierarchicalTreeNode] = ()
