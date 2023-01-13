"""
Data management.
"""
import sys
import os
import copy
import numpy as np
from numpy.linalg import norm
import zipfile
import numpy.lib.format as npy_format
import pandas as pd
from glob import glob
from os import path
import fnmatch
import re
from collections import OrderedDict
from datetime import timedelta
from skimage.util import view_as_windows
# pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None)

from .utils import eval_dict
from .grid import Grid

def col_group(x):
    if x[-1] in 'xyz':
        return x[:-1]
    if ',' in x:
        return x.split(',')[0]
    return x

def match_column(pattern, columns):
    """
    match column pattern from available columns
    m -> (mx, my, mz)
    m.region*x
    """
    cols = []
    if pattern in columns:
        cols.append(pattern)
    elif pattern + "x" in columns:
        cols.append(pattern + "x")
        if pattern + "y" in columns:
            cols.append(pattern + "y")
        if pattern + "z" in columns:
            cols.append(pattern + "z")
    else:
        matches = fnmatch.filter(columns, pattern)
        if matches:
            cols.extend(matches)
    return cols

def match_columns(patterns, columns):
    """ match column patterns """
    cols = []
    for p in patterns:
        cols.extend(match_column(p, columns))
    return cols

def csv_columns(filename):
    """ Parse column names at the top of a CSV file """
    with open(filename) as fp:
        first_line = fp.readline()

    if not first_line.startswith('#'):
        # no header found
        return []

    first_line = first_line.strip('# \n')
    if '(' in first_line:
        # some CSV headers contain extra info such as units per column
        # e.g. "t (s) B_extx (T) ..."
        # remove them from the column names
        first_line = re.sub(r' \([^()]*\)', '', first_line)

    columns = first_line.split()

    return columns

def save_csv(df, filename):
    index = df.index.name is not None
    header = not isinstance(df.columns, pd.RangeIndex)

    fp = open(filename, 'wt')
    if header:
        fp.write('# ')

    # For object columns, df.to_csv uses str(obj) to get a string
    # representation of each value. In case the column contains a numpy array,
    # make sure the entire array is returned, without newlines.
    np.set_string_function(repr, repr=False) # use repr() as the str() function
    with np.printoptions(linewidth=np.inf, threshold=np.inf):
        df.to_csv(fp, sep=' ', index=index, header=header)
    np.set_string_function(None, repr=False) # restore default str() function

def read_csv(filename, index_col=None):
    try:
        names = csv_columns(filename)
        if names:
            df = pd.read_csv(filename, sep=r'\s+', index_col=index_col,
                    names=names, skiprows=1, engine='c')
        else:
            df = pd.read_csv(filename, sep=r'\s+', index_col=index_col,
                    header=None, engine='c')

    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        # empty csv
        df = pd.DataFrame()

    return df

def save_hdf(df, filename):
    filename, key = path.split(filename)
    df.to_hdf(filename, key, mode='a', complevel=9, complib='zlib')

def read_hdf(filename):
    filename, key = archive_key(filename)
    return pd.read_hdf(filename, key)

def hdf_columns(filename):
    filename, key = archive_key(filename)
    store = pd.HDFStore(filename, mode='r')

    if key is None:
        key = store.keys()[0]

    # assuming fixed format
    columns = list(store.get_node('{}/axis0'.format(key)).read().astype(str))
    index_name = store.get_node('{}/axis1'.format(key))._v_attrs.name
    if index_name is not None:
        columns.append(index_name)

    store.close()

    return columns

def read_npy(filename):
    arr = np.load(filename, allow_pickle=True)
    return pd.DataFrame.from_records(arr)

def save_npy(df, filename):
    index = df.index.name is not None
    arr = df.to_records(index=index)
    np.save(filename, arr)

def npy_columns(filename):
    with open(filename, 'rb') as fp:
        version = npy_format.read_magic(fp)
        npy_format._check_version(version)
        shape, fortran_order, dtype = npy_format._read_array_header(fp, version)
        return dtype.names

def read_npz(filename):
    filename, key = archive_key(filename)
    with np.load(filename, allow_pickle=True) as f:
        return pd.DataFrame.from_records(f[key])

def save_npz(df, filename):
    filename, key = archive_key(filename)
    index = df.index.name is not None
    arr = df.to_records(index=index)

    """ np.savez() doesn't support appending to an archive,
    so we need to do it ourselves """
    kw = dict(compression=zipfile.ZIP_DEFLATED, allowZip64=True)
    with zipfile.ZipFile(filename, mode="a", **kw) as zipf:
        fname = key + '.npy'
        # TODO: check for duplicate keys
        # always force zip64, gh-10776
        with zipf.open(fname, 'w', force_zip64=True) as fid:
            npy_format.write_array(fid, arr, allow_pickle=True)

def npz_columns(filename):
    filename, key = archive_key(filename)
    with np.load(filename) as npz:
        fp = npz.zip.open(key + ".npy")
        version = npy_format.read_magic(fp)
        npy_format._check_version(version)
        shape, fortran_order, dtype = npy_format._read_array_header(fp, version,
                max_header_size=2**64)
        return dtype.names

# supported table formats
table_formats = {
    'csv': (read_csv, save_csv, csv_columns),
    'hdf': (read_hdf, save_hdf, hdf_columns),
    'npy': (read_npy, save_npy, npy_columns),
    'npz': (read_npz, save_npz, npz_columns),
}

# map from extension -> format
table_extensions = {
    'csv': 'csv',
    'txt': 'csv',
    'hdf': 'hdf',
    'h5': 'hdf',
    'npy': 'npy',
    'npz': 'npz',
}

archive_formats = ["npz", "hdf"]

table_patterns = ['*.' + ext for ext in table_extensions]

def archive_key(filename):
    base, ext = path.splitext(filename)
    if ext[1:] in archive_formats:
        return filename, None

    head, tail = path.split(filename)
    if not head:
        return tail, None

    return head, tail

def get_format(filename):
    # dir/file.ext
    base, ext = path.splitext(filename)
    if ext:
        return ext[1:]

    # archive.fmt/key
    filename, key = archive_key(filename)
    base, ext = path.splitext(filename)
    if ext:
        return ext[1:]

    # unknown
    return None

def is_archive_format(fmt):
    return fmt in archive_formats

def is_archive(filename):
    fmt = get_format(filename)
    return is_archive_format(fmt)

def is_tablefile(filename):
    return get_format(filename) in table_extensions

def list_dir(filename):
    return os.listdir(filename)

def list_npz(filename):
    with np.load(filename) as npz:
        return npz.files

def list_hdf(filename):
    with pd.HDFStore(filename, mode='r') as store:
        return [k.lstrip('/') for k in store.keys()]

def listfiles(filename):
    files = None

    if not path.exists(filename):
        raise FileNotFoundError(filename)

    if path.isdir(filename):
        files = list_dir(filename)

    elif is_archive(filename):
        fmt = get_format(filename)
        if fmt == 'npz':
            files = list_npz(filename)
        elif fmt == 'hdf':
            files = list_hdf(filename)

    if files:
        files = [path.join(filename, f) for f in sorted(files)]
        return files

    raise ValueError(f"Don't know how to open {filename}, sorry")

def to_table(data):
    if isinstance(data, dict):
        with np.printoptions(linewidth=np.inf, threshold=sys.maxsize):
            data = [[k, repr(v)] for k,v in data.items()]
        df = pd.DataFrame(data)
        return df
        # return pd.DataFrame(data.values(), index=data.keys())

    if not isinstance(data, pd.DataFrame):
        return pd.DataFrame(data)

    return data

def match_any(name, patterns):
    return any([fnmatch.fnmatch(name, pat) for pat in patterns])

def read_table(filename, index_col=None, **kwargs):
    fmt = get_format(filename)
    fmt = table_extensions[fmt]
    reader = table_formats[fmt][0]
    df = reader(filename, **kwargs)
    if index_col is not None and df.index.name != index_col:
        df.set_index(index_col, inplace=True)
    return df

def save_table(data, filename):
    df = to_table(data)
    fmt = get_format(filename)
    fmt = table_extensions[fmt]
    writer = table_formats[fmt][1]
    return writer(df, filename)

def table_columns(filename):
    fmt = get_format(filename)
    fmt = table_extensions[fmt]
    func = table_formats[fmt][2]
    return func(filename)

def read_tables(filenames, index_col=None):
    dfs = [read_table(f, index_col) for f in filenames]

    # merge them
    table = dfs[0]
    for df in dfs[1:]:
        table = table.join(df)

    return table

def read_geometry(filename='geometry.csv'):
    df = read_table(filename)
    pos = np.array(df[['posx', 'posy']])
    angle = np.array(df['angle'])
    return pos, angle

def read_vectors(filenames, quantity='mag', t=None):
    files = []
    columns = []
    for f in filenames:
        cols = table_columns(f)
        # Look for time column
        if 't' not in cols:
            continue

        # Look for quantity
        match = match_column(quantity + '*', cols)
        if not match:
            continue

        # Look for xy data
        match = list(filter(lambda c: c[-1] in 'xy', match))
        if not match:
            continue

        files.append(f)
        columns.extend(match)

    assert files, f"No vector data found for quantity: {quantity}"

    df = read_tables(files, index_col='t')
    df = df[columns]

    if t is not None:
        if np.isscalar(t):
            t = [t]
        df = df.iloc[t]

    assert len(df.columns) % 2 == 0, "Number of columns not divisible by 2, not vector data?"

    UV = np.array(df)
    UV = UV.reshape((UV.shape[0], -1, 2))

    time = np.array(df.index)

    return time, UV

def crop(X, crop, axis=-1):
    """ Crop array X along one or more axes
    crop is a tuple (before, after) for each axis to crop
    axis specifies which axis to start cropping from
    """
    if not isinstance(X, np.ndarray):
        X = np.array(X)

    if np.isscalar(crop):
        crop = (crop, crop)

    crop = np.array(crop)
    if crop.ndim < 2:
        crop = [crop] * len(X.shape)

    if axis < 0:
        axis = X.ndim - len(crop) + axis + 1

    indices = [slice(None) for i in range(X.ndim)]
    for i, (before, after) in enumerate(crop):
        start = before
        stop = -after if after > 0 else None
        indices[axis + i] = slice(start, stop)

    return X[tuple(indices)]

def rolling_window(X, win_shape, step=1, method='sum'):
    """ Apply a function over a rolling window of X """
    assert method in ('sum', 'mean')

    mask = X.mask if np.ma.is_masked(X) else None
    X = np.copy(X)
    dtype = X.dtype
    if mask is not None:
        # view_as_windows doesn't work with masked arrays so set masked values
        # to nan and ignore the nans when computing the mean
        X = X.astype(float)
        X[mask] = np.nan

    if np.isscalar(win_shape):
        win_shape = (win_shape,) * X.ndim

    if np.isscalar(step):
        step = (step,) * X.ndim

    assert len(win_shape) == len(step)

    W = view_as_windows(X, win_shape, step)
    axis = tuple(range(X.ndim, W.ndim))

    if mask is not None:
        if method == 'mean':
            W = np.nanmean(W, axis=axis)
        else:
            W = np.nansum(W, axis=axis)

        # Mask any remaining nan values
        W = np.ma.masked_invalid(W)
        return W.astype(dtype)

    if method == 'mean':
        return np.mean(W, axis=axis)

    return np.sum(W, axis=axis)


def filter_df(df, **kwargs):
    """ Filter dataframe by key=value or range key=slice(start, stop, step) or list key=[key1, key2, key3] """
    for k,v in kwargs.items():
        if callable(v):
            df = df[df[k].apply(v)]

        elif isinstance(v, slice):
            # range (start, stop)
            start = v.start - 1e-8 if v.start is not None else v.start
            stop = v.stop + 1e-8 if v.stop is not None else v.stop
            step = v.step
            df = df.set_index(k).loc[start:stop:step].reset_index()
        else:
            if not isinstance(v, tuple) and not isinstance(v, list):
                v = [v]

            matches = []
            for vi in v:
                # equals
                if isinstance(vi, str) or np.issubdtype(df[k].dtype, np.integer):
                    matches.append(df[k] == vi)
                else:
                    # Determine tolerance based on size of filter value
                    atol = 10**(np.floor(np.log10(np.abs(vi))) - 4)
                    matches.append(np.isclose(df[k], vi, atol=atol))

            df = df[np.logical_or.reduce(matches)]

    return df

class Dataset(object):
    def __init__(self, index=None, params={}, info={}, basepath=None):
        self.index = index
        self.params = params
        self.info = info
        self.basepath = basepath

    @property
    def name(self):
        if self.basepath:
            return path.basename(path.abspath(self.basepath))
        return ''

    def __getitem__(self, i):
        index = self.index.loc[i]
        if isinstance(index, pd.Series):
            # single row returns a Series, but we want a DataFrame
            index = self.index.loc[[i]]
        ds = copy.copy(self)
        ds.index = index
        return ds

    def __repr__(self):
        return 'Dataset({!r}): {} items'.format(self.basepath, len(self))

    def __str__(self):
        s = "Dataset: {}\n\n".format(self.name)
        s += "params:\n"
        for k,v in sorted(self.params.items(), key=lambda i: i[0].lower()):
            s += " {}={}\n".format(k,v)
        s += "\n"
        s += "info:\n"
        for k,v in sorted(self.info.items(), key=lambda i: i[0].lower()):
            s += " {}: {}\n".format(k,v)
        s += "\n"
        s += "index:\n"
        s += str(self.index)
        s += "\n"
        return s

    def keys(self):
        return list(self.index.index)

    def items(self):
        for i in self.index.index:
            yield i, self.__getitem__(i)

    def iterrows(self):
        for i, row in self.index.iterrows():
            yield ((i,) + tuple(row), self.__getitem__(i))

    def __iter__(self):
        for _, ds in self.items():
            yield ds

    def __len__(self):
        return len(self.index)

    def __eq__(self, other):
        return self.basepath == other.basepath and \
                self.params == other.params and \
                (self.index == other.index).all(axis=None)

    def subset(self, i):
        index = self.index.loc[i]
        if isinstance(index, pd.Series):
            # single row returns a Series, but we want a DataFrame
            index = self.index.loc[[i]]
        ds = copy.copy(self)
        ds.index = index
        return ds

    def filter(self, **kwargs):
        ds = copy.copy(self)
        ds.index = filter_df(self.index, **kwargs)

        return ds

    def drop_duplicates(self, **kwargs):
        ds = copy.copy(self)
        ds.index = self.index.drop_duplicates(**kwargs)

        return ds

    def groupby(self, key):
        for k, index in self.index.groupby(key):
            ds = copy.copy(self)
            ds.index = index
            yield k, ds

    def sort_values(self, column):
        ds = copy.copy(self)
        ds.index = ds.index.sort_values(column)
        return ds

    def row(self, row=0):
        return self.index.iloc[row]

    def id(self, row=0):
        return self.row(row).name

    @staticmethod
    def read(basepath):
        index = read_csv(path.join(basepath, 'index.csv'))

        params = read_csv(path.join(basepath, 'params.csv'))
        params = dict(np.array(params))
        params = eval_dict(params)

        info = read_csv(path.join(basepath, 'info.csv'))
        info = dict(np.array(info))
        info = eval_dict(info)

        return Dataset(index, params, info, basepath)

    def save(self, basepath=None):
        if basepath and not self.basepath:
            self.basepath = basepath

        if not basepath:
            basepath = self.basepath

        assert basepath

        save_table(self.index, path.join(basepath, 'index.csv'))
        save_table(self.params, path.join(basepath, 'params.csv'))
        save_table(self.info, path.join(basepath, 'info.csv'))

    def file(self, filename):
        files = []
        for outdir in self.index['outdir']:
            files.append(path.join(self.basepath, outdir, filename))
        if len(files) == 1:
            return files[0]
        return files

    def files(self, patterns=None, squash=True):
        if isinstance(patterns, str):
            patterns = [patterns]

        files = [listfiles(path.join(self.basepath, outdir))
                 for outdir in self.index['outdir']]

        if patterns:
            files = [list(filter(lambda f: match_any(path.basename(f), patterns), fs))
                    for fs in files]

        if len(files) == 1 and squash:
            return files[0]

        return files

    def tablefile(self, tablename, squash=True):
        files = self.files(tablename + '*', squash=False)
        # next() to get the first matching tablefile
        files = [next(filter(is_tablefile, fs)) for fs in files]

        if len(files) == 1 and squash:
            return files[0]

        return files

    def tablefiles(self, patterns=None, squash=True):
        files = self.files(patterns, squash=False)
        files = [list(filter(is_tablefile, fs)) for fs in files]

        if len(files) == 1 and squash:
            return files[0]

        return files

#
# Data conversion
#
def digitize(X, threshold=0):
    return np.where(X > threshold, 1, 0)

def bit_array(x, n_bits):
    """ Convert number x to array of bits """
    return np.array([(x & (1 << bit)) >> bit for bit in range(n_bits)])

def array_bit(a):
    """ Convert bit array a to number """
    return sum([(int(b) << bit) for (bit, b) in enumerate(a)])

def vector_grid(pos, vectors, grid_size=None, crop_width=None,
        win_shape=None, win_step=None, normalize=True, return_grid=False):
    """ Process vectors on a grid """

    # Map the vectors on a grid
    if grid_size:
        # fixed grid width x height
        grid = Grid.fixed_grid(pos, grid_size)
    else:
        # native grid
        grid = Grid(pos)

    XY = grid.center_grid()

    # Determine whether we have a time axis
    assert len(vectors.shape) in (3, 2)
    assert vectors.shape[-1] == 2
    time_axis = 1 if len(vectors.shape) == 3 else 0

    if time_axis:
        # vectors.shape = (time, spin_count, 2)
        # UV.shape = (time, height, width, 2)
        UV = np.array([grid.add_values(UVi) for UVi in vectors])
    else:
        # vectors.shape = (spin_count, 2)
        # UV.shape = (height, width, 2)
        UV = grid.add_values(vectors)

    if crop_width:
        XY = crop(XY, crop_width, axis=0)
        UV = crop(UV, crop_width, axis=time_axis)

    if win_shape:
        if not win_step:
            win_step = win_shape

        # XY.shape = (height, width, 2)
        win_shape += (1,)
        win_step += (1,)
        XY = rolling_window(XY, win_shape, win_step, method='mean')

        if time_axis:
            # UV.shape = (time, height, width, 2)
            win_shape = (1,) + win_shape
            win_step = (1,) + win_step

        UV = rolling_window(UV, win_shape, win_step, method='sum')

    if normalize:
        # Normalize vectors to unit length
        nmax = norm(UV.reshape((-1,2)), axis=-1).max()
        if nmax != 0:
            UV = UV / nmax

    if return_grid:
        return XY, UV, grid

    return XY, UV

#
# Data loading utilities
#
def load_output(dataset, quantity, t=None, grid_size=None, crop_width=None,
        win_shape=None, win_step=None, flatten=True):
    """ Load output vectors from dataset, with optional post-processing """

    assert len(dataset) == 1

    time, UV = read_vectors(dataset.tablefiles(), quantity, t)

    if grid_size or crop_width or win_shape:
        XY, angle = read_geometry(dataset.tablefile('geometry'))
        XY, UV = vector_grid(XY, UV, grid_size, crop_width, win_shape, win_step)

    if flatten:
        UV = UV.reshape((UV.shape[0], -1))

    return UV

def load_input(dataset, t=None, input_column='input'):
    """ Load input data from dataset """

    assert len(dataset) == 1

    df = read_table(dataset.tablefile('input'), index_col='t')
    df = df[input_column]

    if t is not None:
        if np.isscalar(t):
            t = [t]
        df = df.iloc[t]

    return np.array(df)
