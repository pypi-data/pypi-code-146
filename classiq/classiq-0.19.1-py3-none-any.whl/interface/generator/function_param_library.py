from typing import Iterable, Set, Type

from classiq.interface.generator.function_params import FunctionParams


class FunctionParamLibrary:
    def __init__(self, param_list: Iterable[Type[FunctionParams]]) -> None:
        self._param_list: Set[Type[FunctionParams]] = set(param_list)

    @property
    def param_list(self) -> Set[Type[FunctionParams]]:
        return self._param_list.copy()

    # Private methods are for tests only
    def _add(self, param: Type[FunctionParams]) -> None:
        self._param_list.add(param)

    def _remove(self, param: Type[FunctionParams]) -> None:
        self._param_list.remove(param)
