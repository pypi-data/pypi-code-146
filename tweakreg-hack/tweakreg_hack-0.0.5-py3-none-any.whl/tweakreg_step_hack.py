"""
JWST pipeline step for image alignment.

:Authors: Mihai Cara

"""
from os import path
import numpy as np
from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS
from tweakwcs.imalign import align_wcs
#from tweakwcs.tpwcs import JWSTgWCS
from tweakwcs.correctors import JWSTWCSCorrector
from tweakwcs.correctors import FITSWCSCorrector
from tweakwcs.matchutils import TPMatch

# JWST
from jwst.stpipe import Step
from jwst import datamodels

from jwst.tweakreg import astrometric_utils as amutils
from jwst.tweakreg.tweakreg_catalog import make_tweakreg_catalog


__all__ = ['TweakRegStep','tweak_loop']

def create_pixregionfile(x,y,regionname,color,coords='image',radius=1):
    if isinstance(radius,int):
        radius = [radius]*len(x)
    with open(regionname, 'w') as f:
        if isinstance(color,str):
            f.write('global color={0} dashlist=8 3 width=2 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1 \n'.format(color))
            do_col = False
        else:
            do_col = True
            f.write('global dashlist=8 3 width=2 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1 \n')
        f.write('%s \n'%coords)
        for star in range(len(x)):
            xval = x[star]
            yval = y[star]
            if do_col:
                f.write('circle({ra},{dec},{radius}") # color={color}\n'.format(ra=xval, dec=yval,radius=radius[star],color=color[star]))
            else:
                f.write('circle({ra},{dec},{radius}")\n'.format(ra=xval, dec=yval,radius=radius[star]))

#     return (ra_wcs,dec_wcs,flux)
    f.close()

def tweak_loop(init_tweakregstep,images,niters=2):
    for i in range(niters):
        if i>0:
            init_tweakregstep.already_matched = False
            new_images = []
            for im in images:
                ext = im.meta.filename[im.meta.filename.rfind('_')+1:]
                dm = datamodels.open(im.meta.filename.replace(ext,'tweakregstep.fits'))
                dm.source_catalog = None
                new_images.append(dm)
        images = init_tweakregstep.run(images)
    return images

class TweakRegStep(Step):
    """
    TweakRegStep: Image alignment based on catalogs of sources detected in
    input images.
    """

    class_alias = "tweakreg"

    spec = """
        save_catalogs = boolean(default=False) # Write out catalogs?
        catalog_format = string(default='ecsv') # Catalog output file format
        kernel_fwhm = float(default=2.5) # Gaussian kernel FWHM in pixels
        snr_threshold = float(default=10.0) # SNR threshold above the bkg
        brightest = integer(default=200) # Keep top ``brightest`` objects
        peakmax = float(default=None) # Filter out objects with pixel values >= ``peakmax``
        enforce_user_order = boolean(default=False) # Align images in user specified order?
        expand_refcat = boolean(default=False) # Expand reference catalog with new sources?
        minobj = integer(default=15) # Minimum number of objects acceptable for matching
        searchrad = float(default=2.0) # The search radius in arcsec for a match
        use2dhist = boolean(default=True) # Use 2d histogram to find initial offset?
        separation = float(default=1.0) # Minimum object separation in arcsec
        tolerance = float(default=0.7) # Matching tolerance for xyxymatch in arcsec
        xoffset = float(default=0.0), # Initial guess for X offset in arcsec
        yoffset = float(default=0.0) # Initial guess for Y offset in arcsec
        fitgeometry = option('shift', 'rshift', 'rscale', 'general', default='rshift') # Fitting geometry
        nclip = integer(min=0, default=3) # Number of clipping iterations in fit
        sigma = float(min=0.0, default=3.0) # Clipping limit in sigma units
        align_to_gaia = boolean(default=False)  # Align to GAIA catalog
        gaia_catalog = option('GAIADR2', 'GAIADR1', default='GAIADR2')
        min_gaia = integer(min=0, default=5) # Min number of GAIA sources needed
        save_gaia_catalog = boolean(default=False)  # Write out GAIA catalog as a separate product
        output_use_model = boolean(default=True)  # When saving use `DataModel.meta.filename`
    """

    reference_file_types = []

    def __init__(self):

        dummy_step = Step()
        
        self.input_file = ''
        self.name = dummy_step.name
        self.log = dummy_step.log
        self.output_file = ''
        self.suffix = dummy_step.suffix
        self._pre_hooks = dummy_step._pre_hooks
        self._post_hooks = dummy_step._post_hooks
        self.output_use_model = dummy_step.output_use_model
        self.output_ext = dummy_step.output_ext
        self.skip = dummy_step.skip
        self.enforce_user_order = True
        self.align_to_gaia = False
        self.nclip = 3
        self.sigma = 3.0
        self.tolerance = 0.7
        self.gaia_catalog = 'GAIADR2'
        self.override_save = False

        return

    def process(self, input):

        # TODO add these params as actual config items...wherever that happens
        for par,default in [('matching_function',None),('gaia_matching_function',None),
                        ('refcat',None),('already_matched',False),
                        ('brightest_gaia_mag',-999),('faintest_gaia_mag',999),('source_xcol',None),
                        ('source_ycol',None),('source_racol',None),('source_deccol',None),('ref_racol',None),('ref_deccol',None)]:
            if par not in self.__dict__.keys():
                self.__dict__[par] = default


        # try:
        #     temp = self.matching_function
        # except:
        #     self.matching_function = None

        # try:
        #     temp = self.gaia_matching_function
        # except:
        #     self.gaia_matching_function = None

        # try:
        #     temp = self.refcat
        # except:
        #     self.refcat = None

        # try:
        #     temp = self.already_matched
        # except:
        #     self.already_matched = False

        # try:
        #     temp = self.brightest_gaia_mag
        # except:
        #     self.brightest_gaia_mag = -999
        # try:
        #     temp = self.faintest_gaia_mag
        # except:
        #     self.faintest_gaia_mag = 999

        # try:
        #     temp = self.source_xcol
        # except:
        #     self.source_xcol = None



        if isinstance(self.refcat,str):
            try:
                self.refcat = Table.read(self.refcat,format='ascii')
            except:
                try:
                    self.refcat = Table.read(self.refcat,format='ascii.ecsv')
                except RuntimeError as e:
                    e.args = ('REFCAT MUST BE ASCII OR ECSV TABLE',) + e.args[1:]




        try:
            images = datamodels.ModelContainer(input)
        except TypeError as e:
            e.args = ("Input to tweakreg must be a list of DataModels, an "
                      "association, or an already open ModelContainer "
                      "containing one or more DataModels.", ) + e.args[1:]
            raise e
        if self.refcat is None and not self.align_to_gaia and len(images)==1:
            raise RuntimeError('With only one image, must align_to_gaia or provide refcat.')

        if self.align_to_gaia:
            # Set expand_refcat to True to eliminate possibility of duplicate
            # entries when aligning to GAIA
            self.expand_refcat = True
        else:
            self.expand_refcat = False

        if len(images) == 0:
            raise ValueError("Input must contain at least one image model.")

        # Build the catalogs for input images
        self.log.info("NUMBER OF IMAGES: %i"%len(images))
        for image_model in images:
            try:
                # TODO add source catalog to the image model instance
                catalog = image_model.source_catalog

                new_sourcecat = Table()
                if self.source_xcol is not None:
                    new_sourcecat['x'] = catalog[self.source_xcol]
                if self.source_ycol is not None:
                    new_sourcecat['y'] = catalog[self.source_ycol]
                if self.source_racol is not None:
                    new_sourcecat['ra'] = catalog[self.source_racol]
                if self.source_deccol is not None:
                    new_sourcecat['dec'] = catalog[self.source_deccol]
                for col in catalog.colnames:
                    if col not in [self.source_xcol,self.source_ycol,self.source_racol,self.source_deccol]:
                        new_sourcecat[col] = catalog[col]
                catalog = new_sourcecat

            except:
                catalog = make_tweakreg_catalog(
                    image_model, self.kernel_fwhm, self.snr_threshold,
                    brightest=self.brightest, peakmax=self.peakmax
                )
#            catalog.write('input.cat',format='ascii')


            # filter out sources outside the WCS bounding box
            bb = None#image_model.meta.wcs.bounding_box
            if bb is not None:
                ((xmin, xmax), (ymin, ymax)) = bb
                xname = 'xcentroid' if 'xcentroid' in catalog.colnames else 'x'
                yname = 'ycentroid' if 'ycentroid' in catalog.colnames else 'y'
                x = catalog[xname]
                y = catalog[yname]
                mask = (x > xmin) & (x < xmax) & (y > ymin) & (y < ymax)
                catalog = catalog[mask]

            filename = image_model.meta.filename
            nsources = len(catalog)
            if nsources == 0:
                self.log.warning('No sources found in {}.'.format(filename))
            else:
                self.log.info('Detected {} sources in {}.'
                              .format(len(catalog), filename))

            if self.save_catalogs:
                catalog_filename = filename.replace(
                    '.fits', '_cat.{}'.format(self.catalog_format)
                )
                if self.catalog_format == 'ecsv':
                    fmt = 'ascii.ecsv'
                elif self.catalog_format == 'fits':
                    # NOTE: The catalog must not contain any 'None' values.
                    #       FITS will also not clobber existing files.
                    fmt = 'fits'
                else:
                    raise ValueError(
                        '\'catalog_format\' must be "ecsv" or "fits".'
                    )
                catalog.write(catalog_filename, format=fmt, overwrite=True)
                self.log.info('Wrote source catalog: {}'
                              .format(catalog_filename))
                image_model.meta.tweakreg_catalog = catalog_filename

            # Temporarily attach catalog to the image model so that it follows
            # the grouping by exposure, to be removed after use below
            image_model.catalog = catalog

        # group images by their "group id":
        grp_img = list(images.models_grouped)

        self.log.info('')
        self.log.info("Number of image groups to be aligned: {:d}."
                      .format(len(grp_img)))
        self.log.info("Image groups:")

        # if len(grp_img) == 1:
        #     self.log.info("* Images in GROUP 1:")
        #     for im in grp_img[0]:
        #         self.log.info("     {}".format(im.meta.filename))
        #     self.log.info('')

        #     # we need at least two exposures to perform image alignment
        #     self.log.warning("At least two exposures are required for image "
        #                      "alignment.")
        #     self.log.warning("Nothing to do. Skipping 'TweakRegStep'...")
        #     self.skip = True
        #     for model in images:
        #         model.meta.cal_step.tweakreg = "SKIPPED"
        #         # Remove the attached catalogs
        #         del model.catalog
        #     return input

        # create a list of WCS-Catalog-Images Info and/or their Groups:
        imcats = []
        for g in grp_img:
            if len(g) == 0:
                raise AssertionError("Logical error in the pipeline code.")
            else:
                group_name = _common_name(g)
                wcsimlist = list(map(self._imodel2wcsim, g))
                # Remove the attached catalogs
                for model in g:
                    del model.catalog
                self.log.info("* Images in GROUP '{}':".format(group_name))
                for im in wcsimlist:
                    im.meta['group_id'] = group_name
                    self.log.info("     {}".format(im.meta['name']))
                imcats.extend(wcsimlist)

        self.log.info('')

        if self.already_matched and self.refcat is not None:
            #create_pixregionfile(self.refcat['RA'],self.refcat['DEC'],'refcat.reg','red',coords='FK5',radius=1)
            #create_pixregionfile(catalog['x'],catalog['y'],'inputcat.reg','green',coords='image',radius=2)
            self.matching_function = None
        elif self.matching_function is None:
            # align images:
            self.matching_function = TPMatch(
                searchrad=self.searchrad,
                separation=self.separation,
                use2dhist=self.use2dhist,
                tolerance=self.tolerance,
                xoffset=self.xoffset,
                yoffset=self.yoffset
            )
        else:
            self.log.info('USING PROVIDED MATCHING FUNCTION')


        #print(self.refcat)
        try:
            create_pixregionfile(self.refcat[self.ref_racol],self.refcat[self.ref_deccol],
            self.input_file.replace('.fits','.reg'),'red',coords='icrs',radius=[.5]*len(self.refcat))
        except:
            pass
        #sys.exit()
        if self.refcat is not None:
            keep = []
            new_refcat = Table()
            if self.ref_racol is not None:
                new_refcat['RA'] = self.refcat[self.ref_racol]
            if self.ref_deccol is not None:
                new_refcat['DEC'] = self.refcat[self.ref_deccol]
            for col in self.refcat.colnames:
                if col not in [self.ref_racol,self.ref_deccol]:
                    new_refcat[col] = self.refcat[col]
            self.refcat = new_refcat



        self.refcat = self.refcat



        try:
            align_wcs(
                imcats,
                refcat=self.refcat,
                enforce_user_order=self.enforce_user_order,
                expand_refcat=self.expand_refcat,
                minobj=self.minobj,
                match=self.matching_function,
                fitgeom=self.fitgeometry,
                nclip=self.nclip,
                sigma=(self.sigma, 'rmse')
            )

        except ValueError as e:
            raise e
            # msg = e.args[0]
            # if (msg == "Too few input images (or groups of images) with "
            #         "non-empty catalogs."):
            #     # we need at least two exposures to perform image alignment
            #     self.log.warning(msg)
            #     self.log.warning("At least two exposures are required for "
            #                      "image alignment.")
            #     self.log.warning("Nothing to do. Skipping 'TweakRegStep'...")
            #     self.skip = True
            #     for model in images:
            #         model.meta.cal_step.tweakreg = "SKIPPED"
            #     return images

            # else:
            #     raise e

        for imcat in imcats:

            twcs = imcat.wcs

            try:
                wcs = imcat.meta['image_model'].meta.wcs
            except:
                wcs = twcs

            if not self._is_wcs_correction_small(wcs, twcs):
                # Large corrections are typically a result of source
                # mis-matching or poorly-conditioned fit. Skip such models.
                self.log.warning(f"WCS has been tweaked by more than {10 * self.tolerance} arcsec")
                self.log.warning("Skipping 'TweakRegStep'...")
                self.skip = True
                for model in images:
                    model.meta.cal_step.tweakreg = "SKIPPED"
                return images

        if self.align_to_gaia:
            self.log.info('PERFORMING GAIA ALIGNMENT')
            # Get catalog of GAIA sources for the field
            #
            # NOTE:  If desired, the pipeline can write out the reference
            #        catalog as a separate product with a name based on
            #        whatever convention is determined by the JWST Cal Working
            #        Group.
            if self.save_gaia_catalog:
                output_name = 'fit_{}_ref.ecsv'.format(self.gaia_catalog.lower())
            else:
                output_name = None
            ref_cat = amutils.create_astrometric_catalog(images,
                                                         self.gaia_catalog,
                                                         output=output_name)

            ref_cat = ref_cat[np.where(np.logical_and(ref_cat['mag']<self.faintest_gaia_mag,
                                      ref_cat['mag']>self.brightest_gaia_mag))[0]]

            self.log.info('%i in GAIA (%s)'%(len(ref_cat),self.gaia_catalog))

            # Check that there are enough GAIA sources for a reliable/valid fit
            num_ref = len(ref_cat)
            if num_ref < self.min_gaia:
                msg = "Not enough GAIA sources for a fit: {}\n".format(num_ref)
                msg += "Skipping alignment to {} astrometric catalog!\n".format(self.gaia_catalog)
                # Raise Exception here to avoid rest of code in this try block
                self.log.warning(msg)
            else:
                # align images:
                # Update to separation needed to prevent confusion of sources
                # from overlapping images where centering is not consistent or
                # for the possibility that errors still exist in relative overlap.
                if self.gaia_matching_function is None:
                    self.gaia_matching_function = TPMatch(
                        searchrad=self.searchrad,
                        separation=self.separation,
                        use2dhist=self.use2dhist,
                        tolerance=self.tolerance,
                        xoffset=self.xoffset,
                        yoffset=self.yoffset
                    )
                else:
                    self.log.info('USING PROVIDED MATCHING FUNCTION FOR GAIA')

                # Set group_id to same value so all get fit as one observation
                # The assigned value, 987654, has been hard-coded to make it
                # easy to recognize when alignment to GAIA was being performed
                # as opposed to the group_id values used for relative alignment
                # earlier in this step.
                for imcat in imcats:
                    imcat.meta['group_id'] = 987654
                    if 'REFERENCE' in imcat.meta['fit_info']['status']:
                        del imcat.meta['fit_info']


                # Perform fit
                align_wcs(
                    imcats,
                    refcat=ref_cat,
                    enforce_user_order=True,
                    expand_refcat=False,
                    minobj=self.minobj,
                    match=self.gaia_matching_function,
                    fitgeom=self.fitgeometry,
                    nclip=self.nclip,
                    sigma=(self.sigma, 'rmse')
                )

        for n,imcat in enumerate(imcats):
            imcat.meta['image_model'].meta.cal_step.tweakreg = 'COMPLETE'

            # retrieve fit status and update wcs if fit is successful:
            if 'SUCCESS' in imcat.meta.get('fit_info')['status']:

                # Update/create the WCS .name attribute with information
                # on this astrometric fit as the only record that it was
                # successful:
                if self.align_to_gaia:
                    # NOTE: This .name attrib agreed upon by the JWST Cal
                    #       Working Group.
                    #       Current value is merely a place-holder based
                    #       on HST conventions. This value should also be
                    #       translated to the FITS WCSNAME keyword
                    #       IF that is what gets recorded in the archive
                    #       for end-user searches.
                    imcat.wcs.name = "FIT-LVL3-{}".format(self.gaia_catalog)

                imcat.meta['image_model'].meta.wcs = imcat.wcs
                images[n].meta.wcs = imcat.wcs

                # """
                # # Also update FITS representation in input exposures for
                # # subsequent reprocessing by the end-user.
                if True:#self.override_save == True:
                    # gwcs_header = imcat.wcs.to_fits_sip(max_pix_error=0.1,
                    #                                 max_inv_pix_error=0.1,
                    #                                 degree=3,
                    #                                 npoints=128)
                    try:
                        gwcs_header = imcat.wcs.to_header()
                    except:
                        gwcs_header = imcat.wcs.to_fits()[0]
                    #sys.exit()
                    from astropy.io import fits
                    dm_fits = fits.open(self.input_file)
                    dm_fits['SCI',1].header.update(gwcs_header)
                    #for key,value in dict(gwcs_header).items():
                    #    for k in dm_fits['SCI',1].header.keys():
                    #        if k==key:
                    #            print(dm_fits['SCI',1].header[key], value)
                    #            dm_fits['SCI',1].header[key] = value
                    #            break

                    dm_fits.writeto(self.output_file,overwrite=True)
                    #test = imcat.wcs.to_fits() 
                    #test.writeto(self.output_file)
                        
                    return 
                # """
            else:
                raise Exception('TWEAKSTEP ' + imcat.meta.get('fit_info')['status'])

        return images #imcats

    def _is_wcs_correction_small(self, wcs, twcs):
        """Check that the newly tweaked wcs hasn't gone off the rails"""
        tolerance = 10.0 * self.tolerance * u.arcsec

        try:
            ra, dec = wcs.footprint(axis_type="spatial").T
            tra, tdec = twcs.footprint(axis_type="spatial").T
        except:
            try:
                ra, dec = [i[0] for i in wcs.footprint],[i[1] for i in wcs.footprint]
            except:
                ra, dec = wcs.footprint(axis_type="spatial").T
                
            tra, tdec = [i[0] for i in twcs.footprint],[i[1] for i in twcs.footprint]

        skycoord = SkyCoord(ra=ra, dec=dec, unit="deg")
        tskycoord = SkyCoord(ra=tra, dec=tdec, unit="deg")

        separation = skycoord.separation(tskycoord)

        return (separation < tolerance).all()

    def _imodel2wcsim(self, image_model):
        # make sure that we have a catalog:
        if hasattr(image_model, 'catalog'):
            catalog = image_model.catalog
        else:
            catalog = image_model.meta.tweakreg_catalog

        model_name = path.splitext(image_model.meta.filename)[0].strip('_- ')

        if isinstance(catalog, Table):
            if not catalog.meta.get('name', None):
                catalog.meta['name'] = model_name

        else:
            try:
                cat_name = str(catalog)
                catalog = Table.read(catalog, format='ascii.ecsv')
                catalog.meta['name'] = cat_name
            except IOError:
                self.log.error("Cannot read catalog {}".format(catalog))

        if 'xcentroid' in catalog.colnames:
            catalog.rename_column('xcentroid', 'x')
            catalog.rename_column('ycentroid', 'y')

        # create WCSImageCatalog object:
        refang = image_model.meta.wcsinfo.instance
        try:
            #im = JWSTgWCS(
            im = JWSTWCSCorrector(
            wcs=image_model.meta.wcs,
            wcsinfo={'roll_ref': refang['roll_ref'],
                     'v2_ref': refang['v2_ref'],
                     'v3_ref': refang['v3_ref']},
            meta={'image_model': image_model, 'catalog': catalog,
                  'name': model_name}
                  )
        except:
            head = fits.open(self.input_file)[1].header
            wcs = WCS(head)
            wcs.footprint = WCS.calc_footprint(wcs)
            im = FITSWCSCorrector(
            wcs = wcs,
            meta = {'image_model': image_model, 'catalog': catalog,
                  'name': model_name}
            )

        return im


def _common_name(group):
    file_names = [path.splitext(im.meta.filename)[0].strip('_- ')
                  for im in group]
    fname_len = list(map(len, file_names))
    assert all(fname_len[0] == length for length in fname_len)
    cn = path.commonprefix(file_names)
    assert cn
    return cn