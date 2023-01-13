from pathlib import Path

from bitorch_engine.utils.cuda_extension import get_cuda_extension

CUDA_REQUIRED = True
CUTLASS_REQUIRED = True


def get_ext(path: Path):
    return get_cuda_extension(
        path,
        relative_name='binary_linear_cutlass',
        relative_sources=[
            'binary_linear_cutlass.cpp',
            'binary_linear_cutlass_kernel.cu',
        ]
    )
