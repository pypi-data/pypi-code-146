from __future__ import annotations

import warnings

try:
    from ._perffuncs import (  # type: ignore
        active_transport,
        diffusion,
        diffusion_nonavg,
    )
except ImportError:
    warnings.warn("Import failed, falling back to Python diffusion function")

    def diffusion(
        dydt: list[float],
        y0: list[float],
        is_celltype: list[bool],
        celltype_neighbors: list[list[int]],
        alpha: float,
        n_neighbors: float,
    ):
        for cell, cell_conc in enumerate(y0):
            if is_celltype[cell]:
                diff = 0.0
                for neighbor in celltype_neighbors[cell]:
                    if neighbor != -1:
                        diff += y0[neighbor] - cell_conc
                dydt[cell] += diff / n_neighbors * alpha
        return dydt

    def diffusion_nonavg(
        dydt: list[float],
        y0: list[float],
        is_celltype: list[bool],
        celltype_neighbors: list[list[int]],
        alpha: float,
        n_neighbors: float,
    ):
        for cell, cell_conc in enumerate(y0):
            if is_celltype[cell]:
                diff = 0.0
                for neighbor in celltype_neighbors[cell]:
                    if neighbor != -1:
                        diff += y0[neighbor] - cell_conc
                dydt[cell] += diff * alpha
        return dydt

    def active_transport(
        dydt: list[float],
        y0: list[float],
        is_celltype: list[bool],
        celltype_neighbors: list[list[int]],
        alpha: float,
        n_neighbors: float,
    ):
        for cell, cell_conc in enumerate(y0):
            if is_celltype[cell]:
                for neighbor in celltype_neighbors[cell]:
                    if neighbor != -1:
                        diff = (y0[neighbor] - cell_conc) * alpha
                        if diff < 0:
                            dydt[neighbor] += diff
                            dydt[cell] -= diff
        return dydt
