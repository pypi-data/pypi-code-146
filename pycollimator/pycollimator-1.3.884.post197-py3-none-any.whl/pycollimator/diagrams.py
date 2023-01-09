import re

import pandas as pd
from typing import List, Optional

from pycollimator.error import NotFoundError
from pycollimator.i18n import N
from pycollimator.log import Log


# Current structure of SimulationModel:
# "diagram" : { ModelDiagram }
# "submodels": {
#   "references": {
#      "<uuid>": { "diagram_uuid": "<uuid>" },
#       ...
#   },
#   "diagrams": {
#     "<uuid>": { ModelDiagram }
#   }
# }


# FIXME FIXME FIXME
# We don't have a strong representation of the model, and we create
# Block objects on the fly. Modifying them means we need to backtrack
# to the model and update it somehow. Right now this scenario is limited
# to DataSourceBlock input data. We don't really want to allow modifying
# the model, so it's kinda okay. At least for now.


class Block:
    """
    Representation of a block in a model.

    Can be returned to the API user.
    """

    @classmethod
    def from_data(cls, data, model, path):
        if data.get("type") == "core.DataSource":
            return DataSourceBlock(data, model, path)
        return cls(data, model, path)

    def __init__(self, block_json, model, path):
        self.model = model
        self._json = block_json
        self.path = path

    def __getitem__(self, key):
        return self._json[key]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        if Log.is_level_above("DEBUG"):
            return f"<{self.__class__.__name__} name='{self.name}' type='{self.type}' uuid='{self.uuid}'>"
        return f"<{self.__class__.__name__} name='{self.name}' type='{self.type}'>"

    @property
    def name(self):
        return self._json["name"]

    @property
    def uuid(self):
        return self._json["uuid"]

    @property
    def type(self):
        return self._json["type"]

    # @property
    # def parameters(self):
    #     return self._json["parameters"]

    # TODO: expose setting block params

    def get_parameter(self, name: str, no_eval=False):
        param = self._json["parameters"].get(name)
        Log.trace(f"get_parameter: {name}={param}")
        if param is None:
            raise NotFoundError(N(f"Block '{self}' of type '{self.type}' does not have parameter '{name}'"))
        if param.get("is_string", False) is True:
            return str(param["value"])
        if no_eval is True:
            return param["value"]
        expr = param.get("expression") or param["value"]
        evaluated = eval(expr)
        return evaluated


# Special block that reads csv
class DataSourceBlock(Block):
    def __init__(self, block_json, model, path):
        if block_json.get("type") != "core.DataSource":
            raise TypeError(N("DataSourceBlock must be created from a DataSource block"))
        super().__init__(block_json, model, path)
        self.data = None

    def set_data(self, data: pd.DataFrame):
        # FIXME make sure the shape is correct and all that
        if not isinstance(data, pd.DataFrame):
            raise TypeError(N("Input data must be a pandas DataFrame"))
        # set data of a DataSource block
        Log.trace("set_data, shape:", data.shape, "block:", self.__repr__())
        self.data = data.copy()
        self.data.index.name = "time"
        self.model._set_datasource_data(self, self.data)


class ModelDiagram:
    """
    Contents of a fully loaded model diagram (single plane).

    For use by internal APIs.
    """

    def __init__(self, data, model):
        self.model = model
        self.diagram = data

    def __str__(self) -> str:
        if self.diagram.get("name") is not None:
            return self.diagram["name"]
        return self.diagram["uuid"]

    def __repr__(self) -> str:
        if Log.is_level_above("DEBUG"):
            uid = self.diagram["uuid"]
            return f"<{self.__class__.__name__} model='{self.model}' uuid='{uid}'>"
        return f"<{self.__class__.__name__} model='{self.model}'>"

    @property
    def nodes(self):
        return self.diagram.get("nodes", [])

    @property
    def links(self):
        return self.diagram.get("links", [])

    # Full path only works at the model graph level.
    def find_block(self, pattern: str = None, name: str = None, type: str = None, ignorecase=True) -> Optional[Block]:
        blocks = self.find_blocks(pattern=pattern, name=name, type=type, case=ignorecase)
        if len(blocks) == 0:
            return None
        if len(blocks) > 1:
            raise NotFoundError(N(f"Multiple blocks found for '{name}' in model '{self}'"))
        return blocks[0]

    # todo: do a search on model graph that constructs path 5
    # Not to be called with a path name as path name is unique.
    # probably won't need this ModelDiagram helper once BFS / path construction implemented at ModelGraph level
    def find_blocks(self, pattern: str = None, name: str = None, type: str = None, case=True) -> List[Block]:
        found = None
        model_graph = self.model._graph

        if name is None and pattern is None and type is None:
            pattern = ""  # matches any string

        if pattern is not None:
            rgx = re.compile(pattern, re.IGNORECASE if not case else 0)
            # yes. yikes. but going away with support for V2
            found = [
                Block.from_data(
                    node, self.model, model_graph._get_block_path(model_graph.root_diagram, node.get("uuid"), "")
                )
                for node in self.nodes
                if rgx.match(node.get("name"))
            ]
        if name is not None:
            if not case:
                found = [
                    Block.from_data(
                        node, self.model, model_graph._get_block_path(model_graph.root_diagram, node.get("uuid"), "")
                    )
                    for node in self.nodes
                    if node.get("name", "").lower() == name.lower()
                ]
            else:
                found = [
                    Block.from_data(
                        node, self.model, model_graph._get_block_path(model_graph.root_diagram, node.get("uuid"), "")
                    )
                    for node in self.nodes
                    if node.get("name") == name
                ]

        # If type is set: filter by type, or return all blocks of the given type if no other search criteria was set
        if type is not None:
            if not type.startswith("core."):
                type = "core." + type
            type = type.lower()
            if name is None and pattern is None:
                found = [
                    Block.from_data(
                        node, self.model, model_graph._get_block_path(model_graph.root_diagram, node.get("uuid"), "")
                    )
                    for node in self.nodes
                    if node.get("type").lower() == type
                ]
            else:
                found = [blk for blk in found if blk.type.lower() == type]

        return found


class ModelGraph:
    """
    Contents of a fully loaded model graph (all loadable planes).

    For use by internal APIs.
    """

    def __init__(self, data, model):
        self._data = data
        self._model = model
        self.uuid = data.get("uuid")
        self.name = data.get("name")
        self.root_diagram = ModelDiagram(data["diagram"], model=self._model)
        self.diagrams_by_submodel_uuid = {}  # type: Dict[str, ModelDiagram]

        submodel_diagrams = data.get("submodels", {}).get("diagrams", {})
        submodel_references = data.get("submodels", {}).get("references", {})
        self.submodel_references = submodel_references

        for submodel_uuid in self.submodel_references:
            ref = self.submodel_references[submodel_uuid]
            diagram_uuid = ref["diagram_uuid"]
            diagram = submodel_diagrams[diagram_uuid]
            self.diagrams_by_submodel_uuid[submodel_uuid] = ModelDiagram(diagram, model)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        if Log.is_level_above("DEBUG"):
            return f"<{self.__class__.__name__} model='{self._model}' uuid='{self.uuid}'>"
        return f"<{self.__class__.__name__} model='{self._model}'>"

    # def get_diagram(self, diagram_uuid: str = None):
    #     if diagram_uuid is None:
    #         return self.root_diagram
    #     return ModelDiagram(self._data["diagrams"][diagram_uuid], model=self._model)

    # def get_submodel_diagram(self, submodel_uuid):
    #     return ModelDiagram(
    #         self.get_diagram(self._data["submodels"]["references"][submodel_uuid]["diagram_uuid"]), model=self._model
    #     )

    # todo add case flag.
    # todo generalize
    def find_block_by_path(self, path: str):
        diagram = self.root_diagram
        path_to_traverse = path.split(".")

        for name in path_to_traverse[:-1]:
            matched_nodes = [node for node in diagram.nodes if node["name"] == name]
            if len(matched_nodes) == 0:
                raise NotFoundError(N(f"No block was found in path '{path}' "))
            if len(matched_nodes) > 1:
                raise NotFoundError(N(f"Multiple matching blocks found in path '{path}' "))
            node = matched_nodes[0]
            if not (node["type"] == "core.Submodel" or node["type"] == "core.Group"):
                raise NotFoundError(N(f"No block was found in path '{path}' "))
            # move onto next diagram
            diagram = self.diagrams_by_submodel_uuid[node["uuid"]]

        # last name in path can be any type of block
        last_name = path_to_traverse[-1]
        found_blocks = [node for node in diagram.nodes if node["name"] == last_name]

        if len(found_blocks) == 0:
            raise NotFoundError(N(f"No block was found in path '{path}' "))
        if len(found_blocks) > 1:
            raise NotFoundError(N(f"Multiple matching blocks found in path '{path}' "))

        return Block.from_data(found_blocks[0], diagram.model, path)

    # FIXME walk and construct blocks paths
    # For non-path search.
    # The ModelGraph is the 'root' class in which you can traverse. ModelDiagram is a node.
    # No cycles in graph/diagrams representation of model.
    # With submodels v2, UUIDs are not unique, so we must construct full paths for any block that is initialized.
    # Later, consider doing this upfront and only constructing full graph once.
    # todo: do a search the model graph that constructs path 4.
    def find_blocks(self, pattern: str = None, name: str = None, type: str = None, case=True) -> List[Block]:
        found = []

        # find in root diagram
        nodes = self.root_diagram.find_blocks(pattern=pattern, name=name, type=type, case=case)
        for node in nodes:
            found.append(node)

        # todo: BFS through submodel and construct paths
        # FIXME: this walks submodels in random order and doesn't know blocks paths
        # need to use the references
        for submodel_uuid in self.diagrams_by_submodel_uuid:
            submodel_diagram = self.diagrams_by_submodel_uuid[submodel_uuid]
            nodes = submodel_diagram.find_blocks(pattern=pattern, name=name, type=type, case=case)
            for node in nodes:
                found.append(node)

        return found

    # ! Supports V1 only where UUID is unique. OK for now as there's no V2 support yet
    # (submodels missing in V2 models), but will go away with path construction traversal
    # todo remove function completely for V2 submodels as UUID is not unique
    def _get_block_path(self, diagram: ModelDiagram, block_uuid: str, pfx: str) -> str:
        for node in diagram.nodes:
            if node["uuid"] == block_uuid:
                return f"{pfx}{node['name']}"
            if node["type"] == "core.Submodel" or node["type"] == "core.Group":
                submodel_diagram = self.diagrams_by_submodel_uuid[node["uuid"]]
                found = self._get_block_path(submodel_diagram, block_uuid, f"{pfx}{node['name']}.")
                if found:
                    return found
        return None

    def get_block_path(self, block):
        """
        Get the path of a block in the model.
        """
        if not isinstance(block, Block):
            blocks = self.find_blocks(name=block)
            if len(blocks) == 0:
                blocks = self.find_blocks(pattern=block)
            if len(blocks) == 0:
                raise NotFoundError(N(f"No block found for '{block}'"))
            if len(blocks) > 1:
                raise NotFoundError(N(f"Multiple blocks found for '{block}'"))
            return blocks[0].path
        return block.path
