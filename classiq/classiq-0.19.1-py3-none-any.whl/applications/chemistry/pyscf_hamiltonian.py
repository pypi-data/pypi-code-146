import logging
from typing import Tuple

import numpy as np

from classiq.interface.chemistry.fermionic_operator import (
    FermionicOperator,
    SummedFermionicOperator,
)
from classiq.interface.chemistry.ground_state_problem import (
    HamiltonianProblem,
    MoleculeProblem,
)

_logger = logging.getLogger(__name__)

try:
    from pyscf import scf
    from pyscf.gto import Mole
except ImportError:
    _logger.warning(
        "PYSCF module not found. "
        "This module is optional. "
        "If you wish to use this module please install PYSCF manually."
    )


def generate_hamiltonian_from_pyscf(
    molecule_problem: MoleculeProblem,
) -> HamiltonianProblem:
    """
    Conversion method from MoleculeProblem to HamiltonianProblem based on
    PYSCF chemistry package. The method extracts the one-body and two-body
    electron integrals, transfers them from atomic orbitals to molecular orbitals,
    and then presents them using FermionOperators.

    Args:
        molecule_problem (MoleculeProblem): chemical information of the input molecule.

    Returns:
        HamiltonianProblem

    """
    molecule = _to_pyscf_molecule(molecule_problem)

    # running pyscf driver
    rhf = scf.RHF(molecule)
    rhf.verbose = 0  # avoid unnecessary printing
    rhf.kernel()

    # extracting chemical properties from pyscf
    hcore = rhf.get_hcore()
    int2e = molecule.intor("int2e", aosym=1)
    mo_coeff = rhf.mo_coeff

    # atomic orbitals to molecular orbitals
    mo_1e_einsum = _truncate(
        array=np.einsum("pq,pi,qj->ij", hcore, mo_coeff, mo_coeff), threshold=1e-12
    )

    mo_2e_einsum = _truncate(
        array=np.einsum(
            "pqrs,pi,qj,rk,sl->ijkl", int2e, *[mo_coeff] * 4, optimize=True
        ),
        threshold=1e-12,
    )

    fermion_op = _to_summed_fermion_op(mo_1e_einsum) + _to_summed_fermion_op(
        mo_2e_einsum
    )
    return HamiltonianProblem(
        mapping=molecule_problem.mapping,
        z2_symmetries=molecule_problem.z2_symmetries,
        hamiltonian=fermion_op,
        num_particles=_get_num_particles(molecule),
    )


def _truncate(array: np.ndarray, threshold: float) -> np.ndarray:
    return np.where(np.abs(array) > threshold, array, 0.0)


def _to_fermion_op(array_coords: Tuple[int, ...]) -> FermionicOperator:
    if len(array_coords) == 2:
        return FermionicOperator(
            op_list=[("+", array_coords[0]), ("-", array_coords[1])]
        )

    elif len(array_coords) == 4:
        return FermionicOperator(
            op_list=[
                ("+", array_coords[0]),
                ("+", array_coords[2]),
                ("-", array_coords[3]),
                ("-", array_coords[1]),
            ]
        )

    else:
        raise ValueError("array must be 2 or 4 dimensional")


def _to_summed_fermion_op(array: np.ndarray) -> SummedFermionicOperator:
    array = _to_spin_array(array)
    return SummedFermionicOperator(
        op_list=[
            (_to_fermion_op(coords), float(element))
            for coords, element in np.ndenumerate(array)
            if element != 0
        ]
    )


def _to_spin_array(array: np.ndarray) -> np.ndarray:
    if len(array.shape) == 2:
        return np.kron(np.eye(2), array)

    elif len(array.shape) == 4:
        # chemical representation to physical representation
        array = np.einsum("ijkl->ljik", array)
        kron = np.zeros((2, 2, 2, 2))
        kron[(0, 0, 0, 0)] = 1
        kron[(0, 1, 1, 0)] = 1
        kron[(1, 1, 1, 1)] = 1
        kron[(1, 0, 0, 1)] = 1
        return -0.5 * np.kron(kron, array)

    else:
        raise ValueError("array must be 2 or 4 dimensional")


def _get_num_particles(molecule: Mole) -> Tuple[int, int]:
    return molecule.nelec[0], molecule.nelec[1]


def _to_pyscf_molecule(molecule_problem: MoleculeProblem) -> Mole:
    molecule = Mole()
    molecule.atom = molecule_problem.molecule.atoms
    molecule.basis = molecule_problem.basis
    molecule.build()
    return molecule
