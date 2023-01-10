"""Process chains module."""

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

import logging
import os
import glob
import xarray as xr
import pathlib
import datetime as dt
import numpy as np
import wrainfo


# clutter map will be calculated monthly every first day of the month
# -------------------------------------------------------------------

def clutter_chain(start_time,
                  path,
                  elevation_angle="dataset1",
                  days=90,
                  threshold=0,
                  status=True,
                  pattern="_000.scnx.gz",
                  data_type="cmap",
                  logger=logging.getLogger()):
    """Create a ground clutter map and save NetCDF-file.

    Parameters
    ----------
    start_time : datetime.datetime
        start time which files will be read
    path : str
        path to configuration file
    elevation_angle : str
        choose dataset of one elevation angle
        (for example: dataset 1 is elevation angle 0.5°)
    days : integer
        Number of days for which a cmap is created
    threshold : float
        this is a threshold for the DBZH it should not be negative
    status : bool
        percentage of the finished clutter map
    pattern  : str
        extension of the scnx files
        (scnx file: elevation angle 0.5° = "_000.scnx")
    data_type : str
        the clutter map (cmap) were created
    logger : file
         writing status messages to a file

    Returns
    -------
    : files
        NetCDF - files in output directory.
    """
    # read output directory for clutter map from configuration file
    clutter_directory = wrainfo.reader.read_config_file(path=path,
                                                        selection="monthly_clutter_directory")
    radar_location_identifier = wrainfo.reader.read_config_file(path=path,
                                                                selection="radar_location_identifier")

    # create the stop time
    # -----------------------

    stop_time = start_time + dt.timedelta(days=days)

    # create a list of all input files for the defined time period
    # ---------------------------------------------------------------

    flist = wrainfo.reader.create_filelist(path_to_config_file=path,
                                           starttime=start_time,
                                           endtime=stop_time,
                                           pattern=pattern)

    # create clutter map
    # ---------------------
    logger.info("Creating cluttermap.")
    cmap = wrainfo.clutter.create_clutter_map_sequential(files=flist,
                                                         threshold=threshold,
                                                         grp=elevation_angle,
                                                         status=status,
                                                         logger=logger.getChild("wr_furuno.clutter"
                                                                                ".create_clutter_map_sequential"))

    # elevation angle
    # ------------------
    el = cmap.elevation.values[0]

    # create outfilename
    # ---------------------
    outfilename = f"{radar_location_identifier}_{start_time:%Y%m%d}_{stop_time:%Y%m%d}_elev_{el:0.1f}_{data_type}.nc"
    year = str(stop_time.year)
    path1 = clutter_directory + "/" + year

    if not os.path.exists(path1):
        os.makedirs(path1, exist_ok=True)
        # overwrite/remove if exist
        f = pathlib.Path(outfilename)
        f.unlink(missing_ok=True)

    outfilename = os.path.join(path1, outfilename)

    # output file as netcdf
    # ------------------------
    logger.info("Creating cluttermap netcdf output.")
    print(f"-- output to {outfilename}")
    cmap.to_netcdf(outfilename)
    logger.info("Finished cluttermap chain.")

    return True


# static clutter map will be processed each month from 3 last cluttermaps
# -----------------------------------------------------------------------

def static_cmap(path,
                pattern="_elev_0.5_cmap.nc"):
    """Create a static ground clutter map and save NetCDF-file.

    Parameters
    ----------
    path : str
        path to configuration file
    pattern : str
        extension of the netcdf file
        (cmaps for different elevation angles)

    Returns
    -------
    : files
        NetCDF - files in output directory.
    """
    # read path of clutter directory from configuration file
    path_cmap = wrainfo.reader.read_config_file(path=path,
                                                selection="monthly_clutter_directory")
    path_cmap = path_cmap + "*"

    # read radar location identifier from configuration file
    radar_location_identifier = wrainfo.reader.read_config_file(path=path,
                                                                selection="radar_location_identifier")

    # read output directory from configuration file
    outdir = wrainfo.reader.read_config_file(path=path,
                                             selection="static_clutter_directory")

    # load the last 3 cmaps
    cmaps = sorted(glob.glob(os.path.join(path_cmap, "*")))

    # filter for elevation angle
    cmaps_filter = []

    for cmap in cmaps:
        if cmap.endswith(pattern):
            cmaps_filter.append(cmap)
            cmaps_filter = cmaps_filter[-3:]

    # read the last 3 cmaps
    cmap1 = xr.open_dataset(cmaps_filter[0])
    cmap2 = xr.open_dataset(cmaps_filter[1])
    cmap3 = xr.open_dataset(cmaps_filter[2])

    # add cmaps
    cmap_final = cmap1 + cmap2 + cmap3

    # outfilename
    base_name = os.path.basename(cmaps_filter[1])
    el = base_name[28:36]

    outfilename = f"{radar_location_identifier}_static_cluttermap_{el}.nc"

    # output directory
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
        # overwrite/remove if exist
        f = pathlib.Path(outfilename)
        f.unlink(missing_ok=True)

    outfilename = os.path.join(outdir, outfilename)

    print(f"-- output to {outfilename}")
    cmap_final.to_netcdf(outfilename)

    return True


# weather radar routine
# ---------------------

def wr_routine_furuno(starttime,
                      endtime,
                      delta,
                      path,
                      data_type="Level2a",
                      elevation_angle="dataset1",
                      pattern="_000.scnx.gz",
                      logger=logging.getLogger()):
    """Process of Furuno raw data.

    Parameters
    ----------
    starttime : datetime.datetime
    endtime : datetime.datetime
    delta : datetime.delta
    path : str
        path to configuration file
    data_type : str
        Level of processing
    pattern : extension of the scnx file
             (scnx file: elevation angle 0.5° = "_000.scnx")
    elevation_angle : str
        group of hdf5 dataset
    logger : file
         writing status messages to a file

    Returns
    -------
    : files
        NetCDF - files in output directory
    """
    date = starttime
    stop_time = endtime

    # read settings from configuration file
    re_idx = wrainfo.reader.read_config_file(path=path,
                                             selection="re_index_parameters")

    re_index_parameters = np.arange(re_idx[0], re_idx[1], re_idx[2])

    dims = wrainfo.reader.read_config_file(path=path,
                                           selection="dimensions")

    while date < stop_time:

        # read static cmap
        # ----------------

        logger.info("Read static clutter map")
        stat_cmap = wrainfo.reader.read_config_file(path=path,
                                                    selection="static_cmap")
        cmap = xr.open_dataset(stat_cmap)
        cmap_bool = cmap.DBZH_sum_bool

        # load files
        # ----------
        logger.info("Create list of files to be processed")
        flist_raw = wrainfo.reader.create_filelist(path_to_config_file=path,
                                                   starttime=date,
                                                   endtime=date + delta,
                                                   pattern=pattern)

        # start processing
        # ----------------
        for file in flist_raw:

            # extension of the file
            # ---------------------
            extension = os.path.splitext(file)[1]

            if extension == ".gz":

                # read Furuno scnx data
                # ---------------------
                logger.info("Read Furuno scnx file")
                try:
                    ds = xr.open_dataset(file,
                                         engine="furuno",
                                         group=1,
                                         backend_kwargs=dict(reindex_angle=1.0))

                except Exception:
                    # except errors if a file could not read
                    logger.warning("Could not load scnx file:' " + file + "'.")
                    continue

                # rename VRADH to VRAD
                ds['VRAD'] = ds['VRADH']
                ds = ds.drop(['VRADH'])

            if extension == ".h5":

                # read Furuno hdf5 data
                # ---------------------
                logger.info("Read Furuno hdf5 file")
                try:
                    ds = xr.open_dataset(file,
                                         engine="odim",
                                         group=elevation_angle,
                                         backend_kwargs=dict(reindex_angle=1.0))

                except Exception:
                    # except errors if a file could not read
                    logger.warning("Could not load hdf5 file:' " + file + "'.")
                    continue

            # reindexing azimuth resolution
            # -----------------------------
            ds = ds.reindex(azimuth=re_index_parameters,
                            method="nearest")

            # fix errors by elevation angle
            # -----------------------------
            elevation_angle_ds = ds.elevation.median(dim="azimuth")
            ds["elevation"][:] = elevation_angle_ds

            # SNR filter by RHOHV
            # --------------------

            ds = ds.where(ds.RHOHV > 0.9)

            # remove static clutter with cmap
            # --------------------------------

            dbzh = ds.DBZH.where((cmap_bool == False))   # noqa E712

            dbzh_attrs = ds.DBZH.attrs
            ds["DBZH"] = xr.DataArray(dbzh,
                                      dims=dims,
                                      attrs=dbzh_attrs)

            #  clutter detection
            # --------------------
            logger.info("Clutter classification.")
            ds = wrainfo.clutter.fuzzy_echo_classification(ds,
                                                           cmap=cmap,
                                                           path=path,
                                                           moment="DBZH_sum_bool")

            # set clutter pixel to NA
            ds = wrainfo.clutter.dbzh_no_clutter(ds, path=path)

            # phase processing & attenuation correction (ZPHI method)
            # -------------------------------------------------------
            logger.info("Phase processing and attenuation correction.")
            ds = wrainfo.attenuation_corr.attenuation_correction(ds,
                                                                 moment="DBZH_no_clutter",
                                                                 dims=dims)

            # rain rate retreival
            # --------------------
            logger.info("Create precipitation products.")

            # QPE Z(R)
            logger.info("Create precipitation product with Z(R) relationship.")
            ds = wrainfo.precipitation.qpe_zr(ds,
                                              "DBZH_CORR",
                                              path=path,
                                              a=200,
                                              b=1.6)

            # smoothing
            ds = ds.pad(azimuth=(3, 3),
                        mode="wrap").rolling(azimuth=7,
                                             min_periods=3,
                                             center=True).mean().isel(azimuth=slice(3, -3))

            # georeferencing and gridding
            # ---------------------------
            logger.info("Georeferencing and gridding")

            swp_georef = wrainfo.geometry.furuno_georeferencing(ds,
                                                                path=path)

            wrainfo.geometry.furuno_sweep_to_netcdf(swp_georef,
                                                    path=path,
                                                    data_type=data_type)
            del ds
            del swp_georef

        date += delta

    return True
