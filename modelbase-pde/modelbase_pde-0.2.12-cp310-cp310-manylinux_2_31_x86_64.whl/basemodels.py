from __future__ import annotations

import copy
import itertools
import math
from typing import Any, Type
import warnings

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from numpy.typing import NDArray

try:
    from assimulo.problem import Explicit_Problem
    from assimulo.solvers import CVode

    ASSIMULO_SUPPORT_FLAG = True

    def _simulate(
        self: GridModel, y0: NDArray, t_end: float, t_points: int = 0
    ) -> tuple[NDArray, NDArray]:
        if t_points > 0:
            t_points -= 1
        problem = Explicit_Problem(self.get_right_hand_side, y0)
        integrator = CVode(problem)
        integrator.verbosity = 50
        t, y = integrator.simulate(t_end, t_points)
        return np.array(t), np.array(y)

except ImportError:
    import scipy.integrate

    def _simulate(
        self: GridModel, y0: NDArray, t_end: float, t_points: int = 0
    ) -> tuple[NDArray, NDArray]:
        if t_points > 0:
            t = np.linspace(0, t_end, t_points)
        else:
            t = np.linspace(0, t_end, 100)
        y = scipy.integrate.odeint(self.get_right_hand_side, y0, t, tfirst=True)
        return np.array(t), np.array(y)

    ASSIMULO_SUPPORT_FLAG = False

from .utils.coordinates import Cube3D, Oddq, Rod, Square, Triangle


class GridModel:
    """General grid model representation"""

    def __init__(
        self,
        gridsize: tuple[int, ...],
        cells: NDArray | None = None,
        parameters: dict[str, float] | None = None,
    ) -> None:
        warnings.warn("Experimental class, API might change.", FutureWarning)
        self._base_shape = None
        self._n_neighbors = 0
        self.initialized = True
        self.gridsize = gridsize
        if cells is None:
            self.cells = np.zeros(gridsize, dtype="int")
        else:
            self.cells = cells
        self.celltypes: dict[str, int] = {}
        self.celltype_indices: dict[str, list[int]] = {}
        self._is_celltype_array: dict[str, list[bool]] = {}
        self.neighbors: dict[str, int] = {}
        if parameters is None:
            self.parameters = {}
        else:
            self.parameters = parameters
        self.variables: list[str] = []

        if not ASSIMULO_SUPPORT_FLAG:
            warnings.warn("Assimulo not found, disabling sundials support.")

    def __reduce__(
        self,
    ) -> tuple[Type[GridModel], tuple[tuple[int, ...], dict[str, float]]]:
        return (self.__class__, (self.gridsize, self.parameters))

    def copy(self) -> GridModel:
        return copy.deepcopy(self)

    def add_celltype(self, name: str, value: int) -> None:
        self.celltypes[name] = value
        self.celltype_indices[name] = []
        self._is_celltype_array[name] = []
        self.initialized = False

    def add_cell(self, coordinates: tuple[int, int], celltype: str) -> None:
        self.cells[coordinates] = self.celltypes[celltype]
        self.initialized = False

    def remove_cell(self, coordinates: tuple[int, int]) -> None:
        self.cells[coordinates] = 0
        self.initialized = False

    def add_variable(self, variable_name: str) -> None:
        if variable_name not in self.variables:
            self.variables.append(variable_name)
            self.initialized = False

    def get_celltypes(self) -> dict[str, int]:
        return self.celltypes

    def get_index_of_coordinates(self, coordinates: tuple[int, int]) -> Any:
        return np.ravel_multi_index(coordinates, self.gridsize)

    def get_coordinates_of_index(self, index: int) -> Any:
        return np.unravel_index(index, self.gridsize)

    def get_indices_of_celltype(self, celltype: str) -> list[int]:
        type_value = self.celltypes[celltype]
        return [
            self.get_index_of_coordinates(i)  # type: ignore
            for i in zip(*np.where(self.cells == type_value))
        ]

    def get_celltype_of_index(self, index: int) -> NDArray:
        return self.cells[self.get_coordinates_of_index(index)]

    def get_cell_neighbors(self, idx):
        """Fills empty positions with -1"""
        upper_borders = self.cells.shape
        neighbors = np.full(self._n_neighbors, -1)
        for idx, neighbor in enumerate(
            self._base_shape(*self.get_coordinates_of_index(idx)).neighbors()
        ):
            neighbor_coordinates = neighbor.coordinates
            if any((i < 0 for i in neighbor_coordinates)):
                pass
            elif any(
                (i >= j for i, j in zip(neighbor_coordinates, upper_borders))
            ):
                pass
            elif self.cells[neighbor_coordinates] != 0:
                neighbors[idx] = self.get_index_of_coordinates(
                    neighbor_coordinates
                )
        return neighbors

    def get_cell_neighbors_of_celltype(self, idx, celltype):
        celltype = self.celltypes[celltype]
        neighbors = np.full(self._n_neighbors, -1)
        for idx, i in enumerate(self.get_cell_neighbors(idx)):
            if i != -1:
                if self.cells[self.get_coordinates_of_index(i)] == celltype:
                    neighbors[idx] = i
        return neighbors

    def get_all_neighbors_of_celltype(self, celltype, neighbor_celltype):
        arr = np.full((np.product(self.gridsize), self._n_neighbors), -1)
        for idx in self.get_indices_of_celltype(celltype):
            arr[idx] = self.get_cell_neighbors_of_celltype(
                idx, neighbor_celltype
            )
        return arr

    def nearest_neighbor_of_celltype(self, cell, neighbor_celltype):
        start = self._base_shape(*cell)
        distances = []
        for c, r in zip(
            *np.where(self.cells == self.celltypes[neighbor_celltype])
        ):
            distances.append(start.distance(self._base_shape(c, r)))
        return min(distances)

    def nearest_distances_of_celltypes(self, celltype1, celltype2):
        distances = []
        for c, r in zip(*np.where(self.cells == self.celltypes[celltype1])):
            distances.append(
                self.nearest_neighbor_of_celltype((c, r), celltype2)
            )
        return distances

    def initialize(self):
        """
        All functions need boolean arrays of cells
        Diffusion and active transport further need neighbor arrays
        """
        # Generate celltype indices
        for celltype in self.celltypes:
            self.celltype_indices[celltype] = np.array(
                self.get_indices_of_celltype(celltype)
            )
            self._is_celltype_array[celltype] = (
                self.cells.flatten() == self.celltypes[celltype]
            )

        # Generate neighbor arrays
        for in_celltype in self.celltypes:
            for out_celltype in self.celltypes:
                self.neighbors[
                    in_celltype, out_celltype
                ] = self.get_all_neighbors_of_celltype(
                    in_celltype, out_celltype
                )
        self.initialized = True

    def generate_initial_values(self):
        # Let's start with a simple: Everything is zero ;)
        y0 = {
            var: np.zeros(self.gridsize, dtype="float")
            for var in self.variables
        }
        return np.stack(tuple(y0.values())).flatten()

    def get_right_hand_side(self, t, y0):
        raise NotImplementedError

    def simulate(self, y0, t_end, t_points=0):
        t, y = _simulate(self, y0, t_end, t_points)
        n_vars = len(self.variables)
        n_dims = self.cells.shape
        if n_vars < 2:
            return t, y.reshape(len(t), *n_dims)
        else:
            y = y.reshape(len(t), n_vars, *n_dims)
            return (t, *[np.squeeze(i) for i in np.split(y, n_vars, axis=1)])

    def plot_axes(self):
        raise NotImplementedError

    def plot_cell(
        self,
        c,
        r,
        ax,
        facecolor: str | tuple[float, float, float, float] = "C1",
        edgecolor: str | tuple[float, float, float, float] = (0, 0, 0, 1),
    ):
        self._base_shape(c, r).plot(
            ax=ax, facecolor=facecolor, edgecolor=edgecolor
        )

    def plot_grid(self, ax):
        cols, rows = self.cells.shape
        for c, r in itertools.product(range(cols), range(rows)):
            self.plot_cell(c, r, facecolor=(0.50, 0.50, 0.50, 1 / 16), ax=ax)

    def plot_cell_coordinates(self, ax, fontsize=14):
        for coordinates in itertools.product(
            *(range(var) for var in self.cells.shape)
        ):
            ax.text(
                *self._base_shape(*coordinates).to_plot(),
                f"{coordinates}",
                fontsize=fontsize,
                ha="center",
                va="center",
            )

    def plot_cell_concentration(self, ax, concentrations, **kwargs):
        local_kwargs = {"ha": "center", "fontsize": 12}
        if kwargs:
            local_kwargs.update(kwargs)
        for coordinates in zip(*np.where(self.cells != 0)):
            ax.text(
                *self._base_shape(*coordinates).to_plot(),
                f"{concentrations[coordinates]:.2g}",
                **local_kwargs,
            )


class RodGridModel(GridModel):
    def __init__(self, gridsize, cells=None, parameters=None) -> None:
        super().__init__(gridsize, cells=cells, parameters=parameters)
        self._base_shape = Rod
        self._n_neighbors = 2


class TriGridModel(GridModel):
    def __init__(self, gridsize, cells=None, parameters=None) -> None:
        super().__init__(gridsize, cells=cells, parameters=parameters)
        self._base_shape = Triangle
        self._n_neighbors = 3

    def plot_axes(self, figsize=None, ax=None):
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
        else:
            fig = ax.get_figure()
        ax.set_aspect("equal")

        c, r = self.cells.shape
        base_shape = self._base_shape(0, 0)
        x_offset = base_shape.x_offset
        y_offset = base_shape.y_offset
        x_lower = -x_offset
        x_upper = 0.5 * c
        y_lower = -y_offset
        y_upper = r * base_shape.h - y_offset
        ax.set_xlim(x_lower, x_upper)
        ax.set_ylim(y_lower, y_upper)
        ax.axis("off")
        return fig, ax


class SquareGridModel(GridModel):
    def __init__(self, gridsize, cells=None, parameters=None) -> None:
        super().__init__(gridsize, cells=cells, parameters=parameters)
        self._base_shape = Square
        self._n_neighbors = 4

    def plot_axes(self, figsize=None, ax=None):
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
        else:
            fig = ax.get_figure()
        ax.set_aspect("equal")

        c, r = self.cells.shape
        x_offset = self._base_shape(0, 0).x_offset
        y_offset = self._base_shape(0, 0).y_offset

        x_lower = -x_offset - 0.1
        x_upper = c - x_offset + 0.1
        y_lower = -y_offset - 0.1
        y_upper = r - y_offset + 0.1
        ax.set_xlim(x_lower, x_upper)
        ax.set_ylim(y_lower, y_upper)
        ax.axis("off")
        return fig, ax


class HexGridModel(GridModel):
    def __init__(self, gridsize, cells=None, parameters=None) -> None:
        super().__init__(gridsize, cells=cells, parameters=parameters)
        self._base_shape = Oddq
        self._n_neighbors = 6

    def plot_axes(self, figsize=None, ax=None):
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
        else:
            fig = ax.get_figure()
        ax.set_aspect("equal")

        c, r = self.cells.shape
        x_lower = -1
        x_upper = 1 + 3 / 2 * (c - 1)
        y_lower = -math.sqrt(3) * 0.5
        y_upper = math.sqrt(3) * r
        ax.set_xlim(x_lower, x_upper)
        ax.set_ylim(y_lower, y_upper)
        ax.axis("off")
        return fig, ax


class CubeGridModel(GridModel):
    def __init__(self, gridsize, cells=None, parameters=None) -> None:
        super().__init__(gridsize, cells=cells, parameters=parameters)
        self._base_shape = Cube3D
        self._n_neighbors = 6

    def plot_axes(self, figsize=None, ax=None):
        if ax is None:
            fig, ax = plt.subplots(
                1, 1, figsize=figsize, subplot_kw={"projection": "3d"}
            )
        else:
            fig = ax.get_figure()

        a, b, c = self.cells.shape
        ax.set_xlim(0, a)
        ax.set_ylim(0, b)
        ax.set_zlim(0, c)
        ax.axis("off")
        return fig, ax

    def plot_cell(
        self,
        c: float,
        r: float,
        z: float,
        ax: Axes,
        facecolor: str | tuple[float, float, float, float] = "C1",
        edgecolor: str | tuple[float, float, float, float] = (0, 0, 0, 1 / 8),
    ):
        self._base_shape(c, r, z).plot(
            ax=ax, facecolor=facecolor, edgecolor=edgecolor
        )
        return ax

    def plot_grid(
        self,
        ax,
        facecolor: str
        | tuple[float, float, float, float] = (0.50, 0.50, 0.50, 1 / 16),
        edgecolor: str | tuple[float, float, float, float] = (0, 0, 0, 1 / 16),
    ):
        x, y, z = self.cells.shape
        for x, y, z in itertools.product(range(x), range(y), range(z)):
            self.plot_cell(
                x, y, z, facecolor=facecolor, edgecolor=edgecolor, ax=ax
            )
        return ax
