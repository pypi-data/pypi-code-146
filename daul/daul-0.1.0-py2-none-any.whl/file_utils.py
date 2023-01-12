# -*- coding: utf-8 -*-
# Copyright (c) 2023 Miroslav Hruska
"""
**********
File utils
**********

The module provides convenience functions for dealing with files, 
directories and paths.

Overview
********

Reading
=======

.. autosummary::
   read_file_lines
   read_file_first_line
   read_pickle_file

Writing
=======   
   
.. autosummary::
   write_lines_file
   write_pickle_file
   
File extensions
===============

.. autosummary::
   file_ext
   set_ext
   file_complete_ext
   set_complete_ext
   remove_complete_ext
   
Directory listing
=================

.. autosummary::
   list_dir
   walk_dir

Paths
=====

.. autosummary::
   abs_path
   prepend_dir

Directories
===========

.. autosummary::
   safe_create_dir

Sizes
=====

.. autosummary::
   file_size
   dir_size

Symlinks
========

.. autosummary::
   rel_symlink

Utilities
=========

.. autosummary::
   file_frame
   random_hash

"""

#%% Modules
# global
import os # skip
import pathlib # skip
import pickle as _pickle
import pandas as _pd
import functools as _ft
import binascii as _binascii
import fnmatch as _fnmatch

# local
import fplib as _fplib
from daul import pandas_utils as _pdu

#%% * Reading
def read_file_lines(f, strip=False, remove_empty=False, nlines=None):
  """
  Reads all lines of a given file.
  
  Parameters
  ----------
  f : str
    Path to the file.   
    
  strip: bool
    Indicates whether to strip lines of white space.
    
  remove_empty: bool
    Indicates whether to remove empty lines.
    
  nlines : int or None
    If ``None``, reads all the lines. 
    If ``int``, reads the specified number of lines.
  """
  with open(f, "r") as h:
    if nlines is None:    
      lns = h.readlines()
    else:
      lns = []
      for i in range(nlines):
        lns.append(h.readline())
    if strip:
      lns = map(lambda ln: ln.strip(), lns)
    if remove_empty:
      lns = filter(lambda ln: len(ln) > 0, lns)
    return lns
    

def read_file_first_line(f):
  """
  Reads the first line of a given file `f`.
  """
  with open(f, "r") as h:
    return h.readline()
    

def read_pickle_file(f):
  """
  Reads a pickled object from a file `f`.
  """  
  with open(f, "r") as h:
    return _pickle.load(h)
    
    
#%% * Writing
def write_lines_file(lns, f, linedel=''):
  """
  Writes lines into a file.
  
  Parameters
  ----------
  lns : list
    List of lines. 
  
  f : str
    Path to the file. 
    
  linedel : str
    Line delimiter. 
  """
  with open(f, "w") as h:
    if linedel != '':
      lns = map(lambda ln: ln + linedel, lns)
    h.writelines(lns)

  
def write_pickle_file(e, f):
  """
  Writes an object `e` as a pickle into a file `f`.
  """
  with open(f, "w") as h:
    _pickle.dump(e, h)
  

#%% * File extensions
def file_ext(f):
  """
  Returns the extension of a file `f`.
  
  Examples
  --------
  >>> file_ext('abc.txt.gz')
  '.gz'
  >>> file_ext('abc')
  ''
  """    
  return _fplib.snd(os.path.splitext(f))


def set_ext(f, ext=''):
  """
  Changes the file extension of path `f` to `ext` by replacing the 
  text starting at the last period.

  Examples
  --------
  >>> set_ext('abc.txt', '.tex')
  'abc.tex'
  >>> set_ext('abc', '.txt')
  'abc.txt'
  >>> set_ext('/home/user/file', '.cache')
  '/home/user/file.cache'

  The changes are applied only to the basename: 

  >>> set_ext('/home/user/.conf/file', '.cache')
  '/home/user/.conf/file.cache'
  
  If multiple periods are present in the basename, 
  it changes only the last one:
  
  >>> set_ext('file.txt.cache', '.ch')
  'file.txt.ch'
  
  .. seealso:: :func:`set_complete_ext` for changing the complete extension. 
  """
  basename, prev_ext = os.path.splitext(f)
  return basename + ext


def file_complete_ext(f):
  """
  Returns the complete extension of a file `f`.
  
  Examples
  --------
  >>> file_complete_ext('abc.txt.gz')
  '.txt.gz'
  """
  bn = os.path.basename(f)
  p = bn.find('.')
  if p == -1:
    return ''
  else:
    return bn[p:]
    
    
def set_complete_ext(f, ext=''):
  """
  Changes the file extension of path `f` by changing the text after 
  the first period in its basename to `ext`.
  
  Examples
  --------
  >>> set_complete_ext('abc.txt', '.tex')
  'abc.tex'
  >>> set_complete_ext('abc.txt.gz', '.ext')
  'abc.ext'
  >>> set_complete_ext('abc.txt.gz', '')
  'abc'
  
  .. seealso:: :func:`remove_complete_ext` for removing the complete extension.
  """
  dn = os.path.dirname(f)
  bn = os.path.basename(f)
  p = bn.find('.')
  if p == -1:
    return "%s%s" % (os.path.join(dn, bn), ext)
  else:
    return os.path.join(dn, bn[:p] + ext)
  

def remove_complete_ext(f):
  """
  Removes the complete extension of a path `f`.
  
  Examples
  --------  
  >>> remove_complete_ext('abc.txt.gz')
  'abc'
  """
  return set_complete_ext(f, "")


#%% * Directory listings
def list_dir(d, match='*', sort=False):
  """
  Lists files and directories that match a given pattern.
  
  The pattern is checked against the basename of the file/dir.    
  
  Parameters
  ----------
  d : str
    Directory to list. 
    
  match : str
    Name pattern that the files/dirs must match to be included.
    
  sort : bool
    Indicates whether to sort files/dirs by name.
  """
  fls = filter(lambda x: _fnmatch.fnmatch(os.path.basename(x), match), 
               map(_ft.partial(os.path.join, d), os.listdir(d))) 
  if sort:
    fls = sorted(fls)
  return fls


def walk_dir(d, match='*', follow_symlinks=False):
  """
  Walks a given directory and returns files/dirs whose basename 
  matches a given pattern.
  
  Parameters
  ----------
  d : str
    Path to the directory to walk.
    
  match : str
    The pattern of files to return. 
    
  follow_symlinks : bool
    Whether to follow links as in :func:`os.walk`.
  """
  recs = list(os.walk(d, followlinks=follow_symlinks))
  pathss = map(_fplib.npify(lambda base, dirs, files: 
              map(lambda path: os.path.join(base, path), dirs + files)), 
              recs)
  paths = sorted([d] + _fplib.unlist1(pathss))
  paths = filter(lambda x: _fnmatch.fnmatch(os.path.basename(x), match), 
                 paths)
  return paths


#%% * Paths
def as_posix_path(path):
  """
  Returns the path `path` as a POSIX path.
  
  Examples
  --------
  >>> as_posix_path('C:\\Windows')
  'C:/Windows'
  >>> as_posix_path('/home/user')
  '/home/user'
  >>> as_posix_path('C:\\Windows/system32')
  'C:/Windows/system32'
  """
  if '\\' in path:
    return pathlib.PureWindowsPath(path).as_posix()
  else:
    return pathlib.PurePosixPath(path).as_posix()


def abs_path(path, d):
  """
  Returns an absolute POSIX path of `path` given a working directory `d`. 
  
  Examples
  --------  
  >>> abs_path('dir/file', '/base')
  '/base/dir/file'
  """
  if not os.path.isabs(path):
    path = os.path.join(d, path)
  return as_posix_path(path)


def prepend_dir(path, d):
  """
  Prepends a directory `d` just before the path `path`.
  
  Examples
  --------
  >>> prepend_dir('file', 'dir')
  'dir/file'
  >>> prepend_dir('path/file', 'dir')
  'path/dir/file'
  >>> prepend_dir('/home/user/file', 'dir')
  '/home/user/dir/file'
  """
  path = os.path.join(os.path.dirname(path), d, os.path.basename(path))
  return as_posix_path(path)


#%% * Directories
def safe_create_dir(d):
  """
  Creates a directory, if it does not already exist.
  
  Parameters
  ----------
  d : str
    Path to the directory to create.


  :raises OSError: 
    If the `d` exists and it is not a directory, 
    throws an exception. 
  """
  if os.path.exists(d) and os.path.isdir(d):
    return
  os.makedirs(d)
  

#%% * Sizes
def file_size(f):
  """
  Returns the size of a file `f`, in bytes.
  """
  return os.stat(f).st_size


def dir_size(d, recursive=False):
  """
  Returns the sum of size of files in a directory `d`, in bytes.
  
  Parameters
  ----------
  recursive : bool
    Whether to recurse into subdirectories. 
  """
  fn = list_dir if not recursive else walk_dir
  return sum(map(file_size, fn(d)))
  

#%% Utilities * 
def file_frame(fs, bf=True, bfne=False, size=False, stat=False):
  """ 
  Constructs a :class:`~pandas.DataFrame` from file names, having selected columns.

  Parameters
  ----------
  fs : list of str
    a list of file names.  
  
  bf : bool
    whether to include the basename of a file (as "bf" column).
  
  bfne : bool
    whether to include the basename of a file without complete extension 
    (as "bfne" column).
    
  size : bool
    whether to include the size of a file (as "size" column). 
    
  stat : bool
    whether to include the stat of a file (as "stat" column). 
  """
  fdf = _pd.DataFrame({'f': fs})
  if bf:
    fdf = _pdu.update_column(fdf, 'bf', fdf['f'].apply(os.path.basename))
  if bfne:
    fdf = _pdu.update_column(fdf, 'bfne', fdf['f'].apply(os.path.basename)
                                        .apply(remove_complete_ext))
  if size: 
    fdf = _pdu.update_column(fdf, 'size', fdf['f'].apply(file_size))
  if stat: 
    fdf = _pdu.update_column(fdf, 'stat', fdf['f'].apply(os.stat))
  return fdf
  
  
#%% Symlinks
def rel_symlink(d, src, dst):
  """
  Creates a relative symlink, starting at a given directory.
  
  Parameters
  ----------
  d : str
    Directory to temporarily change the current directory to. 
  
  src : str
    Name of the source file.
    
  dst : str
    Name of the destination file. 
  """
  cwd = os.getcwd()
  try:  
    os.chdir(d)
    os.symlink(src, dst)
  finally:
    os.chdir(cwd)
  

def random_hash(n=8):
  """
  Generates `n` random bytes and represents them in a hexadecimal format. 
  
  Parameters
  ----------
  n : int
    Number of bytes to generate.
    
  Examples
  --------
  Let us generate a random hash from 8 bytes:  

  >>> h = random_hash(n=8)
  >>> len(h) # 16: two hex letters for a byte
  16
  """
  return _binascii.b2a_hex(os.urandom(n))


#%% tests
if __name__ == '__main__':
  import doctest
  doctest.testmod()
