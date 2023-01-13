#!/usr/bin/env python3
import sys
import re
import numpy as np
import pandas as pd
import fnmatch
import itertools
from os import path
from numpy.linalg import norm
import matplotlib.pyplot as plt

from flatspin.data import (
        Dataset, table_columns, read_tables, match_column,
        match_columns, col_group)

from flatspin.utils import *
from flatspin.cmdline import *

def func_norm(x):
    x = np.array(x)
    if np.all(x[:,1] == 0):
        d = x[:,0] # x direction
    else:
        d = x[:,1] # y direction
    return (norm(x, axis=1) * np.where(d >= 0, 1, -1)).reshape((-1, 1))

def func_atan(x):
    x = np.array(x)
    return np.rad2deg(np.arctan(x[:,1] / x[:,0])).reshape((-1, 1))

def func_mean(x):
    return np.mean(x, axis=1)

def func_sum(x):
    return np.sum(x, axis=1)

funcs = {
    'norm': func_norm,
    'atan': func_atan,
    'mean': func_mean,
    'sum': func_sum,
}

def connect_picker(fig, ax):
    leg = ax.get_legend()
    leg._line_highlight = -1
    #leg = axes[0].legend(loc='upper left', bbox_to_anchor=(1.0, 1.05))

    for i, (legline, legtext) in enumerate(zip(leg.get_lines(), leg.get_texts())):
        #line.set_picker(5) # 5 pts tolerance
        legline.set_picker(5)
        legtext.set_picker(5)
        legline._line_index = i
        legtext._line_index = i

    def onpick(event):
        if leg._line_highlight < 0:
            leg._line_highlight = event.artist._line_index
        else:
            leg._line_highlight = -1

        for j, line in enumerate(ax.get_lines()):
            if j == leg._line_highlight or leg._line_highlight < 0:
                line.set_alpha(1.0)
                line.set_zorder(10)
            else:
                line.set_alpha(0.1)
                line.set_zorder(0)
        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', onpick)

def load_table(dataset, args):
    files = dataset.tablefiles(args.patterns)
    files = [f for f in files if 't' in table_columns(f)]
    df = read_tables(files, index_col='t')

    columns = []
    functions = []
    x = args.x if args.x else None
    if x:
        cols = match_column(x, df.columns)
        if cols:
            assert len(cols) == 1, "can't have multiple columns on x axis"
            columns.extend(cols)
        else:
            # not a column, is it a function?
            m = parse_func(x)
            assert m, f"Unknown column: {x}"
            fn, cols = m[0], m[1:]
            assert fn in funcs, f"Unknown function: {fn}"
            fn = funcs[fn]
            cols = match_columns(cols, df.columns)
            columns.extend(cols)
            functions.append((args.x, fn, cols))

    if args.columns:
        # k -> [columns] or func(columns)
        # need: list of cols to load
        # need: list of functions to apply
        # need: list of ys to plot
        y = []
        for c in args.columns:
            cols = match_column(c, df.columns)
            if cols:
                columns.extend(cols)
                y.extend(cols)
            else:
                # not a column, is it a function?
                m = parse_func(c)
                assert m, f"Unknown column: {c}"
                fn, cols = m[0], m[1:]
                assert fn in funcs, f"Unknown function: {fn}"
                fn = funcs[fn]
                cols = match_columns(cols, df.columns)
                columns.extend(cols)
                functions.append((c, fn, cols))
                y.append(c)

    else:
        columns = df.columns
        functions = []
        y = df.columns

    assert x not in y, "can't plot x against itself, sorry"

    columns = unique_list(columns)

    # print("columns=", columns)
    # print("functions=", functions)
    # print("x=", x)
    # print("y=", y)

    t = parse_time(args.t, numeric_dict(dataset.params))
    df = df[columns]
    df = df.iloc[t]

    # Apply functions
    for name, func, cols in functions:
        df[name] = func(df[cols])

    if x:
        df = df.set_index(x)

    df = df[y]

    return df

def get_title(dataset, fmt=None):
    param = dataset.index.columns[0]
    if not fmt:
        fmt = param + "={" + param + "}"
    params = dataset.params
    params.update(dataset.row(0))
    kw = {'name': dataset.name, 'basepath': dataset.basepath,
          'index': dataset.id(0), 'params': params}
    kw.update(params)
    kw.update(dataset.info)
    title = fmt.format(**kw)
    return title

def main_table(dataset, args):
    tables = [load_table(ds, args) for ds in dataset]

    plot_kwargs = {}
    if args.marker:
        plot_kwargs['marker'] = args.marker

    if args.single_fig:
        for ds, df in zip(dataset, tables):
            title = get_title(ds, args.title)
            label = f" [{title}]"
            df.columns = [c + label for c in df.columns]
            df.plot(ax=plt.gca(), **plot_kwargs)
    else:
        for ds, df in zip(dataset, tables):
            title = get_title(ds, args.title)
            fig = plt.figure()
            ax = plt.gca()
            df.plot(ax=ax, title=title, **plot_kwargs)
            connect_picker(fig, ax)

    if args.ylim:
        for n in plt.get_fignums():
            plt.figure(n)
            plt.ylim(args.ylim)

    if args.output:
        figs = plt.get_fignums()
        if len(figs) == 1:
            print(args.output)
            plt.savefig(args.output)
        else:
            base, ext = path.splitext(args.output)
            ext = ext.lstrip('.')
            for i, f in enumerate(figs):
                filename = f'{base}-{i}.{ext}'
                print(filename)
                plt.figure(f)
                plt.savefig(filename)
    else:
        plt.show()

    return 0

def main_list_cols(dataset, args):
    for ds in dataset:
        files = ds.tablefiles(args.patterns)
        columns = list(map(table_columns, files))
        for filename, cols in zip(files, columns):
            if not 't' in cols:
                continue
            print(f"{filename}:")
            groups = [list(g) for (k,g) in itertools.groupby(cols, col_group)]
            for g in groups:
                print("    {}".format(", ".join(g)))

    return 0

def main():
    parser = main_dataset_argparser("Plot table data")

    parser.add_argument('-g', '--patterns', nargs='+',
            help='table patterns (default: %(default)s)')
    parser.add_argument('-v', '--list-cols', action='store_true',
            help='list available columns')
    parser.add_argument('-t', default='::1',
            help='time range start:stop:step')
    parser.add_argument('-x',
            help='x axis column')
    parser.add_argument('--ylim', nargs=2, type=float, metavar=('YMIN', 'YMAX'),
            help='set ylim')
    parser.add_argument('-y', '--columns', nargs='*',
            help='list of columns to plot')
    parser.add_argument('--title',
            help='title format string')
    parser.add_argument('--marker', help='marker style')
    parser.add_argument('-1', '--single-fig', action='store_true',
            help='plot everything in a single figure')

    args = parser.parse_args()

    ds = main_dataset(args)

    if args.list_cols:
        return main_list_cols(ds, args)

    return main_table(ds, args)

if __name__ == '__main__':
    main()
