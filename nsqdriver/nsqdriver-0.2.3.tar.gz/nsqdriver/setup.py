from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy as np


extension = [Extension("*", ["nsqdriver/wrapper/*.py"], language='c++'),
             Extension("*", ["nsqdriver/*.py"], language='c++')]

setup(
    name='nsqdriver',
    ext_modules=cythonize(extension, language_level=3),
    include_path=[np.get_include()]
)
