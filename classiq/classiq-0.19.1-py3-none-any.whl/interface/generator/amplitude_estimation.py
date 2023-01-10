from typing import TYPE_CHECKING, List, Union

import pydantic

from classiq.interface.generator import function_params
from classiq.interface.generator.arith.register_user_input import RegisterUserInput

if TYPE_CHECKING:
    PydanticNonEmptyNonNegativeIntList = List[int]
else:
    PydanticNonEmptyNonNegativeIntList = pydantic.conlist(
        pydantic.conint(ge=0), min_items=1
    )


OUTPUT_NAME: str = "OUT"
EXTRA_QUBITS_NAME: str = "EXTRA"
ZERO_INPUT_NAME: str = "ZERO_INPUTS"

NUM_EXTRA_QUBITS_ERROR: str = "AmplitudeEstimation attribute num_extra_qubits does not match actual QASM circuit size"


class AmplitudeEstimation(function_params.FunctionParams):
    """
    Creates a quantum circuit for ampitude estimation
    Provide the state preparation with a qasm string
    """

    state_preparation: str = pydantic.Field(
        description='The state preparation circuit in qasm format. Replace "..." with '
        "'...'. The total number of qubits is the sum of the state preparation qubits "
        "and `num_eval_qubits`"
    )

    num_extra_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits used in the state preparation circuit."
    )

    objective_qubits: Union[
        PydanticNonEmptyNonNegativeIntList, pydantic.NonNegativeInt
    ] = pydantic.Field(
        default=0,
        description='The list of "good" qubits. The good states are the ones that have '
        "1's in the positions defined by objective qubits. The indices in this list "
        "must be in the range defined by `state_preparation`",
    )

    num_eval_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits to evaluate on the amplitude estimation. "
        "More evaluation qubits provide a better estimate of the good states' amplitude"
    )

    def _create_ios(self) -> None:
        self._inputs = dict()
        self._outputs = {
            OUTPUT_NAME: RegisterUserInput(name=OUTPUT_NAME, size=self.num_eval_qubits),
            EXTRA_QUBITS_NAME: RegisterUserInput(
                name=EXTRA_QUBITS_NAME,
                size=self.num_extra_qubits,
            ),
        }

    @pydantic.validator("state_preparation")
    def vscode_qasm2circuit(cls, v):
        vscode_quote = "'"
        qasm_quotes = '"'
        return v.replace(vscode_quote, qasm_quotes)
