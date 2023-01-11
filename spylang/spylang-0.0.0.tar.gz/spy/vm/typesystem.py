"""
SPY Typesystem.

The classes in this module represents the types which are attached to the IR
expressions and to the runtime value used by the VM.

Naming convention: instances of subclasses of W_Type are called wt_* ("wrapped
typed"). I.e.:

    w_foo = ...
    wt_foo = vm.typeof(w_value)
"""

from dataclasses import dataclass
from spy.vm.objects import W_Root

class W_Type(W_Root):
    pass

@dataclass
class W_PrimitiveType(W_Type):
    name: str

@dataclass
class W_FunctionType(W_Type):
    args_wt: list  # List[W_Type]
    wt_return: W_Type

    @property
    def n_args(self):
        return len(self.args_wt)


class wt:
    """
    This is not a real class: just a namespace to contain prebuilt types such as i32.

    Note the exception to the naming convention: since the namespace is
    already called "wt", there is no need to repeat the wt_ prefix for the
    individual fields.  We expect the rest of the code to use e.g. wt.i32
    """

    i32 = W_PrimitiveType('i32')

    @staticmethod
    def function(args_wt, wt_return):
        return W_FunctionType(args_wt, wt_return)
