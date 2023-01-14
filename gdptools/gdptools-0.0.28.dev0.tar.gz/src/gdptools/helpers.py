"""Primary functions for poly-to-poly area-weighted mapping."""
from __future__ import annotations

import itertools
import logging
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import xarray as xr
from shapely.geometry import Polygon

from gdptools.data.odap_cat_data import CatGrids
from gdptools.data.odap_cat_data import CatParams
from gdptools.utils import _check_for_intersection
from gdptools.utils import _get_data_via_catalog
from gdptools.utils import _get_shp_file
from gdptools.utils import _read_shp_file

# from numba import jit

logger = logging.getLogger(__name__)

pd_offset_conv: Dict[str, str] = {
    "years": "Y",
    "months": "M",
    "days": "D",
    "hours": "H",
}


def get_cells_poly_2d(
    xr_a: xr.Dataset, lon_str: str, lat_str: str, in_crs: Any
) -> gpd.GeoDataFrame:
    """Get cell polygons associated with 2d lat/lon coordinates.

    Args:
        xr_a (xr.Dataset): _description_
        lon_str (str): _description_
        lat_str (str): _description_
        in_crs (Any): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    lon = xr_a[lon_str]
    lat = xr_a[lat_str]
    count = 0
    poly = []
    lon_n = [
        lon[i, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_jm1 = [
        lon[i, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1_jm1 = [
        lon[i + 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1 = [
        lon[i + 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1_jp1 = [
        lon[i + 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_jp1 = [
        lon[i, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1_jp1 = [
        lon[i - 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1 = [
        lon[i - 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1_jm1 = [
        lon[i - 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]

    lat_n = [
        lat[i, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_jm1 = [
        lat[i, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1_jm1 = [
        lat[i + 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1 = [
        lat[i + 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1_jp1 = [
        lat[i + 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_jp1 = [
        lat[i, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1_jp1 = [
        lat[i - 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1 = [
        lat[i - 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1_jm1 = [
        lat[i - 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]

    # print(len(lon_n), len(lat_n), type(lon_n), np.shape(lon_n))
    numcells = len(lon_n)
    index = np.array(range(numcells))
    i_index = np.empty(numcells)
    j_index = np.empty(numcells)
    for count, (i, j) in enumerate(
        itertools.product(range(1, lon.shape[0] - 1), range(1, lon.shape[1] - 1))
    ):
        i_index[count] = i
        j_index[count] = j
    tpoly_1_lon = [
        [lon_n[i], lon_jm1[i], lon_ip1_jm1[i], lon_ip1[i]] for i in range(numcells)
    ]
    tpoly_1_lat = [
        [lat_n[i], lat_jm1[i], lat_ip1_jm1[i], lat_ip1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_1_lon), tpoly_1_lon[0])
    newp = [
        Polygon(zip(tpoly_1_lon[i], tpoly_1_lat[i]))  # noqa B905
        for i in range(numcells)
    ]
    p1 = [p.centroid for p in newp]
    # print(type(newp), newp[0], len(p1))

    tpoly_2_lon = [
        [lon_n[i], lon_ip1[i], lon_ip1_jp1[i], lon_jp1[i]] for i in range(numcells)
    ]
    tpoly_2_lat = [
        [lat_n[i], lat_ip1[i], lat_ip1_jp1[i], lat_jp1[i]] for i in range(numcells)
    ]
    print(len(tpoly_2_lon), tpoly_2_lon[0])
    newp = [
        Polygon(zip(tpoly_2_lon[i], tpoly_2_lat[i]))  # noqa B905
        for i in range(numcells)
    ]
    p2 = [p.centroid for p in newp]

    tpoly_3_lon = [
        [lon_n[i], lon_jp1[i], lon_im1_jp1[i], lon_im1[i]] for i in range(numcells)
    ]
    tpoly_3_lat = [
        [lat_n[i], lat_jp1[i], lat_im1_jp1[i], lat_im1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_3_lon), tpoly_3_lon[0])
    newp = [
        Polygon(zip(tpoly_3_lon[i], tpoly_3_lat[i]))  # noqa B905
        for i in range(numcells)
    ]
    p3 = [p.centroid for p in newp]

    tpoly_4_lon = [
        [lon_n[i], lon_im1[i], lon_im1_jm1[i], lon_jm1[i]] for i in range(numcells)
    ]
    tpoly_4_lat = [
        [lat_n[i], lat_im1[i], lat_im1_jm1[i], lat_jm1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_3_lon), tpoly_3_lon[0])
    newp = [
        Polygon(zip(tpoly_4_lon[i], tpoly_4_lat[i]))  # noqa B905
        for i in range(numcells)
    ]
    p4 = [p.centroid for p in newp]

    lon_point_list = [[p1[i].x, p2[i].x, p3[i].x, p4[i].x] for i in range(numcells)]
    lat_point_list = [[p1[i].y, p2[i].y, p3[i].y, p4[i].y] for i in range(numcells)]

    poly = [
        Polygon(zip(lon_point_list[i], lat_point_list[i]))  # noqa B905
        for i in range(numcells)
    ]

    df = pd.DataFrame({"i_index": i_index, "j_index": j_index})
    # tpoly_1 = [Polygon(x) for x in newp]
    # p1 = tpoly_1.centroid
    return gpd.GeoDataFrame(df, index=index, geometry=poly, crs=in_crs)


def build_subset(
    bounds: npt.NDArray[np.double],
    xname: str,
    yname: str,
    tname: str,
    toptobottom: bool,
    date_min: str,
    date_max: Optional[str] = None,
) -> Dict[str, object]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        bounds (np.ndarray): _description_
        xname (str): _description_
        yname (str): _description_
        tname (str): _description_
        toptobottom (bool): _description_
        date_min (str): _description_
        date_max (Optional[str], optional): _description_. Defaults to None.

    Returns:
        dict: _description_
    """
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]
    if not toptobottom:
        return (
            {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
                tname: date_min,
            }
            if date_max is None
            else {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
                tname: slice(date_min, date_max),
            }
        )

    elif date_max is None:
        return {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            tname: date_min,
        }

    else:
        return {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            tname: slice(date_min, date_max),
        }


def build_subset_tiff(
    bounds: npt.NDArray[np.double],
    xname: str,
    yname: str,
    toptobottom: bool,
    bname: str,
    band: int,
) -> Dict[str, object]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        bounds (npt.NDArray[np.double]): _description_
        xname (str): _description_
        yname (str): _description_
        toptobottom (bool): _description_
        bname (str): _description_
        band (int): _description_

    Returns:
        Dict[str, object]: _description_
    """
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]
    ss_dict = {}
    ss_dict = (
        {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
            bname: band,
        }
        if toptobottom
        else {
            xname: slice(minx, maxx),
            yname: slice(maxy, miny),
            bname: band,
        }
    )

    return ss_dict


def build_subset_tiff_da(
    bounds: npt.NDArray[np.double],
    xname: str,
    yname: str,
    toptobottom: bool,
) -> Dict[str, object]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        bounds (npt.NDArray[np.double]): _description_
        xname (str): _description_
        yname (str): _description_
        toptobottom (bool): _description_

    Returns:
        Dict[str, object]: _description_
    """
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]
    ss_dict = {}
    ss_dict = (
        {
            xname: slice(minx, maxx),
            yname: slice(miny, maxy),
        }
        if toptobottom
        else {
            xname: slice(minx, maxx),
            yname: slice(maxy, miny),
        }
    )

    return ss_dict


def get_data_subset_catalog(
    cat_params: CatParams,
    cat_grid: CatGrids,
    shp_file: Union[str, gpd.GeoDataFrame],
    begin_date: str,
    end_date: str,
) -> xr.DataArray:
    """Get xarray subset data.

    Args:
        cat_params (CatParams): _description_
        cat_grid (CatGrids): _description_
        shp_file (Union[str, gpd.GeoDataFrame]): _description_
        begin_date (str): _description_
        end_date (str): _description_

    Returns:
        xr.DataArray: _description_
    """
    # run check on intersection of shape features and gridded data
    gdf = _read_shp_file(shp_file)
    is_intersect, is_degrees, is_0_360 = _check_for_intersection(
        cat_params=cat_params, cat_grid=cat_grid, gdf=gdf
    )

    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf, gdf_bounds = _get_shp_file(
        shp_file=gdf, cat_grid=cat_grid, is_degrees=is_degrees
    )

    rotate_ds = bool((not is_intersect) & is_degrees & (not is_0_360))
    return _get_data_via_catalog(
        cat_params=cat_params,
        cat_grid=cat_grid,
        bounds=gdf_bounds,
        begin_date=begin_date,
        end_date=end_date,
        rotate_lon=rotate_ds,
    )
