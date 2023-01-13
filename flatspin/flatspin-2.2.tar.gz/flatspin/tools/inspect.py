#!/usr/bin/env python3
import itertools
from os import path

from flatspin.data import Dataset, table_columns
from flatspin.cmdline import *

def main_inspect(dataset, args):
    for i, ds in dataset.items():
        print(f"[{i}] ", end='')
        print(" ".join(f"{k}={v}" for k,v in dict(ds.row()).items()), end='')
        print(":")

        tablefiles = ds.tablefiles()
        print(f"    tables ({len(tablefiles)}): ", end='')
        tabletypes = ["[t]" if "t" in table_columns(f) else "" for f in tablefiles]
        print(", ".join(f + t for (f, t) in zip(map(path.basename, tablefiles), tabletypes)))

        files = set(ds.files()) - set(tablefiles)
        if files:
            print(f"    files ({len(files)}): ", end='')
            files = sorted(files, key=lambda f: f[::-1])
            files = itertools.groupby(files, key=lambda f: path.splitext(f)[1][1:])
            print(", ".join(f"{ext} ({len(list(group))})" for ext, group in files if ext))

    return 0


# Parser needs to be accessible at module level for sphinxcontrib.autoprogram
parser = main_dataset_argparser("Inspect the contents of a dataset.")

def main():
    args = parser.parse_args()

    ds = main_dataset(args)

    return main_inspect(ds, args)

if __name__ == '__main__':
    main()
