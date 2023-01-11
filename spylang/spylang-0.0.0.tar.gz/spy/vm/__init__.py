"""
Very simple VM to execute the SPY IR.
"""

from dataclasses import dataclass
from spy import ir
from spy.vm.typesystem import wt, W_Type
from spy.vm.objects import W_Root, W_Function, W_Module
from spy.vm.primitive import W_Primitive

def meta_eval(w_mod):
    """
    Perform the meta-eval phase on the given module.
    """
    vm = SPyVM(w_mod)
    return vm.meta_eval_module(w_mod)


class Frame:

    def __init__(self):
        self.locals = {}

    def set(self, name, value):
        assert isinstance(value, W_Root)
        self.locals[name] = value

    def get(self, name):
        return self.locals[name]


class SPyVM:
    """
    A Virtual Machine to execute SPy code.
    """

    def __init__(self, w_mod):
        # XXX: here we are assuming that there is only a single module inside
        # a VM. This is fine for now, but we need a better model.
        self.w_mod = w_mod

    def wrap(self, value):
        """
        Useful for tests: magic funtion which wraps the given value into the most
        appropriate W_* object.
        """
        # only i32 is supported for now
        assert isinstance(value, int)
        return W_Primitive(wt.i32, value)

    def new_frame(self):
        return Frame()

    def get_w_function(self, name):
        return self.w_mod.lookup(name)

    def meta_eval_module(self, w_mod):
        """
        Run the meta-time parts of w_mod, and return another partially-evaluated w_mod
        """
        funcs_w = w_mod._functions_w.values()
        funcs_w2 = [w_f.vm_meta_eval(self) for w_f in funcs_w]
        w_mod2 = W_Module(w_mod._name)
        for w_func in funcs_w2:
            w_mod2.add(w_func)
        return w_mod2
