"""Testing ancillary functions."""
from typing import Any

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import pytest
import xarray as xr
from pyproj.crs import CRS
from pyproj.exceptions import CRSError

from gdptools.data.odap_cat_data import CatGrids
from gdptools.data.odap_cat_data import CatParams
from gdptools.utils import _check_for_intersection
from gdptools.utils import _get_cells_poly
from gdptools.utils import _get_crs
from gdptools.utils import _get_data_via_catalog
from gdptools.utils import _get_shp_file


@pytest.mark.parametrize(
    "crs",
    [
        "epsg:4326",
        4326,
        "+proj=longlat +a=6378137 +f=0.00335281066474748 +pm=0 +no_defs",
    ],
)
def test__get_crs(crs: Any) -> None:
    """Test the get_crs function."""
    crs = _get_crs(crs)
    assert isinstance(crs, CRS)


@pytest.mark.parametrize(
    "crs",
    [
        "espg:4326",
        43,
        "+a=6378137 +f=0.00335281066474748 +pm=0 +no_defs",
    ],
)
def test__get_bad_crs(crs: Any) -> None:
    """Test the get_crs function."""
    with pytest.raises(CRSError):
        crs = _get_crs(crs)


@pytest.fixture
def catparam() -> CatParams:
    """Return parameter json."""
    cat_params = "https://mikejohnson51.github.io/opendap.catalog/cat_params.json"
    params = pd.read_json(cat_params)
    _id = "gridmet"  # noqa
    _varname = "daily_maximum_temperature"  # noqa
    tc = params.query("id == @_id & varname == @_varname")
    return CatParams(**tc.to_dict("records")[0])


@pytest.fixture
def catgrid() -> CatGrids:
    """Return grid json."""
    cat_grid = "https://mikejohnson51.github.io/opendap.catalog/cat_grids.json"
    grids = pd.read_json(cat_grid)
    _gridid = 176  # noqa
    tc = grids.query("grid_id == @_gridid")
    return CatGrids(**tc.to_dict("records")[0])


@pytest.fixture
def gdf() -> gpd.GeoDataFrame:
    """Create xarray dataset."""
    return gpd.read_file("./tests/data/hru_1210_epsg5070.shp")


@pytest.fixture
def is_degrees(gdf, catparam, catgrid) -> bool:
    """Check if coords are in degrees."""
    is_intersect, is_degrees, is_0_360 = _check_for_intersection(
        cat_params=catparam, cat_grid=catgrid, gdf=gdf
    )
    return is_degrees


@pytest.fixture
def bounds(gdf, catgrid, is_degrees) -> npt.NDArray[np.double]:
    """Get bounds."""
    gdf, bounds = _get_shp_file(gdf, catgrid, is_degrees)
    return bounds


@pytest.fixture
def xarray(catparam, catgrid, bounds) -> xr.Dataset:
    """Create xarray dataset."""
    return _get_data_via_catalog(catparam, catgrid, bounds, "2020-01-01")


def test__get_cells_poly(catparam, catgrid, bounds) -> None:
    """Test _get_cells_poly."""
    ds = _get_data_via_catalog(catparam, catgrid, bounds, "2020-01-01")
    print(ds)
    assert isinstance(ds, xr.DataArray)
    gdf = _get_cells_poly(xr_a=ds, x="lon", y="lat", crs_in=4326)
    assert isinstance(gdf, gpd.GeoDataFrame)
