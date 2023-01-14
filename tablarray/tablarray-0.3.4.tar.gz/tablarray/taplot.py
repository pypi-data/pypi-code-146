#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 15:52:31 2022

@author: chris
"""

import functools
from matplotlib import pyplot

from . import misc
#from .np2ta import passwrap as pw
from .set import TablaSet


def automeshtile(*args):
    '''
    For each arg which is TablArray type, add it to a temporary TablaSet,
    then extract all such args using TablaSet.meshtile, and return all args.

    1. First, this means all TablArray args must be broadcast compatible.
    2. This means after the return, the args will be meshed to flesh out their
    broadcast shape.

    Primarily this is useful for calling plots. So, tablarray has duplicate
    plot methods that should look familiar from matplotlib.pyplot, e.g.
    tablarray.contourf and .plot. Those are wrapped with automeshtile, making
    explicit meshing unnecessary for users.

    Returns
    -------
    args : tuple
        TablaSet.meshtile() filtered copy of input. args of other types are
        returned unchanged.
    '''
    tset = TablaSet()
    N_ta = 0
    # first pass, setup a TablaSet
    for i in range(len(args)):
        arg = args[i]
        if misc.istablarray(arg):
            key = 'a%d' % i
            tset[key] = arg
            N_ta += 1
    args2 = []
    for i in range(len(args)):
        arg = args[i]
        key = 'a%d' % i
        arg = tset.meshtile(key) if misc.istablarray(arg) else arg
        args2.append(arg)
    return tuple(args2)


def _unpack_set(tset, *args):
    args2 = []
    for arg in args:
        if type(arg) is str:
            args2.append(tset[arg])
        else:
            args2.append(arg)
    return tuple(args2)


def _wrap_automesh(func):
    """
    wrapper that filters args using automeshtile
    """
    @functools.wraps(func)
    def automeshed(*args, **kwargs):
        if len(args) >= 2 and misc.istablaset(args[0]):
            args = _unpack_set(*args)
        args2 = automeshtile(*args)
        func(*tuple(args2), **kwargs)
    automeshed.__doc__ = (
        "**automeshed TablArray/TablaSet (passthrough)** %s\n\n" % func.__name__
        + automeshed.__doc__)
    return automeshed


bar = _wrap_automesh(pyplot.bar)
barbs = _wrap_automesh(pyplot.barbs)
boxplot = _wrap_automesh(pyplot.boxplot)
contour = _wrap_automesh(pyplot.contour)
contourf = _wrap_automesh(pyplot.contourf)
csd = _wrap_automesh(pyplot.csd)
hist = _wrap_automesh(pyplot.hist)
plot = _wrap_automesh(pyplot.plot)
polar = _wrap_automesh(pyplot.polar)
psd = _wrap_automesh(pyplot.psd)
#quiver = _wrap_automesh(pyplot.quiver)
scatter = _wrap_automesh(pyplot.scatter)
#triplot = _wrap_automesh(pyplot.triplot)


@_wrap_automesh
def quiver2d(*args, **kwargs):
    '''
    Plot a 2d field of arrows.

    See matplotlib.quiver, now wrapped for TablArray

    Call signature::

        quiver([X, Y], UV, [C], **kwargs)

    Where X, Y, UV are broadcast compatible but meshing is not required
    (see automeshtile).

    Parameters
    ----------
    X, Y : TablArray
        arrow base locations
    UV : TablArray
        2d arrow vectors, i.e. cellular shape c(2,)
    C : ndarray or TablArray
        optionally sets the color
    '''
    if len(args) == 1:
        uv = args[0]
        # factor uv vector for tuple
        u = uv.cell[0]
        v = uv.cell[1]
        args2 = u, v
    elif len(args) == 2:
        uv, c = args
        u = uv.cell[0]
        v = uv.cell[1]
        args2 = u, v, c
    elif len(args) == 3:
        x, y, uv = args
        u = uv.cell[0]
        v = uv.cell[1]
        args2 = x, y, u, v
    elif len(args) == 4:
        x, y, uv, c = args
        u = uv.cell[0]
        v = uv.cell[1]
        args2 = x, y, u, v, c
    else:
        raise ValueError
    pyplot.quiver(*args2, **kwargs)


@_wrap_automesh
def quiver3d(*args, **kwargs):
    '''
    Plot a 3d field of arrows.

    Call signature::

        quiver3d([X, Y, Z], UVW, [C], **kwargs)

    See ax.quiver for 3d, esp. kwargs like length

    Where X, Y, Z, UVW are broadcast compatible but meshing is not required
    (see automeshtile).

    Parameters
    ----------
    X, Y, Z: TablArray
        arrow base locations
    UVW : TablArray
        3d arrow vectors, i.e. cellular shape c(3,)
    C : ndarray or TablArray
        optionally sets the color
    '''
    if len(args) == 1:
        uvw = args[0]
        # factor uv vector for tuple
        u = uvw.cell[0]
        v = uvw.cell[1]
        w = uvw.cell[2]
        args2 = u, v, w
    elif len(args) == 2:
        uvw, c = args
        u = uvw.cell[0]
        v = uvw.cell[1]
        w = uvw.cell[2]
        args2 = u, v, c
    elif len(args) == 4:
        x, y, z, uvw = args
        u = uvw.cell[0]
        v = uvw.cell[1]
        w = uvw.cell[2]
        args2 = x, y, z, u, v, w
    elif len(args) == 5:
        x, y, z, uvw, c = args
        u = uvw.cell[0]
        v = uvw.cell[1]
        w = uvw.cell[2]
        args2 = x, y, z, u, v, w, c
    else:
        raise ValueError
    fig = pyplot.figure()
    ax = fig.add_subplot(projection='3d')
    ax.quiver(*args2, **kwargs)
