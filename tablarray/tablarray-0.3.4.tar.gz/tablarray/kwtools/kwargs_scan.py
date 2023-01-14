#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan utilities for making args from csv data.

Primary members
---------------
arrays_2_args(header, data)


Created on Mon Aug  6 20:54:42 2018

@author: chris
"""

import numpy as np
import csv
import logging

LOG = logging.getLogger(__name__)


def csv_cell_cast(data):
    """Always treat csv cells the same way:
        1. Try to cast to float
        2. if '' then return None (see params_cleanup)
        3. else return whatever (str, basically)
        """
    try:
        param = float(data)
    except:
        if not (data == '' or data == 'None'):
            param = data
        else:
            return None
    return param


def params_cleanup(params):
    """Cleanup None's out of params[] list
    1. Hanging None's are deleted from the end
    2. None's that preceed data are transformed to 0's
        with a WARNING
    """
    # print('should params_cleanup be depreciated?')
    ended = True
    for b in range(len(params)-1, -1, -1):
        if params[b] is None:
            if ended:
                params.pop(b)
            else:
                params[b] = 0
                # hopefully 0 is the least trouble for clients
                LOG.warning('rewriting 0 instead of '' for param%2d' % (b+1))
                # but you probably shouldn't leave it blank
        else:
            ended = False
    return params


def csv_cells_2_params(data):
    """wrapper for list around csv_cell_cast"""
    params = [None] * len(data)
    for b in range(len(data)):
        params[b] = csv_cell_cast(data[b])
    params = params_cleanup(params)
    return params


def params1_dict_option(header, a):
    """use header[0] to decide whether to cast to dict or array"""
    if len(header) == 0:
        return np.array(a)
    is_str = (type(header[0]) is str or
              type(header[0]) is np.str_)
    if (len(header) > 0 and is_str and header[0] != '' and header[0] != '.'):
        # cast a into dict
        return dict(zip(header, a))
    else:
        # cast a into numpy.array
        return np.array(a)


def params2_subarray_option(header, a):
    """Wrapper around array_dict_or_single

    Adds ability to make arrays of other objects if the header is periodic.

    Return:
        array like object
    """
    # determine periodicity in the the header
    period_k, labelindices = _detect_repeating_header(header)

    # if (period_k is None) or (period_k == 1):
    if (period_k is None):
        n_data = params1_dict_option(header, a)
    else:
        n_data = []
        for k in range(len(labelindices)):
            k1 = labelindices[k]
            try:
                k2 = labelindices[k + 1]
            except:
                k2 = len(header)
            array_like = params1_dict_option(header[k1:k2], a[k1:k2])
            #not_dropped = not_dropped or not_dropped_i # do I want True if it gets dropped one time?
            if len(array_like) > 0:
                n_data.append(array_like)
        n_data = np.array(n_data)
    return n_data


def _detect_repeating_header(header):
    """Input:
        header (list of str)
    Return:
        n(int) or None, labelindices[]
    """
    # sanity check
    if header is None or len(header) == 0:
        return None, []
    # find periodicity
    label1 = header[0]
    if label1 == '':
        return None, [0]
    labelindices = []
    n = None
    for a in range(0, len(header)):
        if header[a] == label1:
            labelindices.append(a)
            if a > 0 and n is None:
                n = a
    # special case, if the first header=='.' but it's not otherwise periodic
    # then the period is 1
    if n is None and label1 == '.':
        n = 1
    return n, labelindices


def _find_in_list(key, a, start=None, force=False):
    """key - object you want to find
    a - list to search
    return - index in a
    """
    if start is None:
        sequence = range(0, len(a))
    else:
        sequence = range(start, len(a))
    for i in sequence:
        if a[i] == key:
            return i
    assert not force, '%s not found' % key


def test_depth(array_like):
    """Test object to see how much nested depth it has.

    Compatible with arbitrarily nested list, tuple, dict, or numpy.ndarray.
    Compare with numpy.ndarray.ndim.

    Here we only test array_like[0], which is not thorough.
        E.g.
        test_depth( [1, [0, [3]]] ) == 1
        test_depth( [[[3], 2], 1] ) == 3
    """
    try:
        # use recursive test to add up the depth, of course
        len(array_like)
        if len(array_like) == 0:
            return 1
        if type(array_like) is dict:
            array_like_first = list(array_like.values())[0]
            return 1 + test_depth(array_like_first)
        else:
            return 1 + test_depth(array_like[0])
    except:
        # if len(array_like) causes error, we must be at the bottom
        return 0


def name_ndim(name_str):
    """Input:
        name header string, e.g. 'arr1[' or 'sellmeier[['
    Return:
        name, ndim - e.g. 'arr1', 1 or 'sellmeier', 2
    """
    name, *list_dim = name_str.split('[')
    ndim = len(list_dim)
    return name, ndim


def depth_reduction(array_like, desired_dim):
    """If test_depth(array_like) > desired_dim
        then dereference if possible.
    Input:
        array_like, desired_dim
    Return:
        array_like
    """
    ndim = test_depth(array_like)
    if (ndim > desired_dim) and (type(array_like) is np.ndarray):
        if len(array_like) == 1:
            # we can dereference an array if it's length is 1
            return array_like[0]
        elif len(array_like) == 0:
            # should we dereference if it's length is 0?
            return None
        else:
            pass
    # didn't drop an array, so pass-through
    return array_like


def slice_array(header, data, b):
    """v2 of slice_sub_array (depreciated)
    Input:
        header - ['col1', 'col2', ...]
        data - array of shape (m,n)
        b (int) - start at 'colb'
    Return:
        name (str) = 'colb' without any brackets [[
        array (np.ndarray or dict) - of shape (j) or (j,k) or (j,k,i)
        b (int) - ending
    """
    # check basic requirements
    assert data.ndim == 2, 'slice_array expects data.ndim == 2'
    assert header[b][-1] == '[', 'b %d is pointing to %s, not a name[ cell' % (b, header[b])
    # prep
    name, ndim = name_ndim(header[b])
    end_str = ']' * ndim
    vheader = data[:, b]
    v_end = _find_in_list(end_str, vheader)
    if v_end is None:
        v_end = len(vheader)
    # find where the array ends
    end = _find_in_list(end_str, header, b, force=True)

    # slice out the area of interest
    m_header = header[b + 1:end]
    m_sliced = data[:v_end, b + 1:end]

    # loop over the rows
    m_matrix = []
    for i in range(v_end):
        sliced_i = m_sliced[i, :]
        n_data = params2_subarray_option(m_header, csv_cells_2_params(sliced_i))
        n_data = depth_reduction(n_data, (ndim - 1))
        m_matrix.append(n_data)
    # m_obj, _ = make_optional_single(vheader[:v_end], m_matrix,
    #                                (not_dropped and drop_dim))
    m_obj = params2_subarray_option(vheader[:v_end], m_matrix)
    m_obj = depth_reduction(m_obj, ndim)
    return name, m_obj, end + 1


def arrays_2_args(header, data):
    """Uses a header to control casting of data.
    Returns args, kwargs which are useful for passing to a function.

    Parameters
    ----------
    header : array or numpy.ndarray of str
        Headers which will control casting of data.
    data : array or numpy.ndarray of str
        Data

    Returns
    -------
    args : tuple
        Arguments
    kwargs : dict
        Keyword Arguments
    """
    # cleanup first
    # header, data = cleanup_arrays(header, data)

    # is_1d (bool)
    is_1d = (len(data.shape) == 1)
    assert is_1d or len(data.shape) == 2, 'data should be 1d or 2d'
    # cast to args and kwargs
    args = ()
    kwargs = {}
    # use an iterator to step throught the header
    # this is one way to allow skipping
    b_iter = iter(range(len(header)))
    for b in b_iter:
        # 0. cast the one data cell here for future ref
        if is_1d:
            casted_dat = csv_cell_cast(data[b])
        else:
            casted_dat = csv_cell_cast(data[0, b])
        # 1. '[matrix' means scan for a matrix
        if len(header[b]) > 0 and header[b][-1] == '[':
            # name, array, c = slice_sub_array(header, data, b)
            name, array, c = slice_array(header, data, b)
            if name == '':
                args = args + (array,)
            else:
                kwargs[name] = array
            # skip the iterator to the end of the matrix
            for _ in range(b, c - 1):
                next(b_iter)
        # 2. if the data cell is blank we toss it
        elif casted_dat is None:
            pass
        # 3. if header[b]=='' then this guy goes into args
        elif header[b] == '':
            args = args + (casted_dat,)
        # 4. but if header[b] got somethin, it goes in kwargs
        else:
            kwargs[header[b]] = casted_dat
    return args, kwargs


# for testing

def test_file_2_args(fname):
    """Load a file,
        (slice header and data)
    then send it to array_2_args,
    return args, kwargs.
    """
    with open(fname) as file:
        data = np.array(list(csv.reader(file)))
    head, dat = data[0], data[1:]
    return arrays_2_args(head, dat)


def quick_csv_load(fname):
    """Load a file"""
    with open(fname) as file:
        data = np.array(list(csv.reader(file)))
    return data
