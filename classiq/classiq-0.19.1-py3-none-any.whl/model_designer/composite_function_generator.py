from typing import List

from classiq.interface.generator.function_call import FunctionCall
from classiq.interface.generator.function_params import IO
from classiq.interface.generator.functions import CompositeFunctionData

from classiq.model_designer import function_handler


class CompositeFunctionGenerator(function_handler.FunctionHandler):
    def __init__(self, function_name: str) -> None:
        super().__init__()
        self._name = function_name
        self._logic_flow_list: List[FunctionCall] = list()

    @property
    def _logic_flow(self) -> List[FunctionCall]:
        return self._logic_flow_list

    def to_function_data(self) -> CompositeFunctionData:
        return CompositeFunctionData(
            name=self._name,
            logic_flow=self._logic_flow,
            custom_inputs=self._custom_ios[IO.Input],
            custom_outputs=self._custom_ios[IO.Output],
        )
