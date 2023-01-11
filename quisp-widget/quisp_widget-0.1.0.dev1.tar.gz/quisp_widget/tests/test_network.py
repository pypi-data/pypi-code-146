import pytest

from ..network import Network
from ..qnode import QNode


def test_simple_network():
    network = Network("SimpleTestNetwork")
    qnode1 = QNode(name="qnode1", network=network, is_initiator=True)
    qnode2 = QNode(name="qnode2", network=network)
    qnode1.connect(qnode2)
    assert len(network.quantum_channels) == 1
    assert len(network.classical_channels) == 1
    assert len(network.qnodes) == 2
    expected = """
package networks;

import modules.*;
import channels.*;
import ned.IdealChannel;
import ned.DatarateChannel;
import modules.Backend.Backend;
import modules.Logger.Logger;

network SimpleTestNetwork {
    submodules:
        backend: Backend;
        logger: Logger;

        qnode1: QNode {
            address = 1;
            node_type = "EndNode";
            @display("i=COMP");
            is_initiator = true;
        }
        qnode2: QNode {
            address = 2;
            node_type = "EndNode";
            @display("i=COMP");
            is_initiator = false;
        }
        BSA1_2: HOM {
            address = 10000;
            @display("i=device/device");
        }
    connections:
        qnode1.port++ <--> ClassicalChannel {  distance = 10.0km; } <--> BSA1_2.port++;
        BSA1_2.port++ <--> ClassicalChannel {  distance = 10.0km; } <--> qnode2.port++;
        qnode1.quantum_port++ <--> QuantumChannel {  distance = 10.0km; } <--> BSA1_2.quantum_port++;
        BSA1_2.quantum_port++ <--> QuantumChannel {  distance = 10.0km; } <--> qnode2.quantum_port++;
}
"""
    assert network.dump() == expected

