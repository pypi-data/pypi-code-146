from abc import ABC
from typing import Tuple

from bitorch.layers import QLinearBase
from bitorch.layers.extensions import LayerRecipe
from bitorch.quantizations import Sign, SwishSign

from bitorch_engine.layers.qlinear.qlinear_implementation import QLinearImplementationMixin


class BinaryLinearImplementationMixin(QLinearImplementationMixin, ABC):
    @classmethod
    def can_clone(cls, recipe: LayerRecipe) -> Tuple[bool, str]:
        supported_quantization_functions = (Sign, SwishSign)
        args = QLinearBase.get_args_as_kwargs(recipe)
        if args["input_quantization"].__class__ not in supported_quantization_functions:
            return False, f"the input quantization {args['input_quantization'].name} is not yet supported."
        if args["weight_quantization"].__class__ not in supported_quantization_functions:
            return False, f"the weight quantization {args['weight_quantization'].name} is not yet supported."
        return super().can_clone(recipe)
