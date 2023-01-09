from __future__ import annotations

from typing import Any

from pybind11.setup_helpers import Pybind11Extension, build_ext


def build(setup_kwargs: dict[Any, Any]) -> None:
    ext_modules = [
        Pybind11Extension(
            "modelbase_pde.utils._perffuncs",
            ["src/modelbase_pde/utils/perffuncs.cpp"],
        ),
    ]
    setup_kwargs.update(
        {
            "ext_modules": ext_modules,
            "cmd_class": {"build_ext": build_ext},
            "zip_safe": False,
        }
    )
