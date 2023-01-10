#!/usr/bin/python3

from setuptools import setup
import os

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'ethercram', '__version__.py')) as f:
    exec(f.read(), about)

setup(version=about['__version__'])
