from pathlib import Path

from bitorch_engine.utils.cuda_extension import get_cuda_extension

CUDA_REQUIRED = True
CUTLASS_REQUIRED = True


def get_ext(path: Path):
    return get_cuda_extension(
        path,
        relative_name='q4_conv_cutlass',
        relative_sources=[
            'q4_conv_cutlass.cpp',
            'q4_conv_cutlass_kernel.cu',
        ]
    )
