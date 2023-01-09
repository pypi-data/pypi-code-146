"""
    Copyright (C) 2007-2023, Michele Cappellari

    E-mail: michele.cappellari_at_physics.ox.ac.uk

    Updated versions of the software are available from PyPi
    https://pypi.org/project/jampy

    If you have found this software useful for your research,
    I would appreciate an acknowledgement and a link to the website.

    This software is provided as is without any warranty whatsoever.
    Permission to use, for non-commercial purposes is granted.
    Permission to modify for personal or internal use is granted,
    provided this copyright and disclaimer are included unchanged
    at the beginning of the file. All other rights are reserved.
    In particular, redistribution of the code is not allowed.

############################################################################


CHANGELOG
---------

    V1.0.0: Written and tested against the corresponding MATLAB version,
        Michele Cappellari, Oxford, 22 October, 2007

    V1.1.0: Allow function parameters to be passed via the FUNCTARGS keyword.
        MC, Oxford, 23 October 2007

    V1.1.1: Added STATUS keyword. Provide more informative error messages on failure.
        MC, Windoek, 5 October 2008

    V1.1.2: Renamed CAP_QUADVA to avoid potential naming conflicts.
        MC, Paranal, 8 November 2013

    V2.0.0: Translated from IDL into Python. MC, Paranal, 14 November 2013

    V2.0.1: Fixed possible program stop. MC, Oxford, 27 January 2014

    V2.0.2: Support both legacy Python 2.7 and Python 3. MC, Oxford, 25 May 2014

    V2.0.3: Dropped Python 2.7 support. MC, Oxford, 12 May 2018

    V2.1.0: Included optional plotting of sampled points. MC, Oxford, 25 June 2019

    V3.0.0:
        - Changed interface as a class and renamed quadva --> quad1d
        - Print number of function evaluation if ``verbose=1``.
        - New ``singular`` keyword: set ``singular=False`` to prevent
          transforming the coordinates of the integrand. This is useful
          when one wants to transform the coordinates outside ``quad1d``.
        MC, Oxford, 4 February 2022

    V3.1.0: Change defaults to `singular=False` and `epsabs=0` like `quad2d`.
        MC, Oxford, 3 January 2023

"""
import numpy as np
import matplotlib.pyplot as plt

EPS = 100*np.finfo(float).eps

################################################################################

def _qva_split(interval):
    """
    If breakpoints are specified, split sub-intervals in
    half as needed to get a minimum of 10 sub-intervals.
    """
    v = interval
    while True:
        npts = interval.size
        if npts > 10:
            break
        v = np.zeros(npts*2 - 1)
        v[0::2] = interval
        v[1::2] = interval[:-1] + 0.5*np.diff(interval)
        interval = v

    return v

################################################################################

def _qva_check_spacing(x):
    ax = np.abs(x)
    too_close = np.any(np.diff(x) <= EPS*np.maximum(ax[:-1], ax[1:]))

    return too_close

################################################################################

def _qva_f1(fun, t, a, b, args):
    """
    Transform to weaken singularities at both ends: [a, b] -> [-1, 1]
    """
    x = 0.25*(b - a)*t*(3. - t**2) + 0.5*(b + a)
    too_close = _qva_check_spacing(x)
    if too_close:
        y = []
    else:
        y = fun(x, *args)
        y *= 0.75*(b - a)*(1. - t**2)

    return y, too_close

################################################################################

def _qva_f2(fun, t, a, b, args):
    """
    Transform to weaken singularity at left end: [a, np.Inf) -> [0, Inf).
    Then transform to finite interval: [0, Inf) -> [0, 1].
    """
    Tt = t/(1. - t)
    x = a + Tt**2
    too_close = _qva_check_spacing(x)
    if too_close:
        y = []
    else:
        y = fun(x, *args)
        y *= 2.*Tt/(1. - t)**2

    return y, too_close

################################################################################

def _qva_f3(fun, t, a, b, args):
    """
    Transform to weaken singularity at right end: (-Inf, b] -> (-Inf, 0].
    Then transform to finite interval: (-Inf, 0] -> (-1, 0].
    """
    Tt = t/(1. + t)
    x = b - Tt**2
    too_close = _qva_check_spacing(x)
    if too_close:
        y = []
    else:
        y = fun(x, *args)
        y *= -2.*Tt/(1. + t)**2

    return y, too_close

################################################################################

def _qva_f4(fun, t, a, b, args):
    """
    Transform to finite interval: (-Inf, Inf) -> (-1, 1)
    """
    x = t/(1. - t**2)
    too_close = _qva_check_spacing(x)
    if too_close:
        y = []
    else:
        y = fun(x, *args)
        y *= (1. + t**2)/(1. - t**2)**2

    return y, too_close

################################################################################

def _qva_f5(fun, t, a, b, args):
    """
    Simple linear transformation: [a, b] -> [-1, 1]
    """
    x = 0.5*((b + a) + (b - a)*t)
    too_close = _qva_check_spacing(x)
    if too_close:
        y = []
    else:
        y = fun(x, *args)
        y *= 0.5*(b - a)

    return y, too_close

################################################################################

def _qva_Vadapt(f, tinterval, rtol, atol, samples, nodes, wt, ewt, fun, a, b, args, plot):
    """ Main loop of the quadrature """

    tbma = np.abs(tinterval[-1] - tinterval[0])  # length of transformed interval

    # Initialize array of subintervals of [a,b].
    subs = np.column_stack([tinterval[:-1], tinterval[1:]])  # Two columns array[n, 2]

    # Initialize partial sums.
    IfxOK = errOK = 0

    # Initialize main loop
    OK = first = converged = True
    Ifx = errbnd = fcall = vfcall = 0

    if plot:
        plt.figure('quad1d')
        plt.clf()
        plt.xlabel('x')
        plt.ylabel('y')
        xall = yall = []

    while True:
        # SUBS contains subintervals of [a,b] where the integral is not
        # sufficiently accurate.  The first row of SUBS holds the left end
        # points and the second row, the corresponding right end points.
        midpt = np.sum(subs, axis=1)/2      # midpoints of the subintervals
        halfh = np.diff(subs, axis=1)/2     # half the lengths of the subintervals
        x = nodes*halfh + midpt[:, None]    # broadcasting midpt
        halfh = halfh.ravel()
        x = x.ravel()

        fx, too_close = f(fun, x, a, b, args)
        fcall += fx.size
        vfcall += 1

        # Quit if mesh points are too close or too close to a
        # singular point or got into trouble on first evaluation.
        not_finite = np.any(np.isinf(fx))
        if too_close or not_finite:
            break

        if plot:
            plt.figure('quad1d')
            plt.plot(x, fx, '+')
            xall = np.append(xall, x)
            yall = np.append(yall, fx)

        fx = fx.reshape(-1, samples)

        # Quantities for subintervals.
        Ifxsubs = fx @ wt * halfh
        errsubs = fx @ ewt * halfh

        # Quantities for all of [a, b].
        Ifx = np.sum(Ifxsubs) + IfxOK
        errbnd = abs(np.sum(errsubs) + errOK)

        # Test for convergence:
        tol = max(atol, rtol*np.abs(Ifx))
        if errbnd <= tol:
            converged = True
            break

        # Locate subintervals where the approximate integrals are
        # sufficiently accurate and use them to update partial sums.
        good = np.abs(errsubs) <= (2/tbma)*halfh*tol
        errOK += np.sum(errsubs[good])
        IfxOK += np.sum(Ifxsubs[good])
        # Only keep subintervals which are not yet sufficiently accurate
        subs = subs[~good, :]
        if subs.size == 0:  # all intervals are accurate
            converged = True
            break

        # Split the remaining subintervals in half. Quit if splitting
        # results in too many subintervals.
        many_subint = 2*subs.size > 650  # multiplied limit by 10x MC 26/FEB/2008
        if many_subint:
            break
        midpt = np.sum(subs, axis=1)/2
        tmp = np.column_stack([subs[:, 0], midpt, midpt, subs[:, 1]])
        subs = tmp.reshape(-1, 2)  # ---> subs[n, 2]
        first = False

    if first and not converged:
        if too_close:
            print('***Sub intervals too close.')
        elif not_finite:
            print('***Infinite values in integrand.')
        elif many_subint:
            print('***Too many sub intervals.')
        OK = False

    if plot:
        plt.figure('quad1d')
        w = np.argsort(xall)
        plt.plot(xall[w], yall[w])

    return Ifx, errbnd, OK, fcall, vfcall

################################################################################

class quad1d:
    """
    Calling sequence: ``q = quad1d(fun, interval, epsrel=1e-5, epsabs=0)``
    
    ``q.integ`` and ``q.errbnd`` will contain the value of the integral 
    and the corresponding estimate of the error bound.

    When ``INTERVAL = [A,B]``, computes the integral of a continuous function
    ``f(x)`` from A to B for A < B.  A can be ``-np.inf`` and/or B can be
    ``np.inf``.

    FUN accepts a row vector X and returns a vector Y with ``Y(m) = f(X(m))``
    for ``m = 1,...,len(X)``.

    quad1d returns an approximation Ifx to the integral and optionally an
    approximate bound, ERRBND, on the error ``|integral - Ifx|``. It attempts
    to compute Ifx such that ``|Ifx - integral| <= max(ABSTOL,RELTOL*|Ifx|)``.
    If quad1d is unsuccessful, Ifx and ERRBND are still meaningful, so a
    warning is issued that includes ERRBND.

    If the interval is infinite, say ``[a, np.inf)``, then for the integral to
    exist, ``f(x)`` must decay as ``x -> np.inf`` and quad1d requires it to
    decay rapidly. Special methods should be used for oscillatory functions on
    infinite intervals, but quad1d can be used if ``f(x)`` decays fast enough.

    quad1d will integrate ``f(x)`` that are singular at finite end points if
    the singularities are not too strong. For example, it will integrate
    ``f(x)`` that behave like ``log|x - c|`` or ``|x - c|^p`` for ``p >= -1/2``
    with ``c = a`` and/or ``c = b``. If ``f(x)`` is singular at points inside
    ``(A,B)``, write the integral as a sum of integrals over subintervals with
    the singular points as end points, compute them with quad1d, and add the
    results.

    quad1d starts with samples of ``f(x)`` at 150 points in ``(A,B)``. It must
    be able to recognize the behavior of ``f(x)`` from these samples, so if
    ``f(x)`` oscillates very rapidly or has sharp peaks, it may be necessary to
    subdivide the interval. To do this, make INTERVAL an array with entries
    (breakpoints) that increase from ``A = INTERVAL[0]`` to ``B = INTERVAL[-1]``.
    If ``f(x)`` is only piecewise smooth, the points of discontinuity should
    be breakpoints.

    Based on the algorithm "Vectorized Adaptive Quadrature in Matlab"
    `L.F. Shampine, Journal of Computational and Applied Mathematics
    211 (2008) 131-140 <http://dx.doi.org/10.1016/j.cam.2006.11.021>`_

    """
    def __init__(self, fun, interval, epsrel=1e-5, epsabs=0, plot=False,
                 verbose=False, singular=False, args=()):

        interval = np.asarray(interval)
        nint = interval.size
        assert nint >= 2, "INTERVAL must be a real vector of at least two entries."
        assert np.all(np.diff(interval) > 0), "Entries of INTERVAL must strictly increase."

        a = interval[0]
        b = interval[-1]

        # Generally the error test is a mixed one, but pure absolute error
        # and pure relative error are allowed.  If a pure relative error
        # test is specified, the tolerance must be at least 100*EPS. 
        #
        rtol = max(epsrel, EPS)
        atol = epsabs

        # Gauss-Kronrod (7,15) pair. Use symmetry in defining nodes and weights.
        #
        samples = 15
        pnodes = np.array(
            [0.2077849550078985, 0.4058451513773972, 0.5860872354676911,
             0.7415311855993944, 0.8648644233597691, 0.9491079123427585,
             0.9914553711208126])
        nodes = np.hstack([-pnodes[::-1], 0, pnodes])
        pwt = np.array(
            [0.2044329400752989, 0.1903505780647854, 0.1690047266392679,
             0.1406532597155259, 0.1047900103222502, 0.06309209262997855,
             0.02293532201052922])
        wt = np.hstack([pwt[::-1], 0.2094821410847278, pwt])
        pwt7 = np.array([0, 0.3818300505051189, 0, 0.2797053914892767,
                         0, 0.1294849661688697, 0])
        ewt = wt - np.hstack([pwt7[::-1], 0.4179591836734694, pwt7])

        # Identify the task. If breakpoints are specified, work out
        # how they map into the standard interval.
        #
        if singular or np.inf in [a, b]:

            if a != -np.Inf and b != np.Inf:
                if nint > 2:
                    # Analytical transformation suggested by K.L. Metlov:
                    alpha = 2.*np.sin(np.arcsin((a + b - 2.*interval[1:-1])/(a - b))/3.)
                    tinterval = np.hstack([-1., alpha, 1.])
                    tinterval = _qva_split(tinterval)
                else:
                    tinterval = np.linspace(-1, 1, 11)

                Ifx, errbnd, OK, fcall, vfcall = _qva_Vadapt(
                    _qva_f1, tinterval, rtol, atol, samples, nodes, wt, ewt,
                    fun, a, b, args, plot)

            elif a != -np.Inf and b == np.Inf:
                if nint > 2:
                    alpha = np.sqrt(interval[1:-1] - a)
                    tinterval = np.hstack([0., alpha/(1. + alpha), 1.])
                    tinterval = _qva_split(tinterval)
                else:
                    tinterval = np.linspace(0, 1, 11)

                Ifx, errbnd, OK, fcall, vfcall = _qva_Vadapt(
                    _qva_f2, tinterval, rtol, atol, samples, nodes, wt, ewt,
                    fun, a, b, args, plot)

            elif a == -np.Inf and b != np.Inf:
                if nint > 2:
                    alpha = np.sqrt(b - interval[1:-1])
                    tinterval = np.hstack([-1., -alpha/(1. + alpha), 0.])
                    tinterval = _qva_split(tinterval)
                else:
                    tinterval = np.linspace(-1, 0, 11)

                Ifx, errbnd, OK, fcall, vfcall = _qva_Vadapt(
                    _qva_f3, tinterval, rtol, atol, samples, nodes, wt, ewt,
                    fun, a, b, args, plot)

            elif a == -np.Inf and b == np.Inf:
                if nint > 2:
                    # Analytical transformation suggested by K.L. Metlov:
                    alpha = np.tanh(np.arcsinh(2.*interval[1:-1])/2.)
                    tinterval = np.hstack([-1., alpha, 1.])
                    tinterval = _qva_split(tinterval)
                else:
                    tinterval = np.linspace(-1, 1, 11)

                Ifx, errbnd, OK, fcall, vfcall = _qva_Vadapt(
                    _qva_f4, tinterval, rtol, atol, samples, nodes, wt, ewt,
                    fun, a, b, args, plot)

        else:

            tinterval = np.linspace(-1, 1, 11)
            Ifx, errbnd, OK, fcall, vfcall = _qva_Vadapt(
                _qva_f5, tinterval, rtol, atol, samples, nodes, wt, ewt,
                fun, a, b, args, plot)

        if OK:
            status = 0  # success   
        else:
            print('***Integral does not satisfy error test.')
            print('***Approximate bound on error is', errbnd)
            status = 1

        if verbose:
            print(f"Integral: {Ifx} +/- {errbnd}")
            print(f"Function calls: {vfcall}, Function evaluations: {fcall}")

        self.integ = Ifx
        self.errbnd = errbnd
        self.status = status

################################################################################

def quad1d_test1(x, a=3, b=5):
    """
    Gladwell's problem no1. limits x=[0,8]
    Precise result: 0.33333333332074955152

    """
    return np.exp(-a*x)-np.cos(b*np.pi*x)

################################################################################

def quad1d_test2(x):
    """
    Gladwell's problem no2. limits x=[-1,2]
    Precise result: 5.9630898453302550932

    """
    return np.abs(x - 1/np.sqrt(3)) + np.abs(x + 1/np.sqrt(2))

################################################################################

def quad1d_test3(x, a=2.0/3):
    """
    Gladwell's problem no3. limits x=[0,1]
    Precise result: 3 with x^(-2d/3d)

    """
    return x**a

################################################################################

def quad1d_test4(x):
    """
    Gladwell's problem no3. limits x=[0,1]
    Precise result: 2.5066282746310005024

    """
    return np.exp(-x**2/2)

################################################################################

def quad1d_examples():

    print('\ntest 1 ###############################\n')
    ifx = quad1d(quad1d_test1, [0, 8], args=(3, 5), epsrel=0, epsabs=1e-12, singular=1, verbose=1).integ
    print('actual error:', ifx - 0.33333333332074955152)
    print('\ntest 2 ###############################\n')
    ifx = quad1d(quad1d_test2, [-1, 2], epsrel=0, epsabs=1e-12, singular=1, verbose=1).integ
    print('actual error:', ifx - 5.9630898453302550932)
    print('\ntest 2 with breakpoints ##############\n')
    ifx = quad1d(quad1d_test2, [-1, -1/np.sqrt(2), 1/np.sqrt(3), 2], epsrel=0, singular=1, epsabs=1e-12, verbose=1).integ
    print('actual error:', ifx - 5.9630898453302550932)
    print('\ntest 3 ###############################\n')
    ifx = quad1d(quad1d_test3, [0, 1], args=(-2.0/3,), epsrel=0, epsabs=1e-12, singular=1, verbose=1).integ
    print('actual error:', ifx - 3)
    print('\ntest 4 ###############################\n')
    ifx = quad1d(quad1d_test4, [-np.Inf, np.Inf], epsrel=1e-8, epsabs=0, singular=1, verbose=1).integ
    print('actual error:', ifx - 2.5066282746310005024, "\n")
    ifx = quad1d(quad1d_test4, [-8, 8], epsrel=1e-8, epsabs=0, singular=0, verbose=1, plot=1).integ
    print('actual error:', ifx - 2.5066282746310005024)

################################################################################

if __name__ == '__main__':
    quad1d_examples()
