# fmt: off
# This file is automatically generated, DO NOT EDIT

from os.path import abspath, join, dirname
_root = abspath(dirname(__file__))

libinit_import = "playingwithfusion._init_playingwithfusion"
depends = ['wpilibc', 'wpilib_core', 'wpiutil', 'playingwithfusion_driver']
pypi_package = 'robotpy-playingwithfusion'

def get_include_dirs():
    return [join(_root, "include"), join(_root, "rpy-include")]

def get_library_dirs():
    return [join(_root, "lib")]

def get_library_dirs_rel():
    return ['lib']

def get_library_names():
    return ['PlayingWithFusion']

def get_library_full_names():
    return ['libPlayingWithFusion.dylib']