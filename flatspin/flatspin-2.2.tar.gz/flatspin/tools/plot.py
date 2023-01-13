#!/usr/bin/env python3
import sys
import re
import numpy as np
import pandas as pd
import fnmatch
import itertools
import textwrap
from os import path
from joblib import delayed
import matplotlib.pyplot as plt

from flatspin.data import (Dataset, read_table, table_columns, col_group,
        match_column, match_columns, filter_df, save_table)

from flatspin.plotting import format_label, heatmap, format_labels
from flatspin.cmdline import (main_dataset_argparser, main_dataset,
        FilterAction, ProgressBar, ParallelProgress)

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

def aslist(a):
    if a is None:
        return []

    if not isinstance(a, list):
        return [a]

    return a

def astuple(a):
    if a is not None and not isinstance(a, tuple):
        a = (a,)
    return a

def pivot(df, index=None, columns=None, values=None):
    """ Alternative pivot which supports multiple columns for index/columns """
    if index:
        df = df.set_index(index)

    if columns:
        df = df.set_index(columns, append=True).unstack(columns)

    if values:
        df = df[values]

    return df

def load_one_dataset_tables(dataset, patterns=None, key=None, columns=None, table_filter=None):
    """ Load tables from one dataset """
    assert len(dataset) == 1

    df = pd.DataFrame()
    for f in dataset.tablefiles(patterns):
        cols = []
        if columns:
            # Skip tables that have none of the columns we're interested in
            tablecols = table_columns(f)
            matches = match_columns(columns, tablecols)
            if not matches:
                continue
            cols.extend(list(set(matches)))

        d = read_table(f)

        if not df.columns.intersection(d.columns).empty:
            # Join on common columns
            df = df.merge(d, how='outer')
        else:
            # No common columns -> join on index
            df = df.join(d, how='outer')

    if table_filter:
        df = filter_df(df, **table_filter)

    return df

def load_dataset_tables(dataset, patterns=None, key=None, columns=None, table_filter=None):
    """ Load tables from datasets """
    # Load tables from each dataset in parallell
    progress_bar = ProgressBar(desc="Loading tables", total=len(dataset))
    parallel = ParallelProgress(progress_bar, n_jobs=-1)

    dfs = parallel(
        delayed(load_one_dataset_tables)(ds, patterns, key, columns, table_filter)
        for ds in dataset)

    progress_bar.close()

    # Concatenate tables vertically, adding a column for the key
    key = aslist(key)
    if key:
        keys = list(dataset.index[key].itertuples(index=False))
    else:
        keys = list(dataset.index.index)
        key = ['idx']

    df = pd.concat(dfs, sort=False, axis=0, keys=keys, names=key)
    df = df.reset_index(level=key) # trick to get key as a column

    return df

def load_file_table(filename, table_filter=None):
    """ Load one table from file """
    df = read_table(filename)
    if table_filter:
        df = filter_df(df, **table_filter)
    return df

def load_file_tables(files, table_filter=None):
    """ Load tables from file """
    dfs = [load_file_table(f, table_filter) for f in files]
    df = pd.concat(dfs, sort=False, axis=0)
    return df

def aggregate(df, x=None, y=None, groupby=None, agg='mean'):
    """ Perform aggregation across one or more axes """
    x = aslist(x)
    y = aslist(y)
    groupby = aslist(groupby)

    if x and y:
        # Aggregate over x + y
        df = df.groupby(x + y).agg(agg).reset_index()
    elif x:
        # Aggregate over x + groupby (optional)
        grp = list(set(groupby + x))
        df = df.groupby(grp).agg(agg).reset_index()
    elif groupby:
        # Aggregate over index + groupby
        # Move original index to its own column
        df = df.reset_index()
        idx_col = df.columns[0]
        # Group by index col + groupby
        df = df.groupby(groupby + [idx_col]).agg(agg).reset_index()
        # Restore index
        df.set_index(idx_col, inplace=True)
        df.index.name = None
    else:
        # Aggregate over index only
        df = df.groupby(level=0).agg(agg)

    return df

def plot_xy(df, x=None, y=None, groupby=None, agg=None, xlim=None, ylim=None, **kwargs):
    """ Plot x vs y as lines """
    y = aslist(y) if y else None
    groupby = aslist(groupby)

    agg_label = False
    if agg:
        orig_len = len(df)
        df = aggregate(df, x, None, groupby, agg)
        new_len = len(df)
        if new_len < orig_len:
            print(f"Aggregating ({agg}): {orig_len} rows -> {new_len} rows")
            agg_label = True

    if groupby and x not in groupby:
        df = pivot(df, columns=groupby)
        #df = df.set_index(groupby, append=True).unstack(groupby)
        if agg_label:
            df.columns.set_names(f'{agg}(y)', level=0, inplace=True)
        else:
            df.columns.set_names('y', level=0, inplace=True)

    fig, ax = plt.subplots()

    if isinstance(df.columns, pd.MultiIndex):
        levels = list(range(1, df.columns.nlevels))
        for key, d in df.groupby(level=levels, axis=1):
            d = d.dropna(how='all')
            key = astuple(key)
            xi = (x,) + key if x else None
            d.plot(x=xi, y=y, ax=ax, **kwargs)
        plt.xlabel(x)
    else:
        if agg_label:
            df = df.rename(columns={col: f"{agg}({col})" for col in df.columns if col != x})
            y = [f"{agg}({col})" for col in y] if y else None
        df.plot(x=x, y=y, ax=ax, **kwargs)

    if xlim:
        plt.xlim(*xlim)
    if ylim:
        plt.ylim(*ylim)

    connect_picker(fig, ax)

def plot_xyz(df, x=None, y=None, z=None, groupby=None, agg=None, xlim=None, ylim=None, zlim=None):
    """ Plot x vs y vs z as heatmap """
    x = aslist(x)
    y = aslist(y)
    z = aslist(z)
    groupby = aslist(groupby)

    zlabel = 'z'
    if len(z) == 1:
        zlabel = z[0]

    if agg:
        orig_len = len(df)
        df = aggregate(df, x, y, groupby, agg)
        new_len = len(df)
        if new_len < orig_len:
            print(f"Aggregating ({agg}): {orig_len} rows -> {new_len} rows")
            zlabel = f"{agg}({zlabel})"

    index = x[0] if len(x) == 1 else x if x else None
    columns = y[0] if len(y) == 1 else y if y else None
    values = z[0] if len(z) == 1 else z if z else None

    if groupby and not y:
        # Plot each column as a row in the heatmap
        columns = groupby
        df = pivot(df, index=index, columns=groupby)
    else:
        df = pivot(df, index=index, columns=columns, values=values)

    if isinstance(df.columns, pd.MultiIndex) and df.columns.names[0] is None:
        df.columns.set_names('y', level=0, inplace=True)

    xlabel = format_label(df.index.names)
    ylabel = format_label(df.columns.names)

    pcolor = heatmap(df.index, df.columns, df.T, xlabel, ylabel, zlabel, xlim, ylim, zlim)

    plt.colorbar(pcolor, label=zlabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def func_atan(x):
    return np.rad2deg(np.arctan2(x[1], x[0]))

funcs = {
    'norm': np.linalg.norm,
    'atan': func_atan,
}

def parse_func(column):
    """ Parse column function

    New columns may be specified in the form:
        name=function(col1 col2 col3)

    Returns a tuple (name, function, [col1, col2, col3])
    """
    m = re.match(r'(\w+)=(\w+)\((.*)\)', column)
    if m:
        name = m.group(1)
        fn = m.group(2)
        fn = funcs.get(fn, fn)
        cols = list(map(str.strip, m.group(3).split()))
        return (name, fn, cols)

    # Not a function (nop)
    return (column, None, [column])

def parse_funcs(columns):
    """ Parse column functions """
    names = []
    cols = []
    functions = []

    for c in columns:
        name, func, col = parse_func(c)
        names.append(name)
        cols.extend(col)
        if func:
            functions.append((name, func, col))

    return names, cols, functions

def main_plot(dataset, args):
    # Columns to plot
    x = None
    y = None
    z = None

    # Any function specifications
    # name=func(cols)
    # functions is a list of (name, func, cols) tuples
    functions = []

    # List of columns we need from the tables
    columns = []

    # Parse any functions for -x -y and -z
    if args.x:
        x, cols, funcs = parse_funcs(args.x)
        columns.extend(cols)
        functions.extend(funcs)

    if args.y:
        y, cols, funcs = parse_funcs(args.y)
        columns.extend(cols)
        functions.extend(funcs)

    if args.z:
        z, cols, funcs = parse_funcs(args.z)
        columns.extend(cols)
        functions.extend(funcs)

    #print(f"x={x} y={y} z={z} (args)")
    #print(f"columns={columns}")
    #print(f"functions={functions}")

    # Load tables
    patterns = [(p, p + '.*') for p in args.tables]
    patterns = list(itertools.chain(*patterns))

    dfs = []
    if dataset:
        df = load_dataset_tables(dataset, patterns, args.groupby, columns, args.table_filter)
        dfs.append(df)

    if args.files:
        df = load_file_tables(args.files, args.table_filter)
        dfs.append(df)

    df = pd.concat(dfs, sort=False, axis=0)

    # Round columns a bit
    df = df.round(10)

    # Apply functions as new columns
    # TODO: support for functions returning multiple values?
    for name, fn, cols in functions:
        cols = match_columns(cols, df.columns) or cols
        # ... or cols to cause KeyError when no match
        df[name] = df[cols].agg(fn, axis=1)

    # Now that we have the table, we can determine which columns to plot
    # (some column arguments may be patterns, e.g., "spin*x")
    if x:
        x = match_columns(x, df.columns) or x
    if y:
        y = match_columns(y, df.columns) or y
    if z:
        z = match_columns(z, df.columns) or z

    print(f"x={x} y={y} z={z}")

    groupby = args.groupby
    if dataset and not args.groupby:
        # Group by the dataset index by default
        groupby = 'idx'

    if z or y:
        # Keep only columns we're interested in
        xyz = aslist(x) + aslist(y) + aslist(z)
        df = df[list(set(xyz + aslist(groupby)))]

        # Drop rows where x, y and z are all NaN
        df = df.dropna(how='all', subset=xyz)

    if x:
        # Drop rows where x is NaN
        df = df.dropna(subset=x, how='any')
    if z and y:
        # Drop rows where y is NaN
        df = df.dropna(subset=y, how='any')

    print(df)

    if args.table_out:
        print("Saving table {}".format(args.table_out))
        save_table(df, args.table_out)

    if args.z:
        # 3D plot
        plot_xyz(df, x, y, z, groupby, args.aggregate, args.xlim, args.ylim, args.zlim)

    else:
        # 2D plot
        if x and len(x) > 1:
            raise ValueError("Multiple columns on x axis is not supported")
        x = x[0] if x else None

        plot_xy(df, x, y, groupby, args.aggregate, args.xlim, args.ylim,
                marker=args.marker, linestyle=args.linestyle)

    # Set the title
    title = args.title
    if dataset and title:
        params = dataset.params
        params.update(dataset.row(0))
        kw = {'name': dataset.name, 'basepath': dataset.basepath,
              'index': dataset.id(0), 'params': params}
        kw.update(params)
        kw.update(dataset.info)
        title = title.format(**kw)

    plt.title(title)

    if args.output:
        print("Saving figure {}".format(args.output))
        plt.savefig(args.output, dpi=args.dpi)
    else:
        plt.show()

    return 0

def main_list_cols(dataset, args):
    if dataset:
        for ds in dataset:
            patterns = [(p, p + '.*') for p in args.tables]
            patterns = list(itertools.chain(*patterns))
            files = ds.tablefiles(patterns)
            columns = list(map(table_columns, files))
            for filename, cols in zip(files, columns):
                print(f"{filename}:")
                print(f"  columns ({len(cols)}):")
                print(textwrap.fill(", ".join(cols), initial_indent="  ", subsequent_indent="  "))

    if args.files:
        columns = list(map(table_columns, args.files))
        for filename, cols in zip(args.files, columns):
            print(f"{filename}")
            print(f"  columns ({len(cols)}):")
            print(textwrap.fill(", ".join(cols), initial_indent="  ", subsequent_indent="  "))

    return 0


# Parser needs to be accessible at module level for sphinxcontrib.autoprogram
parser = main_dataset_argparser("Plot table data.")

parser.add_argument('-f', '--files', nargs='*',
        help='tables to load from file')
parser.add_argument('-g', '--tables', nargs='+', default=[],
        help='tables to load from the dataset')
parser.add_argument('-k', '--groupby', nargs='*',
        help='group by column(s)')
parser.add_argument('-v', '--list-cols', action='store_true',
        help='list available columns')
parser.add_argument('-x', nargs='*',
        help='name of column(s) to use for x axis')
parser.add_argument('-y', nargs='*',
        help='name of column(s) to use for y axis')
parser.add_argument('-z', nargs='*',
        help='name of column(s) to use for z axis')
parser.add_argument('-a', '--aggregate',
        help='aggregate method')
parser.add_argument('-c', '--table-filter', action=FilterAction, default={},
        help='select a subset of the table (column=value)')
parser.add_argument('--xlim', nargs=2, type=float, metavar=('XMIN', 'XMAX'))
parser.add_argument('--ylim', nargs=2, type=float, metavar=('YMIN', 'YMAX'))
parser.add_argument('--zlim', nargs=2, type=float, metavar=('ZMIN', 'ZMAX'))
parser.add_argument('--title', help='title format string')
parser.add_argument('--marker', help='marker style (XY plots only)')
parser.add_argument('--linestyle', help='line style (XY plot only)')
parser.add_argument('-to', '--table-out', help='dump result table to file')
parser.add_argument('--dpi', type=int, default=100,
        help='dots per inch (default: %(default)s)')

def main():
    args = parser.parse_args()

    # With -f, we won't load dataset tables unless explicitly told to with -b/--datapath
    ds = None
    if not args.files or args.datapath is not None:
        ds = main_dataset(args)

    if args.list_cols:
        return main_list_cols(ds, args)

    return main_plot(ds, args)

if __name__ == '__main__':
    main()
