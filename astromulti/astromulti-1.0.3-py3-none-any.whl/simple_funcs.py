import numpy as np
from astropy import units as u
from copy import deepcopy as dcp

def FWHM_to_SD(quantity):
    # convert Gaussian FWHM to standard deviation
    return quantity/2/np.sqrt(2*np.log(2))

def dimless(quantity):
    # a function to convert the input dimensionless quantity to as such by stripping its useless units
    return quantity.to(u.dimensionless_unscaled).value

def s_clip( data, niter=20, nsigma=3 ):
    # perform sigma-clipping to estimate mean and STD
    ndata = dcp(data)
    for i in range(niter+1):
        mean = np.nanmean(ndata)
        std  = np.nanstd(ndata)
        lim1 = mean - (nsigma*std)
        lim2 = mean + (nsigma*std)
        ndata[ (ndata>lim2) + (ndata<lim1) ] = np.nan
    return [mean, std]

def ask_user():
    # just ask user whether to continue or not
    userinput = input('~~ Continue? [y/n]: ')
    if userinput=='n':
        raise RuntimeError('User made a stop')

def mymontage(funcname,**kwargs):
    # a simple wrapper for montage to raise errors properly
    mont = funcname(**kwargs)
    #print(mont)
    if mont['status']!='0':
        raise RuntimeError(mont['msg'])

def angle_ICRS2GAL( GLong,GLat ):
    """
    Calculates the angle offset between ICRS and GAL
    To be used in the following way:
      You have an angle "A" degrees in ICRS
      Its value in GAL is = A + angle_ICRS2GAL( l,b )
    """
    from astropy.coordinates import SkyCoord
    a  = 0.005   # some small angle in degrees
    c0 = SkyCoord(GLong, GLat, unit='deg', frame='galactic')
    c1 = SkyCoord(GLong, GLat+a, unit='deg', frame='galactic')
    return c0.icrs.position_angle(c1).deg
