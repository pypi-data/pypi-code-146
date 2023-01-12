import math
import numpy as np
from ..resources.logger import LoggerOrPrint
from ..misc import fourier_filters
from ..misc.padding import pad_interpolate, recut
from ..utils import get_fftw_threads

class GeoPars:
    """
    A class to describe the geometry of a phase contrast radiography with
    a source obtained by a focussing system, possibly astigmatic, which is
    at distance z1_vh from the sample. The detector is at z2 from the sample
    """

    def __init__(
        self,
        z1_vh=None,
        z2=None,
        pix_size_det=None,
        wavelength=None,
        magnification=True,
        length_scale=10.0e-6,
        logger=None,
    ):
        """
        Parameters
        ----------
        z1_vh : None, a float, or a sequence of two floats
           the source sample distance (meters), if None the parallel beam is assumed.
           If two floats are given then they are taken as the distance of the vertically focused source (horizontal line)
           and the horizontaly focused source (vertical line) for KB mirrors.
        z2 : float
           the sample detector distance (meters).
        pix_size_det: float
           pixel size (meters)
        wavelength: float
           beam wave length (meters).
        magnification: boolean defaults to True
           if false no magnification is considered
        length_scale: float
            rescaling length scale, meant to avoid having too big or too small numbers.
            defaults to 10.0e-6
        logger: Logger, optional
            A logging object
        """
        self.logger = LoggerOrPrint(logger)
        if z1_vh is None:
            self.z1_vh = None
        else:
            if hasattr(type(z1_vh), "__iter__"):
                self.z1_vh = np.array(z1_vh)
            else:
                self.z1_vh = np.array([z1_vh, z1_vh])
        self.z2 = z2
        self.magnification = magnification
        self.pix_size_det = pix_size_det

        if self.magnification and self.z1_vh is not None:
            self.M_vh = (self.z1_vh + self.z2) / self.z1_vh
        else:
            self.M_vh = np.array([1, 1])

        self.logger.debug("Magnification : h ({}) ;  v ({}) ".format(self.M_vh[1], self.M_vh[0]))

        self.length_scale = length_scale
        self.wavelength = wavelength

        self.maxM = self.M_vh.max()

        self.pix_size_rec = self.pix_size_det / self.maxM  # we bring everything to highest magnification

        which_unit = np.sum(np.array([(self.pix_size_rec > small) for small in [1.0e-6, 1.0e-7]]).astype(np.int32))
        self.pixelsize_string = [
            "{:.1f} nm".format(self.pix_size_rec * 1e9),
            "{:.3f} um".format(self.pix_size_rec * 1e6),
            "{:.1f} um".format(self.pix_size_rec * 1e6),
        ][which_unit]

        if self.magnification:
            self.logger.debug(
                "All images are resampled to smallest pixelsize: {}".format(self.pixelsize_string),
            )
        else:
            self.logger.debug("Pixelsize images:  {}".format(self.pixelsize_string))


class CTFPhaseRetrieval:
    def __init__(
        self, shape, geo_pars, delta_beta,
        padded_shape="auto", padding_mode="reflect", translation_vh=None, normalize_by_mean=False,
        lim1=1.0e-5, lim2=0.2, use_rfft=False, fftw_num_threads=None, logger=None
    ):
        """
        This class implements the CTF formula (see equation 8 in Boliang Yu et al
        Optic Express Vol 26, No 9, 2018) in its regularised form which avoids the zeros
        of unregularised_filter_denominator
        (unreg_filter_denom is the so here named denominator/delta_beta of equation 8)

        Parameters
        ----------
        geo_pars: GeoPars
            the geometry description
        delta_beta : float
            the delta/beta ratio
        padded_shape: str or tuple, optional
            Padded image shape, in the form (num_rows, num_columns) i.e (vertical, horizontal).
            By default, it is twice the image shape.
        padding_mode: str
            Padding mode. It must be valid for the numpy.pad function
        translation_vh: array, optional
            Shift in the form (y, x). It is used to perform a translation of the image before applying the CTF filter.
        normalize_by_mean: bool
            Whether to divide the (padded) image with its mean before applying the CTF filter.
        lim1: float >0
            the regulariser strenght at low  frequencies
        lim2: float >0
            the regulariser strenght at high frequencies
        use_rfft: bool, optional
            Whether to use real-to-complex (R2C) FFT instead of usual complex-to-complex (C2C).
        fftw_num_threads: bool or None or int, optional
            Whether to use FFTW for speeding up FFT.
            Let `n_max` denote the number of available cores, then:

               - If an positive integer `n` is provided, then `n` threads are used
               - If a negative integer `n` is provided, then `n_max + n` threads are used
               - If `True` is provided, then `n_max` threads are used
               - If `False`or `None` is provided (default), then FFTW is not used
        logger: optional
            a logger object
        """
        self.logger = LoggerOrPrint(logger)
        if not isinstance(geo_pars, GeoPars):
            raise ValueError("Expected GeoPars instance for 'geo_pars' parameter")
        self.geo_pars = geo_pars
        self._calc_shape(shape, padded_shape, padding_mode)
        self.delta_beta = delta_beta

        self.lim = None
        self.lim1 = lim1
        self.lim2 = lim2
        self.normalize_by_mean = normalize_by_mean
        self.translation_vh = translation_vh
        self.use_rfft = use_rfft
        self._fft_func = np.fft.rfft2 if use_rfft else np.fft.fft2
        self._ifft_func = np.fft.irfft2 if use_rfft else np.fft.ifft2
        self._setup_fftw(fftw_num_threads)
        self._get_ctf_filter()


    def _calc_shape(self, shape, padded_shape, padding_mode):
        if np.isscalar(shape):
            shape = (shape, shape)
        else:
            assert len(shape) == 2
        self.shape = shape
        if padded_shape is None or padded_shape is False:
            padded_shape = self.shape # no padding
        elif isinstance(padded_shape, (tuple, list, np.ndarray)):
            pass
        elif padded_shape == "auto":
            padded_shape = (2 * self.shape[0], 2 * self.shape[1])
        self.shape_padded = tuple(padded_shape)
        self.padding_mode = padding_mode


    def _setup_fftw(self, fftw_num_threads):
        fftw_num_threads = get_fftw_threads(fftw_num_threads)
        self.use_fftw = False
        if self.use_rfft and (fftw_num_threads > 0):
            # importing silx.math.fft creates opencl contexts all over the place
            # because of the silx.opencl.ocl singleton.
            # So, import silx as late as possible
            from silx.math.fft.fftw import FFTW, __have_fftw__
            if __have_fftw__:
                self.use_fftw = True
                self.fftw = FFTW(
                    shape=self.shape_padded, dtype="f", num_threads=fftw_num_threads
                )
                self._fft_func = self.fftw.fft
                self._ifft_func = self.fftw.ifft


    def _get_ctf_filter(self):
        """
        The parameter "length_scale" was mentioned, in the octave code,
        as a rescaling length scale, which is meant to avoid
        having too big or too small numbers.
        From the mathematical point of view, it is infact completely trasparent:
        its action is on fsamplex, fsampley and  betash, betasv.
        But these latters ( beta's)  are multiplied by  the formers (fsample's) so that
        "length_scale" mathematically disappears, however in case of simple precision float
        the exponent of a float number ranges from -38 to 38, and one could approach it
        as an example by taking the square of a very small number ( 1.0e-19), and losing significant bits
        in he mantissa or getting zero, or the square of a big number, thus generting inf
        Althought the values involved in our x-ray regimes seems safe, with respect to these problems,
        this length_scale parameters does not hurt.
        """
        padded_img_shape = self.shape_padded
        fsample_vh = np.array(
            [self.geo_pars.length_scale / self.geo_pars.pix_size_rec, self.geo_pars.length_scale / self.geo_pars.pix_size_rec]
        )

        if not self.use_rfft:
            ff_index_vh = list(map(np.fft.fftfreq, padded_img_shape))
        else:
            ff_index_vh = [np.fft.fftfreq(padded_img_shape[0]), np.fft.rfftfreq(padded_img_shape[1])]

        # if padded_img_shape[1]%2 == 0 : # change to holotomo_slave indexing (by a transparent 2pi shift)
        #     ff_index_x[ ff_index_x  == -0.5    ] =  +0.5
        # if padded_img_shape[0]%2 == 0 : # change to holotomo_slave indexing (by a transparent 2pi shift)
        #     ff_index_y[ ff_index_y  == -0.5    ] =  +0.5

        frequencies_vh = np.array(
            np.meshgrid(ff_index_vh[0] * fsample_vh[0], ff_index_vh[1] * fsample_vh[1], indexing="ij")
        )

        frequencies_squared_vh = frequencies_vh * frequencies_vh

        """
        ---------------  fresnelnumbers and forward propagators -------------------
        In the limit of parallel beam, z1_h and z1_v would be infinite
        so that the here below distances becomes z2
        which is sample-detector distance.
        """

        if self.geo_pars.z1_vh is not None:
            distances_vh = (self.geo_pars.z1_vh * self.geo_pars.z2) / (self.geo_pars.z1_vh + self.geo_pars.z2)
        else:
            distances_vh = np.array([self.geo_pars.z2, self.geo_pars.z2])

        """
        Citing David Paganin (2002) :
        The intensity I_{R_1}(r⊥,z) at a distance z  of a weakly refracting object illuminated by a
        point source at distance R1  behind the said object, is related to the intensity
        I∞(r⊥,z), which would result from normally
        incident collimated illumination of the same object, by (Pogany et al., 1997):
          I_{R_1}(r⊥,z) = 1/{M^2} I∞(r⊥/M , z/M)
        where M is the magnification.
        This explains the effective distance formula expressed by
        distancesh, distancesv  above.
        ------------------------------------------------------------------------------
        """

        lambda_dist_vh = self.geo_pars.wavelength * distances_vh / (self.geo_pars.length_scale ** 2)

        """
        ---------------------------------------------------------------------------------------
        -> cut_v at first maximum of ctf largest distance

        In the paraxial expansion of the Fresnel propagator, the phase is equal to
                          1/2 K_{parallel}^2 wavelength * Distance /2 / pi

        When this is equal to a multiple of 2 pi, the effect of propagation disappears
        and we have a singularity in equation 8.

        The sampling in the reciprocal space is done with  a step length of 2*pi*fsamplex,y
          (note: fsamples are the plain inverse of pixel size)
        The first singularity occurs  at a frequence number
                        K_{parallel}/2/pi/ fsamplex

         for K_{parallel}^2 = 2 * (2pi)^2 /( wavelength * distance  )

         which would correspond to
                   K_{parallel}/2/pi/ fsamplex  =  sqrt( 2/wavelength*distance) / fsample

        Question:( why the factor 2 appear at the denominator in the square root below?)
        Answer : the below defined cut corresponds to the first maximum of the denominator,
        before arriving to the first zero. In this way the regularisation
        is already at ( almost) full strenght on the first pole.ation
        ## is already at ( almost) full strenght on the first pole.
        """
        self.cut_v = math.sqrt(1.0 / 2 / lambda_dist_vh[0]) / fsample_vh[0]
        self.cut_v = min(self.cut_v, 0.5)

        self.logger.debug("Normalized cut-off = {:5.3f}".format(self.cut_v))

        self.r = fourier_filters.get_lowpass_filter(
            padded_img_shape,
            cutoff_par=(
                0.5 / (self.cut_v + 1.0 / padded_img_shape[0]),
                0.01 * padded_img_shape[0] / (1 + self.cut_v * padded_img_shape[0]),
            ),
            use_rfft=self.use_rfft
        )
        self.r /= self.r[0, 0]

        self.lim = self.lim1 * self.r + self.lim2 * (1 - self.r)

        # more methods exist in the original code, and they are initialized starting from here
        # (ht_app1, ht_app2... ht_app7)

        fresnel_phase = (
            np.pi * lambda_dist_vh[1] * frequencies_squared_vh[1] + np.pi * lambda_dist_vh[0] * frequencies_squared_vh[0]
        )

        if self.delta_beta:
            self.logger.debug(
                "Taking into account absorption assuming homogeneous object.\n"
                "Set delta_beta = 0 if this is not the purpose."
            )
            unreg_filter_denom = np.sin(fresnel_phase) + (1.0 / self.delta_beta) * np.cos(fresnel_phase)
        else:
            unreg_filter_denom = np.sin(fresnel_phase)
        self.unreg_filter_denom = unreg_filter_denom.astype(np.float32)
        self._ctf_filter_denom = (2 * self.unreg_filter_denom * self.unreg_filter_denom + self.lim).astype(np.complex64)


    def _apply_filter(self, img):
        img_f = self._fft_func(img)
        img_f *= self.unreg_filter_denom

        unreg_filter_denom_0_mean = self.unreg_filter_denom[0, 0]
        nf, mf = img.shape

        # here it is assumed that the average of img is 1 and the DC component is removed
        img_f[0, 0] -= nf * mf * unreg_filter_denom_0_mean

        ## formula 8, with regularisation to stay at a safe distance from the poles
        img_f /= self._ctf_filter_denom
        ph = self._ifft_func(img_f).real
        return ph


    def retrieve_phase(self, img):
        """
        Apply the CTF filter to retrieve the phase.

        Parameters
        ----------
        img: np.ndarray
            Projection image. It must have been already flat-fielded.

        Returns
        --------
        ph: numpy.ndarray
            Phase image
        """
        padded_img = pad_interpolate(
            img, self.shape_padded, translation_vh=self.translation_vh, padding_mode=self.padding_mode
        )
        if self.normalize_by_mean:
            padded_img /= padded_img.mean()
        phase_img = self._apply_filter(padded_img)
        res = recut(phase_img, img.shape)
        return res


CtfFilter = CTFPhaseRetrieval