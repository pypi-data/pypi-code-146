from typing import List

from classiq.interface.chemistry import ground_state_problem
from classiq.interface.chemistry.ground_state_problem import (
    CHEMISTRY_PROBLEMS_TYPE,
    GroundStateProblemAndExcitations,
    HamiltonianProblem,
)
from classiq.interface.chemistry.operator import PauliOperator
from classiq.interface.generator.excitations import EXCITATIONS_TYPE

from classiq._internals import async_utils
from classiq._internals.api_wrapper import ApiWrapper


async def generate_hamiltonian_async(
    problem: CHEMISTRY_PROBLEMS_TYPE,
) -> PauliOperator:
    hamiltonian = await ApiWrapper.call_generate_hamiltonian_task(problem)

    problem.num_qubits = hamiltonian.num_qubits

    return hamiltonian


ground_state_problem.GroundStateProblem.generate_hamiltonian = async_utils.syncify_function(generate_hamiltonian_async)  # type: ignore[attr-defined]
ground_state_problem.GroundStateProblem.generate_hamiltonian_async = generate_hamiltonian_async  # type: ignore[attr-defined]


async def generate_ucc_operators_async(
    problem: CHEMISTRY_PROBLEMS_TYPE,
    excitations: EXCITATIONS_TYPE,
) -> List[PauliOperator]:
    problem_and_excitations = GroundStateProblemAndExcitations(
        problem=problem, excitations=excitations
    )
    pauli_operators = await ApiWrapper.call_generate_ucc_operators_task(
        problem=problem_and_excitations
    )
    return pauli_operators.operators


ground_state_problem.GroundStateProblem.generate_ucc_operators = async_utils.syncify_function(generate_ucc_operators_async)  # type: ignore[attr-defined]
ground_state_problem.GroundStateProblem.generate_ucc_operators_async = generate_ucc_operators_async  # type: ignore[attr-defined]


async def update_problem_async(
    problem: CHEMISTRY_PROBLEMS_TYPE,
) -> CHEMISTRY_PROBLEMS_TYPE:
    if isinstance(problem, HamiltonianProblem) and not problem.z2_symmetries:
        num_qubits = problem.hamiltonian.num_qubits

    else:
        hamiltonian = await generate_hamiltonian_async(problem)
        num_qubits = hamiltonian.num_qubits

    problem.num_qubits = num_qubits

    return problem


ground_state_problem.GroundStateProblem.update_problem = async_utils.syncify_function(  # type: ignore[attr-defined]
    update_problem_async
)
ground_state_problem.GroundStateProblem.update_problem_async = update_problem_async  # type: ignore[attr-defined]
