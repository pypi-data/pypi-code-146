#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-module-docstring,exec-used

import setuptools


with open("README.md", 'r', encoding='utf-8') as file:
    long_description = file.read()


setuptools.setup(
    name="lisaorbits",
    use_scm_version=True,
    author='Jean-Baptiste Bayle',
    author_email='j2b.bayle@gmail.com',
    description="LISA Orbits generates orbit files containing spacecraft positions and velocities, proper pseudo-ranges, and spacecraft proper times.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.in2p3.fr/lisa-simulation/orbits",
    license='BSD-3-Clause',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'h5py',
        'numpy',
        'scipy',
        'matplotlib',
        'lisaconstants',
        'oem', 'lxml', 'defusedxml',
        'astropy',
        'importlib_resources',
        'importlib_metadata',
    ],
    setup_requires=['setuptools_scm'],
    tests_require=['pytest'],
    python_requires='>=3.8',
)
