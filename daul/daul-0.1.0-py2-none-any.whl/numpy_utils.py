# -*- coding: utf-8 -*-
# Copyright (c) 2023 Miroslav Hruska
"""
***************
NumPy utilities
***************

Dealing with NumPy arrays. 

Overview
********

Selectors
=========

.. autosummary::
   first_nrows
   each_nth

Run-length encoding
===================

.. autosummary::
   rle

Normalization
=============

.. autosummary::
   onesum_norm

Rounding
========

.. autosummary::
   floor_decimals

Length groups
=============

.. autosummary::
   lengroup_select
   lengroup_starts_ends

Array construction
==================

.. autosummary::
   nonzeros_at

Cumulative sums
===============

.. autosummary::
   zero_cumsum_nolast

Zero/Empty-aware operations
===========================

.. autosummary::
   zaw_1d_concatenate
   eaw_loc

"""

#%% Modules
# global
import numpy as np # skip
import itertools as _it
import fplib as _fplib

#%% * Selectors
def first_nrows(arr, n):
  """
  Selects first `n` rows of a 2-dimensional array `arr`.

  Examples
  --------
  >>> arr = np.array([[1, 2], [2, 3], [3, 4]])
  >>> arr  
  array([[1, 2],
         [2, 3],
         [3, 4]])
  >>> first_nrows(arr, 1)
  array([[1, 2]])
  """
  return arr[:n, :] if not _fplib.zerolenp(arr) else arr
  
  
def each_nth(arr, n=1):
  """
  Selects each `n`-th element of an array `arr`.

  >>> list(each_nth(np.arange(10), 3))
  [0, 3, 6, 9]
  """
  return arr[(np.arange(len(arr)) % n) == 0]


#%% * Run-length encoding
def rle(l):
  """
  Run-length encodes a given list `l`.

  Examples
  --------
  >>> l = ['a', 'a', 'a', 'b', 'c', 'c', 'a']
  >>> rle(l)
  [('a', 3), ('b', 1), ('c', 2), ('a', 1)]
  """
  return [(k, sum(1 for _ in g)) for k, g in _it.groupby(l)]


#%% * Normalization
def onesum_norm(x):
  """
  Normalizes an array `x` to sum to one.

  Examples
  --------
  >>> onesum_norm(np.array([1, 3]))
  array([0.25, 0.75])
  """
  return 1.0 * x / np.sum(x)


#%% * Decimal-level rounding
def floor_decimals(x, dec=0):
  """
  Floors a value `x` to a given number `dec` of decimal places.
  
  Examples
  --------
  >>> x = 123.456

  >>> floor_decimals(x, 0)
  123.0
  >>> floor_decimals(x, 1)
  123.4
  >>> floor_decimals(x, 2)
  123.45
  
  Note the behavior for a negative number of decimals.  
  
  >>> floor_decimals(x, -1)
  120.0
  >>> floor_decimals(x, -2)
  100.0
  >>> floor_decimals(x, -3)
  0.0
  """
  mul = np.power(10.0, dec)
  return np.floor(x * mul) / mul
  

#%% * Length-groups
def lengroup_select(arrs, inds):
  """
  Selects elements from a list of arrays 
  using absolute indices as if the arrays were concatenated.

  Parameters
  ----------
  arrs : list of arrays
    The arrays from which to select elements.

  inds : array_like
    Indices to choose.

  Examples
  --------
  >>> arrs = [np.array([10, 11, 12]), np.array([21, 22])]
  >>> inds = [0, 3]  
  >>> lengroup_select(arrs, inds)
  [10, 21]
  
  >>> arrs_2d = [np.array([[0, 1], [2, 3]]), np.array([[4, 5, 6], [7, 8, 9]])]
  >>> lengroup_select(arrs_2d, inds)
  [array([0, 1]), array([7, 8, 9])]

  >>> lengroup_select(arrs_2d, [])
  []
  """
  clengs = np.array(zero_cumsum_nolast(map(len, arrs)), dtype=np.int)
  # outer array indexes
  out_locs = np.searchsorted(clengs, inds, side='right') - 1
  # inner array indexes
  in_locs = inds - clengs[out_locs]
  return map(lambda o, i: arrs[o][i], out_locs, in_locs)
  
  
def lengroup_outer_inner_indices(lens, lpos):
  """
  Returns the outer and inner indices given lengths `lens` of 
  length-grouped arrays and the desired position `lpos`. 
  
  Examples
  --------
  Suppose we have a length-group array with 2, 4, and 3 elements. 
  
  >>> lens = np.array([2, 4, 3])

  For convenience, let us label the function with a shorter name. 
  
  >>> f = lengroup_outer_inner_indices

  Now, let us obtain all possible absolute indices.   
    
  >>> lpos = np.arange(sum(lens))
  >>> o, i = f(lens, lpos)
  
  Let us take a look at outer indices:   
  >>> list(o)
  [0, 0, 1, 1, 1, 1, 2, 2, 2]
  
  We see that we are getting the proper outer index. 
  
  Let us take a look at inner within-group indices:   
  >>> list(i)
  [0, 1, 0, 1, 2, 3, 0, 1, 2]
  
  Note that an exception is raised if we have out of scope indices.
  
  >>> f(lens, -1)
  Traceback (most recent call last):
  ...
  IndexError: The absolute index is not within limits.

  >>> f(lens, sum(lens))
  Traceback (most recent call last):
  ...
  IndexError: The absolute index is not within limits.

  If we provide empty indices, we also get empty ones. 
  >>> o, i = f(lens, [])
  >>> len(o) == 0 and len(i) == 0
  True
  """
  lpos = np.array(lpos)
  if lpos.size == 0:
    return (np.empty(0, dtype=np.int), np.empty(0, dtype=np.int))
  if np.min(lpos) < 0 or np.max(lpos) >= np.sum(lens):
    raise IndexError("The absolute index is not within limits.")
  clengs = zero_cumsum_nolast(lens)
  oI = np.searchsorted(clengs, lpos, side='right') - 1
  iI = lpos - clengs[oI]
  return oI, iI


def lengroup_starts_ends(lens):
  """
  Obtains starting and ending positions of individual length-groups with 
  lengths specified by `lens`. 
  
  Examples
  --------
  >>> lens = [2, 4, 3]
  >>> s, e = lengroup_starts_ends(lens)  
  >>> s 
  array([0, 2, 6])
  >>> e
  array([2, 6, 9])
  """
  return zero_cumsum_nolast(lens), np.cumsum(lens)
  
  
#%% * Array construction
def nonzeros_at(l, pos, val, dtype):
  """
  Creates an array of a particular length (`l`), 
  by specifying all non-zero values (`val`)
  and their positions (`pos`).
  
  Parameters
  ----------
  dtype : dtype
    The dtype of the array. 
  
  Examples
  --------
  >>> nonzeros_at(l=5, pos=[2, 3], val=1, dtype=np.int)
  array([0, 0, 1, 1, 0])
  """
  T = np.zeros(l, dtype=dtype)
  if len(pos) > 0:
    T[pos] = val
  return T


#%% * Cumulative sums
def zero_cumsum_nolast(arr):
  """
  Returns the cumulative sum of an array `arr`, 
  but starting at the zero and without the last element.
  
  .. note::
    The function is useful when dealing with a list of arrays 
    (of varying lengths). Applying the function over a list of lengths 
    gives starting positions in absolute indices. :func:`~numpy.cumsum` then gives
    the ending positions.
  
  Examples
  --------
  For the sake of illustration, let us show a practical example 
  using a list of strings. 

  >>> seqs = ['abc', 'defgh', 'ij', 'klmnop']  
  
  Let us obtain their lengths:  
  
  >>> arr = map(len, seqs)

  Now we get their starting and ending positions:
  
  >>> starts = zero_cumsum_nolast(arr)
  >>> ends = np.cumsum(arr)  
  
  Suppose the string is concatenated: 
  
  >>> useq = "".join(seqs)  
  >>> useq  
  'abcdefghijklmnop'
  
  We can select the corresponding elements like this:

  >>> i = 1
  >>> s, e = starts[i], ends[i]
  >>> useq[s:e]
  'defgh'
  
  """  
  arr = np.array(arr)
  return np.cumsum(arr) - arr  
  

#%% * Zero/Empty aware functionality
def zaw_1d_concatenate(arrs, default=np.array([])):
  """
  Concatenates 1-d arrays `arrs`, or returns `default` if an empty 
  list was provided.

  Examples
  --------
  >>> default = np.array([], dtype=np.int32)
  >>> zaw_1d_concatenate([], default=default)
  array([], dtype=int32)

  >>> zaw_1d_concatenate([[1, 2], [3]])
  array([1, 2, 3])
  """
  if len(arrs) == 0:
    return default
  else:
    return np.concatenate(arrs)
  
  
def eaw_loc(arr, loc):
  """
  Returns the elements of an array `arr` specified by indices `loc`, 
  and returns an empty array if the indices are empty. 
  
  Examples
  --------
  >>> list(eaw_loc(np.arange(0, 10), []))
  []
  >>> list(eaw_loc([10, 11, 12], [1, 2]))
  [11, 12]
  """
  arr = np.array(arr)
  loc = np.array(loc)  
  if len(loc) == 0:
    return arr[:0]
  else:
    return arr[loc]
  
  
#%% Main
if __name__ == "__main__":
  import doctest
  doctest.testmod()
