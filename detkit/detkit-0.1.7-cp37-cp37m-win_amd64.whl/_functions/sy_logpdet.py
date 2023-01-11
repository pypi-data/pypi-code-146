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
import scipy
import scipy.linalg
from ._math_utilities import logdet, triang_logdet

__all__ = ['sy_logpdet']


# ==========
# sy logpdet
# ==========

def sy_logpdet(A, X, Xp, method='proj', sym_pos=False, X_orth=False):
    """
    Implementation of `logpdet` function using scipy.
    """

    if method == 'legacy':
        return _sy_logpdet_legacy(A, X, sym_pos=sym_pos, X_orth=X_orth)
    elif method == 'proj':
        return _sy_logpdet_proj(A, X, X_orth=X_orth)
    elif method == 'comp':
        return _sy_logpdet_comp(A, X, Xp, sym_pos=sym_pos, X_orth=X_orth)
    else:
        raise ValueError('"method" should be either "legacy" or "proj", ' +
                         'or "comp".')


# =================
# sy logpdet legacy
# =================

def _sy_logpdet_legacy(A, X, sym_pos=False, X_orth=False):
    """
    Using legacy method.
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
        W = X.T @ Y
        logdet_W, sign_W = logdet(W, sym_pos=sym_pos)

    if X_orth:
        logdet_XtX = 0.0
    else:
        XtX = X.T @ X
        logdet_XtX, sign_XtX = logdet(XtX, sym_pos=True)

    logpdet_ = logdet_XtX - logdet_A - logdet_W

    return logpdet_, sign_A


# ===============
# sy logpdet proj
# ===============

def _sy_logpdet_proj(A, X, X_orth=False):
    """
    using proj method.
    """

    I = numpy.eye(A.shape[0])                                      # noqa: E741
    A_I = A - I

    if X_orth:
        M = A_I @ X
        S = M @ X.T

    else:
        XtX = X.T @ X
        L = scipy.linalg.cholesky(XtX, lower=True)
        Y = scipy.linalg.solve_triangular(L, X.T, lower=True)
        M = A_I @ Y.T
        S = M @ Y

    N = A - S
    logdet_N, sign_N = logdet(N, sym_pos=False)

    logpdet_ = -logdet_N

    return logpdet_, sign_N


# ===============
# sy logpdet comp
# ===============

def _sy_logpdet_comp(A, X, Xp, sym_pos=False, X_orth=False):
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

    loggdet_ = -logdet_Ap
    sign_ = sign_Ap

    return loggdet_, sign_
