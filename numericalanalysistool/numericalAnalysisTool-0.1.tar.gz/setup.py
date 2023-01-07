#!/usr/bin/env python

from distutils.core import setup

setup(name='numericalAnalysisTool',
      version='0.1',
      description='Numerical anlysis tool',
      author='Clément Dutriez',
      author_email='clement.dutriez@u-pem.fr',
      url='https://github.com/CafeKrem/pyNumericalAnlysis',
      packages=['numericalAnalysis'],
      long_description=open('README.rst').read(),
     )