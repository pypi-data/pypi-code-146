"""Tests for .helper functions."""
import geopandas as gpd
import pandas as pd
import pytest
import xarray as xr

from gdptools.data.odap_cat_data import CatGrids
from gdptools.data.odap_cat_data import CatParams
from gdptools.helpers import get_data_subset_catalog


@pytest.fixture()
def get_gdf() -> gpd.GeoDataFrame:
    """Create GeoDataFrame."""
    return gpd.read_file("./tests/data/hru_1210_epsg5070.shp")


@pytest.fixture()
def get_xarray() -> xr.Dataset:
    """Create xarray Dataset."""
    # return xr.open_dataset("./tests/data/cape_cod_tmax.nc")
    return xr.open_dataset(
        "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_met_tmmx_1979_CurrentYear_CONUS.nc"
    )


@pytest.fixture()
def get_file_path(tmp_path):
    """Get temp file path."""
    return tmp_path / "test.csv"


@pytest.fixture()
def get_out_path(tmp_path):
    """Get temp file output path."""
    return tmp_path


data_crs = 4326
x_coord = "lon"
y_coord = "lat"
t_coord = "day"
sdate = "1979-01-01"
edate = "1979-01-07"
var = "daily_maximum_temperature"
shp_crs = 5070
shp_poly_idx = "hru_id_nat"
wght_gen_crs = 6931


@pytest.fixture(scope="module")
def catparam() -> CatParams:
    """Return parameter json."""
    cat_params = "https://mikejohnson51.github.io/opendap.catalog/cat_params.json"
    params = pd.read_json(cat_params)
    _id = "terraclim"  # noqa
    _varname = "aet"  # noqa
    tc = params.query("id == @_id & varname == @_varname")
    return CatParams(**tc.to_dict("records")[0])


@pytest.fixture(scope="module")
def catgrid(catparam) -> CatGrids:
    """Return grid json."""
    cat_grid = "https://mikejohnson51.github.io/opendap.catalog/cat_grids.json"
    grids = pd.read_json(cat_grid)
    _gridid = catparam.grid_id  # noqa
    tc = grids.query("grid_id == @_gridid")
    return CatGrids(**tc.to_dict("records")[0])


@pytest.fixture(scope="module")
def get_gdf_world() -> gpd.GeoDataFrame:
    """Get gdf file with country testing."""
    return gpd.read_file(
        "./tests/data/TM_WORLD_BORDERS_SIMPL-0.3/TM_WORLD_BORDERS_SIMPL-0.3.shp"
    )


@pytest.fixture(scope="module")
def get_begin_date() -> str:
    """Get begin date."""
    return "2005-01-01"


@pytest.fixture(scope="module")
def get_end_date() -> str:
    """Get end date."""
    return "2005-02-01"


@pytest.mark.parametrize(
    "cp,cg,gdf,sd,ed,name",
    [
        (
            "catparam",
            "catgrid",
            "get_gdf_world",
            "get_begin_date",
            "get_end_date",
            "Chile",
        ),
        (
            "catparam",
            "catgrid",
            "get_gdf_world",
            "get_begin_date",
            "get_end_date",
            "Netherlands",
        ),
        (
            "catparam",
            "catgrid",
            "get_gdf_world",
            "get_begin_date",
            "get_end_date",
            "Kenya",
        ),
        (
            "catparam",
            "catgrid",
            "get_gdf_world",
            "get_begin_date",
            "get_end_date",
            "Samoa",
        ),
        (
            "catparam",
            "catgrid",
            "get_gdf_world",
            "get_begin_date",
            "get_end_date",
            "Fiji",
        ),
    ],
)
def test_get_data_subset_catalog(cp, cg, gdf, sd, ed, name, request):
    """Test subset catalog."""
    ds = get_data_subset_catalog(
        cat_params=request.getfixturevalue(cp),
        cat_grid=request.getfixturevalue(cg),
        shp_file=request.getfixturevalue(gdf).query("NAME == @name"),
        begin_date=request.getfixturevalue(sd),
        end_date=request.getfixturevalue(ed),
    )

    assert isinstance(ds, xr.DataArray)
