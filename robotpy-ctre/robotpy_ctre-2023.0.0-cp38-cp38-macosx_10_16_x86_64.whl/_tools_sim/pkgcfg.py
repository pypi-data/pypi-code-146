# fmt: off
# This file is automatically generated, DO NOT EDIT

from os.path import abspath, join, dirname
_root = abspath(dirname(__file__))

libinit_import = "ctre._tools_sim._init_ctre_tools_sim"
depends = ['ctre_simpropigeon2', 'ctre_simprocancoder', 'ctre_simprotalonfx', 'ctre_simcancoder', 'ctre_simtalonfx', 'ctre_simpigeonimu', 'ctre_simtalonsrx', 'ctre_simvictorspx']
pypi_package = 'robotpy-ctre'

def get_include_dirs():
    return [join(_root, "include"), join(_root, "rpy-include")]

def get_library_dirs():
    return [join(_root, "lib")]

def get_library_dirs_rel():
    return ['lib']

def get_library_names():
    return ['CTRE_PhoenixTools_Sim']

def get_library_full_names():
    return ['libCTRE_PhoenixTools_Sim.dylib']