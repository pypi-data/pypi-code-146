#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to deal with the RPW L1 BIAS CDF file production."""

from roc.rap.tasks.bia.current import set_current
from roc.rap.tasks.bia.sweep import set_sweep

__all__ = ['extract_bia_current', 'extract_bia_sweep']


def extract_bia_current(l0, task):
    """
    Extract BIAS current data from L0 file.

    :param l0:
    :param task:
    :return:
    """

    data = set_current(l0, task)

    return data


def extract_bia_sweep(l0, task):
    """
    Extract Bias sweep data from L0 file.

    :param l0: h5py object containing l0 file data
    :param task: pipeline task instance
    :return: Bias sweep data as a numpy ndarray
    """

    # Get LFR data during Bias sweep
    data = None
    if 'TM_DPU_SCIENCE_BIAS_CALIB' in l0['TM']:
        data = set_sweep(l0['TM']['TM_DPU_SCIENCE_BIAS_CALIB']['source_data'], task, 'F3')
    elif 'TM_DPU_SCIENCE_BIAS_CALIB_LONG' in l0['TM']:
        data = set_sweep(l0['TM']['TM_DPU_SCIENCE_BIAS_CALIB_LONG']['source_data'], task, 'LONG_F3')

    return data
