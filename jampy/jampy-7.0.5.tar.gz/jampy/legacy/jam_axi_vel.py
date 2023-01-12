"""
#############################################################################

Copyright (C) 2003-2020, Michele Cappellari
E-mail: michele.cappellari_at_physics.ox.ac.uk

Updated versions of the software are available from my web page
http://purl.org/cappellari/software

If you have found this software useful for your research,
I would appreciate an acknowledgement to the use of the
"JAM modelling method of Cappellari (2008)"

This software is provided as is without any warranty whatsoever.
Permission to use, for non-commercial purposes is granted.
Permission to modify for personal or internal use is granted,
provided this copyright and disclaimer are included unchanged
at the beginning of the file. All other rights are reserved.
In particular, redistribution of the code is not allowed.

#############################################################################

MODIFICATION HISTORY:
    V1.0.0: Written and tested by Michele Cappellari, Oxford, 24 April 2008
    V1.1.0: First released version. MC, Oxford, 12 August 2008
    V1.2.0: Updated documentation. MC, Oxford, 14 August 2008
    V2.0.0: Implemented PSF convolution using interpolation on polar grid. Dramatic
        speed-up of calculation. Further documentation.
        MC, Oxford, 11 September 2008;
    V2.0.1: Bug fix: when EVEL was not given, the default was not properly set.
        Included keyword STEP. The keyword FLUX is now only used for output: the
        surface brightness for plotting is computed from the MGE model.
        MC, Windhoek, 29 September 2008
    V2.0.2: Bug fix: Velocity was not multiplied by sign(x) without convolution.
        MC, Oxford, 22 October 2008
    V2.0.3: Added keywords NRAD and NANG. Thanks to Michael Williams for reporting
        possible problems with too coarse interpolation.
        MC, Oxford, 21 November 2008
    V2.1.0: Allow for alternative definition of tangential anisotropy via the
        keyword GAMMA. MC, Oxford, 6 December 2008
    V2.1.1: Added keyword RBH. MC, Oxford 4 April 2009
    V2.1.2: Do not change KAPPA on output.
        Compute FLUX even when not plotting. MC, Oxford, 29 May 2009
    V2.1.3: Skip unnecessary interpolation when computing few points
        without PSF convolution. After feedback from Eric Emsellem.
        MC, Oxford, 6 July 2009
    V2.1.4: The routine TEST_JAM_AXISYMMETRIC_VEL with the usage example now
        adopts a more realistic input kinematics. MC, Oxford, 08 February 2010
    V2.1.5: Forces q_lum && q_pot < 1. MC, Oxford, 01 March 2010
    V2.1.6: Allow for counter-rotating components as described
        in Note 8 of the JAM paper. MC, Oxford, 10 March 2010
    V2.1.7: Use linear instead of smooth interpolation. After feedback
        from Eric Emsellem. MC, Oxford, 09 August 2010
    V2.1.8: Plot and output with FLUX keyword the PSF-convolved MGE
        surface brightness. MC, Oxford, 15 September 2010
    V2.1.9: Fix: always print output value of kappa on plots.
        MC, Oxford, 28 February 2011
    V2.2.0: Only calculates FLUX if required. MC, Oxford, 8 December 2011
    V2.2.1: Use renamed CAP_* routines to avoid potential naming conflicts.
        MC, Paranal, 8 November 2013
    V3.0.0: Translated from IDL into Python. MC, Winchester, 24 January 2014
    V3.1.0: Speed up by ~60x by broadcasting the inner integral, optimizing the
        LOS integration range and sacrificing some unnecessary accuracy.
        Included x and y proper motion components. MC, Oxford, 29 January 2014
    V3.1.1: Plot bi-symmetrized V as in IDL version. MC, Oxford, 24 February 2014
    V3.1.2: Support both Python 2.6/2.7 and Python 3.x. MC, Oxford, 25 May 2014
    V3.1.3: Use correct "MODIFICATION HISTORY". MC, Oxford, 5 August 2014
    V3.1.4: Modified final plot layout. MC, Oxford, 31 October 2014
    V3.1.5: Fixed potential program stop for models at very large radii.
        MC, Verona, 15 November 2014
    V3.1.6: Return chi2=None when vel is not given in input.
        MC, Oxford, 7 January 2015
    V3.1.7: Introduced further checks on matching input sizes.
        MC, Sydney, 5 February 2015
    V3.1.8: Improved density sampling when computing LOS integration interval.
      - Properly assign velocity symmetry before convolution as in IDL version.
      - Fixed possible program stop with negative Gaussians.
      - Changed meaning of goodbins to be a boolean vector.
        MC, Oxford, 23 May 2015
    V3.1.9: Plot bad bins on the data. MC, Oxford, 18 September 2015
    V3.1.10: Pass **kwargs for plotting. MC, Oxford, 23 February 2016
    V3.1.11: Use odd kernel size for convolution.
      - Fixed corner case with coordinates falling outside the
        interpolation region, due to finite machine precision.
        MC, Oxford, 17 February 2017
    V3.1.12: Included `flux_obs` keyword. Updated documentation.
      - Fixed DeprecationWarning in Numpy 1.12.
        MC, Oxford, 17 March 2017
    V3.1.13: Raise an error if goodbins is all False. MC, Oxford, 10 August 2017
    V3.1.14: Make default `step` depend on `sigmapsf` regardless of `pixsize`.
        MC, Oxford, 10 September 2017
    V3.1.15: Minor improvement to sampling of LOS integration range.
      - Fixed velocity symmetry with few values and no PSF convolution.
        Thanks to Martha Tabor (Nottingham) for reporting the bug.
      - Print a message when no PSF convolution was performed.
      - Broadcast kernel and MGE convolution loops.
      - Force `nsteps` to be odd. MC, Oxford, 22 January 2018
    V3.1.16: Check that PSF is normalized. MC, Oxford, 7 March 2018
    V3.1.17: Do not assume positive kappa when the input vector contains
        identical values. Thanks to Matha Tabor (Nottingham) for reporting this.
        MC, Oxford, 13 April 2018
    V3.1.18: Fixed MatplotlibDeprecationWarning in Matplotlib 2.2.
      - Changed imports for jam as a package.
      - Removed example. MC, Oxford, 17 April 2018
    V3.1.19: Dropped Python 2.7 support. MC, Oxford, 12 May 2018
    V3.1.20: Fixed clock DeprecationWarning in Python 3.7.
        MC, Oxford, 27 September 2018
    V3.2.0: Replaced quadva with TAHN LOS quadrature (~4x speedup).
        MC, Oxford, 30 May 2019
    V3.2.1: Use analytic mge_surf in convolution. MC, Oxford, 31 October 2019
    V3.2.2: Invert sign of V_x for consistency with Cappellari (2020) and
        with the new jam_axi_proj. MC, Oxford, 22 July 2020

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import special, signal, ndimage, integrate
from time import perf_counter as clock

from plotbin.plot_velfield import plot_velfield
from plotbin.symmetrize_velfield import symmetrize_velfield

##############################################################################

def mge_surf(x, y, surf, sigma, qobs):
    """ MGE surface brightness for a set of coordinates (x, y) """

    mge = surf*np.exp(-0.5/sigma**2*(x[..., None]**2 + (y[..., None]/qobs)**2))

    return mge.sum(-1)

##############################################################################

def bilinear_interpolate(xv, yv, im, xout, yout):
    """
    The input array has size im[ny,nx] as in the output
    of im = f(meshgrid(xv, yv))
    xv and yv are vectors of size nx and ny respectively.

    """
    ny, nx = im.shape
    assert (nx, ny) == (xv.size, yv.size), "Input arrays dimensions do not match"

    xi = (nx-1.)/(xv[-1] - xv[0]) * (xout - xv[0])
    yi = (ny-1.)/(yv[-1] - yv[0]) * (yout - yv[0])

    return ndimage.map_coordinates(im.T, [xi, yi], order=1, mode='nearest')

##############################################################################

def rotate_points(x, y, ang):
    """
    Rotates points conter-clockwise by an angle ANG in degrees.
    Michele cappellari, Paranal, 10 November 2013
    """
    theta = np.radians(ang)
    xNew = x*np.cos(theta) - y*np.sin(theta)
    yNew = x*np.sin(theta) + y*np.cos(theta)

    return xNew, yNew

##############################################################################

def integrand(u, s2_lum, q2_lum, dens_pot, s2_pot, q2_pot,
               R2, z2, bani, kappa, gamma, nu):

    """
    This routine computes the inner integrand of Eq.(38) of Cappellari (2008)
    for a model with constant anisotropy
    sigma_R**2 = b*sigma_z**2 and <V_R*V_z> = 0.

    """
    u2 = u**2
    s2q2_lum = s2_lum*q2_lum
    e2_pot = 1. - q2_pot

    c = e2_pot - s2q2_lum/s2_pot                            # equation (22)
    d = 1 - bani*q2_lum - ((1 - bani)*c + e2_pot*bani)*u2   # equation (23)

    # The next line gives an extra term for equation (38) using the alternative
    # definition of tangential anisotropy of equation (33) instead of the
    # default form of equation (35). This term is zero by default (gamma=0)
    # (also see note 10 here http://adsabs.harvard.edu/abs/2015ApJ...804L..21C)
    if np.any(gamma):
        d = d + gamma*bani*s2q2_lum/R2

    # Double summation over (j, k) of eq.(38) for all values of integration
    # variable u and z' LOS positions. The quadruple loop in (j, k, u, z') is
    # replaced by broadcast Numpy array operations.
    p2 = 1 - e2_pot*u2
    hj = np.exp(-0.5/s2_pot*u2*(R2+z2/p2))/np.sqrt(p2)      # equation (17)
    e = np.sqrt(q2_pot)*dens_pot*u2*hj
    arr = np.sign(kappa)*kappa**2*nu*(d/(1 - c*u2))*e       # equation (38)

    # arr has the dimensions (q_lum.size, q_pot.size, u.size, z.size)

    return arr.sum((0, 1)) # sum over light and mass Gaussians

##############################################################################

def los_integrand(z1, dens_lum, sigma_lum, qintr_lum,
                   dens_pot, sigma_pot, qintr_pot,
                   x1, y1, inc, beta, kappa, gamma, component, nsteps):
    """
    This function returns the outer integrand in equation (38)
    of Cappellari (2008, hereafter C08). Also included is the optional
    extension to proper motions as in D'Souza & Rix (2013, hereafter DR13).

    """
    s2_lum = sigma_lum**2
    q2_lum = qintr_lum**2
    s2_pot = sigma_pot**2
    q2_pot = qintr_pot**2
    bani = 1./(1. - beta) # Anisotropy ratio b = (sig_R/sig_z)**2

    # Tracer distribution parameters
    dens_lum = dens_lum[:, None, None, None]
    s2_lum = s2_lum[:, None, None, None]
    q2_lum = q2_lum[:, None, None, None]
    bani = bani[:, None, None, None]
    kappa = kappa[:, None, None, None]
    gamma = gamma[:, None, None, None]

    # Mass distribution parameters
    dens_pot = dens_pot[None, :, None, None]
    s2_pot = s2_pot[None, :, None, None]
    q2_pot = q2_pot[None, :, None, None]

    uu = np.linspace(0., 1., nsteps)  # integration variable from 0-1
    u = uu[None, None, :, None]

    z1 = z1[None, None, None, :]  # LOS integration variable
    R2 = (z1*np.sin(inc) - y1*np.cos(inc))**2 + x1**2  # Equation (25) of C08
    z2 = (z1*np.cos(inc) + y1*np.sin(inc))**2

    nu = dens_lum*np.exp(-0.5/s2_lum*(R2 + z2/q2_lum))
    tmp = integrand(u, s2_lum, q2_lum, dens_pot, s2_pot, q2_pot,
                     R2, z2, bani, kappa, gamma, nu)
    tmp = integrate.simps(tmp, dx=uu[1], axis=0)

    nu = nu.sum((0, 1, 2))  # Sum over luminous Gaussians

    if np.ptp(kappa):
        integ = np.sign(tmp)*np.sqrt(abs(nu*tmp))  # Note 8 pg. 77 of C08
    else:
        integ = np.sqrt(nu*tmp.clip(0)) if kappa[0] > 0 else -np.sqrt((-nu*tmp).clip(0))

    if component == 'x':
        f = z1*np.sin(inc) - y1*np.cos(inc)     # See Eq.(B9) of DR13
    elif component == 'y':
        f = x1*np.cos(inc)                      # See Eq.(B8) of DR13
    elif component == 'z':
        f = x1*np.sin(inc)                      # z' LOS equation (38) of C08

    # This routine returns a vector of values computed at different values of z1
    #
    G = 0.004301  # (km/s)^2 pc/Msun [6.674e-11 SI units (CODATA2018)]

    return 2.*np.sqrt(np.pi*G)*f*integ

##############################################################################

def surf_vlos(x1, y1, inc,
               dens_lum, sigma_lum, qintr_lum,
               dens_pot, sigma_pot, qintr_pot,
               beta, kappa, gamma, component, nsteps):
    """
    This routine gives the projected weighted first moment Sigma*<V_los>

    """
    # TANH quadrature rule
    rmax = 3*np.max(sigma_lum)
    tmax = 8    # break is rmax/tmax
    t, dt = np.linspace(-tmax, tmax, nsteps, retstep=True)
    scale = rmax/np.sinh(tmax)
    z1 = scale*np.sinh(t)
    dxdt = dt*scale*np.cosh(t)

    sb_mu1 = np.empty_like(x1)
    for j, (xj, yj) in enumerate(zip(x1, y1)):
        integ = los_integrand(z1, dens_lum, sigma_lum, qintr_lum,
                               dens_pot, sigma_pot, qintr_pot,
                               xj, yj, inc, beta, kappa, gamma, component, nsteps)
        sb_mu1[j] = integ @ dxdt     # DE quadrature

    return sb_mu1

##############################################################################

def vlos(x, y, inc_deg,
         surf_lum, sigma_lum, qobs_lum,
         surf_pot, sigma_pot, qobs_pot,
         beta, kappa, gamma, sigmaPsf, normPsf,
         pixSize, pixAng, step, nrad, nang, component, nsteps):
    """
    This routine gives the second V moment after convolution with a PSF.
    The convolution is done unp.sing interpolation of the model on a
    polar grid, as described in Appendix A of Cappellari (2008).

    """
    # Axisymmetric deprojection of both luminous and total mass.
    # See equation (12)-(14) of Cappellari (2008)
    #
    inc = np.radians(inc_deg)

    qintr_lum = qobs_lum**2 - np.cos(inc)**2
    if np.any(qintr_lum <= 0):
        raise RuntimeError('Inclination too low q_lum < 0')
    qintr_lum = np.sqrt(qintr_lum)/np.sin(inc)
    if np.any(qintr_lum < 0.05):
        raise RuntimeError('q_lum < 0.05 components')
    dens_lum = surf_lum*qobs_lum / (sigma_lum*qintr_lum*np.sqrt(2*np.pi))

    qintr_pot = qobs_pot**2 - np.cos(inc)**2
    if np.any(qintr_pot <= 0):
        raise RuntimeError('Inclination too low q_pot < 0')
    qintr_pot = np.sqrt(qintr_pot)/np.sin(inc)
    if np.any(qintr_pot < 0.05):
        raise RuntimeError('q_pot < 0.05 components')
    dens_pot = surf_pot*qobs_pot / (sigma_pot*qintr_pot*np.sqrt(2*np.pi))

    # Define parameters of polar grid for interpolation
    #
    w = sigma_lum < np.max(np.abs(x)) # Characteristic MGE axial ratio in observed range

    if w.sum() < 3:
        qmed = np.median(qobs_lum)
    else:
        qmed = np.median(qobs_lum[w])

    rell = np.sqrt(x**2 + (y/qmed)**2) # Elliptical radius of input (x,y)

    psfConvolution = (np.max(sigmaPsf) > 0) and (pixSize > 0)

    # Kernel step is 1/4 of largest value between sigma(min) and 1/2 pixel side.
    # Kernel half size is the sum of 3*sigma(max) and 1/2 pixel diagonal.
    if (nrad*nang > x.size) and (not psfConvolution): # Just calculate values

        xPol = x
        yPol = y

    else:  # Interpolate values on polar grid

        if psfConvolution:   # PSF convolution
            if step == 0:
                step = np.min(sigmaPsf)/4.
            mx = 3*np.max(sigmaPsf) + pixSize/np.sqrt(2)
        else:                                   # No convolution
            step = max(np.sqrt(2), np.min(rell)) # Minimum radius of 1pc
            mx = 0

        # Make linear grid in log of elliptical radius RAD and eccentric anomaly ANG
        # See Appendix A
        rmax = np.max(rell) + mx # Major axis of ellipse containing all data + convolution
        logRad = np.linspace(np.log(step/np.sqrt(2)), np.log(rmax), nrad) # Linear grid in np.log(rell)
        ang = np.linspace(0, np.pi/2, nang) # Linear grid in eccentric anomaly
        radGrid, angGrid = map(np.ravel, np.meshgrid(np.exp(logRad), ang))
        xPol = radGrid*np.cos(angGrid)
        yPol = radGrid*np.sin(angGrid) * qmed

    # The model Vel computation is only performed on the polar grid
    # which is then used to interpolate the values at any other location
    wmPol = surf_vlos(xPol, yPol, inc,
                      dens_lum, sigma_lum, qintr_lum,
                      dens_pot, sigma_pot, qintr_pot,
                      beta, kappa, gamma, component, nsteps)

    if psfConvolution: # PSF convolution

        nx = int(np.ceil(rmax/step))
        ny = int(np.ceil(rmax*qmed/step))
        x1 = np.linspace(0.5 - nx, nx - 0.5, 2*nx)*step
        y1 = np.linspace(0.5 - ny, ny - 0.5, 2*ny)*step
        xCar, yCar = np.meshgrid(x1, y1)  # Cartesian grid for convolution

        # Interpolate MGE model and Vel over cartesian grid
        r1 = 0.5*np.log(xCar**2 + (yCar/qmed)**2)  # Log elliptical radius of cartesian grid
        e1 = np.arctan2(np.abs(yCar/qmed), np.abs(xCar)) # Eccentric anomaly of cartesian grid

        # Division by mgePol before interpolation reduces interpolation error
        mgeCar = mge_surf(xCar, yCar, surf_lum, sigma_lum, qobs_lum)
        mgePol = mge_surf(xPol, yPol, surf_lum, sigma_lum, qobs_lum)
        wmCar = mgeCar*bilinear_interpolate(logRad, ang, (wmPol/mgePol).reshape(nang, nrad), r1, e1)

        if component in ('y', 'z'):
            wmCar *= np.sign(xCar) # Calculation was done in positive quadrant
        else:
            wmCar *= np.sign(yCar)  # Calculation was done in positive quadrant

        nk = int(np.ceil(mx/step))
        kgrid = np.linspace(-nk, nk, 2*nk + 1)*step
        xgrid, ygrid = np.meshgrid(kgrid, kgrid) # Kernel is square
        if pixAng != 0:
            xgrid, ygrid = rotate_points(xgrid, ygrid, pixAng)

        # Compute kernel with equation (A6) of Cappellari (2008).
        # Normalization is irrelevant here as it cancels out.
        #
        dx = pixSize/2
        sp = np.sqrt(2)*sigmaPsf
        xg, yg = xgrid[..., None], ygrid[..., None]
        kernel = normPsf*(special.erf((dx - xg)/sp) + special.erf((dx + xg)/sp)) \
                        *(special.erf((dx - yg)/sp) + special.erf((dx + yg)/sp))
        kernel = kernel.sum(2)   # Sum over PSF components

        # Seeing and aperture convolution with equation (A3)
        #
        muCar = signal.fftconvolve(wmCar, kernel, mode='same') \
              / signal.fftconvolve(mgeCar, kernel, mode='same')

        # Interpolate convolved image at observed apertures.
        # Aperture integration was already included in the kernel.
        #
        mu = bilinear_interpolate(x1, y1, muCar, x, y)

    else: # No PSF convolution

        muPol = wmPol/mge_surf(xPol, yPol, surf_lum, sigma_lum, qobs_lum)

        if nrad*nang > x.size:      # Just returns values
            mu = muPol
        else:                      # Interpolate values
            r1 = 0.5*np.log(x**2 + (y/qmed)**2) # Log elliptical radius of input (x,y)
            e1 = np.arctan2(np.abs(y/qmed), np.abs(x))    # Eccentric anomaly of input (x,y)
            mu = bilinear_interpolate(logRad, ang, muPol.reshape(nang, nrad), r1, e1)

            if component in ('y', 'z'):
                mu *= np.sign(x)  # Calculation was done in positive quadrant
            else:
                mu *= np.sign(y)  # Calculation was done in positive quadrant

    return mu, psfConvolution

##############################################################################

def jam_axi_vel(surf_lum, sigma_lum, qobs_lum, surf_pot, sigma_pot, qobs_pot,
                inc, mbh, distance, xbin, ybin, beta=None, component='z',
                evel=None, flux_obs=None, gamma=None, goodbins=None,
                kappa=None, nang=10, normpsf=1., nrad=20, nsteps=65, pixang=0.,
                pixsize=0., plot=True, quiet=False, rbh=0.01, sigmapsf=0.,
                step=0., vel=None, vmax=None, **kwargs):

    """

    Purpose
    -------

    This procedure calculates a prediction for the mean line-of-sight velocity
    V_z and the two proper motion components (V_x, V_y) for an anisotropic
    axisymmetric galaxy model. It implements the solution of the anisotropic
    Jeans equations presented in `Cappellari (2008, MNRAS, 390, 71)
    <https://ui.adsabs.harvard.edu/abs/2008MNRAS.390...71C>`_
    PSF convolution is done as described in the Appendix of that paper.

    Calling sequence
    ----------------

    .. code-block:: python

        from jampy.jam_axi_vel import jam_axi_vel

        velModel, kappa, chi2, flux = jam_axi_vel(
            surf_lum, sigma_lum, qobs_lum, surf_pot, sigma_pot, qobs_pot,
            inc, mbh, distance, xbin, ybin, beta=None, component='z',
            evel=None, gamma=None, goodbins=None, kappa=None, nang=10,
            normpsf=1., nrad=20, nsteps=50, pixang=0., pixsize=0.,
            plot=True, quiet=False, rbh=0.01, sigmapsf=0., step=0.,
            vel=None, vmax=None)

    Input parameters
    ----------------

    SURF_LUM:
        vector of length N containing the peak surface brightness of the
        MGE Gaussians describing the galaxy surface brightness in units of
        Lsun/pc^2 (solar luminosities per parsec^2).
    SIGMA_LUM:
        vector of length N containing the dispersion in arcseconds of
        the MGE Gaussians describing the galaxy surface brightness.
    QOBS_LUM:
        vector of length N containing the observed axial ratio of the MGE
        Gaussians describing the galaxy surface brightness.
    SURF_POT:
        vector of length M containing the peak value of the MGE Gaussians
        describing the galaxy surface density in units of Msun/pc^2 (solar
        masses per parsec^2). This is the MGE model from which the model
        potential is computed.

        In a common usage scenario, with a self-consistent model, one will use
        the same Gaussians for both the surface brightness and the potential.
        One will use JAM_AXISYMMETRIC_RMS to fit the global M/L and then call
        JAM_AXISYMMETRIC_VEL with SURF_POT = SURF_LUM*(M/L),
        SIGMA_POT = SIGMA_LUM and QOBS_POT = QOBS_LUM.
    SIGMA_POT:
        vector of length M containing the dispersion in arcseconds of
        the MGE Gaussians describing the galaxy surface density.
    QOBS_POT:
        vector of length M containing the observed axial ratio of the MGE
        Gaussians describing the galaxy surface density.
    INC:
        inclination in degrees (90 being edge-on).
    MBH:
        Mass of a nuclear supermassive black hole in solar masses.
    DISTANCE:
        distance in Mpc.
    XBIN:
        Vector of length P with the X coordinates in arcseconds of the bins
        (or pixels) at which one wants to compute the model predictions. The
        X-axis is assumed to coincide with the galaxy projected major axis. The
        galaxy center is at (0,0).

        When no PSF/pixel convolution is performed (SIGMAPSF=0 or PIXSIZE=0)
        there is a singularity at (0,0) which should be avoided by the input
        coordinates.
    YBIN:
        Vector of length P with the Y coordinates in arcseconds of the bins
        (or pixels) at which one wants to compute the model predictions. The
        Y-axis is assumed to concide with the projected galaxy symmetry axis.

    Optional keywords
    -----------------

    BETA:
        Vector of length N with the vertical anisotropy
        beta_z = 1 - (sigma_z/sigma_R)^2 of the individual MGE Gaussians.
        A scalar can be used if the model has constant anisotropy.
        (Default: BETA=0)
    COMPONENT:
        Set this keyword to either 'x' (=major axis), 'y' (=minor axis)
        or 'z' (=line-of-sight: default) to calculate the corresponding component
        of the velocity. The extension for x and y components is done as in
        D'Souza & Rix (2013, MNRAS, 429, 1887).
    EVEL:
        Vector of length P with the 1sigma error associated to the VEL
        measurements in each bin. (Default EVEL=1)
    FLUX_OBS:
        Optional mean surface brigfhtness of each bin for plotting.
    GAMMA:
        Vector of length N with the tangential anisotropy
        gamma = 1 - (sigma_phi/sigma_R)^2 of the individual MGE Gaussians.
        A scalar can be used if the model has constant anisotropy.
        (Default: GAMMA=0)

        IMPORTANT: In a common usage this keyword is *not* needed and the
        tangential anisotropy is only parameterized with the much more
        efficient KAPPA parameter below. However this form, which uses the
        definition of tangential anisotropy of equation (33) of Cappellari
        (2008), can be sometimes useful as an alternative (Sec.3.1.5 of
        Cappellari 2008 for a discussion).

        When this keyword is set and nonzero, one should generally not set the
        input keyword VEL with the vector of observed velocities. In this way
        KAPPA=1 is not fitted and the output VELMODEL has a well defined shape
        of the velocity ellipsoid. However VEL can still be set and KAPPA can
        be fitted to allow for further generality.
    GOODBINS:
        Boolean vector of length P with values True for the bins which
        have to be included in the fit (if requested) and chi^2 calculation.
        (Default: fit all bins).
    KAPPA:
        Rotation parameter (Default: KAPPA=1). Vector of length N defining
        by how much the model rotation of each individual MGE Gaussian is
        scaled, with respect to the velocity of a model with an oblate (GAMMA=0)
        velocity ellipsoid (Sec.3.1.5 of Cappellari 2008 for details).

        If the observed velocities are passed via the keyword VEL then KAPPA
        is the one required to match the observed projected angular momentum
        via equation (52) of Cappellari (2008).

        If the input KAPPA is a vector of length N, then the full vector is
        scaled to match the observed projected angular momentum.

        KAPPA can have both positive and negative elements to model
        counter-rotating stellar components (e.g. the S0 galaxy NGC4550).

        If GAMMA is set and nonzero then KAPPA defines by how much the model
        velocity field is scaled with respect to a model with tangential
        anisotropy GAMMA.
    NANG:
        Same as for NRAD, but for the number of angular intervals
        (default: NANG=10).
    NORMPSF:
        Vector of length Q with the fraction of the total PSF flux
        contained in the circular Gaussians describing the PSF of the
        observations. It has to be total(NORMPSF) = 1. The PSF will be used for
        seeing convolution of the model kinematics.
    NRAD:
        Number of logarithmically spaced radial positions for which the
        models is evaluated before interpolation and PSF convolution. One may
        want to increase this value if the model has to be evaluated over many
        orders of magnitudes in radius (default: NRAD=20). The computation time
        scales as NRAD*NANG.
    NSTEPS:
        Steps for the integration in the interval [0, 1] (default 50).
    PIXANG:
        angle between the observed spaxels and the galaxy major axis X.
    PIXSIZE:
        Size in arcseconds of the (square) spatial elements at which the
        kinematics is obtained. This may correspond to the side of the spaxel
        or lenslets of an integral-field spectrograph. This size is used to
        compute the kernel for the seeing and aperture convolution.

        If this is not set, or PIXSIZE=0, then convolution is not performed.
    PLOT:
        Set this keyword to produce a plot at the end of the calculation.
    QUIET:
        Set this keyword not to print values on the screen.
    RBH:
        This scalar gives the sigma in arcsec of the Gaussian representing the
        central black hole of mass MBH (See Section 3.1.2 of Cappellari 2008).
        The gravitational potential is indistinguishable from a point source
        for radii > 2*RBH, so the default RBH=0.01 arcsec is appropriate in
        most current situations.

        RBH should not be decreased unless actually needed!
    SIGMAPSF:
        Vector of length Q with the dispersion in arcseconds of the
        circular Gaussians describing the PSF of the observations.

        If this is not set, or SIGMAPSF=0, then convolution is not performed.

        IMPORTANT: PSF convolution is done by creating a 2D image, with pixels
        size given by STEP=MAX(SIGMAPSF,PIXSIZE/2)/4, and convolving it with
        the PSF + aperture. If the input radii RAD are very large with respect
        to STEP, the 2D image may require a too large amount of memory. If this
        is the case one may compute the model predictions at small radii
        separately from those at large radii, where PSF convolution is not
        needed.
    STEP:
        Spatial step for the model calculation and PSF convolution in arcsec.
        This value is automatically computed by default as
        STEP=MAX(SIGMAPSF,PIXSIZE/2)/4. It is assumed that when PIXSIZE or
        SIGMAPSF are big, high resolution calculations are not needed. In some
        cases however, e.g. to accurately estimate the central Vrms in a very
        cuspy galaxy inside a large aperture, one may want to override the
        default value to force smaller spatial pixels using this keyword.
    VEL:
        Vector of length P with the input observed mean stellar velocity V at
        the coordinates positions given by the vectors XBIN and YBIN.
    VMAX:
        Maximum absolute value of the velocity to plot.

    Output parameters
    -----------------

    VELMODEL:
        Vector of length P with the model predictions for the mean
        velocity of each bin.
    KAPPA:
        Best fitting kappa parameter. If kappa is given in input, this value
        represents by how much the input need to be scaled to reproduce the
        projected angular momentum of the data.
    CHI2:
        Reduced chi^2 describing the quality of the fit::

            chi^2 = total(((vel[goodBins]-velModel[goodBins])/evel[goodBins])^2)
                  / goodBins.sum()

        IMPORTANT: by default the rotation parameter KAPPA is determined by
        requiring the projected angular momentum to be the same in the data and
        in the model. The chi^2 is not necessarily minimized (Sec.4.2 of
        Cappellari 2008 for details).
    FLUX:
        Vector of length P with the PSF-convolved MGE surface brightness of
        each bin in Lsun/pc^2, used to plot the isophotes on the model results.

    """
    assert nsteps % 2 == 1, "`nsteps` must be odd"  # for optimal Simpson
    if beta is None:
        beta = np.zeros_like(surf_lum)  # Anisotropy parameter beta = 1 - (sig_z/sig_R)**2  (beta=0-->circle)
    if kappa is None:
        kappa = np.ones_like(surf_lum)  # Anisotropy parameter: V_obs = kappa * V_iso (kappa=1-->circle)
    if gamma is None:
        gamma = np.zeros_like(surf_lum)  # Anisotropy parameter gamma = 1 - (sig_phi/sig_R)^2 (gamma=0-->circle)
    assert (surf_lum.size == sigma_lum.size == qobs_lum.size
            == beta.size == gamma.size == kappa.size), "The luminous MGE components and anisotropies do not match"
    assert surf_pot.size == sigma_pot.size == qobs_pot.size, "The total mass MGE components do not match"
    assert xbin.size == ybin.size, "xbin and ybin do not match"
    if vel is not None:
        if evel is None:
            evel = np.full_like(vel, 5.)  # Constant 5 km/s errors
        if goodbins is None:
            goodbins = np.ones_like(vel, dtype=bool)
        else:
            assert goodbins.dtype == bool, "goodbins must be a boolean vector"
            assert np.any(goodbins), "goodbins must contain some True values"
        assert xbin.size == vel.size == evel.size == goodbins.size, "(vel, evel, goodbins) and (xbin, ybin) do not match"
    assert component in ['x', 'y', 'z'], "component must be one of 'x', 'y', 'z'"

    sigmapsf = np.atleast_1d(sigmapsf)
    normpsf = np.atleast_1d(normpsf)
    assert sigmapsf.size == normpsf.size, "sigmaPSF and normPSF do not match"
    assert round(np.sum(normpsf), 2) == 1, "PSF not normalized"

    pc = distance*np.pi/0.648 # Constant factor to convert arcsec --> pc

    surf_lum_pc = surf_lum
    surf_pot_pc = surf_pot
    sigma_lum_pc = sigma_lum*pc         # Convert from arcsec to pc
    sigma_pot_pc = sigma_pot*pc         # Convert from arcsec to pc
    xbin_pc = xbin*pc                   # Convert all distances to pc
    ybin_pc = ybin*pc
    pixSize_pc = pixsize*pc
    sigmaPsf_pc = sigmapsf*pc
    step_pc = step*pc

    # Add a Gaussian with small sigma and the same total mass as the BH.
    # The Gaussian provides an excellent representation of the second moments
    # of a point-like mass, to 1% accuracy out to a radius 2*sigmaBH.
    # The error increses to 14% at 1*sigmaBH, independently of the BH mass.
    #
    if mbh > 0:
        sigmaBH_pc = rbh*pc # Adopt for the BH just a very small size
        surfBH_pc = mbh/(2*np.pi*sigmaBH_pc**2)
        surf_pot_pc = np.append(surfBH_pc, surf_pot_pc) # Add Gaussian to potential only!
        sigma_pot_pc = np.append(sigmaBH_pc, sigma_pot_pc)
        qobs_pot = np.append(1., qobs_pot)  # Make sure vectors do not have extra dimensions

    qobs_lum = qobs_lum.clip(0, 0.999)
    qobs_pot = qobs_pot.clip(0, 0.999)

    t = clock()
    velModel, psfConvolution = vlos(
        xbin_pc, ybin_pc, inc, surf_lum_pc, sigma_lum_pc, qobs_lum,
        surf_pot_pc, sigma_pot_pc, qobs_pot, beta, kappa, gamma,
        sigmaPsf_pc, normpsf, pixSize_pc, pixang, step_pc,
        nrad, nang, component, nsteps)

    if not quiet:
        print('jam_axis_vel elapsed time sec: %.2f' % (clock() - t))
        if not psfConvolution:
            txt = "No PSF convolution:"
            if np.max(sigmapsf) == 0:
                txt += " sigmapsf == 0;"
            if pixsize == 0:
                txt += " pixsize == 0;"
            print(txt)

    # Analytic convolution of the MGE model with an MGE circular PSF
    # using Equations (4,5) of Cappellari (2002, MNRAS, 333, 400).
    # Broadcast triple loop over (n_MGE, n_PSF, n_bins)
    #
    sigmaX2 = sigma_lum**2 + sigmapsf[:, None]**2
    sigmaY2 = (sigma_lum*qobs_lum)**2 + sigmapsf[:, None]**2
    surf_conv = surf_lum_pc*qobs_lum*sigma_lum**2*normpsf[:, None]/np.sqrt(sigmaX2*sigmaY2)
    flux = surf_conv[..., None]*np.exp(-0.5*(xbin**2/sigmaX2[..., None] + ybin**2/sigmaY2[..., None]))
    flux = flux.sum((0, 1))  # PSF-convolved Lsun/pc**2

    ####### Output and optional M/L fit
    # If RMS keyword is not given all this section is skipped

    if vel is None:
        
        chi2 = None
        
    else:

        # Only consider the good bins for the chi**2 estimation
        #
        # Scale by having the same angular momentum
        # in the model and in the galaxy (equation 52)
        #
        kappa2 = np.sum(np.abs(vel[goodbins]*xbin[goodbins])) \
               / np.sum(np.abs(velModel[goodbins]*xbin[goodbins]))
        kappa = kappa*kappa2  # Rescale input kappa by the best fit

        # Measure the scaling one would have from a standard chi^2 fit of the V field.
        # This value is only used to get proper sense of rotation for the model.
        # y1 = rms; dy1 = erms (y1 are the data, y2 the model)
        # scale = total(y1*y2/dy1^2)/total(y2^2/dy1^2)  (equation 51)
        #
        kappa3 = np.sum(vel[goodbins]*velModel[goodbins]/evel[goodbins]**2) \
               / np.sum((velModel[goodbins]/evel[goodbins])**2)

        velModel *= kappa2*np.sign(kappa3)

        chi2 = np.sum(((vel[goodbins]-velModel[goodbins])/evel[goodbins])**2) / goodbins.sum()

        if not quiet:
            print('inc=%.1f kappa=%.2f beta_z=%.2f BH=%.2e chi2/DOF=%#.3g' % (inc, kappa[0], beta[0], mbh, chi2))
            mass = 2*np.pi*surf_pot_pc*qobs_pot*sigma_pot_pc**2
            print('Total mass MGE %#.4g:' % np.sum(mass))

        if plot:

            if flux_obs is None:
                flux_obs = flux

            vel1 = vel.copy() # Only symmetrize good bins
            vel1[goodbins] = symmetrize_velfield(xbin[goodbins], ybin[goodbins], vel[goodbins], sym=1)

            if vmax is None:
                vmax = np.percentile(np.abs(vel1[goodbins]), 99)

            plt.clf()
            plt.subplot(121)
            plot_velfield(xbin, ybin, vel1, vmin=-vmax, vmax=vmax, flux=flux_obs, **kwargs)
            plt.title(r"Input $V_{\rm los}$")

            plt.subplot(122)
            plot_velfield(xbin, ybin, velModel, vmin=-vmax, vmax=vmax, flux=flux, **kwargs)
            plt.plot(xbin[~goodbins], ybin[~goodbins], 'ok', mec='white')
            plt.title(r"Model $V_{\rm los}$")
            plt.tick_params(labelleft=False)
            plt.subplots_adjust(wspace=0.03)

    return velModel, kappa, chi2, flux

##############################################################################
