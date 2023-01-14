# Copyright (C) 2023 Dusan Reljic.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

LONG_DESCRIPTION = """
Dict Objectify (DO) allows specification of python classes hierarchy that are 
backed by dictionaries. Specification is done similar to ORM frameworks, 
by declaratively specifying dictionary keys as fields, 
Every field is defined as either nested (DO) class for nested dictionaries 
or one of the provided type classes for values of the 
type: int, float, text, bool, array, datetime or enum.

Mapping between dictionaries and these objects works both ways.

This allows easy parsing of hierarchical documents into python object hierarchy, 
doing pre processing on dict values, doing any kind of processing on 
that hierarchy and then transforming root objects back into dictionaries 
for eventual dumping into same document formats.
""".strip()

SHORT_DESCRIPTION = """
Dictionary to Object hierarchy mapper.""".strip()

DEPENDENCIES = [
    'str2bool'
]

TEST_DEPENDENCIES = [
    'pytest'
]

VERSION = '0.0.2'
URL = 'https://github.com/reljicd/dict-objectify'

setup(
    name='dict-objectify',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,

    author='Dusan Reljic',
    author_email='reljicd@google.com',
    license='Apache Software License',

    packages=find_packages('.', exclude=['docker', 'scripts',
                                         'tests', 'tests.*']),

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],

    keywords='mapper mapping dict dictionary object oop xml json csv',

    install_requires=DEPENDENCIES,
    tests_require=TEST_DEPENDENCIES
)
