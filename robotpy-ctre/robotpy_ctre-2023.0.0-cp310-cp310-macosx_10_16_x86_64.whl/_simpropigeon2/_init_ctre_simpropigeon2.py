# This file is automatically generated, DO NOT EDIT
# fmt: off

from os.path import abspath, join, dirname, exists
_root = abspath(dirname(__file__))


from ctypes import cdll

try:
    _lib = cdll.LoadLibrary(join(_root, "lib", "libCTRE_SimProPigeon2.dylib"))
except FileNotFoundError:
    if not exists(join(_root, "lib", "libCTRE_SimProPigeon2.dylib")):
        raise FileNotFoundError("libCTRE_SimProPigeon2.dylib was not found on your system. Is this package correctly installed?")
    raise FileNotFoundError("libCTRE_SimProPigeon2.dylib could not be loaded. There is a missing dependency.")

