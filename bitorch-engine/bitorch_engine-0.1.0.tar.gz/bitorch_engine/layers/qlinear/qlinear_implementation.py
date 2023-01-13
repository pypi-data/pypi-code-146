from abc import ABC
from typing import Tuple

from bitorch.layers import CustomImplementationMixin, QLinearBase
from bitorch.layers.extensions import LayerRecipe


class QLinearImplementationMixin(CustomImplementationMixin, ABC):
    @classmethod
    def can_clone(cls, recipe: LayerRecipe) -> Tuple[bool, str]:
        args = QLinearBase.get_args_as_kwargs(recipe)
        if args["bias"]:
            return False, f"bias is not yet supported."
        if args["in_features"] % 32 != 0:
            return False, f"in_features ({args['in_features']}) is not divisible by 32."
        return True, ""
