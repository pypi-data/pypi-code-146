#!/usr/bin/env python3
'''
Hydra resolvers.
'''

import multiprocessing

import torch
from omegaconf import OmegaConf
from hydra.core.utils import setup_globals as hydra_setup_globals


def _get_divisor(args):
    '''
    Internal function to handle optional divisor to some resolvers.
    '''
    if len(args) > 0:
        divisor = int(args[0])
        if divisor > 0:
            return divisor
    return 1


def get_n_cpu(*args):
    '''
    Get the number of available CPUs. Optionally accept an integer argument
    which will be used to divide the result.

    Args:
        *args:
            An optional single integer argument. If given, the number of CPUs
            will be divided by this number.

    Returns:
        The number of available CPUs. If a divisior is given then this will
        always return a value of at least 1.
    '''
    n_cpu = multiprocessing.cpu_count()
    return max(n_cpu // _get_divisor(args), 1)


def get_n_gpu_pytorch(*args):
    '''
    Get the number of available PyTorch GPUs. Optionally accept an integer
    argument which will be used to divide the result.

    Args:
        *args:
            An optional single integer argument. If given, the number of CPUs
            will be divided by this number.

    Returns:
        The number of available PyTorch GPUs. If the number is greater than 0
        than a value of at least 1 will always be returned when an optional
        divisor is given.
    '''
    n_gpu = torch.cuda.device_count()
    if n_gpu < 1:
        return 0
    return max(n_gpu // _get_divisor(args), 1)


def register() -> dict[str, str]:
    '''
    Register custom resolvers.

    Returns:
        A dict mapping resolver names to their descriptions.
    '''

    resolvers = {}
    for name, desc, func in (
            (
                'n_cpu',
                'The number of available CPUs on the current system.',
                get_n_cpu
            ),
            (
                'n_gpu_pytorch',
                'The number of GPUs recognized by PyTorch.',
                get_n_gpu_pytorch
            ),
            (
                'max',
                'The maximum argument.',
                max
            ),
            (
                'min',
                'The minimum argument.',
                min
            )
    ):
        OmegaConf.register_new_resolver(name, func)
        resolvers[name] = desc
    return resolvers


def reregister() -> None:
    '''
    Reregister custom and Hydra resolvers. This is necessary due to a bug in the
    process launcher.
    '''
    if not OmegaConf.has_resolver('n_cpu'):
        register()
    if not OmegaConf.has_resolver('hydra'):
        hydra_setup_globals()
