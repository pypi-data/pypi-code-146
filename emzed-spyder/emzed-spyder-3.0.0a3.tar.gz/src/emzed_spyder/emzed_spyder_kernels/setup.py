from __future__ import print_function

from setuptools import setup

setup(
    version="0.0.3",
    name="emzed-spyder-kernels",
    py_modules=["emzed_spyder_kernels"],
    install_requires=["spyder-kernels==1.9.1"],
    include_package_data=True,
)
