"""Tests for raster functions."""
from pathlib import Path
from tempfile import TemporaryDirectory

import geopandas as gpd
import pandas as pd
import pytest
import rioxarray as rxr
import xarray as xr

from gdptools import ZonalGen
from gdptools.data.user_data import UserTiffData


@pytest.fixture(scope="module")
def get_tiff_slope() -> xr.DataArray:
    """Get tiff slope file."""
    return rxr.open_rasterio("./tests/data/rasters/slope/slope.tif")


@pytest.fixture(scope="module")
def get_tiff_text() -> xr.DataArray:
    """Get tiff text_prms file."""
    return rxr.open_rasterio("./tests/data/rasters/TEXT_PRMS/TEXT_PRMS.tif")


@pytest.fixture(scope="module")
def get_gdf() -> gpd.GeoDataFrame:
    """Get gdf file."""
    return gpd.read_file("./tests/data/Oahu.shp")


@pytest.mark.parametrize(
    "vn,xn,yn,bd,bn,crs,cat,ds,gdf,fid",
    [
        (
            "slope",
            "x",
            "y",
            1,
            "band",
            26904,
            False,
            "get_tiff_slope",
            "get_gdf",
            "fid",
        ),
        (
            "TEXT_PRMS",
            "x",
            "y",
            1,
            "band",
            26904,
            True,
            "get_tiff_text",
            "get_gdf",
            "fid",
        ),
    ],
)
def test_cat_tiff_intersection(vn, xn, yn, bd, bn, crs, cat, ds, gdf, fid, request):
    """Test tiff intersection function."""
    data = UserTiffData(
        var=vn,
        ds=request.getfixturevalue(ds),
        proj_ds=crs,
        x_coord=xn,
        y_coord=yn,
        bname=bn,
        band=bd,
        f_feature=request.getfixturevalue(gdf),
        id_feature=fid,
        proj_feature=crs,
    )
    tmpdir = TemporaryDirectory()
    zonal_gen = ZonalGen(
        user_data=data,
        zonal_engine="serial",
        zonal_writer="csv",
        out_path=tmpdir.name,
        file_prefix="tmpzonal",
    )
    stats = zonal_gen.calculate_zonal(categorical=cat)

    assert isinstance(stats, pd.DataFrame)
    file = Path(tmpdir.name) / "tmpzonal.csv"
    assert file.exists()
    # tdata = TiffAttributes(
    #     varname=vn,
    #     xname=xn,
    #     yname=yn,
    #     band=bd,
    #     bname=bn,
    #     crs=crs,
    #     categorical=cat,
    #     ds=request.getfixturevalue(ds),
    # )

    # ngdf = tiff_intersection_by_feature(
    #     data=tdata, gdf=request.getfixturevalue(gdf), poly_idx=fid
    # )

    # assert isinstance(ngdf, pd.DataFrame)
