"""Executor module, implementing facilities for executing quantum programs using Classiq platform."""

import asyncio
import itertools
from typing import (
    Awaitable,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from typing_extensions import TypeAlias

from classiq.interface.backend.backend_preferences import BackendPreferencesTypes
from classiq.interface.executor import execution_request
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.executor.execution_request import (
    ExecutionRequest,
    QuantumProgramExecution,
)
from classiq.interface.executor.hamiltonian_minimization_problem import (
    HamiltonianMinimizationProblem,
)
from classiq.interface.executor.quantum_instruction_set import QuantumInstructionSet
from classiq.interface.executor.quantum_program import (
    Arguments,
    MultipleArguments,
    QuantumBaseProgram,
    QuantumProgram,
)
from classiq.interface.executor.result import (
    ExecutionDetails,
    FinanceSimulationResults,
    GroverSimulationResults,
    MultipleExecutionDetails,
)
from classiq.interface.executor.vqe_result import VQESolverResult
from classiq.interface.generator import finance, grover_operator, identity
from classiq.interface.generator.result import GeneratedCircuit

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import Asyncify, syncify_function
from classiq._internals.registers_initialization import InitialConditions
from classiq.exceptions import ClassiqExecutionError, ClassiqValueError

BatchExecutionResult: TypeAlias = Union[ExecutionDetails, BaseException]
ProgramAndResult: TypeAlias = Tuple[QuantumProgram, BatchExecutionResult]
BackendPreferencesProgramAndResult: TypeAlias = Tuple[
    BackendPreferencesTypes, QuantumProgram, BatchExecutionResult
]

QuantumProgramLike: TypeAlias = Union[
    GeneratedCircuit, QuantumProgram, QuantumBaseProgram, str
]
SpecialExecutionResult: TypeAlias = Union[
    FinanceSimulationResults, GroverSimulationResults
]
SpecialExecutionParams: TypeAlias = Union[
    grover_operator.GroverOperator, finance.Finance
]
SpecialExecutionCallMethod: TypeAlias = Callable[
    [ExecutionRequest], Awaitable[SpecialExecutionResult]
]


_SPECIAL_EXECUTION_METHODS: Dict[
    Type[SpecialExecutionParams], SpecialExecutionCallMethod
] = {
    grover_operator.GroverOperator: ApiWrapper.call_execute_grover,
    finance.Finance: ApiWrapper.call_execute_finance,
}


SINGLE_ARGUMENTS_ERROR_MESSAGE = "Arguments should be provided either as "
"positional arguments, keyword arguments or as a quantum_program. "
"Defining more than one option is not allowed."


class Executor(metaclass=Asyncify):
    """Executor is the entry point for executing quantum programs on multiple quantum hardware vendors."""

    def __init__(
        self, preferences: Optional[ExecutionPreferences] = None, **kwargs
    ) -> None:
        """Init self.

        Args:
            preferences (): Execution preferences, such as number of shots.
        """
        self._preferences = preferences or ExecutionPreferences(**kwargs)

    @property
    def preferences(self) -> ExecutionPreferences:
        return self._preferences

    @staticmethod
    def _combine_arguments(
        arguments_list: MultipleArguments,
        arguments_as_tuple: MultipleArguments,
        arguments_from_quantum_program: MultipleArguments,
        is_assert_multiple_definitions: bool = False,
    ) -> MultipleArguments:
        if (
            is_assert_multiple_definitions
            and sum(
                [
                    bool(arguments_list),
                    bool(arguments_as_tuple),
                    bool(arguments_from_quantum_program),
                ]
            )
            > 1
        ):
            raise ClassiqExecutionError(SINGLE_ARGUMENTS_ERROR_MESSAGE)

        return (
            arguments_list or arguments_as_tuple or arguments_from_quantum_program or ()
        )

    def _pre_process_quantum_program_request(
        self,
        quantum_program_like: QuantumProgramLike,
        *arguments_list: Arguments,
        arguments: MultipleArguments = (),
        initial_values: Optional[InitialConditions] = None,
    ) -> ExecutionRequest:
        quantum_program = _convert_to_quantum_program(
            quantum_program_like, initial_values
        )

        arguments_as_tuple = (
            (arguments,) if isinstance(arguments, dict) else arguments
        )  # backwards compatibility
        quantum_program.arguments = self._combine_arguments(
            arguments_list,
            arguments_as_tuple,
            quantum_program.arguments,
            is_assert_multiple_definitions=True,
        )

        return ExecutionRequest(
            preferences=self._preferences,
            execution_payload=quantum_program.dict(),
        )

    def _post_process_quantum_program_request(
        self,
        result: MultipleExecutionDetails,
        request: ExecutionRequest,
        arguments_list: MultipleArguments,
        arguments: MultipleArguments,
    ) -> Union[ExecutionDetails, MultipleExecutionDetails]:
        request.execution_payload = cast(
            QuantumProgramExecution, request.execution_payload
        )
        output_qubits_map = request.execution_payload.output_qubits_map
        for res in result.details:
            res.output_qubits_map = output_qubits_map

        if self._should_return_single_item(
            request.execution_payload, result, arguments_list, arguments
        ):
            return result[0]
        else:
            return result

    def _should_return_single_item(
        self,
        execution_payload: QuantumProgramExecution,
        result: MultipleExecutionDetails,
        arguments_list: MultipleArguments,
        arguments: MultipleArguments,
    ) -> bool:
        is_passed_as_single_arguments = (
            len(arguments_list) == 1 and not arguments
        ) or (isinstance(arguments, dict))

        is_no_arguments_at_all = not self._combine_arguments(
            arguments_list, arguments, execution_payload.arguments
        )

        should_return_single_item = len(result.details) == 1 and (
            is_no_arguments_at_all or is_passed_as_single_arguments
        )
        return should_return_single_item

    async def _execute_quantum_program_async(
        self,
        quantum_program_like: QuantumProgramLike,
        *arguments_list: Arguments,
        arguments: MultipleArguments = (),
        initial_values: Optional[InitialConditions] = None,
    ) -> Union[ExecutionDetails, MultipleExecutionDetails]:

        request = self._pre_process_quantum_program_request(
            quantum_program_like,
            *arguments_list,
            arguments=arguments,
            initial_values=initial_values,
        )

        result = await ApiWrapper.call_execute_quantum_program(request=request)

        return self._post_process_quantum_program_request(
            result,
            request,
            arguments_list,
            arguments,
        )

    async def _execute_amplitude_estimation_async(
        self,
        quantum_program_like: QuantumProgramLike,
    ) -> ExecutionDetails:
        quantum_base_program = _convert_to_quantum_base_program(quantum_program_like)

        request = ExecutionRequest(
            preferences=self._preferences,
            execution_payload=execution_request.AmplitudeEstimationExecution(
                **quantum_base_program.dict()
            ),
        )

        return await ApiWrapper.call_execute_amplitude_estimation(request=request)

    async def batch_execute_quantum_program_async(
        self, quantum_programs: Collection[QuantumProgram]
    ) -> List[ProgramAndResult]:
        results = await asyncio.gather(
            *map(self._execute_quantum_program_async, quantum_programs),
            return_exceptions=True,
        )
        return list(zip(quantum_programs, results))

    async def _execute_quantum_program_like(
        self, quantum_program_like: QuantumProgramLike, *args, **kwargs
    ) -> Union[ExecutionDetails, MultipleExecutionDetails]:
        if self._preferences.amplitude_estimation is not None:
            return await self._execute_amplitude_estimation_async(
                quantum_program_like, *args, **kwargs
            )
        return await self._execute_quantum_program_async(
            quantum_program_like, *args, **kwargs
        )

    @staticmethod
    def _extract_special_execution_params(
        generated_circuit: GeneratedCircuit,
    ) -> Optional[SpecialExecutionParams]:
        if not generated_circuit.model:
            return None
        non_identity_params = [
            call.function_params
            for call in generated_circuit.model.logic_flow
            if not isinstance(call.function_params, identity.Identity)
        ]
        if len(non_identity_params) != 1:
            return None
        params = non_identity_params[0]
        return params if type(params) in _SPECIAL_EXECUTION_METHODS else None  # type: ignore[return-value]

    async def _call_execute_with_special_params(
        self, generation_result: GeneratedCircuit, params: SpecialExecutionParams
    ) -> SpecialExecutionResult:
        payload = execution_request.GeneratedCircuitExecution(
            **generation_result.dict()
        )
        request = ExecutionRequest(
            preferences=self._preferences, execution_payload=payload
        )
        return await _SPECIAL_EXECUTION_METHODS[type(params)](request)

    async def _execute_generated_circuit_async(
        self, generation_result: GeneratedCircuit, *args, **kwargs
    ) -> Union[SpecialExecutionResult, ExecutionDetails, MultipleExecutionDetails]:
        special_params = self._extract_special_execution_params(generation_result)
        if special_params:
            return await self._call_execute_with_special_params(
                generation_result=generation_result, params=special_params
            )
        return await self._execute_quantum_program_like(
            generation_result, *args, **kwargs
        )

    async def _execute_hamiltonian_minimization_async(
        self,
        hamiltonian_minimization_problem: HamiltonianMinimizationProblem,
    ) -> VQESolverResult:
        payload = execution_request.HamiltonianMinimizationProblemExecution(
            **hamiltonian_minimization_problem.dict()
        )
        request = ExecutionRequest(
            preferences=self._preferences,
            execution_payload=payload,
        )
        return await ApiWrapper.call_execute_vqe(request=request)

    async def execute_async(
        self,
        execution_payload: Union[QuantumProgramLike, HamiltonianMinimizationProblem],
        *args,
        **kwargs,
    ) -> Union[
        VQESolverResult,
        SpecialExecutionResult,
        ExecutionDetails,
        MultipleExecutionDetails,
    ]:
        if isinstance(execution_payload, HamiltonianMinimizationProblem):
            return await self._execute_hamiltonian_minimization_async(
                execution_payload, *args, **kwargs
            )

        if isinstance(execution_payload, GeneratedCircuit):
            return await self._execute_generated_circuit_async(
                execution_payload, *args, **kwargs
            )

        return await self._execute_quantum_program_like(
            execution_payload, *args, **kwargs
        )


def _convert_to_quantum_program(
    arg: QuantumProgramLike,
    initial_values: Optional[InitialConditions] = None,
) -> QuantumProgram:
    if isinstance(arg, GeneratedCircuit):
        program = arg.to_program(initial_values)
    elif isinstance(arg, QuantumProgram):
        program = arg
    elif isinstance(arg, QuantumBaseProgram):
        program = QuantumProgram(**arg.dict())
    elif isinstance(arg, str):
        program = QuantumProgram(code=arg)
    else:
        raise ClassiqValueError("Invalid executor input")

    return program


def _convert_to_quantum_base_program(
    arg: QuantumProgramLike,
) -> QuantumBaseProgram:
    if isinstance(arg, GeneratedCircuit):
        code = arg.to_base_program()
    elif isinstance(arg, QuantumProgram):
        code = QuantumBaseProgram(code=arg.code, syntax=arg.syntax)
    elif isinstance(arg, QuantumBaseProgram):
        code = arg
    elif isinstance(arg, str):
        code = QuantumBaseProgram(code=arg)
    else:
        raise ClassiqValueError("Invalid executor input")

    return code


async def batch_execute_multiple_backends_async(
    preferences_template: ExecutionPreferences,
    backend_preferences: Sequence[BackendPreferencesTypes],
    quantum_programs: Collection[QuantumProgram],
) -> List[BackendPreferencesProgramAndResult]:
    """
    Execute all the provided quantum programs (n) on all the provided backends (m).
    In total, m * n executions.
    The return value is a list of the following tuples:

    - An element from `backend_preferences`
    - An element from `quantum_programs`
    - The execution result of the quantum program on the backend. If the execution failed,
      the value is an exception.

    The length of the list is m * n.

    The `preferences_template` argument is used to supplement all other preferences.

    The code is equivalent to:
    ```
    for backend in backend_preferences:
        for program in quantum_programs:
            preferences = preferences_template.copy()
            preferences.backend_preferences = backend
            Executor(preferences).execute(program)
    ```
    """
    executors = [
        Executor(
            preferences=preferences_template.copy(
                update={"backend_preferences": backend}
            )
        )
        for backend in backend_preferences
    ]
    results = await asyncio.gather(
        *(
            executor.batch_execute_quantum_program_async(quantum_programs)
            for executor in executors
        ),
        return_exceptions=True,
    )

    def map_return_value(
        executor: Executor,
        result: Union[List[ProgramAndResult], BaseException],
    ) -> Iterable[BackendPreferencesProgramAndResult]:
        nonlocal quantum_programs
        preferences = executor.preferences.backend_preferences
        if isinstance(result, BaseException):
            return ((preferences, program, result) for program in quantum_programs)
        else:
            return (
                (preferences, program, single_result)
                for program, single_result in result
            )

    return list(
        itertools.chain.from_iterable(
            map_return_value(executor, result)
            for executor, result in zip(executors, results)
        )
    )


batch_execute_multiple_backends = syncify_function(
    batch_execute_multiple_backends_async
)


__all__ = ["QuantumProgram", "QuantumInstructionSet", "batch_execute_multiple_backends"]
