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
Various helper utils:
* Collections and iterators
* Env vars
* Design Patterns
* Documents parsing
* File System
* Logging
* Multiprocessing
* Profiling
* Relational Databases
* Various other utils
""".strip()

SHORT_DESCRIPTION = """
Various helper utils.""".strip()

DEPENDENCIES = [
    'fire',
    'profilehooks',
    'SQLAlchemy',
    'sqlalchemy-utils',
    'psycopg2-binary',
    'boto3',
    'xmltodict',
    'pandas',
    'str2bool',
    'numpy'
]

VERSION = '0.0.1'
URL = 'https://github.com/reljicd/python-snippets-lib'

setup(
    name='reljicd-utils',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,

    author='Dusan Reljic',
    author_email='reljicd@google.com',
    license='Apache Software License',

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

    keywords='helpers utils multiprocessing config collections profiling sql',

    install_requires=DEPENDENCIES
)
