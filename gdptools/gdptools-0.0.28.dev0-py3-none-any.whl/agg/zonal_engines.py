"""Engines for calculated zonal stats based on non-area-weighted statistics."""
import os
import time
from abc import ABC
from abc import abstractmethod
from typing import Optional

import geopandas as gpd
import numpy as np
import pandas as pd
from joblib import delayed
from joblib import Parallel
from joblib import parallel_backend

from gdptools.data.agg_gen_data import AggData
from gdptools.data.user_data import UserData
from gdptools.helpers import build_subset_tiff_da
from gdptools.utils import _get_shp_bounds_w_buffer
from gdptools.weights.calc_weight_engines import _make_valid


class ZonalEngine(ABC):
    """Base class for zonal stats engines."""

    def calc_zonal_from_aggdata(
        self, user_data: UserData, categorical: Optional[bool] = False
    ) -> pd.DataFrame:
        """calc_zonal_from_aggdata Template method for calculated zonal stats.

        _extended_summary_

        Args:
            user_data (UserData): _description_
            categorical (Optional[bool], optional): _description_. Defaults to False.

        Returns:
            pd.DataFrame: _description_
        """
        self._user_data = user_data
        self._categorical = categorical

        return self.zonal_stats()

    @abstractmethod
    def zonal_stats(self) -> pd.DataFrame:
        """Abstract method for calculating zonal stats."""
        pass


class ZonalEngineSerial(ZonalEngine):
    """Serial zonal stats engine."""

    def zonal_stats(self) -> pd.DataFrame:
        """zonal_stats Calculate zonal stats serially.

        _extended_summary_

        Returns:
            pd.DataFrame: _description_
        """
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        ds_ss = agg_data.da

        if self._categorical:
            d_categories = list(pd.Categorical(ds_ss.values.flatten()).categories)

        tstrt = time.perf_counter()
        lon, lat = np.meshgrid(
            ds_ss[agg_data.cat_grid.X_name].values,
            ds_ss[agg_data.cat_grid.Y_name].values,
        )
        lat_flat = lat.flatten()
        lon_flat = lon.flatten()
        ds_vals = ds_ss.values.flatten()
        df_points = pd.DataFrame(
            {
                "index": np.arange(len(lat_flat)),
                "vals": ds_vals,
                "lat": lat_flat,
                "lon": lon_flat,
            }
        )
        try:
            fill_val = ds_ss._FillValue
            df_points_filt = df_points[df_points.vals != fill_val]
        except Exception:
            df_points_filt = df_points
        # df_points_filt = df_points[df_points.vals >= ds_min]
        source_df = gpd.GeoDataFrame(
            df_points_filt,
            geometry=gpd.points_from_xy(df_points_filt.lon, df_points_filt.lat),
        )
        tend = time.perf_counter()
        print(f"converted tiff to points in {tend - tstrt:0.4f} seconds")
        source_df.set_crs(agg_data.cat_grid.proj, inplace=True)
        target_df = agg_data.feature.to_crs(agg_data.cat_grid.proj)
        target_df = _make_valid(target_df)
        target_df.reset_index()
        target_df_keys = target_df[agg_data.id_feature].values
        tstrt = time.perf_counter()
        ids_tgt, ids_src = source_df.sindex.query_bulk(
            target_df.geometry, predicate="contains"
        )
        tend = time.perf_counter()
        print(f"overlaps calculated in {tend - tstrt:0.4f} seconds")
        if self._categorical:

            val_series = pd.Categorical(
                source_df["vals"].iloc[ids_src], categories=d_categories
            )

            agg_df = pd.DataFrame(
                {
                    agg_data.id_feature: target_df[agg_data.id_feature]
                    .iloc[ids_tgt]
                    .values
                }
            )
            agg_df["vals"] = val_series
            tstrt = time.perf_counter()
            stats = agg_df.groupby(agg_data.id_feature)["vals"].describe(
                include=["category"]
            )
            tend = time.perf_counter()
            print(f"categorical zonal stats calculated in {tend - tstrt:0.4f} seconds")
        else:
            agg_df = pd.DataFrame(
                {
                    agg_data.id_feature: target_df[agg_data.id_feature]
                    .iloc[ids_tgt]
                    .values,
                    "vals": source_df["vals"].iloc[ids_src],
                }
            )
            tstrt = time.perf_counter()
            stats = agg_df.groupby(agg_data.id_feature)["vals"].describe()
            # stats.insert(-1, "sum", agg_df.groupby(agg_data.id_feature).sum())
            stats["sum"] = agg_df.groupby(agg_data.id_feature).sum()
            # stats.set_index(agg_data.id_feature)
            tend = time.perf_counter()
            print(f"zonal stats calculated in {tend - tstrt:0.4f} seconds")

        tstrt = time.perf_counter()
        stats_inds = stats.index

        missing = np.setdiff1d(target_df_keys, stats_inds)
        target_df_stats = target_df.loc[
            target_df[agg_data.id_feature].isin(list(stats_inds))
        ]
        target_df_missing = target_df.loc[
            target_df[agg_data.id_feature].isin(list(missing))
        ]
        nearest = target_df_stats.sindex.nearest(
            target_df_missing.geometry, return_all=False
        )
        print(nearest)
        print(f"number of missing values: {len(missing)}")
        stats_missing = stats.iloc[nearest[1]]
        stats_missing.index = missing
        stats_tot = pd.concat([stats, stats_missing])
        stats_tot.index.name = agg_data.id_feature
        tend = time.perf_counter()
        print(
            f"fill missing values with nearest neighbors in {tend - tstrt:0.4f} seconds"
        )

        return stats_tot


class ZonalEngineParallel(ZonalEngine):
    """Parallel zonal stats engine."""

    def zonal_stats(self) -> pd.DataFrame:
        """zonal_stats Calculate zonal stats serially.

        _extended_summary_

        Returns:
            pd.DataFrame: _description_
        """
        n_jobs = os.cpu_count() - 1
        # n_jobs = 2
        zvars = self._user_data.get_vars()
        tstrt = time.perf_counter()
        agg_data: AggData = self._user_data.prep_agg_data(zvars[0])
        tend = time.perf_counter()
        print(f"data prepped for zonal in {tend - tstrt:0.4f} seconds")
        ds_ss = agg_data.da

        if self._categorical:
            d_categories = list(pd.Categorical(ds_ss.values.flatten()).categories)
        else:
            d_categories = []

        target_df = agg_data.feature.set_crs(agg_data.cat_grid.proj, inplace=True)
        target_df = _make_valid(target_df)
        # target_df.reset_index(inplace=True)
        target_df_keys = target_df[agg_data.id_feature].values
        to_workers = _chunk_dfs(
            target_df,
            ds_ss,
            agg_data.cat_grid.X_name,
            agg_data.cat_grid.Y_name,
            agg_data.cat_grid.proj,
            agg_data.cat_grid.toptobottom,
            self._categorical,
            agg_data.id_feature,
            d_categories,
            n_jobs=n_jobs,
        )

        tstrt = time.perf_counter()
        worker_out = self.get_stats_parallel(n_jobs, to_workers)
        for i in range(len(worker_out)):
            if i == 0:
                stats = worker_out[i]
                print(type(stats))
            else:
                stats = pd.concat([stats, worker_out[i]])
        stats.set_index(agg_data.id_feature, inplace=True)
        # stats = pd.concat(worker_out)
        tend = time.perf_counter()
        print(f"Parallel calculation of zonal stats in {tend - tstrt:0.04} seconds")

        tstrt = time.perf_counter()
        stats_inds = stats.index

        missing = np.setdiff1d(target_df_keys, stats_inds)
        if len(missing) <= 0:
            return stats
        target_df_stats = target_df.loc[
            target_df[agg_data.id_feature].isin(list(stats_inds))
        ]
        target_df_missing = target_df.loc[
            target_df[agg_data.id_feature].isin(list(missing))
        ]
        nearest = target_df_stats.sindex.nearest(
            target_df_missing.geometry, return_all=False
        )
        print(nearest)
        print(f"number of missing values: {len(missing)}")
        stats_missing = stats.iloc[nearest[1]]
        stats_missing.index = missing
        stats_tot = pd.concat([stats, stats_missing])
        stats_tot.index.name = agg_data.id_feature
        tend = time.perf_counter()
        print(
            f"fill missing values with nearest neighbors in {tend - tstrt:0.4f} seconds"
        )

        return stats_tot

    def get_stats_parallel(self, n_jobs, to_workers):
        """get_stats_parallel -Parallel engine.

        _extended_summary_

        Args:
            n_jobs (int): Number of processors
            to_workers (list): List of chunked dataframe and addtional parameters

        Returns:
            _type_: _description_
        """
        with parallel_backend("loky", inner_max_num_threads=1):
            worker_out = Parallel(n_jobs=n_jobs)(
                delayed(_get_stats_on_chunk)(*chunk_pair) for chunk_pair in to_workers
            )
        return worker_out


def _get_stats_on_chunk(
    geom, df, x_name, y_name, proj, toptobottom, categorical, id_feature, cats
):
    num_features = len(geom.index)
    comp_stats = []
    for index in range(num_features):
        target_df = geom.iloc[[index]]
        feat_bounds = _get_shp_bounds_w_buffer(
            gdf=target_df, ds=df, crs=proj, lon=x_name, lat=y_name
        )

        subset_dict = build_subset_tiff_da(
            bounds=feat_bounds, xname=x_name, yname=y_name, toptobottom=toptobottom
        )
        ds_ss = df.sel(**subset_dict)
        lon, lat = np.meshgrid(
            ds_ss[x_name].values,
            ds_ss[y_name].values,
        )
        lat_flat = lat.flatten()
        lon_flat = lon.flatten()
        ds_vals = ds_ss.values.flatten()
        df_points = pd.DataFrame(
            {
                "index": np.arange(len(lat_flat)),
                "vals": ds_vals,
                "lat": lat_flat,
                "lon": lon_flat,
            }
        )
        try:
            fill_val = ds_ss._FillValue
            df_points = df_points[df_points.vals != fill_val]
        except Exception:
            df_points = df_points

        source_df = gpd.GeoDataFrame(
            df_points,
            geometry=gpd.points_from_xy(df_points.lon, df_points.lat),
            crs=proj,
        )

        ids_src = source_df.sindex.query(
            target_df.geometry.values[0], predicate="contains"
        )
        if categorical:

            val_series = pd.Categorical(
                source_df["vals"].iloc[ids_src], categories=cats
            )

            agg_df = pd.DataFrame(data={"vals": val_series})
            stats = agg_df.describe(include=["category"]).T
        else:
            agg_df = pd.DataFrame(
                data={
                    "vals": source_df["vals"].iloc[ids_src].values,
                },
                # index=[target_df[id_feature].values[0]]
            )
            stats = agg_df.describe().T
            stats["sum"] = agg_df["vals"].sum()

        stats[id_feature] = target_df[id_feature].values[0]
        if stats["count"].values[0] <= 0:
            continue
        comp_stats.append(stats)

    return pd.concat(comp_stats)


def _chunk_dfs(
    geoms_to_chunk, df, x_name, y_name, proj, ttb, categorical, id_feature, cats, n_jobs
):
    """Chunk dataframes for parallel processing."""
    start = 0
    chunk_size = geoms_to_chunk.shape[0] // n_jobs + 1

    # if length < chunk_size:
    #     yield \
    #         geoms_to_chunk[:], \
    #         df, \
    #         x_name, \
    #         y_name, \
    #         proj, \
    #         ttb, \
    #         categorical, \
    #         id_feature, \
    #         cats
    #     return

    # while start + chunk_size <= length:
    #     yield \
    #         geoms_to_chunk[start:(chunk_size + start)], \
    #         df, \
    #         x_name, \
    #         y_name, \
    #         proj, \
    #         ttb, \
    #         categorical, \
    #         id_feature, \
    #         cats
    #     print(start, (chunk_size + start))
    #     start += chunk_size

    # if start < length:
    #     yield \
    #         geoms_to_chunk[start:], \
    #         df, \
    #         x_name, \
    #         y_name, \
    #         proj, \
    #         ttb, \
    #         categorical, \
    #         id_feature, \
    #         cats
    #     print(start)
    #     start += chunk_size
    #     return

    # chunk_size = geoms_to_chunk.shape[0] // n_jobs + 1
    for i in range(n_jobs):
        start = i * chunk_size
        yield geoms_to_chunk.iloc[
            start : start + chunk_size
        ], df, x_name, y_name, proj, ttb, categorical, id_feature, cats
