#!/usr/bin/env python

# stdlib imports
import os.path
import pathlib
from tempfile import mkdtemp, mkstemp
from unittest import mock

# third party imports
import pandas as pd

# local imports
from strec.utils import (
    create_config,
    get_config,
    get_config_file_name,
    read_input_file,
    render_row,
)


def move_config():
    strec_config_file = get_config_file_name()
    tempfile = None
    if os.path.isfile(strec_config_file):
        tempdir = mkdtemp()
        tempfile = os.path.join(tempdir, "strec.ini")
        os.rename(strec_config_file, tempfile)
    return tempfile


def restore_config(tempfile):
    strec_config_file = get_config_file_name()
    if tempfile is not None:
        tempdir, fname = os.path.split(tempfile)
        os.rename(tempfile, strec_config_file)
        os.rmdir(tempdir)


def get_config_dict(config):
    if not isinstance(config, dict):
        dictionary = {}
        for section in config.sections():
            dictionary[section] = {}
            for option in config.options(section):
                dictionary[section][option] = config.get(section, option)
    else:
        dictionary = config.copy()

    return dictionary


def test_get_config():
    # this tests a config file that may or may not be present
    # on a users system.  So, if one is there let's move it aside
    # so that testing is always consistent between systems.
    try:
        tempdir = mkdtemp()
        tempfile = os.path.join(tempdir, "config.ini")
        with mock.patch("strec.utils.get_config_file_name") as mocked_getfile:
            mocked_getfile.return_value = pathlib.Path(tempfile)
            create_config(tempdir)
            config = get_config()
            dictionary = get_config_dict(config)
            assert sorted(list(dictionary.keys())) == ["CONSTANTS", "DATA"]
            cmp_options = [
                "maxradial_disthist",
                "ddepth_intra",
                "depth_rangecomp",
                "ddepth_interf",
                "maxradial_distcomp",
                "dstrike_interf",
                "minradial_distcomp",
                "default_szdip",
                "dlambda",
                "minno_comp",
                "step_distcomp",
                "minradial_disthist",
                "ddip_interf",
            ]
            assert sorted(cmp_options) == sorted(config["CONSTANTS"].keys())
    except Exception as e:
        raise (e)
    finally:
        if pathlib.Path(tempfile).is_file():
            os.remove(tempfile)


def test_read_input_file():
    df = pd.DataFrame({"lat": [1, 2, 3], "lon": [1, 2, 3], "depth": [1, 2, 3]})
    tmpfile = None
    try:
        h, tmpfile = mkstemp(suffix=".xlsx")
        os.close(h)
        df.to_excel(tmpfile)
        read_input_file(tmpfile, [None], None)
        df.to_csv(tmpfile)
        read_input_file(tmpfile, [None], None)
        f = open(tmpfile, "wb")
        barray = bytearray([123, 3, 255, 0, 100])
        f.write(barray)
        f.close()
        try:
            _ = read_input_file(tmpfile, [None], None)
        except ValueError:
            assert 1 == 1
    except Exception as e:
        raise (e)
    finally:
        if tmpfile is not None:
            os.remove(tmpfile)


def test_render_row():
    row = pd.Series({"lat": 32.123, "lon": -118.123, "depth": 30.0})
    for pformat in ["pretty", "json", "csv"]:
        render_row(row, pformat, [None])


if __name__ == "__main__":
    test_get_config()
    test_render_row()
    test_read_input_file()
