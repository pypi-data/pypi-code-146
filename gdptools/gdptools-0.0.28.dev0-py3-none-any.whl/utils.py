"""Ancillary function to support core functions in helper.py."""
from __future__ import annotations

import json
import logging
import re
import sys
import time
import warnings
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

import geopandas as gpd
import netCDF4
import numpy as np
import numpy.typing as npt
import pandas as pd
import shapely
import xarray as xr
from pyproj import CRS
from shapely.geometry import box
from shapely.geometry import LineString
from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon
from shapely.ops import split

from gdptools.data.odap_cat_data import CatGrids
from gdptools.data.odap_cat_data import CatParams


logger = logging.getLogger(__name__)


def _get_grid_cell_sindex(grid_cells):
    start = time.perf_counter()
    spatial_index = grid_cells.sindex
    # print(type(spatial_index))
    end = time.perf_counter()
    print(f"Spatial index generations finished in {round(end-start, 2)} second(s)")
    return spatial_index


def _reproject_for_weight_calc(poly, grid_cells, grid_out_crs, wght_gen_crs):
    start = time.perf_counter()
    # grid_cells.set_crs(grid_in_crs, inplace=True)
    grid_cells.to_crs(grid_out_crs, inplace=True)
    poly.to_crs(grid_out_crs, inplace=True)
    end = time.perf_counter()
    print(
        f"Reprojecting to epsg:{wght_gen_crs} finished in {round(end-start, 2)}"
        " second(s)"
    )
    return poly, grid_cells


def _check_grid_cell_crs(grid_cells):
    if not grid_cells.crs:
        error_string = f"grid_cells don't contain a valid crs: {grid_cells.crs}"
        raise ValueError(error_string)


def _check_feature_crs(poly):
    if not poly.crs:
        error_string = f"polygons don't contain a valid crs: {poly.crs}"
        raise ValueError(error_string)


def _check_poly_idx(poly, poly_idx):
    if poly_idx not in poly.columns:
        error_string = (
            f"Error: poly_idx ({poly_idx}) is not found in the poly ({poly.columns})"
        )
        raise ValueError(error_string)


def _get_print_on(numrows: int) -> int:
    """Return an interval to print progress of run_weights() function.

    Args:
        numrows (int): Number of rows: as in number of polygons

    Returns:
        int: Reasonable interval to print progress statements. Prints at about 10%
    """
    if numrows <= 10:  # pragma: no cover
        print_on = 1
    elif numrows <= 100:
        print_on = 10
    elif numrows <= 1000:
        print_on = 100
    elif numrows <= 10000:
        print_on = 1000
    elif numrows <= 100000:
        print_on = 10000
    else:
        print_on = 50000
    return int(print_on)


def _get_crs(crs_in: Any) -> CRS:
    """Return pyproj.CRS given integer or string.

    Args:
        crs_in (Any): integer: epsg code or pyproj string

    Returns:
        CRS: pyproj.CRS
    """
    # if type(crs_in) == int:
    #     in_crs = CRS.from_epsg(crs_in)
    # elif type(crs_in) == str:
    #     in_crs = CRS.from_proj4(crs_in)
    return CRS.from_user_input(crs_in)


def _get_cells_poly(  # noqa
    xr_a: Union[xr.Dataset, xr.DataArray],
    x: str,
    y: str,
    crs_in: Any,
    verbose: Optional[bool] = False,
) -> gpd.GeoDataFrame:
    """Get cell polygons associated with "nodes" in xarray gridded data.

    Args:
        xr_a (Union[xr.Dataset, xr.DataArray]): _description_
        x (str): _description_
        y (str): _description_
        crs_in (Any): _description_
        verbose (Optional[bool], optional): _description_. Defaults to False.

    Returns:
        gpd.GeoDataFrame: _description_
    """
    tlon = xr_a[x]
    tlat = xr_a[y]
    in_crs = _get_crs(crs_in)
    # if type(crs_in) == int:
    #     in_crs = CRS.from_epsg(crs_in)
    # elif type(crs_in) == str:
    #     in_crs = CRS.from_proj4(crs_in)

    # out_crs = _get_crs(4326)
    lon, lat = np.meshgrid(tlon, tlat)
    poly = []
    if verbose:
        logger.info("calculating surrounding cell vertices")
    start = time.perf_counter()
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
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating surrounding cell vertices in {round(end-start, 2)} second(s)"
        )

    # print(len(lon_n), len(lat_n), type(lon_n), np.shape(lon_n))
    numcells = len(lon_n)
    index = np.array(range(numcells))
    i_index = np.empty(numcells)
    j_index = np.empty(numcells)
    count = 0
    for i in range(1, lon.shape[0] - 1):
        for j in range(1, lon.shape[1] - 1):
            i_index[count] = i
            j_index[count] = j
            count += 1

    if verbose:
        logger.info("calculating cell 1 centroids")
    start = time.perf_counter()
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
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 1 centroids in {round(end-start, 2)} second(s)"
        )
    del tpoly_1_lat, tpoly_1_lon

    if verbose:
        logger.info("calculating cell 2 centroids")
    start = time.perf_counter()
    tpoly_2_lon = [
        [lon_n[i], lon_ip1[i], lon_ip1_jp1[i], lon_jp1[i]] for i in range(numcells)
    ]
    tpoly_2_lat = [
        [lat_n[i], lat_ip1[i], lat_ip1_jp1[i], lat_jp1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_2_lon), tpoly_2_lon[0])
    newp = [
        Polygon(zip(tpoly_2_lon[i], tpoly_2_lat[i]))  # noqa B905
        for i in range(numcells)
    ]
    p2 = [p.centroid for p in newp]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 2 centroids in {round(end-start, 2)} second(s)"
        )

    del tpoly_2_lat, tpoly_2_lon, newp

    if verbose:
        logger.info("calculating cell 3 centroids")
    start = time.perf_counter()
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
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 3 centroids in {round(end-start, 2)} second(s)"
        )

    del tpoly_3_lat, tpoly_3_lon, newp

    if verbose:
        logger.info("calculating cell 4 centroids")
    start = time.perf_counter()
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
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 4 centroids in {round(end-start, 2)} second(s)"
        )

    del tpoly_4_lat, tpoly_4_lon, newp
    del (
        lon_n,
        lon_jm1,
        lon_ip1_jm1,
        lon_ip1,
        lon_ip1_jp1,
        lon_jp1,
        lon_im1_jp1,
        lon_im1,
        lon_im1_jm1,
    )
    del (
        lat_n,
        lat_jm1,
        lat_ip1_jm1,
        lat_ip1,
        lat_ip1_jp1,
        lat_jp1,
        lat_im1_jp1,
        lat_im1,
        lat_im1_jm1,
    )

    if verbose:
        logger.info("creating bounding polygons")
    start = time.perf_counter()
    lon_point_list = [[p1[i].x, p2[i].x, p3[i].x, p4[i].x] for i in range(numcells)]
    lat_point_list = [[p1[i].y, p2[i].y, p3[i].y, p4[i].y] for i in range(numcells)]
    poly = [
        Polygon(zip(lon_point_list[i], lat_point_list[i]))  # noqa B905
        for i in range(numcells)
    ]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished creating bounding polygons in {round(end-start, 2)} second(s)"
        )

    if verbose:
        logger.info("reprojecting cells")
    start = time.perf_counter()
    # grd_shp = xr_a[var].values.shape
    df = pd.DataFrame({"i_index": i_index, "j_index": j_index})
    gmcells = gpd.GeoDataFrame(df, index=index, geometry=poly, crs=in_crs)
    # gmcells.to_crs(crs=out_crs, inplace=True)
    end = time.perf_counter()
    if verbose:
        logger.info(f"finished reprojecting cells in {round(end-start, 2)} second(s)")

    return gmcells


def _build_subset_cat(
    cat_params: CatParams,
    cat_grid: CatGrids,
    bounds: npt.NDArray[np.double],
    date_min: str,
    date_max: Optional[str] = None,
) -> Dict[Any, Any]:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        cat_params (CatParams): _description_
        cat_grid (CatGrids): _description_
        bounds (npt.NDArray[np.double]): _description_
        date_min (str): _description_
        date_max (str, optional): _description_. Defaults to None.

    Returns:
        dict: _description_
    """
    xname = cat_grid.X_name
    yname = cat_grid.Y_name
    # print(type(xname), type(yname))
    tname = cat_params.T_name
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]
    gridorder = bool(cat_grid.toptobottom)
    if not gridorder:
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


def _read_shp_file(shp_file: Union[str, Path, gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
    """Read shapefile.

    Args:
        shp_file (Union[str, gpd.GeoDataFrame]): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    if not isinstance(shp_file, gpd.GeoDataFrame):
        return gpd.read_file(shp_file)
    else:
        return shp_file


def _get_shp_file(
    shp_file: gpd.GeoDataFrame, cat_grid: CatGrids, is_degrees: bool
) -> Tuple[gpd.GeoDataFrame, npt.NDArray[np.double]]:
    """Return GeoDataFrame and bounds of shapefile.

    Args:
        shp_file (gpd.GeoDataFrame): _description_
        cat_grid (CatGrids): _description_
        is_degrees (bool): _description_

    Returns:
        Union[gpd.GeoDataFrame, npt.NDArray[np.double]y]: _description_
    """
    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf = shp_file.to_crs(cat_grid.proj)
    # buffer polygons bounding box by twice max resolution of grid
    bbox = box(*gdf.total_bounds)
    gdf_bounds = bbox.buffer(2 * max(cat_grid.resX, cat_grid.resY)).bounds
    if is_degrees and (gdf_bounds[0] < -180.0) & (gdf_bounds[2] > 180.0):
        newxmax = 180 - (abs(gdf_bounds[0]) - 180.0)
        newxmin = -180.0 + (abs(gdf_bounds[2]) - 180.0)
        gdf_bounds = (newxmin, gdf_bounds[1], newxmax, gdf_bounds[3])
        print("Warning: The feature data crosses the anitmeridian.")

    # TODO: need to rethink buffer - leaving it out for now
    # gdf_bounds = gdf.total_bounds.buffer(2.0*buffer)
    return gdf, gdf_bounds


def _is_degrees(ds: xr.Dataset, cat_grid: CatGrids) -> bool:
    """Test if degrees in attributes on longitude.

    Args:
        ds (xr.Dataset): _description_
        cat_grid (CatGrids): _description_

    Returns:
        bool: _description_
    """
    xvals = ds[cat_grid.X_name]
    t_attr = xvals.attrs
    units = t_attr.get("units")
    return bool(re.search("degrees", units, flags=re.IGNORECASE))


def _is_degrees_nc(ds: xr.Dataset, x_name: str) -> bool:
    """Test if degrees in attributes on longitude.

    Args:
        ds (xr.Dataset): _description_
        x_name (str): _description_

    Returns:
        bool: _description_
    """
    xvals = ds[x_name]
    t_attr = xvals.attrs
    try:
        units = t_attr.get("units")
    except KeyError:
        tkey = "units"
        print(
            f" Error: key- {tkey} not found in coordinates of xarray"
            "dataset - make sure the coordinates of the dataset include"
            "a unit attribute per cf-conventions"
        )

    return bool(re.search("degrees", units, flags=re.IGNORECASE))


def _is_lon_0_360(vals: npt.NDArray[np.double]) -> bool:
    """Test if longitude spans 0-360.

    Args:
        vals (npt.NDArray[np.double]): _description_

    Returns:
        bool: _description_
    """
    result = False
    if (vals[0] > 180.0) & (np.min(vals) > 0.0):
        result = False
    elif (np.max(vals) > 180.0) & (np.min(vals) > 180.0):
        result = False
    elif np.max(vals) > 180.0:
        result = True

    return result


def _get_shp_bounds_w_buffer(
    gdf: gpd.GeoDataFrame, ds: xr.Dataset, crs: Any, lon: str, lat: str
) -> npt.NDArray[np.double]:
    """Return bounding box based on 2 * max(ds.dx, ds.dy).

    Args:
        gdf (gpd.GeoDataFrame): _description_
        ds (xr.Dataset): _description_
        crs (Any): _description_
        lon (str): _description_
        lat (str): _description_

    Returns:
        tuple: _description_
    """
    bbox = box(*gdf.to_crs(crs).total_bounds)
    return np.asarray(
        bbox.buffer(
            2 * max(max(np.diff(ds[lat].values)), max(np.diff(ds[lon].values)))
        ).bounds
    )


def _check_for_intersection(
    cat_params: CatParams,
    cat_grid: CatGrids,
    gdf: gpd.GeoDataFrame,
) -> Tuple[bool, bool, bool]:
    """Check broadly for intersection between features and grid.

    Args:
        cat_params (CatParams): _description_
        cat_grid (CatGrids): _description_
        gdf (gpd.GeoDataFrame): _description_

    Returns:
        Tuple[bool, bool, bool]: _description_
    """
    is_degrees = False
    is_intersect = True
    is_0_360 = False
    ds_url = cat_params.URL
    ds = xr.open_dataset(
        ds_url + "#fillmismatch", decode_coords=True, chunks={}
    )  # type:ignore
    xvals = ds[cat_grid.X_name]
    yvals = ds[cat_grid.Y_name]
    minx = xvals.values.min()
    maxx = xvals.values.max()
    miny = yvals.values.min()
    maxy = yvals.values.max()
    ds_bbox = box(minx, miny, maxx, maxy)
    bounds = _get_shp_bounds_w_buffer(
        gdf,
        ds,
        cat_grid.proj,
        cat_grid.X_name,
        cat_grid.Y_name,
    )
    is_degrees = _is_degrees(ds=ds, cat_grid=cat_grid)
    if is_degrees & (not ds_bbox.intersects(box(*np.asarray(bounds).tolist()))):
        is_intersect = False
        is_0_360 = _is_lon_0_360(xvals.values)
        if is_0_360:
            warning_string = (
                "0-360 longitude crossing the international date line encountered.\n"
                "Longitude coordinates will be 0-360 in output."
            )
            warnings.warn(warning_string)

    return is_intersect, is_degrees, is_0_360


def _check_for_intersection_nc(
    ds: xr.Dataset,
    x_name: str,
    y_name: str,
    proj: Any,
    gdf: gpd.GeoDataFrame,
) -> Tuple[bool, bool, bool]:
    """Check broadly for intersection between features and grid.

    Args:
        ds (xr.Dataset): _description_
        x_name (str): _description_
        y_name (str): _description_
        proj (Any): _description_
        gdf (gpd.GeoDataFrame): _description_

    Returns:
        Tuple[bool, bool, bool]: _description_
    """
    is_degrees = False
    is_intersect = True
    is_0_360 = False

    xvals = ds[x_name]
    yvals = ds[y_name]
    minx = xvals.values.min()
    maxx = xvals.values.max()
    miny = yvals.values.min()
    maxy = yvals.values.max()
    ds_bbox = box(minx, miny, maxx, maxy)
    bounds = _get_shp_bounds_w_buffer(
        gdf,
        ds,
        proj,
        x_name,
        y_name,
    )
    is_degrees = _is_degrees_nc(ds=ds, x_name=x_name)
    if is_degrees & (not ds_bbox.intersects(box(*np.asarray(bounds).tolist()))):
        is_intersect = False
        is_0_360 = _is_lon_0_360(xvals.values)
        if is_0_360:
            warning_string = (
                "0-360 longitude crossing the international date line encountered.\n"
                "Longitude coordinates will be 0-360 in output."
            )
            warnings.warn(warning_string)

    return is_intersect, is_degrees, is_0_360


def _get_data_via_catalog(
    cat_params: CatParams,
    cat_grid: CatGrids,
    bounds: npt.NDArray[np.double],
    begin_date: str,
    end_date: Optional[str] = None,
    rotate_lon: Optional[bool] = False,
) -> xr.DataArray:
    """Get xarray spatial and temporal subset.

    Args:
        cat_params (CatParams): _description_
        cat_grid (CatGrids): _description_
        bounds (np.ndarray): _description_
        begin_date (str): _description_
        end_date (Optional[str], optional): _description_. Defaults to None.
        rotate_lon (Optional[bool], optional): _description_. Defaults to False.

    Returns:
        xr.DataArray: _description_
    """
    ds_url = cat_params.URL
    ds = xr.open_dataset(
        ds_url + "#fillmismatch", decode_coords=True, chunks={}
    )  # type:ignore
    if rotate_lon:
        lon = cat_grid.X_name
        ds.coords[lon] = (ds.coords["lon"] + 180) % 360 - 180
        ds = ds.sortby(ds[lon])

    # get grid data subset to polygons buffered bounding box
    ss_dict = _build_subset_cat(cat_params, cat_grid, bounds, begin_date, end_date)
    # gridMET requires the '#fillmismatch' see:
    # https://discourse.oceanobservatories.org/
    # t/
    # accessing-data-on-thredds-opendap-via-python-netcdf4-or-xarray
    # -dealing-with-fillvalue-type-mismatch-error/61

    varname = cat_params.varname
    return ds[varname].sel(**ss_dict)  # type: ignore


def _get_wieght_df(wght_file: Union[str, pd.DataFrame], poly_idx: str) -> pd.DataFrame:
    if isinstance(wght_file, pd.DataFrame):
        # wghts = wght_file.copy()
        wghts = wght_file.astype({"i": int, "j": int, "wght": float, poly_idx: str})
    elif isinstance(wght_file, str):
        wghts = pd.read_csv(
            wght_file, dtype={"i": int, "j": int, "wght": float, poly_idx: str}
        )
    else:
        sys.exit("wght_file must be one of string or pandas.DataFrame")
    return wghts


def _date_range(p_start: str, p_end: str, intv: int) -> Iterator[str]:
    """Return a date range.

    Args:
        p_start (str): _description_
        p_end (str): _description_
        intv (int): _description_

    Yields:
        Iterator[str]: _description_
    """
    start = datetime.strptime(p_start, "%Y-%m-%d")
    end = datetime.strptime(p_end, "%Y-%m-%d")
    diff = (end - start) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%Y-%m-%d")
    yield end.strftime("%Y-%m-%d")


def _get_catalog_time_increment(param: dict) -> Tuple[int, str]:
    interval = param.get("interval").split(" ")
    return int(interval[0]), str(interval[1])


def _get_dataframe(object: Union[str, pd.DataFrame]) -> pd.DataFrame:
    if isinstance(object, str):
        return pd.DataFrame.from_dict(json.loads(object))
    else:
        return object


# this function is copied from here:
# https://github.com/gboeing/osmnx/blob/main/osmnx/utils_geo.py
# if it turns out to be helpful in speedin up intersections then I'll import it via
# the package - for now copied in here for development testing.
def _quadrat_cut_geometry(
    geometry: Union[shapely.geometry.Polygon, shapely.geometry.MultiPolygon],
    quadrat_width: float,
    min_num: Optional[int] = 3,
) -> shapely.geometry.MultiPolygon:
    """Split a Polygon or MultiPolygon up into sub-polygons of a specified size.

    Args:
        geometry (Union[shapely.geometry.Polygon, shapely.geometry.MultiPolygon]): _description_
        quadrat_width (float): _description_
        min_num (Optional[int], optional): _description_. Defaults to 3.

    Returns:
        shapely.geometry.MultiPolygon: _description_
    """
    # create n evenly spaced points between the min and max x and y bounds
    west, south, east, north = geometry.bounds
    x_num = int(np.ceil((east - west) / quadrat_width) + 1)
    y_num = int(np.ceil((north - south) / quadrat_width) + 1)
    x_points = np.linspace(west, east, num=max(x_num, min_num))
    y_points = np.linspace(south, north, num=max(y_num, min_num))

    # create a quadrat grid of lines at each of the evenly spaced points
    vertical_lines = [
        LineString([(x, y_points[0]), (x, y_points[-1])]) for x in x_points
    ]
    horizont_lines = [
        LineString([(x_points[0], y), (x_points[-1], y)]) for y in y_points
    ]
    lines = vertical_lines + horizont_lines

    # recursively split the geometry by each quadrat line
    geometries = [geometry]

    for line in lines:
        # split polygon by line if they intersect, otherwise just keep it
        split_geoms = [
            split(g, line).geoms if g.intersects(line) else [g] for g in geometries
        ]
        # now flatten the list and process these split geoms on the next line in
        # the list of lines
        geometries = [g for g_list in split_geoms for g in g_list]

    return MultiPolygon(geometries)


def _get_default_val(native_dtype: np.dtype):
    """Get default fill value based on gridded data dtype.

    Args:
        native_dtype (np.dtype): _description_

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """
    if native_dtype.kind == "i":
        dfval = netCDF4.default_fillvals["i8"]
    elif native_dtype.kind == "f":
        dfval = netCDF4.default_fillvals["f8"]
    else:
        raise TypeError(
            "gdptools currently only supports int and float types."
            f"The value type here is {native_dtype}"
        )

    return dfval


def _get_interp_array(n_geo: int, nts: int, native_dtype: np.dtype, default_val: Any):
    """Get array for interpolation based on the dtype of the gridded data.

    Args:
        n_geo (int): _description_
        nts (int): _description_
        native_dtype (np.dtype): _description_
        default_val (Any): _description_

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """
    if native_dtype.kind == "i":
        # val_interp = np.empty((nts, n_geo), dtype=np.dtype("int64"))
        val_interp = np.full(
            (nts, n_geo), dtype=np.dtype("int64"), fill_value=default_val
        )
    elif native_dtype.kind == "f":
        # val_interp = np.empty((nts, n_geo), dtype=np.dtype("float64"))
        val_interp = np.full(
            (nts, n_geo), dtype=np.dtype("float64"), fill_value=default_val
        )
    else:
        raise TypeError(
            "gdptools currently only supports int and float types."
            f"The value type here is {native_dtype}"
        )

    return val_interp


def _get_top_to_bottom(data: Union[xr.Dataset, xr.DataArray], y_coord: str) -> bool:
    """Get orientation of y-coordinate data in xarray Dataset.

    Args:
        data (xr.Dataset): _description_
        y_coord (str): _description_

    Returns:
        bool: _description_
    """
    yy = data.coords[y_coord].values
    ttb: bool = yy[0] <= yy[-1]
    return ttb
