"""Precipitation estimation module."""

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
import xarray as xr
from wrainfo.reader import read_config_file


# quantitative precipitation estimation (QPE): R(Z)
# -------------------------------------------------

def qpe_zr(ds,
           moment,
           path,
           a=200,
           b=1.6):
    """Qualitative precipitation estimation with z-R conversion.

    Parameters
    ----------
    ds : xarray.Dataset
    moment : str
        name of the clutter and attenuation corrected data array in the dataset.
    path : str
        path to configuration file
    a : integer
        parameter for the z-R-conversion
       (Marschall Palmer default value: a = 200, German Weather Service = 256)
    b : float
        parameter for the z-R-conversion
       (Marschall Palmer default value: b = 1.6, German Weather Service = 1.42)

    Returns
    -------
    : xarray.Dataset
        xarray.Dataset with a data array of derived precipitation amounts.
    """
    # read setting from configuration file
    dims = read_config_file(path=path, selection="dimensions")
    interval = read_config_file(path=path, selection="scan_interval")

    # precipitation attributes
    prec_attrs = {"standard_name": "precipitation_amount_z_r_relationship",
                  "long_name": "precipitation_amount_z_r_relationship",
                  "unit": "mm", }

    # QPE Z(R)
    rr = ds[moment].pipe(wrl.trafo.idecibel).pipe(wrl.zr.z_to_r, a=a, b=b)
    depth = wrl.trafo.r_to_depth(rr, interval)

    # add to dataset
    ds["PREC_ZR"] = xr.DataArray(depth, dims=dims, attrs=prec_attrs)

    # fix encoding
    enc = dict(zlib=True, complevel=7, chunksizes=(1,) + ds.PREC_ZR.shape)
    ds.PREC_ZR.encoding = enc

    return ds
