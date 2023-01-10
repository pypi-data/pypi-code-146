from typing import Any, Dict, Hashable, List, Optional

import pydantic

import classiq.interface.generator.validations.flow_graph as flow_graph
from classiq.interface.generator.function_call import FunctionCall
from classiq.interface.generator.functions import (
    CompositeFunctionData,
    FunctionLibraryData,
)
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.generator.user_defined_function_params import CustomFunction
from classiq.interface.helpers.versioned_model import VersionedModel

LOGIC_FLOW_DUPLICATE_NAME_ERROR_MSG = (
    "Cannot have multiple function calls with the same name"
)

LOGIC_FLOW_DUPLICATE_ID_ERROR_MSG = (
    "Cannot have multiple function calls with the same call ID"
)


def _is_list_unique(lst: List[Hashable]) -> bool:
    return len(set(lst)) == len(lst)


class Model(VersionedModel):
    """
    All the relevant data for generating quantum circuit in one place.
    """

    # Must be validated before logic_flow
    function_library: Optional[FunctionLibraryData] = pydantic.Field(
        default=None,
        description="The user-defined custom function library.",
    )

    inputs: Dict[str, str] = pydantic.Field(
        default_factory=dict,
        description="A mapping between the name of an input and the name of the wire "
        "that connects to this input",
    )
    outputs: Dict[str, str] = pydantic.Field(
        default_factory=dict,
        description="A mapping between the name of an output and the name of the wire "
        "that connects to this output",
    )
    logic_flow: List[FunctionCall] = pydantic.Field(
        default_factory=list,
        description="List of function calls to be applied in the circuit",
    )

    constraints: Constraints = pydantic.Field(default_factory=Constraints)
    preferences: Preferences = pydantic.Field(default_factory=Preferences)

    @pydantic.validator("logic_flow")
    def validate_logic_flow(
        cls, logic_flow: List[FunctionCall], values: Dict[str, Any]
    ) -> List[FunctionCall]:
        if not logic_flow:
            return logic_flow

        if not _is_list_unique([call.name for call in logic_flow]):
            raise ValueError(LOGIC_FLOW_DUPLICATE_NAME_ERROR_MSG)

        if not _is_list_unique([call.id for call in logic_flow]):
            raise ValueError(LOGIC_FLOW_DUPLICATE_ID_ERROR_MSG)

        functions_to_validate = logic_flow.copy()
        library = values.get("function_library")

        while functions_to_validate:
            function_call = functions_to_validate.pop()
            params = function_call.function_params

            if not isinstance(params, CustomFunction):
                continue

            if isinstance(params, CustomFunction) and library and params not in library:
                raise ValueError("The function is not found in included library.")

            assert isinstance(library, FunctionLibraryData)
            function_data = library.function_dict[params.name]
            params.generate_ios(
                inputs=function_data.inputs,
                outputs=function_data.outputs,
            )
            function_call.validate_custom_function_io()
            if isinstance(function_data, CompositeFunctionData):
                functions_to_validate.extend(function_data.logic_flow)

        inputs: Dict[str, str] = values.get("inputs", dict())
        outputs: Dict[str, str] = values.get("outputs", dict())

        flow_graph.validate_legal_wiring(
            logic_flow,
            flow_input_names=list(inputs.values()),
            flow_output_names=list(outputs.values()),
        )
        flow_graph.validate_acyclic_logic_flow(
            logic_flow,
            flow_input_names=list(inputs.values()),
            flow_output_names=list(outputs.values()),
        )

        return logic_flow
