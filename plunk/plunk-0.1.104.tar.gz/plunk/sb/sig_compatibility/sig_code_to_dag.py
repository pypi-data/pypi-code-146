from i2 import Sig


def is_compatible(func, new_sig):
    sig = Sig(func)
    return sig.is_call_compatible_with(new_sig)
