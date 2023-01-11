from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass
from .types import LinkType

if TYPE_CHECKING:
    from .network import Network
    from .qnode import QNode


@dataclass
class ChannelOption:
    # [km]
    quantum_channel_distance: float  = 20.0
    classical_channel_distance: float = 20.0
    link_type: LinkType = LinkType.MIM
    bsa_node_name: Optional[str] = None
    bsa_node_addr: Optional[int] = None

class ClassicalChannel:
    qnode1: "QNode"
    qnode2: "QNode"
    network: "Network"
    option: "ChannelOption"

    def __init__(self, qnode1: "QNode", qnode2: "QNode", option: "ChannelOption") -> None:
        self.qnode1 = qnode1
        self.qnode2 = qnode2
        self.network = qnode1.network
        self.option = option

    def dump(self) -> str:
        if self.option.link_type is LinkType.MM:
            return f"""
        {self.qnode1.name}.port++ <--> ClassicalChannel {{  distance = {self.option.classical_channel_distance}km; }} <--> {self.qnode2.name}.port++;"""
        else:
            assert self.option.bsa_node_name is not None
            assert self.option.bsa_node_addr is not None
            return f"""
        {self.qnode1.name}.port++ <--> ClassicalChannel {{  distance = {self.option.classical_channel_distance * 0.5}km; }} <--> {self.option.bsa_node_name}.port++;
        {self.option.bsa_node_name}.port++ <--> ClassicalChannel {{  distance = {self.option.classical_channel_distance * 0.5}km; }} <--> {self.qnode2.name}.port++;"""

class QuantumChannel:
    qnode1: "QNode"
    qnode2: "QNode"
    network: "Network"
    option: "ChannelOption"

    def __init__(self, qnode1: "QNode", qnode2: "QNode", option: "ChannelOption") -> None:
        self.qnode1 = qnode1
        self.qnode2 = qnode2
        self.network = qnode1.network
        self.option = option

    def dump(self) -> str:
        if self.option.link_type is LinkType.MM:
            return f"""
        {self.qnode1.name}.quantum_port++ <--> QuantumChannel {{  distance = {self.option.quantum_channel_distance}km; }} <--> {self.qnode2.name}.quantum_port++;"""
        else:
            assert self.option.bsa_node_name is not None
            assert self.option.bsa_node_addr is not None
            return f"""
        {self.qnode1.name}.quantum_port++ <--> QuantumChannel {{  distance = {self.option.quantum_channel_distance * 0.5}km; }} <--> {self.option.bsa_node_name}.quantum_port++;
        {self.option.bsa_node_name}.quantum_port++ <--> QuantumChannel {{  distance = {self.option.quantum_channel_distance * 0.5}km; }} <--> {self.qnode2.name}.quantum_port++;"""

