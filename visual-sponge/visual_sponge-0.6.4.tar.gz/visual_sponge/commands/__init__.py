from pathlib import Path
from importlib import import_module


__all__ = []

for file in Path(__file__).parent.glob("*.py"):
    module_name = file.stem
    MODULE_NAME = str(module_name).upper()
    if module_name != "__init__":
        module = import_module(f"{__name__}.{module_name}")
        __all__.append(MODULE_NAME)
        globals()[MODULE_NAME] = getattr(module, str(MODULE_NAME))
