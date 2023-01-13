# -*- coding: utf-8 -*-
"""
Check the health of a dataset.
"""
import os
import numpy as np
import pandas as pd
from flatspin.data import Dataset, read_table
from flatspin.cmdline import *

def main_fsck(dataset, args):
    if len(dataset) == 0:
        print(f"Dataset is empty, nothing to do")
        return 1

    missing = ~dataset.index['outdir'].apply(os.path.exists)
    missing = dataset.index[missing]

    if len(missing) > 0:
        print(f"Missing data for {len(missing)} runs")
        if args.verbose:
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', int(os.getenv('COLUMNS') if os.getenv('COLUMNS') is not None else None))
            print(missing)
        return 2
    else:
        print(f"Dataset appears healthy :)")
        return 0


# Parser needs to be accessible at module level for sphinxcontrib.autoprogram
parser = main_dataset_argparser(__doc__)
parser.add_argument('-v', '--verbose', action='store_true')

def main():
    args = parser.parse_args()

    ds = main_dataset(args)

    return main_fsck(ds, args)

if __name__ == '__main__':
    main()
