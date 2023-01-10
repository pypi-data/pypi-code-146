from typing import Any, Dict, Optional

import pydantic

from classiq.interface.generator.arith.arithmetic import ArithmeticOracle
from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.generator.state_preparation import StatePreparation


class GroverOperator(FunctionParams):
    oracle: ArithmeticOracle
    state_preparation: StatePreparation = pydantic.Field(default=None)
    diffuser: Optional[str] = None

    def _create_ios(self) -> None:
        self._inputs = {**self.oracle.inputs}
        self._outputs = {**self.oracle.outputs}

    @pydantic.validator("state_preparation", always=True)
    def _validate_state_preparation(
        cls, state_preparation: Optional[StatePreparation], values: Dict[str, Any]
    ) -> StatePreparation:
        if state_preparation:
            return state_preparation
        oracle = values.get("oracle")
        if oracle is None:
            raise ValueError("Must receive an oracle")
        num_states = 2 ** oracle.num_input_qubits(assign_zero_ios=False)
        return StatePreparation(probabilities=[1.0 / float(num_states)] * num_states)
