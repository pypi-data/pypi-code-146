from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

import pypika
import sqlparse

from tecton_core.vendor.treelib import Tree

INDENT_BLOCK = "  "


@dataclass
class NodeRef:
    """
    Used so we can more easily modify the QueryTree by inserting and removing nodes, e.g.
    def subtree_rewrite(subtree_node_ref):
        subtree_node_ref.node = NewNode(subtree_node_ref.node)
    """

    node: "QueryNode"

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.node.columns

    @property
    def inputs(self):
        return self.node.inputs

    @property
    def input_names(self):
        return self.node.input_names

    def as_str(self) -> str:
        return self.node.as_str()

    def pretty_str(
        self,
        node_id: bool = True,
        name: bool = True,
        description: bool = True,
        columns: bool = False,
    ) -> str:
        """Returns a string that represents the query tree which has this NodeRef as the root node.

        Args:
            node_id: If True, the unique id associated with each node will be rendered.
            name: If True, the class names of the nodes will be rendered.
            description: If True, the actions of the nodes will be rendered.
            columns: If True, the columns of each node will be rendered as an appendix after tree itself.
        """
        assert name or description, "At least one of 'name' or 'description' must be True."
        if columns:
            assert node_id, "Can only show columns if 'node_id' is True."
        tree = self.create_tree(node_id=node_id, name=name, description=description)

        # key=False ensures that nodes on the same level are sorted by id and stdout=False ensures a string is returned
        tree_str = tree.show(key=False, stdout=False)

        if not columns:
            return tree_str

        node_columns = []
        max_node_id = tree.size()
        for unique_id in range(1, max_node_id + 1):
            node = tree.get_node(unique_id).data
            node_columns.append(f"<{unique_id}> " + f"{'|'.join(node.columns)}")

        return tree_str + "\n" + "\n".join(node_columns)

    def _to_query(self) -> pypika.Query:
        return self.node._to_query()

    def to_sql(self) -> str:
        """
        Attempts to recursively generate sql for this and child nodes.
        """
        return self.node.to_sql()

    def create_tree(self, node_id: bool = True, name: bool = True, description: bool = True) -> Tree:
        """Creates a Tree to represent the query tree which has this NodeRef as the root node.

        The Tree is built so that it can immediately generate a string representation.

        Args:
            node_id: If True, the unique id associated with each node will be rendered.
            name: If True, the class names of the nodes will be rendered.
            description: If True, the actions of the nodes will be rendered.
            columns: If True, the columns of each node will be rendered as an appendix after tree itself.
        """
        tree = Tree()
        self._create_tree(tree=tree, parent_id=None, node_id=node_id, name=name, description=description)
        return tree

    def _create_tree(
        self,
        tree: Tree,
        prefix: str = "",
        parent_id: Optional[int] = None,
        node_id: bool = True,
        name: bool = True,
        description: bool = True,
    ):
        tag = ""

        # Node ids are assigned sequentially, starting with 1.
        unique_id = tree.size() + 1
        if node_id:
            tag += f"<{unique_id}> "

        tag += prefix

        # Add parameter names to the node class. For example, EntityFilterNode(feature_data, entities).
        node_name = self.node.__class__.__name__
        if self.input_names:
            node_name += f"({', '.join(self.input_names)})"

        if name and description:
            tag += f"{node_name}: {self.as_str()}"
        elif name:
            tag += f"{node_name}"
        elif description:
            tag += f"{self.as_str()}"

        # The rendering is messed up if the tag has a newline.
        assert "\n" not in tag

        # We attach this NodeRef so that it can be retrieved later by its node id.
        tree.create_node(tag=tag, identifier=unique_id, parent=parent_id, data=self.node)

        # Recursively handle all children.
        if self.input_names:
            assert len(self.input_names) == len(
                self.inputs
            ), f"`input_names` has length {len(self.input_names)} but `inputs` has length {len(self.inputs)}"
            for input_name, i in zip(self.input_names, self.inputs):
                prefix = f"[{input_name}] "
                i._create_tree(
                    tree=tree,
                    prefix=prefix,
                    parent_id=unique_id,
                    node_id=node_id,
                    name=name,
                    description=description,
                )
        else:
            for i in self.inputs:
                i._create_tree(
                    tree=tree,
                    parent_id=unique_id,
                    node_id=node_id,
                    name=name,
                    description=description,
                )


class QueryNode(ABC):
    @property
    @abstractmethod
    def columns(self) -> Tuple[str, ...]:
        """
        The columns in the projectlist coming out of this node.
        """

    def as_ref(self) -> NodeRef:
        return NodeRef(self)

    # used for recursing through the tree for tree rewrites
    @property
    @abstractmethod
    def inputs(self) -> Tuple[NodeRef]:
        pass

    @property
    def input_names(self) -> Optional[List[str]]:
        """Returns a list of names for the inputs of this node, if all inputs have names. Otherwise returns None.

        If a list is returned, the order of the names should correspond to the order of nodes in the `inputs` property.
        """
        return None

    @abstractmethod
    def as_str(self) -> str:
        """
        Prints contents of this node and calls recursively on its inputs.
        Used by tecton.TectonDataFrame.explain
        """

    def to_sql(self) -> str:
        """
        Attempts to recursively generate sql for this and child nodes.
        """
        sql_str = self._to_query().get_sql()
        return sqlparse.format(sql_str, reindent=True)

    @abstractmethod
    def _to_query(self) -> pypika.Query:
        """
        Attempts to recursively generate sql query for this and child nodes.
        """


class DataframeWrapper(ABC):
    """
    A wrapper around pyspark, pandas, snowflake, etc dataframes provides a common interface through which we
    can register views.
    """

    @property
    def _dataframe(self) -> Any:
        """
        The underlying dataframe
        """
        raise NotImplementedError

    @property
    def columns(self) -> List[str]:
        """
        The columns of the dataframe
        """
        raise NotImplementedError

    @abstractmethod
    def _register_temp_view(self):
        """
        Registers a temp view for the data
        """

    # @abstractmethod
    @property
    def _temp_view_name(self):
        """
        Gets the temp view name registered by register()
        """
        return f"TMP_VIEW_{id(self._dataframe)}"


def recurse_query_tree(node_ref: NodeRef, f: Callable):
    f(node_ref.node)
    for child in node_ref.inputs:
        recurse_query_tree(child, f)
