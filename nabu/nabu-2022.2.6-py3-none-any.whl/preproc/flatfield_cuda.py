from typing import Union
import numpy as np
import pycuda.gpuarray as garray
from ..preproc.flatfield import FlatFieldArrays
from ..cuda.kernel import CudaKernel
from ..utils import get_cuda_srcfile
from ..io.reader import load_images_from_dataurl_dict


class CudaFlatFieldArrays(FlatFieldArrays):
    def __init__(
        self,
        radios_shape: tuple,
        flats: dict,
        darks: dict,
        radios_indices=None,
        interpolation: str = "linear",
        distortion_correction=None,
        nan_value=1.0,
        radios_srcurrent=None,
        flats_srcurrent=None,
        cuda_options: Union[dict, None] = None,
    ):
        """
        Initialize a flat-field normalization CUDA process.
        Please read the documentation of nabu.preproc.flatfield.FlatField for help
        on the parameters.
        """
        #
        if distortion_correction is not None:
            raise NotImplementedError(
                "Flats distortion correction is not implemented with the Cuda backend"
            )
        #
        super().__init__(
            radios_shape,
            flats,
            darks,
            radios_indices=radios_indices,
            interpolation=interpolation,
            distortion_correction=distortion_correction,
            radios_srcurrent=radios_srcurrent,
            flats_srcurrent=flats_srcurrent,
            nan_value=nan_value
        )
        self._set_cuda_options(cuda_options)
        self._init_cuda_kernels()
        self._load_flats_and_darks_on_gpu()

    def _set_cuda_options(self, user_cuda_options):
        self.cuda_options = {"device_id": None, "ctx": None, "cleanup_at_exit": None}
        if user_cuda_options is None:
            user_cuda_options = {}
        self.cuda_options.update(user_cuda_options)

    def _init_cuda_kernels(self):
        # TODO
        if self.interpolation != "linear":
            raise ValueError(
                "Interpolation other than linar is not yet implemented in the cuda back-end"
            )
        #
        self._cuda_fname = get_cuda_srcfile("flatfield.cu")
        options = [
            "-DN_FLATS=%d" % self.n_flats,
            "-DN_DARKS=%d" % self.n_darks,
        ]
        if self.nan_value is not None:
            options.append("-DNAN_VALUE=%f" % self.nan_value)
        self.cuda_kernel = CudaKernel(
            "flatfield_normalization",
            self._cuda_fname,
            signature="PPPiiiPP",
            options=options
        )
        self._nx = np.int32(self.shape[1])
        self._ny = np.int32(self.shape[0])


    def _load_flats_and_darks_on_gpu(self):
        # Flats
        self.d_flats = garray.zeros((self.n_flats,) + self.shape, np.float32)
        for i, flat_idx in enumerate(self._sorted_flat_indices):
            self.d_flats[i].set(np.ascontiguousarray(self.flats[flat_idx], dtype=np.float32))
        # Darks
        self.d_darks = garray.zeros((self.n_darks,) + self.shape, np.float32)
        for i, dark_idx in enumerate(self._sorted_dark_indices):
            self.d_darks[i].set(np.ascontiguousarray(self.darks[dark_idx], dtype=np.float32))
        self.d_darks_indices = garray.to_gpu(
            np.array(self._sorted_dark_indices, dtype=np.int32)
        )
        # Indices
        self.d_flats_indices = garray.to_gpu(self.flats_idx)
        self.d_flats_weights = garray.to_gpu(self.flats_weights)

    def normalize_radios(self, radios):
        """
        Apply a flat-field correction, with the current parameters, to a stack
        of radios.

        Parameters
        -----------
        radios_shape: `pycuda.gpuarray.GPUArray`
            Radios chunk.
        """
        if not(isinstance(radios, garray.GPUArray)):
            raise ValueError("Expected a pycuda.gpuarray (got %s)" % str(type(radios)))
        if radios.dtype != np.float32:
            raise ValueError("radios must be in float32 dtype (got %s)" % str(radios.dtype))
        if radios.shape != self.radios_shape:
            raise ValueError("Expected radios shape = %s but got %s" % (str(self.radios_shape), str(radios.shape)))
        self.cuda_kernel(
            radios,
            self.d_flats,
            self.d_darks,
            self._nx,
            self._ny,
            np.int32(self.n_radios),
            self.d_flats_indices,
            self.d_flats_weights,
        )
        if self.normalize_srcurrent:
            for i in range(self.n_radios):
                radios[i] *= self.srcurrent_ratios[i]
        return radios

CudaFlatField = CudaFlatFieldArrays

class CudaFlatFieldDataUrls(CudaFlatField):
    def __init__(
        self,
        radios_shape: tuple,
        flats: dict,
        darks: dict,
        radios_indices=None,
        interpolation: str = "linear",
        distortion_correction=None,
        nan_value=1.0,
        radios_srcurrent=None,
        flats_srcurrent=None,
        cuda_options: Union[dict, None] = None,
        **chunk_reader_kwargs
    ):

        flats_arrays_dict = load_images_from_dataurl_dict(flats, **chunk_reader_kwargs)
        darks_arrays_dict = load_images_from_dataurl_dict(darks, **chunk_reader_kwargs)
        super().__init__(
            radios_shape,
            flats_arrays_dict,
            darks_arrays_dict,
            radios_indices=radios_indices,
            interpolation=interpolation,
            distortion_correction=distortion_correction,
            radios_srcurrent=radios_srcurrent,
            flats_srcurrent=flats_srcurrent,
            cuda_options=cuda_options
        )
