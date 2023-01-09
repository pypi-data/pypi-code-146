from __future__ import annotations

import logging
import numpy as np
from .data import AlgebraicModule, ModuleFunction
from dataclasses import dataclass, field
from queue import Empty, SimpleQueue
from typing import Iterable, Iterator, Optional, cast
from ..types import Array

logger = logging.getLogger(__name__)


@dataclass
class AlgebraicModuleContainer:
    modules: dict[str, AlgebraicModule] = field(default_factory=dict)
    module_order: list[str] = field(default_factory=list)

    def __iter__(self) -> Iterator[AlgebraicModule]:
        return iter(self.modules.values())

    def _sort_algebraic_modules(self, available_args: set[str], max_iterations: int = 10_000) -> None:
        module_order = []
        modules_to_sort: SimpleQueue[tuple[str, AlgebraicModule]] = SimpleQueue()
        for k, v in self.modules.items():
            modules_to_sort.put((k, v))

        last_name = None
        i = 0
        while True:
            try:
                name, mod = modules_to_sort.get_nowait()
            except Empty:
                break
            if set(mod.args).issubset(available_args):
                available_args.update(mod.derived_variables)
                module_order.append(name)
            else:
                if last_name == name:
                    module_order.append(name)
                    break
                modules_to_sort.put((name, mod))
                last_name = name
            i += 1
            if i > max_iterations:
                raise ValueError(
                    "Exceeded max iterations on algebraic module sorting. Check if there are circular references."
                )
        self.module_order = module_order

    def get_derived_variables(self) -> list[str]:
        return [variable for module in self.modules.values() for variable in module.derived_variables]

    def add(
        self,
        module: AlgebraicModule,
        available_args: set[str],
        sort_modules: bool,
    ) -> None:
        if (name := module.name) in self.modules:
            raise KeyError(f"Module {name} already exists.")
        logger.info(f"Adding algebraic module {name}")
        self.modules[name] = module
        if sort_modules:
            self._sort_algebraic_modules(available_args)

    def update(
        self,
        name: str,
        function: Optional[ModuleFunction],
        derived_variables: Optional[list[str]],
        args: Optional[list[str]],
        available_args: set[str],
    ) -> None:
        module = self.remove(name, available_args, sort_modules=False)
        if function is not None:
            module.function = function
        if derived_variables is not None:
            module.derived_variables = derived_variables
        if args is not None:
            module.args = args
        self.add(module, available_args, sort_modules=True)

    def remove(
        self,
        name: str,
        available_args: set[str],
        sort_modules: bool,
    ) -> AlgebraicModule:
        logger.info(f"Removing algebraic module {name}")
        module = self.modules.pop(name)
        if sort_modules:
            self._sort_algebraic_modules(available_args)
        return module

    ##########################################################################
    # Simulation functions
    ##########################################################################

    def get_values_float(self, args: dict[str, float]) -> dict[str, float]:
        derived_variables: dict[str, float] = {}
        for name in self.module_order:
            module = self.modules[name]
            _values = module.function(*(args[arg] for arg in module.args))
            values = dict(zip(module.derived_variables, _values))
            derived_variables |= values
            args |= values
        return derived_variables

    def get_values_array(
        self,
        args: dict[str, Array],
    ) -> dict[str, Array]:
        derived_variables: dict[str, Array] = {}
        for name in self.module_order:
            module = self.modules[name]
            # values = np.array(module.function(*(args[arg] for arg in module.args)), dtype=float)
            # values = values.reshape((len(module.derived_variables), -1))
            _values = cast(Iterable[Array], module.function(*(args[arg] for arg in module.args)))
            values = dict(zip(module.derived_variables, _values))
            derived_variables |= values
            args |= values
        return derived_variables
