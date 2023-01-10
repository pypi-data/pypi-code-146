"""Представление для https://github.com/blockdiag/nwdiag.

Примеры диаграмм - http://blockdiag.com/en/nwdiag/nwdiag-examples.html
"""

from typing import NamedTuple


from dataclass_to_diagram.dia.base import BaseDiagram, Image
from dataclass_to_diagram.service.kroki import (
    DiagramTypes,
    OutputFormats,
    get_image,
)


class NodeInNetwork(NamedTuple):
    """Узел в сети."""

    node: "Node"
    address: list[str]


class Node:
    """Узел."""

    def __init__(self: "Node", name: str) -> None:
        """Construct node."""
        self.__name = name

    @property
    def name(self: "Node") -> str:
        """Node name."""
        return self.__name


class Network:
    """Сеть."""

    def __init__(
        self: "Network",
        name: str = "",
        address: str = None,
    ) -> None:
        """Construct network."""
        self.__name = name
        self.__address = address
        self.__nodes: list[NodeInNetwork] = []

    def __repr__(self: "Network") -> str:
        """Represent string."""
        out = ""
        out += f"\tnetwork {self.__name} {{\n"
        if self.__address is not None:
            out += f'\t\taddress = "{self.__address}"\n'
        for node in self.__nodes:
            address = ", ".join(node.address)
            out += f'\t\t{node.node.name} [address = "{address}"]\n'
        out += "\t}\n"
        return out

    def add_node(self: "Network", node: Node, address: set[str] = ()) -> None:
        """Добавить узел к сети."""
        self.__nodes.append(NodeInNetwork(node=node, address=address))


class PeerNetwork:
    """Одноранговая сеть."""

    def __init__(
        self: "PeerNetwork",
        node1: NodeInNetwork,
        node2: NodeInNetwork,
    ) -> None:
        """Создать однорангувую сеть."""
        self.__node1 = node1
        self.__node2 = node2

    def __repr__(self: "PeerNetwork") -> str:
        """Represent string."""
        out = ""
        out += f"\t{self.__node1.name}\n"
        out += f"\t{self.__node2.name}\n"
        out += f"\t{self.__node1.name} -- {self.__node2.name}\n"
        return out


class Group:
    """Группа узлов."""

    def __init__(
        self: "Group",
        name: str,
        nodes: set[Node],
        color: str | None = None,
    ) -> None:
        """Construct group."""
        self.__name = name
        self.__color = color
        self.__nodes = nodes

    def __repr__(self: "Group") -> str:
        """Represent string."""
        out = ""
        out += f"\tgroup {self.__name} {{\n"
        if self.__color is not None:
            out += f'\t\tcolor = "{self.__color}";\n'
        for node in self.__nodes:
            out += f"\t\t{node.name};\n"
        out += "\t}\n"
        return out


class Diagram(BaseDiagram):
    """Общая диаграмма."""

    def __init__(
        self: "Diagram",
        filename: str,
        networks: set[Network],
        peer_networks: set[PeerNetwork] = (),
        groups: set[Group] = (),
    ) -> None:
        """Construct diagram."""
        super().__init__(filename)
        self.__networks = networks
        self.__peer_networks = peer_networks
        self.__groups = groups

    def add_network(self: "Diagram", network: Network) -> None:
        """Добавить сеть на диаграмму."""
        self.__networks.append(network)

    def get_images(self: "Diagram") -> tuple[Image]:
        """Возвращает кортеж изображений."""
        images: list[Image] = []
        for fmt in (OutputFormats.PNG, OutputFormats.SVG):
            images.append(
                Image(
                    filename=self.filename + "." + fmt.value,
                    content=get_image(
                        source=repr(self),
                        diagram_type=DiagramTypes.NWDIAG,
                        output_format=fmt,
                    ),
                ),
            )
        return tuple(images)

    def __repr__(self: "Diagram") -> str:
        """Represent string."""
        out = ""
        out += "nwdiag {\n"
        for net in self.__peer_networks:
            out += repr(net)
        for net in self.__networks:
            out += repr(net)
        for group in self.__groups:
            out += repr(group)
        out += "}\n"
        return out
