import sys
import numpy as np
import pandas as pd
import itertools
from collections import OrderedDict
from copy import copy
from glob import glob

from .cmdline import param_globals

def parse_spec(spec, ctx=None):
    return eval(spec, param_globals, ctx)

def parse_sweep_spec(specs, ctx={}):
    if not specs:
        return None

    sweep_spec = []

    key, spec = specs[0]

    for value in parse_spec(spec, ctx):
        ctx = copy(ctx)
        ctx[key] = value
        subspec = parse_sweep_spec(specs[1:], ctx)
        if subspec:
            sweep_spec.extend([((key, value),) + sub for sub in subspec])
        else:
            sweep_spec.append(((key, value),))

    return sweep_spec

def parse_repeat_spec(specs, ctx=None):
    repeat_spec = []
    for k, v in specs.items():
        repeat_spec.append([(k, vi) for vi in parse_spec(v, ctx)])

    if not repeat_spec:
        return [()]

    assert all(len(rs) == len(repeat_spec[0]) for rs in repeat_spec)
    return list(zip(*repeat_spec))


def sweep(sweep_spec, repeat=1, repeat_spec=None, params={}, seed=0):
    # NB: order of sweep spec may be important, so need to use OrderedDict
    # TODO: require sweep_spec to be list of tuples instead?
    sweep_spec = list(sweep_spec.items())
    sweep_list = parse_sweep_spec(sweep_spec, ctx=params)

    if not repeat_spec:
        repeat_spec = OrderedDict()
    if repeat > 1:
        repeat_spec['repeat'] = f'range({repeat})'
        repeat_spec['random_seed'] = f'randseed({repeat})'

    for i, sweep_params in enumerate(sweep_list):
        ctx = copy(params)
        ctx.update(sweep_params)

        # Re-seed the RNG to ensure we get the same random sequence across
        # sweeps, but different sequences across repeats
        np.random.seed(seed)

        repeat_list = parse_repeat_spec(repeat_spec, ctx=ctx)
        # print('repeat_list', repeat_list)

        for j, repeat_params in enumerate(repeat_list):
            runparams = dict(sweep_params)
            runparams.update(repeat_params)

            yield i, j, runparams

