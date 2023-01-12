#!/usr/bin/env python




#   Copyright 2023 Paul Krug
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import sys
import logging
from setuptools import setup, find_packages


# Set up the logging environment
logging.basicConfig()
log = logging.getLogger()

# Handle the -W all flag
if 'all' in sys.warnoptions:
    log.level = logging.DEBUG

# Get version from the module
with open('TensorTract/__init__.py') as f:
    for line in f:
        if line.find('__version__') >= 0:
            version = line.split('=')[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

# Dependencies
DEPENDENCIES = [
    'numpy',
    ]

CLASSIFIERS = """
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Topic :: Software Development
Topic :: Scientific/Engineering
Typing :: Typed
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
"""

setup_args = dict(
    name='TensorTract',
    version=version,
    description='TT',
    author='Paul Krug',
    author_email='paul_konstantin.krug@tu-dresden.de',
    license='Apache-2.0',
    classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f],
    keywords=[ 'Neural network', 'Python' ],
    packages=find_packages(),
    package_dir={'TensorTract': 'TensorTract'},
    install_requires=DEPENDENCIES,
    zip_safe= True,
)

setup(**setup_args)