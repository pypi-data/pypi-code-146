#!/usr/bin/env python3

"""Time reading of DICOM files."""

# Copyright (c) 2013-2022 Erling Andersen, Haukeland University Hospital, Bergen, Norway

import sys
import os.path
import argparse
import urllib
import logging
import numpy as np
from .cmdline import add_argparse_options
from .formats import find_plugin, NotImageError
from .readdata import _get_sources
from .transports import Transport
from .series import Series
from pympler import tracker


logger = logging.getLogger()



def main():
    parser = argparse.ArgumentParser()
    add_argparse_options(parser)
    parser.add_argument("in_dirs", nargs='+',
                        help="Input directories and files")
    args = parser.parse_args()
    logger.setLevel(args.loglevel)

    # memory_tracker = tracker.SummaryTracker()
    try:
        si = Series(args.in_dirs, args.input_order, args)
    except NotImageError:
        print("Could not determine input format of %s." % args.in_dirs[0])
        import traceback
        traceback.print_exc(file=sys.stdout)
        return 1
    # memory_tracker.print_diff()

    selection = si

    _min = np.min(selection)
    _max = np.max(selection)
    _mean = np.mean(selection)
    _std = np.std(selection)
    _median = np.median(np.array(selection))
    _size = selection.size
    _dtype = selection.dtype

    print('Min: {}, max: {}'.format(_min, _max))
    print('Mean: {} +- {}, median: {}'.format(_mean, _std, _median))
    print('Points: {}, shape: {}, dtype: {}'.format(_size, si.shape, _dtype))
    return 0

