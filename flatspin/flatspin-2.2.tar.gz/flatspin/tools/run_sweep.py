#!/usr/bin/env python3
import sys
import os
import argparse
import shlex
import numpy as np
import pandas as pd
from collections import OrderedDict
from copy import copy

from flatspin import __version__
from flatspin.cmdline import StoreKeyValue, eval_params, main_version
from flatspin.sweep import sweep
from flatspin.data import Dataset, table_formats, is_archive_format, read_table, eval_dict
from flatspin.runner import run, run_local, run_dist
from flatspin import runner
from flatspin.utils import get_default_params, import_class
from .run import main_list_params, main_list_encoders, main_help_encoder, visualize_run

# Parser needs to be accessible at module level for sphinxcontrib.autoprogram
parser = argparse.ArgumentParser(description='Run flatspin sweep.')
parser.add_argument('-r', '--run', choices=['local', 'dist', 'none'], default='local',
                    help='run locally or distributed on a cluster')
parser.add_argument('-p', '--param', action=StoreKeyValue, default={},
                    help='set model parameter key=value')
parser.add_argument('-s', '--sweep', action=StoreKeyValue, metavar='key=SPEC',
                    help='set sweep parameter key=SPEC')
parser.add_argument('-n', '--repeat', type=int, default=1, metavar='N',
                    help='repeat each experiment N times (default: %(default)s)')
parser.add_argument('-ns', '--repeat-spec', action=StoreKeyValue, metavar='key=SPEC',
                    help='repeat each according to key=SPEC')
parser.add_argument('--seed', type=int, default=0, help='random seed')
parser.add_argument('-m', '--model', default='SquareSpinIceClosed',
        help='name of model (default: %(default)s) ')
parser.add_argument('-e', '--encoder', default='Sine',
        help='input encoder (type of external field, default: %(default)s)')
parser.add_argument('-o', '--basepath', help='output directory for results')
parser.add_argument('-f', '--format', choices=table_formats.keys(), default='npz',
        help='format of output files (default: %(default)s)')
parser.add_argument('--params-file',
        help='load parameters from file (params.csv), loaded before -p')
parser.add_argument('--sweep-file', help='load sweep (index.csv) from file')
parser.add_argument('--list-params', action='store_true')
parser.add_argument('--list-encoders', action='store_true')
parser.add_argument('--help-encoder', action='store_true')
parser.add_argument('-V', '--version', help='display flatspin version', action='store_true')
parser.add_argument('--show-plot', help='plot the state as the simulation runs', action='store_true')

def main():
    args = parser.parse_args()

    if args.version:
        return main_version(args)
    if args.list_params:
        return main_list_params(args)

    if args.list_encoders:
        if args.encoder == parser.get_default('encoder'):
            args.encoder = 'flatspin.encoder'
        return main_list_encoders(args)

    if args.help_encoder:
        return main_help_encoder(args)

    if args.basepath is None or (args.sweep is None and args.sweep_file is None):
        parser.error('The following arguments are required: -o/--basepath, -s/--sweep/--sweep-file')

    if args.sweep and args.sweep_file:
        parser.error('Cannot have both -s/--sweep and --sweep-file')

    model_class = import_class(args.model, 'flatspin.model')
    model_name = model_class.__name__
    encoder_class = import_class(args.encoder, 'flatspin.encoder')

    # -e Sine is really just an alias for -p encoder=Sine
    params = get_default_params(run)
    params['encoder'] = f'{encoder_class.__module__}.{encoder_class.__name__}'
    params.update(get_default_params(model_class))
    params.update(get_default_params(encoder_class))

    if args.params_file:
        prms = read_table(args.params_file)
        prms = dict(np.array(prms))
        prms = eval_dict(prms)
        params.update(prms)

    params.update(eval_params(args.param))

    info = {
        'model': f'{model_class.__module__}.{model_class.__name__}',
        'model_name': model_name,
        'data_format': args.format,
        'command': ' '.join(map(shlex.quote, sys.argv)),
        'version': __version__,
    }


    ext = args.format if is_archive_format(args.format) else "out"
    if args.repeat > 1 or args.repeat_spec:
        outdir_tpl = model_name + ".{:06d}.{:06d}." + ext
    else:
        outdir_tpl = model_name + ".{:06d}." + ext

    basepath = args.basepath

    if args.sweep_file:
        # Load index from file
        index = read_table(args.sweep_file)
        if not 'outdir' in index:
            # Generate outdir column
            outdirs = list(map(outdir_tpl.format, range(len(index))))
            index['outdir'] = outdirs

    else:
        # Generate index
        index = []

        for i, j, sweep_params in sweep(args.sweep, args.repeat, args.repeat_spec, params, args.seed):

            outdir = outdir_tpl.format(i, j)
            outpath = os.path.join(basepath, outdir)

            row = OrderedDict(sweep_params)
            row.update({'outdir': outdir})
            index.append(row)

        index = pd.DataFrame(index)

    if os.path.exists(basepath):
        # Refuse to overwrite an existing dataset
        raise FileExistsError(basepath)
    os.makedirs(basepath)

    # Save dataset
    dataset = Dataset(index, params, info, basepath)
    dataset.save()

    # Run!
    print("Starting sweep with {} runs".format(len(dataset)))
    if args.run == 'local':
        if args.show_plot:
            runner.run_sample_callback = visualize_run
        run_local(dataset)

    elif args.run == 'dist':
        run_dist(dataset)

if __name__ == '__main__':
    main()
