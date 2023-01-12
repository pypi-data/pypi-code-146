from typing import List, Literal
from pydantic import BaseModel
from fabrique_nodes_core.ui_params import UIParams  # noqa: F401
from fabrique_nodes_core.port_types import port_type
from fabrique_nodes_core.configs_model import Port, NodeData, Node as NodeModel


class NodeConfig(NodeData):
    """Node config data model

    :param id_: unique node id in actor
    :param ports_out: output ports list
    :param ports_in: input ports list
    :param description: node description
    :param schema_: node json schema
    :param config: configs form UI
    """
    id_: str
    ports_out: List[Port] = []
    ports_in: List[Port] = []
    description: str = ''
    schema_: str = ''
    config: BaseModel = None


class BaseNode:
    """Base Node class
    :param type_: your unique node type
    :param group_type_: leave this value undefined, will be filled automatically if this node belongs to a group
    :param category: one of ['StructOps', 'IO', 'Funcional', 'Stateful', 'Misc'] used for grouping and styling nodes
    :param ui_params: UIParams your custom port groups parameters
    :param initial_config: initial node configuration
    """
    type_: str = ''
    group_type_: str = ''
    category: Literal['StructOps', 'IO', 'Funcional', 'Stateful', 'Misc'] = 'Misc'
    ui_params: UIParams = UIParams()
    initial_config: NodeModel = None

    def __init__(self, cfg: NodeConfig):
        """Node init

        :param cfg: node configuration
        :type cfg: NodeConfig
        """
        cfg.ports_in = [p for ports in cfg.g_ports_in for p in ports]
        cfg.ports_out = [p for ports in cfg.g_ports_out for p in ports]
        self.cfg = cfg

    def process(self, *args) -> list:
        """Default processing logic

        :param args: list of input values to process
        :return: list of output values
        :rtype: list
        """
        raise Exception('Process method must be implemented!')


class NodesGroup:
    """Node group wrapper
    :param type_: will be copied in group_type_ of BaseNode
    :param nodes_array: list of Node classes to group
    """
    type_: str = ''
    nodes_array: list[BaseNode] = []


root_port = Port(id_='root', name='root', type_=port_type[None], special=False, code='')
