from enum import Enum
from typing import List, Optional, Tuple, Union

import pydantic

from classiq.interface.chemistry import molecule
from classiq.interface.chemistry.fermionic_operator import SummedFermionicOperator
from classiq.interface.generator.excitations import EXCITATIONS_TYPE

"""
The correct type hint is:
NumSpinUpParticles = pydantic.NonNegativeInt
NumSpinDownParticles = pydantic.NonNegativeInt
NumParticles = Tuple[NumSpinUpParticles, NumSpinDownParticles]

But:
A) the NonNegativeInt makes the ts-schemas have a `Minimum` object,
    which is undefined, thus causing an error
B) a tuple of a specific size gives another, different error

Thus, we use `int` and manually check its value
And use a list, and manually check its length
"""
NumSpinUpParticles = pydantic.NonNegativeInt
NumSpinDownParticles = pydantic.NonNegativeInt
NumParticles = Tuple[NumSpinUpParticles, NumSpinDownParticles]


class FermionMapping(str, Enum):
    JORDAN_WIGNER = "jordan_wigner"
    PARITY = "parity"
    BRAVYI_KITAEV = "bravyi_kitaev"
    FAST_BRAVYI_KITAEV = "fast_bravyi_kitaev"


class GroundStateProblem(pydantic.BaseModel):
    mapping: FermionMapping = pydantic.Field(
        default=FermionMapping.JORDAN_WIGNER, description="Fermionic mapping type"
    )
    z2_symmetries: bool = pydantic.Field(
        default=False,
        description="whether to perform z2 symmetries reduction",
    )
    num_qubits: Optional[int] = pydantic.Field(default=None)

    @pydantic.validator("z2_symmetries")
    def validate_z2_symmetries(cls, value, values):
        if value and values.get("mapping") == FermionMapping.FAST_BRAVYI_KITAEV:
            raise ValueError(
                "z2 symmetries reduction can not be used for fast_bravyi_kitaev mapping"
            )
        return value


class MoleculeProblem(GroundStateProblem):
    molecule: molecule.Molecule
    basis: str = pydantic.Field(default="sto3g", description="Molecular basis set")
    freeze_core: bool = pydantic.Field(default=False)
    remove_orbitals: List[int] = pydantic.Field(
        default_factory=list, description="list of orbitals to remove"
    )


class HamiltonianProblem(GroundStateProblem):
    hamiltonian: SummedFermionicOperator = pydantic.Field(
        description="Hamiltonian as a fermionic operator"
    )
    num_particles: List[pydantic.PositiveInt] = pydantic.Field(
        description="Tuple containing the numbers of alpha particles and beta particles"
    )

    @pydantic.validator("num_particles")
    def validate_num_particles(cls, num_particles: List[int]) -> List[int]:
        assert isinstance(num_particles, list)
        assert len(num_particles) == 2

        # This probably will never happen, since pydantic automatically converts
        #   floats to ints
        assert isinstance(num_particles[0], int)
        assert num_particles[0] >= 1

        assert isinstance(num_particles[1], int)
        assert num_particles[1] >= 1

        return num_particles


CHEMISTRY_PROBLEMS = (MoleculeProblem, HamiltonianProblem)
CHEMISTRY_PROBLEMS_TYPE = Union[MoleculeProblem, HamiltonianProblem]
CHEMISTRY_ANSATZ_NAMES = ["hw_efficient", "ucc", "hva"]


class GroundStateProblemAndExcitations(pydantic.BaseModel):
    problem: CHEMISTRY_PROBLEMS_TYPE
    excitations: EXCITATIONS_TYPE
