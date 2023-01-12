"""
#############################################################################

    Copyright (C) 2019, Michele Cappellari

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

#############################################################################

V1.0.0: Ported to Python from Shampine's MATLAB version
        by Michele Cappellari, Oxford, 4 June 2019

"""
import numpy as np
import matplotlib.pyplot as plt

################################################################################

class quad2d:
    """
    quad2d Purpose
    ----------------

    quad2d numerically evaluate the integral of f(x, y) over a plane region.

    It implements the algorithm described in
    `Shampine (2008) <https://doi.org/10.1016/j.amc.2008.02.012>`_

    Calling Sequence
    ----------------

    .. code-block:: python

        res = quad2d(fun, [a, b], [c, d], epsrel=0, epsabs=1e-5,  args=())
        print(f"integral = {res.integ} +/- {res.errbnd}")
        print("function calls:", res.fcall)

    approximates the integral

    .. math::

        I = \int_a^b \int_c^d f(x,y) dy dx

    Input Parameters
    ----------------

    fun:
        Evaluates ``f(x,y)``.  It must accept arrays X and Y and return an
        array ``Z = f(X,Y)`` of corresponding values. These arrays are all 14x14.
        The region is a generalized rectangle which is described in Cartesian
        coordinates (x,y) by ``a <= x <= b`` -- A and B must be constants and
        ``c <= y <= d`` -- C and D can be constants or functions of x that
        describe the lower and upper boundaries. Functions must be vectorized.
        ``res.integ`` is an approximation to the integral with an estimated
        bound ``ERRBND`` on the error that satisfies  ``ERRBND <= 1e-5``.
    epsabs:
        Absolute error tolerance
    epsrel:
        Relative error tolerance

        quad2d attempts to satisfy ERRBND <= max(epsabs, epsrel*|Q|).
        This is absolute error control when |Q| is sufficiently small and
        relative error control when |Q| is larger. A default tolerance
        value is used when a tolerance is not specified. The default value
        of 'epsrel' is 1e-5. The default value of 'epsabs' is 0.
    singular: quad2d can be applied to f(x,y) that are singular on a
       boundary. With value True, this option causes quad2d to use
       transformations to weaken singularities for better performance.
    args:
        Parameters to pass to the user function ``fun``

    """
    def __init__(self, fun, xlim, ylim, epsrel=1e-5, epsabs=0,
                 plot=False, verbose=False, singular=False, args=()):

        a, b = xlim
        c, d = ylim
        if callable(c):
            self.phiBvar = c
        elif np.isscalar(c):
            self.phiBvar = lambda x: np.full_like(x, c)
        else:
            raise ValueError('C must be a constant or a function')

        if callable(d):
            self.phiTvar = d
        elif np.isscalar(d):
            self.phiTvar = lambda x: np.full_like(x, d)
        else:
            raise ValueError('D must be a constant or a function')

        if plot:
            plt.figure('quad2d')
            plt.clf()
            fig, self.axis = plt.subplots(2, gridspec_kw={'hspace': 0.02},
                                          sharex=True, sharey=True, num='quad2d')
            self.axis[0].set_ylabel('y')
            self.axis[1].set_xlabel('x')
            self.axis[1].set_ylabel('y')
            self.xall = self.yall = self.zall = []

        self.plot = plot
        self.EPS = 100.*np.finfo(float).eps
        self.singular = singular

        if singular:
            thetaL, thetaR = 0, np.pi
            phiB, phiT = 0, np.pi
        else:
            thetaL, thetaR = a, b
            phiB, phiT = 0, 1

        # Set defaults and then process optional values.
        self.FUN = fun
        self.fcall = 0
        self.AREA = (thetaR - thetaL)*(phiT - phiB)

        # Gauss-Kronrod (3,7) pair with degrees of precision 5 and 11.
        NODES = np.array([-0.9604912687080202, -0.7745966692414834, -0.4342437493468026,
                          0, 0.4342437493468026, 0.7745966692414834, 0.9604912687080202])
        self.NODES = np.hstack([NODES + 1, NODES + 3])/4
        WT3 = np.array([0, 5, 0, 8, 0, 5, 0])/9
        WT7 = np.array([0.1046562260264672, 0.2684880898683334, 0.4013974147759622,
                        0.4509165386584744, 0.4013974147759622, 0.2684880898683334,
                        0.1046562260264672])

        # Compute initial approximations on four subrectangles.  Initialize LIST
        # of information about subrectangles for which the approximations are
        # not sufficiently accurate.  NLIST is the number of subrectangles that
        # remain to be processed.  ERRBND is a bound on the error.
        Qsub, esub = self.tensor(a, b, thetaL, thetaR, phiB, phiT, WT3, WT7, args)
        self.integ = Qsub.sum()
        # Use an artificial value of TOL to force the program to refine.
        self.TOL = self.EPS*np.abs(self.integ)
        self.ERR_OK = 0
        self.ADJUST = 1
        self.LIST = np.zeros((200, 7))
        self.NLIST = -1
        self.Save2LIST(Qsub, esub, thetaL, thetaR, phiB, phiT)
        if self.NLIST < 0 or self.errbnd <= self.TOL:
            return

        while True:
            # Get entries from LIST corresponding to the biggest (adjusted) error.
            q, e, thetaL, thetaR, phiB, phiT = self.NextEntry()

            # Approximate integral over four subrectangles.
            Qsub, esub = self.tensor(a, b, thetaL, thetaR, phiB, phiT, WT3, WT7, args)

            # Saved in LIST is "e", a conservative estimate of the error in the
            # approximation "q" of the integral over a rectangle.  Newq = sum(Qsub)
            # is a much better approximation to the integral.  It is used here to
            # estimate the error in "q" and thereby determine that the estimator is
            # conservative by a factor of "ADJUST".  This factor is applied to the
            # estimate of the error in "Newq" to get a more realistic estimate.
            # This scheme loses the sign of the error, so a conservative local test
            # is used to decide convergence.
            Newq = Qsub.sum()
            self.ADJUST = min(1, abs(q - Newq)/e)
            self.integ += Newq - q
            TOL = max(epsabs, epsrel*abs(self.integ))/8
            TOL = max(TOL, self.EPS*abs(self.integ))
            self.Save2LIST(Qsub, esub, thetaL, thetaR, phiB, phiT)

            # Test for convergence and failures.
            if self.NLIST < 0 or self.errbnd <= TOL:
                break
            elif self.NLIST >= 2000:
                if self.errbnd > max(epsabs, max(self.EPS, epsrel)*abs(self.integ)):
                    raise ValueError(f'Maximum number of subintervals {self.NLIST}: Q does NOT pass error test.')
                else:
                    print(f'Maximum number of subintervals {self.NLIST}: Q appears to pass error test.')
                break

        if verbose:
            print(f"Integral: {self.integ} +/- {self.errbnd}")
            print(f"Function calls: {self.fcall} Function evaluations: {self.fcall*14**2}")

        if self.plot:
            self.axis[1].tricontourf(self.xall, self.yall, self.zall)
            self.axis[1].plot(self.xall, self.yall, 'w,')

################################################################################

    def tensor(self, a, b, thetaL, thetaR, phiB, phiT, WT3, WT7, args):
        """
        Compute the integral with respect to theta from thetaL to thetaR of the
        integral with respect to phi from phiB to phiT of F in four blocks.

        """
        n = WT7.size
        dtheta = thetaR - thetaL
        theta = thetaL + dtheta*self.NODES
        if self.singular:
            xx = 0.5*(b + a) + 0.5*(b - a)*np.cos(theta)
        else:
            xx = theta
        dphi = phiT - phiB
        phi = (phiB + dphi*self.NODES)[:, None]
        top = self.phiTvar(xx)
        bottom = self.phiBvar(xx)
        dydt = top - bottom
        if self.singular:
            t = 0.5 + 0.5*np.cos(phi)
        else:
            t = phi
        x = np.tile(xx, (2*n, 1))
        y = bottom + t*dydt
        z = self.FUN(x.ravel(), y.ravel(), *args)
        z = z.reshape(x.shape)
        self.fcall += 1
        if self.singular:
            z *= 0.25*(b - a)*np.sin(phi)*(dydt*np.sin(theta))
        else:
            z *= dydt

        # Split array into four n*n quadrants
        zz = z.reshape(2, n, 2, n).swapaxes(1, 2).reshape(4, n, n)

        # Four tensor products: Gauss 3 point formula
        esub = WT3 @ zz @ WT3
        esub = (esub/4)*(dtheta/2)*(dphi/2)

        # Four tensor products: Kronrod 7 point formula
        Qsub = WT7 @ zz @ WT7
        Qsub = (Qsub/4)*(dtheta/2)*(dphi/2)

        esub = np.abs(esub - Qsub)

        if self.plot:
            self.axis[0].plot(x.ravel(), y.ravel(), '+')
            self.xall = np.append(self.xall, x)
            self.yall = np.append(self.yall, y)
            self.zall = np.append(self.zall, z)

        return Qsub, esub

################################################################################

    def NextEntry(self):
        """
        Take entries from LIST corresponding to the biggest adjusted error

        """
        index = np.argmax(np.abs(self.LIST[:self.NLIST + 1, 6]))
        row = self.LIST[index, :6]
        self.LIST = np.delete(self.LIST, index, axis=0)
        self.NLIST -= 1

        return row

################################################################################

    def Save2LIST(self, Qsub, esub, thetaL, thetaR, phiB, phiT):
        """
        Save to the list information about subrectangles for which the
        integral is not sufficiently accurate. NLIST is the number of
        subrectangles to be processed.

        """
        dtheta = thetaR - thetaL
        dphi = phiT - phiB
        localtol = self.TOL*(dtheta/2)*(dphi/2)/self.AREA
        localtol = max(localtol, self.EPS*abs(Qsub.sum()))

        adjerr = self.ADJUST*esub
        if self.NLIST + 5 > len(self.LIST):
            self.LIST = np.vstack([self.LIST, np.zeros((100, 7))])

        if adjerr[0] > localtol:
            self.NLIST += 1
            self.LIST[self.NLIST] = [Qsub[0], esub[0], thetaL, thetaL + dtheta/2, phiB, phiB + dphi/2, adjerr[0]]
        else:
            self.ERR_OK += adjerr[0]

        if adjerr[1] > localtol:
            self.NLIST += 1
            self.LIST[self.NLIST] = [Qsub[1], esub[1], thetaL + dtheta/2, thetaR, phiB, phiB + dphi/2, adjerr[1]]
        else:
            self.ERR_OK += adjerr[1]

        if adjerr[2] > localtol:
            self.NLIST += 1
            self.LIST[self.NLIST] = [Qsub[2], esub[2], thetaL, thetaL + dtheta/2, phiB + dphi/2, phiT, adjerr[2]]
        else:
            self.ERR_OK += adjerr[2]

        if adjerr[3] > localtol:
            self.NLIST += 1
            self.LIST[self.NLIST] = [Qsub[3], esub[3], thetaL + dtheta/2, thetaR, phiB + dphi/2, phiT, adjerr[3]]
        else:
            self.ERR_OK += adjerr[3]

        self.errbnd = self.ERR_OK + self.LIST[:, 6].sum()

################################################################################
