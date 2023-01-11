#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-module-docstring,exec-used
import setuptools

# DO NOT EDIT THIS NUMBER!
# It is changed automatically by python-semantic-release
__version__ = "0.2.1"

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='vasp_suite',
    version=__version__,
    author='Chilton Group',
    author_email='nicholas.chilton@manchester.ac.uk',
    description='A package for creating and handling input files for vasp',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_url={
        "Bug Tracker": "https://github.com/chilton-group/vasp_suite/issues",
        "Documentation": "https://chilton-group.gitlab.io/vasp_suite",
        "Source": "https://github.com/chilton-group/vasp_suite",
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
        ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'gemmi',
        ],
    entry_points={
        'console_scripts': [
            'vasp_suite = vasp_suite.cli:main'
            ]
        }
    )
    

