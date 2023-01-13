#!/usr/bin/env python3
import os
import time
from joblib import delayed
from flatspin.data import *
from flatspin.cmdline import *

def convert_tables(outdir, tablefiles, data_format):
    if not is_archive(outdir):
        os.makedirs(outdir)

    for src in tablefiles:
        df = read_table(src)
        head, tail = os.path.split(src)
        name, ext = os.path.splitext(tail)

        if not is_archive(outdir):
            name = f"{name}.{data_format}"

        dst = os.path.join(outdir, name)
        save_table(df, dst)

def convert_dataset(dataset, destdir, fmt):
    if os.path.exists(destdir):
        # Refuse to overwrite an existing dataset
        raise FileExistsError(destdir)

    os.makedirs(destdir)

    queue = []
    keys = []
    new_outdir = []
    for i, tablefiles in enumerate(dataset.tablefiles(squash=False)):
        row = dataset.row(i)
        outdir = row['outdir']
        base, ext = os.path.splitext(outdir)
        if is_archive_format(fmt):
            outdir = f"{base}.{fmt}"
        else:
            outdir = f"{base}.out"
        new_outdir.append(outdir)

        dst = os.path.join(destdir, outdir)
        queue.append([dst, tablefiles, fmt])

    dataset.index['outdir'] = new_outdir
    dataset.save(destdir)

    queue = [delayed(convert_tables)(*q) for q in queue]

    progress_bar = ProgressBar(desc="dataset-convert", total=len(queue))
    parallel = ParallelProgress(progress_bar, n_jobs=1)
    parallel(queue)

    progress_bar.close()


# Parser needs to be accessible at module level for sphinxcontrib.autoprogram
parser = main_dataset_argparser("Convert between dataset formats.")

parser.add_argument('-f', '--format', choices=table_formats.keys(), default='npy',
        help='format of output files (default: %(default)s)')

def main():
    args = parser.parse_args()

    ds = main_dataset(args)

    convert_dataset(ds, args.output, args.format)

if __name__ == '__main__':
    main()
