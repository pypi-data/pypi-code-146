"""Test WghtGen and AggGen classes."""
from pathlib import Path
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory
from typing import Dict

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import pytest
import xarray as xr

from gdptools import AggGen
from gdptools import ODAPCatData
from gdptools import UserCatData
from gdptools import WeightGen

gm_vars = ["aet", "pet", "PDSI"]


@pytest.fixture
def aet_ma_average() -> npt.NDArray[np.double]:
    """Test values for masked-average calculation."""
    return np.asarray(
        [
            [3.1605408],
            [0.0121277],
            [41.983784],
            [68.91504],
            [81.72351],
            [92.60617],
            [48.96107],
            [37.30392],
            [27.883911],
            [64.65818],
            [52.897045],
            [1.6390916],
        ]
    )


@pytest.fixture
def aet_average() -> npt.NDArray[np.double]:
    """Test values for average calculation."""
    return np.asarray(
        [
            [3.1551743],
            [0.0121071],
            [41.9124973],
            [68.7980207],
            [81.5847434],
            [92.4489252],
            [48.8779355],
            [37.2405776],
            [27.8365651],
            [64.5483926],
            [52.8072282],
            [1.63630845],
        ]
    )


@pytest.fixture
def param_dict(vars=gm_vars) -> Dict:
    """Return parameter json."""
    cat_params = "https://mikejohnson51.github.io/opendap.catalog/cat_params.json"
    params = pd.read_json(cat_params)
    _id = "terraclim"  # noqa
    var_params = [
        params.query(
            "id == @_id & variable == @_var", local_dict={"_id": _id, "_var": _var}
        ).to_dict(orient="records")[0]
        for _var in vars
    ]
    return dict(zip(vars, var_params))  # noqa B905


@pytest.fixture
def grid_dict(vars=gm_vars) -> Dict:
    """Return grid json."""
    cat_grid = "https://mikejohnson51.github.io/opendap.catalog/cat_grids.json"
    grids = pd.read_json(cat_grid)
    _gridid = 116  # noqa
    var_grid = [
        grids.query(
            "grid_id == @_gridid", local_dict={"_gridid": _gridid, "_var": _var}
        ).to_dict(orient="records")[0]
        for _var in vars
    ]
    return dict(zip(vars, var_grid))  # noqa B905


@pytest.fixture
def gdf() -> gpd.GeoDataFrame:
    """Create xarray dataset."""
    return gpd.read_file("./tests/data/hru_1210_epsg5070.shp")


@pytest.fixture
def poly_idx() -> str:
    """Return poly_idx."""
    return "hru_id_nat"


@pytest.fixture
def wght_gen_proj() -> int:
    """Return wght gen projection."""
    return 6931


def test_odapcatdata_p(
    param_dict, grid_dict, gdf, poly_idx, wght_gen_proj, aet_ma_average, aet_average
) -> None:
    """Test ODAPCatData."""
    user_data = ODAPCatData(
        param_dict=param_dict,
        grid_dict=grid_dict,
        f_feature=gdf,
        id_feature=poly_idx,
        period=["1980-01-01", "1980-12-31"],
    )
    tmpfile = NamedTemporaryFile()

    gen_weights = WeightGen(
        user_data=user_data,
        method="parallel",
        output_file=tmpfile.name,
        weight_gen_crs=wght_gen_proj,
    )

    _wghts = gen_weights.calculate_weights()  # noqa: F841

    tmpdir = TemporaryDirectory()
    gen_agg = AggGen(
        user_data=user_data,
        stat_method="masked_average",
        agg_engine="serial",
        agg_writer="netcdf",
        weights=tmpfile.name,
        out_path=tmpdir.name,
        file_prefix="test_agg_gen",
    )

    _ngdf, nvals = gen_agg.calculate_agg()
    file = Path(tmpdir.name) / "test_agg_gen.nc"
    assert file.exists()

    np.testing.assert_allclose(aet_ma_average, nvals[0], rtol=1e-4, verbose=True)

    tmpdir2 = TemporaryDirectory()
    gen_agg = AggGen(
        user_data=user_data,
        stat_method="average",
        agg_engine="serial",
        agg_writer="csv",
        weights=tmpfile.name,
        out_path=tmpdir2.name,
        file_prefix="test_agg_gen",
    )

    test_arr = np.asarray(
        [
            [3.1551743],
            [0.0121071],
            [41.9124973],
            [68.7980207],
            [81.5847434],
            [92.4489252],
            [48.8779355],
            [37.2405776],
            [27.8365651],
            [64.5483926],
            [52.8072282],
            [1.63630845],
        ]
    )
    _ngdf, nvals2 = gen_agg.calculate_agg()
    file = Path(tmpdir2.name) / "test_agg_gen.csv"
    assert file.exists()
    print(nvals2[0])
    np.testing.assert_allclose(test_arr, nvals2[0], rtol=1e-4, verbose=True)


def test_odapcatdata(
    param_dict, grid_dict, gdf, poly_idx, wght_gen_proj, tvars=gm_vars
) -> None:
    """Test ODAPCatData."""
    user_data = ODAPCatData(
        param_dict=param_dict,
        grid_dict=grid_dict,
        f_feature=gdf,
        id_feature=poly_idx,
        period=["1980-01-01", "1980-12-31"],
    )
    tmpfile = NamedTemporaryFile()

    gen_weights = WeightGen(
        user_data=user_data,
        method="serial",
        output_file=tmpfile.name,
        weight_gen_crs=wght_gen_proj,
    )

    _wghts = gen_weights.calculate_weights()  # noqa: F841

    tmpdir = TemporaryDirectory()

    gen_agg = AggGen(
        user_data=user_data,
        stat_method="masked_average",
        agg_engine="serial",
        agg_writer="netcdf",
        weights=tmpfile.name,
        out_path=tmpdir.name,
        file_prefix="test_agg_gen",
    )

    _ngdf, nvals = gen_agg.calculate_agg()

    tmpdir2 = TemporaryDirectory()
    gen_agg2 = AggGen(
        user_data=user_data,
        stat_method="masked_average",
        agg_engine="serial",
        agg_writer="csv",
        weights=tmpfile.name,
        out_path=tmpdir2.name,
        file_prefix="test_agg_gen",
    )

    _ngdf2, _nvals2 = gen_agg2.calculate_agg()

    test_arr = np.asarray(
        [
            [3.1605408],
            [0.0121277],
            [41.983784],
            [68.91504],
            [81.72351],
            [92.60617],
            [48.96107],
            [37.30392],
            [27.883911],
            [64.65818],
            [52.897045],
            [1.6390916],
        ]
    )

    np.testing.assert_allclose(test_arr, nvals[0], rtol=1e-4, verbose=True)

    file = Path(tmpdir.name) / "test_agg_gen.nc"

    assert file.exists()


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


def test_usercatdata(get_xarray, get_gdf, get_file_path, get_out_path) -> None:
    """Test UserCatData."""
    user_data = UserCatData(
        ds=get_xarray,
        proj_ds=data_crs,
        x_coord=x_coord,
        y_coord=y_coord,
        t_coord=t_coord,
        var=[var],
        f_feature=get_gdf,
        proj_feature=shp_crs,
        id_feature=shp_poly_idx,
        period=[sdate, edate],
    )

    tmpfile = NamedTemporaryFile()
    weight_gen = WeightGen(
        user_data=user_data,
        method="serial",
        output_file=tmpfile.name,
        weight_gen_crs=wght_gen_crs,
    )

    wghts = weight_gen.calculate_weights()

    weight_gen2 = WeightGen(
        user_data=user_data,
        method="parallel",
        output_file=tmpfile.name,
        weight_gen_crs=wght_gen_crs,
    )

    _wghts2 = weight_gen2.calculate_weights()  # noqa: F841

    tmpdir = TemporaryDirectory()

    agg_gen = AggGen(
        user_data=user_data,
        stat_method="average",
        agg_engine="serial",
        agg_writer="csv",
        weights=wghts,
        out_path=tmpdir.name,
        file_prefix="test_agg_gen_2",
    )

    _ngdf, _nvals = agg_gen.calculate_agg()
    print(_nvals[0])

    tmpdir2 = TemporaryDirectory()
    agg_gen = AggGen(
        user_data=user_data,
        stat_method="masked_average",
        agg_engine="serial",
        agg_writer="netcdf",
        weights=wghts,
        out_path=tmpdir2.name,
        file_prefix="test_agg_gen_2",
    )

    _ngdf, _nvals = agg_gen.calculate_agg()

    outfile = Path(tmpdir.name) / "test_agg_gen_2.csv"

    assert outfile.exists()
