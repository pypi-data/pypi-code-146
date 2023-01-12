# -*- coding: utf-8 -*-
# Copyright (c) 2023 Miroslav Hruska
"""
****************
Pandas utilities
****************

The module collects utilities for dealing with :class:`~pandas.DataFrame`\ s. 

Overview
********

Columns
=======

.. autosummary::
   rename_cols
   set_cols
   reorder_cols
   prefix_cols
   drop_cols
   safe_drop_cols

Column updates
==============

.. autosummary::
   update_column
   update_tuple_col
   update_fixed_column
   column_apply

Transformations
===============

.. autosummary::
   expand
   expand_dicts_as_cols

Inner frames
============

.. autosummary::
   groupby_as_frame
   extract_inner_col
   include_outer_col
   attach_inner_col
   attach_inner_cols
   rename_inner_cols

Row splitting
=============

.. autosummary::
   row_split_ngroups
   row_split_group_size
   row_split_sizes
   row_split_bool

Joins
=====

.. autosummary::
   left_join
   left_join_def

Conversion to dictionaries
==========================

.. autosummary::
   twocol_dict
   twocol_dictf
   twocol_dictfd
   twocol_listvaldict
   twocol_listvaldictf
   twocol_listvaldictfd

Selectors
=========

.. autosummary::
   nodup
   take_middle_n_rows
   ifst

Generic
=======

.. autosummary::
   empty_frame
   pdmap
   renumber_index
   values_list
   values_set

Empty-aware utilities
=====================

.. autosummary::
   eaw_row_concat

Compatibility
=============

.. autosummary::
   sort
   row_concat

"""

#%% Libraries
# global
import pandas as pd # skip
import numpy as np # skip
import math as _math
import functools as _ft

# local
import fplib as _fplib
from fplib import fst as _fst, snd as _snd

from daul import numpy_utils as _npu

#%% * Columns
def rename_cols(df, d):
  """
  Returns a copy of a frame `df` with 
  renamed columns as defined by the dictionary `d`. 
  
  Examples
  --------
  Let us create a an empty frame with two columns:

  >>> adf = pd.DataFrame({'a': [], 'b': []})

  Rename a copy of the frame:

  >>> bdf = rename_cols(adf, {'b': 'c'})
  >>> list(bdf.columns)
  ['a', 'c']
  
  Note that the column labels of the previous frame are unchanged: 
    
  >>> list(adf.columns)
  ['a', 'b']
  """
  # remove columns that are to be renamed to 
  # remove_cols = list(set(df.columns).intersection(d.values()))
  # df = drop_cols(df, remove_cols)  
  # set the column labels  
  df = set_cols(df, map(_fplib.dictfdf(d), df.columns))
  return df


def set_cols(df, cols):
  """
  Returns a copy of a frame `df` with its labels being `cols`. 
  
  Examples
  --------
  >>> adf = empty_frame(['a', 'b'])  
  >>> bdf = set_cols(adf, ['c', 'd'])
  >>> list(bdf.columns)
  ['c', 'd']
  
  Note that the columns of `adf` are not changed:
  
  >>> list(adf.columns)
  ['a', 'b']
  """
  ndf = df.copy()
  ndf.columns = cols
  return ndf


def reorder_cols(df, first_cols=[], last_cols=[]):
  """
  Returns a copy of frame `df` with reordered columns.

  The cols `first_cols` specifies the columns that will be the 
  put first, and `last_cols` the ones that will be the last. 
  
  Examples
  --------
  >>> adf = empty_frame(['a', 'b', 'c', 'd'])
  >>> bdf = reorder_cols(adf, ['b'], ['a'])
  >>> list(bdf.columns)
  ['b', 'c', 'd', 'a']
  
  Note that the order remains unchanged in the original frame.  
  
  >>> list(adf.columns)
  ['a', 'b', 'c', 'd']
  """
  cols = df.columns
  return df[first_cols 
            + filter(lambda col: not col in first_cols + last_cols, cols) 
            + last_cols]


def prefix_cols(df, pref):
  """
  Returns a copy of a frame `df` with prefix `pref` applied to column labels.

  Examples
  --------
  >>> df = pd.DataFrame({'a': [], 'b': []})
  >>> list(prefix_cols(df, 'l:').columns)
  ['l:a', 'l:b']
  """
  df = set_cols(df, map(lambda c: "%s%s" % (pref, c), df.columns))
  return df 


def drop_cols(df, cols):
  """
  Returns a copy of a frame `df` with columns `cols` dropped.
  
  Examples
  --------
  >>> df = empty_frame(['a', 'b', 'c'])  

  We can use it for one column:
  
  >>> list(drop_cols(df, 'a').columns)
  ['b', 'c']

  And also for multiple columns:  
  
  >>> list(drop_cols(df, ['a', 'b']).columns)
  ['c']
  """  
  return df.drop(cols, axis=1)


def safe_drop_cols(df, cols):
  """
  Returns a copy of a frame `df` with columns `cols` dropped, but 
  without raising exceptions if they do not exist.
  
  Examples
  --------
  >>> df = empty_frame(['a', 'b', 'c'])

  >>> list(safe_drop_cols(df, ['a', 'd']).columns)
  ['b', 'c']

  >>> list(safe_drop_cols(df, 'a').columns)
  ['b', 'c']
  """
  return df.drop(cols, axis=1, errors='ignore')


#%% * Column updates
def update_column(df, col, values, copy=True):
  """
  Returns a copy of a frame `df` with column `col` set to `values`.

  Parameters
  ----------
  copy: bool
    Whether to return a copy.
  
  Examples
  --------
  >>> adf = pd.DataFrame({'v': [0, 1, 2]})
  
  If a column with the desirable label does not exists, a new one is created:  
  
  >>> bdf = update_column(adf, 'e', ['a', 'b', 'c'])
  >>> list(bdf['e'])
  ['a', 'b', 'c']
  
  If it does, the column will have new values:
  
  >>> cdf = update_column(bdf, 'e', ['d', 'e', 'f'])
  >>> list(cdf['e'])
  ['d', 'e', 'f']
  
  Note that the previous frame remains the same.  
  
  >>> list(bdf['e'])
  ['a', 'b', 'c']
  """
  if copy:
    df = df.copy()
  df[col] = list(values)
  return df


def update_tuple_col(df, cola, colb, values, copy=True):
  """
  Returns a copy of a frame `df` and sets values of two columns
  (`cola`, `colb`) from a list of 2-len tuples (`values`).

  Parameters
  ----------
  copy: bool
    Whether to return a copy.
  
  Examples
  --------
  >>> df = pd.DataFrame({'id': [0, 1]})
  >>> values = [('green', '#00ff00'), ('blue', '#0000ff')]
  >>> df = update_tuple_col(df, 'name', 'hex', values)  
  >>> df
     id   name      hex
  0   0  green  #00ff00
  1   1   blue  #0000ff
  """
  if copy:
    df = df.copy()
  df[cola] = map(_fst, values)
  df[colb] = map(_snd, values)
  return df


def update_fixed_column(df, col, value, copy=True):
  """
  Returns a copy of a frame `df` with a column `col` set to a 
  fixed value `value`. 
  
  See also :func:`daul.shortcuts.pdufc` for a shorter form.  

  Parameters
  ----------
  copy: bool
    Whether to return a copy.
  
  Examples
  --------
  >>> df = pd.DataFrame({'a': [0, 1]})
  >>> df = update_fixed_column(df, 'b', 'text')
  >>> list(df['b'])
  ['text', 'text']
  
  .. warning:: 
    Be aware that the objects assigned are identical and 
    if mutable, changing one will result in the change of others.
    
  >>> df = pd.DataFrame({'a': [0, 1]})
  >>> df = update_fixed_column(df, 'b', [])
  >>> list(df['b'])
  [[], []]
  
  >>> df['b'].iloc[0].append(1) # change the first object
  >>> list(df['b'])
  [[1], [1]]
  """
  df = update_column(df, col, 
                     map(_fplib.constf(value), np.arange(len(df))),
                     copy=copy)
  return df


def column_apply(df, col, f, store_as=None, copy=True):
  """
  Returns a copy of a frame with a function `f` being applied over a column
  `col` and stored as the same column `col`. 
  
  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    The frame. 

  col : 
    The column over which to apply `f`. 
    
  f : function
    The function to apply over `col`.
    
  store_as : column-label or None
    The label of the column to store results of applying 
    `f`. If None, it is the same as `col`.
    
  copy : bool
    Whether to return a copy of the frame. 
  
  Examples
  --------
  >>> df = pd.DataFrame({'a': [0, 1]})
  >>> df = column_apply(df, 'a', lambda x: x + 1)
  >>> df
     a
  0  1
  1  2
  """
  store_col = col if store_as is None else store_as
  df = update_column(df, store_col, df[col].apply(f), copy=copy)
  return df


#%% * Transformations
def expand(df, col, exp_col=None, remove_col=False):
  """
  Expands the values of a list-like column into separate rows,
  while keeping the rest of the columns fixed.
  
  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    The frame to expand.   
  
  col : str
    A column of `df` to expand.
    
  exp_col : str
    The label to store the expanded column as.
    If None, then name of `col` used.

  remove_col : bool
    Indicates whether to remove the non-expanded column.
  
  Examples
  --------
  >>> df = pd.DataFrame({'a': [1, 2], 
  ...                    'fruits': [['orange', 'apple'], 
  ...                               ['kiwi']]})
  >>> df
     a           fruits
  0  1  [orange, apple]
  1  2           [kiwi]
  >>> df = expand(df, 'fruits', 'fruit')
  >>> df
     a           fruits   fruit
  0  1  [orange, apple]  orange
  0  1  [orange, apple]   apple
  1  2           [kiwi]    kiwi
  >>> 
  
  """
  I = np.repeat(np.arange(len(df)), 
                np.array(df[col].apply(len).values, dtype=np.int))
  edf = df.iloc[I]
  if exp_col is None:
    exp_col = col
  edf = update_column(edf, exp_col, _fplib.unlist1(df[col]))
  if remove_col:
    edf = edf.drop([col], axis=1)
  return edf


def expand_dicts_as_cols(df, col, remove_col=False):
  """
  Returns a frame in which the values of a dict-based column `col` in 
  frame `df` are expanded into separate columns.
  
  Parameters
  ----------
  remove_col : bool
    Whether to remove the dict-based column.   
  
  Examples
  --------
  Suppose a frame with dict-like column `v`.
  
  >>> df = pd.DataFrame({'i': [0, 1], 
  ...                    'v': [{'a': 1, 'b': 2}, 
  ...                          {'a': 2, 'b': 3}]})
  >>> df
     i                   v
  0  0  {u'a': 1, u'b': 2}
  1  1  {u'a': 2, u'b': 3}

  Now let us expand the dictionaries in `v`. 

  >>> df = expand_dicts_as_cols(df, 'v', remove_col=True)
  >>> df[['i', 'a', 'b']]
     i  a  b
  0  0  1  2
  1  1  2  3
  """
  ndf = pd.DataFrame(list(df[col]))
  for ecol in ndf.columns:
    df = update_column(df, ecol, list(ndf[ecol]))
  if remove_col:
    df = df.drop([col], axis=1)
  return df


#%% * Inner frames
def groupby_as_frame(df, col, df_col='df'):
  """
  Groups a frame by a column and stores the frames as inner frames. 
  
  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    The frame to group. 
    
  col : label
    The column by which to group. 
    
  df_col : label
    The label that will hold the resulting subframes. 

  Examples
  --------
  >>> df = pd.DataFrame({'a': [0, 0, 1], 'b': ['a', 'b', 'c']})
  >>> df
     a  b
  0  0  a
  1  0  b
  2  1  c
  
  Let us group the frame on the `a` column:

  >>> gdf = groupby_as_frame(df, 'a')
  
  Let us see the groups: 
  
  >>> gdf[['a']]
     a
  0  0
  1  1
  
  The first group (with `a = 0`):  
  
  >>> gdf['df'].iloc[0]
     a  b
  0  0  a
  1  0  b

  The second group (with `a = 1`):

  >>> gdf['df'].iloc[1]
     a  b
  2  1  c
  """  
  if len(df) == 0:
    return pd.DataFrame({df_col: [], col: []})
  gdf = pd.DataFrame(list(df.groupby(col)))
  gdf = set_cols(gdf, [col, df_col])
  return gdf


def extract_inner_col(df, df_col, inndf_col, aggf=list):
  """
  Extracts values from an inner frame's column 
  and applies a function over them. 
  
  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    The frame.

  df_col : str
    The label of column in `df` that holds the inner frames. 
    
  inndf_col : str
    The label of column in the inner frames. 
    
  aggf : function
    The function to aggregate the columns. 
  
  Examples
  --------
  Let us first create a frame and then group it (see :func:`groupby_as_frame`), 
  such that is has an inner frame:
  
  >>> df = pd.DataFrame({'a': [0, 0, 1, 2], 'b': [1, 3, 5, 7]})
  >>> gdf = groupby_as_frame(df, 'a') # inner frame in `df`

  Now let us extract the values from the columns `b` from the inner frame:

  >>> extract_inner_col(gdf, 'df', 'b')
  0    [1, 3]
  1       [5]
  2       [7]
  Name: df, dtype: object
  
  We can also apply some function, e.g., to sum the values:  
  
  >>> extract_inner_col(gdf, 'df', 'b', sum)
  0    4
  1    5
  2    7
  Name: df, dtype: int64
  """
  return df[df_col].apply(lambda df: aggf(df[inndf_col]))


def include_outer_col(df, inndf_col, col):
  """
  Includes column from the outer frame as a fixed column in the inner frame.

  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    Frame to update. 
    
  inndf_col : label
    The label of the column that holds the inner frames. 
    
  col : label
    The label of the column which to include from `df` to the inner frames. 
  """
  df = update_column(
      df, 
      inndf_col, 
      map(lambda col_value, inndf: 
        update_fixed_column(inndf, col, col_value), df[col], df[inndf_col]))
  return df


def attach_inner_col(df, col, df_col, inndf_col, aggf=list):
  """
  Attaches a column to the outer frame by 
  aggregating the values in the inner frame.
  
  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    The frame to attach the column to.

  col : str  
    The label of the column that will be attached to the outer frame.
    
  df_col : str
    The label of the column where the inner frames are stored.

  inndf_col : str
    The label of the column in the inner frame, which will be aggregated. 
    
  aggf : function
    The function that aggregates the values. 
  """
  df = update_column(df, col, 
                     df[df_col].apply(lambda inndf: aggf(inndf[inndf_col])))
  return df


def attach_inner_cols(df, cols, df_col, aggf, namef=_fplib.idf):
  """
  Attaches selected columns from the inner frame. 
  
  Parameters
  ----------
    df : :class:`~pandas.DataFrame`
      The frame to attach the columns to. 
      
    cols : list
      The labels of the columns in the inner frame to attach to the 
      outer frame. See also `namef` parameter.
      
    df_col : str
      The label of the column where the inner frames are stored.
      
    aggf : function
      The function that aggregates the values from the inner frames.
      
    namef : function
      The function that maps labels of the columns from the inner frame
      to the labels in the outer frame. 
  
  Examples
  --------
  Let us create a simple frame that we will group to obtain inner frames:
  
  >>> df = pd.DataFrame({'a': [0, 0, 1, 2], 'b': ['a', 'b', 'c', 'd']})
  >>> df
     a  b
  0  0  a
  1  0  b
  2  1  c
  3  2  d

  Group it: 

  >>> gdf = groupby_as_frame(df, 'a') # inner frame is in 'df' column
  
  Now we can attach the inner columns as outer ones:
  
  >>> gdf = attach_inner_cols(gdf, ['b'], 'df', list)
  >>> gdf[['a', 'b']]
     a       b
  0  0  [a, b]
  1  1     [c]
  2  2     [d]
  """
  for col in cols:
    df = attach_inner_col(df, namef(col), df_col, col, aggf)
  return df


def rename_inner_cols(df, df_col, d={}):
  """
  Renames columns of inner frames.
  
  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    The frame to transform.
    
  df_col: str
    The label of the column where the inner frames are stored.
    
  d : dict
    The renaming dictionary.
  """
  df = column_apply(df, df_col, _ft.partial(rename_cols, d=d))
  return df


#%% * Row spliting
def _row_split_empty(df, empty):
  if not (empty in ['nogroup', 'zerolengroup']):
    raise ValueError("The *empty* must be one of nogroup or zerolengroup.")
  if empty == 'zerolengroup':
    return [df]
  elif empty == 'nogroup':
    return []


def row_split_ngroups(df, n, empty='zerolengroup'):
  """
  Row-splits the frame into `n` approximately equal-length frames. 

  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    The frame to row-split.
    
  n : int
    The number of groups.

  empty : str
    Applies only if the frame to split is of zero length. 
    Using 'zerolengroup' returns one group of zero length 
    (with the column labels preserved). 
    Using 'nogroup' returns an empty list.
  
  .. note:: 
    Uses NumPy :func:`array_split` for splitting the frame. 

  .. note::
    If the number of rows `r` in the frame is less than `n`, returns
    `r` groups. 

  Examples
  --------
  >>> df = pd.DataFrame({'x': np.arange(0, 1000)})
  >>> n = 10  
  >>> dfs = row_split_ngroups(df, n)
  
  The total number of frames:
  
  >>> len(dfs)
  10
  
  The size of the first frame:
  
  >>> len(dfs[0])
  100

  Note the behavior if the number of groups is less than rows:
  
  >>> df = pd.DataFrame({'x': np.arange(0, 5)})
  >>> dfs = row_split_ngroups(df, 10)
  >>> len(dfs)
  5
  
  In case of an empty frame, the result is a one group of 
  with an empty frame, by default: 
  
  >>> df = empty_frame(['a', 'b'])
  >>> dfs = row_split_ngroups(df, 5, empty='zerolengroup')
  >>> len(dfs)
  1
  >>> len(dfs[0])
  0
  
  In this case the shape of the frame is preserved and thus 
  further processing of the frame will likely succeed:

  >>> list(dfs[0].columns)
  ['a', 'b']
  
  In case of 'nogroup', returns an empty list:
  
  >>> row_split_ngroups(df, 5, empty='nogroup')  
  []
  """
  if len(df) == 0:
    return _row_split_empty(df, empty=empty)
  locs = np.array_split(np.arange(len(df), dtype=np.int), n)
  locs = filter(lambda x: len(x) > 0, locs)
  dfs  = map(lambda iloc: df.iloc[iloc], locs)
  return dfs


def row_split_group_size(df, sz, empty='zerolengroup'):
  """
  Row-splits the frame into frames having `sz` rows. 
  
  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    The frame to row-split. 
    
  sz : int
    The number of rows in a group.
  
  empty : str
    Applies only if the frame to split is of zero length. 
    Using 'zerolengroup' returns one group of zero length 
    (with the column labels preserved). 
    Using 'nogroup' returns an empty list.
    
  Examples
  --------
  >>> df = pd.DataFrame({'x': np.arange(0, 1000)})
  >>> dfs = row_split_group_size(df, 5)  
  >>> len(dfs)
  200
  >>> len(dfs[0])
  5

  .. seealso:: 
     :func:`row_split_ngroups` for examples when the frame to split 
     has zero rows.
  """
  if len(df) == 0:
    return _row_split_empty(df, empty=empty)
  locs = np.array_split(np.arange(len(df), dtype=np.int), 
                        _math.ceil(1.0 * len(df) / sz))
  dfs = map(lambda iloc: df.iloc[iloc], locs)
  return dfs


def row_split_sizes(df, lens):
  """
  Splits a frame `df` according to a list `lens` of lengths.
  
  Examples
  --------
  >>> df = pd.DataFrame({'x': np.arange(0, 10)})  
  >>> lens = [1, 3, 2, 4]
  
  Split and check whether the lengths correspond. 
  
  >>> dfs = row_split_sizes(df, lens)
  >>> map(len, dfs)
  [1, 3, 2, 4]

  Let us take a look at the last frame:

  >>> dfs[-1]
     x
  6  6
  7  7
  8  8
  9  9
  """
  if sum(lens) != len(df):  
    raise ValueError("The sum of the lens must be the same as " \
                     "the len of the frame.")
  nf = _npu.zero_cumsum_nolast(lens)
  nt = np.cumsum(lens)
  return map(lambda s, e: df[s:e], nf, nt)


def row_split_bool(df, arr):
  """
  Row-splits a frame `df` into two parts: 
  the rows for which the `arr` is True and those for which it is False.
  
  Returns
  -------
   tdf, fdf : tuple  
  
  Examples
  --------  
  >>> df = pd.DataFrame({'a': np.arange(0, 10)})
  
  Split the frame into those with an even and odd numbers:
  
  >>> adf, bdf = row_split_bool(df, df['a'] % 2 == 0)
  >>> adf  
     a
  0  0
  2  2
  4  4
  6  6
  8  8
  """
  if len(df) != len(arr):  
    raise ValueError("The length of the boolean array must be the same " \
                     "as that of the frame.")
  arr = np.array(arr, dtype=np.bool)
  tdf = df.loc[ arr]
  fdf = df.loc[~arr]
  return tdf, fdf


#%% * Joins
def left_join(ldf, rdf, jcol, rcols=[]):
  """
  Returns a copy of the left frame with columns joined from the right frame on
  a specified column.
  
  Parameters
  ----------
    ldf : :class:`~pandas.DataFrame`
      The left frame.
      
    rdf : :class:`~pandas.DataFrame`
      The right frame. 
      
    jcol : str
      The label of the column used on which to perform the join.
      
    rcols: list
      The columns from `rdf` to join. 
      

  .. note::
    No default behavior if the particular value in `jcol` is missing 
    in the right frame; see :func:`left_join_def`.

  Examples
  --------
  >>> ldf = pd.DataFrame({'a': [0, 0, 1, 2]})
  >>> rdf = pd.DataFrame({'a': [0, 1, 2], 'b': ['zero', 'one', 'two']})
  >>> left_join(ldf, rdf, 'a', ['b'])
     a     b
  0  0  zero
  1  0  zero
  2  1   one
  3  2   two
  """
  for rcol in rcols:
    ldf = update_column(ldf, rcol, 
                        ldf[jcol].apply(twocol_dictf(rdf[[jcol, rcol]])))
  return ldf


def left_join_def(df, jdf, jcol, cols=[], default=None):
  """
  Returns a copy of the left frame with columns joined from the right frame,
  providing a default value. 
  
  .. note::
    See :func:`left_join` for explanation of parameters.
  """  
  for col in cols:
    df = update_column(df, col, 
                       df[jcol].apply(twocol_dictfd(jdf[[jcol, col]], 
                                                    default=default)))
  return df


#%% * Conversion to dictionaries
def twocol_dict(df):
  """
  Creates a dictionary from the first two columns of a frame `df` 
  (`keys` --- the first column, `values` --- the second column). 
  
  .. seealso:: 
    :func:`twocol_listvaldict` for creating a list-valued dictionary. 
  
  Examples
  --------
  >>> df = pd.DataFrame({'k': ['a', 'b'], 'v': ['x', 'y']})[['k', 'v']]
  >>> df
     k  v
  0  a  x
  1  b  y
  >>> twocol_dict(df)
  {'a': 'x', 'b': 'y'}
  """
  return dict(zip(df[_fst(df.columns)], df[_snd(df.columns)]))


def twocol_dictf(df):
  """
  Creates a function that maps values from the first column of `df` to the 
  values in the corresponding rows of the second column.
  
  .. note::
    Creates a dictionary using :func:`twocol_dict`. 
  """  
  return _fplib.dictf(twocol_dict(df))


def twocol_dictfd(df, default):
  """
  Creates a function that maps values from the first column of `df` to the 
  values in the corresponding rows of the second column, 
  with a default value `default`. 
  """
  return _fplib.dictfd(twocol_dict(df), default=default)

# List-valued dictionaries

def twocol_listvaldict(df):
  """
  Creates a dictionary from the first two columns of a frame `df`, 
  (`keys` --- the first column, `values` --- list-aggregated values
  from the second column for the same `key`).
  
  .. seealso:: :func:`twocol_dict`. 
  
  Examples
  --------
  >>> df = pd.DataFrame({'k': ['a', 'a', 'b'], 'v': ['c', 'd', 'e']})[['k', 'v']]
  >>> df
     k  v
  0  a  c
  1  a  d
  2  b  e
  >>> twocol_listvaldict(df)
  {'a': ['c', 'd'], 'b': ['e']}
  """
  return _fplib.listvaldict(zip(df[_fst(df.columns)], df[_snd(df.columns)]))
  

def twocol_listvaldictf(df):
  """
  Creates a function that maps `keys` from the first column of `df` 
  into a `list` of `values` from the second column corresponding to the same `key`.
  
  .. seealso::
    The function is a wrapper over :func:`twocol_listvaldict`.
  """  
  return _fplib.dictf(twocol_listvaldict(df))
  
  
def twocol_listvaldictfd(df, default):
  """
  Creates a function that maps `keys` from the first column of `df` into a 
  `list` of `values` from the second column corresponding to the same `key`
  (with a default value `default`, if no such `key` is found).

  .. seealso::
    The function is a wrapper over :func:`twocol_listvaldict`.
  """
  return _fplib.dictfd(twocol_listvaldict(df), default=default)


#%% * Selectors
def take_middle_n_rows(df, n, error_if_less=False):
  """
  Selects `n` middle rows of a frame.

  :raises: ValueError
    
    If the `df` has less than `n` rows, and if 
    `error_if_less` is set. 

  Examples
  --------
  >>> df = pd.DataFrame({'col': ['a', 'b', 'c']})  
  >>> take_middle_n_rows(df, 1)
    col
  1   b
  >>> take_middle_n_rows(df, 2)
    col
  0   a
  1   b
  """  
  if len(df) >= n:
    return df.iloc[((len(df) - n) / 2): ((len(df) + n) / 2)]
  else:
    if error_if_less:
      raise ValueError("Not enough rows.")
    else:
      return df


def ifst(x):
  """
  Returns the first element of `x` using `iloc` of a frame, or a series.
  """
  return x.iloc[0]


def nodup(df, cols=None):
  """
  Returns non-duplicated rows of a frame `df`.
  
  If the `cols` is :code:`None`, then all columns are used.  
  """
  if cols is None:
    cols = df.columns
  return df.loc[-df[cols].duplicated()]


#%% * Empty-aware utilities
def eaw_row_concat(dfs, cols):
  """ 
  Performs a row-wise concatenation of frames `dfs`. If an empty list is given, 
  returns an empty frame with the specified columns `cols`.
  """
  if sum(map(len, dfs)) == 0:
    return empty_frame(cols)
  else:
    return row_concat(dfs)



#%% Generic
def empty_frame(cols=[]):
  """
  Creates an empty frame with the given column labels `cols`. 
  
  Examples
  --------
  >>> df = empty_frame(['a', 'b'])  
  >>> len(df)
  0
  >>> list(df.columns)
  ['a', 'b']
  """
  return pd.DataFrame(dict(_fplib.zipe(cols, [])))


def renumber_index(df, copy=True):
  """
  Returns a copy of a frame `df`, with the index having consecutive values in 
  the range from :code:`0` to :code:`len(df) - 1`. 
  
  Parameters
  ----------
  copy : bool
    Whether to return a copy of the frame. 

  """
  if copy:  
    df = df.copy()
  df.index = np.arange(len(df))
  return df


def pdmap(f, df):
  """
  Maps a function `f` over rows of a frame `df`, with the function application 
  being done over all columns as positional arguments. 
  
  Examples
  --------
  >>> df = pd.DataFrame({'a': [0, 1]})
  >>> df = update_column(df, 'b', df['a'] + 10)
  >>> df
     a   b
  0  0  10
  1  1  11
  >>> pdmap(lambda x, y: x + y, df)
  [10, 12]
  """
  cols = map(lambda i: df[df.columns[i]].values, range(len(df.columns)))
  return map(f, *cols)
  

def values_list(x):
  """
  Returns the `x.values` of `x` as a list.
  
  Examples
  --------
  >>> df = pd.DataFrame({'x': np.arange(5)})  
  >>> values_list(df['x'])
  [0, 1, 2, 3, 4]
  """
  return list(x.values)


def values_set(x):
  """
  Returns the `x.values` of `x` as a set.
  
  Examples
  --------
  >>> df = pd.DataFrame({'x': ['a', 'a', 'a']})  
  >>> values_set(df['x'])
  set(['a'])
  """
  return set(x.values)
  
  
#%% * Compatibility
def sort(df, col, ascending=True):
  """
  Sorts frame by given col(s).
  
  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    The frame to sort. 
    
  col : str or list
    Columns by which to sort. 
  
  ascending : bool or list
    Whether to sort in ascending order. 
  
  .. note:: 
    Internally uses :func:`pd.DataFrame.sort_values` 
    or :func:`pd.DataFrame.sort` if not available.
  """
  if hasattr(df, 'sort_values'):
    return df.sort_values(col, ascending=ascending)
  else:
    return df.sort(col, ascending=ascending)
    

def row_concat(dfs):
  """
  Concatenates frames `dfs`, row-wise.
  """
  if not 'sort' in pd.concat.func_code.co_varnames:
    return pd.concat(list(dfs))
  else:
    return pd.concat(list(dfs), sort=False)


#%% * Empty-aware
def eaw_groupby_agg(df, groupby, aggd):
  """
  Groups a frame and aggregates values, even for an empty frame. 

  Parameters
  ----------
  df : :class:`~pandas.DataFrame`
    Frame to group. 
    
  groupby : str
    Label of column to groupby. 
    
  aggd : dict
    Dictionary of labels and functions to as in 
    :func:`pandas.DataFrame.agg`. 

  Examples
  --------
  >>> df = pd.DataFrame({'x': [0, 0, 1], 'y': [1, 2, 3]})
  >>> df
     x  y
  0  0  1
  1  0  2
  2  1  3
  >>> gdf = eaw_groupby_agg(df, 'x', {'y': np.max}).reset_index()
  >>> gdf
     x  y
  0  0  2
  1  1  3
  >>> df = empty_frame(['x', 'y'])
  >>> gdf = eaw_groupby_agg(df, 'x', {'y': np.max}).reset_index()
  >>> gdf
  Empty DataFrame
  Columns: [x, y]
  Index: []
  """
  if len(df) == 0:
    gdf = pd.DataFrame(dict(_fplib.zipe(aggd.keys(), [])), index=pd.Index([], name=groupby))
    return gdf
  else:
    return df.groupby(groupby).agg(aggd)


#%% Main
if __name__ == '__main__':
  import doctest
  doctest.testmod()
