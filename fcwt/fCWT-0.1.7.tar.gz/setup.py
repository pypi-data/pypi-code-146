#!/usr/bin/env python

"""
setup.py file for SWIG
"""

from setuptools import Extension, setup
import sysconfig
import numpy


# Obtain the numpy include directory.  This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()
    

libraries = ['fftw3f-win']
comp_args = ["/arch:AVX","/O2","/openmp"]
link_args = []
files = ["omp.h","fcwt.h","fftw3.h","fftw3f-win.dll","fftw3f-win.lib","libfftw3f-mac.a","libfftw3f_omp-mac.a","libomp.a","libfftw3f-linux.so","libfftw3f_omp-linux.so"]

if "macosx" in sysconfig.get_platform() or "darwin" in sysconfig.get_platform():
    libraries = ['fftw3f-mac','fftw3f_omp-mac']
    comp_args = ["-mavx","-O3"]
    link_args = ["-lomp"]

if "linux" in sysconfig.get_platform():
    libraries = ['fftw3f-linux','fftw3f_omp-linux']
    comp_args = ["-mavx","-O3"]
    link_args = ["-lomp"]

  

setup (ext_modules=[
            Extension('fcwt._fcwt',
                sources=[
                    'src/fcwt/fcwt.cpp',
                    'src/fcwt/fcwt_wrap.cxx'
                ],
                library_dirs = ['src/fcwt'],
                include_dirs = ['src/fcwt',numpy_include],
                libraries = libraries,
                extra_compile_args = comp_args,
                extra_link_args = link_args
            )
        ],
        package_data={'fcwt':files}
        )

#swig -c++ -python fcwt-swig.i