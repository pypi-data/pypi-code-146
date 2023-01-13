"""
Dipole model runner
"""
import sys
import os
import numpy as np
import pandas as pd
import time
from numbers import Number
from datetime import timedelta
import subprocess
from copy import copy
from importlib import import_module
import warnings

from .cmdline import ProgressBar
from .data import read_table, to_table, save_table, is_archive, archive_key
from .utils import (pop_params, label_columns, label_columns_2d, eval_dict,
        import_class)

#
# List of deprecated parameters
#
# If you rename a parameter, please add it here to raise an error if it's being
# used! Otherwise it will go unnoticed since we ignore unknown parameters to
# facilitate fancy sweeps such as -s 'sz=arange(10,51,10)' -s 'size=[(sz,sz)]'
#
deprecated_params = ('sw_a', 'sw_alpha', 'temp_interp', 'temp_func', 'temp')

class DeprecationError(Exception):
    pass

run_sample_callback = None

def run(model, encoder='Sine', input=1, input_key=None, periods=100, spp=100,
        **params):
    """
    Run a flatspin simulation

    Parameters
    ----------
    model : SpinIce
        Model instance
    encoder : string or Encoder
        Name of input encoder to use or Encoder instance.
        See flatspin.encoder for a list of available encoders
    input : float, array or string
        Input to be encoded
        float: constant input repeated periods times
        array: array of input to encode
        string: filename of table input data
    input_key : int or str
        Index into input (table column)
    periods : int
        Number of periods of the external field to run
        Only used if input is a float
    spp : int
        Number of samples to save per input value
    params : dict
        Params to pass to the encoder
    """
    # unknown params are ignored

    if isinstance(encoder, str):
        encoder_class = import_class(encoder, 'flatspin.encoder')
        encoder = encoder_class()

    encoder_params = pop_params(encoder, params)
    encoder.set_params(**encoder_params)

    # Bail out if user tries any deprecated params
    for p in params.keys():
        if p in deprecated_params:
            raise DeprecationError("Parameter is deprecated", p)

    # Extract any time-varying parameters
    params_t = {k[:-2]: params.pop(k) for k in list(params.keys()) if k.endswith('_t')}

    for k in params_t:
        set_fn = f"set_{k}"
        if not hasattr(model, set_fn):
            raise ValueError(f"Invalid parameter: {k}_t")

    if "h_ext" in params_t:
        raise ValueError(f"h_ext_t is not supported, use the input encoders to set h_ext")

    # Warn on unknown params
    if params:
        unknown_params = ", ".join(params.keys())
        warnings.warn("Ignoring unknown parameters: " + unknown_params)

    result = {}

    if isinstance(input, str):
        # load input from file
        input = read_table(input)
        result['input'] = input
    elif isinstance(input, Number):
        # constant
        input = input * np.ones(periods)
        result['input'] = pd.DataFrame(input, columns=['input'])
    else:
        # array/list
        input = np.array(input)
        if input.ndim > 1:
            cols = label_columns(np.ndindex(*input.shape[1:]), prefix='input')
            input_flat = input.reshape((input.shape[0], -1))
            result['input'] = pd.DataFrame(input_flat, columns=cols)
        else:
            result['input'] = pd.DataFrame(input, columns=['input'])

    if input_key is not None:
        input = input[input_key]
    input = np.array(input, dtype=float)

    t0 = time.time()

    # Encode input as h_ext
    h_ext = encoder(input)

    # Figure out timesteps per period
    ts = len(h_ext) / len(input)
    if ts % spp != 0:
        print(f"WARNING: spp {spp} does not evenly divide the encoded input")
        print(f"         spp should divide the number of timesteps per input {ts}, e.g. spp={ts}")
    sample_every = int(np.round(ts / spp))

    # Input has now been encoded into h_ext, resulting in spp samples per input
    # value. Repeat input values spp times so that h_ext and input DataFrames
    # can be easily joined on the same index when needed. We keep the original
    # input index as an extra column called "index".
    input_df = result['input']
    input_df = input_df.loc[input_df.index.repeat(spp)].reset_index()
    input_df.index.name = 't'
    result['input'] = input_df

    # Time-varying parameters
    for k, v in list(params_t.items()):
        if isinstance(v, str):
            # load values from file
            v = read_table(v)
            v = np.array(v)
            if v.shape[-1] == 1:
                # Treat single-column tables 1d
                v = v.reshape(v.shape[:-1])

        if len(v) != len(input):
            raise ValueError(f"Length of {k}_t (={len(v)}) does not match length of input (={len(input)})")
        repeats = len(h_ext) / len(v)
        params_t[k] = np.repeat(v, repeats, axis=0)

    # Save h_therm if temperature > 0
    save_h_therm = model.temperature != 0 or \
            ('temperature' in params_t and np.any(params_t['temperature'] != 0))

    result['geometry'] = pd.DataFrame({
        'posx': model.pos[:,0].copy(),
        'posy': model.pos[:,1].copy(),
        'angle': model.angle.copy()})

    result['hc'] = pd.DataFrame({'threshold': model.threshold.copy()})

    cols = label_columns(model.labels, prefix='init')
    result['init'] = pd.DataFrame([model.spin.copy()], columns=cols)

    # TODO: dump model?
    # make a copy of model so we store the initial state in the dataset
    #    'model': copy.deepcopy(model),

    steps = 0

    sample_index = []
    result['spin'] = []
    result['mag'] = []
    result['h_ext'] = []
    if save_h_therm:
        result['h_therm'] = []
    result['energy'] = []
    result['steps'] = []
    if params_t:
        result['params_t'] = []

    msg = type(model).__name__
    disable_progress = not sys.stdout.isatty()
    progress_bar = ProgressBar(desc=msg, total=len(h_ext), disable=disable_progress)

    for i, h in enumerate(h_ext):
        if h.ndim > 1:
            # grid
            model.set_grid('h_ext', h)
        else:
            # global field
            model.set_h_ext(h)

        # Time-varying parameters
        for k, v in params_t.items():
            set_fn = getattr(model, f"set_{k}")
            set_fn(v[i])

        should_sample = (i % sample_every == 0)

        steps += model._relax(copy_gpu_to_cpu=should_sample)

        progress_bar.update()

        if should_sample:
            sample_index.append(i)
            result['spin'].append(model.spin.copy())
            result['mag'].append(model.vectors.flatten())
            result['energy'].append(model.total_energies())
            if save_h_therm:
                if isinstance(model.h_therm, np.ndarray):
                    result['h_therm'].append(model.h_therm.flatten())
                else:
                    result['h_therm'].append(np.zeros(model.spin_count * 2))
            if h.ndim > 1:
                # local field
                result['h_ext'].append(model.h_ext.flatten())
            else:
                # global field
                result['h_ext'].append(h)

            # Time-varying parameters
            if params_t:
                result['params_t'].append([v[i] for v in params_t.values()])

            result['steps'].append(steps)

            if run_sample_callback:
                run_sample_callback(model, i, len(h_ext), result, params)


    progress_bar.close()

    cols = label_columns(model.labels, prefix='spin')
    result['spin'] = pd.DataFrame(result['spin'], columns=cols, index=sample_index, dtype=result['spin'][0].dtype)
    result['spin'].index.name = 't'

    cols = label_columns_2d(model.labels, prefix='mag')
    result['mag'] = pd.DataFrame(result['mag'], columns=cols, index=sample_index, dtype=result['mag'][0].dtype)
    result['mag'].index.name = 't'

    cols = ['h_extx', 'h_exty']
    if h_ext.ndim > 2:
        # local field
        cols = label_columns_2d(model.labels, prefix='h_ext')
    result['h_ext'] = pd.DataFrame(result['h_ext'], columns=cols, index=sample_index, dtype=model.h_ext.dtype)
    result['h_ext'].index.name = 't'

    if save_h_therm:
        cols = label_columns_2d(model.labels, prefix='h_therm')
        result['h_therm'] = pd.DataFrame(result['h_therm'], columns=cols, index=sample_index, dtype=np.float64)
        result['h_therm'].index.name = 't'

    cols = ["E_dip", "E_ext", "E_therm", "E_tot"]
    result['energy'] = pd.DataFrame(result['energy'], columns=cols, index=sample_index, dtype=np.float64)
    result['energy'].index.name = 't'

    result['steps'] = pd.DataFrame(result['steps'], columns=['steps'], index=sample_index, dtype=int)
    result['steps'].index.name = 't'


    runtime = time.time() - t0

    result['stats'] = {
        'runtime': runtime,
        'steps': steps,
    }

    # Time-varying parameters
    if params_t:
        result['params_t'] = pd.DataFrame(result['params_t'], columns=params_t.keys(), index=sample_index)
        result['params_t'].index.name = 't'

    td = timedelta(seconds=runtime)
    print(f'Completed {steps} steps in {td}')

    return result

def run_and_save(model_class, params, outdir, data_format):
    params_table = to_table(params)

    model_params = pop_params(model_class, params)
    model = model_class(**model_params)

    results = run(model, **params)
    results["params"] = params_table

    if not is_archive(outdir):
        os.makedirs(outdir)

    for name, data in results.items():
        df = to_table(data)
        if not is_archive(outdir):
            name = f"{name}.{data_format}"
        save_table(df, os.path.join(outdir, name))

def run_local(dataset, verbose=True):
    """ Run on localhost """
    n_runs = len(dataset)

    mod, cls = dataset.info['model'].rsplit('.', 1)
    module = import_module(mod)
    model_class = getattr(module, cls)
    data_format = dataset.info['data_format']

    for i, ds in enumerate(dataset):
        params = copy(ds.params)
        params.update(eval_dict(ds.row().to_dict()))
        outdir = params['outdir']
        outpath = os.path.join(dataset.basepath, outdir)
        if verbose:
            description = ["{}={}".format(k,v) for (k,v) in ds.row().items()]
            description = " ".join(description)
            print(f"Run {i+1}/{n_runs}: {description}")
        run_and_save(model_class, params, outpath, data_format)

def generate_script(template, outfile, **params):
    with open(template) as fp:
        tpl = fp.read()
    script = tpl.format(**params)
    with open(outfile, 'w') as fp:
        fp.write(script)

job_script_template = os.path.join(os.path.dirname(__file__), 'flatspin.slurm.sh')

def run_dist(dataset, wait=True, max_jobs=1000):
    """ Run distributed on a cluster """

    #
    # Generate job script
    #

    # Construct a sensible name for the job script
    job_script_dir = dataset.basepath
    job_script_name = os.path.basename(job_script_template)
    job_script = os.path.join(job_script_dir, job_script_name)

    # Job template params
    job_params = {
        'job_script_dir': job_script_dir,
        'job_script_name': job_script_name,
        'basepath': dataset.basepath,
    }

    generate_script(job_script_template, job_script, **job_params)

    #
    # Submit jobs
    #

    # array size will never exceed max_jobs
    array_size = min(max_jobs, len(dataset))

    cmd = ['sbatch']
    if wait:
        cmd.append('--wait')
    cmd.append(f'--array=0-{array_size-1}')
    cmd.append(job_script)
    print(cmd)
    p = subprocess.Popen(cmd)

    if wait:
        p.wait()

