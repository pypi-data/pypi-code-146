from __future__ import annotations

import functools
import importlib
import os
import sys
import yaml

from .default_generator import DefaultGenerator


__all__ = ("load_manifest", "get_secrets_generator")


def _list_parent_dirs() -> list[str]:
    dirs = []
    parts = os.path.dirname(os.path.abspath(os.getcwd())).split("/")
    while parts:
        dirs.append("/".join(parts))
        parts.pop()
    dirs.append("")
    return dirs


@functools.lru_cache
def load_manifest():
    task_name = os.environ.get("TASK_NAME")
    for dir_path in ["/task", "."] + _list_parent_dirs():
        if task_name:
            file_path = f"{dir_path}/{task_name}.yaml"
        else:
            file_path = f"{dir_path}/{os.path.basename(dir_path)}.yaml"
        if not os.path.exists(file_path):
            continue
        with open(file_path) as f:
            return yaml.unsafe_load(f)
    return None


@functools.lru_cache
def get_secrets_generator():
    for dir_path in ["/task", "/controller"] + _list_parent_dirs():
        location = f"{dir_path}/secrets_generator.py"
        if os.path.exists(location):
            spec = importlib.util.spec_from_file_location("secrets_generator", location)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            return module

    manifest = load_manifest()
    if manifest is not None and "secrets" in manifest:
        return DefaultGenerator(manifest["secrets"])

    raise ValueError("Secrets generator is not found at common locations")
