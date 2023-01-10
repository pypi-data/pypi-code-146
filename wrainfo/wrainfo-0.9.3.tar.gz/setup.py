#!/usr/bin/env python

"""The setup script."""

# WRaINfo, Is a software to process FURUNO weather radar data.
#
# Copyright (c) 2023, FernLab (GFZ Potsdam, fernlab@gfz-potsdam.de)
#
# This software was developed within the context of the RaINfo ("Potential use of
# high resolution weather data in agriculture") project of FernLab funded by
# the Impulse and Networking Fund of the Helmholtz Association.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

version = {}

with open("wrainfo/version.py") as version_file:
    exec(version_file.read(), version)

req = ['numpy==1.20.3',
       'pytest>=6.2.5',
       'scipy>=1.7.0',
       'wradlib>=1.15.0',
       'xarray[complete]==0.20.2',
       'rioxarray==0.12.0']

req_setup = ['pytest-runner']

req_test = ['pytest>=3', 'pytest-cov', 'pytest-reporter-html1', 'urlchecker==0.0.32']

req_doc = [
    'sphinx>=4.1.1',
    'sphinx-argparse',
    'sphinx-autodoc-typehints',
    'sphinx_rtd_theme',
    'pandoc',
    'nbsphinx']

req_lint = ['flake8', 'pycodestyle', 'pydocstyle']

req_dev = ['twine'] + req_setup + req_test + req_doc + req_lint

setup(
    author="FernLab",
    author_email='fernlab@gfz-potsdam.de',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    description="Is a software to process FURUNO weather radar data.",
    entry_points={
        'console_scripts': [
            'wrainfo=bin.wrainfo_cli:main',
        ],
    },
    extras_require={
        "doc": req_doc,
        "test": req_test,
        "lint": req_lint,
        "dev": req_dev
    },
    install_requires=req,
    license="Apache Software License 2.0",
    include_package_data=True,
    keywords=['wrainfo', 'weather radar', 'X-Band', 'preprocessing', 'clutter detection', 'attenuation correction', 'precipitation estimation'],
    long_description=readme,
    name='wrainfo',
    packages=find_packages(include=['wrainfo', 'wrainfo.*']),
    project_urls={
        "Source code": "https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo",
        "Documentation": "https://fernlab.git-pages.gfz-potsdam.de/products/furuno/wrainfo/doc/",
        "Change log": "https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo/-/blob/main/HISTORY.rst"
    },
    setup_requires=req_setup,
    test_suite='tests',
    tests_require=req + req_test,
    url='https://git.gfz-potsdam.de/fernlab/products/furuno/wrainfo',
    version=version['__version__'],
    zip_safe=False,
)
