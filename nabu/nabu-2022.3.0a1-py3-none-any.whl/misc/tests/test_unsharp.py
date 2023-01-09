import numpy as np
import pytest
from scipy.misc import ascent
from nabu.misc.unsharp import UnsharpMask
from nabu.misc.unsharp_opencl import OpenclUnsharpMask, __have_opencl__ as __has_pyopencl__
from nabu.cuda.utils import __has_pycuda__, get_cuda_context

if __has_pyopencl__:
    from pyopencl import CommandQueue
    import pyopencl.array as parray
    from silx.opencl.common import ocl
if __has_pycuda__:
    import pycuda.gpuarray as garray
    from nabu.misc.unsharp_cuda import CudaUnsharpMask


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.data = np.ascontiguousarray(ascent()[:, :511], dtype=np.float32)
    cls.tol = 1e-4
    cls.sigma = 1.6
    cls.coeff = 0.5
    if __has_pycuda__:
        cls.ctx = get_cuda_context(cleanup_at_exit=False)
    if __has_pyopencl__:
        cls.cl_ctx = ocl.create_context()
    yield
    if __has_pycuda__:
        cls.ctx.pop()


@pytest.mark.usefixtures("bootstrap")
class TestUnsharp:
    def get_reference_result(self, method, data=None):
        if data is None:
            data = self.data
        unsharp_mask = UnsharpMask(data.shape, self.sigma, self.coeff, method=method)
        return unsharp_mask.unsharp(data)

    def check_result(self, result, method, data=None, error_msg_prefix=None):
        reference = self.get_reference_result(method, data=data)
        mae = np.max(np.abs(result - reference))
        err_msg = str(
            "%s: max error is too high with method=%s: %.2e > %.2e" % (error_msg_prefix or "", method, mae, self.tol)
        )
        assert mae < self.tol, err_msg

    @pytest.mark.skipif(not (__has_pyopencl__), reason="Need pyopencl for this test")
    def testOpenclUnsharp(self):
        cl_queue = CommandQueue(self.cl_ctx)
        d_image = parray.to_device(cl_queue, self.data)
        d_out = parray.zeros_like(d_image)
        for method in OpenclUnsharpMask.avail_methods:
            d_image = parray.to_device(cl_queue, self.data)
            d_out = parray.zeros_like(d_image)

            opencl_unsharp = OpenclUnsharpMask(self.data.shape, self.sigma, self.coeff, method=method, ctx=self.cl_ctx)
            opencl_unsharp.unsharp(d_image, output=d_out)
            res = d_out.get()
            self.check_result(res, method, error_msg_prefix="OpenclUnsharpMask")

    @pytest.mark.skipif(not (__has_pycuda__), reason="Need cuda/pycuda for this test")
    def testCudaUnsharp(self):
        d_image = garray.to_gpu(self.data)
        d_out = garray.zeros_like(d_image)
        for method in CudaUnsharpMask.avail_methods:
            cuda_unsharp = CudaUnsharpMask(
                self.data.shape, self.sigma, self.coeff, method=method, cuda_options={"ctx": self.ctx}
            )
            cuda_unsharp.unsharp(d_image, output=d_out)
            res = d_out.get()
            self.check_result(res, method, error_msg_prefix="CudaUnsharpMask")
