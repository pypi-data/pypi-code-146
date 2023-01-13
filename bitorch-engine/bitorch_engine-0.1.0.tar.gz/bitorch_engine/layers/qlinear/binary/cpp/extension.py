from pathlib import Path

from bitorch_engine.utils.cpp_extension import get_cpp_extension


def get_ext(path: Path):
    return get_cpp_extension(
        path,
        relative_name='binary_linear_cpp',
        relative_sources=['binary_linear.cpp']
    )
