from dataclasses import dataclass
from typing import Optional, Tuple

import networkx as nx

from classiq.interface.generator.function_call import ZERO_INDICATOR, FunctionCall
from classiq.interface.generator.function_params import IO

from classiq.exceptions import ClassiqWiringError
from classiq.model_designer import logic_flow_change_handler
from classiq.quantum_register import QReg, Qubit


# We need the dataclass to be hashable for inserting it into the graph,
# hence the dataclass is frozen.
@dataclass(frozen=True)
class _Pin:
    pin_name: str
    index: int
    func_call: Optional[FunctionCall]
    io: IO  # We need to store IO because a function may have an input and an output pin with the same name

    def __str__(self) -> str:
        return f"{self.pin_name}[{self.index}]"


@dataclass(frozen=True)
class _ZeroPin(_Pin):
    def __init__(self, io: IO):
        super().__init__(pin_name=ZERO_INDICATOR, index=0, func_call=None, io=io)

    def __str__(self) -> str:
        return ZERO_INDICATOR


class _StrictDiGraph(nx.DiGraph):
    def add_edge(self, u_of_edge, v_of_edge, **attr) -> None:
        if u_of_edge in self and v_of_edge in self[u_of_edge]:
            raise ClassiqWiringError(
                f"Cannot reconnect an already connected edge: {u_of_edge}, {v_of_edge}"
            )
        super().add_edge(u_of_edge, v_of_edge, **attr)


INVALID_QUBITS_ERROR_MESSAGE = (
    "Cannot use a QReg with consumed or uninitialized qubits:"
)


class LogicFlowBuilder:
    def __init__(self) -> None:
        self._logic_flow_graph = _StrictDiGraph()
        self._connect_qubit_func = {
            IO.Input: self._connect_qubit_to_func_call,
            IO.Output: self._connect_func_call_to_qubit,
        }

    def _is_qubit_available(self, qubit: Qubit) -> bool:
        return qubit in self._logic_flow_graph.nodes

    def _validate_qreg(self, qreg: QReg) -> None:
        invalid_qubit_indices = [
            i
            for i, qubit in enumerate(qreg.qubits)
            if not self._is_qubit_available(qubit)
        ]
        if invalid_qubit_indices:
            raise ClassiqWiringError(
                f"{INVALID_QUBITS_ERROR_MESSAGE} {invalid_qubit_indices}"
            )

    def _verify_no_loops(self, dest_node: FunctionCall):
        if not nx.is_directed_acyclic_graph(self._logic_flow_graph):
            raise ClassiqWiringError(f"Cannot wire function {dest_node} to itself")

    def _connect_qubit_to_func_call(
        self, qubit: Qubit, dest_pin: _Pin, dest_node: Optional[FunctionCall]
    ) -> None:
        if dest_node is not None:
            self._logic_flow_graph.add_edge(dest_pin, dest_node)
        source_node, source_pin = self._get_source_node_and_pin(qubit)
        # relabel_nodes replaces a node with another (inplace and keeping the edges)
        nx.relabel_nodes(self._logic_flow_graph, {qubit: dest_pin}, copy=False)
        logic_flow_change_handler.handle_inner_connection(
            source_node,
            str(source_pin),
            str(dest_pin),
            dest_node,
        )

    def _get_source_node_and_pin(self, qubit: Qubit) -> Tuple[FunctionCall, _Pin]:
        source_pin = next(self._logic_flow_graph.predecessors(qubit))
        source_node = next(self._logic_flow_graph.predecessors(source_pin))
        return source_node, source_pin

    def _connect_func_call_to_qubit(
        self, qubit: Qubit, source_pin: _Pin, source_node: FunctionCall
    ) -> None:
        self._logic_flow_graph.add_edge(source_node, source_pin)
        self._logic_flow_graph.add_edge(source_pin, qubit)

    def _connect_io(
        self,
        io: IO,
        func_node: FunctionCall,
        pin_name: str,
        qreg: QReg,
        pin_indices: Optional[range] = None,
    ) -> None:
        if pin_indices is None:
            pin_indices = range(len(qreg))
        pins = [_Pin(pin_name, i, func_node, io) for i in pin_indices]
        for pin, qubit in zip(pins, qreg.qubits):
            self._connect_qubit_func[io](qubit, pin, func_node)

    def connect_qreg_to_func_call(
        self,
        source: QReg,
        dest_pin_name: str,
        dest_func_call: FunctionCall,
        pin_indices: Optional[range] = None,
    ) -> None:
        self._validate_qreg(source)
        self._connect_io(IO.Input, dest_func_call, dest_pin_name, source, pin_indices)
        self._verify_no_loops(dest_func_call)

    def connect_func_call_to_qreg(
        self, source_func_call: FunctionCall, source_pin_name: str, dest: QReg
    ) -> None:
        self._connect_io(IO.Output, source_func_call, source_pin_name, dest)

    def connect_qreg_to_zero(self, source: QReg) -> None:
        for qubit in source.qubits:
            self._connect_qubit_to_func_call(qubit, _ZeroPin(IO.Output), None)
