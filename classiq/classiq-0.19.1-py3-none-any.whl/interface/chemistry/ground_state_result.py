from typing import Dict, Union

from classiq.interface.executor.vqe_result import VQESolverResult
from classiq.interface.generator.complex_type import Complex
from classiq.interface.helpers.versioned_model import VersionedModel

GroundStateMapping = Dict[str, Complex]


class GroundStateExactResult(VersionedModel):
    energy: float
    ground_state: GroundStateMapping


class MoleculeExactResult(GroundStateExactResult):
    nuclear_repulsion_energy: float
    total_energy: float
    hartree_fock_energy: float


class HamiltonianExactResult(GroundStateExactResult):
    pass


#
class MoleculeResult(MoleculeExactResult, VQESolverResult):
    pass


class HamiltonianResult(HamiltonianExactResult, VQESolverResult):
    pass


CHEMISTRY_RESULTS_TYPE = Union[MoleculeResult, HamiltonianResult]
