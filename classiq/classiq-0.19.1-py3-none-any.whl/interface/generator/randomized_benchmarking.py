import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import FunctionParams

_DEFAULT_RB_NAME = "rb_reg"


class RandomizedBenchmarking(FunctionParams):
    num_of_qubits: pydantic.PositiveInt
    num_of_cliffords: pydantic.PositiveInt
    register_name: str = _DEFAULT_RB_NAME

    def _create_ios(self) -> None:
        self._inputs = {
            self.register_name: RegisterUserInput(
                name=self.register_name, size=self.num_of_qubits
            )
        }
        self._outputs = {**self._inputs}
