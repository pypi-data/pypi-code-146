import os, sys

from distutils.core import setup, Extension
from distutils import sysconfig
# specify the path of pybind header file and funcs.hpp
# cpp_args = ["-I./"]
cpp_args = ["/std:c++20"]

ext_modules = [
  Extension(
    'wcap_core',
    ['func.cpp'],
    include_dirs=['pybind11/include'],
    language='c++',
    extra_compile_args=cpp_args,
  ),
]
setup(
  name='window-capture-audio-py',
  version='0.0.3',
  author='zzqq2199',
  author_email="zhouquanjs@qq.com",
  packages=["wcap"],
  description='Get audio data from specified window.',
  ext_modules=ext_modules,
  install_requires=['numpy'],
  python_requires='>=3.9'
)