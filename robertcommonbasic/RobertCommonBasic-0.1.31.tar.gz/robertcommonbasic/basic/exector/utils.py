import sys
import importlib.util as lib_util
from importlib import import_module
from bson import ObjectId
from dataclasses import dataclass, field
from io import StringIO
from types import ModuleType
from typing import List, Optional


@dataclass(frozen=True)
class Code:

    class PatchStd:

        def __init__(self):
            self._out = sys.stdout
            self.out = StringIO()
            self.value = ""

        def _print(self, *args):
            print(*args, file=self._out)

        def __enter__(self):
            sys.stdout = self.out
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout = self._out
            self.value = self.out.getvalue()
            del self.out

    code_content: str = field(default="", repr=False)   # 代码
    code_with_run: bool = field(default=True)   # 代码是否自动运行
    module_name: str = field(default=f"module_{ObjectId().__str__()}")  # 模块名称
    lib_module: Optional[ModuleType] = field(default=None, repr=False)  # 模块

    def __post_init__(self):
        if self.code_content != "":
            object.__setattr__(self, "lib_module", self.import_dmod(self.module_name, self.functionalise_src(self.code_content)))
        else:
            raise Exception(f"Source code is missing.")

        self.validate_properties(self.lib_module, ["func_default"] if self.code_with_run else [])

    def run_func_default(self):
        result = None
        with self.PatchStd() as std:
            if hasattr(self.lib_module, 'func_default'):
                result = self.lib_module.func_default()
        if len(std.value) > 0:
            print(std.value)
        return result

    def run_func(self, func_name: Optional[str] = None, *args, **kwargs):
        result = None
        with self.PatchStd() as std:
            if hasattr(self.lib_module, func_name):
                result = self.lib_module.__getattribute__(func_name)(*args, **kwargs)
            else:
                raise Exception(f"no function({func_name})")
        if len(std.value) > 0:
            print(std.value)
        return result

    def run_code(self, func_name: Optional[str] = None, *args, **kwargs):
        if self.code_with_run:
            return self.run_func_default()
        else:
            return self.run_func(func_name, *args, *kwargs)

    def validate_properties(self, module: ModuleType, properties: List[str]):
        for prop in properties:
            if not hasattr(module, prop):
                raise Exception(f"Property {prop} is missing.")

    def functionalise_src(self, src: str) -> str:
        if self.code_with_run is True:
            return f"""def func_default():\n\t""" + src.replace("\n", "\n\t")
        else:
            return src

    def import_dmod(self, module_name: str, code_content: str) -> ModuleType:
        spec = lib_util.spec_from_loader(module_name, loader=None)
        module = None
        try:
            module = lib_util.module_from_spec(spec)
            exec(code_content, module.__dict__)
        except Exception as E:
            module = lib_util.module_from_spec(spec)
            _src = self.functionalise_src(f'print("""{repr(E)}""")')
            exec(_src, module.__dict__)
        return module

    def save_module_to_file(self, code_content: str, module_name: str) -> None:
        with open(module_name + ".py", "w") as f:
            f.write(code_content)

    def import_file(self, mod_name: str) -> ModuleType:
        return import_module(mod_name)
