#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Pyxel CosmiX model to generate charge by ionization."""

import bisect
from pathlib import Path
from typing import Callable, Optional

import numpy as np
import pandas as pd
from scipy import interpolate


def sampling_distribution(distribution: np.ndarray) -> float:
    u: float = np.random.random()
    # random_value_from_dist = distribution[bisect.bisect(distribution[:, 1], u) - 1, 0]
    random_value_from_dist = get_xvalue_with_interpolation(
        function_array=distribution, y_value=u
    )

    return random_value_from_dist


def get_xvalue_with_interpolation(function_array: np.ndarray, y_value: float) -> float:
    if y_value <= function_array[0, 1]:
        intpol_x_value: float = function_array[0, 0]
    elif y_value >= function_array[-1, 1]:
        intpol_x_value = function_array[-1, 0]
    else:
        value_bisect: int = bisect.bisect(
            a=function_array[:, 1],  # type: ignore
            x=y_value,
        )
        y_index_bot: int = value_bisect - 1

        y_index_top: int = y_index_bot + 1
        y_value_bot: float = function_array[y_index_bot, 1]
        y_value_top: float = function_array[y_index_top, 1]
        x_value_bot: float = function_array[y_index_bot, 0]
        x_value_top: float = function_array[y_index_top, 0]

        intpol_x_value = x_value_bot + (y_value - y_value_bot) * (
            x_value_top - x_value_bot
        ) / (y_value_top - y_value_bot)

    return intpol_x_value


def get_yvalue_with_interpolation(function_array, x_value):
    x_index_bot = bisect.bisect(function_array[:, 0], x_value) - 1
    x_index_top = x_index_bot + 1
    x_value_bot = function_array[x_index_bot, 0]
    x_value_top = function_array[x_index_top, 0]
    y_value_bot = function_array[x_index_bot, 1]
    y_value_top = function_array[x_index_top, 1]

    intpol_y_value = y_value_bot + (x_value - x_value_bot) * (
        y_value_top - y_value_bot
    ) / (x_value_top - x_value_bot)

    return intpol_y_value


def load_histogram_data(
    file_name: Path,
    hist_type: str,
    skip_rows: Optional[int] = None,
    read_rows: Optional[int] = None,
) -> pd.DataFrame:
    # TODO store count in pandas dataframe as int !!!

    step_size_data = pd.read_csv(
        file_name,
        delimiter="\t",
        names=[hist_type, "counts"],
        usecols=[1, 2],
        skiprows=skip_rows,
        nrows=read_rows,
    )
    return step_size_data


# def load_energy_data(file_name, step_rows):
#     """TBW.
#
#     :param file_name:
#     :param step_rows:
#     :return:
#     """
#     # 'proton_' + energy + '_' + thickness + '_1M.ascii'
#     spectrum_data = pd.read_csv(file_name, delimiter="\t",
#                                 names=["energy", "counts"], usecols=[1, 2], skiprows=step_rows + 8)
#
#     return spectrum_data


def read_data(file_name: Path) -> np.ndarray:
    full_path = file_name.resolve()
    if not full_path.exists():
        raise FileNotFoundError(f"Cannot find file '{full_path}' !")

    data: np.ndarray = np.loadtxt(full_path, "float", "#")
    return data


def interpolate_data(data: np.ndarray) -> Callable[[np.ndarray], np.ndarray]:
    data_function: Callable[[np.ndarray], np.ndarray] = interpolate.interp1d(
        data[:, 0], data[:, 1], kind="linear"
    )
    return data_function
