from math import ceil
import numpy as np
from ...utils import deprecated
from ...preproc.flatfield_cuda import CudaFlatFieldDataUrls
from ...preproc.shift import VerticalShift
from ...preproc.shift_cuda import CudaVerticalShift

from ...preproc.phase_cuda import CudaPaganinPhaseRetrieval
from ...reconstruction.sinogram_cuda import CudaSinoBuilder, CudaSinoNormalization
from ...reconstruction.sinogram import SinoBuilder, SinoNormalization
from ...misc.unsharp_cuda import CudaUnsharpMask
from ...misc.rotation_cuda import CudaRotation
from ...misc.histogram_cuda import CudaPartialHistogram
from .fbp import BackprojectorHelical


try:
    from ...reconstruction.hbp import HierarchicalBackprojector  # pylint: disable=E0401,E0611

    print("Successfully imported hbp")
except:
    HierarchicalBackprojector = None

from ...cuda.utils import get_cuda_context, __has_pycuda__, __pycuda_error_msg__, replace_array_memory
from ..utils import pipeline_step
from .helical_chunked_regridded import HelicalChunkedRegriddedPipeline

if __has_pycuda__:
    import pycuda.gpuarray as garray


class CudaHelicalChunkedRegriddedPipeline(HelicalChunkedRegriddedPipeline):
    """
    Cuda backend of HelicalChunkedPipeline
    """

    VerticalShiftClass = CudaVerticalShift
    SinoBuilderClass = CudaSinoBuilder
    FBPClass = BackprojectorHelical
    HBPClass = HierarchicalBackprojector

    HistogramClass = CudaPartialHistogram
    SinoNormalizationClass = CudaSinoNormalization

    def __init__(
        self,
        process_config,
        sub_region,
        logger=None,
        extra_options=None,
        phase_margin=None,
        cuda_options=None,
        reading_granularity=10,
        span_info=None,
        num_weight_radios_per_app=1000,
    ):
        self._init_cuda(cuda_options)
        super().__init__(
            process_config,
            sub_region,
            logger=logger,
            extra_options=extra_options,
            phase_margin=phase_margin,
            reading_granularity=reading_granularity,
            span_info=span_info,
        )
        self._register_callbacks()

        self.num_weight_radios_per_app = num_weight_radios_per_app

    def _init_cuda(self, cuda_options):
        if not (__has_pycuda__):
            raise ImportError(__pycuda_error_msg__)
        cuda_options = cuda_options or {}
        self.ctx = get_cuda_context(**cuda_options)
        self._d_radios = None
        self._d_radios_weights = None
        self._d_sinos = None
        self._d_recs = None

    def _allocate_array(self, shape, dtype, name=None):
        name = name or "tmp"  # should be mandatory
        d_name = "_d_" + name
        d_arr = getattr(self, d_name, None)
        if d_arr is None:
            self.logger.debug("Allocating %s: %s" % (name, str(shape)))
            d_arr = garray.zeros(shape, dtype)
            setattr(self, d_name, d_arr)
        return d_arr

    def _process_finalize(self):
        pass

    def _post_primary_data_reduction(self, i_slice):
        self._allocate_array((self.num_weight_radios_per_app,) + self.radios_slim.shape[1:], "f", name="radios_weights")

        if self.process_config.nabu_config["reconstruction"]["angular_tolerance_steps"]:
            self.radios[:, i_slice, :][np.isnan(self.radios[:, i_slice, :])] = 0
        self.radios_slim.set(self.radios[:, i_slice, :])

    def _register_callbacks(self):
        pass

    #
    # Pipeline execution (class specialization)
    #

    @pipeline_step("histogram", "Computing histogram")
    def _compute_histogram(self, data=None):
        if data is None:
            data = self._d_recs
        self.recs_histogram = self.histogram.compute_histogram(data)

    def _dump_data_to_file(self, step_name, data=None):
        if data is None:
            data = self.radios
        if step_name not in self._data_dump:
            return
        if isinstance(data, garray.GPUArray):
            data = data.get()
        super()._dump_data_to_file(step_name, data=data)
