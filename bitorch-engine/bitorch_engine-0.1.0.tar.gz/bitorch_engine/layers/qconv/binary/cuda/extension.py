from pathlib import Path

from bitorch_engine.utils.cuda_extension import get_cuda_extension

CUDA_REQUIRED = True


def get_ext(path: Path):
    return get_cuda_extension(
        path,
        relative_name='binary_conv_cuda',
        relative_sources=[
            'binary_conv_cuda.cpp',
            'binary_conv_cuda_kernel.cu',
        ]
    )
