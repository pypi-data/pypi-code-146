#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solve
-----
main members:
    1. solver_spec
    2. TablaSolver

workflow:

0. build library of solvers having solver specs:
    'func(arg1, arg2, ...) --> (out1, out2, ...)'
1. Populate a TablaSet with seed data
2. Create TablaSolver with the seed dataset and set of solvers
2.5 (Supplementary info to steer solver):
    a. atol / rtol to define change tolerance
    b. supercession of multiple solvers (can dependency mapping resolve?)
3. Call TablaSolver

Todo:
    0. rtol and/or atol
    1. dependency map
    2. Can dependency map identify run_once implication?
    3. Is it good to use such an implication to lockout repitition, or
        does the user need to do that explicitly?

Created on Tue Feb 16 07:35:42 2021

@author: chris
"""

import attr
import copy
import logging
import numpy as np
import re

from . import misc
from . import np2ta


def _dummy_viewarg(arg):
    """dummy function does nothing to args"""
    return arg


def _dummy_log(*args, **kwargs):
    pass


def _factory_viewargs(view):
    def _viewargs(args):
        """for each TablArray in args, force using the expected argview"""
        args2 = []
        for arg in args:
            arg2 = arg.__view__(view) if misc.istablarray(arg) else arg
            args2.append(arg2)
        return tuple(args2)
    return _viewargs


def _factory_viewkwargs(view):
    def _viewkwargs(kwargs):
        """for each TablArray in kwargs, force using the expected argview"""
        kwargs2 = {}
        for key, item in kwargs.items():
            item2 = item.__view__(view) if misc.istablarray(item) else item
            kwargs2[key] = item2
        return kwargs2
    return _viewkwargs


def _survey_view(args, kwargs):
    """find the most popular view of TablArrays in args and kwargs"""
    views = ['table', 'bcast', 'cell', 'array']
    idx = dict(zip(views, range(4)))
    counts = np.zeros(4, dtype=int)
    for arg in args:
        if misc.istablarray(arg):
            view = arg.view
            counts[idx[view]] += 1
    for _, arg in kwargs.items():
        if misc.istablarray(arg):
            view = arg.view
            counts[idx[view]] += 1
    print('counts %s' % counts)
    popular_idx = np.argsort(counts)[-1]
    return views[popular_idx]


@attr.s
class _Spec_Wrap(object):
    """a function wrapped with spec data, """
    _func = attr.ib()
    inargs = attr.ib(type=list)
    inkwargs = attr.ib(type=list)
    outargs = attr.ib(type=list)
    inview = attr.ib(type=str, default='cell')
    outview = attr.ib(type=str, default='ignore')
    _options = dict(rval2dict=False, debugging=False)

    def __attrs_post_init__(self):
        # validate parameters
        if len(self.inargs) < 1 and len(self.inkwargs) < 1:
            raise ValueError('need to spec inargs or inkwargs')
        for arg in self.inargs:
            if type(arg) is not str:
                raise TypeError('got type %s instead of str' % type(arg))
        for arg in self.inkwargs:
            if type(arg) is not str:
                raise TypeError('got type %s instead of str' % type(arg))
        if self.inview not in ['ignore', 'cell', 'table', 'bcast', 'array']:
            raise ValueError('unrecognized argview "%s"' % self.inview)
        if self.outview not in ['ignore', 'cell', 'table', 'bcast', 'array']:
            raise ValueError('unrecognized argview "%s"' % self.outview)
        # set the docstring to show what is wrapped and how
        self._doc0 = ("%s%s {'%s'} --> %s {'%s'}" % (
            self._func.__name__,
            tuple(self.inargs + self.inkwargs), self.inview,
            tuple(self.outargs), self.outview))
        doc0 = ('solver_spec wrap (for TablaSet / TablaSolver)\n\n'
                + self._doc0 + '\n\n'
                + 'Original Function Below\n\n'
                + '-----------------------\n\n')
        self.__doc__ = doc0 + ('' if self._func.__doc__ is None
                               else self._func.__doc__)
        # init options
        self.set_options()
        # setup a function for input arg and kwarg views
        if self.inview == 'ignore':
            self._viewinargs = _dummy_viewarg
            self._viewinkwargs = _dummy_viewarg
        else:
            self._viewinargs = _factory_viewargs(self.inview)
            self._viewinkwargs = _factory_viewkwargs(self.inview)
        # setup a function for input arg and kwarg views
        if self.outview == 'ignore':
            self._viewoutargs = _dummy_viewarg
        else:
            self._viewoutargs = _factory_viewargs(self.outview)

    def __str__(self):
        return self._doc0

    def set_options(self, **options):
        """
        Options
        -------
        debugging : bool (default=False)
            debugging messages to logging.debug
        """
        self._options.update(**options)
        if self._options['debugging']:
            # set a logger
            log = logging.getLogger(__name__ + ': ' + self._func.__name__)
            self._logdebug = log.debug
        else:
            # or debug into the void
            self._logdebug = _dummy_log

    def __call__(self, *args, rval2dict=False, **kwargs):
        if len(args) >= 1 and misc.istablaset(args[0]):
            self._logdebug('client gave a TablaSet to load args')
            if len(args) > 1:
                self._logdebug('ignoring %d args from client',
                               len(args[1:]))
            set1 = args[0]
            keys = set1.keys()
            # get args1 from set1
            args1 = []
            for inarg in self.inargs:
                if inarg in keys:
                    args1.append(set1[inarg])
                else:
                    self._logdebug('element "%s" not found in TablaSet',
                                   inarg)
            # get kwargs1 from set1
            kwargs1 = {}
            for inkwarg in self.inkwargs:
                if inkwarg in keys:
                    kwargs1[inkwarg] = set1[inkwarg]
                else:
                    self._logdebug('element "%s" not found in TablaSet',
                                   inkwarg)
            # combine kwargs from the line
            if len(kwargs) > 0:
                self._logdebug('combining keywords %s from client',
                               list(kwargs.keys()))
            kwargs1.update(kwargs)
        else:
            self._logdebug("fall back on func(*args, **kwargs)")
            args1 = args
            kwargs1 = kwargs
        # finished mangling args and kwargs, now call func
        rvals = self._func(*self._viewinargs(args1),
                           **self._viewinkwargs(kwargs1))
        # find TablArray returns and force the view
        rvals = [rvals] if type(rvals) is not tuple else rvals
        rvals2 = self._viewoutargs(rvals)
        if rval2dict:
            rval_dict = dict(zip(self.outargs, rvals2))
            return rval_dict
        else:
            return rvals2[0] if len(rvals) == 1 else tuple(rvals2)


def _str2spec(spec):
    """
    given a spec string return a dict with specs

    >>> _str2spec('addition(a, b) --> (c)')
    {'inargs': ['a', 'b'], 'inkwargs': [], 'outargs': ['c']}
    >>> _str2spec('addition(a, b){cell} --> (c){table}')
    {'inargs': ['a', 'b'],
     'inkwargs': [],
     'outargs': ['c'],
     'inview': 'cell',
     'outview': 'table'}
    """
    # remove spaces
    spec2 = re.sub(' ', '', spec)
    left1, right1 = tuple(spec2.split('-->'))
    _, inargs0, inview0 = tuple(re.split('\\(|\\)', left1))
    inargs1 = inargs0.split(',')
    _, outargs0, outview0 = tuple(re.split('\\(|\\)', right1))
    outargs1 = outargs0.split(',')
    rval = dict(inargs=inargs1, inkwargs=[], outargs=outargs1)
    if len(inview0) > 0:
        rval['inview'] = re.sub('\\{|\\}', '', inview0)
    if len(outview0) > 0:
        rval['outview'] = re.sub('\\{|\\}', '', outview0)
    return rval


def solver_spec(*args, **kwargs):
    """
    solver_spec
    -----------
    Decorator factory for TablaSet / TablaSolver methods

    Signature spec string
    ---------------------
    fname(inargs){view[optional]} --> (outargs){view[optional]}

    E.g.::

        @solver_spec('multiply(a, b){cell} --> (c){table}')
        def multiply(a, b):
            return a * b

        @solver_spec('add(a, b) --> (c)')
        def add(a, b)
            return a + b

    or Individual Specs
    -------------------
    inargs: list of str
        input arguments for your func
    inkwargs: list of str
        input arguments passed by keyword arguments for your func
    outargs: list of str
        names of outputs of your func
    inview: str (default='cell')
        set TablArray to this view before pass in args to func
    outview: str (default='ignore')
        set TablArray view before out rvals return
    run_once: bool
        maximum of one time your solver ought to run

    E.g.::

        @solver_spec(inargs=['a', 'b'], inkwargs=[], outargs=['c'],
                     inview='cell', outview='table')
        def multiply(a, b):
            return a * b

        @solver_spec(inargs=['a', 'b'], inkwargs=[], outargs=['c'])
        def add(a, b)
            return a + b
    """
    if len(args) > 0 and type(args[0]) is str:
        # passing a string for first arg triggers processing a spec string
        args1 = ()
        kwargs1 = _str2spec(args[0])
    else:
        args1 = args
        kwargs1 = kwargs

    def decorator_solver(func):
        return _Spec_Wrap(func, *args1, **kwargs1)
    return decorator_solver


class TablaSolver(object):
    """
    TablaSolver
    -----------
    When called, solvers execute in a sequence to satisfy dependencies.
    And iterate (up to a maxiter) until dataset no longer changes.

    Parameters:
    a : TablaSet
        starting point data, and results loaded here
    solvers: list of solver_spec
        all of the solver (methods) needed
    """

    def __init__(self, tset, solvers):
        self.tset = tset
        for solver in solvers:
            if not isinstance(solver, _Spec_Wrap):
                raise TypeError('solvers must be wrapped using "solver_spec"')
        self.solvers = solvers
        # log name could be improved
        self._log = logging.getLogger(__name__)
        self._prior_state = None
        self._haschanged = {}

    @property
    def dependency_map(self):
        # TODO
        pass

    def haschanged(self, key):
        """whether or not values under key have changed since prior state"""
        if self._prior_state is None:
            return True
        if key not in self._prior_state or key not in self._haschanged:
            return True
        prior = self._prior_state[key]
        current = self.tset[key]
        # missing: I want a method for specifying atol or rtol per key
        haschanged = not np2ta.allclose(prior, current)
        return haschanged

    def _update_haschanged(self):
        prior_state = self._prior_state
        for key, values in self.tset.items():
            has_changed = False
            if self._prior_state is None or key not in prior_state:
                has_changed = True
            else:
                old = prior_state[key]
                current = self.tset[key]
                has_changed = not np2ta.allclose(old, current)
            self._haschanged[key] = has_changed
        self._prior_state = copy.copy(self.tset)

    def _call_solver(self, a):
        """may or may not call a solver, determined by state of dependencies"""
        solver = self.solvers[a]
        # check dependencies
        if not all([arg in self.tset for arg
                    in (solver.inargs + solver.inkwargs)]):
            self._log.debug('Missing dependency for solver %s',
                            solver)
            return False
        # shunt if dependencies haven't changed
        dependency_changed = any([self.haschanged(inarg) for inarg
                                  in solver.inargs + solver.inkwargs])
        if not dependency_changed:
            self._log.debug('No change to dependencies for solver %s',
                            solver)
            return False
        # shunt if run_once and done_table
        '''if only_once and pilotpath.done_table(provides):
            log.info('%s is already done so shunt solver %s',
                     provides, func)
            return True'''
        # now run the solver with a dict return
        rvals = solver(self.tset, rval2dict=True)
        # update our data set with the rvals
        self.tset.update(**rvals)
        return True

    def __call__(self, maxiter):
        for a in range(maxiter):
            for a in range(len(self.solvers)):
                self._call_solver(a)
            self._update_haschanged()
