# This file is automatically generated, DO NOT EDIT
# fmt: off

from os.path import abspath, join, dirname, exists
_root = abspath(dirname(__file__))

# runtime dependencies
import ctre._simpropigeon2._init_ctre_simpropigeon2
import ctre._simprocancoder._init_ctre_simprocancoder
import ctre._simprotalonfx._init_ctre_simprotalonfx
import ctre._simcancoder._init_ctre_simcancoder
import ctre._simtalonfx._init_ctre_simtalonfx
import ctre._simpigeonimu._init_ctre_simpigeonimu
import ctre._simtalonsrx._init_ctre_simtalonsrx
import ctre._simvictorspx._init_ctre_simvictorspx
from ctypes import cdll

try:
    _lib = cdll.LoadLibrary(join(_root, "lib", "libCTRE_PhoenixTools_Sim.dylib"))
except FileNotFoundError:
    if not exists(join(_root, "lib", "libCTRE_PhoenixTools_Sim.dylib")):
        raise FileNotFoundError("libCTRE_PhoenixTools_Sim.dylib was not found on your system. Is this package correctly installed?")
    raise FileNotFoundError("libCTRE_PhoenixTools_Sim.dylib could not be loaded. There is a missing dependency.")

