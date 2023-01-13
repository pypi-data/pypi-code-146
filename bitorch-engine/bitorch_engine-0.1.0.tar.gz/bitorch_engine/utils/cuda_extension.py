import os
import subprocess
from pathlib import Path
from typing import Dict, Any

from torch.utils.cpp_extension import CUDAExtension

from bitorch_engine.extensions import EXTENSION_PREFIX


def get_cuda_extension(root_path: Path, relative_name: str, relative_sources) -> Any:
    return CUDAExtension(
        name=EXTENSION_PREFIX + relative_name,
        sources=[str(root_path / rel_path) for rel_path in relative_sources],
        **get_kwargs()
    )


def gcc_version():
    output = subprocess.run(['gcc', '--version'], check=True, capture_output=True, text=True)
    if output.returncode > 0 or "clang" in output.stdout:
        return 0, 0, 0
    first_line = output.stdout.split("\n")[0]
    version = first_line.split(" ")[-1]
    major, minor, patch = list(map(int, version.split(".")))
    return major, minor, patch


def get_kwargs() -> Dict[str, Any]:
    major, minor, patch = gcc_version()
    kwargs = {
        "extra_compile_args": {
            "cxx": [
                "-Wno-deprecated-declarations",
                "-L/usr/lib/gcc/x86_64-pc-linux-gnu/10.3.0/libgomp.so",
                "-fopenmp",
            ],
            "nvcc": [
                "-Xcompiler",
                "-fopenmp",
                f"-arch={os.environ.get('BIE_CUDA_ARCH', 'sm_80')}",
            ],
        },
    }
    if major > 11:
        print("Using GCC 11 host compiler for nvcc.")
        kwargs["extra_compile_args"]["nvcc"].append("-ccbin=/usr/bin/gcc-11")
    return kwargs
