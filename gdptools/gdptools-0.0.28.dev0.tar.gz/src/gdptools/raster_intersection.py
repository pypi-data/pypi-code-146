"""kernal functions for poly-to-poly area-weighted mapping."""
import copy
import logging
import multiprocessing
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

import geopandas as gpd
import numpy as np
import pandas as pd
from pygeos import GEOSException

from .gdp_data_class import TiffAttributes
from .helpers import build_subset_tiff
from .utils import _get_crs
from .utils import _get_print_on
from .utils import _get_shp_bounds_w_buffer
from .utils import _quadrat_cut_geometry

logger = logging.getLogger(__name__)


def tiff_intersection(
    data: TiffAttributes,
    gdf: gpd.GeoDataFrame,
    poly_idx: str,
    wght_gen_proj: Any,
) -> gpd.GeoDataFrame:
    """Tiff intersection.

    Args:
        data (TiffAttributes): _description_
        gdf (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        wght_gen_proj (Any): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    feat_bounds = _get_shp_bounds_w_buffer(
        gdf=gdf, ds=data.ds, crs=data.crs, lon=data.xname, lat=data.yname
    )

    subset_dict = build_subset_tiff(
        bounds=feat_bounds,
        xname=data.xname,
        yname=data.yname,
        toptobottom=data.toptobottom,
        bname=data.bname,
        band=data.band,
    )
    ds_ss = data.ds.sel(**subset_dict).rio.interpolate_na()
    lon, lat = np.meshgrid(ds_ss[data.xname].values, ds_ss[data.yname].values)
    lat_flat = lat.flatten()
    lon_flat = lon.flatten()
    df_points = pd.DataFrame(
        {"index": np.arange(len(lat_flat)), "lat": lat_flat, "lon": lon_flat}
    )
    dm_pnt_gdf = gpd.GeoDataFrame(
        df_points, geometry=gpd.points_from_xy(df_points.lon, df_points.lat)
    )
    dm_pnt_gdf.set_crs(data.crs, inplace=True)
    wproj = _get_crs(wght_gen_proj)
    dm_pnt_gdf_wproj = dm_pnt_gdf.to_crs(wproj)
    gdf_wproj = gdf.to_crs(wproj)

    # pintersect = gpd.sjoin(dm_pnt_gdf_wproj, gdf_wproj, op='within', how='right')
    pintersect = dm_pnt_gdf_wproj.sjoin(gdf_wproj, how="right", predicate="intersects")
    # pintersect_nr = gpd.sjoin_nearest(dm_pnt_gdf_wproj, gdf_wproj, how='right')
    pintersect_nr = dm_pnt_gdf_wproj.sjoin_nearest(gdf_wproj, how="right")

    ds_vals = ds_ss.values.flatten()
    if data.categorical:
        d_categories = list(pd.Categorical(ds_vals).categories)
    num_features = len(gdf.index)
    u_ids = pintersect.groupby(poly_idx, dropna=False)
    u_ids_nr = pintersect_nr.groupby(poly_idx, dropna=False)
    for index in range(num_features):
        feature = gdf.iloc[[index]]
        feature_id = feature[poly_idx].values[0]
        tiff_inds_nr = u_ids_nr.get_group(feature_id).index_left.values
        tiff_inds = u_ids.get_group(feature_id).index_left.values
        if not np.isnan(tiff_inds).any():
            tval = (
                pd.Series(ds_vals[tiff_inds.astype(int)], dtype="category").to_frame()
                if data.categorical
                else pd.Series(ds_vals[tiff_inds.astype(int)]).to_frame()
            )
        else:
            tval = (
                pd.Series(
                    ds_vals[tiff_inds_nr.astype(int)], dtype="category"
                ).to_frame()
                if data.categorical
                else pd.Series(ds_vals[tiff_inds_nr.astype(int)]).to_frame()
            )

        if data.categorical:
            stats = tval.describe(include=["category"]).T
            stats_freq = (
                pd.Categorical(ds_vals[tiff_inds.astype(int)], categories=d_categories)
                .describe()
                .freqs.T
            )
            stats = stats.merge(stats_freq, how="cross")
        else:
            stats = tval.describe().T
        # stats.insert(0, poly_idx, gdf[poly_idx])
        statframe: pd.DataFrame = (
            stats if index == 0 else pd.concat([statframe, stats], axis=0)
        )
    statframe.insert(0, poly_idx, gdf[poly_idx].values)
    statframe.set_index(poly_idx, inplace=True)

    return statframe


def chunks(
    data: TiffAttributes,
    gdf: gpd.GeoDataFrame,
    poly_idx: str,
    wght_gen_proj: Any,
    num_cores: int,
) -> Tuple[TiffAttributes, gpd.GeoDataFrame, str, Any]:
    """Chuck gdf for multiprocessing.

    Args:
        data (TiffAttributes): _description_
        gdf (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        wght_gen_proj (Any): _description_
        num_cores (int): _description_

    Yields:
        Iterator[Tuple[TiffAttributes, gpd.GeoDataFrame, str, Any]]: _description_
    """
    num_features = len(gdf.index)
    for i in range(0, num_features, num_cores):
        yield (
            copy.deepcopy(data),
            gdf.iloc[i : i + num_cores],
            poly_idx,
            wght_gen_proj,
        )


# This doesn't work because I think of collisions when subsetting the xarray.
# TODO: sounds like I need to pass the path to file, and have each process read file.
def p_tiff_intersection_by_feature(
    data: TiffAttributes,
    gdf: gpd.GeoDataFrame,
    poly_idx: str,
    wght_gen_proj: Any,
) -> gpd.GeoDataFrame:
    """Multiprocessing version of tiff_intersection_by_feature.

    Args:
        data (TiffAttributes): _description_
        gdf (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        wght_gen_proj (Any): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    cores = multiprocessing.cpu_count()
    p = multiprocessing.Pool(cores - 1)
    return p.starmap(
        tiff_intersection_by_feature,
        chunks(
            data=data,
            gdf=gdf,
            poly_idx=poly_idx,
            wght_gen_proj=wght_gen_proj,
            num_cores=cores - 1,
        ),
    )


def tiff_intersection_by_feature(
    data: TiffAttributes,
    gdf: gpd.GeoDataFrame,
    poly_idx: str,
) -> pd.DataFrame:
    """Tiff intersection.

    Args:
        data (TiffAttributes): _description_
        gdf (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    num_features = len(gdf.index)
    print_val = _get_print_on(num_features)
    wproj = _get_crs(data.crs)
    gdf_wproj = gdf.to_crs(wproj)
    if data.categorical:
        d_categories = list(pd.Categorical(data.ds.values.flatten()).categories)

    for index in range(num_features):
        if index % print_val == 0:
            print(f"Processing feature: {index}")
        feature = gdf_wproj.iloc[[index]]
        if data.categorical:
            stats = _tiff_get_stat_by_feature_2(
                data=data,
                feature=feature,
                feat_index=index,
                poly_idx=poly_idx,
                d_cats=d_categories,
            )
        else:
            stats = _tiff_get_stat_by_feature_2(
                data=data, feature=feature, feat_index=index, poly_idx=poly_idx
            )
        statframe: pd.DataFrame = (
            stats if index == 0 else pd.concat([statframe, stats], axis=0)
        )
    # statframe.insert(0, poly_idx, gdf_wproj[poly_idx].values)
    statframe.set_index(poly_idx, inplace=True)

    return statframe


def _tiff_get_stat_by_feature(
    data: TiffAttributes,
    feature: gpd.GeoDataFrame,
    poly_idx: str,
    d_cats: Optional[List[object]] = None,
) -> pd.DataFrame:
    """Generate stats per feature.

    Args:
        data (TiffAttributes): _description_
        feature (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        d_cats (Optional[List[object]], optional): _description_. Defaults to None.

    Returns:
        pd.DataFrame: _description_
    """
    feat_bounds = _get_shp_bounds_w_buffer(
        gdf=feature, ds=data.ds, crs=data.crs, lon=data.xname, lat=data.yname
    )

    subset_dict = build_subset_tiff(
        bounds=feat_bounds,
        xname=data.xname,
        yname=data.yname,
        toptobottom=data.toptobottom,
        bname=data.bname,
        band=data.band,
    )
    ds_ss = data.ds.sel(**subset_dict).rio.interpolate_na()
    lon, lat = np.meshgrid(ds_ss[data.xname].values, ds_ss[data.yname].values)
    lat_flat = lat.flatten()
    lon_flat = lon.flatten()
    df_points = pd.DataFrame(
        {"index": np.arange(len(lat_flat)), "lat": lat_flat, "lon": lon_flat}
    )
    dm_pnt_gdf = gpd.GeoDataFrame(
        df_points, geometry=gpd.points_from_xy(df_points.lon, df_points.lat)
    )
    dm_pnt_gdf.set_crs(data.crs, inplace=True)
    dm_pnt_gdf_wproj = dm_pnt_gdf.to_crs(data.crs)

    # pintersect = gpd.sjoin(dm_pnt_gdf_wproj, gdf_wproj, op='within', how='right')
    pintersect = dm_pnt_gdf_wproj.sjoin(feature, how="right", predicate="intersects")
    # pintersect_nr = gpd.sjoin_nearest(dm_pnt_gdf_wproj, gdf_wproj, how='right')
    pintersect_nr = dm_pnt_gdf_wproj.sjoin_nearest(feature, how="right")

    ds_vals = ds_ss.values.flatten()

    u_ids = pintersect.groupby(poly_idx, dropna=False)
    u_ids_nr = pintersect_nr.groupby(poly_idx, dropna=False)

    feature_id = feature[poly_idx].values[0]
    tiff_inds_nr = u_ids_nr.get_group(feature_id).index_left.values
    tiff_inds = u_ids.get_group(feature_id).index_left.values
    if not np.isnan(tiff_inds).any():
        tval = (
            pd.Series(ds_vals[tiff_inds.astype(int)], dtype="category").to_frame()
            if data.categorical
            else pd.Series(ds_vals[tiff_inds.astype(int)]).to_frame()
        )
    else:
        tval = (
            pd.Series(ds_vals[tiff_inds_nr.astype(int)], dtype="category").to_frame()
            if data.categorical
            else pd.Series(ds_vals[tiff_inds_nr.astype(int)]).to_frame()
        )
    # elif data.categorical:
    #     tval = pd.Series(ds_vals[tiff_inds_nr.astype(int)], dtype="category").to_frame()
    # else:
    #     tval = pd.Series(ds_vals[tiff_inds_nr.astype(int)]).to_frame()
    if data.categorical:
        stats = tval.describe(include=["category"]).T
        if not np.isnan(tiff_inds).any():
            stats_freq = (
                pd.Categorical(ds_vals[tiff_inds.astype(int)], categories=d_cats)
                .describe()
                .T
            )
        else:
            stats_freq = (
                pd.Categorical(ds_vals[tiff_inds_nr.astype(int)], categories=d_cats)
                .describe()
                .T
            )
        stats = stats.merge(stats_freq.iloc[[1]], how="cross")
    else:
        stats = tval.describe().T
    stats.insert(0, poly_idx, feature[poly_idx].values[0])
    return stats


def _tiff_get_stat_by_feature_2(  # noqa:C901
    data: TiffAttributes,
    feature: gpd.GeoDataFrame,
    feat_index: int,
    poly_idx: str,
    d_cats: Optional[List[object]] = None,
) -> pd.DataFrame:
    """Generate stats per feature.

    Args:
        data (TiffAttributes): _description_
        feature (gpd.GeoDataFrame): _description_
        feat_index (int): _description_
        poly_idx (str): _description_
        d_cats (Optional[List[object]], optional): _description_. Defaults to None.

    Returns:
        pd.DataFrame: _description_
    """
    feat_bounds = _get_shp_bounds_w_buffer(
        gdf=feature, ds=data.ds, crs=data.crs, lon=data.xname, lat=data.yname
    )

    subset_dict = build_subset_tiff(
        bounds=feat_bounds,
        xname=data.xname,
        yname=data.yname,
        toptobottom=data.toptobottom,
        bname=data.bname,
        band=data.band,
    )
    ds_ss = data.ds.sel(**subset_dict).rio.interpolate_na()
    lon, lat = np.meshgrid(ds_ss[data.xname].values, ds_ss[data.yname].values)
    lat_flat = lat.flatten()
    lon_flat = lon.flatten()
    df_points = pd.DataFrame(
        {"index": np.arange(len(lat_flat)), "lat": lat_flat, "lon": lon_flat}
    )
    dm_pnt_gdf = gpd.GeoDataFrame(
        df_points, geometry=gpd.points_from_xy(df_points.lon, df_points.lat)
    )
    dm_pnt_gdf.set_crs(data.crs, inplace=True)
    dm_pnt_gdf_wproj = dm_pnt_gdf.to_crs(data.crs)
    dx, dy = data.ds.rio.resolution()
    multipoly = _quadrat_cut_geometry(
        feature["geometry"][feat_index], np.mean([abs(dx), abs(dy)]) * 50.0
    )
    spatial_index = dm_pnt_gdf_wproj.sindex
    ds_vals = ds_ss.values.flatten()
    geoms = set()
    for spindex, poly in enumerate(multipoly.geoms):
        try:
            possible_matches_index = list(spatial_index.intersection(poly.bounds))
        except AttributeError:
            print(
                f"User feature Attribute error index: {feat_index} \
                    subpoly_index: {spindex} has an error"
            )

        if possible_matches_index:
            possible_matches = dm_pnt_gdf_wproj.iloc[possible_matches_index]
            try:
                precise_matches = possible_matches[possible_matches.intersects(poly)]
            except GEOSException:
                print(
                    f"User feature GEOSException error: index={feat_index}, \
                    sub_poly={spindex}"
                )
            except TypeError:
                print(
                    f"User feature Type error: index={feat_index}, \
                    sub_poly={spindex}"
                )
            geoms.update(precise_matches.index)

    if list(geoms):
        tval = (
            pd.Series(ds_vals[list(geoms)], dtype="category").to_frame()
            if data.categorical
            else pd.Series(ds_vals[list(geoms)]).to_frame()
        )
    else:
        nrpnt = spatial_index.nearest(feature["geometry"].centroid, return_all=False)
        tval = (
            pd.Series(ds_vals[nrpnt[1, :]], dtype="category").to_frame()
            if data.categorical
            else pd.Series(ds_vals[nrpnt[1, :]]).to_frame()
        )

    if data.categorical:
        stats = tval.describe(include=["category"]).T
        if not np.isnan(list(geoms)).any():
            stats_freq = (
                pd.Categorical(ds_vals[list(geoms)], categories=d_cats).describe().T
            )
        else:
            stats_freq = (
                pd.Categorical(ds_vals[nrpnt[1, :]], categories=d_cats).describe().T
            )
        stats = stats.merge(stats_freq.iloc[[1]], how="cross")
    else:
        stats = tval.describe().T
        stats.insert(0, "sum", tval.sum())
    stats.insert(0, poly_idx, feature[poly_idx].values[0])
    return stats


def tiff_intersection_by_feature_2(
    data: TiffAttributes,
    gdf: gpd.GeoDataFrame,
    poly_idx: str,
) -> gpd.GeoDataFrame:
    """Tiff intersection.

    Args:
        data (TiffAttributes): _description_
        gdf (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    num_features = len(gdf.index)
    print_val = _get_print_on(num_features)
    wproj = _get_crs(data.crs)
    gdf_wproj = gdf.to_crs(wproj)
    if data.categorical:
        d_categories = list(pd.Categorical(data.ds.values.flatten()).categories)

    for index in range(num_features):
        if index % print_val == 0:
            print(f"Processing feature: {index}")
        feature = gdf_wproj.iloc[[index]]
        if data.categorical:
            stats = _tiff_get_stat_by_feature(
                data=data,
                feature=feature,
                poly_idx=poly_idx,
                d_cats=d_categories,
            )
        else:
            stats = _tiff_get_stat_by_feature(
                data=data,
                feature=feature,
                feat_index=index,
                poly_idx=poly_idx,
                wproj=wproj,
            )
        statframe: pd.DataFrame = (
            stats if index == 0 else pd.concat([statframe, stats], axis=0)
        )
    # statframe.insert(0, poly_idx, gdf_wproj[poly_idx].values)
    statframe.set_index(poly_idx, inplace=True)

    return statframe
