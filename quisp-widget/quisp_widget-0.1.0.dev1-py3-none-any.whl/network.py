from typing import TYPE_CHECKING, List
from .types import LinkType

if TYPE_CHECKING:
    from .qnode import QNode
    from .channel import ClassicalChannel, QuantumChannel


class Network:
    qnodes: List["QNode"]
    classical_channels: List["ClassicalChannel"]
    quantum_channels: List["QuantumChannel"]
    name: str

    def __init__(self, name: str) -> None:
        self.qnodes = []
        self.classical_channels = []
        self.quantum_channels = []
        self.name = name

    def add_classical_channel(self, channel: "ClassicalChannel") -> None:
        if channel not in self.classical_channels:
            self.classical_channels.append(channel)

    def add_quantum_channel(self, channel: "QuantumChannel") -> None:
        if channel not in self.quantum_channels:
            self.quantum_channels.append(channel)

    def add_qnode(self, qnode: "QNode") -> None:
        if qnode not in self.qnodes:
            self.qnodes.append(qnode)
            qnode.addr = len(self.qnodes)

    def dump_qnodes(self) -> str:

        ned_str = ""
        for qnode in self.qnodes:
            ned_str += f"""
        {qnode.name}: QNode {{
            address = {qnode.addr};
            node_type = "EndNode";
            @display("i=COMP");
            is_initiator = {"true" if qnode.is_initiator else "false"};
        }}"""

        for c in self.quantum_channels:
            if c.option.link_type is LinkType.MIM:
                ned_str += f"""
        {c.option.bsa_node_name}: HOM {{
            address = {c.option.bsa_node_addr};
            @display("i=device/device");
        }}"""
        return ned_str

    def dump_connections(self) -> str:
        ned_str = ""
        for channel in self.classical_channels:
            ned_str += channel.dump()
        for channel in self.quantum_channels:
            ned_str += channel.dump()
        return ned_str

    def dump(self) -> str:
        for i, c in enumerate(self.quantum_channels):
            opt = c.option
            if opt.link_type is LinkType.MIM:
                opt.bsa_node_addr = i + 10000
                opt.bsa_node_name = f"BSA{c.qnode1.addr}_{c.qnode2.addr}"
        connections = self.dump_connections()
        qnodes = self.dump_qnodes()
        return """
package networks;

import modules.*;
import channels.*;
import ned.IdealChannel;
import ned.DatarateChannel;
import modules.Backend.Backend;
import modules.Logger.Logger;

network {} {{
    submodules:
        backend: Backend;
        logger: Logger;
{}
    connections:{}
}}
""".format(
            self.name, qnodes, connections
        )
