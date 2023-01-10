#!/usr/bin/env python
# -*- coding: utf-8 -*-

from roc.rap.tasks.tds.normal_rswf import set_rswf
from roc.rap.tasks.tds.normal_tswf import set_tswf

"""
Contains wrapper method to process SBM1 and SBM2 TDS L1 data.
"""

__all__ = ["rswf", "tswf"]

def rswf(l0, task):
    """
    Method to call normal_rswf.set_rswf() with is_sbm input keyword as True.

    :param l0: L0 HDF5 object containing packet data
    :param task: Task class instance
    :return: numpy.ndarray with TDS_SCIENCE_SBM1_RSWF L1 data
    """
    return set_rswf(l0, task, is_sbm=True)


def tswf(l0, task):
    """
    Method to call normal_tswf.set_tswf() with is_sbm input keyword as True.

    :param l0: L0 HDF5 object containing packet data
    :param task: Task class instance
    :return: numpy.ndarray with TDS_SCIENCE_SBM1_TSWF L1 data
    """
    return set_tswf(l0, task, is_sbm=True)