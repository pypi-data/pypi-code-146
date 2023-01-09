from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from .basemodels import (
    CubeGridModel,
    HexGridModel,
    SquareGridModel,
    TriGridModel,
)
from .utils import perffuncs
from matplotlib.axes import Axes


def photosynthesis_constant(_: float, k: float) -> float:
    return k


def photosynthesis_saturating(sugar: float, km: float, vmax: float) -> float:
    return vmax / np.exp(km * sugar)


def photosynthesis_co2(sugar: float, co2: float, vmax: float) -> float:
    return vmax * co2 / np.exp(sugar)


def photosynthesis_reversible(
    sugar: float, co2: float, midpoint: float, magnitude: float
) -> float:
    return (magnitude / (1 + np.exp(sugar - midpoint)) - magnitude / 2) * co2


def co2_influx(co2: float, x0: float = 10, L: float = 1) -> float:
    """Self-limiting co2 influx function"""
    return L / (1 + np.exp(co2 - x0)) - L / 2


def outflux(sugar: float, alpha: float) -> float:
    return -sugar * alpha


class _Leaf:
    def __init__(self) -> None:
        self.influx_functions = {}
        self.single_cell_outflux_functions = {}
        self.outflux_functions = {}
        self.diffusion_functions = {}
        self.active_transport = {}

    def add_influx_function(
        self,
        name,
        in_vars,
        out_vars,
        input_cells,
        output_cells,
        function,
        parameters,
    ):
        self.influx_functions[name] = {
            "func": function,
            "in_vars": in_vars,
            "out_vars": out_vars,
            "pars": parameters,
            "in_cells": input_cells,
            "out_cells": output_cells,
        }

    def add_outflux_function(
        self, name, out_vars, output_cells, function, parameters
    ):
        self.outflux_functions[name] = {
            "func": function,
            "out_vars": out_vars,
            "pars": parameters,
            "out_cells": output_cells,
        }

    def add_single_cell_outflux_function(
        self, name, cell_index, var_type, function, parameters
    ):
        self.single_cell_outflux_functions[name] = {
            "func": function,
            "cell_index": cell_index,
            "var_type": var_type,
            "pars": parameters,
        }

    def add_diffusion_function(
        self, name, variable, in_cells, out_cells, parameter
    ):
        self.diffusion_functions[name] = {
            "variable": variable,
            "in_cells": in_cells,
            "out_cells": out_cells,
            "parameter": parameter,
        }

    def add_active_transport_function(
        self, name, variable, in_cells, out_cells, parameter
    ):
        self.active_transport[name] = {
            "variable": variable,
            "in_cells": in_cells,
            "out_cells": out_cells,
            "parameter": parameter,
        }

    def get_right_hand_side(self, t, y):
        # y
        in_vars = dict(zip(self.variables, np.hsplit(y, len(self.variables))))
        # dydt
        out_vars = {
            i: np.zeros(self.gridsize).flatten() for i in self.variables
        }

        # Influx functions
        for influx_function in self.influx_functions.values():
            (
                func,
                in_types,
                out_type,
                pars,
                in_cells,
                out_cells,
            ) = influx_function.values()
            out_vars[out_type][self.celltype_indices[out_cells]] += func(
                *[
                    in_vars[type_][self.celltype_indices[in_cells]]
                    for type_ in in_types
                ],
                *[self.parameters[i] for i in pars],
            )

        # Diffusion functions
        for func in self.diffusion_functions.values():
            variable, in_cells, out_cells, parameter = func.values()
            out_vars[variable] = self.diffusion_function(
                out_vars[variable],
                in_vars[variable],
                self._is_celltype_array[in_cells],
                self.neighbors[in_cells, out_cells],
                self.parameters[parameter],
                self._n_neighbors,
            )

        # Active transport functions
        for func in self.active_transport.values():
            variable, in_cells, out_cells, parameter = func.values()
            out_vars[variable] = self.active_transport_function(
                out_vars[variable],
                in_vars[variable],
                self._is_celltype_array[in_cells],
                self.neighbors[in_cells, out_cells],
                self.parameters[parameter],
                self._n_neighbors,
            )

        # Single cell outflux functions
        for outflux_func in self.single_cell_outflux_functions.values():
            func, cell_index, var_type, pars = outflux_func.values()
            out_vars[var_type][cell_index] += func(
                in_vars[var_type][cell_index],
                *[self.parameters[i] for i in pars],
            )

        # Outflux functions
        for outflux_function in self.outflux_functions.values():
            func, in_types, pars, in_cells = outflux_function.values()
            out_vars[in_types][self.celltype_indices[in_cells]] += func(
                *[
                    in_vars[type_][self.celltype_indices[in_cells]]
                    for type_ in in_types
                ],
                *[self.parameters[i] for i in pars],
            )
        return np.array(list(out_vars.values())).flatten()

    def plot_cells(
        self,
        ax: Axes,
        concentrations=None,
        min_conc=None,
        max_conc=None,
        alpha=None,
        **kwargs,
    ):
        if concentrations is None:
            concentrations = np.ones(self.gridsize)
            min_conc = 0
            max_conc = 1
        else:
            if min_conc is None:
                min_conc = np.min(
                    concentrations[self.cells != 0]
                )  # Otherwise this is always 0
            if max_conc is None:
                max_conc = np.max(concentrations)
            if min_conc == max_conc:
                max_conc += 0.1
        normalized_concentrations = (concentrations - min_conc) / (
            max_conc - min_conc
        )

        # Photosynthetic cells
        for c, r in zip(*np.where(self.cells == 1)):
            if alpha is None:
                al = max(normalized_concentrations[c, r], 0.05)
            else:
                al = alpha
            self.plot_cell(
                c,
                r,
                facecolor=(0.00, 0.50, 0.00, al),
                edgecolor=(0, 0, 0, 1),
                ax=ax,
            )

        # Veins
        for c, r in zip(*np.where(self.cells == 2)):
            if alpha is None:
                al = max(normalized_concentrations[c, r], 0.05)
            else:
                al = alpha
            self.plot_cell(
                c,
                r,
                facecolor=(0.30, 0.15, 0.03, al),
                edgecolor=(0, 0, 0, 1),
                ax=ax,
            )

        # Stoma
        for c, r in zip(*np.where(self.cells == 3)):
            if alpha is None:
                al = max(normalized_concentrations[c, r], 0.05)
            else:
                al = alpha
            self.plot_cell(
                c,
                r,
                facecolor=(0.80, 0.37, 0.04, al),
                edgecolor=(0, 0, 0, 1),
                ax=ax,
            )
        return ax

    def plot(
        self,
        concentrations=None,
        min_conc=None,
        max_conc=None,
        figsize=(10, 10),
        ax: Axes | None = None,
        annotate=False,
        alpha=None,
        **kwargs,
    ):
        fig, ax = self.plot_axes(figsize=figsize, ax=ax)
        ax = self.plot_cells(
            ax, concentrations, min_conc, max_conc, alpha, **kwargs
        )
        if annotate:
            ax = self.plot_cell_concentrations(ax, concentrations, **kwargs)
        return fig, ax

    def time_lapse(
        self,
        y,
        annotate=False,
        filename=None,
        figsize=(10, 10),
        ffmpeg_path="/usr/bin/ffmpeg",
    ):
        plt.rcParams["animation.ffmpeg_path"] = ffmpeg_path
        fig, ax = self.plot_axes(figsize=figsize)
        plt.close()

        def init():
            ax.patches = []
            return fig, ax

        def update_func(frame):
            ax.patches = []
            ax.texts = []
            y_current = y[frame]
            self.plot_cells(ax=ax, concentrations=y_current)
            if annotate:
                self.plot_cell_concentration(ax=ax, concentrations=y_current)
            return None

        anim = animation.FuncAnimation(
            fig,
            update_func,
            frames=list(range(len(y) // 2)),
            init_func=init,
            repeat=False,
        )
        return anim


class _VeinModel:
    def __init__(self, vein_base_coordinates) -> None:
        self.add_celltype("mesophyll", 1)
        self.add_celltype("vein", 2)
        self.add_variable("sucrose")
        self._vein_base = self.get_index_of_coordinates(vein_base_coordinates)

        self.add_influx_function(
            "ps",
            in_vars=["sucrose"],
            out_vars="sucrose",
            input_cells="mesophyll",
            output_cells="mesophyll",
            function=photosynthesis_saturating,
            parameters=["ps_km", "ps_vmax"],
        )
        self.add_diffusion_function(
            name="suc_meso_to_meso",
            variable="sucrose",
            in_cells="mesophyll",
            out_cells="mesophyll",
            parameter="suc_meso_to_meso",
        )
        self.add_diffusion_function(
            name="suc_vein_to_vein",
            variable="sucrose",
            in_cells="vein",
            out_cells="vein",
            parameter="suc_vein_to_vein",
        )
        self.add_active_transport_function(
            name="suc_meso_to_vein",
            variable="sucrose",
            in_cells="mesophyll",
            out_cells="vein",
            parameter="suc_meso_to_vein",
        )
        self.add_single_cell_outflux_function(
            name="main_vein",
            cell_index=self._vein_base,
            var_type="sucrose",
            function=outflux,
            parameters=["suc_vein_to_vein"],
        )

    def get_vein_outflux(self, y):
        """Get vein outflux for a single concentration array"""
        func, cell_idx, var_type, pars = self.single_cell_outflux_functions[
            "main_vein"
        ].values()
        if y.ndim == 2:
            return (
                func(y.flatten()[cell_idx], *[self.parameters[i] for i in pars])
                * -1
            )
        else:
            res = [
                func(i.flatten()[cell_idx], *[self.parameters[i] for i in pars])
                for i in y
            ]
            return np.array(res) * -1


class _StomataModel(_VeinModel):
    def __init__(self, vein_base_coordinates) -> None:
        super().__init__(vein_base_coordinates=vein_base_coordinates)
        self.add_celltype("stoma", 3)
        self.add_variable("co2")

        self.add_influx_function(
            "ps",
            in_vars=["sucrose", "co2"],
            out_vars="sucrose",
            input_cells="mesophyll",
            output_cells="mesophyll",
            function=photosynthesis_co2,
            parameters=["ps_vmax"],
        )
        self.add_influx_function(
            "co2_influx",
            in_vars=["co2"],
            out_vars="co2",
            input_cells="stoma",
            output_cells="stoma",
            function=photosynthesis_saturating,
            parameters=["co2_km", "co2_vmax"],
        )
        self.add_active_transport_function(
            name="co2_stoma_to_meso",
            variable="co2",
            in_cells="stoma",
            out_cells="mesophyll",
            parameter="co2_stoma_to_meso",
        )
        self.add_diffusion_function(
            name="co2_meso_to_meso",
            variable="co2",
            in_cells="mesophyll",
            out_cells="mesophyll",
            parameter="co2_meso_to_meso",
        )


class TriLeafModel(_Leaf, TriGridModel):
    def __init__(self, gridsize, cells=None, parameters=None) -> None:
        TriGridModel.__init__(
            self, gridsize, cells=cells, parameters=parameters
        )
        _Leaf.__init__(self)
        self.diffusion_function = perffuncs.diffusion_nonavg
        self.active_transport_function = perffuncs.active_transport


class SquareLeafModel(_Leaf, SquareGridModel):
    def __init__(self, gridsize, cells=None, parameters=None) -> None:
        SquareGridModel.__init__(
            self, gridsize, cells=cells, parameters=parameters
        )
        _Leaf.__init__(self)
        self.diffusion_function = perffuncs.diffusion_nonavg
        self.active_transport_function = perffuncs.active_transport


class HexLeafModel(_Leaf, HexGridModel):
    def __init__(self, gridsize, cells=None, parameters=None) -> None:
        HexGridModel.__init__(
            self, gridsize, cells=cells, parameters=parameters
        )
        _Leaf.__init__(self)
        self.diffusion_function = perffuncs.diffusion_nonavg
        self.active_transport_function = perffuncs.active_transport


class CubeLeafModel(_Leaf, CubeGridModel):
    def __init__(self, gridsize, cells=None, parameters=None) -> None:
        CubeGridModel.__init__(
            self, gridsize, cells=cells, parameters=parameters
        )
        _Leaf.__init__(self)
        self.diffusion_function = perffuncs.diffusion_nonavg

    def plot_cells(
        self,
        ax: Axes,
        concentrations=None,
        min_conc=None,
        max_conc=None,
        alpha=None,
        **kwargs,
    ):
        # Normalize concentrations
        if concentrations is None:
            concentrations = np.ones(self.gridsize)
            min_conc = 0
            max_conc = 1
        else:
            if min_conc is None:
                min_conc = np.min(
                    concentrations[self.cells != 0]
                )  # Otherwise this is always 0
            if max_conc is None:
                max_conc = np.max(concentrations)
            if min_conc == max_conc:
                max_conc += 0.1
        normalized_concentrations = (concentrations - min_conc) / (
            max_conc - min_conc
        )

        for x, y, z in zip(*np.where(self.cells == 1)):
            if alpha is None:
                al = max(normalized_concentrations[x, y, z], 0)
            else:
                al = alpha
            self.plot_cell(
                x,
                y,
                z,
                facecolor=(0.00, 0.50, 0.00, al),
                edgecolor=(0, 0, 0, 1),
                ax=ax,
            )

        for x, y, z in zip(*np.where(self.cells == 2)):
            if alpha is None:
                al = max(normalized_concentrations[x, y, z], 0)
            else:
                al = alpha
            self.plot_cell(
                x,
                y,
                z,
                facecolor=(0.30, 0.15, 0.03, al),
                edgecolor=(0, 0, 0, 1),
                ax=ax,
            )

        for x, y, z in zip(*np.where(self.cells == 3)):
            if alpha is None:
                al = max(normalized_concentrations[x, y, z], 0)
            else:
                al = alpha
            self.plot_cell(
                x,
                y,
                z,
                facecolor=(0.80, 0.37, 0.04, al),
                edgecolor=(0, 0, 0, 1),
                ax=ax,
            )
        return ax

    def plot(
        self,
        concentrations=None,
        min_conc=None,
        max_conc=None,
        figsize=(10, 10),
        ax=None,
        annotate=False,
        alpha=None,
        **kwargs,
    ):
        fig, ax = self.plot_axes(figsize=figsize, ax=ax)
        self.plot_cells(
            ax=ax,
            concentrations=concentrations,
            min_conc=min_conc,
            max_conc=max_conc,
            alpha=alpha,
            **kwargs,
        )
        return fig, ax


class TriVeinModel(TriLeafModel, _VeinModel):
    def __init__(
        self, gridsize, vein_base_coordinates, cells=None, parameters=None
    ) -> None:
        TriLeafModel.__init__(
            self, gridsize, cells=cells, parameters=parameters
        )
        _VeinModel.__init__(self, vein_base_coordinates)

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.gridsize,
                self.get_coordinates_of_index(self._vein_base),
                self.cells,
                self.parameters,
            ),
        )


class SquareVeinModel(SquareLeafModel, _VeinModel):
    def __init__(
        self, gridsize, vein_base_coordinates, cells=None, parameters=None
    ) -> None:
        SquareLeafModel.__init__(
            self, gridsize, cells=cells, parameters=parameters
        )
        _VeinModel.__init__(self, vein_base_coordinates)

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.gridsize,
                self.get_coordinates_of_index(self._vein_base),
                self.cells,
                self.parameters,
            ),
        )


class HexVeinModel(HexLeafModel, _VeinModel):
    def __init__(
        self, gridsize, vein_base_coordinates, cells=None, parameters=None
    ) -> None:
        HexLeafModel.__init__(
            self, gridsize, cells=cells, parameters=parameters
        )
        _VeinModel.__init__(self, vein_base_coordinates)

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.gridsize,
                self.get_coordinates_of_index(self._vein_base),
                self.cells,
                self.parameters,
            ),
        )


class TriStomataModel(TriLeafModel, _StomataModel):
    def __init__(
        self, gridsize, vein_base_coordinates, cells=None, parameters=None
    ) -> None:
        TriLeafModel.__init__(
            self, gridsize, cells=cells, parameters=parameters
        )
        _StomataModel.__init__(self, vein_base_coordinates)

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.gridsize,
                self.get_coordinates_of_index(self._vein_base),
                self.cells,
                self.parameters,
            ),
        )


class SquareStomataModel(SquareLeafModel, _StomataModel):
    def __init__(
        self, gridsize, vein_base_coordinates, cells=None, parameters=None
    ) -> None:
        SquareLeafModel.__init__(
            self, gridsize, cells=cells, parameters=parameters
        )
        _StomataModel.__init__(self, vein_base_coordinates)

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.gridsize,
                self.get_coordinates_of_index(self._vein_base),
                self.cells,
                self.parameters,
            ),
        )


class HexStomataModel(HexLeafModel, _StomataModel):
    def __init__(
        self, gridsize, vein_base_coordinates, cells=None, parameters=None
    ) -> None:
        HexLeafModel.__init__(
            self, gridsize=gridsize, cells=cells, parameters=parameters
        )
        _StomataModel.__init__(
            self, vein_base_coordinates=vein_base_coordinates
        )

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.gridsize,
                self.get_coordinates_of_index(self._vein_base),
                self.cells,
                self.parameters,
            ),
        )
