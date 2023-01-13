#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataset statistics.
"""
import numpy as np
import pandas as pd
from joblib import delayed
from flatspin.data import Dataset, read_table, save_table
from flatspin.cmdline import *

def load_stats(ds):
    df = read_table(ds.tablefile('stats'))
    col0, col1 = df.columns
    keys = list(df[col0])
    values = list(df[col1].astype(float))
    df = pd.DataFrame([values], columns=keys)
    return df

def main_stats(dataset, args):
    # Do it in parallell
    progress_bar = ProgressBar(desc="Stats", total=len(dataset))
    parallel = ParallelProgress(progress_bar, n_jobs=-1)

    stats = parallel(delayed(load_stats)(ds) for ds in dataset)

    progress_bar.close()

    df = pd.concat(stats, ignore_index=True)

    if args.output:
        out = pd.concat([dataset.index, df], axis=1)
        save_table(out, args.output)
    #df['runtime'] = pd.to_timedelta(df['runtime'], unit='s')

    stats = OrderedDict()
    for col, d in df.items():
        stats[col] = [ d.count(), d.mean(), d.std(), d.min(), d.max(), d.sum() ]
    stats = pd.DataFrame(stats, index=['count', 'mean', 'std', 'min', 'max', 'sum'])

    pd.options.display.float_format = '{:.1f}'.format
    print(stats)

# Parser needs to be accessible at module level for sphinxcontrib.autoprogram
parser = main_dataset_argparser(__doc__)

parser.add_argument('-q', '--stats', nargs='+', default=['runtime'],
        help='type of stats')

def main():
    args = parser.parse_args()

    ds = main_dataset(args)

    return main_stats(ds, args)

if __name__ == '__main__':
    main()
