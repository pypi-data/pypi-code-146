import os
import pytest
import textwrap
import sexpdata
from spy import parser
from spy.vm import SPyVM, meta_eval
from spy.backend import compile_module_to_wat
import wasmtime

def spy_parse(src):
    return parser.parse(textwrap.dedent(src))

def sexp_equal(a, b):
    """
    Compare two sexp, ignoring whitespaces
    """
    sa = sexpdata.parse(a)
    sb = sexpdata.parse(b)
    return sa == sb


class InterpModuleWrapper:

    def __init__(self, w_mod):
        self._vm = SPyVM(w_mod)
        for name, w_func in self._vm.w_mod._functions_w.items():
            func_wrapper = InterpFuncWrapper(self._vm, w_func)
            setattr(self, name, func_wrapper)

class InterpFuncWrapper:

    def __init__(self, vm, w_func):
        self._vm = vm
        self._w_func = w_func

    def __call__(self, *args):
        # *args contains python-level objs. We want to wrap them into args_w
        # *and to call the func, and unwrap the result
        args_w = [self._vm.wrap(arg) for arg in args]
        w_res = self._w_func.call(self._vm, args_w)
        t, val = w_res.unwrap()
        return val


class WasmModuleWrapper:

    def __init__(self, w_mod, wasmfile):
        store = wasmtime.Store()
        module = wasmtime.Module.from_file(store.engine, wasmfile)
        instance = wasmtime.Instance(store, module, [])
        exports = instance.exports(store)
        for name, wasm_func in exports._extern_map.items():
            wasm_func_wrapper = WasmFuncWrapper(store, wasm_func)
            setattr(self, name, wasm_func_wrapper)

class WasmFuncWrapper:

    def __init__(self, store, wasm_func):
        self._store = store
        self._wasm_func = wasm_func

    def __call__(self, *args):
        return self._wasm_func(self._store, *args)


@pytest.mark.usefixtures('init')
class SPyTest:

    @pytest.fixture(params=['interp', 'meta', 'wasm'])
    def spy_eval_strategy(self, request):
        """
        Each test is run 3 times, with different eval strategies:

          - interp: the whole module is interpreted as is

          - meta: the module is partially evaluated, and then interpreted

          - wasm: the module is partially evaluated, then compiled to wasm,
            then executed by wasmtime
        """
        return request.param

    @pytest.fixture
    def init(self, tmpdir, spy_eval_strategy):
        self.tmpdir = tmpdir
        self.spy_eval_strategy = spy_eval_strategy

    def parse(self, src):
        """
        Parse the given source code and return a w_mod
        """
        return spy_parse(src)

    def compile(self, src):
        w_mod = self.parse(src)
        if self.spy_eval_strategy == 'interp':
            return InterpModuleWrapper(w_mod)
        elif self.spy_eval_strategy == 'meta':
            w_mod2 = meta_eval(w_mod)
            return InterpModuleWrapper(w_mod2)
        elif self.spy_eval_strategy == 'wasm':
            w_mod2 = meta_eval(w_mod)
            wasmfile = self._compile_wasm(w_mod2)
            return WasmModuleWrapper(w_mod, wasmfile)
        else:
            assert False

    def _compile_wasm(self, w_mod):
        wat = compile_module_to_wat(w_mod)
        watfile = self.tmpdir.join('mymod.wat')
        wasmfile = self.tmpdir.join('mymod.wasm')
        watfile.write(wat)
        ret = os.system(f'wat2wasm {watfile} -o {wasmfile}')
        assert ret == 0
        return wasmfile
