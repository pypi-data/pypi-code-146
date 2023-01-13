#! /usr/bin/env python3
# -*- coding:Utf8 -*-

import os
import sys

from distutils.command.build_ext import build_ext
from distutils.core import Extension
from distutils.errors import CCompilerError
from distutils.errors import DistutilsExecError
from distutils.errors import DistutilsPlatformError

# Need packet_structure from roc.rpl plugin
from roc.rpl import packet_structure

# import numpy and cython
from Cython.Build import cythonize
import numpy

RPL_PACKET_STRUCTURE_PATH = os.path.dirname(packet_structure.__file__)

# C Extensions
with_extensions = os.getenv("RAP_EXTENSIONS", None)

if with_extensions == "1" or with_extensions is None:
    with_extensions = True

if with_extensions == "0" or hasattr(sys, "pypy_version_info"):
    with_extensions = False

extensions = []
if with_extensions:
    extensions = list()
    extensions += cythonize(Extension(
        name='*',
        sources=['roc/rap/tasks/thr/*.pyx'],
        include_dirs=[numpy.get_include(), RPL_PACKET_STRUCTURE_PATH]))

    extensions += cythonize(Extension(
        name='*',
        sources=['roc/rap/tasks/lfr/*.pyx'],
        include_dirs=[numpy.get_include(), RPL_PACKET_STRUCTURE_PATH]))

    extensions += cythonize(Extension(
        name='*',
        sources=['roc/rap/tasks/tds/*.pyx'],
        include_dirs=[numpy.get_include(), RPL_PACKET_STRUCTURE_PATH]))


class BuildFailed(Exception):

    pass


class ExtBuilder(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            print("************************************************************")
            print("Cannot compile RAP Cython module!")
            print("************************************************************")

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError, ValueError):
            print("************************************************************")
            print("Cannot compile Cython module!")
            print("************************************************************")


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update(
        {"ext_modules": extensions, "cmdclass": {"build_ext": ExtBuilder}}
    )
