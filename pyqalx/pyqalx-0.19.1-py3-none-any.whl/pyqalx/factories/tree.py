from treelib import Tree

from pyqalx.core.errors import QalxError


class QalxTree(Tree):
    """
    Given a tree structure as a dictionary will build a treelib.Tree
    instance of that structure.  Implements a few helper methods in order
    to find specific nodes quickly
    """

    def __init__(self, tree_definition, *args, **kwargs):
        super(QalxTree, self).__init__(*args, **kwargs)
        assert isinstance(tree_definition, dict)

        if len(tree_definition) > 1:
            raise QalxError(
                f"Must have only one root node."
                f'  Got {", ".join(tree_definition.keys())}'
            )
        root, successors = tuple(tree_definition.items())[0]
        self.create_node(root, root)
        # Create all the successor nodes recursively
        self.create_successors(root, successors)

    def create_successors(self, root, successor):
        """
        For a given root will create the successor nodes recursively
        :param root: The root node
        :param successor: The successor node
        """
        if isinstance(successor, str):
            # Leaf Node
            self.create_node(successor, successor, parent=root)
        elif isinstance(successor, dict):
            # Dict with successor nodes
            for _successor_name, _successors in successor.items():
                self.create_node(_successor_name, _successor_name, parent=root)
                self.create_successors(_successor_name, _successors)
        elif isinstance(successor, list):
            # List of sibling nodes
            for _ in successor:
                self.create_successors(root, _)

    def get_successors(self, node_name):
        """
        Given a name will provide the immediate successors to this node
        :param node_name: The name of the node that you want to find the
        successors for
        :return:The immediate successors to the found node
        """
        node = self.get_node(node_name)
        if node is not None:
            return node.successors(self.identifier)
