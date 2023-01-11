from __future__ import annotations

from typing import List
from tcsoa.gen.RelationshipViewer._2012_10.NetworkEngine import RGBValue, Type
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GraphTypeListResponse(TcBaseObj):
    """
    Graph type response.
    
    :var views: A list of  role based avaliable graph views. Different role may get different view list.
    :var serviceData: Service data contains the partial errors which used to report any partial failures.
    """
    views: List[GraphViewDescription] = ()
    serviceData: ServiceData = None


@dataclass
class GraphViewDescription(TcBaseObj):
    """
    The description of a graph view
    
    :var name: Name of the graph view. It is also the identifier of graph view.
    :var displayName: Display name of the graph view. It is also the identifier of graph view.
    :var defaultLayout: the default layout of the view. The possible values are: IncrementalHierarchic, Top-to-Bottom,
    Left-to-Right, Bottom-to-Top, Right-to-Left.
    :var defaultExpandDirection: the default expansion direction of the view. The possibile values are: forward,
    backward, all.
    :var visible: Flag to indicate whether the view is visible on graph control panel.
    :var diagramMode: Flag to indicate whether the graph view is in diagram mode by default.
    :var groups: The list of graph view groups.
    """
    name: str = ''
    displayName: str = ''
    defaultLayout: str = ''
    defaultExpandDirection: str = ''
    visible: bool = False
    diagramMode: bool = False
    groups: List[GraphGroup] = ()


@dataclass
class GraphFilter(TcBaseObj):
    """
    Structure for representing information of a filter item, including filter name, RGB values to color the legend of
    the filter at client side. It is used in structure GraphGroup.
    
    :var name: name of the filter
    :var displayName: display name of the filter
    :var color: The color used for legend of this filter at client side
    :var types: The list of types belong to this category.
    """
    name: str = ''
    displayName: str = ''
    color: RGBValue = None
    types: List[Type] = ()


@dataclass
class GraphGroup(TcBaseObj):
    """
    The graph group is a group name with a list of filters. A filter take effect either on node or edge, it filts out
    graph that fall into its type. It is used in structure GraphViewDescription.
    
    :var name: Backend name of the group. Currently, there are two available groups, relations and objects.
    :var filters: The list of graph group filter names. For example: the relations graph group may have Attach,
    Tracability, Structure, Folder, Connectivity as filters. The objects graph group may have Requirement, Functional,
    Logical, Physical, Dataset, Plant as filters.
    """
    name: str = ''
    filters: List[GraphFilter] = ()
