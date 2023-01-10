"""Reader module."""

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

import datetime as dt
import os
import glob
import re
import xarray as xr
import numpy as np
import pickle
import json
from pathlib import Path


# read configuration file
# -----------------------

def read_config_file(path=".../example_settings_path_dependencies_wr_furuno.json", selection=None):
    """Read wr_furuno config file in json format.

    Parameter
    ---------
    path : str
        Path to config file.
    selection : str
        select setting parameter

    Return
    ------
    : dict
        configured directories in the configuration file.
    """
    path = path.replace("~", str(Path.home()))

    if not Path(path).is_file():
        raise Exception("wrainfo.reader.read_config_file(): Config file'", path, "' not found.")

    file = open(path)
    conf = json.load(file)
    file.close()

    if selection is not None:
        if selection in conf.keys():
            return conf[selection]
        else:
            raise Exception("wrainfo.reader.read_config_file(): Setting parameter'",
                            selection,
                            "' not in settings file '",
                            path,
                            "'.")
    else:
        return conf


# Functions to read the Furuno data
# ----------------------------------

def get_furuno_path(path, start_time=dt.datetime.today()):
    """Create path of Furuno radar data files.

    Parameters
    ----------
    path : str
        Path to configuration file
    start_time : datetime.datetime
        datetime object to select correct folder

    Returns
    -------
    radar_path : str
        Path to radar data
    """
    raw_path = read_config_file(path=path, selection="raw_data_directory")
    subfolder_struct_raw_path = read_config_file(path=path, selection="subfolder_structure_raw_data")

    radar_path = os.path.join(raw_path, subfolder_struct_raw_path)
    return radar_path.format(start_time.year, start_time.month, start_time.day)


def get_file_date_regex(filename):
    """Get regex from filename."""
    # regex for ""%Y-%m-%d--%H:%M:%S"
    reg0 = r"\d{4}.\d{2}.\d{2}..\d{2}.\d{2}.\d{2}"
    # regex for "%Y%m%d%H%M%S"
    reg1 = r"\d{14}"
    # regex for 20220216_085000
    reg2 = r"\d{4}\d{2}\d{2}.\d{2}\d{2}\d{2}"
    for reg in [reg0, reg1, reg2]:
        match = re.search(reg, os.path.basename(filename))
        if match is not None:
            return reg
    return None


def get_datetime_from_filename(filename, regex):
    """Get datetime from filename."""
    fmt = "%Y%m%d%H%M%S"
    match = re.search(regex, os.path.basename(filename))
    match = "".join(re.findall(r"[0-9]+", match.group()))
    return dt.datetime.strptime(match, fmt)


def load_error_flist(path):
    """Load error file list.

    Parameter
    ---------
    path : str
        Path to configuration file

    Returns
    ------
    : list
        list of error files.
    """
    path_error_flist = read_config_file(path=path, selection="error_flist_directory")

    with open(path_error_flist, 'rb') as fp:
        error_files = pickle.load(fp)

    return error_files


def create_filelist(starttime, endtime, path_to_config_file, pattern="_000.scnx.gz"):
    """Create filelist from path_glob and filename dates.

    Parameters
    ----------
    starttime : dt.datetime
        start time
    endtime : dt.datetime
        end time
    path_to_config_file : str
        Path to configuration file
    pattern : str
        extension of the scnx/netcdf file
        (scnx file: elevation angle 0.5° = "_000.scnx.gz")

    Returns
    -------
    : list
        list of files
    """
    flist = []
    flist_scnx = []
    flist_h5 = []
    datetime_list = []
    date = starttime

    path_error_flist = read_config_file(path=path_to_config_file, selection="error_flist_directory")

    if os.path.isfile(path_error_flist):
        error_flist = load_error_flist(path=path_to_config_file)
    else:
        error_flist = []

    while date <= endtime:

        raw_path = get_furuno_path(path=path_to_config_file, start_time=date)

        file_names = sorted(glob.glob(os.path.join(raw_path, "*")))

        # fixed empty list of file_names
        if len(file_names) > 0:
            regex = get_file_date_regex(file_names[0])

            for fname in file_names:
                time = get_datetime_from_filename(fname, regex)
                if time >= date:
                    if time < endtime:
                        if fname.endswith(pattern):
                            if fname not in error_flist:
                                flist_scnx.append(fname)
                        if fname.endswith(".h5"):
                            if fname not in error_flist:
                                flist_h5.append(fname)

            if len(flist_scnx) == 0:
                if len(flist_h5) > 0:
                    for file in flist_h5:
                        flist.append(file)

            if len(flist_scnx) > 0:
                for file in flist_scnx:
                    filetime_scnx = get_datetime_from_filename(file, regex)
                    datetime_list.append(filetime_scnx)
                    flist.append(file)
                if len(flist_h5) > 0:
                    for file in flist_h5:
                        filetime_h5 = get_datetime_from_filename(file, regex)
                        if filetime_h5 not in datetime_list:
                            flist.append(file)

        date = date + dt.timedelta(1)

        flist = sorted(set(flist))

    return flist


# read single file of Furuno data
# (important for create the clutter map)
# ---------------------------------------

def read_single_file(file, grp="dataset1"):
    """Read a single file, reindexes and returns a dataset object.

    Parameters
    ----------
    file : str
        path to file as string
    grp : str
        hdf5 group (elevation angle)

    Returns
    -------
    : xarray Dataset
        xarray Dataset with variables.
    """
    extension = os.path.splitext(file)[1]

    if extension == ".gz":
        # the elevation angle the elevation angle is already selected in the flist!
        tmp = xr.open_mfdataset((file,), engine="wradlib-furuno", group=1,
                                concat_dim="time", combine="nested",
                                backend_kwargs=dict(reindex_angle=1.0))
        # rename VRADH to VRAD
        tmp['VRAD'] = tmp['VRADH']
        tmp = tmp.drop(['VRADH'])

        # rename WRADH to WRAD
        tmp['WRAD'] = tmp['WRADH']
        tmp = tmp.drop(['WRADH'])

    else:
        tmp = xr.open_mfdataset((file,), engine="wradlib-odim", group=grp,
                                concat_dim="time", combine="nested",
                                backend_kwargs=dict(reindex_angle=1.0))

    # TODO add case sensitive decision on these parameters
    re_index_parameters = np.arange(0.25, 360, 0.5)

    ri = tmp.reindex(azimuth=re_index_parameters, method="nearest")
    return ri


# read multiple files
# -------------------

def read_multiple_scnx_files(starttime, endtime, path, pattern):
    """Read multiple files, reindexes and returns a dataset object.

    Parameters
    ----------
    starttime : dt.datetime
        start time
    endtime : dt.datetime
        end time
    path : str
        path to configuration file
    pattern : str
        extension of the scnx/netcdf file
        (scnx file: elevation angle 0.5° = "_000.scnx.gz")

    Returns
    -------
    : xarray Dataset
        xarray Dataset with variables.
    """
    flist = create_filelist(starttime=starttime,
                            endtime=endtime,
                            path_to_config_file=path,
                            pattern=pattern)

    scnx = xr.open_mfdataset(flist,
                             engine="wradlib-furuno",
                             group=1,
                             combine="nested",
                             concat_dim="time",
                             backend_kwargs=dict(reindex_angle=1.0))

    # rename VRADH to VRAD
    scnx['VRAD'] = scnx['VRADH']
    scnx = scnx.drop(['VRADH'])

    # rename WRADH to WRAD
    scnx['WRAD'] = scnx['WRADH']
    scnx = scnx.drop(['WRADH'])

    return scnx


# read processed cluttermap from Furuno
# -------------------------------------

def get_cmap(starttime,
             endtime,
             path,
             elev="0.5",
             timestr="%Y%m%d"):
    """Read processed cluttermap from Furuno.

    Parameters
    ---------
    starttime : datetime.datetime
        datetime - object to select correct files for list
    endtime : datetime.datetime
        datetime - object to select correct files for list
    path : str
        Path to configuration file
    elev : str
        selected elevation angle of cmap

    Returns
    -------
    : xarray.Dataset
        clutter map as xarray.Dataset.
    """
    # read settings from configuration file
    clutter_dir = read_config_file(path=path, selection="monthly_clutter_directory")
    subfolderstruct = read_config_file(path=path, selection="subfolder_structure_clutter_directory")

    # create file structure
    file_struct = os.path.join(f"{clutter_dir}", f"{subfolderstruct}", "*")

    path = file_struct.format(year=starttime.year)

    # list all cmaps in the folder
    cmaps = [cmap for cmap in sorted(glob.glob(path)) if cmap.endswith(".nc")]

    selected_map = None
    last_date = dt.datetime(1900, 1, 1)

    for cmap in cmaps:
        # choose the stop time from filename
        filetime_end = dt.datetime.strptime((os.path.basename(cmap)[19:27]), timestr)
        elev_cmap = os.path.basename(cmap)[33:36]

        if filetime_end > (endtime - dt.timedelta(45)):
            if filetime_end > last_date:
                if elev_cmap == elev:   # noqa E712
                    selected_map = cmap
                    last_date = filetime_end

        if selected_map is None:
            print("wrainfo.reader.get_cmap(): No cmap found for these dates.")

    # read cmap
    cmap = xr.open_dataset(selected_map)

    return cmap
