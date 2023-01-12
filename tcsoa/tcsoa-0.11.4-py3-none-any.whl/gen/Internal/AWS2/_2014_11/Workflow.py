from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject, EPMTask
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RGBValue(TcBaseObj):
    """
    Structure for representing color using RGB values, used in structure FilterData.
    
    :var redValue: The Red component of color. Legal range is 0-255.
    :var greenValue: The Green component of color. Legal range is 0-255.
    :var blueValue: The Blue component of color. Legal range is 0-255.
    """
    redValue: float = 0.0
    greenValue: float = 0.0
    blueValue: float = 0.0


@dataclass
class TypeData(TcBaseObj):
    """
    Structure containing the type information.
    
    :var typeName: The name of the type.
    :var displayName: The display name of the type.
    """
    typeName: str = ''
    displayName: str = ''


@dataclass
class WorkflowGraphInput(TcBaseObj):
    """
    Structure represents the parameters required to get the workflow.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var selection: The object for which the latest associated workflow to be retrieved.
    :var workflowGraphInfo: A map (string, list of strings) of workflow related information like zoom level etc.Valid
    keys are zoomLevel and layout. The valid value for zoomLevel is any percentage. Valid values for layout are
    Incremental, Orthographic,Tree,Left To Right, Right To Left.
    """
    clientId: str = ''
    selection: BusinessObject = None
    workflowGraphInfo: NameValuePair = None


@dataclass
class WorkflowGraphLegendData(TcBaseObj):
    """
    Structure represents the output data of getWorkflowGraphLegend operation.
    
    :var name: The name of the Legend.
    :var displayName: The localized display name of the Legend.
    :var defaultLayout: The default layout of the view. The values are  Incremental, Orthographic,Tree,Left To Right
    andRight To Left   This value is utilized by the Graph component.
    :var objectGroup: A list of filters associated with objects.
    :var relationGroup: A list of filters associated with relations.
    """
    name: str = ''
    displayName: str = ''
    defaultLayout: str = ''
    objectGroup: List[FilterData] = ()
    relationGroup: List[FilterData] = ()


@dataclass
class WorkflowGraphLegendResponse(TcBaseObj):
    """
    Structure represents the output parameters of getWorkflowGraphLegend operation.
    
    :var legendData: The list of  WorkflowGraphLegendData structures.The legend data will be created based on the XML
    configuration file. This XML file is read from the dataset specified in the preference
    WRKFLW_graph_legend_configuration_file_name.
     
    
     
     
    
    :var presentationRulesXML: The information about how a Node or an Edge is to be rendered based on the type it
    represents is defined in this XML. For instance, a Node representing the EPMTask type is shown as a Tile.  This XML
    is read from the dataset specified  in the preference WRKFLW_graph_presentation_rules_file_name.
    :var presentationStylesXML: The information about shapes, size, line style, arrowstyle etc.    This will be used
    for representation of nodes and edges. This XML is read from the dataset specified  in the preference
    WRKFLW_graph_presentation_styles_file_name.
    :var serviceData: The Service Data.
    """
    legendData: List[WorkflowGraphLegendData] = ()
    presentationRulesXML: str = ''
    presentationStylesXML: str = ''
    serviceData: ServiceData = None


@dataclass
class WorkflowGraphOutput(TcBaseObj):
    """
    Structure represents the output of getWorkflowGraphLegend operation.
    
    :var clientId: The clientId from the input  WorkflowGraphInput structure. This value is unchanged from the input,
    and can be used to identify this response element with the corresponding input element.
    :var workflowGraphInfo: A map (string, list of strings) of diagram related information.
    Valid keys are zoomLevel and layout. The valid value for zoomLevel is any percentage. Valid values for layout are
    Incremental, Orthographic,Tree,Left To Right, Right To Left.
    :var elementData: A list of elements to be shown in the workflow.
    :var edgeData: A list of relations to be shown in the workflow graph. A relation represents the information about
    the connection between the elements in workflow graph.
    """
    clientId: str = ''
    workflowGraphInfo: NameValuePair = None
    elementData: List[ElementData] = ()
    edgeData: List[EdgeData] = ()


@dataclass
class WorkflowGraphResponse(TcBaseObj):
    """
    Structure represents the output parameters of getWorkflowGraph operation.
    
    :var output: A list of WorkflowGraphOutput structures.
    :var serviceData: The Service Data.
    """
    output: List[WorkflowGraphOutput] = ()
    serviceData: ServiceData = None


@dataclass
class EdgeData(TcBaseObj):
    """
    Structure represents the relation to be shown on the graph.
    
    :var end1Element: The primary end of the relation.
    :var end2Element: The secondary end of the relation.
    :var edge: The relation object.
    :var edgeInfo: The information (string, list of strings)  about the relation. Valid key is edgeType and the valid
    value is the type of the relation. This information is used by graphical framework for rendering the Edge. An
    example is:  An edge type defined with name "FailSuccessor" can be configured to render a line with red color with
    dash style to show the fail path in workflow graph.
    """
    end1Element: EPMTask = None
    end2Element: EPMTask = None
    edge: BusinessObject = None
    edgeInfo: NameValuePair = None


@dataclass
class ElementData(TcBaseObj):
    """
    Structure represents the element to be shown on the graph.
    
    :var element: The EPMTask object to be shown in the workflow.
    :var elementInfo: The information (string, list of strings) about the element. Valid key is elementType and the
    valid value is the type of the element.  This information is used by graphical framework for rendering the Element.
    An example is an element type defined as "EPM_started" can be configured to be render the element with yellow color
    frame in workflow graph.
    """
    element: WorkspaceObject = None
    elementInfo: NameValuePair = None


@dataclass
class FilterData(TcBaseObj):
    """
    Structure for representing information of a filter, including filter name, RGB values to color the legend of the
    filter at client side.
    
    :var name: The name of the filter.
    :var displayName: The display name of the filter.
    :var types: The object or relation type information to be shown in the legend.
    :var color: The color used for legend of this filter on the client.
    """
    name: str = ''
    displayName: str = ''
    types: List[TypeData] = ()
    color: RGBValue = None


"""
NameValuePair is a map of property name (key) and property values (values) in string format.
"""
NameValuePair = Dict[str, List[str]]
