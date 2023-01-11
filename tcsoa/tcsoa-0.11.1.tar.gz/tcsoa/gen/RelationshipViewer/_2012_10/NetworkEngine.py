from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateRelationInput(TcBaseObj):
    """
    Input struct for createRelations operation.
    
    :var clientId: Unique client identifier, optional.
    :var relationType: The relation type to create between the two input Business Objects. For example: FND_TraceLink,
    PSConnection, Content. You can get all the supported relation type decriptions by service opertion NetworkEngine
    .getView2().
    :var primaryObject: The primary object to create relation from.
    :var secondaryObject: The secondary object to create relation to.
    :var props: The (string, string) map contains properties for relation creation.
    """
    clientId: str = ''
    relationType: str = ''
    primaryObject: BusinessObject = None
    secondaryObject: BusinessObject = None
    props: StringPropertyMap = None


@dataclass
class CreateRelationsResponse(TcBaseObj):
    """
    Output struct for createRelations operation.
    
    :var clientId: Identifier that helps the client to track the relation(s) created.
    :var edges: The list of new created network edges which representing the relation between Business Objects.
    :var nodeUpdates: The (string,Node) map contains the uid of input node and output node to be updated. This is
    especially useful for BOM struction creation, as the input is uid of ItemRevision, while the output is a BomLine
    node, so client can update network if necessary.
    :var serviceData: Service data including partial errors.
    """
    clientId: str = ''
    edges: List[Edge] = ()
    nodeUpdates: NodeUpdateMap = None
    serviceData: ServiceData = None


@dataclass
class GraphStyleDefResponse(TcBaseObj):
    """
    graph style definition
    
    :var styleXMLStr: XML string contains graph style definition.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors is used
    to report any partial failures.
    """
    styleXMLStr: str = ''
    serviceData: ServiceData = None


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
    :var defaultLayout: the default layout of the view
    :var defaultExpandDirection: the default expansion direction of the view
    :var visible: Flag to indicate whether the view is visible on graph control panel.
    :var diagramMode: Flag to indicate whether the graph view is in diagram mode by default.
    :var parameters: The list of graph view parameters.
    :var inquiries: The list of supported graph view inquiries. For example: numOfNodes, numOfEdges.
    :var groups: The list of graph view groups.
    """
    name: str = ''
    defaultLayout: str = ''
    defaultExpandDirection: str = ''
    visible: bool = False
    diagramMode: bool = False
    parameters: List[GraphParameterInfo] = ()
    inquiries: List[GraphInquiry] = ()
    groups: List[GraphGroup] = ()


@dataclass
class NetworkResponse(TcBaseObj):
    """
    network response
    
    :var graph: Graph data of the network.
    :var serviceData: Service data contains the list of Teamcenter business objects and also the partial errors is used
    to report any partial failures.
    """
    graph: Graph = None
    serviceData: ServiceData = None


@dataclass
class Node(TcBaseObj):
    """
    node of the graph
    
    :var id: Node id. A unique immutable identifier of the node. It is business object UID for Teamcenter data source.
    :var name: Name of node
    :var metaObject: Underlying Teamcenter object. For example: BomLine, Item, ItemRevision, Function etc. Can be null.
    For external data source, it can be RuntimeObject.
    :var props: A map of property name and property value pairs (string/string). For example, [in_degree, 2],
    [out_degree, 4].
    """
    id: str = ''
    name: str = ''
    metaObject: BusinessObject = None
    props: StringPropertyMap = None


@dataclass
class QueryNetworkInputs(TcBaseObj):
    """
    The input structure containing parameters for query network.
    
    :var rootIds: A list of object IDs that input as network root nodes. If data source is Teamcenter, it is the UID
    list of Teamcenter business objects.
    :var viewName: The name of graph view that will be used for network expansion. Call getViews() service method to
    get available view names.
    :var queryMode: The query mode that applied to this query operation.
    :var serviceCursor: The cursor of the start service index in service list. It's set to 0 for initial call. If
    client get a partial graph by queryNetwork2 operation, it can be set great than 0 to get remaining part of graph.
    :var graphParamMap: A map of graph parameter name and parameter value list (string / list of string), such as
    expansion level, expansion direction. Parameters are inputs leveraged by the graph generation logic. Call
    getViews() service method to get available graph parameters supported by the specified view.
    :var inquiries: A list of inquiries.. Inqueries identify calculations that are performed using the graph contents
    as inputs. The full supported inquires can be got by calling getView() method. Currently supported inquires:
    numOfNodes, numOfEdges.
    """
    rootIds: List[str] = ()
    viewName: str = ''
    queryMode: QueryModeEnum = None
    serviceCursor: int = 0
    graphParamMap: GraphParamMap = None
    inquiries: List[str] = ()


@dataclass
class RGBValue(TcBaseObj):
    """
    Structure for representing color using RGB values, used in structure GraphFilter.
    
    :var redValue: The red component of color.
    :var greenValue: The green component of color.
    :var blueValue: The blue component of color.
    """
    redValue: float = 0.0
    greenValue: float = 0.0
    blueValue: float = 0.0


@dataclass
class Type(TcBaseObj):
    """
    The graph element type structure, used in structure GraphFilter.
    
    :var internalName: The internal type name.
    :var displayName: The display name of type.
    """
    internalName: str = ''
    displayName: str = ''


@dataclass
class Edge(TcBaseObj):
    """
    The structure of edge.
    
    :var leftId: Left node id
    :var rightId: Right node id.
    :var relationType: The logical type of the edge. It is localized.
    :var metaObject: Underlining Teamcenter object.
    :var startPortObject: The start port object associated with the meta object.
    :var endPortObject: The end port object associated with the meta object.
    :var props: A map of property name and property value pairs  (string/string).
    """
    leftId: str = ''
    rightId: str = ''
    relationType: str = ''
    metaObject: BusinessObject = None
    startPortObject: BusinessObject = None
    endPortObject: BusinessObject = None
    props: StringPropertyMap = None


@dataclass
class Graph(TcBaseObj):
    """
    Structure of network graph data.
    
    :var viewName: Graph name of the network.
    :var rootIds: A list of graph root IDs. If data source is Teamcenter, it is the UID list of Teamcenter business
    objects.
    :var serviceCursor: The cursor point to query service that going to be called. For initial query, set service
    cursor to 0.
    :var nodes: A list of Node structures.
    :var edges: A list of Edge structures.
    :var analysisResult: A (string,string) map of inquery and answer pairs.
    :var isPartial: The flag indicates whether it's a partial graph.
    """
    viewName: str = ''
    rootIds: List[str] = ()
    serviceCursor: int = 0
    nodes: List[Node] = ()
    edges: List[Edge] = ()
    analysisResult: GraphInquiryMap = None
    isPartial: bool = False


@dataclass
class GraphFilter(TcBaseObj):
    """
    Structure for representing information of a filter item, including filter name, RGB values to color the legend of
    the filter at client side. It is used in structure GraphGroup.
    
    :var name: name of the filter
    :var color: The color used for legend of this filter at client side
    :var types: The list of types belong to this category.
    """
    name: str = ''
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


@dataclass
class GraphInquiry(TcBaseObj):
    """
    The supported inquiry of graph.
    
    :var name: Backend name of the inquiry. A inquery is a short query clause that can be used to retrieve information
    from network graph.
    :var description: Description of the inquiry. Not localized.
    """
    name: str = ''
    description: str = ''


@dataclass
class GraphParameterInfo(TcBaseObj):
    """
    The info of graph parameter
    
    :var name: Backend name of the parameter.
    :var valueMask: The regular expression that used to validate the parameter value.
    :var type: The value type of the parameter. Currently supported types: int, double, string.
    :var defaultValue: Default value of the parameter
    :var description: the description of the parameter. Not localized.
    """
    name: str = ''
    valueMask: str = ''
    type: str = ''
    defaultValue: str = ''
    description: str = ''


class QueryModeEnum(Enum):
    """
    The query mode enumeration.
    
    :var DegreeOnly: Only calculate node degree without return graph.
    :var ExpandOnly: Only expand graph without calculate node degree.
    :var ExpandAndDegree: Expand graph and calculate node degree together.
    """
    DegreeOnly = 'DegreeOnly'
    ExpandOnly = 'ExpandOnly'
    ExpandAndDegree = 'ExpandAndDegree'


"""
the inquiry/answer map
"""
GraphInquiryMap = Dict[str, str]


"""
Network graph parameter map
"""
GraphParamMap = Dict[str, List[str]]


"""
The map with the key of input node uid to output node.
"""
NodeUpdateMap = Dict[str, Node]


"""
The map contains key and value for string property.
"""
StringPropertyMap = Dict[str, str]
