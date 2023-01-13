"""
Command-line related utilities
"""
import sys
import re
import argparse
import fnmatch
import numpy as np
from glob import glob
from collections import OrderedDict
import copy
from tqdm.auto import tqdm
from joblib import Parallel

from flatspin import __version__
from flatspin.data import Dataset
from flatspin.data import read_table

class StoreKeyValue(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        k, v = values.split('=')
        if getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, OrderedDict())
        d = getattr(namespace, self.dest)
        d[k] = self.parse_value(v)

    def parse_value(self, value):
        return value

class IndexAction(argparse.Action):
    """ index or start:stop:step (all ints) """
    def __call__(self, parser, namespace, values, option_string=None):
        v = parse_index(values)
        setattr(namespace, self.dest, v)

class FilterAction(StoreKeyValue):
    """ key=<filter> where <filter>=start or start:stop (arbitrary types) """
    def parse_value(self, value):
        return parse_filter(value)

class SizeAction(argparse.Action):
    """ <size> or <sizex>x<sizey> """
    def __call__(self, parser, namespace, values, option_string=None):
        v = parse_size(values)
        setattr(namespace, self.dest, v)

class CropAction(argparse.Action):
    """ crop window <crop> or <cropx>,<cropy> where <crop> is before or before:after """
    def __call__(self, parser, namespace, values, option_string=None):
        v = parse_crop(values)
        setattr(namespace, self.dest, v)

class WindowAction(argparse.Action):
    """ window size <sizex>x<sizey> [<stepx>,<stepy>] """
    def __call__(self, parser, namespace, values, option_string=None):
        v = parse_window(values)
        setattr(namespace, self.dest, v)

class DropDuplicatesAction(argparse.Action):
    """column name or 'name1, name2, ..."""
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, list())
        v = values if values else None
        getattr(namespace, self.dest).append(v)

def parse_index(index_str):
    """ index or start:stop:step (all ints) """
    if ':' in index_str:
        s = index_str.split(':')
        s = list(map(lambda i: int(i) if len(i)>0 else None, s))
        return slice(*s)
    elif '[' in index_str:
        import ast
        return ast.literal_eval(index_str)
    return int(index_str)

def parse_filter(filter_str):
    """ start or start:stop (arbitrary types) """
    if ':' in filter_str and 'lambda' not in filter_str:
        s = filter_str.split(':')
        s = tuple(map(lambda i: parse_filter(i) if len(i)>0 else None, s))
        return slice(*s)
    try:
        return eval(filter_str, {}, {})
    except:
        return filter_str

def parse_size(size):
    """ <size> or <sizex>x<sizey> """
    if 'x' in size:
        return tuple(map(int, size.split('x')))

    return (int(size), int(size))

def parse_crop(crop):
    """ crop window <crop> or <cropx>,<cropy> where <crop> is before or before:after """
    def parse_one_crop(crop):
        if ':' in crop:
            before, after = crop.split(':')
        else:
            before = crop
            after = before

        before = int(before) if before else 0
        after = int(after) if after else 0

        return (before, after)

    if ',' in crop:
        cropx, cropy = tuple(map(parse_one_crop, crop.split(',')))
        return (cropy, cropx)

    crop = parse_one_crop(crop)

    return (crop, crop)

def parse_window(window):
    """ window size <sizex>x<sizey> [<stepx>,<stepy>] """
    try:
        size, step = window
    except ValueError:
        size = window[0]
        step = None

    sizex, sizey = parse_size(size)
    size = (sizey, sizex)

    if step:
        if "," in step:
            stepx, stepy = tuple(map(int, step.split(',')))
            step = (stepy, stepx)
        else:
            step = int(step)
            step = (step, step)
    else:
        step = size

    return size, step

def parse_func(func_str):
    """ fn(arg1, arg2, ...) """
    m = re.match(r'(\w+)\((.*)\)', func_str)
    if m:
        fn = m.group(1)
        c = tuple(map(str.strip, m.group(2).split(',')))
        return (fn,) + c

    return None

def parse_time(time_str, ctx={}):
    """ start:stop:step (arbitrary types, with local ctx) OR index """
    if ":" not in time_str:
        # single index
        return eval(time_str, {}, ctx)

    s = []
    for i in time_str.split(':'):
        if len(i) > 0:
            s.append(eval(i, {}, ctx))
        else:
            s.append(None)
    return slice(*s)

# Functions available to eval_param()
def func_bin(values):
    values = np.array(values, dtype=int)
    max_value = np.max(values)
    assert max_value >= 0, "Values must be unsigned"
    if max_value == 0:
        n_bits = 1
    else:
        n_bits = int(np.floor(np.log2(max_value)) + 1)
    fmt = '{:0' + str(n_bits) + 'b}' # ugh
    bits = list(map(fmt.format, values))
    return bits

def func_randint(low=sys.maxsize, *args, **kwargs):
    return np.random.randint(low, *args, **kwargs)

def func_randseed(n):
    return np.random.randint(2**32, size=n, dtype='int64')

def func_glob(pathname):
    return sorted(glob(pathname))

def func_read_table(table):
    df = read_table(table)
    return df.values


param_globals = {
    'np': np,
    'bin': func_bin,
    'randint': func_randint,
    'randseed': func_randseed,
    'glob': func_glob,
    'inf': np.inf,
    'read_table': func_read_table,
}

def eval_param(v, ctx=None):
    """ Try to eval(v), on failure return v """
    try:
        return eval(v, param_globals, ctx)
    except:
        return v

def eval_params(params, ctx=None):
    d = dict(ctx) if ctx else {}
    for k,v in params.items():
        d[k] = eval_param(v, ctx=d)
    return d

class ProgressBar(tqdm):
    pass

class ParallelProgress(Parallel):
    def __init__(self, progress_bar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._progress_bar = progress_bar

    def print_progress(self):
        inc = self.n_completed_tasks - self._progress_bar.n
        self._progress_bar.update(inc)

def main_dataset_argparser(description, output_required=False):
    """ Common argparser for scripts which deal with a dataset """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-b', '--datapath', metavar='DATA_PATH',
            help='path to dataset (default: %(default)s)')
    parser.add_argument('-i', '--subset', action=IndexAction, metavar='INDEX',
            help='select a subset of the dataset by index')
    parser.add_argument('-s', '--filter', action=FilterAction, default={},
            help='filter a subset of the dataset by parameter')
    parser.add_argument('-l', '--list', action='store_true',
            help='list the dataset')
    parser.add_argument('-o', '--output', required=output_required,
            metavar='FILE', help='save result(s) to file(s)')
    parser.add_argument('-d', '--drop-duplicates', action=DropDuplicatesAction, nargs="*",
            help='drop duplicates, <column name> or "<column name 1>, ... ,<column name n>"')
    parser.add_argument('-V', '--version', help='display flatspin version', action='store_true')

    return parser

def main_dataset_grid_argparser(description, output_required=False):
    """ Common argparser for scripts dealing with grid operations on a dataset """
    parser = main_dataset_argparser(description, output_required)

    parser.add_argument('-t', default='::spp',
            help='time range start:stop:step (default: %(default)s)')
    parser.add_argument('-g', '--grid', action=SizeAction,
            help='grid size <size> or <sizex>x<sizey> (set GRID to 0 to disable grid)')
    parser.add_argument('-c', '--crop', action=CropAction,
            help='''crop window CROP or CROPx,CROPy where CROP is before or before:after
                    (when GRID is 0, CROP,CROPx,CROPy denote the percentage to crop)''')
    parser.add_argument('-w', '--window', action=WindowAction, nargs='+',
            help='window size <sizex>x<sizey> [<stepx>,<stepy>]')

    return parser

def main_version(args):
    print(f'flatspin version {__version__}')

def main_dataset(args):
    """ Common main function for scripts which deal with a dataset """
    if args.version:
        main_version(args)
        sys.exit(0)

    datapath = args.datapath if args.datapath else '.'
    ds = Dataset.read(datapath)

    if args.filter:
        kwargs = args.filter
        ds = ds.filter(**kwargs)

    if args.subset is not None:
        if type(args.subset) == list:
            ds = ds[args.subset]
        else:
            key = args.subset
            ds = ds[key]

    if args.drop_duplicates is not None:
        for drop_dup in args.drop_duplicates:
            ds = ds.drop_duplicates(subset=drop_dup)

    if args.list:
        print(ds)
        sys.exit(0)

    return ds

