from ...preproc.ccd_cuda import CudaLog, CudaCCDFilter
from ...preproc.flatfield_cuda import CudaFlatFieldDataUrls
from ...preproc.shift_cuda import CudaVerticalShift
from ...preproc.double_flatfield_cuda import CudaDoubleFlatField
from ...preproc.phase_cuda import CudaPaganinPhaseRetrieval
from ...preproc.ctf_cuda import CudaCTFPhaseRetrieval
from ...reconstruction.sinogram_cuda import CudaSinoBuilder, CudaSinoNormalization
from ...reconstruction.rings_cuda import CudaMunchDeringer
from ...misc.unsharp_cuda import CudaUnsharpMask
from ...misc.rotation_cuda import CudaRotation
from ...misc.histogram_cuda import CudaPartialHistogram
from ...reconstruction.fbp import Backprojector
from ...reconstruction.cone import __have_astra__, ConebeamReconstructor
from ...cuda.utils import get_cuda_context, __has_pycuda__, __pycuda_error_msg__
from ..utils import pipeline_step
from .chunked import ChunkedPipeline

if __has_pycuda__:
    import pycuda.gpuarray as garray
if not (__have_astra__):
    ConebeamReconstructor = None


class CudaChunkedPipeline(ChunkedPipeline):
    """
    Cuda backend of ChunkedPipeline
    """

    backend = "cuda"
    FlatFieldClass = CudaFlatFieldDataUrls
    DoubleFlatFieldClass = CudaDoubleFlatField
    CCDCorrectionClass = CudaCCDFilter
    PaganinPhaseRetrievalClass = CudaPaganinPhaseRetrieval
    CTFPhaseRetrievalClass = CudaCTFPhaseRetrieval
    UnsharpMaskClass = CudaUnsharpMask
    ImageRotationClass = CudaRotation
    VerticalShiftClass = CudaVerticalShift
    SinoDeringerClass = CudaMunchDeringer
    MLogClass = CudaLog
    SinoBuilderClass = CudaSinoBuilder
    FBPClass = Backprojector
    ConebeamClass = ConebeamReconstructor
    HistogramClass = CudaPartialHistogram
    SinoNormalizationClass = CudaSinoNormalization

    def __init__(self, process_config, chunk_shape, logger=None, extra_options=None, margin=None, cuda_options=None):
        self._init_cuda(cuda_options)
        super().__init__(process_config, chunk_shape, logger=logger, extra_options=extra_options, margin=margin)
        self._allocate_array(self.radios.shape, "f", name="radios")

    def _init_cuda(self, cuda_options):
        if not (__has_pycuda__):
            raise ImportError(__pycuda_error_msg__)
        cuda_options = cuda_options or {}
        self.ctx = get_cuda_context(**cuda_options)
        self._d_radios = None
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

    def _transfer_radios_to_gpu(self):
        self._d_radios.set(self.radios)
        self._h_radios = self.radios
        self.radios = self._d_radios

    def _process_finalize(self):
        self.radios = self._h_radios

    #
    # Pipeline execution (class specialization)
    #

    def _read_data(self):
        super()._read_data()
        self.logger.debug("Transfering radios to GPU")
        self._transfer_radios_to_gpu()

    def _reconstruct(self):
        super()._reconstruct()
        if "reconstruction" not in self.processing_steps:
            return
        if self.processing_options["reconstruction"]["method"] == "cone":
            ((U, D), (L, R)) = self.margin
            U, D = U or None, -D or None
            # not sure why slicing can't be done before get()
            self.recs = self.recs.get()[U:D, ...]
        else:
            self.recs = self.recs.get()

    def _write_data(self, data=None):
        super()._write_data(data=data)
        if "reconstruction" in self.processing_steps:
            self.recs = self._d_recs
        self.radios = self._h_radios

    @pipeline_step("histogram", "Computing histogram")
    def _compute_histogram(self, data=None):
        if data is None:
            data = self._d_recs
        self.recs_histogram = self.histogram.compute_histogram(data)

    def _dump_data_to_file(self, step_name, data=None):
        if data is None:
            data = self.radios
        if step_name not in self.datadump_manager.data_dump:
            return
        if isinstance(data, garray.GPUArray):
            data = data.get()
        self.datadump_manager.dump_data_to_file(step_name, data=data)
