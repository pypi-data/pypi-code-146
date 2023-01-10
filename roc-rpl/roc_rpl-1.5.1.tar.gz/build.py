#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob

from distutils.command.build_ext import build_ext
from distutils.core import Extension
from distutils.errors import CCompilerError
from distutils.errors import DistutilsExecError
from distutils.errors import DistutilsPlatformError

# import numpy and cython
from Cython.Build import cythonize
import numpy

# the path for rice module and rpl
RICE_PATH = os.path.join('roc', 'rpl', 'rice')

# path to packet_structure for PacketParser
RPL_PACKET_STRUCTURE_PATH = os.path.join('roc', 'rpl', 'packet_structure')

# Path to packet_parser
RPL_PACKET_PARSER_PATH = os.path.join('roc', 'rpl', 'packet_parser', 'parser')

# C Extensions
with_extensions = os.getenv('RPL_EXTENSIONS', None)

if with_extensions == '1' or with_extensions is None:
    with_extensions = True

if with_extensions == '0' or hasattr(sys, 'pypy_version_info'):
    with_extensions = False

extensions = []
if with_extensions:
    extensions = list()
    extensions += cythonize(
        Extension(
            'roc.rpl.packet_structure.header',
            ['roc/rpl/packet_structure/header.pyx', 'roc/rpl/packet_structure/type_conversion.c'],
            include_dirs=[numpy.get_include(), RPL_PACKET_STRUCTURE_PATH],
        ),
    )
    extensions += cythonize(
        Extension(
            'roc.rpl.packet_structure.parameter',
            ['roc/rpl/packet_structure/parameter.pyx', 'roc/rpl/packet_structure/type_conversion.c'],
            include_dirs=[numpy.get_include(), RPL_PACKET_STRUCTURE_PATH],
        ),
    )
    extensions += cythonize(
        Extension(
            'roc.rpl.packet_structure.data',
            ['roc/rpl/packet_structure/data.pyx', 'roc/rpl/packet_structure/type_conversion.c'],
            include_dirs=[numpy.get_include(), RPL_PACKET_STRUCTURE_PATH],
        ),
    )
    extensions += cythonize(
        Extension(
            'roc.rpl.packet_parser.parser.identify_packets',
            sources=['roc/rpl/packet_parser/parser/identify_packets.pyx',
                     'roc/rpl/packet_structure/type_conversion.c'],
            include_dirs=[numpy.get_include(), RPL_PACKET_PARSER_PATH,
                          RPL_PACKET_STRUCTURE_PATH]
        ),
    )
    extensions += cythonize(
        Extension(
            'roc.rpl.packet_parser.parser.parse_packets',
            sources=['roc/rpl/packet_parser/parser/parse_packets.pyx',
                     'roc/rpl/packet_structure/type_conversion.c'],
            include_dirs=[numpy.get_include(), RPL_PACKET_PARSER_PATH,
                          RPL_PACKET_STRUCTURE_PATH]
        ),
    )

    # now add an extension for compiling the rice compression library
    extensions += cythonize(
        Extension(
            'roc.rpl.rice.rice',  # this will be the name of the module
            sources=[os.path.join(RICE_PATH, 'rice.pyx')] +
                    [fn for fn in glob.glob(os.path.join(RICE_PATH, '*.cpp'))
                     if not os.path.basename(fn) == 'rice.cpp'],
            include_dirs=[numpy.get_include(), RICE_PATH, RPL_PACKET_STRUCTURE_PATH],
            language='c++',
            define_macros=[('GAUSS', '1')],
        )
    )


class BuildFailed(Exception):

    pass


class ExtBuilder(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            print('************************************************************')
            print('Cannot compile RPL Cython module!')
            print('************************************************************')

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError, ValueError):
            print('************************************************************')
            print('Cannot compile Cython module!')
            print('************************************************************')


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update(
        {'ext_modules': extensions, 'cmdclass': {'build_ext': ExtBuilder}}
    )
