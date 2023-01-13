#!/usr/bin/env python3
import numpy as np
from os import listdir
import time

from flatspin.cmdline import *

def get_completed(basepath, outdirs):
    files = listdir(basepath)
    return len(set(outdirs).intersection(set(files)))

def main_progress(dataset, args):
    assert args.interval >= 0.1

    outdirs = dataset.index['outdir']

    total = len(outdirs)
    completed = get_completed(dataset.basepath, outdirs)

    progress_bar = ProgressBar(desc="Completed", total=total, initial=completed)

    while completed < total:
        comp = get_completed(dataset.basepath, outdirs)
        delta = comp - completed
        if delta:
            progress_bar.update(delta)
        completed = comp
        time.sleep(args.interval)

    return 0


# Parser needs to be accessible at module level for sphinxcontrib.autoprogram
parser = main_dataset_argparser("Monitor progress of a flatspin run.")
parser.add_argument('-n', '--interval', type=float, default=60,
        help='Update interval (default: %(default)s seconds)')

def main():
    args = parser.parse_args()

    ds = main_dataset(args)

    return main_progress(ds, args)

if __name__ == '__main__':
    main()
