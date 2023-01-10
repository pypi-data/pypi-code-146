from pydantic import BaseModel

from classiq.interface.chemistry.operator import PauliOperator
from classiq.interface.executor.quantum_program import QuantumProgram


class HamiltonianMinimizationProblem(BaseModel):
    ansatz: QuantumProgram
    hamiltonian: PauliOperator
