"""OpenDAP Catalog Data classes."""
from __future__ import annotations

from typing import Optional

import numpy as np
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


class CatParams(BaseModel):
    """Class representing elements of Mike Johnsons OpenDAP catalog params.

    https://mikejohnson51.github.io/opendap.catalog/cat_params.json
    """

    id: Optional[str] = None
    URL: str
    grid_id: Optional[int] = -1
    variable: Optional[str] = None
    varname: str
    long_name: Optional[str] = ...
    T_name: Optional[str] = ...
    duration: Optional[str] = None
    units: Optional[str] = ...
    interval: Optional[str] = None
    nT: Optional[int] = 0  # noqa
    tiled: Optional[str] = None
    model: Optional[str] = None
    ensemble: Optional[str] = None
    scenario: Optional[str] = None

    @validator("grid_id", pre=True, always=True)
    def set_grid_id(cls, v):  # noqa:
        """Convert to int."""
        return int(v)

    @validator("nT", pre=True, always=False)
    def set_nt(cls, v):  # noqa:
        """Convert to int."""
        return 0 if np.isnan(v) else int(v)


class CatGrids(BaseModel):
    """Class representing elements of Mike Johnsons OpenDAP catalog grids.

    https://mikejohnson51.github.io/opendap.catalog/cat_grids.json
    """

    grid_id: Optional[int] = None
    X_name: str
    Y_name: str
    X1: Optional[float] = None
    Xn: Optional[float] = None
    Y1: Optional[float] = None
    Yn: Optional[float] = None
    resX: Optional[float] = None  # noqa
    resY: Optional[float] = None  # noqa
    ncols: Optional[int] = None
    nrows: Optional[int] = None
    proj: str
    toptobottom: int
    tile: Optional[str] = None
    grid_id_1: Optional[str] = Field(None, alias="grid.id")

    @validator("toptobottom", pre=True, always=True)
    def get_toptobottom(cls, v):  # noqa:
        """Convert str to int."""
        return int(v)
