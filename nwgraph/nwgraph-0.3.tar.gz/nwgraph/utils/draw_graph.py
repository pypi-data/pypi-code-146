"""Graph drawer module"""
from typing import List
from pathlib import Path
from graphviz import Digraph

from ..logger import logger

class GraphDrawer:
    """Graph drawer class"""
    def __init__(self, nodes: List["Node"], edges: List["Edge"]):
        self.nodes = nodes
        self.edges = edges

        # Convert the names into basic ones, labeled by a string digit
        self.node_to_index = {nodes[i]: f"{i}" for i in range(len(nodes))}
        self.dot = self._build_dot()

    def _build_dot(self):
        """Build the dot object"""
        dot = Digraph(format="png", engine="fdp")
        # Each node also has a subgraph for other stuff, like GT box or edge networks
        subgraphs = {}
        for node in self.nodes:
            dot.node(name=self.node_to_index[node], label=node.name, shape="oval")
            subgraphs[node] = Digraph()

        # Draw all edges, assuming there are only two nodes
        for i in range(len(self.edges)):
            edge = self.edges[i]
            A, B = edge.nodes[0:2]
            dot.edge(self.node_to_index[A], self.node_to_index[B], len="2.0", label=f"  {i + 1}  ")

        return dot

    def draw(self, file_name: Path, cleanup: bool, view: bool):
        """The draw method"""
        file_name = Path(file_name).absolute()
        logger.debug(f"Graph draw saved to '{file_name}'")
        if file_name.suffix == ".png":
            file_name = Path(".".join(str(file_name).split(".")[0:-1]))
        self.dot.render(file_name, view=view, cleanup=cleanup)

    def __call__(self, file_name: Path, cleanup: bool = True, view: bool = False):
        self.draw(file_name, cleanup, view)
