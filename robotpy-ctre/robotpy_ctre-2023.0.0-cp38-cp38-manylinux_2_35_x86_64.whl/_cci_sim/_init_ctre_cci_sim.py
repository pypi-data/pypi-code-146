# This file is automatically generated, DO NOT EDIT
# fmt: off

from os.path import abspath, join, dirname, exists
_root = abspath(dirname(__file__))

# runtime dependencies
import ctre._tools_sim._init_ctre_tools_sim
from ctypes import cdll

try:
    _lib = cdll.LoadLibrary(join(_root, "lib", "libCTRE_PhoenixCCISim.so"))
except FileNotFoundError:
    if not exists(join(_root, "lib", "libCTRE_PhoenixCCISim.so")):
        raise FileNotFoundError("libCTRE_PhoenixCCISim.so was not found on your system. Is this package correctly installed?")
    raise FileNotFoundError("libCTRE_PhoenixCCISim.so could not be loaded. There is a missing dependency.")

