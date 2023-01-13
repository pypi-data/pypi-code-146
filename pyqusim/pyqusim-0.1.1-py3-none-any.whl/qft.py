from collections.abc import Collection

import numpy as np

from quantalpy.circuit import Circuit
from quantalpy.unary_qubit_gate import Hadamard, PhaseShift
from quantalpy.binary_qubit_gate import ControlledQubitGate
from quantalpy.utils import export


@export
def qft(indices: Collection[int]) -> Circuit:
    c = Circuit()

    for i in indices:
        c.gates.append(Hadamard(i))
        for a, x in enumerate(range(2, len(indices) + 1 - i), start=1):
            gate = PhaseShift(phi=2 * np.pi / (2**x), index=i)
            c.gates.append(ControlledQubitGate(gate=gate, control=i + a))

    return c
