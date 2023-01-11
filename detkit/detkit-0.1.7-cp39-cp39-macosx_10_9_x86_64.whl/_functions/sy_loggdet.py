# SPDX-FileCopyrightText: Copyright 2022, Siavash Ameli <sameli@berkeley.edu>
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the license found in the LICENSE.txt file in the root directory
# of this source tree.


# =======
# Imports
# =======

import numpy
import numpy.linalg
import scipy.linalg
from ._math_utilities import logdet, triang_logdet

__all__ = ['sy_loggdet']


# ==========
# sy loggdet
# ==========

def sy_loggdet(A, X, Xp, method='proj', sym_pos=False, X_orth=False):
    """
    Implementation of `loggdet` function using scipy.
    """

    if method == 'legacy':
        return _sy_loggdet_legacy(A, X, sym_pos=sym_pos)
    elif method == 'proj':
        return _sy_loggdet_proj(A, X, X_orth=X_orth)
    elif method == 'comp':
        return _sy_loggdet_comp(A, X, Xp, sym_pos=sym_pos, X_orth=X_orth)
    else:
        raise ValueError('"method" should be either "legacy", "proj", ' +
                         'or "comp".')


# =================
# sy loggdet legacy
# =================

def _sy_loggdet_legacy(A, X, sym_pos=False):
    """
    using legacy method.
    """

    if sym_pos:

        L = scipy.linalg.cholesky(A, lower=True)
        logdet_L, sign_L = triang_logdet(L)
        logdet_A = 2.0 * logdet_L
        sign_A = sign_L

        Y = scipy.linalg.solve_triangular(L, X, lower=True)
        W = Y.T @ Y
        logdet_W, sign_W = logdet(W, sym_pos=sym_pos)

    else:

        lu, piv = scipy.linalg.lu_factor(A)
        logdet_A, sign_A = triang_logdet(lu)

        Y = scipy.linalg.lu_solve((lu, piv), X)

        # If Y is inf, it means A is singular. Remove inf to compute pseudo
        # inverse of A instead.
        Y_inf = numpy.isinf(Y)
        if numpy.any(Y_inf):
            Y[Y_inf] = 0.0

        W = X.T @ Y
        logdet_W, sign_W = logdet(W, sym_pos=sym_pos)

    loggdet_ = logdet_A + logdet_W

    return loggdet_, sign_A


# ===============
# sy loggdet proj
# ===============

def _sy_loggdet_proj(A, X, X_orth=False):
    """
    using proj method.
    """

    I = numpy.eye(A.shape[0])                                      # noqa: E741

    A_I = A - I

    if X_orth:
        M = A_I @ X
        S = M @ X.T
        logdet_XtX = 0.0

    else:
        XtX = X.T @ X
        L = scipy.linalg.cholesky(XtX, lower=True)
        logdet_L, sign_L = triang_logdet(L)
        logdet_XtX = 2.0 * logdet_L
        Y = scipy.linalg.solve_triangular(L, X.T, lower=True)
        M = A_I @ Y.T
        S = M @ Y

    N = S - A
    logdet_N, sign_N = logdet(N, sym_pos=False)
    loggdet_ = logdet_N + logdet_XtX

    return loggdet_, sign_N


# ===============
# sy loggdet comp
# ===============

def _sy_loggdet_comp(A, X, Xp, sym_pos=False, X_orth=False):
    """
    Using compression method.
    """

    # Finding Xp, the orthonormal complement of X
    if Xp is None:
        q, r = numpy.linalg.qr(X, mode='complete')
        Xp = q[:, X.shape[1]:]

    # Computing compression of A on the column space of Xp
    Ap = Xp.T @ A @ Xp

    # Logdet of Ap
    logdet_Ap, sign_Ap = logdet(Ap, sym_pos=sym_pos)

    # Logdet of XtX
    if X_orth:
        sign_XtX = 1.0
        logdet_XtX = 0.0

    else:
        XtX = X.T @ X
        L = scipy.linalg.cholesky(XtX, lower=True)
        logdet_L, sign_L = triang_logdet(L)
        logdet_XtX = 2.0 * logdet_L
        sign_XtX = 1.0

    loggdet_ = logdet_Ap + logdet_XtX
    sign_ = sign_Ap * sign_XtX

    return loggdet_, sign_
