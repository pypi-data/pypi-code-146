# fmt: off
# This file is automatically generated, DO NOT EDIT

from os.path import abspath, join, dirname
_root = abspath(dirname(__file__))

libinit_import = "ctre._init_ctre"
depends = ['wpiutil', 'wpinet', 'wpimath_cpp', 'wpiHal', 'ntcore', 'wpilibc', 'ctre_wpiapi_cpp_sim', 'ctre_api_cpp_sim', 'ctre_cci_sim', 'ctre_tools_sim', 'ctre_simtalonsrx', 'ctre_simtalonfx', 'ctre_simvictorspx', 'ctre_simpigeonimu', 'ctre_simcancoder', 'ctre_simprotalonfx', 'ctre_simprocancoder', 'ctre_simpropigeon2']
pypi_package = 'robotpy-ctre'

def get_include_dirs():
    return [join(_root, "include"), join(_root, "rpy-include")]

def get_library_dirs():
    return []

def get_library_dirs_rel():
    return []

def get_library_names():
    return []

def get_library_full_names():
    return []