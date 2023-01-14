"""Command line script for filling missing data in file."""
import sys
from pathlib import Path
from typing import Optional

import geopandas as gpd
import pandas as pd
import xarray

from gdptools.utils import _get_default_val


def fill_onhm_ncf(  # noqa:C901
    nfile: str,
    output_dir: str,
    var: str,
    lat: str,
    lon: str,
    feature_id: str,
    mfile: str,
    genmap: Optional[bool] = False,
) -> None:
    """Function uses nearest-neighbor, to fill missing feature values.

    Args:
        nfile (str): _description_
        output_dir (str): _description_
        var (str): _description_
        lat (str): _description_
        lon (str): _description_
        feature_id (str): _description_
        mfile (str): _description_
        genmap (Optional[bool], optional): _description_. Defaults to False.
    """
    odir = Path(output_dir)
    if not odir.exists():
        print(f"Path: {odir} does not exist")
        exit
    data = xarray.open_dataset(nfile, engine="netcdf4")  # type: ignore

    if var not in list(data.keys()):
        print(f"Error: {var} not in dataset")
        exit
    try:
        dfval = _get_default_val(data.var.dtype)
    except TypeError as e:
        print(e)
    if genmap:
        # create geodatafrom from masked data of missing values
        data_1d = data.isel(time=[0])
        df_mask = data_1d.where(data_1d >= dfval, drop=True)
        if df_mask.dims.get("nhru") == 0:
            sys.exit("No missing data - exiting")
        tmax_m_vals = df_mask[var].values[0, :]
        lon_m = df_mask[lon].values[:]
        lat_m = df_mask[lat].values[:]
        hruid_m = df_mask[feature_id].values
        df_m = pd.DataFrame(
            {"featid": hruid_m, "lon": lon_m, "lat": lat_m, "tmax": tmax_m_vals}
        )
        gdf_m = gpd.GeoDataFrame(df_m, geometry=gpd.points_from_xy(df_m.lon, df_m.lat))

        # create geodatafrom from non-missing data
        df_filled = data_1d.where(data.tmax < dfval, drop=True)
        tmax_f_vals = df_filled[var].values[0, :]
        lon_f = df_filled[lon].values[:]
        lat_f = df_filled[lat].values[:]
        hruid_f = df_filled[feature_id].values
        df_f = pd.DataFrame(
            {"featid": hruid_f, "lon": lon_f, "lat": lat_f, "tmax": tmax_f_vals}
        )
        gdf_f = gpd.GeoDataFrame(df_f, geometry=gpd.points_from_xy(df_f.lon, df_f.lat))

        # use spatial-join to find nearest filled data for each missing hru-id
        nearest_m = gdf_m.sjoin_nearest(gdf_f, distance_col="distance")

        # print(nearest_m.head())
        nearest_m.drop(
            ["lon_left", "lat_left", "lon_right", "lat_right"], axis=1
        ).to_csv(odir / "fill_missing_nearest.csv")
    else:
        nearest_m = pd.read_csv(mfile)

    miss_index = nearest_m.featid_left.values
    fill_index = nearest_m.featid_right.values

    # fill missing values
    for dvar in data.data_vars:
        if dvar != "crs":
            print(f"processing {dvar}")
            data["tmax"].loc[dict(nhru=miss_index)] = (
                data["tmax"].loc[dict(nhru=fill_index)].values
            )

    oldfile = Path(nfile)
    newfile = oldfile.parent / f"{oldfile.name[:-3]}_filled.nc"

    # write new netcdf file with _filled appended to existing filename
    encoding = {}
    encoding_keys = "_FillValue"
    for data_var in data.data_vars:
        encoding[data_var] = {
            key: value
            for key, value in data[data_var].encoding.items()
            if key in encoding_keys
        }
        encoding[data_var].update(zlib=True, complevel=2)

    for data_var in data.coords:
        encoding[data_var] = {
            key: value
            for key, value in data[data_var].encoding.items()
            if key in encoding_keys
        }
        encoding[data_var].update(_FillValue=None, zlib=True, complevel=2)
    print(encoding)
    data.to_netcdf(path=newfile, encoding=encoding)
