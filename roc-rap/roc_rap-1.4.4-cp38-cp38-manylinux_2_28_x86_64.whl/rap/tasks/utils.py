#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import h5py
from poppy.core.logger import logger

__all__ = ['PLUGIN',
           'order_by_increasing_time',
           'sort_data',
           'h5_group_to_dict',
           'decode']

# the name of the plugin
PLUGIN = 'roc.rap'


def order_by_increasing_time(data,
                             sort_by='epoch',
                             unique=False):
    """
    Given a structured array of data containing an epoch or acquisition_time field, the
    data is reordered by its values, and returns a new structured array of the
    ordered data.
    If no Epoch found then acquisition time is used instead.

    :param data: Input numpy.ndarray object to sort by ascending time
    :param sort_by: Name of the time variable used to sort data ("epoch" by defaut)
    :param unique; If True, remove duplicate Epoch data
    :return: sorted numpy.ndarray object
    """

    logger.debug('Ordering data by increasing time')
    if sort_by.lower() == 'epoch' and 'epoch' in data.dtype.names:
        if unique:
            _, indices = np.unique(data['epoch'], return_index=True)
            data = data[indices[:]]

        # If epoch found, then sort by ascending epoch values (nanosec resolution)
        data.sort(order='epoch')

    elif sort_by.lower() == 'acquisition_time' and 'acquisition_time' in data.dtype.names:
        # If not epoch found, then use CCSDS CUC acquisition time (~15 microsec resolution)
        if unique:
            _, indices = np.unique(data['acquisition_time'], return_index=True, axis=0)
            data = data[indices[:]]

        # get the indices of the reordering (with lexsort, the last column in the
        # array is the primary column for the sort).
        indices = np.lexsort(
            (
                data['acquisition_time'][:, 1],
                data['acquisition_time'][:, 0],
            )
        )
        data = data[indices[:]]
    else:
        logger.debug('No valid time variable, skip time ordering')

    # return the ordered data
    return data


def h5_group_to_dict(h5_group):
    """
    Return HDF5 group as a dictionary

    :param h5_group: HDF5 subgroup
    :return: dictionary
    """
    return {
        name: h5_group[name][()]
        for name in h5_group.keys()
    }


def sort_data(data, sort_by):
    """
    Sort input data using numpy.lexsort method().

    :param data: dictionary to sort
    :param sort_by: tuple containing data variables to sort by
    :return: sorted data
    """

    # If input data is a h5py group then
    # copy h5 data into a dictionary (to avoid change in the h5 file)
    if isinstance(data, h5py.Group):
        data = h5_group_to_dict(data)

    # Get sorted indices
    indices = np.lexsort(sort_by)
    for name in data.keys():
        data[name] = data[name][indices[:]]

    # Return sorted data and related indices
    return data, indices


def decode(binary, encoding='UTF-8'):
    """
    Decode input binary into string.

    :param binary: binary/ies to decode
    :param encoding: See string.decode() encoding keyword
    :return: Decoded string(s)
    """
    if isinstance(binary, list):
        return [element.decode(encoding) for element in binary]
    elif isinstance(binary, np.ndarray):
        def f(x):
            return x.decode(encoding)

        return np.vectorize(f)(binary)
    elif isinstance(binary, bytes):
        return binary.decode(encoding)
    else:
        raise ValueError(f'Input binary type ({type(binary)}) is not valid!')
