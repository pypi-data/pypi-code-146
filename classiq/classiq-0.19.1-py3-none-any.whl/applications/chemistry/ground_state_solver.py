from classiq.interface.chemistry import ground_state_solver
from classiq.interface.chemistry.ground_state_result import (
    CHEMISTRY_RESULTS_TYPE,
    MoleculeExactResult,
)
from classiq.interface.generator.model.preferences.preferences import QuantumFormat
from classiq.interface.generator.result import GeneratedCircuit

from classiq._internals import async_utils
from classiq._internals.api_wrapper import ApiWrapper


async def solve_async(
    gs_solver: ground_state_solver.GroundStateSolver,
) -> CHEMISTRY_RESULTS_TYPE:
    for attr in "ansatz", "optimizer_preferences", "backend_preferences":
        if getattr(gs_solver, attr, None) is None:
            raise ValueError(f"{attr} field must be specified")

    # when incorporating OPENQASM3, OPENQASM 3, OPENQASM 3.0, QASM 3.0, this might need updating
    valid_generated_circuit_format = isinstance(
        gs_solver.ansatz, GeneratedCircuit
    ) and (QuantumFormat.QASM in gs_solver.ansatz.output_format)
    valid_qasm = isinstance(gs_solver.ansatz, str) and (
        "openqasm" in gs_solver.ansatz.lower()
    )

    if (not valid_generated_circuit_format) and (not valid_qasm):
        raise ValueError(
            "unknown circuit format. Supported circuit formats are: openqasm"
        )

    return await ApiWrapper.call_ground_state_solve_task(problem=gs_solver)


async def solve_exact_async(
    gs_solver: ground_state_solver.GroundStateSolver,
) -> MoleculeExactResult:
    return await ApiWrapper.call_solve_exact_task(
        problem=gs_solver.ground_state_problem
    )


ground_state_solver.GroundStateSolver.solve = async_utils.syncify_function(  # type: ignore[attr-defined]
    solve_async
)
ground_state_solver.GroundStateSolver.solve_async = solve_async  # type: ignore[attr-defined]
ground_state_solver.GroundStateSolver.solve_exact = async_utils.syncify_function(solve_exact_async)  # type: ignore[attr-defined]
ground_state_solver.GroundStateSolver.solve_exact_async = solve_exact_async  # type: ignore[attr-defined]
