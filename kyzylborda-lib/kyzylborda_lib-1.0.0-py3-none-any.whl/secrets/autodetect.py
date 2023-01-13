import functools
import importlib
import os
import sys
import yaml

from .default_generator import DefaultGenerator


__all__ = ("load_manifest", "get_secrets_generator")


@functools.lru_cache
def load_manifest():
    if "TASK_NAME" not in os.environ:
        return None
    task_name = os.environ["TASK_NAME"]
    for file_path in [f"/task/{task_name}.yaml", f"./{task_name}.yaml"]:
        if not os.path.exists(file_path):
            continue
        with open(file_path) as f:
            return yaml.unsafe_load(f)
    return None


@functools.lru_cache
def get_secrets_generator():
    for location in ["/task/secrets_generator.py", "/controller/secrets_generator.py", "./secrets_generator.py"]:
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
