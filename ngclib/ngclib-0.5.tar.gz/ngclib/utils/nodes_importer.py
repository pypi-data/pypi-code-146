"""Module that handles the loading of the nodes from an arbitrary module"""
from __future__ import annotations
import sys
import importlib
from typing import List, Dict, Type
from pathlib import Path
from nwgraph import Node
from ..logger import logger

class NodesImporter:
    """
    NodesImporter implementation that imports and instantiates the required nodes
    """
    def __init__(self, node_names: List[str], node_types: List[str], node_args: Dict[str, Dict],
                 node_str_to_type: Dict[str, Type[Node]] = None, nodes_module_path: Path = None):
        if node_str_to_type is None:
            node_str_to_type = {}

        self.node_names = node_names
        self.node_types = node_types
        self.node_args = node_args
        self.nodes_module_path = nodes_module_path
        self.node_type_str_to_type: Dict[str, Type[Node]] = self._get_nodes_types(node_str_to_type)
        self._nodes: List[Node] = None

    @classmethod
    def from_graph_cfg(cls, graph_cfg: "GraphCfg", *args, **kwargs) -> NodesImporter:
        """Class method to construct from graph_cfg."""
        return cls(graph_cfg.node_names, graph_cfg.node_types, graph_cfg.node_args, *args, **kwargs)

    def _get_nodes_types(self, node_str_to_type: Dict[str, Type[Node]]) -> Dict[str, Type[Node]]:
        """Tries to resolve all the node types based on import module or provided types list"""
        imported_types = self._import_nodes_from_module()
        clashes = set(imported_types.keys()).intersection(node_str_to_type.keys())
        if len(clashes) > 0:
            logger.warning("Node name clashes: {clashes}. Manually provided ones will take precedence.")
        types = {**imported_types, **node_str_to_type}
        res = {}
        for node_type in self.node_types:
            assert node_type in types, f"Node type '{node_type}' does not exist in provided list: {types}"
            res[node_type] = types[node_type]
        return res

    @property
    def nodes(self) -> List[Node]:
        """Gets the nodes, and imports them just once."""
        if self._nodes is None:
            self._nodes = self._instantiate_nodes()
        return self._nodes

    def _instantiate_nodes(self) -> List[Node]:
        """Instantiates the nodes. Used by self.nodes singleton."""
        nodes = []
        for node_type_name, node_name in zip(self.node_types, self.node_names):
            assert node_type_name in self.node_type_str_to_type, \
                f"Node '{node_name}' (type: {node_type_name}) not in loaded nodes"
            if node_name not in self.node_args:
                logger.warning(f"Node '{node_name}' has no args. Instantiating with no args!")
            node_type = self.node_type_str_to_type[node_type_name]
            node_args = self.node_args[node_name] if node_name in self.node_args else {}

            try:
                node_instance = node_type(name=node_name, **node_args)
            except Exception as e:
                logger.debug(f"Failed instantiating node '{node_name}' of type '{node_type_name}' with exception: {e}")
                raise Exception(e)
            nodes.append(node_instance)
        return nodes


    def _import_nodes_from_module(self) -> Dict[str, Type[Node]]:
        """Import all nodes from a given modules path"""
        if self.nodes_module_path is None:
            return {}

        # Check that __init__.py file exists
        module_path = Path(self.nodes_module_path).absolute()
        assert module_path.is_dir(), f"Module path '{module_path}' is not the nodes/ modules directory."
        init_py_file = module_path / "__init__.py"
        assert init_py_file.exists(), f"__init__.py does not exist in {module_path}"
        logger.info(f"Importing nodes from '{module_path}' based on the types")

        spec = importlib.util.spec_from_file_location("custom", init_py_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        node_type_str_to_type = {}
        for node_type in self.node_types:
            module_node_type = getattr(module, node_type)
            globals()[node_type] = module_node_type
            node_type_str_to_type[node_type] = module_node_type
            sys.modules[f"{spec.name}.{node_type}"] = module_node_type
        return node_type_str_to_type
