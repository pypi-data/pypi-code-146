import functools
import typing as t

from pyqusim.ctx import _get_current_ctx
from pyqusim.qpu import QPU
from pyqusim.runnable import Runnable
from pyqusim.circuit import Circuit
from pyqusim.unary_qubit_gate import UnaryQubitGate, Hadamard, PhaseShift

from pyqusim.measure import Measure
from pyqusim.utils import export


class _GateReplacer:
    def __init__(self, gate: UnaryQubitGate, circuit: Circuit, pos: int) -> None:
        self.gate = gate
        self.circuit = circuit
        self.pos = pos

    def controlled(self, control: int) -> None:
        self.circuit.gates[self.pos] = self.gate.controlled(control=control)


def _create_ctx_function(f: t.Type, name: str) -> t.Callable:
    @functools.wraps(f, assigned=("__annotations__",), updated=())
    def wrapper(*args, **kwargs):
        ctx = _get_current_ctx()
        runnable: Runnable = f(*args, **kwargs)
        result = None
        match ctx:
            case QPU():
                result = runnable.run(qpu=ctx)
            case Circuit():
                pos = len(ctx.gates)
                ctx.gates.append(runnable)
                if isinstance(runnable, UnaryQubitGate):
                    result = _GateReplacer(gate=runnable, circuit=ctx, pos=pos)
            case _:
                raise TypeError
        return result

    wrapper.__name__ = name
    wrapper.__qualname__ = name

    return wrapper


had = export(_create_ctx_function(Hadamard, "had"))
phase_shift = export(_create_ctx_function(PhaseShift, "phase_shift"))
measure = export(_create_ctx_function(Measure, "measure"))
