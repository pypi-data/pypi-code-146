from __future__ import annotations

import logging
import numpy as np
import pandas as pd
from .data import DerivedStoichiometry, RateFunction, Reaction, StoichiometryByVariable
from dataclasses import dataclass, field
from typing import Optional
from ..types import Array

logger = logging.getLogger()


@dataclass
class ReactionContainer:
    reactions: dict[str, Reaction] = field(default_factory=dict)
    stoichiometries_by_variables: dict[str, StoichiometryByVariable] = field(default_factory=dict)

    def set_stoichiometry(self, variable: str, reaction: str, factor: float) -> None:
        self.stoichiometries_by_variables.setdefault(variable, {})[reaction] = factor

    def update_stoichiometry(self, name: str, reaction: Reaction) -> None:
        for variable, factor in reaction.stoichiometry.items():
            self.set_stoichiometry(variable, name, factor)

    def update_derived_stoichiometry(self, name: str, reaction: Reaction, constants: dict[str, float]) -> None:
        for variable, derived_stoich in reaction.derived_stoichiometry.items():
            factor = derived_stoich.function(*(constants[i] for i in derived_stoich.args))
            self.set_stoichiometry(variable, name, factor)

    def update_derived_stoichiometries(self, constants: dict[str, float]) -> None:
        for name, reaction in self.reactions.items():
            self.update_derived_stoichiometry(name, reaction, constants)

    def add(self, reaction: Reaction, constants: dict[str, float]) -> None:
        if (name := reaction.name) in self.reactions:
            raise KeyError(f"Reaction {name} already exists in the model.")
        self.reactions[name] = reaction
        self.update_stoichiometry(name, reaction)
        self.update_derived_stoichiometry(name, reaction, constants)

    def remove(self, name: str) -> Reaction:
        reaction = self.reactions.pop(name)
        for variable in reaction.stoichiometry:
            del self.stoichiometries_by_variables[variable][name]
            if not bool(self.stoichiometries_by_variables[variable]):
                del self.stoichiometries_by_variables[variable]

        return reaction

    def update(
        self,
        name: str,
        function: Optional[RateFunction],
        stoichiometry: Optional[StoichiometryByVariable],
        # derived_stoichiometry: Optional[DerivedStoichiometry],
        derived_stoichiometry: Optional[dict[str, DerivedStoichiometry]],
        args: Optional[list[str]],
        constants: dict[str, float],
    ) -> None:
        reaction = self.remove(name)
        if function is not None:
            reaction.function = function
        if stoichiometry is not None:
            reaction.stoichiometry = stoichiometry
        if derived_stoichiometry is not None:
            reaction.derived_stoichiometry = derived_stoichiometry
        if args is not None:
            reaction.args = args
        self.add(reaction, constants)

    def get_names(self) -> list[str]:
        return list(self.reactions)

    def get_stoichiometries(self) -> pd.DataFrame:
        reactions = self.reactions
        variables = self.stoichiometries_by_variables
        variable_indexes = {v: k for k, v in enumerate(variables)}
        reaction_indexes = {v: k for k, v in enumerate(reactions)}

        data = np.zeros(shape=[len(variables), len(reactions)])
        for cpd, stoich in variables.items():
            for reaction, factor in stoich.items():
                data[variable_indexes[cpd], reaction_indexes[reaction]] = factor
        # for stoich_idx, reaction in enumerate(reactions.values()):
        #     for cpd, stoich in reaction.stoichiometry.items():
        #         data[variable_indexes[cpd], stoich_idx] = stoich
        return pd.DataFrame(
            data=data,
            index=variables,
            columns=reactions,
        )

    def get_fluxes_float(self, args: dict[str, float]) -> dict[str, float]:
        fluxes = {}
        for name, reaction in self.reactions.items():
            fluxes[name] = reaction.function(*(args[arg] for arg in reaction.args))
        return fluxes

    def get_fluxes_array(self, args: dict[str, Array]) -> dict[str, Array]:
        fluxes = np.full((len(self.reactions), len(args["time"])), np.nan, dtype=float)
        for i, reaction in enumerate(self.reactions.values()):
            fluxes[i, :] = reaction.function(*(args[arg] for arg in reaction.args))
        return dict(zip(self.reactions.keys(), fluxes))

    def get_right_hand_side_float(self, fluxes: dict[str, float]) -> dict[str, float]:
        rhs: dict[str, float] = {}
        for cpd, stoichiometry in self.stoichiometries_by_variables.items():
            for rate, factor in stoichiometry.items():
                rhs[cpd] = rhs.get(cpd, 0) + factor * fluxes[rate]
        return rhs
