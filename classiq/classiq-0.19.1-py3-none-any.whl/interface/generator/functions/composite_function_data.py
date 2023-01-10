from typing import Dict, List, Set

import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_call import FunctionCall, WireDict, WireName
from classiq.interface.generator.function_params import ArithmeticIODict, IOName
from classiq.interface.generator.functions.function_data import FunctionData


class IOData(pydantic.BaseModel):
    wire: WireName = pydantic.Field(description="The name of the wire of the IO data.")

    reg: RegisterUserInput = pydantic.Field(
        description="The register information about the IO data."
    )


class CompositeFunctionData(FunctionData, extra=pydantic.Extra.forbid):
    """
    Facilitates the creation of a user-defined composite function

    This class sets extra to forbid so that it can be used in a Union and not "steal"
    objects from other classes.
    """

    logic_flow: List[FunctionCall] = pydantic.Field(
        default=list(), description="List of function calls to perform."
    )
    custom_inputs: Dict[IOName, IOData] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the input name to the register information",
    )
    custom_outputs: Dict[IOName, IOData] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the output name to the register information",
    )

    @pydantic.validator("logic_flow")
    def validate_logic_flow_call_names(cls, logic_flow) -> List[FunctionCall]:
        function_call_names = {call.name for call in logic_flow}
        if len(function_call_names) != len(logic_flow):
            raise ValueError("Cannot have two function calls with the same name")

        return logic_flow

    @property
    def inputs_to_wires(self) -> WireDict:
        return {name: io_data.wire for name, io_data in self.custom_inputs.items()}

    @property
    def outputs_to_wires(self) -> WireDict:
        return {name: io_data.wire for name, io_data in self.custom_outputs.items()}

    @property
    def inputs(self) -> ArithmeticIODict:
        return {name: io_data.reg for name, io_data in self.custom_inputs.items()}

    @property
    def outputs(self) -> ArithmeticIODict:
        return {name: io_data.reg for name, io_data in self.custom_outputs.items()}

    @property
    def input_set(self) -> Set[IOName]:
        return set(self.inputs_to_wires.keys())

    @property
    def output_set(self) -> Set[IOName]:
        return set(self.outputs_to_wires.keys())
