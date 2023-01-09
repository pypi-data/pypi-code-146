import sys, subprocess, numpy as np
from copy import deepcopy as dcp
import itertools as itrt

from astropy import units as u
from astropy.io import fits
from astropy.wcs import WCS
from astropy.nddata import Cutout2D
from astropy.modeling import models, fitting
from astropy.convolution import convolve, convolve_fft, Gaussian2DKernel
from astropy.coordinates import SkyCoord
from regions import CircleSkyRegion

from .region_meta import get_extent, get_center, rot_PolySkyReg
from .simple_funcs import s_clip, ask_user, FWHM_to_SD, dimless
from .linear_fitting import plane_fit


def remove_axes_34(infits,outfits):
    # remove degenerate axes if present
    data, hdr = fits.getdata(infits,0,header=True)
    hdr['NAXIS'] = 2
    for cardname in ['NAXIS3','CRVAL3','CTYPE3','CDELT3','CRPIX3','CROTA3','NAXIS4','CRVAL4','CTYPE4','CDELT4','CRPIX4','CROTA4']:
        try:
            del hdr[cardname]
            print("Deleted card: "+cardname)
        except:
            pass
    if len(np.shape(data))==2:
        fits.writeto(outfits, data, hdr, overwrite=True)
        print("Output saved to: "+outfits)
    if len(np.shape(data))==3:
        fits.writeto(outfits, data[0], hdr, overwrite=True)
        print("Output saved to: "+outfits)
    if len(np.shape(data))==4:
        fits.writeto(outfits, data[0][0], hdr, overwrite=True)
        print("Output saved to: "+outfits)
    if len(np.shape(data))>=5:
        print("Data has too many axes, check and do this manually.")


def cutout_fits( infits, outfits, skypos, cutsize, overwr=True ):
    '''
    Make a 2D cutout of a fits file
    '''
    indata,hdr = fits.getdata(infits,header=True)
    fitswcs = WCS(hdr)
    cutout  = Cutout2D( indata, skypos, cutsize, fitswcs )
    newhdr  = cutout.wcs.to_header()
    for key in hdr.keys():          # copy keys and values from old header to new header
        try:                        # only if it doesn't already exist
            dummy = newhdr[key]
        except:
            if key!='HISTORY' and key!='COMMENT':      # history and comments will be handled later
                newhdr[key] = hdr[key]
            else:
                pass
    if 'HISTORY' in hdr.keys():
        hist_items = str(hdr['HISTORY']).split('\n')
        for item in hist_items:
            newhdr['HISTORY'] = item
    if 'COMMENT' in hdr.keys():
        hist_items = str(hdr['COMMENT']).split('\n')
        for item in hist_items:
            newhdr['COMMENT'] = item
    fits.writeto(outfits,cutout.data,newhdr,overwrite=overwr)


def bgf( fits_input, fits_res, fits_bg, bgftype, beam_l, beam_b, niter, use_fft=True, **kwargs ):
    '''
    Function to do background filtering on images
    fits_input : name of input fits file (assuming BMAJ=BMIN in the header ie circular beam)
    fits_res   : name of output residuals
    fits_bg    : name of output background
    bgftype    : 'I'  (based on Sofue & Reich 1979, for Stokes I images ie only +ve features)
               : 'QU' (based on Kothes & Kerton 2002, for Stokes Q/U images ie both +/- features)
    beam_l     : filtering beam FWHM along axis 1 (should be same units as fits header info)
    beam_b     : filtering beam FWHM along axis 2 (should be same units as fits header info)
    niter      : number of iterations to converge on good bg/res estimates
    use_fft    : use convolve() or convolve_fft()?
    **kwargs   : keyword arguments to be passed to convolve(_fft)
    '''

    # Get original map, check units
    orig, hdr = fits.getdata(fits_input,0,header=True)
    originalhdr = dcp(hdr)
    if hdr['BUNIT'].lower() not in [ 'k', 'mk', 'uk', 'millik tb', 'microk tb', 'milli k', 'micro k' ]:
        print('BUNIT of the fits file is '+hdr['BUNIT']+', which is not recognized.')
        print('It is strongly advised to use Kelvin units for this operation.')
        print("Can convert to K, but the header must contain FREQUE in Hz.")
        uinput = input("Proceed to convert to Kelvin scale? [y/n]: ")
        if uinput=='y':
            change_BUNIT( fits_input, "temp-K.fits", "K" )
            orig, hdr = fits.getdata("temp-K.fits",0,header=True)
        else:
            print("OK, not converting, remember that results may not make sense.")

    # header info fixes
    try:
        dummy = hdr['CDELT1']
    except:
        hdr['CDELT1'] = hdr['CD1_1']
        hdr['CDELT2'] = hdr['CD2_2']

    # convert smoothing beams to pixels, define smoothing kernel
    fin_beams  = np.abs(np.array( [beam_l/hdr['CDELT1'],beam_b/hdr['CDELT2']] ))
    smo_beams  = FWHM_to_SD(np.sqrt( fin_beams**2 - hdr['BMAJ']**2 ))
    gauss_kern = Gaussian2DKernel(smo_beams[0],smo_beams[1])

    # which convolution function to use
    if use_fft==True:
        convolvefunc = convolve_fft
    if use_fft==False:
        convolvefunc = convolve

    # ensure that only the coordinate axes data are used if NAXIS>2; copy to new array
    if len(orig.shape)>2:
        print("Removing unnecessary axes...")
    while len(orig.shape)>2:
        orig = orig[0]
    sm_features = dcp(orig)                                                     # copy of original image which will be modified in the next steps

    # bgf iterations: after these iterations 'sm_features' has the best possible residuals
    for idx in np.arange(niter):
        sys.stdout.write("\r Iteration: %d / %d ..." %(idx+1,niter))
        sys.stdout.flush()
        initbg = convolvefunc( sm_features, gauss_kern,
                               preserve_nan=True, **kwargs )                    # first background estimate
        diffim = orig - initbg                                                  # difference image (=residuals)
        if bgftype=='QU': signim = diffim * orig                                # for Stokes Q/U: sign map is orig*diffim; it has compact emissions > 0 and extended < 0
        if bgftype=='I':  signim = diffim                                       # for Stokes I: sign map is same as diffim; it has compact emissions > 0 and extended < 0
        sm_features[np.where(signim>0)] = initbg[np.where(signim>0)]            # compact emissions are replaced by first background
        newbg = convolvefunc( sm_features, gauss_kern,
                              preserve_nan=True, **kwargs )                     # new background
        sm_features = orig - newbg                                              # new residuals: from this we remove background again
    finalbg = orig - sm_features                                                # final background
    print()

    # write outputs
    if fits_res:
        print("Writing out the filtered data fits file: "+fits_res)
        hdr['HISTORY'] = "RD: "+str(niter)+" iterations of bgf-type "+bgftype+" with"
        hdr['HISTORY'] = "beam_l="+str(beam_l)+', beam_b='+str(beam_b)
        fits.writeto( fits_res, sm_features, hdr, overwrite=True )
        if originalhdr['BUNIT'].lower() not in [ 'k', 'mk', 'uk', 'millik tb', 'microk tb', 'milli k', 'micro k' ]:
            if uinput=='y':     # to change back to original units!
                change_BUNIT( fits_res, fits_res, "Jy/beam" )
    if fits_bg:
        print("Writing out the background data fits file: "+fits_bg)
        hdr['HISTORY'] = "RD: "+str(niter)+" iterations of bgf-type "+bgftype+" with"
        hdr['HISTORY'] = "beam_l="+str(beam_l)+', beam_b='+str(beam_b)
        fits.writeto( fits_bg, finalbg, hdr, overwrite=True )
        if originalhdr['BUNIT'].lower() not in [ 'k', 'mk', 'uk', 'millik tb', 'microk tb', 'milli k', 'micro k' ]:
            if uinput=='y':     # to change back to original units!
                change_BUNIT( fits_bg, fits_bg, "Jy/beam" )

    return None


def change_BUNIT( infits, outfits, targetunit, TbyS=None, freq=None, beamsz=None, overwr=True ):
    '''
    Given a fits file, its data are converted to the targetunit: only K or Jy/beam.
    - TbyS (T/S) must be in K/Jy.  If this is given, only this will be used!
    - freq must be in Hz and beamsz in degrees.
    - If they are not given, their values will be taken from the header (FREQUE and BMAJ)
    !!.. Assuming that BMAJ=BMIN ..!!
    this code is not very robust, but works.
    '''

    indata, hdr = fits.getdata(infits,0,header=True)
    imageunit   = hdr['BUNIT'].lower()
    targetunit  = targetunit.lower()

    if imageunit==targetunit:
        print("Input is already in target units, so, directly writing to output.")
        fits.writeto( outfits,indata,hdr,overwrite=overwr )
        return

    if 'milli' in imageunit or (imageunit=='m'+targetunit):
        indata = indata/1e3
        newimageunit = imageunit.replace("milli","").replace("m","",1)
    elif 'micro' in imageunit or (imageunit=='u'+targetunit):
        indata = indata/1e6
        newimageunit = imageunit.replace("micro","").replace("u","",1)
    else:
        newimageunit = imageunit
    if newimageunit==targetunit or ("k" in newimageunit and targetunit=="k"):
        print("Only a factor micro/milli different, no T-S conversion needed.")
        hdr['BUNIT'] = targetunit
        fits.writeto( outfits,indata,hdr,overwrite=overwr )
        return

    # calculate T/S if it is not given
    if TbyS is None:
        # get beam size and frequency
        if beamsz is None:
            try:
                beamsz = hdr['BMAJ']
                print("Using beam size info from fits header.")
            except:
                raise RuntimeError('beamsz was not given; input fits also has no BMAJ in it!')
        if freq is None:
            try:
                freq = hdr['FREQUE']
                print("Using frequency info from fits header.")
            except:
                raise RuntimeError('freq was not given; input fits also has no FREQUE in it!')
        TbyS = ((1*u.Jy/(np.pi*(beamsz*u.degree)**2/4/np.log(2))).to(u.K, equivalencies=u.brightness_temperature(freq*u.Hz))).value
        print('Calculated the following conversion factor: '+str(TbyS))

    if (newimageunit=='k' or newimageunit=='k tb') and targetunit=="jy/beam":
        hdr['BUNIT'] = 'Jy/beam'
        fits.writeto( outfits,indata/TbyS,hdr,overwrite=overwr )
        return
    if newimageunit=="jy/beam" and targetunit=='k':
        hdr['BUNIT'] = 'K'
        fits.writeto( outfits,indata*TbyS,hdr,overwrite=overwr )
        return

    # if the code reached here, it means something did not work
    print("The image unit is: "+imageunit)
    print("The given target unit is: "+targetunit)
    print("Target units must be only 'Jy/beam' or 'K'")
    raise RuntimeError("Something wrong with the units.")


def regioncut( fitsfile, ds9reg=None, units=True ):
    '''
    Extracts data from a single fits file and also gives its units.
    The data is returned in the same shape as input, except the coordinate axes of course.
        Along the coordinates, it takes a 2D shape rather than the mask shape.
        Values outside the mask are converted to NaN.
    '''

    # data and details from the fits files
    im_I1, h1 = fits.getdata(fitsfile,0,header=True)
    wcshdr1   = WCS(h1)

    # get axis indices of GLON/RA and GLAT/DEC, and the other axes
    # _4wcs is for popping axes; _4arr is for array operations
    wcs_axis_names = wcshdr1.axis_type_names
    for axisname in wcs_axis_names:
        if 'glon' in axisname.lower() or 'ra' in axisname.lower():
            l_axis_4wcs = [ yy for yy in range(len(wcs_axis_names)) if wcs_axis_names[yy]==axisname ][0]
            l_axis_4arr = len(np.shape(im_I1)) - l_axis_4wcs - 1
        if 'glat' in axisname.lower() or 'dec' in axisname.lower():
            b_axis_4wcs = [ yy for yy in range(len(wcs_axis_names)) if wcs_axis_names[yy]==axisname ][0]
            b_axis_4arr = len(np.shape(im_I1)) - b_axis_4wcs - 1
    o_axes = [ kk for kk in range(len(np.shape(im_I1))) if kk not in [l_axis_4arr,b_axis_4arr] ]

    # if there are planes other than l and b
    if o_axes!=[]:
        # we will build a dictionary of all the planes,
        #   with keys corresponding to indices (no l,b indices of course)
        # example:
        #   [l,b]=[2,3]  &  o_axes=[0,1,4]  &  key=(d,e,f)
        #   =>  we must access image with (d,e,:,:,f)
        dict_full  = {}                                                         # this dictionary will contain the full data (not cropped yet)
        mykeys_arr = [ np.arange(np.shape(im_I1)[oo]) for oo in o_axes ]        # a list of arrays, each array has the index number that will be iterated over
        mykeys_fin = [ aa for aa in itrt.product(*mykeys_arr) ]                 # all the required keys
        for key in mykeys_fin:                                                  # iterating over each key
            arrayslicer = [ slice(None) ] * len(np.shape(im_I1))                # we'll use this to slice the cube (start with :,:,:,... )
            for eachaxis in range(len(np.shape(im_I1))):                        # iterate over each axis
                if eachaxis not in [l_axis_4arr,b_axis_4arr]:                   # if this axis is either l or b, we don't want to change slice(None)
                    keyidx = [ oo for oo in o_axes if oo==eachaxis ][0]         # the index (in o_axes) that corresponds to the current axis
                    arrayslicer[eachaxis] = key[keyidx]                         # finally prepare the slicer
            dict_full[key] = im_I1[tuple(arrayslicer)]                          # slice the cube and save it in dict_full
        # remember that all planes will have the same WCS, same shape
        new_wcs = dcp(wcshdr1)                                                  # make a deepcopy before modifying
        # make a list of unnecessary axes and sort them in reverse (for popping correctly)
        unnec_axes = [ idx for idx in range(wcshdr1.naxis) if idx!=l_axis_4wcs and idx!=b_axis_4wcs ]
        unnec_axes = np.sort(unnec_axes)[::-1]
        for axis2rem in unnec_axes:                                             # drop unnecessary axes
            new_wcs = new_wcs.dropaxis(axis2rem)
        # so we have corrected the WCS by dropping the unnecessary axes.
        # now we will create a new dictionary, this time it will contain cropped data.
        dict_crpd = {}
        msk1 = ds9reg.to_pixel(new_wcs).to_mask()                               # mask for the 2D image plane
        for key in mykeys_fin:                                                  # iterating over each key (just reusing the same old keys)
            croppeddata = msk1.multiply(dict_full[key],fill_value=np.nan)       # values of 'I' pixels inside the bounding box
            dict_crpd[key] = np.array( croppeddata )                            # save in the dictionary as an array
            if (dict_crpd[key]==None).all() == True:                            # raise error if object mask can't be prepared
                print("Something went wrong at this key: "+str(key))
                raise RuntimeError('Mask cannot be prepared!')
                return
        # OK so we have the cutout data in a dictionary with appropriate keys
        # now we should arrange it back in original shape
        fin_shape = np.array(np.shape(im_I1))                                   # first start with original shape
        new_l_idx = int(l_axis_4wcs<b_axis_4wcs)                                # (l,b) = (0,1) or (1,0) ?
        new_b_idx = int(l_axis_4wcs>b_axis_4wcs)
        fin_shape[l_axis_4arr] = np.shape(dict_crpd[key])[new_l_idx]            # put correct value of length along 'l'
        fin_shape[b_axis_4arr] = np.shape(dict_crpd[key])[new_b_idx]            # put correct value of length along 'b'
        finaldata = np.zeros(fin_shape) + np.nan                                # initialize the data array to be returned
        # use arrayslicer part from above
        for key in mykeys_fin:                                                  # iterating over each key
            arrayslicer = [ slice(None) ] * len(np.shape(im_I1))                # we'll use this to slice the cube (start with :,:,:,... )
            for eachaxis in range(len(fin_shape)):                              # iterate over each axis
                if eachaxis not in [l_axis_4arr,b_axis_4arr]:                   # if this axis is either l or b, we don't want to change slice(None)
                    keyidx = [ oo for oo in o_axes if oo==eachaxis ][0]         # the index (in o_axes) that corresponds to the current axis
                    arrayslicer[eachaxis] = key[keyidx]                         # finally prepare the slicer
            finaldata[tuple(arrayslicer)] = dict_crpd[key]                      # save the data from dictionary to the final array
        I_vals1 = finaldata

    # if there are no axes other than l and b
    if o_axes==[]:
        msk1    = ds9reg.to_pixel(wcshdr1).to_mask()                            # mask for actual data
        I_vals1 = np.array( msk1.multiply(im_I1,fill_value=np.nan) )            # values of 'I' pixels inside the bounding box
        if (I_vals1==None).all() == True:                                       # skip if object mask can't be prepared
            raise RuntimeError('Mask cannot be prepared!')
            return

    # return according to units
    if units==True:
        try:
            imageuni1 = h1['BUNIT']
            return I_vals1,imageuni1
        except:
            import warnings
            warnings.warn("header does not contain BUNIT, not returning units!")
            return I_vals1, None
    else:
        return I_vals1


def subtract_bg( infits, outfits, tpds9reg, bgboxsize ):
    '''
    Performs twisted plane background subtraction (1st order correction).
    'tpds9reg' must be a DS9 region with vertices that trace the background.
    A plane is fit to the brightness values of the vertices which is subtracted.
    'bgboxsize' decides the area of the box in which median will be calculated.
    '''

    vertcs_sky = tpds9reg.vertices.galactic

    # data and details from the fits files
    im_I, hdr = fits.getdata(infits,0,header=True)
    wcshdr    = WCS(hdr)

    # for indices of the box in which median is calculated
    lowerlim = -int(bgboxsize/2)
    upperlim = int(bgboxsize/2) + 1

    # get data and do the actual work
    v_arr   = np.array( vertcs_sky.to_pixel(wcshdr) )                           # convert sky coordinates to array coordinates
    pixels  = np.round(np.fliplr( v_arr.T )).astype('int')                      # make pixel array
    zvals   = []
    for indices in pixels:                                                      # get median values around pixel
        medianval = np.median( im_I[ indices[0]-lowerlim : indices[0]+upperlim , indices[1]-lowerlim : indices[1]+upperlim ] )
        zvals.append( [ medianval ] )
    points  = np.hstack((pixels,zvals))                                         # x,y,z points array
    vals,e  = plane_fit(points)                                                 # a,b,c (plane equation: a*x + b*y + c = z )
    x1,y1   = np.ogrid[ :np.shape(im_I)[0], :np.shape(im_I)[1] ]                # mesh grid for vectorizing background image
    bgim    = vals[0]*x1 + vals[1]*y1 + vals[2]                                 # bg image

    # save the bg-subtracted fits image
    fits.writeto(outfits,im_I-bgim,hdr,overwrite=True)

    return


def TTdata( fits1, fits2, s2n=1.0, conv2commbeam=True, ds9reg=None, tpds9reg=None, tpboxsize=None, bgds9reg=None ):
    '''
    Gives out data for making T-T plots (T1 and T2) and also units.
    - fits1 and fits2 must be images at two frequencies with same WCS info.
    - s2n is the signal/noise threshold below which the pixels will be masked.
        Use s2n=None if no masking must be done.
    - If tpds9reg is True, then a 'twisted plane' will be fit to the background.
      The tpds9reg must be a polygon with at least 4 vertices that are
        representative of the surrounding background emission.
      The parameter 'tpboxsize' must be given if bg correction needs to be done.
      This will decide the area of the box in which median will be calculated.
    - Use conv2commbeam=True if they have different beam sizes!
      ( the fits file with higher resolution will be convolved to the
        beam size of the lower resolution file )
      If the beam sizes are already the same, then this parameter does not matter
    '''

    # data and details from the fits files
    im_I1, h1 = fits.getdata(fits1,0,header=True)
    wcshdr1   = WCS(h1)
    imageuni1 = h1['BUNIT']
    im_I2, h2 = fits.getdata(fits2,0,header=True)
    wcshdr2   = WCS(h2)
    imageuni2 = h2['BUNIT']

    # first check for common beam size
    if ~np.isclose(h1['BMAJ'],h2['BMAJ'],rtol=1e-4) or ~np.isclose(h1['BMIN'],h2['BMIN'],rtol=1e-4):
        if conv2commbeam==True:
            smooth_fits_to_commonbeam( fits1,fits2,'lb1.fits','lb2.fits' )
            # get new details from the files convolved to a common beam
            fits1 = 'lb1.fits'
            fits2 = 'lb2.fits'
            im_I1, h1 = fits.getdata(fits1,0,header=True)
            wcshdr1   = WCS(h1)
            imageuni1 = h1['BUNIT']
            im_I2, h2 = fits.getdata(fits2,0,header=True)
            wcshdr2   = WCS(h2)
            imageuni2 = h2['BUNIT']
        else:
            print("Beam sizes are not same and conv2commbeam is set to False.")
            print("Results are (almost definitely) incorrect if you choose to continue!!")

    # if something is wrong, let the user know and stop
    if ~np.isclose(h1['BMAJ'],h2['BMAJ'],rtol=1e-4) or ~np.isclose(h1['BMIN'],h2['BMIN'],rtol=1e-4):
        print( '  file1 beam major axis: ' + str(h1['BMAJ']) )
        print( '  file2 beam major axis: ' + str(h2['BMAJ']) )
        print( '  file1 beam minor axis: ' + str(h1['BMIN']) )
        print( '  file2 beam minor axis: ' + str(h2['BMIN']) )
        ask_user()
    if imageuni1 != imageuni2:
        print( '  Units of image 1: ' + imageuni1 )
        print( '  Units of image 2: ' + imageuni2 )
        ask_user()
    if h1['CTYPE1'] != h2['CTYPE1']  or  h1['CTYPE2'] != h2['CTYPE2']:
        print("Axis types are different.")
        ask_user()
    if len(np.shape(im_I1))>2:
        print("Unnecessary axes present in fits1, will consider only first two axes.")
        print("If twisted plane background subtraction must be done, there may be problems.")
    if len(np.shape(im_I2))>2:
        print("Unnecessary axes present in fits2, will consider only first two axes.")
        print("If twisted plane background subtraction must be done, there may be problems.")

    # twisted plane background subtraction
    if tpds9reg is not None:
        subtract_bg( fits1, "temp-bgsubim1.fits", tpds9reg, tpboxsize )
        subtract_bg( fits2, "temp-bgsubim2.fits", tpds9reg, tpboxsize )
        fits1 = "temp-bgsubim1.fits"
        fits2 = "temp-bgsubim2.fits"

    # make the masks and confirm that the cutout data have the same shape
    I_vals1 = regioncut( fits1, ds9reg, units=False )
    I_vals2 = regioncut( fits2, ds9reg, units=False )
    if np.shape(I_vals1) != np.shape(I_vals2):
        raise RuntimeError('Cutouts have different shapes, you must REGRID!')
        return

    # remove pixels below the threshold
    if s2n is not None:
        if bgds9reg is not None:
            noisereg = bgds9reg
        if bgds9reg is None:
            noisereg = CircleSkyRegion( get_center(ds9reg), radius=get_extent(ds9reg) )
        noisevals1 = regioncut( fits1, noisereg, units=False )
        noisevals2 = regioncut( fits2, noisereg, units=False )
        mn1,std1   = s_clip( np.array( noisevals1 ) )                       # sigmal clipping to get mean and STD
        mn2,std2   = s_clip( np.array( noisevals2 ) )                       # "
        maskval1   = mn1 + s2n*std1                                         # mask based on mean and STD from sigma clipping
        maskval2   = mn2 + s2n*std2                                         # "
        mask0      = (I_vals1>maskval1) * (I_vals2>maskval2)                # use only pixels that are over the threshold in both images
        I_vals1    = I_vals1[mask0]
        I_vals2    = I_vals2[mask0]

    return I_vals1,I_vals2,imageuni2


def measure_FD( fitsfile, ds9reg=None,
                noise='auto', noisereg=None, noiseval=None, s2n=0.0, cal_error=0.1,
                tpds9reg=None, bgboxsize=None, bgregrotate=15*u.degree ):
    '''
    Measures the flux density (Jy) of an extended object.
    BUNIT in the header must be only jy/beam or K or a factor of it.
    If noise=='semi', noise value will be calculated from the values inside 'noisereg'.
    If noise=='auto', noise value will be calculated from the values inside a large surrounding region.
    If noise=='manual', noiseval will be used.
    Values below s2n will be masked.
        where s2n=signal/noise=I/rms
    'cal_error' is the calibration uncertainty
    The uncertainty = sqrt( RMS**2 *npix/BAinPix + (FD*cal_error)**2 + bgsub_unc**2 )
        where bgsub_unc is obtained by varying 'tpds9reg'
        (varying is done by rotating the region by +/- 'bgregrotate')
    If 'tpds9reg' is given, then a 'twisted plane' will be fit to the background.
    'tpds9reg' must be a polygon with at least 4 vertices that are
        representative of the surrounding background emission.
    The parameter 'bgboxsize' must be given if bg correction needs to be done,
        which will decide the area of the box in which median will be calculated.
    '''

    hdr     = fits.getheader(fitsfile)
    wcshdr1 = WCS(hdr)

    # header info fixes
    try:
        _ = hdr['CDELT1']
    except:
        hdr['CDELT1'] = hdr['CD1_1']
        hdr['CDELT2'] = hdr['CD2_2']

    # region for noise estimation
    if noise=='auto':
        noisereg = CircleSkyRegion( get_center(ds9reg), radius=get_extent(ds9reg) )

    # some required info
    BAinSqDeg = np.pi * hdr['BMAJ'] * hdr['BMIN'] / ( 4*np.log(2) )             # beam area; square degree
    pixSize   = np.abs(hdr['CDELT1']) * np.abs(hdr['CDELT2'])                   # pixel size; square degree
    BAinPix   = BAinSqDeg / pixSize                                             # beam area; pixels

    # convert to jy/beam
    hdr = fits.getheader(fitsfile)
    if hdr['BUNIT'].lower()!='jy/beam':
        change_BUNIT(fitsfile,fitsfile[:-5]+"_JyPB.fits","Jy/beam")
        fitsfile = fitsfile[:-5]+"_JyPB.fits"

    # twisted plane background subtraction
    if tpds9reg is not None:
        tpds9reg_r1 = rot_PolySkyReg( tpds9reg, bgregrotate )
        tpds9reg_r2 = rot_PolySkyReg( tpds9reg,-bgregrotate )
        subtract_bg( fitsfile, "temp-bgsubim.fits", tpds9reg, bgboxsize )
        subtract_bg( fitsfile, "temp-bgsubim2.fits", tpds9reg_r1, bgboxsize )
        subtract_bg( fitsfile, "temp-bgsubim3.fits", tpds9reg_r2, bgboxsize )
        fitsfile  = "temp-bgsubim.fits"
        fitsfile2 = "temp-bgsubim2.fits"
        fitsfile3 = "temp-bgsubim3.fits"

    # get the values and units inside the region, and number of pixels (for uncertainty)
    I_vals,img_uni = regioncut( fitsfile, ds9reg, units=True )                  # returns 2D array instead of the masked values
    totalnpixels = 1
    for dim in np.shape(I_vals):
        totalnpixels *= dim
    numNaN = np.sum(np.isnan(I_vals))                                           # since values outside the region mask are NaN's)
    totalnpixels = totalnpixels - numNaN                                        # assuming that the image itself has no NaNs inside the region mask

    # get noise and final values after masking
    if noise=='auto' or noise=='semi':
        noiseregvals = regioncut( fitsfile, noisereg, units=False )
        ns_mn,ns_std = s_clip( np.array( noiseregvals ) )
        if tpds9reg is not None:                                                # if bg is being subtracted
            maskval  = ns_std * s2n                                             # mask based on STD from sigma clipping
            noiseval = ns_std
        else:                                                                   # if no bg is subtracted
            ns_rms   = np.sqrt(ns_std**2+ns_mn**2)                              # get RMS
            maskval  = ns_rms * s2n                                             # mask based on RMS
            noiseval = ns_rms
    if noise=='manual':
        maskval = s2n * noiseval
    I_vals = I_vals[I_vals>maskval]

    # if bg-sub was done, get the uncertainty in this operation
    if tpds9reg is not None:
        # first bg-subbed image
        I_vals2 = regioncut( fitsfile2, ds9reg, units=False )
        if noise=='auto' or noise=='semi':
            noiseregvals2  = regioncut( fitsfile2, noisereg, units=False )
            ns_mn2,ns_std2 = s_clip( np.array( noiseregvals2 ) )
            maskval2     = ns_std2 * s2n                                        # mask based on STD from sigma clipping
            noiseval2    = ns_std2
        if noise=='manual':
            maskval2 = s2n * noiseval
        I_vals2 = I_vals2[I_vals2>maskval2]
        # second bg-subbed image
        I_vals3 = regioncut( fitsfile3, ds9reg, units=False )
        if noise=='auto' or noise=='semi':
            noiseregvals3  = regioncut( fitsfile3, noisereg, units=False )
            ns_mn3,ns_std3 = s_clip( np.array( noiseregvals3 ) )
            maskval3     = ns_std3 * s2n                                        # mask based on STD from sigma clipping
            noiseval3    = ns_std3
        if noise=='manual':
            maskval3 = s2n * noiseval
        I_vals3 = I_vals3[I_vals3>maskval3]
        # finally get the uncertainty
        bgsub_unc = np.std(np.array([ np.sum(I_vals),np.sum(I_vals2),np.sum(I_vals3) ])) /BAinPix
    else:
        bgsub_unc = 0

    # final conversion before returning the required values
    FD_imguni = np.sum( I_vals )                                                # get FD in image units
    FD   = FD_imguni / BAinPix
    FD_e = np.sqrt( totalnpixels/BAinPix*maskval**2 + (cal_error*FD)**2 + bgsub_unc**2 )

    if FD==0.:
        print("No emission found at this s2n, 1-sigma upper limit is stored in uncertainty!")
        FD_e = totalnpixels/BAinPix*maskval
    else:
        if FD < maskval:
            import warnings
            warnings.warn("flux density < mask value, so it may be incorrect. Try to reduce s2n parameter!")
        if len(I_vals) < BAinPix:
            import warnings
            warnings.warn("signal_npix < beam_area_npix, so FD may be incorrect. Try to reduce s2n parameter!")

    return np.array([FD,FD_e])*u.Jy


def smooth_fits( inimage, outimage, beamsize, target, overwr=True ):
    '''
    Given an input fits file and the gaussian beam FWHM,
      the output image will be the result of convolution.
    Currently can only handle circular Gaussian beams (BMIN=BMAJ).
    'beamsize' must be in whatever units the input image BMAJ/BMIN are!
    '''
    data0, hdr = fits.getdata(inimage,0,header=True)
    if len(np.shape(data0))>2:
        print("Removing degenerate axes before smoothing")
    while len(np.shape(data0))>2:
        data0 = data0[0]

    # header info fixes
    try:
        dummy = hdr['CDELT1']
    except:
        hdr['CDELT1'] = hdr['CD1_1']
        hdr['CDELT2'] = hdr['CD2_2']

    # if something is wrong, let the user know and stop
    if beamsize < hdr['BMAJ']:
        raise RuntimeError('input beam size is too small')
    if ~np.isclose(hdr['BMAJ'],hdr['BMIN'],rtol=1e-5):
        print( '  beam major axis: ' + str(hdr['BMAJ']) )
        print( '  beam minor axis: ' + str(hdr['BMIN']) )
        ask_user()
    if ~np.isclose(np.abs(hdr['CDELT1']),np.abs(hdr['CDELT2']),rtol=1e-5):
        print( '  pixel dimension 1: ' + str(hdr['CDELT1']) )
        print( '  pixel dimension 2: ' + str(hdr['CDELT2']) )
        ask_user()

    # decide the convolving beam
    if target==False:
        oldbeam_px = hdr['BMAJ'] / np.abs(hdr['CDELT1'])
        conbeam_px = beamsize / np.abs(hdr['CDELT1'])
        newbeam_px = np.sqrt(oldbeam_px**2 + conbeam_px**2)
        newbeam_d  = newbeam_px * np.abs(hdr['CDELT1'])                         # just to put this value in the header
    elif target==True:
        oldbeam_px = hdr['BMAJ'] / np.abs(hdr['CDELT1'])
        newbeam_px = beamsize / np.abs(hdr['CDELT1'])
        conbeam_px = np.sqrt(newbeam_px**2 - oldbeam_px**2)
        newbeam_d  = beamsize                                                   # just to put this value in the header
    else:
        raise RuntimeError('target parameter must be either True/False!')

    # convolve with appropriate normalization
    if 'jy' in hdr['BUNIT'].lower() or 'jansky' in hdr['BUNIT'].lower():
        beamAreaRatio = (newbeam_px/oldbeam_px)**2                              # to normalize the flux densities
        data1 = convolve_fft( data0, Gaussian2DKernel(FWHM_to_SD(conbeam_px)),
                              preserve_nan=True, allow_huge=True,
                              normalize_kernel=(lambda _: beamAreaRatio) )
    elif 'k' in hdr['BUNIT'].lower():
        data1 = convolve_fft( data0, Gaussian2DKernel(FWHM_to_SD(conbeam_px)),
                              preserve_nan=True, allow_huge=True )
    else:
        raise RuntimeError('unknown BUNIT in header of the fits file!')

    # edit header and save data
    hdr['BMAJ'] = newbeam_d
    hdr['BMIN'] = newbeam_d
    fits.writeto( outimage, data1, hdr, overwrite=overwr )
    print('Smoothed the file '+inimage+' to the output file '+outimage)


def smooth_fits_to_commonbeam( fits1,fits2,outfits1,outfits2,newbeam=None,overwrite=True ):
    '''
    Given 2 fits files, they will be convolved to the same beam size 'newbeam'
    If newbeam=None, the file with the higher resolution will be
      convolved to the beam size of the file with the lower resolution.
      In this case the low-res file will be copied to 'outfits'.
    If newbeam is given, it must have same units as input images beam units.
    Currently works only with circular beam sizes!
    '''

    im_I1, h1 = fits.getdata(fits1,0,header=True)
    im_I2, h2 = fits.getdata(fits2,0,header=True)

    # If newbeam is given, directly smooth both files to that.
    # Otherwise, convolve only the high-res file to low-res beam size.
    if newbeam:
        smooth_fits(fits1,outfits1,newbeam,True)
        smooth_fits(fits2,outfits2,newbeam,True)
    else:
        # find out which one is bigger first
        BA1 = np.pi*h1['BMAJ']*h1['BMIN'] / (4*np.log(2))
        BA2 = np.pi*h2['BMAJ']*h2['BMIN'] / (4*np.log(2))
        if BA1>BA2:
            hiresfile = fits2
            hinewname = outfits2
            loresfile = fits1
            lonewname = outfits1
        elif BA1<BA2:
            hiresfile = fits1
            hinewname = outfits1
            loresfile = fits2
            lonewname = outfits2
        else:
            print('Both files have same beam size already')
            print('Not performing any convolution, just copying to new filenames')
            subprocess.Popen(['cp',fits1,outfits1])
            subprocess.Popen(['cp',fits2,outfits2])
            return None

        # copy low-res file, convolve high-res file
        subprocess.Popen(['cp',loresfile,lonewname])
        loreshdr = fits.getheader(loresfile)
        smooth_fits(hiresfile,hinewname,loreshdr['BMAJ'],True)


def gauss2Dfit_fits( fitsfile, skyposition, cutsize, calibr_uncert=0.1 ):
    '''
    perform 2D gaussian fitting on a point source.
    skyposition is made with SkyCoord().
    cutsize is the cutout size over which fitting is performed.
    assumes that the pixels are square shaped.
    '''

    fitshdu = fits.open(fitsfile)[0]
    fitshdr = fitshdu.header

    # header info fixes
    try:
        dummy = fitshdr['CDELT1']
    except:
        fitshdr['CDELT1'] = fitshdr['CD1_1']
        fitshdr['CDELT2'] = fitshdr['CD2_2']

    fitswcs = WCS(fitshdr)
    fitsdata= fitshdu.data
    cutout  = Cutout2D( fitsdata, skyposition, cutsize, fitswcs )
    beamSTD = FWHM_to_SD( fitshdr['BMAJ']/np.abs(fitshdr['CDELT1']) )
    cutdata = cutout.data
    maxval  = np.nanmax(cutdata)
    initx   = np.where(cutdata==maxval)[0]
    inity   = np.where(cutdata==maxval)[0]
    p_init  = models.Gaussian2D( amplitude=maxval, x_mean=initx, y_mean=inity,
                                    x_stddev=beamSTD, y_stddev=beamSTD )
    fit_p   = fitting.LevMarLSQFitter()
    y, x    = np.mgrid[ :cutdata.shape[0], :cutdata.shape[1] ]
    p       = fit_p( p_init, x, y, cutdata )

    peakamp = p.amplitude.value
    majorax = p.x_stddev.value
    minorax = p.y_stddev.value

    uncert = np.std(cutdata[cutdata<0.5*peakamp])
    #rms = np.sqrt( np.std(cutdata)**2 + np.mean(cutdata)**2 )

    # integrated flux density and its error (from NVSS paper, w/ compact sources assumption)
    fdint   = peakamp * np.sqrt(majorax*minorax/beamSTD/beamSTD)
    fdint_e = np.sqrt( (calibr_uncert*fdint)**2 +
                       (uncert/peakamp)**2 * ( majorax**2 * minorax**2 / (4*beamSTD**2+minorax**2) / (4*beamSTD**2+majorax**2) )**1.5 )

    #return [ p.amplitude.value, cutout.wcs.pixel_to_world(p.x_mean.value,p.y_mean.value), (p.x_mean.value,p.y_mean.value) ]
    #return [ p.amplitude.value, cutout.wcs.pixel_to_world(p.x_mean.value,p.y_mean.value) ]
    #return [ peakamp, cutout.wcs.pixel_to_world(p.x_mean.value,p.y_mean.value), majorax, minorax, (p.x_mean.value,p.y_mean.value) ]
    #return [ peakamp, uncert, fdint, fdint_e, cutout.wcs.pixel_to_world(p.x_mean.value,p.y_mean.value), p.x_mean.value,p.y_mean.value ]
    return [ peakamp, uncert, fdint, fdint_e ]


























