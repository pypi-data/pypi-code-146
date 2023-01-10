"""Compression module."""

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
import pathlib
import tarfile
import os
import glob
from wrainfo.reader import read_config_file
from wrainfo.reader import get_furuno_path


# create tar.gz files
# -------------------

def compress_furuno_raw_data(start_time,
                             end_time,
                             path,
                             delta=dt.timedelta(days=1),
                             delete_files=False):
    """Create daily tar.gz files of FURUNO raw data.

    Parameters
    ----------
    start_time : datetime.datetime
    end_time : datetime.datetime
    path : str
        Path to configuration file
    delta: datetime.delta
        timestamp in which sequence the data will be processed
    delete_files : bool
        if True than files which are packed into tar.gz file were delete

    Returns
    -------
    : files
        daily tar.gz files in output directory.
    """
    date = start_time
    stop_time = end_time
    file_names = []

    outputdir = read_config_file(path=path, selection="output_directory_tar_gz_files")
    radar_location_identifier = read_config_file(path=path, selection="radar_location_identifier")

    while date < stop_time:

        path_day = get_furuno_path(path=path, start_time=date)

        file_names = sorted(glob.glob(os.path.join(path_day, "*")))

        if len(file_names) == 0:

            date += delta

        else:
            file = file_names[1]
            basename = os.path.basename(file)
            year = basename[5:9]
            month = basename[9:11]
            day = basename[11:13]

            outfilename = f"{radar_location_identifier}_{year}{month}{day}.tar.gz"

            path1 = outputdir + "/"

            # output path will create if not exists
            if not os.path.exists(path1):
                os.makedirs(path1, exist_ok=True)
                # overwrite/remove if exist
                f = pathlib.Path(outfilename)
                f.unlink(missing_ok=True)

            # absolute output path
            outfilename = os.path.join(path1, outfilename)
            if not os.path.exists(outputdir):
                os.makedirs(outputdir)
            # overwrite/remove if exist
            f = pathlib.Path(outfilename)
            f.unlink(missing_ok=True)

            with tarfile.open(outfilename, "w:gz") as tar_handle:
                for file in file_names:
                    tar_handle.add(file, arcname=file[35:])

            if delete_files is True:

                for file in file_names:
                    os.remove(file)
                    print("delete file:", file)

            date += delta

    return True


# extract tar.gz files
# ---------------------

def extract_files(path,
                  out_dir):
    """Extract tar.gz - files.

    Parameters
    ---------
    path : path to configuration file
    out_dir : dir where the extracted tar.gz files are saved

    Returns
    -------
    : files
        Extracted tar.gz files in output directory.
    """
    dir_compressed_files = read_config_file(path=path, selection="output_directory_tar_gz_files")

    flist = sorted(glob.glob(os.path.join(dir_compressed_files, "*")))

    for gz_file in flist:
        file = tarfile.open(gz_file)
        file.extractall(out_dir)
        file.close()

    return True
