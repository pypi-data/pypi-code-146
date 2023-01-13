from pathlib import Path
from typing import Dict, Any

from torch.utils.cpp_extension import CppExtension, IS_MACOS

from bitorch_engine.extensions import EXTENSION_PREFIX


def get_cpp_extension(root_path: Path, relative_name: str, relative_sources) -> Any:
    return CppExtension(
        name=EXTENSION_PREFIX + relative_name,
        sources=[str(root_path / rel_path) for rel_path in relative_sources],
        **get_kwargs()
    )


def get_kwargs() -> Dict[str, Any]:
    return {
        "include_dirs": [
            "/usr/local/opt/llvm/include",
        ],
        "libraries": [
            "omp" if IS_MACOS else "gomp",
        ],
        "extra_compile_args": [
            '-Wall',
            '-Wno-deprecated-register',
            '-Xpreprocessor',
            '-fopenmp',
        ]
    }
