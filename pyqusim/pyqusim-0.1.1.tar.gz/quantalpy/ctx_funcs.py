import functools
import typing as t

from quantalpy.ctx import _get_current_ctx
from quantalpy.qpu import QPU
from quantalpy.runnable import Runnable
from quantalpy.circuit import Circuit
from quantalpy.unary_qubit_gate import Hadamard, PhaseShift
from quantalpy.measure import Measure
from quantalpy.utils import export


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
                ctx.gates.append(runnable)
            case _:
                raise TypeError
        return result

    wrapper.__name__ = name
    wrapper.__qualname__ = name

    return wrapper


had = export(_create_ctx_function(Hadamard, "had"))
phase_shift = export(_create_ctx_function(PhaseShift, "phase_shift"))
measure = export(_create_ctx_function(Measure, "measure"))
