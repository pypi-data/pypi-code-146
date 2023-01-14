"""Data classes."""
from __future__ import annotations

from typing import Any

import xarray as xr
from attrs import define
from attrs import field
from pyproj.crs import CRS


def check_xname(instance, attribute, value):
    """Validate xname."""
    if value not in instance.ds.coords:
        raise ValueError(f"xname:{value} not in {instance.ds.coords}")


def check_yname(instance, attribute, value):
    """Validate yname."""
    if value not in instance.ds.coords:
        raise ValueError(f"yname:{value} not in {instance.ds.coords}")


def check_band(instance, attribute, value):
    """Validate band name."""
    if value not in instance.ds.coords:
        raise ValueError(f"band:{value} not in {instance.ds.coords}")


def check_crs(instance, attribute, value):
    """Validate crs."""
    crs = CRS.from_user_input(value)
    if not isinstance(crs, CRS):
        raise ValueError(f"crs:{crs} not in valid")


@define(kw_only=True)
class TiffAttributes(object):
    """Tiff qttributes data class."""

    varname: str
    xname: str = field(validator=check_xname)
    yname: str = field(validator=check_yname)
    bname: str = field(validator=check_band)
    band: int = field()
    toptobottom: bool = field(init=False)
    crs: Any = field(validator=check_crs)
    categorical: bool = field()
    ds: xr.DataArray

    def __attrs_post_init__(self):
        """Generate toptobottom."""
        yy = self.ds.coords[self.yname].values
        self.toptobottom = yy[0] <= yy[-1]
