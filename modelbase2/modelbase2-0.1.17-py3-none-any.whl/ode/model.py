from __future__ import annotations

import numpy as np
import pandas as pd
from ..core import (
    AlgebraicModule,
    AlgebraicModuleContainer,
    Constant,
    ConstantContainer,
    DerivedConstant,
    NameContainer,
    Reaction,
    ReactionContainer,
    Variable,
    VariableContainer,
)
from ..core.data import (
    DerivedStoichiometry,
    ModuleFunction,
    RateFunction,
    StoichiometryByReaction,
    StoichiometryByVariable,
)
from ..types import Array, Series
from dataclasses import dataclass, field
from functools import singledispatchmethod
from modelbase.ode import Model as OldModel
from typing import Iterable, Literal, Optional, Union, overload


def _sort_derived_compounds(m: Model, max_iterations: int = 10_000) -> list[str]:
    from queue import Empty, SimpleQueue

    available = set(m.constants)
    order = []
    to_sort: SimpleQueue = SimpleQueue()
    for v in m.derived_constants.values():
        to_sort.put((v.name, set(v.args)))

    last_name: str | None = None
    i = 0
    while True:
        try:
            name, args = to_sort.get_nowait()
        except Empty:
            break
        if args.issubset(available):
            available.add(name)
            order.append(name)
        else:
            if last_name == name:
                order.append(name)
                break
            to_sort.put((name, args))
            last_name = name
        i += 1
        if i > max_iterations:
            while True:
                try:
                    name, args = to_sort.get_nowait()
                    print(name, args)
                except Empty:
                    break

            raise ValueError("Exceeded max iterations on sorting. Check if there are circular references.")
    return order


@dataclass
class Model:
    _algebraic_modules: AlgebraicModuleContainer = field(default_factory=AlgebraicModuleContainer)
    _variables: VariableContainer = field(default_factory=VariableContainer)
    _constants: ConstantContainer = field(default_factory=ConstantContainer)
    _reactions: ReactionContainer = field(default_factory=ReactionContainer)
    _names: NameContainer = field(default_factory=NameContainer)

    def __add__(self, other: "Model") -> "Model":
        for name, variable in other.variables.items():
            if name in self.variables:
                continue
            else:
                self.add_variable(variable)

        for name, constant in other.constants.items():
            if name in self.constants:
                self.update_constant(name, constant.value)
            else:
                self.add_constant(constant)

        # for name, derived_constant in other.derived_constants.items():
        for name in other._constants._derived_constant_order:
            derived_constant = other.derived_constants[name]
            if name in self.derived_constants:
                self.update_derived_constant(
                    name,
                    derived_constant.function,
                    derived_constant.args,
                    derived_constant.unit,
                )
            else:
                self.add_derived_constant(derived_constant)

        # for name, module in other.algebraic_modules.items():
        for name in other._algebraic_modules.module_order:
            module = other.algebraic_modules[name]
            if name in self.algebraic_modules:
                self.update_algebraic_module(
                    name,
                    module.function,
                    module.derived_variables,
                    module.args,
                )
            else:
                self.add_algebraic_module(module)

        for name, reaction in other.reactions.items():
            if reaction.name in self.reactions:
                self.update_reaction(
                    reaction.name,
                    reaction.function,
                    reaction.stoichiometry,
                    reaction.derived_stoichiometry,
                    reaction.args,
                )
            else:
                self.add_reaction(
                    Reaction(
                        name=reaction.name,
                        function=reaction.function,
                        stoichiometry=reaction.stoichiometry,
                        derived_stoichiometry=reaction.derived_stoichiometry,
                        args=reaction.args,
                    )
                )

        return self

    @property
    def constants(self) -> dict[str, Constant]:
        return self._constants.constants

    @property
    def derived_constants(self) -> dict[str, DerivedConstant]:
        return self._constants.derived_constants

    @property
    def constant_values(self) -> dict[str, float]:
        return self._constants.values

    @property
    def variables(self) -> dict[str, Variable]:
        return self._variables.variables

    @property
    def derived_variables(self) -> list[str]:
        return self._algebraic_modules.get_derived_variables()

    @property
    def all_variables(self) -> list[str]:
        return list(self.variables) + self.derived_variables

    @property
    def algebraic_modules(self) -> dict[str, AlgebraicModule]:
        return self._algebraic_modules.modules

    @property
    def reactions(self) -> dict[str, Reaction]:
        return self._reactions.reactions

    @property
    def stoichiometries(self) -> dict[str, StoichiometryByVariable]:
        return self._reactions.stoichiometries_by_variables

    @singledispatchmethod
    def add(
        self,
        element: Union[list, Constant, DerivedConstant, Variable, AlgebraicModule],
    ) -> None:
        raise NotImplementedError(element.__class__.__name__)

    @add.register
    def _add_iterable(self, elements: list) -> None:
        for element in elements:
            self.add(element)

    ##########################################################################
    # Constants
    ##########################################################################

    @add.register
    def add_constant(self, constant: Constant) -> None:
        self._names.add(constant.name, "constant")
        self._constants.add_basic(constant)

    def scale_constant(self, name: str, factor: float) -> None:
        value = self.constant_values[name]
        self.update_constant(name, value * factor)

    def update_constant(self, name: str, value: float) -> None:
        self._constants.update_basic(name, value)
        self._reactions.update_derived_stoichiometries(self.constant_values)

    def update_constants(self, constants: dict[str, float]) -> None:
        for name, value in constants.items():
            self.update_constant(name, value)

    def remove_constant(self, name: str) -> None:
        self._names.remove(name)
        self._constants.remove_basic(name)

    def remove_constants(self, names: Iterable[str]) -> None:
        for name in names:
            self.remove_constant(name)

    ##########################################################################
    # Derived Constants
    ##########################################################################

    @add.register
    def add_derived_constant(self, constant: DerivedConstant) -> None:
        self._names.require_multiple(constant.args)
        self._names.add(constant.name, "derived_constant")
        self._constants.add_derived(constant)

    def update_derived_constant(
        self,
        name: str,
        function: Optional[RateFunction] = None,
        args: Optional[Iterable[str]] = None,
        unit: Optional[str] = None,
    ) -> None:
        old = self.remove_derived_constant(name)
        if function is None:
            function = old.function
        if args is None:
            args = old.args
        if unit is None:
            unit = old.unit
        self.add_derived_constant(DerivedConstant(name, function, list(args), unit))
        self._reactions.update_derived_stoichiometries(self.constant_values)

    def remove_derived_constant(self, name: str) -> DerivedConstant:
        self._names.remove(name)
        return self._constants.remove_derived(name)

    def remove_derived_constants(self, names: Iterable[str]) -> None:
        for name in names:
            self.remove_derived_constant(name)

    ##########################################################################
    # Variables
    ##########################################################################

    @add.register
    def add_variable(self, variable: Variable) -> None:
        self._names.add(variable.name, "variable")
        self._variables.add(variable)

    def remove_variable(self, name: str) -> None:
        self._names.remove(name)
        self._variables.remove(name)

    def remove_variables(self, names: Iterable[str]) -> None:
        for name in names:
            self.remove_variable(name)

    ##########################################################################
    # Algebraic Modules
    ##########################################################################

    def _get_available_args(self) -> set[str]:
        return set(self.all_variables) | set(self._constants.values)

    @add.register
    def add_algebraic_module(self, module: AlgebraicModule) -> None:
        for name in module.derived_variables:
            self._names.add(name, "derived_variable")
        self._names.require_multiple(module.args)
        self._algebraic_modules.add(
            module,
            self._get_available_args(),
            sort_modules=True,
        )

    def remove_algebraic_module(self, name: str) -> AlgebraicModule:
        module = self._algebraic_modules.remove(
            name,
            set(),
            sort_modules=False,
        )
        for name in module.derived_variables:
            self._names.remove(name)
        return module

    def remove_algebraic_modules(self, names: Iterable[str]) -> None:
        for name in names:
            self.remove_algebraic_module(name)

    def update_algebraic_module(
        self,
        name: str,
        function: Optional[ModuleFunction] = None,
        derived_variables: Optional[list[str]] = None,
        args: Optional[list[str]] = None,
    ) -> None:
        old_module = self.remove_algebraic_module(name)
        if function is None:
            function = old_module.function
        if derived_variables is None:
            derived_variables = old_module.derived_variables
        if args is None:
            args = old_module.args
        self.add_algebraic_module(AlgebraicModule(name, function, derived_variables, args))

        self._algebraic_modules.update(
            name,
            function,
            derived_variables,
            args,
            self._get_available_args(),
        )

    ##########################################################################
    # Reactions
    ##########################################################################

    @add.register
    def add_reaction(
        self,
        reaction: Reaction,
    ) -> None:
        self._names.require_multiple(reaction.args)
        self._reactions.add(reaction, self.constant_values)

    def remove_reaction(self, name: str) -> None:
        self._reactions.remove(name=name)

    def remove_reactions(self, names: Iterable[str]) -> None:
        for name in names:
            self.remove_reaction(name=name)

    def update_reaction(
        self,
        name: str,
        function: Optional[RateFunction] = None,
        stoichiometry: Optional[StoichiometryByReaction] = None,
        # derived_stoichiometry: Optional[DerivedStoichiometry] = None,
        derived_stoichiometry: Optional[dict[str, DerivedStoichiometry]] = None,
        args: list[str] | None = None,
    ) -> None:
        self._reactions.update(
            name,
            function,
            stoichiometry,
            derived_stoichiometry,
            args,
            self.constant_values,
        )

    def get_stoichiometries(self) -> pd.DataFrame:
        return self._reactions.get_stoichiometries()

    # ##########################################################################
    # # Simulation functions
    # ##########################################################################

    def _get_problem(self, t: float, y: Iterable[float]) -> list[float]:
        """Integration function"""
        variables = dict(zip(self.stoichiometries, y)) | {"time": t}
        args = variables | self.constant_values
        args |= self._algebraic_modules.get_values_float(args)
        fluxes = self._reactions.get_fluxes_float(args)
        rhs = self._reactions.get_right_hand_side_float(fluxes)
        return list(rhs.values())

    def _get_all_args(self, variables: dict[str, float], time: float) -> dict[str, float]:
        args = variables | self.constant_values | {"time": time}
        args |= self._algebraic_modules.get_values_float(args)
        return args

    def get_derived_variables(self, variables: dict[str, float], time: float = 0.0) -> dict[str, float]:
        args = variables | self.constant_values | {"time": time}
        return self._algebraic_modules.get_values_float(args)

    @overload
    def get_fluxes(
        self,
        variables: dict[str, float],
        return_type: Literal["dict"],
        time: float = 0,
    ) -> dict[str, float]:
        ...

    @overload
    def get_fluxes(
        self,
        variables: dict[str, float],
        return_type: Literal["array"],
        time: float = 0,
    ) -> Array:
        ...

    @overload
    def get_fluxes(
        self,
        variables: dict[str, float],
        return_type: Literal["series"],
        time: float = 0,
    ) -> Series:
        ...

    @overload
    def get_fluxes(
        self,
        variables: dict[str, float],
        return_type: Literal["dict"] = "dict",
        time: float = 0,
    ) -> dict[str, float]:
        ...

    def get_fluxes(
        self,
        variables: dict[str, float],
        return_type: Literal["array", "dict", "series"] = "dict",
        time: float = 0.0,
    ) -> Union[Array, dict[str, float], pd.Series]:
        args = self._get_all_args(variables, time)
        fluxes_dict = self._reactions.get_fluxes_float(args)
        if return_type == "dict":
            return fluxes_dict
        elif return_type == "series":
            return pd.Series(fluxes_dict)
        elif return_type == "array":
            return np.fromiter(fluxes_dict.values(), dtype="float")
        else:
            raise NotImplementedError(f"Unknown return type {return_type}")

    def get_right_hand_side(self, variables: dict[str, float], time: float = 0.0) -> dict[str, float]:
        fluxes = self.get_fluxes(variables, time=time)
        return self._reactions.get_right_hand_side_float(fluxes)

    def to_version_1(self) -> OldModel:
        old = OldModel()

        old.add_compounds(list(self.variables))

        old.add_parameters({k: v.value for k, v in self.constants.items()})

        for k in _sort_derived_compounds(self):
            dc = self.derived_constants[k]
            old.add_derived_parameter(k, dc.function, dc.args)

        for k, am in self.algebraic_modules.items():
            old.add_algebraic_module_from_args(k, am.function, am.derived_variables, am.args)

        for r in self.reactions.values():
            old.add_reaction_from_args(r.name, r.function, r.stoichiometry, r.args)
        return old
