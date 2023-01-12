from importlib import import_module


def absolute_component_factory_module(module_path: str):
    return import_module(f"{module_path}.service")
