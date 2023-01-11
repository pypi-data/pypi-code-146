"""
#############################################################################

Copyright (C) 2010-2018, Michele Cappellari
E-mail: cappellari_at_astro.ox.ac.uk

Updated versions of the software are available from my web page
http://purl.org/cappellari/software

If you have found this software useful for your research,
I would appreciate an acknowledgement to the use of the
"JAM modelling package of Cappellari (2008)"
or an explicit reference to the equation given below.

This software is provided as is without any warranty whatsoever.
Permission to use, for non-commercial purposes is granted.
Permission to modify for personal or internal use is granted,
provided this copyright and disclaimer are included unchanged
at the beginning of the file. All other rights are reserved.
In particular, redistribution of the code is not allowed.

#############################################################################

MODIFICATION HISTORY:
    V1.0.0: Written and tested. Michele Cappellari, Oxford, 24 April 2010
    V1.0.1: Use major axis fluxes as reference for isophotes.
        MC, Oxford, 27 July 2011
    V2.0.0: Translated from IDL into Python. MC, Oxford, 21 February 2014
    V2.1.0: Major speedup using histogram. Updated documentation.
        MC, Oxford, 11 March 2016
    V2.2.0: Scale image based on circularized reff.
      - Interpolate reff_maj for increased accuracy.
      - Removed now-unnecessary `npix` keyword.
        MC, Oxford, 22 March 2017
    V2.2.1: Broadcast image creation. MC, Oxford, 22 January 2018

"""

import numpy as np

##############################################################################

def mge_half_light_radius(surf, sigma, q_obs, distance=1e-5):
    """
    Computes the circularized projected half-light radius of an
    MGE model using the approach described after equation (11)
    in Cappellari et al. (2013, MNRAS, 432, 1709)
    https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C

    """
    assert surf.size == sigma.size == q_obs.size, "The MGE components do not match"

    pc = distance*np.pi/0.648         # Constant factor to convert arcsec --> pc
    sigma = sigma*np.sqrt(q_obs)      # Circularize while conserving luminosity
    lum = 2*np.pi*surf*(sigma*pc)**2  # Keep peak surface brightness of each Gaussian
    lum_tot = np.sum(lum)             # If distance is given, lum_tot is in Lsun

    nrad = 50
    rad = np.geomspace(np.min(sigma), np.max(sigma),  nrad)  # arcsec
    lum_r = (lum*(1 - np.exp(-0.5*(rad[:, None]/sigma)**2))).sum(1)
    reff = np.interp(lum_tot/2, lum_r, rad)

    return reff, lum_tot

##############################################################################

def mge_half_light_isophote(surf, sigma, q_obs, distance=1e-5):
    """
    PURPOSE
    -------

        Computes the half-light radius, the  major axis and ellipticity of
        the MGE isophote containing 1/2 of the analytic MGE total light.

        This procedure implements the steps (i)-(iv) described above
        equation (12) in `Cappellari et al. (2013, MNRAS, 432, 1709)
        <https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C>`_

    CALLING SEQUENCE
    ----------------

    .. code-block:: python

        from jampy.mge_half_light_isophote import mge_half_light_isophote

        reff, reff_maj, eps_e, lum_tot = mge_half_light_isophote(
                surf, sigma, q_obs, distance=distance)

    INPUT PARAMETERS
    ----------------

    surf:
        Peak surface brightness of each Gaussian in Lsun/pc**2
    sigma:
        Gaussian dispersion in arcsec
    q_obs: 
        Observed axial ratio of each Gaussian

    OPTIONAL KEYWORD
    ----------------

    distance:
        Galaxy distance in Mpc. This is only required to obtain
        the total luminosity of the MGE model in proper units.

        If the distance is not given, 10pc is assumed. In this case the
        following expression gives the galaxy apparent total magnitude:
        ``mag = sunMag - 2.5*alog10(lum_tot)``

    OUTPUTS
    -------

    reff:
        Effective (projected half-light) radius Re. This is the
        "circularized" Re=sqrt(Area/pi), where the area is the one
        of the isophote containing 1/2 of the analytic total MGE light.
        This is in the same units as SIGMA (typically arcsec).
    reff_maj:
        Major axis (largest size) of the isophote containing
        1/2 of the total MGE light.
    eps_e:
        Ellipticity of the isophote containing 1/2 of the total MGE
        light, computed from the inertia tensor within the isophote.
    lum_tot:
        Analytic total luminosity in solar luminosities if the
        optional distance in Mpc is provided.

    """
    assert surf.size == sigma.size == q_obs.size, "The MGE components do not match"

    # Scale image based on the circularized Reff and an extreme axial ratio
    reff1, lum_tot = mge_half_light_radius(surf, sigma, q_obs, distance=distance)
    rmax = reff1/np.sqrt(np.min(q_obs).clip(0.1))

    # Create image from MGE model. Only compute one quadrant for symmetry
    npix = 100                   # This gives better than 0.1% accuracy
    scale = rmax/(npix - 0.5)    # image scale in arcsec/pix
    x = np.linspace(scale/2, rmax, npix)  # open interval for bi-symmetry
    xx2, yy2 = np.meshgrid(x**2, x**2)
    image = surf*np.exp(-0.5/sigma**2*(xx2[..., None] + yy2[..., None]/q_obs**2))
    image = image.sum(2)

    # Find enclosed light inside isophotes defined by the MGE flux for the
    # pixels on the major axis, then interpolate to find half-light isophote
    h = np.histogram(image, bins=image[0, ::-1], weights=image)[0]
    lum_r = np.cumsum(h[::-1])
    pc = distance*np.pi/0.648  # Constant factor to convert arcsec --> pc
    surf_e = np.interp(lum_tot/8/(pc*scale)**2, lum_r, image[0, 1:])

    mask = image >= surf_e                  # Pixels inside half-light isophote
    reff = np.sqrt(4*mask.sum()/np.pi)*scale    # Radius of same-area circle
    reff_maj = np.interp(surf_e, image[0, ::-1], x[::-1])

    # Compute coefficients of the diagonal moment of inertia tensor
    # using equation (12) of Cappellari et al. (2013, MNRAS, 432, 1709)
    x2 = image[mask] @ xx2[mask]
    y2 = image[mask] @ yy2[mask]
    eps_e = 1 - np.sqrt(y2/x2)

    return reff, reff_maj, eps_e, lum_tot

##############################################################################
