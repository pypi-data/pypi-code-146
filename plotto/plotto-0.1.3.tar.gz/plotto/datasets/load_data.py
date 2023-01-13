from __future__ import annotations

from os.path import abspath, join, split

from pandas import read_csv


def _get_path(f: str):
    return split(abspath(f))[0]


def _load_data(module: str, file_name: str):
    return read_csv(join(_get_path(module), file_name))


def params():
    """output from differences"""
    return _load_data(__file__, "params.csv")
