#!/usr/bin/env python3
import sys
import os
import argparse
import shlex
import numpy as np
import pandas as pd
import importlib
import inspect
import matplotlib.pyplot as plt

from flatspin import __version__
from flatspin.cmdline import StoreKeyValue, eval_params, main_version
from flatspin.data import Dataset, table_formats, is_archive_format, read_table, eval_dict
from flatspin.encoder import Encoder
from flatspin.runner import run, run_local, run_dist
from flatspin import runner
from flatspin.utils import get_default_params, import_class, get_subclasses

def main_worker(args):
    # Run!
    dataset = Dataset.read(args.basepath)

    worker_id = args.worker_id
    num_jobs = len(dataset)
    num_workers = args.num_workers

    # Calculate which jobs in the dataset to run
    # See https://stackoverflow.com/questions/27553218/algorithm-for-distributing-workload-in-a-thread-pool
    from_idx = (worker_id * num_jobs) // num_workers
    to_idx = ((worker_id + 1) * num_jobs) // num_workers

    dataset = dataset[from_idx:to_idx-1]
    run_local(dataset)

def main_list_params(args):
    model_class = import_class(args.model, 'flatspin.model')
    model_name = model_class.__name__
    encoder_class = import_class(args.encoder, 'flatspin.encoder')
    encoder_name = encoder_class.__name__

    print(f"Default model parameters [{model_name}]:")
    for k,v in get_default_params(model_class).items():
        print(f" {k}={v}")

    print("")

    print(f"Default run parameters:")
    for k,v in get_default_params(run).items():
        print(f" {k}={v}")

    print("")

    print(f"Default encoder parameters [{encoder_name}]:")
    for k,v in get_default_params(encoder_class).items():
        print(f" {k}={v}")

def main_list_encoders(args):
    module = args.encoder if args.encoder else 'flatspin.encoder'
    module = importlib.import_module(module)
    classes = get_subclasses(module, Encoder)

    print(f"Encoder listing for {module.__name__}:")
    for name, cls in classes:
        print(name)

def main_help_encoder(args):
    encoder_class = import_class(args.encoder, 'flatspin.encoder')
    print(f"{encoder_class.__module__}.{encoder_class.__name__}(", end='')
    print(", ".join(f"{k}={v}" for k,v in
        get_default_params(encoder_class).items()), end='')
    print(")", end='\n\n')
    if encoder_class.__doc__:
        print(inspect.cleandoc(encoder_class.__doc__))
    else:
        print("<no docstring>")

def visualize_run(model, i, max_i, result_table, params):
    model.plot(replace=True)
    plt.title(f"{i + 1} / {max_i}")
    plt.suptitle(params['outdir'])
    plt.pause(0.001)

def main_normal(args):
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
        'version': __version__
    }

    basepath = args.basepath
    if os.path.exists(basepath):
        # Refuse to overwrite an existing dataset
        raise FileExistsError(basepath)
    os.makedirs(basepath)

    if is_archive_format(args.format):
        outdir = f"{model_name}.{args.format}"
    else:
        outdir = f"{model_name}.out"
    outpath = os.path.join(basepath, outdir)

    # Save dataset
    index = pd.DataFrame({'outdir': [outdir]})
    dataset = Dataset(index, params, info, basepath)
    dataset.save()

    # Run!
    if args.run == 'local':
        if args.show_plot:
            runner.run_sample_callback = visualize_run
        run_local(dataset)

    elif args.run == 'dist':
        run_dist(dataset)


# Parser needs to be accessible at module level for sphinxcontrib.autoprogram
parser = argparse.ArgumentParser(description='Run flatspin simulation.')
parser.add_argument('-r', '--run', choices=['local', 'dist', 'none', 'worker'], default='local',
        help='run locally or distributed on a cluster')
parser.add_argument('-p', '--param', action=StoreKeyValue, default={},
        help='set model/run parameter key=value')
parser.add_argument('-m', '--model', default='SquareSpinIceClosed',
        help='name of model (default: %(default)s) ')
parser.add_argument('-e', '--encoder', default='Sine',
        help='input encoder (type of external field, default: %(default)s)')
parser.add_argument('-o', '--basepath',
        help='output directory for results')
parser.add_argument('-f', '--format', choices=table_formats.keys(), default='npz',
        help='format of output files (default: %(default)s)')
parser.add_argument('--params-file',
        help='load parameters from file (params.csv), loaded before -p')

parser.add_argument('--list-params', action='store_true')
parser.add_argument('--list-encoders', action='store_true')
parser.add_argument('--help-encoder', action='store_true')
parser.add_argument('--worker-id', help='worker id', type=int)
parser.add_argument('--num-workers', help='number of workers in total', type=int)
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

    if args.run == 'worker':
        if args.worker_id is None or args.num_workers is None or args.basepath is None:
            parser.error('The following arguments are required for worker mode: --worker-id, --num-workers, --basepath')
    else:
        if args.basepath is None:
            parser.error('The following arguments are required: -o/--basepath')

    if args.run == 'worker':
        # Taking part in distributed run
        return main_worker(args)
    elif args.list_params:
        return main_list_params(args)

    return main_normal(args)

if __name__ == '__main__':
    main()
