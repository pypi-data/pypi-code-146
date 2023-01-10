"""Clutter detection module."""

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

import logging
import xarray as xr
import wradlib as wrl
import numpy as np
from wrainfo.reader import read_single_file
from wrainfo.reader import read_config_file


# fuzzy echo classification based on wRadlib
# -------------------------------------------

def fuzzy_echo_classification(ds, cmap, path, moment="DBZH_sum_bool"):
    """Fuzzy echo classification and clutter identification based on polarimetric variables.

    Parameters
    ----------
    ds : xarray.Dataset
    cmap : xarray.DataArray
        processed clutter map
    path : str
        path to configuration file
    moment: str
        boolean array of the clutter map

    Returns
    -------
    : xarray.Dataset
        xarray.Dataset with a clutter map.
    """
    # extract boolean array of the clutter map
    cmap_bool = cmap[moment]

    trpz_default = {"zdr": [0.7, 1.0, 9999, 9999],
                    "rho": [0.1, 0.15, 9999, 9999],
                    "phi": [15, 20, 10000, 10000],
                    "dop": [-0.2, -0.1, 0.1, 0.2],
                    "map": [1, 1, 9999, 9999],
                    "rho2": [-9999, -9999, 0.95, 0.98],
                    "dr": [-20, -12, 9999, 9999],
                    "cpa": [0.6, 0.9, 9999, 9999], }

    weights = {"zdr": 0.4,
               "rho": 0.4,
               "rho2": 0.4,
               "phi": 0.1,
               "dop": 0.1,
               "map": 0.5}

    dat = dict(rho=ds.RHOHV.values,
               phi=ds.PHIDP.values,
               ref=ds.DBZH.values,
               rho2=ds.RHOHV.values,
               dop=ds.VRAD.values,
               zdr=ds.ZDR.values,
               map=cmap_bool.values)

    dims = read_config_file(path=path, selection="dimensions")

    clmap, nanmask = wrl.clutter.classify_echo_fuzzy(dat,
                                                     weights=weights,
                                                     trpz=trpz_default,
                                                     thresh=0.5)

    ds = ds.assign(dict(FUZZ=(dims, clmap)))

    return ds


# remove clutter
# --------------

def dbzh_no_clutter(ds, path):
    """Set DBZH values, where clutter were identified, to NaN-values.

    Parameters
    ----------
    ds : xarray.Dataset
    path : str
        path to configuration file

    Returns
    -------
    : xarray.Dataset
        xarray.Dataset with removed clutter.
    """
    dims = read_config_file(path=path, selection="dimensions")

    dbzh_no_clutter = ds.DBZH.where(ds.FUZZ == False)   # noqa E712

    dbzh_no_clutter_attrs = {"standard_name": "radar_equivalent_reflectivity_factor_h",
                             "long_name": "Equivalent reflectivity factor H",
                             "unit": "dBZ", }

    ds["DBZH_no_clutter"] = xr.DataArray(dbzh_no_clutter,
                                         dims=dims,
                                         attrs=dbzh_no_clutter_attrs)

    return ds


def create_clutter_map_sequential(files, threshold=0, grp="dataset1", status=False, logger=logging.getLogger()):
    """Create a clutter map sequential in order to not overload the working memory.

    Parameters
    ----------
    files : list
    threshold : integer
        threshold of the reflectivity
    status : bool
        percent of progress

    Returns
    -------
    : xarray.Dataset
        xarray.Dataset with clutter values.
    """
    file_count = 0
    elapsed = 0
    logger.info("Processing " + str(len(files)) + " files sequentially.")
    file = files[0]
    sum_dbzh_values = None

    for file in files:
        try:
            # read furuno files
            data = read_single_file(file=file, grp=grp)

        except Exception:
            # except errors if a file could not read
            logger.warning("Could not load file:' " + file + "'.")
            continue

        # create a data array of reflectivity values
        if sum_dbzh_values is None:
            sum_dbzh_values = np.zeros_like(data.DBZH[0, :, :].values)

        else:
            values = data.DBZH[0, :, :].values

            # extract only correct values without NaN values
            good = ~np.isnan(values)
            sum_dbzh_values[good] += np.zeros_like(data.DBZH[0, :, :].values[good])

        file_count += 1

        new = round(20 * file_count / len(files), 0)

        if status:
            if new > elapsed:
                elapsed = new
                print(str(elapsed * 5) + "% done")

    logger.info("Creating boolean clutter map.")
    sum_dbzh_bool = sum_dbzh_values > threshold

    # set attributes for the new data array
    sum_dbzh_values_attrs = {"standard_name": "radar_equivalent_reflectivity_factor_h",
                             "long_name": "Equivalent reflectivity factor H",
                             "unit": "dBZ", }

    # create dataset
    logger.info("Creating arrays.")
    data["DBZH_sum_values"] = xr.DataArray(sum_dbzh_values,
                                           dims=["azimuth", "range"],
                                           attrs=sum_dbzh_values_attrs)

    data["DBZH_sum_bool"] = xr.DataArray(sum_dbzh_bool,
                                         dims=["azimuth", "range"],
                                         attrs=sum_dbzh_values_attrs)

    # delete all other moments in the dataset except for clutter map
    variables = ['DBZH_sum_bool', 'DBZH_sum_values']
    cmap = data[variables]

    return cmap
