import numpy as np
import pandas as pd
import pytest
import collections

from flatspin.sweep import sweep

def test_sweep_spec():
    sweep_spec = {'a': '[1,2,3]'}
    sweep_params = list(sweep(sweep_spec))
    assert sweep_params == [(0, 0, {'a': 1}), (1, 0, {'a': 2}), (2, 0, {'a': 3})]

def test_sweep_arange():
    sweep_spec = {'a': 'np.arange(3)'}
    sweep_params = list(sweep(sweep_spec))
    assert sweep_params == [(0, 0, {'a': 0}), (1, 0, {'a': 1}), (2, 0, {'a': 2})]

def test_sweep_expression():
    sweep_spec = {'a': 'bar + np.arange(foo)'}
    params = {'foo': 3, 'bar': 42}
    sweep_params = list(sweep(sweep_spec, params=params))
    assert sweep_params == [(0, 0, {'a': 42}), (1, 0, {'a': 43}), (2, 0, {'a': 44})]

def test_sweep_multiple():
    sweep_spec = {'a': 'np.arange(3)', 'b': '[1,10]'}
    sweep_params = list(sweep(sweep_spec))
    assert sweep_params == [
            (0, 0, {'a': 0, 'b': 1}),
            (1, 0, {'a': 0, 'b': 10}),
            (2, 0, {'a': 1, 'b': 1}),
            (3, 0, {'a': 1, 'b': 10}),
            (4, 0, {'a': 2, 'b': 1}),
            (5, 0, {'a': 2, 'b': 10})]

def test_sweep_depend():
    sweep_spec = {'a': 'np.arange(3)', 'b': 'np.arange(a, 3)'}
    sweep_params = list(sweep(sweep_spec))
    assert sweep_params == [
            (0, 0, {'a': 0, 'b': 0}),
            (1, 0, {'a': 0, 'b': 1}),
            (2, 0, {'a': 0, 'b': 2}),
            (3, 0, {'a': 1, 'b': 1}),
            (4, 0, {'a': 1, 'b': 2}),
            (5, 0, {'a': 2, 'b': 2})]

    sweep_spec = {'a': 'np.arange(3)', 'b': 'np.arange(a)'}
    sweep_params = list(sweep(sweep_spec))
    assert sweep_params == [
            (0, 0, {'a': 0}),
            (1, 0, {'a': 1, 'b': 0}),
            (2, 0, {'a': 2, 'b': 0}),
            (3, 0, {'a': 2, 'b': 1})]

def test_sweep_repeat():
    sweep_spec = {'a': 'range(3)'}
    sweep_params = list(sweep(sweep_spec, repeat=2))
    seeds = [p['random_seed'] for i,j,p in sweep_params]
    assert sweep_params == [
            (0, 0, {'a': 0, 'repeat': 0, 'random_seed': seeds[0]}),
            (0, 1, {'a': 0, 'repeat': 1, 'random_seed': seeds[1]}),
            (1, 0, {'a': 1, 'repeat': 0, 'random_seed': seeds[0]}),
            (1, 1, {'a': 1, 'repeat': 1, 'random_seed': seeds[1]}),
            (2, 0, {'a': 2, 'repeat': 0, 'random_seed': seeds[0]}),
            (2, 1, {'a': 2, 'repeat': 1, 'random_seed': seeds[1]})]

def test_sweep_repeat_spec():
    sweep_spec = {'a': 'range(3)'}
    repeat_spec = {'b': 'range(2)'}
    sweep_params = list(sweep(sweep_spec, repeat_spec=repeat_spec))
    assert sweep_params == [
            (0, 0, {'a': 0, 'b': 0}), (0, 1, {'a': 0, 'b': 1}),
            (1, 0, {'a': 1, 'b': 0}), (1, 1, {'a': 1, 'b': 1}),
            (2, 0, {'a': 2, 'b': 0}), (2, 1, {'a': 2, 'b': 1})]

def test_sweep_repeat_specs():
    sweep_spec = {'a': 'range(3)'}
    repeat_spec = {'b': 'range(2)', 'c': '[10,20]'}
    sweep_params = list(sweep(sweep_spec, repeat_spec=repeat_spec))
    assert sweep_params == [
            (0, 0, {'a': 0, 'b': 0, 'c': 10}), (0, 1, {'a': 0, 'b': 1, 'c': 20}),
            (1, 0, {'a': 1, 'b': 0, 'c': 10}), (1, 1, {'a': 1, 'b': 1, 'c': 20}),
            (2, 0, {'a': 2, 'b': 0, 'c': 10}), (2, 1, {'a': 2, 'b': 1, 'c': 20})]

def test_sweep_repeat_seed():
    sweep_spec = {'a': '[42]'}
    seeds = []
    for i in range(10):
        sweep_params = sweep(sweep_spec, repeat=10, seed=0)
        seeds.append([p['random_seed'] for i,j,p in sweep_params])

    seeds = np.array(seeds)

    # Should get same sequence of seeds for each call to sweep()
    assert np.all(seeds == seeds[0])

