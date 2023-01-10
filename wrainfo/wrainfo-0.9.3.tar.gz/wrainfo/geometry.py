"""Geometry module."""

# WRaINfo, Is a software to process FURUNO weather radar data.
#
# Copyright (c) 2023, FernLab (GFZ Potsdam, fernlab@gfz-potsdam.de)
#
# This software was developed within the context of the RaINfo ("Potential use of
# high resolution weather data in agriculture") project of FernLab funded by
# the Impulse and Networking Fund of the Helmholtz Association.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# imports
# -------

import wradlib as wrl
import numpy as np
import os
import xarray as xr
from wrainfo.reader import read_config_file


# functions to georeferencing and gridding the Furuno data
# --------------------------------------------------------

def get_target_grid(ds, nb_pixels):
    """Get target grid."""
    xgrid = np.linspace(ds.x.min(), ds.x.max(), nb_pixels, dtype=np.float32)
    ygrid = np.linspace(ds.y.min(), ds.y.max(), nb_pixels, dtype=np.float32)
    grid_xy_raw = np.meshgrid(xgrid, ygrid)
    grid_xy_grid = np.dstack((grid_xy_raw[0], grid_xy_raw[1]))
    return xgrid, ygrid, grid_xy_grid


def get_target_coordinates(grid):
    """Get target coordinates."""
    grid_xy = np.stack((grid[..., 0].ravel(), grid[..., 1].ravel()), axis=-1)
    return grid_xy


def get_source_coordinates(ds):
    """Get source coordinates."""
    xy = np.stack((ds.x.values.ravel(), ds.y.values.ravel()), axis=-1)
    return xy


def create_dataarray(ds, data, moment):
    """Create data array."""
    # get moment attrributes
    mom_attrs = ds[moment].attrs
    # remove _Undetect since it's not in the original data
    mom_attrs.pop("_Undetect", None)
    # create moment DataArray
    mom = xr.DataArray(data.astype(np.float32),
                       dims=["y", "x"],
                       attrs=mom_attrs
                       )
    # fix encoding
    mom.encoding = dict(zlib=True, _FillValue=0., least_significant_digit=2)
    return mom


def create_dataset(ds, moments, xgrid, ygrid):
    """Create xarray dataset."""
    # create x,y DataArrays
    x = xr.DataArray(xgrid, dims=["x"], attrs=dict(standard_name="projection_x_coordinate",
                                                   long_name="x coordinate of projection",
                                                   units="m"))
    y = xr.DataArray(ygrid, dims=["y"], attrs=dict(standard_name="projection_y_coordinate",
                                                   long_name="y coordinate of projection",
                                                   units="m"))
    data_vars = dict()
    data_vars.update(moments)
    data_vars.update({"time": ds.reset_coords().time})

    # create Dataset
    ds_out = xr.Dataset(
        data_vars=data_vars,
        coords={"x": x, "y": y},
    )
    # apply CF Conventions
    ds_out.attrs['Conventions'] = 'CF-1.5'
    return ds_out


# georeferencing and gridding of Furuno data
# ------------------------------------------

def furuno_georeferencing(ds, path):
    """Georeference FURUNO Dataset, Grid/Project moments to raster dataset with EPSG Code.

    Parameters
    ----------
    ds : xarray.Dataset
    moments : list
        list of selected data variables from the dataset
    path : str
        path to configuration file

    Returns
    -------
    : xarray.Dataset
        Georeferenced xarray.Dataset.
    """
    # read configuration file for epsg_code and nb_pixels
    epsg_code = read_config_file(path=path, selection="epsg_code")
    nb_pixels = read_config_file(path=path, selection="nb_pixels")
    moments = read_config_file(path=path, selection="moments_in_processed_files")

    # create projection
    proj = wrl.georef.epsg_to_osr(epsg_code)

    # georeference single sweep
    ds = ds.pipe(wrl.georef.georeference_dataset, proj=proj)

    # get source coordinates
    src = get_source_coordinates(ds)

    # create target grid
    xgrid, ygrid, trg_grid = get_target_grid(ds, nb_pixels)

    # get target coordinates
    trg = get_target_coordinates(trg_grid)

    # setup interpolator
    ip_near = wrl.ipol.Nearest(src, trg)

    # calculate moments, create DataArrays
    moment_dict = dict()
    for mom in moments:
        res = ip_near(ds[mom].values.ravel()).reshape((len(ygrid), len(xgrid)))
        moment_dict[mom] = create_dataarray(ds, res, mom)

    # create output dataset
    ds_out = create_dataset(ds, moment_dict, xgrid, ygrid)

    # write crs (projection) to netcdf_file
    ds_out = ds_out.rio.write_crs(epsg_code, grid_mapping_name="transverse_mercator")
    ds_out.attrs["elevation_angle"] = ds.elevation.values[0]

    # add time dimension
    time1 = [1]
    ds_out = ds_out.expand_dims(time=time1)

    return ds_out


# output as netcdf
# ----------------

def furuno_sweep_to_netcdf(ds,
                           path,
                           data_type=None):
    """Create and save georeferenced NetCDF files.

    Parameter
    ---------
    ds : xarray.Dataset
    path: str
        path to configuration file
    data_type : str
        level of processing (Level1, Level2, or Level3)

    Return
    ------
    : NetCDF files
        NetCDF files in output directory.
    """
    # read configuration file
    radar_location_identifier = read_config_file(path=path, selection="radar_location_identifier")
    outdir = read_config_file(path=path, selection="output_path_processed_files")
    moments = read_config_file(path=path, selection="moments_in_processed_files")

    # choose moments, which will save in the netcdf
    ds = ds[moments]

    # case distinction for extraction of elevation angle
    # use time, elevation, and epsg code to create filename
    if hasattr(ds, "elevation"):
        el = ds.elevation.median().values
        t0 = ds.time.values.astype("M8[s]").astype("O")
    else:
        el = ds.elevation_angle
        t0 = ds.time.values.astype("M8[s]").astype("O")[0]

    if data_type is not None:
        outfilename = f"{radar_location_identifier}_{t0:%Y%m%d}_{t0:%H%M%S}UTC_elev_{el}_{data_type}.nc"
    else:
        outfilename = f"{radar_location_identifier}_{t0:%Y%m%d}_{t0:%H%M%S}UTC_elev_{el}.nc"

    # add time dimension
    if len(ds.dims) == 2:  # noqa E712
        time1 = [1]
        ds = ds.expand_dims(time=time1)

    # extract year, month, day from filename
    year = t0.year
    month = f'{t0.month:02d}'
    day = t0.day

    # create output directory
    path1 = outdir + "/" + str(year) + "/" + str(month) + "/" + str(day) + "/" + "elev_" + str(el)

    # absolute output path
    outfilename = os.path.join(path1, outfilename)

    # output path will create if not exists
    if not os.path.exists(path1):
        os.makedirs(path1, exist_ok=True)

    # check whether output file exists
    if not os.path.isfile(outfilename):
        # output file
        print(f"-- output to {outfilename}")
        ds.to_netcdf(outfilename)

    return True
