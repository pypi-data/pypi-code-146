"""
    Module d'interprétation de la configuration des geos
"""

from __future__ import annotations
from typing import List, Tuple, Union, Optional
from pathlib import Path

import xarray as xr
from pydantic import validator

from mfire.settings import get_logger, Settings, ALT_MIN, ALT_MAX
from mfire.utils.xr_utils import MaskLoader, ArrayLoader
from mfire.composite.base import BaseComposite


# Logging
LOGGER = get_logger(name="geos.mod", bind="geos")


class GeoComposite(BaseComposite):
    """Création d'un objet Geo contenant la configuration des périodes
    de la tâche de production promethee

    Args:
        baseModel : modèle de la librairie pydantic

    Returns:
        baseModel : objet Geo
    """

    file: Path
    mask_id: Optional[Union[List[str], str]]
    grid_name: Optional[str]

    def _compute(self) -> xr.DataArray:
        return MaskLoader(filename=self.file, grid_name=self.grid_name).load(
            ids_list=self.mask_id
        )

    def bounds(self, geo_id: Optional[str] = None) -> Tuple[float, float, float, float]:
        if geo_id is None:
            mask_da = self.compute().max(dim="id")
        else:
            mask_da = self.compute().sel(id=geo_id)
        mask_da = mask_da.where(mask_da.notnull(), drop=True)
        return (
            mask_da.longitude.values.min(),
            mask_da.latitude.values.min(),
            mask_da.longitude.values.max(),
            mask_da.latitude.values.max(),
        )


class AltitudeComposite(BaseComposite):
    """Création d'un objet Field contenant la configuration des champs
    de la tâche de production promethee

    Args:
        baseModel : modèle de la librairie pydantic

    Returns:
        baseModel : objet Field
    """

    filename: Path
    alt_min: Optional[int] = ALT_MIN
    alt_max: Optional[int] = ALT_MAX

    @validator("alt_min")
    def init_alt_min(cls, v: int) -> int:
        if v is None:
            return ALT_MIN
        return v

    @validator("alt_max")
    def init_alt_max(cls, v: int) -> int:
        if v is None:
            return ALT_MAX
        return v

    @validator("filename")
    def init_filename(cls, v: Path) -> Path:
        filename = Path(v)
        if not filename.is_file():
            raise FileNotFoundError(f"No such file {v}.")
        return filename

    def _compute(self) -> xr.DataArray:
        # on load le fichier d'altitude
        field_da = ArrayLoader(filename=self.filename).load()
        # on applique les restrictions d'alt min et alt max
        return field_da.where(field_da >= self.alt_min).where(field_da <= self.alt_max)

    @classmethod
    def from_grid_name(
        cls,
        grid_name: str,
        alt_min: Optional[int] = None,
        alt_max: Optional[int] = None,
    ) -> AltitudeComposite:
        return cls(
            filename=Path(Settings().altitudes_dirname) / f"{grid_name}.nc",
            alt_min=alt_min,
            alt_max=alt_max,
        )
