"""Create error file list module."""

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

import pickle
from wrainfo.reader import load_error_flist
from wrainfo.reader import create_filelist
from wrainfo.reader import read_config_file


# create error flist
# ------------------

def create_error_filelist(out_dir):
    """Create error file list.

    Parameter
    ---------
    out_dir : str
        Output directory with filename

    Return
    ------
    : file
        empty file in output directory.
    """
    error_flist = []

    with open(out_dir, 'wb') as fh:
        pickle.dump(error_flist, fh)

    print(f"-- output to {out_dir}")

    return True


# update error file list
# ----------------------

def update_error_flist(start_time,
                       end_time,
                       path,
                       pattern='_000.scnx.gz'):
    """Update error file list manually.

    Parameter
    ---------
    start_time : datetime.datetime
    end_time : datetime.datetime
    path : str
        Path to the configuration file
    pattern : str
        extension of the scnx file (elevation angle 0.5° = "_000.scnx.gz")

    Return
    ------
    : list
        list of error files.
    """
    error_flist = load_error_flist(path=path)

    flist = create_filelist(starttime=start_time,
                            endtime=end_time,
                            path=path,
                            pattern=pattern)

    outdir = read_config_file(path=path, selection="output_path_error_flist")

    for fname in flist:
        print("Would you like add this file to error flist?" + "\n" + fname)
        user_input = input('Confirm? [Y/N] ')

        if user_input.lower() in ('y', 'yes'):
            error_flist.append(fname)
            print(fname + "\n" + "successfully added to error file list.")
        elif user_input.lower() in ('n', 'no'):
            continue

    print("Would you like save the changes to output directory?")
    user_input = input('Confirm? [Y/N] ')

    if user_input.lower() in ('y', 'yes'):
        with open(outdir, 'wb') as fp:
            pickle.dump(error_flist, fp)
            print("output to" + "\n" + outdir)
            return True

    elif user_input.lower() in ('n', 'no'):
        return error_flist
