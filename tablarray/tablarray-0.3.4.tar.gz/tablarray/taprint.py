#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print options and print functions for TablArray and TablaSet

Created on Sat Jan 23 10:21:06 2021

@author: chris
"""

import contextlib
import numpy as np

from . import misc

_taprint_options = {
    'threshold': 50,  # size > threshold triggers summarization
    'linewidth': 75,
    'precision': 8,
    'tashapestyle': 'trailing'}


def _check_options_2dict(threshold=None, linewidth=None,
                         precision=None, tashapestyle=None):
    """validate options, return a dict of non-None options"""
    options = {k: v for k, v in locals().items() if v is not None}
    # validate options
    if precision is not None:
        if type(precision) is not int:
            raise TypeError('precision must be int')
        if precision < 1:
            raise ValueError('precision must be at least 1')
    if linewidth is not None:
        if type(linewidth) is not int:
            raise TypeError('linewidth must be int')
        if linewidth < 6:
            raise ValueError('linewidth %d, must be at least 6' % linewidth)
    if threshold is not None:
        if type(threshold) is not int:
            raise TypeError('threshold must be int')
        if threshold < 1:
            raise ValueError('threshold must be at least 1')
    if tashapestyle not in [None, 'trailing', 'nextline', 'ignore']:
        raise ValueError("tashapestyle must be one of 'trailing',"
                         "'nextline', or 'ignore'")
    return options


def set_printoptions(threshold=None, linewidth=None, precision=None,
                     tashapestyle=None):
    """
    Set string printing options for tablarray.

    Parameters
    ----------
    precision: int > 1 [optional]
        Digits of precision for floating point (default 8).
    threshold: int > 1 [optional]
        Number of array elements that triggers summarization. (default 50)
    linewidth: int > 6 [optional]
        Number of characters per line that triggers linebreaks in arrays.
        (default 75)
    tashapestyle: 'trailing' 'nextline' 'ignore' [optional]
        Placement of tablarray shape with respect to array display.
        'trailing' (default) places shape at end of last line.
        'nextline' inserts a carriage return between last line of array and
        tablarray shape. 'ignore' does not display the shape. Note that
        tablaset2string forces 'ignore'.
    """
    options = _check_options_2dict(threshold, linewidth, precision,
                                   tashapestyle)
    _taprint_options.update(options)


def get_printoptions():
    """
    Return the current string printing options for tablarray.

    Returns
    -------
    options: dict
        - precision: int
        - threshold: int
        - linewidth: int
        - tashapestyle: int
    """
    return _taprint_options.copy()


@contextlib.contextmanager
def printoptions(*args, **kwargs):
    """
    Context manager for setting string printing options for tablarray.

    >>> import numpy as np
    >>> import tablarray as ta
    >>> with ta.printoptions(precision=3, tashapestyle='ignore'):
    >>>    print(np.pi * ta.ones((2, 2, 2), 1))
    ... [[|[3.14 3.14]|
    ...   |[3.14 3.14]|]
    ... 
    ...  [|[3.14 3.14]|
    ...   |[3.14 3.14]|]]

    See set_printoptions for parameters.
    """
    # save prior printoptions
    opts = get_printoptions()
    try:
        set_printoptions(*args, **kwargs)
        # yield with the requested options in context
        yield get_printoptions()
    finally:
        # always return to prior printoptions
        set_printoptions(**opts)


def tablarray2string(a, threshold=None, linewidth=None,
                     precision=None, tashapestyle=None):
    """Convert a TablArray to string, then use the tdim (tabular-dim)
    add a barrier '|' demarking tabular boundary.

    TODO: handle case where table is displayed across a single row"""
    if not hasattr(a, 'ts'):
        raise TypeError('type is not TablArray')
    tdim = a.ts.tdim

    overrides = _check_options_2dict(
        threshold=threshold, linewidth=linewidth, precision=precision,
        tashapestyle=tashapestyle)
    options = _taprint_options.copy()
    options.update(overrides)

    # array2string in numpy printoptions context
    with np.printoptions(
            precision=options['precision'], linewidth=options['linewidth'],
            threshold=options['threshold']):
        arraystr = a.base.__str__()

    # arraystr = array2str(a)
    # initial setup before parse
    new_arraystr = ''               # start output as blank
    lines = arraystr.split('\n')    # split input by lines
    n_lines = len(lines)            # number of input lines
    dim_i = 0                       # current dim = 0
    # parse line by line through the arraystr
    for i in range(n_lines):
        line = lines[i]
        if len(line) < 1:
            # blank lines are unmodified, nothing do to here
            pass
        else:
            # count number of brackets
            dim_opened = len(line.split('[')) - 1
            dim_closed = len(line.split(']')) - 1
            # determine whether to add front barrier or not
            if (dim_i + dim_opened) >= tdim:
                # front-side barrier
                new_arraystr += line[:tdim]
                new_arraystr += '|'
                # determine where to put back barrier
                dim_i2 = dim_i + (dim_opened - dim_closed)
                del_dim = dim_i2 - tdim
                back = ' ' * (dim_i2 - tdim) + '|'
                if del_dim >= 0:
                    # tdim does not have closure, so back-'|' is at end
                    new_arraystr += line[tdim:] + back
                else:
                    # tdim does have closure, so back-'|' precedes some ']'
                    new_arraystr += (line[tdim:del_dim] + back
                                     + line[del_dim:])
            else:
                # no barrier
                new_arraystr += line
            # update dim_i
            dim_i = dim_i2
        # newlines only only go between lines
        if i < (n_lines - 1):
            new_arraystr += '\n'

    # normally print a reminder of the TablArray shape spec
    ts_style = options['tashapestyle']
    if ts_style == 'trailing':
        new_arraystr += '%s' % a.ts
    elif ts_style == 'nextline':
        new_arraystr += '\n%s' % a.ts
    # tashapestyle == 'ignore' means no shape spec

    return new_arraystr


def _int2str(obj, precision=8, **kwargs):
    if type(obj) is not int:
        # return None if this function doesn't handle obj
        return None
    # %d is one option for int
    d = '%d' % obj
    # for very large int %0.xg will be shorter
    g_format = '%%0.%dg' % precision
    g = g_format % obj
    # only return the conversion that's actually shorter
    return d if len(d) <= len(g) else g


def _float2str(obj, precision=8, **kwargs):
    if type(obj) is not float and not np.isscalar(obj):
        # return None if this function doesn't handle obj
        return None
    # %f is one option for float
    f_format = '%%0.%df' % precision
    f = f_format % obj
    # %e is another option for float
    e_format = '%%0.%de' % precision
    e = e_format % obj
    return f if len(f) <= len(e) else e


def _str2str(obj, **kwargs):
    if type(obj) is not str:
        # return None if this function doesn't handle obj
        return None
    return obj


def _none2str(obj, **kwargs):
    if obj is not None:
        # return None if this function doesn't handle obj
        return None
    return ''


def _np2str(obj, precision=None, linewidth=None, threshold=None, **kwargs):
    if not isinstance(obj, np.ndarray):
        # return None if this function doesn't handle obj
        return None
    with np.printoptions(precision=precision, linewidth=linewidth,
                         threshold=threshold):
        string = '%s' % obj
    return string


def _ta2str(obj, **kwargs):
    if not misc.istablarray(obj):
        # return None if this function doesn't handle obj
        return None
    return tablarray2string(obj, **kwargs)


def _misc2str(obj, **kwargs):
    if type(obj) is not list and type(obj) is not tuple:
        # return None if this function doesn't handle obj
        return None
        # print('unidentified %s of type %s' % (obj, type(obj)))
        # pass
    return obj.__str__()


def cell2str(obj, **kwargs):
    """find a method to convert obj to string, considering kwargs
    such as precision"""
    for method in [_none2str, _str2str, _int2str, _float2str, _np2str,
                   _ta2str, _misc2str]:
        rval = method(obj, **kwargs)
        if rval is not None:
            return rval
    raise TypeError('method for "%s" type %s not found' % (obj, type(obj)))


def _count_str(string):
    """count rows and columns of a string"""
    lines = string.split('\n')
    cols = len(lines)
    rows = 0
    for line in lines:
        rows = max(rows, len(line))
    return rows, cols


def _str2line(string, line):
    """fetch a line of a multi-line string"""
    lines = string.split('\n')
    if line >= len(lines):
        # return '' if indexed outside of nlines
        return ''
    else:
        return lines[line]


def _listlist2string(listlist, **options):
    """given a list of lists of objects, convert to a pretty tabular string"""
    nrows = len(listlist)
    ncols = len(listlist[0])
    rows = np.zeros((nrows, ncols), dtype=int)
    cols = np.zeros((nrows, ncols), dtype=int)

    # divide the linewidth option by ncols
    linewidth = min(12, int(options['linewidth'] / ncols + .9999))
    # set tashapestyle='ignore'
    options.update(linewidth=linewidth, tashapestyle='ignore')

    strings = []
    for i in range(nrows):
        row = []
        for j in range(ncols):
            string = cell2str(listlist[i][j], **options)
            row.append(string)
            rows[i, j], cols[i, j] = _count_str(string)
        strings.append(row)

    # know the column widths
    widths = rows.max(axis=0)
    # setup line and underline formats
    my_format = ''
    underline = ''
    # print(widths)
    for width in widths:
        my_format += ' {:%d} |' % width
        underline += '-' * int(width + 2) + '+'

    string = ''
    for i in range(nrows):
        nlines = int(cols[i, :].max())
        # print('nlines', nlines)
        # print('nlines %d' % nlines)
        for line in range(nlines):
            row_args = []
            for j in range(ncols):
                str_ij = _str2line(strings[i][j], line)
                # print(i, j, str_ij)
                row_args.append(str_ij)
            row = my_format.format(*tuple(row_args))
            string += row + '\n'
        string += underline + '\n'
    return string


def _mangle_table_get(obj, index):
    """
    mangle indexing of object

    e.g. obj[0, 0, 1] = obj[1] if obj.ndim == 1

    e.g. obj[0, 0] = obj if obj.ndim == 0 or obj doesn't have ndim
    """
    if hasattr(obj, 'view') and obj.view == 'bcast':
        index2 = index
    elif not hasattr(obj, 'ndim') or obj.ndim < 1:
        if np.allclose(index, 0):
            # if obj is scalar, we do return obj if all indices are 0
            return obj
        else:
            return None
    elif not np.isscalar(index) and len(index) > obj.ndim:
        kept_index = index[-obj.ndim:]
        if len(kept_index) == 1:
            kept_index = kept_index[0]
        drop_index = index[:(len(index) - obj.ndim)]
        if np.allclose(drop_index, 0):
            # print('%s --> %s' % (index, obj.shape), kept_index, drop_index)
            # print('mangling')
            index2 = kept_index
        else:
            index2 = index
    else:
        index2 = index
    # index obj if possible, otherwise return None
    try:
        return obj[index2]
    except:
        return None


def tablaset2string(set, elmnt_size=None, elmnt_shape=None, threshold=None,
                    linewidth=None, precision=None, tashapestyle=None):
    """
    Print assembly (dict of arrays or TablaSet) to string using flat indices

    Parameters
    ----------
        set: dict of arrays or TablaSet
            data in the form of a dict of arrays or tablarray.TablaSet
        elmnt_size: int (leave as None if set is TablaSet)
            size of the arrays
        elmnt_shape: tuple (leave as None if set is TablaSet)
            shape of the arrays
            max linewidth
        see set_printoptions
    """
    # check required inputs
    if misc.istablaset(set):
        elmnt_size = set._size if elmnt_size is None else elmnt_size
        elmnt_shape = set._shape if elmnt_shape is None else elmnt_shape
    else:
        # maybe add check on set type if not TablaSet
        pass
    if elmnt_size is None or elmnt_shape is None:
        raise ValueError('size and shape required for non-TablaSet types')

    # get options
    overrides = _check_options_2dict(
        threshold=threshold, linewidth=linewidth, precision=precision,
        tashapestyle=tashapestyle)
    options = _taprint_options.copy()
    options.update(overrides)

    # 'header' just means list of keys
    header = list(set.keys())
    # assemble a list of array indices
    indices = []

    def pack_indices(iarray):
        for i in iarray:
            indices.append(np.unravel_index(i, elmnt_shape))
    iarray = np.arange(elmnt_size)
    threshold = options['threshold']
    if elmnt_size <= threshold:
        pack_indices(iarray)
    else:
        left = list(range(int(threshold / 2 + .5)))
        pack_indices(iarray[left])
        indices.append(None)  # index=None is code for '...'
        right = list(range(-int(threshold / 2), 0))
        pack_indices(iarray[right])

    listlist = []
    # header is the first row of the listlist
    listlist.append([None] + header)
    for index in indices:
        row = []
        if index is None:
            row.append('...')
        elif type(index is tuple):
            row.append(list(index))
        else:
            row.append(index)
        for key in header:
            if index is None:
                row.append('...')
            else:
                array = set[key]
                val = _mangle_table_get(array, index)
                # print(key, index2)
                # try:
                #    val = array[index2]
                # except:
                #    val = None
                row.append(val)
        listlist.append(row)
    return _listlist2string(listlist, **options)
