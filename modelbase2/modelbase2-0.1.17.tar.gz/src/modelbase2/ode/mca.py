from __future__ import annotations

import copy
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ..types import Array, DataFrame, Series
from ..utils.plotting import get_norm as _get_norm
from ..utils.plotting import heatmap_from_dataframe as _heatmap_from_dataframe
from .integrator import Assimulo
from .model import Model
from .simulator import Simulator
from matplotlib import cm
from matplotlib.axes import Axes
from matplotlib.collections import QuadMesh
from matplotlib.figure import Figure
from typing import Optional, cast

_DISPLACEMENT = 1e-4
_DEFAULT_TOLERANCE = 1e-8


def get_variable_elasticity(
    m: Model,
    variable: str,
    y: dict[str, float],
    displacement: float = _DISPLACEMENT,
) -> Array:
    """Get sensitivity of all rates to a change of the concentration of a variable.

    Also called epsilon-elasticities. Not in steady state!
    """
    y_full = y | m.get_derived_variables(y)
    old_concentration = y_full[variable]
    fluxes: list[Array] = []
    for new_concentration in (
        old_concentration * (1 + displacement),
        old_concentration * (1 - displacement),
    ):
        y_full[variable] = new_concentration
        fluxes.append(m.get_fluxes(y_full, "array"))
    elasticity_coef = (fluxes[0] - fluxes[1]) / (2 * displacement * old_concentration)
    # normalise
    y_full[variable] = old_concentration
    flux_array = m.get_fluxes(y_full, "array")
    elasticity_coef *= old_concentration / flux_array
    return np.atleast_1d(np.squeeze(elasticity_coef))


def get_variable_elasticities(
    m: Model,
    variables: list[str],
    y: dict[str, float],
    displacement: float = _DISPLACEMENT,
) -> DataFrame:
    """Get sensitivity of all rates to a change of the concentration of multiple variables.

    Also called epsilon-elasticities. Not in steady state!
    """
    stoichiometries = m.get_stoichiometries().columns
    elasticities = np.full(shape=(len(variables), len(stoichiometries)), fill_value=np.nan)
    for i, variable in enumerate(variables):
        elasticities[i] = get_variable_elasticity(
            m=m,
            variable=variable,
            y=y,
            displacement=displacement,
        )
    return pd.DataFrame(elasticities, index=variables, columns=stoichiometries)


def get_constant_elasticity(
    m: Model,
    constant: str,
    y: dict[str, float],
    displacement: float = _DISPLACEMENT,
) -> Array:
    """Get sensitivity of all rates to a change of a constant value.

    Also called pi-elasticities. Not in steady state!
    """
    m = copy.deepcopy(m)
    old_value = m.constant_values[constant]
    fluxes = []
    for new_value in [old_value * (1 + displacement), old_value * (1 - displacement)]:
        m.update_constant(constant, new_value)
        fluxes.append(m.get_fluxes(y, "array"))
    elasticity_coef = (fluxes[0] - fluxes[1]) / (2 * displacement * old_value)
    # normalise
    m.update_constant(constant, old_value)
    fluxes_array = m.get_fluxes(y, "array")
    elasticity_coef *= old_value / fluxes_array
    return np.atleast_1d(np.squeeze(elasticity_coef))


def get_constant_elasticities(
    m: Model,
    constants: list[str],
    y: dict[str, float],
    displacement: float = _DISPLACEMENT,
) -> DataFrame:
    """Get sensitivity of all rates to a change of multiple constant values.

    Also called pi-elasticities. Not in steady state!
    """
    stoichiometries = m.get_stoichiometries().columns
    elasticities = np.full(shape=(len(constants), len(stoichiometries)), fill_value=np.nan)
    for i, constant in enumerate(constants):
        elasticities[i] = get_constant_elasticity(
            m=m,
            constant=constant,
            y=y,
            displacement=displacement,
        )
    return pd.DataFrame(elasticities, index=constants, columns=stoichiometries)


def _get_response_coefficients_single_constant(
    m: Model,
    constant: str,
    y0: dict[str, float],
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
) -> tuple[Optional[Series], Optional[Series]]:
    """Get response of the steady state concentrations and fluxes to a change of the given constant."""
    old_value = m.constant_values[constant]
    m = copy.deepcopy(m)

    # normalise
    y_ss = Simulator(m, Assimulo, y0).simulate_to_steady_state(tolerance=tolerance)
    if y_ss is None:
        return None, None
    y_full = y0 | m.get_derived_variables(y_ss)
    y_ss_norm = old_value / np.fromiter(y_full.values(), dtype="float")
    fluxes_norm = old_value / m.get_fluxes(y_full, return_type="array")

    # scan
    ss: list[Array] = []
    fluxes: list[Array] = []
    for new_value in [
        old_value * (1 + displacement),
        old_value * (1 - displacement),
    ]:
        m.update_constant(constant, new_value)
        y_ss = Simulator(m, Assimulo, y_ss).simulate_to_steady_state(tolerance=tolerance)
        if y_ss is None:
            return None, None
        y_full = y_ss | m.get_derived_variables(y_ss)
        ss.append(np.fromiter(y_full.values(), dtype="float"))
        fluxes.append(m.get_fluxes(y_full, return_type="array"))

    conc_resp_coef = (ss[0] - ss[1]) / (2 * displacement * old_value)
    flux_resp_coef = (fluxes[0] - fluxes[1]) / (2 * displacement * old_value)

    return (
        pd.Series(conc_resp_coef * y_ss_norm, index=list(y_full.keys())).replace([np.inf, -np.inf], np.nan),
        pd.Series(flux_resp_coef * fluxes_norm, index=list(m.reactions)).replace([np.inf, -np.inf], np.nan),
    )


def get_response_coefficients(
    m: Model,
    constants: list[str],
    y0: dict[str, float],
    displacement: float = _DISPLACEMENT,
    tolerance: float = _DEFAULT_TOLERANCE,
) -> tuple[DataFrame, DataFrame]:
    crcs: dict[str, pd.Series] = {}
    frcs: dict[str, pd.Series] = {}
    for constant in constants:
        crc, frc = _get_response_coefficients_single_constant(
            m=m,
            constant=constant,
            y0=y0,
            displacement=displacement,
            tolerance=tolerance,
        )
        if crc is not None and frc is not None:
            crcs[constant] = crc
            frcs[constant] = frc
    return pd.DataFrame(crcs).T, pd.DataFrame(frcs).T


def plot_coefficient_heatmap(
    df: pd.DataFrame,
    title: str,
    cmap: str = "RdBu_r",
    norm: plt.Normalize | None = None,
    annotate: bool = True,
    colorbar: bool = True,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ax: Optional[Axes] = None,
    cax: Optional[Axes] = None,
    figsize: tuple[float, float] = (8, 6),
) -> tuple[Figure, Axes, QuadMesh]:
    df = df.T.round(2)
    if norm is None:
        end = abs(df.abs().max().max())
        norm = _get_norm(vmin=-end, vmax=end)

    fig, ax, hm = _heatmap_from_dataframe(
        df=df,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        annotate=annotate,
        colorbar=colorbar,
        cmap=cmap,
        norm=norm,
        ax=ax,
        cax=cax,
        figsize=figsize,
    )
    ax.set_xticklabels(ax.get_xticklabels(), **{"rotation": 45, "ha": "right"})
    return fig, ax, hm


def plot_multiple(
    dfs: list[pd.DataFrame],
    titles: list[str],
    cmap: str = "RdBu_r",
    annotate: bool = True,
    colorbar: bool = True,
    figsize: tuple[float, float] = (20, 10),
    norm: plt.Normalize | None = None,
) -> tuple[Figure, Axes]:
    if norm is None:
        vmin = min(i.values.min() for i in dfs)
        vmax = max(i.values.max() for i in dfs)
        end = max(abs(vmin), abs(vmax))
        norm = _get_norm(vmin=-end, vmax=end)

    n_cols = 2
    n_rows = math.ceil(len(dfs) / n_cols)

    if figsize is None:
        figsize = (n_cols * 4, n_rows * 4)

    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=figsize, squeeze=False)
    axs = cast(Axes, axs)
    for ax, df, title in zip(axs.ravel(), dfs, titles):
        plot_coefficient_heatmap(
            df=df,
            title=title,
            cmap=cmap,
            annotate=annotate,
            colorbar=False,
            norm=norm,
            ax=ax,
        )

    # Add a colorbar
    if colorbar:
        cb = fig.colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap),
            ax=axs.ravel()[-1],
        )
        cb.outline.set_linewidth(0)
    fig.tight_layout()
    return fig, axs
