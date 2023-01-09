from __future__ import annotations

from .data import Constant, DerivedConstant
from dataclasses import dataclass, field
from queue import Empty, SimpleQueue

# import logging
# logger = logging.getLogger(__name__)


@dataclass
class ConstantContainer:
    constants: dict[str, Constant] = field(default_factory=dict)
    derived_constants: dict[str, DerivedConstant] = field(default_factory=dict)
    _derived_from_constants: set[str] = field(default_factory=set)
    _derived_constant_order: list[str] = field(default_factory=list)
    values: dict[str, float] = field(default_factory=dict)

    ###############################################################################
    # Basic
    ###############################################################################

    def add_basic(self, constant: Constant, update_derived: bool = True) -> None:
        if (name := constant.name) in self.constants:
            raise KeyError(f"Constant {name} already exists in the model.")
        self.constants[name] = constant
        self.values[name] = constant.value
        # if name in self._derived_from_constants and update_derived:
        #     self._update_derived_constant_values()

    def remove_basic(self, name: str) -> None:
        del self.constants[name]
        del self.values[name]

    def update_basic(self, name: str, value: float, update_derived: bool = True) -> None:
        if name not in self.constants:
            raise KeyError(f"Constant {name} is not in the model. You have to add it first")
        self.constants[name].value = value
        self.values[name] = value
        if name in self._derived_from_constants and update_derived:
            self._update_derived_constant_values()

    ###############################################################################
    # Derived
    ###############################################################################

    def _sort_derived_constants(self, max_iterations: int = 10_000) -> None:
        available_args = set(self.constants)
        order = []
        to_sort: SimpleQueue[tuple[str, DerivedConstant]] = SimpleQueue()
        for k, v in self.derived_constants.items():
            to_sort.put((k, v))

        i = 0
        last_name = ""
        while True:
            try:
                name, constant = to_sort.get_nowait()
                # logger.warning(f"Trying {name}, which requires {constant.args}")
            except Empty:
                break
            if set(constant.args).issubset(available_args):
                # logger.warning(f"Sorting in {name}")
                available_args.add(name)
                order.append(name)
            elif name == last_name:
                raise ValueError(f"Missing args for {name}")
            else:
                # logger.warning(f"{name} doesn't fit yet, {set(constant.args).difference(available_args)} missing")
                to_sort.put((name, constant))
                last_name = name
            i += 1
            if i > max_iterations:
                raise ValueError(
                    f"Exceeded max iterations on derived constants sorting {name}. "
                    "Check if there are circular references."
                )
        self._derived_constant_order = order

    def _update_derived_constant_values(self) -> None:
        for name in self._derived_constant_order:
            derived_constant = self.derived_constants[name]
            value = derived_constant.function(*(self.values[i] for i in derived_constant.args))
            self.values[name] = value

    def add_derived(self, constant: DerivedConstant, update_derived: bool = True) -> None:
        name = constant.name
        self.derived_constants[name] = constant
        for arg in constant.args:
            self._derived_from_constants.add(arg)

        # Calculate initial value
        value = constant.function(*(self.values[i] for i in constant.args))
        self.values[name] = value
        self._sort_derived_constants()

        if name in self._derived_from_constants and update_derived:
            self._update_derived_constant_values()

    def remove_derived(self, name: str) -> DerivedConstant:
        """Remove a derived constant from the model."""
        old_constant = self.derived_constants.pop(name)
        derived_from = old_constant.args
        for i in derived_from:
            if all(i not in j.args for j in self.derived_constants.values()):
                self._derived_from_constants.remove(i)
        del self.values[name]
        self._derived_constant_order.remove(name)
        return old_constant
