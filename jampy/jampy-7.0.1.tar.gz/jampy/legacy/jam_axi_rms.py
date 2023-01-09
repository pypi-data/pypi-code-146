"""
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

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import special, signal, ndimage
from time import perf_counter as clock

from plotbin.plot_velfield import plot_velfield
from plotbin.symmetrize_velfield import symmetrize_velfield
from jampy.quad1d import quad1d

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
    ny, nx = np.shape(im)
    assert (nx, ny) == (xv.size, yv.size), "Input arrays dimensions do not match"

    xi = (nx - 1.)/(xv[-1] - xv[0]) * (xout - xv[0])
    yi = (ny - 1.)/(yv[-1] - yv[0]) * (yout - yv[0])

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

def integrand(u1,
               dens_lum, sigma_lum, q_lum,
               dens_pot, sigma_pot, q_pot,
               x1, y1, inc, beta, tensor):
    """
    This routine computes the integrand of Eq.(28) of Cappellari (2008; C08) for
    a model with constant anisotropy sigma_R**2 = b*sigma_z**2 and <V_R*V_z> = 0.
    The components of the proper motion dispersions tensor are calculated as
    described in note 5 of C08.
    See Cappellari (2012; C12 http://arxiv.org/abs/1211.7009)
    for explicit formulas for the proper motion tensor.
    The formulas are also given in Appendix A3 of Cappellari (2020, C20)
    https://ui.adsabs.harvard.edu/abs/2020MNRAS.494.4819C


    """
    dens_lum = dens_lum[:, None, None]
    sigma_lum = sigma_lum[:, None, None]
    q_lum = q_lum[:, None, None]
    beta = beta[:, None, None]

    dens_pot = dens_pot[None, :, None]
    sigma_pot = sigma_pot[None, :, None]
    q_pot = q_pot[None, :, None]

    u = u1[None, None, :]

    kani = 1./(1 - beta)  # Anisotropy ratio b = (sig_R/sig_z)**2
    ci = np.cos(inc)
    si = np.sin(inc)
    si2 = si**2
    ci2 = ci**2
    x2 = x1**2
    y2 = y1**2
    u2 = u**2

    s2_lum = sigma_lum**2
    q2_lum = q_lum**2
    e2_lum = 1 - q2_lum
    s2q2_lum = s2_lum*q2_lum

    s2_pot = sigma_pot**2
    e2_pot = 1 - q_pot**2

    # Double summation over (j, k) of eq.(28) for all values of integration variable u.
    # The triple loop in (j, k, u) is replaced by broadcast Numpy array operations.
    e2u2_pot = e2_pot*u2
    a = 0.5*(u2/s2_pot + 1/s2_lum)               # equation (29) in C08
    b = 0.5*(e2u2_pot*u2/(s2_pot*(1 - e2u2_pot)) + e2_lum/s2q2_lum) # equation (30) in C08
    c = e2_pot - s2q2_lum/s2_pot                  # equation (22) in C08
    d = 1 - kani*q2_lum - ((1 - kani)*c + e2_pot*kani)*u2 # equation (23) in C08
    e = a + b*ci2
    if tensor == 'xx':
        f = kani*s2q2_lum + d*((y1*ci*(a+b)/e)**2 + si2/(2*e)) # equation (4) in C12
    elif tensor == 'yy':
        f = s2q2_lum*(si2 + kani*ci2) + d*x2*ci2  # equation (5) in C12
    elif tensor == 'zz':
        f = s2q2_lum*(ci2 + kani*si2) + d*x2*si2  # z' LOS equation (28) in C08
    elif tensor == 'xy':
        f = -d*np.abs(x1*y1)*ci2*(a+b)/e          # equation (6) in C12
    elif tensor == 'xz':
        f = -d*np.abs(x1*y1)*si*ci*(a+b)/e         # -equation (7) in C12
    elif tensor == 'yz':
        f = -si*ci*(s2q2_lum*(1 - kani) - d*x2)   # -equation (8) in C12

    # arr has the dimensions (q_lum.size, q_pot.size, u.size)

    arr = q_pot*dens_pot*dens_lum*u2*f*np.exp(-a*(x2 + y2*(a + b)/e)) \
        / ((1. - c*u2)*np.sqrt((1. - e2u2_pot)*e))

    G = 0.004301  # (km/s)^2 pc/Msun [6.674e-11 SI units (CODATA2018)]

    return 4*np.pi**1.5*G*arr.sum((0, 1))

##############################################################################

def surf_v2los(x1, y1, inc,
               dens_lum, sigma_lum, qintr_lum,
               dens_pot, sigma_pot, qintr_pot,
               beta, tensor):
    """
    This routine gives the projected weighted second moment Sigma*<V^2_los>

    """
    sb_mu2 = np.empty_like(x1)
    for j, (xj, yj) in enumerate(zip(x1, y1)):
        sb_mu2[j] = quad1d(integrand, [0., 1.], epsabs=0,
                            args=(dens_lum, sigma_lum, qintr_lum,
                                  dens_pot, sigma_pot, qintr_pot,
                                  xj, yj, inc, beta, tensor)).integ

    return sb_mu2

##############################################################################

def vrms2(x, y, inc_deg,
           surf_lum, sigma_lum, qobs_lum,
           surf_pot, sigma_pot, qobs_pot,
           beta, tensor, sigmaPsf, normPsf,
           pixSize, pixAng, step, nrad, nang):
    """
    This routine gives the second V moment after convolution with a PSF.
    The convolution is done using interpolation of the model on a
    polar grid, as described in Appendix A of Cappellari (2008).

    """
    # Axisymmetric deprojection of both luminous and total mass.
    # See equation (12)-(14) of Cappellari (2008)
    #
    inc = np.radians(inc_deg)

    qintr_lum = qobs_lum**2 - np.cos(inc)**2
    if np.any(qintr_lum <= 0):
        raise RuntimeError('Inclination too low q <= 0')
    qintr_lum = np.sqrt(qintr_lum)/np.sin(inc)
    if np.any(qintr_lum < 0.05):
        raise RuntimeError('q < 0.05 components')
    dens_lum = surf_lum*qobs_lum / (sigma_lum*qintr_lum*np.sqrt(2*np.pi))

    qintr_pot = qobs_pot**2 - np.cos(inc)**2
    if np.any(qintr_pot <= 0):
        raise RuntimeError('Inclination too low q <= 0')
    qintr_pot = np.sqrt(qintr_pot)/np.sin(inc)
    if np.any(qintr_pot < 0.05):
        raise RuntimeError('q < 0.05 components')
    dens_pot = surf_pot*qobs_pot / (sigma_pot*qintr_pot*np.sqrt(2*np.pi))

    # Define parameters of polar grid for interpolation
    #
    w = sigma_lum < np.max(np.abs(x)) # Characteristic MGE axial ratio in observed range

    if w.sum() < 3:
        qmed = np.median(qobs_lum)
    else:
        qmed = np.median(qobs_lum[w])

    rell = np.sqrt(x**2 + (y/qmed)**2)  # Elliptical radius of input (x, y)

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
            step = max(np.sqrt(2), np.min(rell))  # Minimum radius of 1pc
            mx = 0

        # Make linear grid in log of elliptical radius RAD and eccentric anomaly ANG
        # See Appendix A
        rmax = np.max(rell) + mx  # Major axis of ellipse containing all data + convolution
        logRad = np.linspace(np.log(step/np.sqrt(2)), np.log(rmax), nrad)  # Linear grid in np.log(rell)
        ang = np.linspace(0, np.pi/2, nang)  # Linear grid in eccentric anomaly
        radGrid, angGrid = map(np.ravel, np.meshgrid(np.exp(logRad), ang))
        xPol = radGrid*np.cos(angGrid)
        yPol = radGrid*np.sin(angGrid) * qmed

    # The model Vrms computation is only performed on the polar grid
    # which is then used to interpolate the values at any other location
    wm2Pol = surf_v2los(xPol, yPol, inc,
                        dens_lum, sigma_lum, qintr_lum,
                        dens_pot, sigma_pot, qintr_pot,
                        beta, tensor)

    if psfConvolution:  # PSF convolution

        nx = int(np.ceil(rmax/step))
        ny = int(np.ceil(rmax*qmed/step))
        x1 = np.linspace(0.5 - nx, nx - 0.5, 2*nx)*step
        y1 = np.linspace(0.5 - ny, ny - 0.5, 2*ny)*step
        xCar, yCar = np.meshgrid(x1, y1)  # Cartesian grid for convolution

        # Interpolate MGE model and Vrms over cartesian grid
        r1 = 0.5*np.log(xCar**2 + (yCar/qmed)**2) # Log elliptical radius of cartesian grid
        e1 = np.arctan2(np.abs(yCar/qmed), np.abs(xCar))    # Eccentric anomaly of cartesian grid

        # Division by mgePol before interpolation reduces interpolation error
        mgeCar = mge_surf(xCar, yCar, surf_lum, sigma_lum, qobs_lum)
        mgePol = mge_surf(xPol, yPol, surf_lum, sigma_lum, qobs_lum)
        wm2Car = mgeCar*bilinear_interpolate(logRad, ang, (wm2Pol/mgePol).reshape(nang, nrad), r1, e1)

        if tensor in ('xy', 'xz'):
            wm2Car *= np.sign(xCar*yCar)  # Calculation was done in positive quadrant

        nk = int(np.ceil(mx/step))
        kgrid = np.linspace(-nk, nk, 2*nk + 1)*step
        xgrid, ygrid = np.meshgrid(kgrid, kgrid)  # Kernel is square
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
        muCar = signal.fftconvolve(wm2Car, kernel, mode='same') \
              / signal.fftconvolve(mgeCar, kernel, mode='same')

        # Interpolate convolved image at observed apertures.
        # Aperture integration was already included in the kernel.
        #
        mu = bilinear_interpolate(x1, y1, muCar, x, y)

    else:  # No PSF convolution

        muPol = wm2Pol/mge_surf(xPol, yPol, surf_lum, sigma_lum, qobs_lum)

        if nrad*nang > x.size:      # Just returns values
            mu = muPol
        else:                      # Interpolate values
            r1 = 0.5*np.log(x**2 + (y/qmed)**2) # Log elliptical radius of input (x,y)
            e1 = np.arctan2(np.abs(y/qmed), np.abs(x))    # Eccentric anomaly of input (x,y)
            mu = bilinear_interpolate(logRad, ang, muPol.reshape(nang, nrad), r1, e1)

            if tensor in ('xy', 'xz'):
                mu *= np.sign(x*y)  # Calculation was done in positive quadrant

    return mu, psfConvolution

##############################################################################

def jam_axi_rms(surf_lum, sigma_lum, qobs_lum, surf_pot, sigma_pot, qobs_pot,
                inc, mbh, distance, xbin, ybin, beta=None, erms=None,
                flux_obs=None, goodbins=None, ml=None, nang=10, normpsf=1.,
                nrad=20, pixang=0., pixsize=0., plot=True, quiet=False,
                rbh=0.01, rms=None, sigmapsf=0., step=0., tensor='zz',
                vmax=None, vmin=None, **kwargs):

    """

    Purpose of jam_axi_rms
    ----------------------

    This procedure calculates a prediction for the projected second
    velocity moment ``V_RMS = sqrt(V**2 + sigma**2)``, or optionally any
    of the six components of the symmetric proper motion dispersion
    tensor, for an anisotropic (three integrals) axisymmetric galaxy model.
    It implements the solution of the anisotropic Jeans equations presented
    in equation (28) and note 5 of `Cappellari (2008).
    <https://ui.adsabs.harvard.edu/abs/2008MNRAS.390...71C>`_
    PSF convolution in done as described in the Appendix of that paper.
    See `Cappellari (2012; C12) <http://arxiv.org/abs/1211.7009>`_
    for explicit formulas for the full proper motion tensor.

    Calling Sequence
    ----------------

    .. code-block:: python

        rmsModel, ml, chi2, flux = jam_axi_rms(
                surf_lum, sigma_lum, qobs_lum, surf_pot, sigma_pot, qobs_pot,
                inc, mbh, distance, xbin, ybin, beta=None, erms=None,
                flux_obs=None, goodbins=None, ml=None, nang=10, normpsf=1.,
                nrad=20, pixang=0., pixsize=0., plot=True, quiet=False,
                rbh=0.01, rms=None, sigmapsf=0., step=0., tensor='zz',
                vmax=None, vmin=None)

    Input Parameters
    ----------------

    SURF_LUM:
        vector of length ``N`` containing the peak surface brightness of the
        MGE Gaussians describing the galaxy surface brightness in units of
        ``Lsun/pc**2`` (solar luminosities per parsec**2).
    SIGMA_LUM:
        vector of length ``N`` containing the dispersion in arcseconds of
        the MGE Gaussians describing the galaxy surface brightness.
    QOBS_LUM:
        vector of length ``N`` containing the observed axial ratio of the MGE
        Gaussians describing the galaxy surface brightness.
    SURF_POT:
        vector of length ``M`` containing the peak value of the MGE Gaussians
        describing the galaxy surface density in units of ``Msun/pc**2`` (solar
        masses per parsec**2). This is the MGE model from which the model
        potential is computed.

        In a common usage scenario, with a self-consistent model, one has
        the same Gaussians for both the surface brightness and the potential.
        This implies ``SURF_POT = SURF_LUM``, ``SIGMA_POT = SIGMA_LUM`` and
        ``QOBS_POT = QOBS_LUM``. The global M/L of the model is fitted by the
        routine when passing the ``RMS`` and ``ERMS`` keywords with the observed
        kinematics.
    SIGMA_POT:
        vector of length ``M`` containing the dispersion in arcseconds of
        the MGE Gaussians describing the galaxy surface density.
    QOBS_POT:
        vector of length ``M`` containing the observed axial ratio of the MGE
        Gaussians describing the galaxy surface density.
    INC:
        inclination in degrees (90 being edge-on).
    MBH:
        Mass of a nuclear supermassive black hole in solar masses.

        VERY IMPORTANT: The model predictions are computed assuming SURF_POT
        gives the total mass. In the common self-consistent case one has
        ``SURF_POT = SURF_LUM`` and if requested (keyword ML) the program can
        scale the output ``RMSMODEL`` to best fit the data. The scaling is
        equivalent to multiplying *both* SURF_POT and MBH by a factor M/L.
        To avoid mistakes, the actual MBH used by the output model is printed
        on the screen.
    DISTANCE:
        distance of the galaxy in Mpc.
    XBIN:
        Vector of length ``P`` with the X coordinates in arcseconds of the bins
        (or pixels) at which one wants to compute the model predictions. The
        X-axis is assumed to coincide with the galaxy projected major axis. The
        galaxy center is at (0,0).

        When no PSF/pixel convolution is performed (``SIGMAPSF=0`` or
        ``PIXSIZE=0``) there is a singularity at (0,0) which should be avoided
        by the input coordinates.
    YBIN:
        Vector of length ``P`` with the Y coordinates in arcseconds of the bins
        (or pixels) at which one wants to compute the model predictions. The
        Y-axis is assumed to coincide with the projected galaxy symmetry axis.

    Optional Keywords
    -----------------

    BETA:
        Vector of length ``N`` with the anisotropy
        ``beta_z = 1 - (sigma_z/sigma_R)**2`` of the individual MGE Gaussians.
    ERMS:
        Vector of length ``P`` with the 1sigma errors associated to the ``RMS``
        measurements. From the error propagation::

            ERMS = sqrt((dVel*velBin)^2 + (dSig*sigBin)^2)/RMS,

        where ``velBin`` and ``sigBin`` are the velocity and dispersion in each
        bin and ``dVel`` and ``dSig`` are the corresponding errors.
        (Default: constant errors ``ERMS=0.05*np.median(RMS)``)
    FLUX_OBS:
        Optional mean surface brightness of each bin for plotting.
    GOODBINS:
        Boolean vector of length ``P`` with values True for the bins which
        have to be included in the fit (if requested) and ``chi**2`` calculation.
        (Default: fit all bins).
    ML:
        Mass-to-light ratio to multiply the values given by SURF_POT.
        Setting this keyword is completely equivalent to multiplying the
        output ``RMSMODEL`` by ``np.sqrt(M/L)`` after the fit. This implies that
        the BH mass becomes ``MBH*(M/L)``.

        If this keyword is not set, or set to a negative number in input, the M/L
        is fitted from the data and the best-fitting M/L is returned in output.
        The BH mass of the best-fitting model is ``MBH*(M/L)``.
    NORMPSF:
        Vector of length ``Q`` with the fraction of the total PSF flux
        contained in the circular Gaussians describing the PSF of the
        observations. It has to be ``np.sum(NORMPSF) = 1``. The PSF will be used
        for seeing convolution of the model kinematics.
    NANG:
        Same as for ``NRAD``, but for the number of angular intervals
        (default: ``NANG=10``).
    NRAD:
        Number of logarithmically spaced radial positions for which the
        models is evaluated before interpolation and PSF convolution. One may
        want to increase this value if the model has to be evaluated over many
        orders of magnitutes in radius (default: ``NRAD=20``). The computation
        time scales as ``NRAD*NANG``.
    PIXANG:
        angle between the observed spaxels and the galaxy major axis X.
    PIXSIZE:
        Size in arcseconds of the (square) spatial elements at which the
        kinematics is obtained. This may correspond to the side of the spaxel
        or lenslets of an integral-field spectrograph. This size is used to
        compute the kernel for the seeing and aperture convolution.

        If this is not set, or ``PIXSIZE=0``, then convolution is not performed.
    PLOT:
        Set this keyword to produce a plot at the end of the calculation.
    QUIET:
        Set this keyword to avoid printing values on the screen.
    RBH:
        This scalar gives the sigma in arcsec of the Gaussian representing the
        central black hole of mass MBH (See Section 3.1.2 of `Cappellari 2008.
        <http://adsabs.harvard.edu/abs/2008MNRAS.390...71C>`_)
        The gravitational potential is indistinguishable from a point source
        for ``radii > 2*RBH``, so the default ``RBH=0.01`` arcsec is appropriate
        in most current situations.

        ``RBH`` should not be decreased unless actually needed!
    RMS:
        Vector of length ``P`` with the input observed velocity second moment::

            V_RMS = sqrt(velBin**2 + sigBin**2)

        at the coordinates positions given by the vectors ``XBIN`` and ``YBIN``.

        If ``RMS`` is set and ``ML`` is negative or not set, then the model is
        fitted to the data, otherwise the adopted ML is used and just the
        ``chi**2`` is returned.
    SIGMAPSF:
        Vector of length ``Q`` with the dispersion in arcseconds of the
        circular Gaussians describing the PSF of the observations.

        If this is not set, or ``SIGMAPSF=0``, then convolution is not performed.

        IMPORTANT: PSF convolution is done by creating a 2D image, with pixels
        size given by ``STEP=MAX(SIGMAPSF, PIXSIZE/2)/4``, and convolving it
        with the PSF + aperture. If the input radii RAD are very large with
        respect to STEP, the 2D image may require a too large amount of memory.
        If this is the case one may compute the model predictions at small radii
        separately from those at large radii, where PSF convolution is not
        needed.
    STEP:
        Spatial step for the model calculation and PSF convolution in arcsec.
        This value is automatically computed by default as
        ``STEP=MAX(SIGMAPSF,PIXSIZE/2)/4``. It is assumed that when ``PIXSIZE``
        or ``SIGMAPSF`` are big, high resolution calculations are not needed. In
        some cases however, e.g. to accurately estimate the central Vrms in a
        very cuspy galaxy inside a large aperture, one may want to override the
        default value to force smaller spatial pixels using this keyword.
    TENSOR:
        String specifying the component of the velocity dispersion tensor.

        ``TENSOR='xx'`` gives sigma_xx=sqrt<V_x'^2> of the component of the
        proper motion dispersion tensor in the direction parallel to the
        projected major axis.

        ``TENSOR='yy'`` gives sigma_yy=sqrt<V_y'^2> of the component of the
        proper motion dispersion tensor in the direction parallel to the
        projected symmetry axis.

        ``TENSOR='zz'`` (default) gives the usual line-of-sight V_rms=sqrt<V_z'^2>.

        ``TENSOR='xy'`` gives the mixed component <V_x'V_y'> of the proper
        motion dispersion tensor.

        ``TENSOR='xz'`` gives the mixed component <V_x'V_z'> of the proper
        motion dispersion tensor.

        ``TENSOR='yz'`` gives the mixed component <V_y'V_z'> of the proper
        motion dispersion tensor.
    VMAX:
        Maximum value of the ``Vrms`` to plot.
    VMIN:
        Minimum value of the ``Vrms`` to plot.

    Output Parameters
    -----------------

    RMSMODEL:
        Vector of length P with the model predictions for the velocity
        second moments for each bin::

            V_RMS = sqrt(vel**2 + sig**2)

        Any of the six components of the symmetric proper motion dispersion
        tensor can be provided in output using the ``TENSOR`` keyword.
    ML:
        Best fitting M/L.
    CHI2:
        Reduced ``chi**2`` describing the quality of the fit::

            chi2 = (((rms[goodBins] - rmsModel[goodBins])/erms[goodBins])**2).sum()
                 / goodBins.sum()

    FLUX:
        Vector of length ``P`` with the PSF-convolved MGE surface brightness of
        each bin in ``Lsun/pc**2``, used to plot the isophotes on the model results.

    """
    if beta is None:
        beta = np.zeros_like(surf_lum)  # Anisotropy parameter beta = 1 - (sig_z/sig_R)**2
    assert surf_lum.size == sigma_lum.size == qobs_lum.size == beta.size, "The luminous MGE components do not match"
    assert surf_pot.size == sigma_pot.size == qobs_pot.size, "The total mass MGE components do not match"
    assert xbin.size == ybin.size, "xbin and ybin do not match"
    if rms is not None:
        if erms is None:
            erms = np.full_like(rms, np.median(rms)*0.05)  # Constant ~5% errors
        if goodbins is None:
            goodbins = np.ones_like(rms, dtype=bool)
        else:
            assert goodbins.dtype == bool, "goodbins must be a boolean vector"
            assert np.any(goodbins), "goodbins must contain some True values"
        assert xbin.size == rms.size == erms.size == goodbins.size, "(rms, erms, goodbins) and (xbin, ybin) do not match"
    assert tensor in ['xx', 'yy', 'zz', 'xy', 'xz', 'yz'], \
        "`tensor` must be one of 'xx', 'yy', 'zz', 'xy', 'xz', 'yz'"

    sigmapsf = np.atleast_1d(sigmapsf)
    normpsf = np.atleast_1d(normpsf)
    assert sigmapsf.size == normpsf.size, "sigmaPSF and normPSF do not match"
    assert round(np.sum(normpsf), 2) == 1, "PSF not normalized"

    pc = distance*np.pi/0.648 # Constant factor to convert arcsec --> pc (with distance in Mpc)

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
    rmsModel, psfConvolution = vrms2(
        xbin_pc, ybin_pc, inc, surf_lum_pc, sigma_lum_pc, qobs_lum,
        surf_pot_pc, sigma_pot_pc, qobs_pot, beta, tensor,
        sigmaPsf_pc, normpsf, pixSize_pc, pixang, step_pc, nrad, nang)

    if not quiet:
        print('jam_axi_rms elapsed time sec: %.2f' % (clock() - t))
        if not psfConvolution:
            txt = "No PSF convolution:"
            if np.max(sigmapsf) == 0:
                txt += " sigmapsf == 0;"
            if pixsize == 0:
                txt += " pixsize == 0;"
            print(txt)

    if tensor in ('xx', 'yy', 'zz'):
        rmsModel = np.sqrt(rmsModel.clip(0))  # Return SQRT and fix possible rounding errors

    # Analytic convolution of the MGE model with an MGE circular PSF
    # using Equations (4,5) of Cappellari (2002, MNRAS, 333, 400).
    # Broadcast triple loop over (n_MGE, n_PSF, n_bins)
    #
    sigmaX2 = sigma_lum**2 + sigmapsf[:, None]**2
    sigmaY2 = (sigma_lum*qobs_lum)**2 + sigmapsf[:, None]**2
    surf_conv = surf_lum_pc*qobs_lum*sigma_lum**2*normpsf[:, None]/np.sqrt(sigmaX2*sigmaY2)
    flux = surf_conv[..., None]*np.exp(-0.5*(xbin**2/sigmaX2[..., None] + ybin**2/sigmaY2[..., None]))
    flux = flux.sum((0, 1))  # PSF-convolved Lsun/pc**2

    if rms is None:

        chi2 = None
        if ml is None:
            ml = 1.
        else:
            rmsModel *= np.sqrt(ml)

    else:

        d, m = (rms/erms)[goodbins], (rmsModel/erms)[goodbins]
        if (ml is None) or (ml <= 0):
            ml = ((d @ m)/(m @ m))**2   # (C08 equation 51)
        rmsModel *= np.sqrt(ml)
        chi2 = ((d - m*np.sqrt(ml))**2).sum() / goodbins.sum()

        if not quiet:
            print(f'inc={inc:.1f} beta_z={beta[0]:.2f} M/L={ml:#.3g} BH={mbh*ml:.2e} chi2/DOF={chi2:#.3g}')
            mass = 2*np.pi*surf_pot_pc*qobs_pot*sigma_pot_pc**2
            print(f'Total mass MGE: {np.sum(mass*ml):#.4g}')

        if plot:

            if flux_obs is None:
                flux_obs = flux

            rms1 = rms.copy() # Only symmetrize good bins
            rms1[goodbins] = symmetrize_velfield(xbin[goodbins], ybin[goodbins], rms[goodbins])

            if (vmin is None) or (vmax is None):
                vmin, vmax = np.percentile(rms1[goodbins], [0.5, 99.5])

            plt.clf()
            plt.subplot(121)
            plot_velfield(xbin, ybin, rms1, vmin=vmin, vmax=vmax, flux=flux_obs, **kwargs)
            plt.title(r"Input $V_{\rm rms}$")

            plt.subplot(122)
            plot_velfield(xbin, ybin, rmsModel, vmin=vmin, vmax=vmax, flux=flux, **kwargs)
            plt.plot(xbin[~goodbins], ybin[~goodbins], 'ok', mec='white')
            plt.title(r"Model $V_{\rm rms}$")
            plt.tick_params(labelleft=False)
            plt.subplots_adjust(wspace=0.03)

    return rmsModel, ml, chi2, flux

##############################################################################
