from pathlib import Path

from bitorch_engine.utils.cuda_extension import get_cuda_extension

CUDA_REQUIRED = True


def get_ext(path: Path):
    return get_cuda_extension(
        path,
        relative_name='bcompressed_embedding_bag_cuda',
        relative_sources=[
            'bcompressed_embedding_bag_cuda.cpp',
            'bcompressed_embedding_bag_cuda_kernel.cu',
        ],
    )
