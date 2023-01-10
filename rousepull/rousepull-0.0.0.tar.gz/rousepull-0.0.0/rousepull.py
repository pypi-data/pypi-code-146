"""
This module provides the `ForceInference` class, which uses the Rouse model to
infer forces in chromatin pulling experiments.

Units: once calibrated (using MSD data), the code works with physical units.
We use s, μm, pN.
"""
import os, sys

import numpy as np
import scipy.linalg as la
import scipy.special

class ForceInference:
    """
    Inference for a single trajectory ``x(t)``.

    Parameters
    ----------
    t : (N,) array
        sampling times in seconds, i.e. the times associated with the
        observations `!x`.
    x : (N, ...) array
        trajectory in μm. ``x[0]`` should be the equilibrium position of the
        locus (i.e. the math assumes that the locus is in equilibrium at the
        start of the trajectory). `!x` can have multiple dimensions; the first
        one is assumed to be time and consequently should match `!t`.
    Gamma : float
        MSD prefactor, used for calibration. Should have units
        ``μm^2/s^alpha``.
    tR : Rouse time of a finite tether on one side. If ``None`` (default), both
        tethers will be infinite. Mathematically this of course simply means
        ``tR = inf``. So far, a finite tether is implemented only for ``alpha =
        0.5``.
    alpha : float in (0, 1)
        Scaling exponent of the MSD, i.e. this controls viscoelasticity of
        the medium. So far this is implemented by tweaking the formulas, so no
        guarantees on correctness for any alpha != 0.5.  That being said,
        doesn't look too bad.
    s : float
        relative shift of the force switches (see Notes).

    Attributes
    ----------
    t, x : array
        like input
    M, Minv : (N, N) array
        the constitutive matrix ``M`` and its inverse, such that ``x = M.f``
        and ``f = Minv.x``.
    fpoly : (N,) array
        the inferred force profile (after running `populate()`)
    tf : (N+1,) array
        precise positions of the switches in the force profile, including
        beginning and end points.
    xf : (N+1,) array
        interpolated displacement at `!tf`. Mostly used to calculate `!vAt`.
    vAt : (N,) array
        estimate for locus velocity at the observation times. This is estimated
        as the velocity over the corresponding constant-force time window and
        thus depends on `!s`: ``vAt = Δxf / Δtf``.

    Notes
    -----
    The inference should always give ``f[0] = 0``, by construction.

    We assume that ``x(t)`` is sampled at discrete times ``t[i]``, giving
    ``x[i] := x(t[i])``, such that the locus is in equilibrium / at rest at
    ``x[0]`` before the experiment. The force profile is assumed to be
    piecewise constant, such that ``f[i]`` is the force acting over the
    half-open interval ``( t[i-1], t[i] ]``.
    
    Generalizing the logic above, we allow for a shift ``s`` of the
    force profile relative to the observation times, such that the switches in
    the force do not necessarily have to coincide with the observation times.
    This parameter is mostly intended to check that the ultimate conclusions
    drawn from the inferred forces do not depend on where exactly the switches
    are assumed to be (in which case the assumption of a piecewise constant
    force would be questionable in the first place). An overview over the
    different discretizations then looks as follows::

        t:        |     |     |     |     |     |
        x:        0     1     2     3     4     5
        f:     __0__|--1--|--2--|--3--|__4__|--5--
        shift:      '-s-'

    See also the Quickstart example for an illustration with (dummy) data.
    """
    def __init__(self, t, x=None, Gamma=None, tR=None, alpha=0.5, shift=1):
        if tR is not None and alpha != 0.5:
            print("Warning: finite tether not supported for alpha != 0.5!")

        self.t = t
        self.x = x
        self.tR = tR
        self.alpha = alpha
        self.s = shift

        if Gamma is not None:
            self._calibrate(Gamma)
        else:
            self._kT = 1
            self._spgk = 1
            self.Gamma = 2*self._kT/self._spgk

        self.updateM(tR=tR)

    def _calibrate(self, Gamma, kT=4.114e-3):
        """
        Set prefactors according to calibration

        Parameters
        ----------
        Gamma : float
            MSD prefactor of a single polymer locus, in units ``μm^2/s^alpha``.
        kT : float
            thermal energy, in units ``pN*μm``.
        """
        self._kT = kT
        self._spgk = 2*kT / Gamma # sqrt(pi * gamma * kappa) in the Rouse model
        self.Gamma = Gamma
        self.updateM()
        
    def updateM(self, tR=None):
        r"""
        Calculate the matrix ``M`` and its inverse.

        The expected trajectory x[i] given a force profile f[i] is given by ``x
        = M.f``, i.e. we can calculate the force from the observed trajectory
        as ``f = M\x``.

        Parameters
        ----------
        tR : float, optional
            finite tether Rouse time
        """
        if tR is None:
            def resqrt(x):
                return ((1+np.sign(x))/2*x)**self.alpha
        else:
            def resqrt(x):
                ind = x > 1e-10
                ret = np.zeros_like(x)
                ret[ind] = np.sqrt(x[ind])*(1-np.exp(-np.pi**2*tR/x[ind])) + np.pi**(3/2)*np.sqrt(tR)*scipy.special.erfc(np.pi*np.sqrt(tR/x[ind]))
                return ret

        tf = list( (1-self.s)*self.t[1:] + self.s*self.t[:-1] )
        tf = np.array([self.t[0]-self.t[1]+tf[0]] + tf + [self.t[-1] + tf[-1] - self.t[-2]])
        self.M = 1/self._spgk * ( resqrt(self.t[:, None] - tf[None, :-1]) 
                                - resqrt(self.t[:, None] - tf[None, 1:])
                                )
        self.invM = la.inv(self.M)
        self.tf = tf

### The mathematical basis ###
    def _generate(self, f):
        """
        Calculate trajectory from given force profile

        Parameters
        ----------
        f : (N,) array
            force profile, in pN

        Returns
        ------
        x : (N,) array
            expected trajectory, in μm
        """
        assert len(f) == len(self.t)
        return self.M @ f

    def _infer(self, x):
        """
        Infer force profile from observed trajectory

        Parameters
        ----------
        x : (N,) array
            observed trajectory, in μm

        Returns
        -------
        f : (N,) array
            inferred force profile, in pN

        See also
        --------
        populate
        """
        assert len(x) == len(self.t)
        return self.invM @ (x - x[[0]])
### ###

    def populate(self, x=None, returnf=False):
        """
        Populate this object with inference results.

        This is basically a wrapper for ``self._infer``, just that it also
        calculates some other stuff that could be useful, like velocities.

        Parameters
        ----------
        x : (N,) array, optional
            the trajectory to use, if not specified in ``self.x``
        returnf : bool, optional
            whether to return the output or just store internally (in
            ``self.fpoly``).

        Returns
        -------
        f : (N,) array
            inferred force profile, in pN; same as ``self.fpoly`` and only
            returned if ``returnf == True``.
        """
        if x is not None:
            self.x = x
        
        # The basic inference
        self.fpoly = -self._infer(self.x)

        # Calculate velocities "at" t[i]
        # Technically, velocity can just refer to average velocity over a given
        # time window; so we choose the same windows we also chose for the
        # forces, i.e. the ones given by tf. To calculate displacements
        # over these windows, approximate x(t) as linear between t[i].
        # xf[0] = 0 by construction
        # xf[-1] should be linearly extrapolated, same as tf[-1]
        xf = (1-self.s)*self.x[1:] + self.s*self.x[:-1]
        xf = np.append(np.insert(xf, 0, 0), xf[-1] + self.x[-1] - self.x[-2])
        self.xf = xf
        self.vAt = np.diff(self.xf) / np.diff(self.tf)

        if returnf:
            return self.fpoly

    def difMagnetic(self, fmagnetic):
        """
        Calculate the "unexplained force" as ``self.funex``.

        Parameters
        ----------
        fmagnetic : (N,) array
            total magnetic pull force
        """
        self.fmagnetic = fmagnetic
        self.funex = -self.fmagnetic - self.fpoly

### Noise ###
    def covTrajectory(self):
        """
        Covariance matrix for the trajectory, for fixed x[0].
        
        This is given by ::

            S(t, t') = 1/2*(MSD(t) + MSD(t') - MSD(|Δt|)) .

        Returns
        -------
        S : (N, N) array
        """
        t0 = self.t[:, None] - self.t[0]
        t1 = self.t[None, :] - self.t[0]

        return 0.5*self.Gamma*( t0**self.alpha + t1**self.alpha - np.abs(t0-t1)**self.alpha )

    def covForce(self):
        """
        Covariance matrix for the force.
        
        From covariance of the trajectory, this is simple Gaussian error
        propagation::

            S_force = M^{-1} @ S @ M^{-T} .

        Returns
        -------
        S_force : (N, N) array
        """
        return self.invM @ self.covTrajectory() @ self.invM.T

### Dragging ###
    def computeFdrag(self, density, mode=0, ix=1, returnFdrag=False, returnTrajectories=False):
        """
        Calculate additional force exerted on the locus due to dragging.

        Parameters
        ----------
        density : (N,) array
            the local density at the position of the locus. This is basically
            just a local proportionality factor.
        mode : int
            specifies the model to use. Implemented so far are

            |  0 = sticky chromatin
            |  1 = two-sided glove
            |  2 = one-sided glove

        ix : int or other index, optional
            if ``self.x`` is multidimensional, this should be an index such
            that ``x[:, ix]`` gives a 1D trace to work with.
        returnFdrag : bool, optional
            whether to return the dragging force or just store it internally in
            ``self.fdrag``.
        returnTrajectories : bool, optional
            whether to return the trajectories of the `!N` virtual particles

        Returns
        -------
        Fdrag : (N,) array
            the dragging force, in pN. Only returned if ``returnFdrag ==
            True``.
        """
        if len(self.x.shape) == 1:
            x = self.x
            v = self.vAt
        else:
            x = self.x[:, ix]
            v = self.vAt[:, ix]

        if returnTrajectories:
            trajs = np.zeros((len(x), len(x)))
        fdrag = np.zeros_like(x)
        for j in range(len(x)):
            offset = x[j]
            traj = x - offset
            traj[:j] = 0

            moveForward = v[j] > 0 # If moving backwards, the glove also works backwards!
            if mode == 2:
                moveForward = True

            while True:
                F = -self._infer(traj)
                if moveForward:
                    ind = np.nonzero(F > 1e-10) # can only exert restoring force
                else:
                    ind = np.nonzero(F < -1e-10)

                if len(ind) == 0 or mode == 0:
                    break
                ind = ind[0]

                F[ind:] = 0
                traj = self._generate(-F)
                traj[ind:] = (np.maximum if moveForward else np.minimum)(traj[ind:], x[ind:]-offset)

            fdrag += density[j]*F
            if returnTrajectories:
                trajs[:, j] = traj

        # Handle all the output possibilities
        if len(self.x.shape) == 1:
            self.fdrag = fdrag
        else:
            if not hasattr(self, 'fdrag'):
                self.fdrag = np.empty(self.x.shape)
                self.fdrag[:] = np.nan
            self.fdrag[:, ix] = fdrag

        if returnFdrag and returnTrajectories:
            return fdrag, trajs
        elif returnFdrag:
            return fdrag
        elif returnTrajectories:
            return trajs
