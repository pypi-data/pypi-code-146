"""
Utilities related to the flatspin model
"""
import numpy as np
import copy
import itertools
import os
import inspect
from datetime import timedelta
from collections import OrderedDict
import importlib

def numeric_dict(d):
    return {k: int(v) for k,v in d.items() if str(v).isnumeric()}

def filter_dict(d, keys):
    return d.__class__((k,v) for k,v in d.items() if k in keys)

def pop_dict(d, keys):
    return d.__class__((k, d.pop(k)) for k in list(d.keys()) if k in keys)

def try_eval(s):
    """ Try to eval(s), on failure return s """
    try:
        return eval(s, {'array': np.array, 'inf': np.inf})
    except:
        return s

def eval_dict(d):
    return d.__class__((k, try_eval(v)) for k,v in d.items())

def make_tuple(tup):
    if isinstance(tup, tuple):
        return tup
    return (tup,)

def unique_list(l):
    u = []
    for i in l:
        if not i in u:
            u.append(i)
    return u

def get_default_args(func, exclude=['self']):
    sig = inspect.signature(func)
    params = OrderedDict((k,p.default) for k,p in sig.parameters.items() if k not in exclude)
    return params

def get_default_kwargs(func, exclude=[]):
    params = get_default_args(func, exclude)
    params = OrderedDict((k,d) for k,d in params.items() if d is not inspect._empty)
    return params

def get_default_params(cls):
    try:
        default_params = cls.get_default_params()
    except AttributeError:
        if inspect.isclass(cls):
            # Walk up the class hierarchy to discover all available parameters
            # Assumes each sub class' __init__() will only contain new parameters
            # or modified defaults.  Old parameters are delegatet to the parent
            # class through **kwargs
            default_params = {}
            mro = inspect.getmro(cls)
            for cls in reversed(mro):
                default_params.update(get_default_kwargs(cls.__init__))
        else:
            default_params = get_default_kwargs(cls)
    return dict(default_params)

def check_params(params, classes):
    cls_params = split_params(params, classes)
    unknown_params = cls_params[-1]
    if unknown_params:
        raise TypeError("Invalid params", list(unknown_params.keys()))

def filter_params(cls, params):
    valid = get_default_params(cls)
    return filter_dict(params, valid)

def pop_params(cls, params):
    valid = get_default_params(cls)
    return pop_dict(params, valid)

def split_params(params, classes):
    """ Split params belonging to the given list of classes.

    Returns a list of parameters matching the the given list of classes. The
    last element of the list are parameters which didn't match any of the
    class signatures. """

    params = copy.deepcopy(params)
    valid_params = list(map(get_default_params, classes))

    # Check that classes don't have overlapping parameters
    overlap = set.intersection(*[set(p.keys()) for p in valid_params])
    assert not overlap, f"Overlapping parameters for {classes}: {overlap}"

    result = []
    for cls, valid in zip(classes, valid_params):
        cls_params = filter_dict(params, valid)
        result.append(cls_params)
        for k in cls_params.keys():
            del params[k]

    result.append(params) # remaining params

    return result

def format_label(label):
    if isinstance(label, np.ndarray):
        label = tuple(label)
    return str(label).replace(' ', '')

def label_columns(labels, prefix='spin'):
    labels = list(map(format_label, labels))
    return [prefix + str(c) for c in labels]

def label_columns_2d(labels, prefix='spin'):
    cols = label_columns(labels, prefix)
    cols = [[col + 'x', col + 'y'] for col in cols]
    return list(itertools.chain(*cols))

def get_outdir(script_filename):
    root, ext = os.path.splitext(script_filename)
    return root + ".out"

def make_outdir(script_filename):
    outdir = get_outdir(script_filename)
    os.makedirs(outdir, exist_ok=True)
    return outdir

def import_class(name, module=None):
    if '.' in name:
        # Full module path
        module, cls = name.rsplit('.', maxsplit=1)
    else:
        assert module
        cls = name

    module = importlib.import_module(module)
    return getattr(module, cls)

def get_subclasses(module, superclass):
    predicate = lambda cls: inspect.isclass(cls) and issubclass(cls,
            superclass) and cls is not superclass

    return inspect.getmembers(module, predicate)
