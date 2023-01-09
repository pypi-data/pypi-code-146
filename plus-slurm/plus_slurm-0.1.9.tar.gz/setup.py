# -*- coding: utf-8 -*-

import os.path
from codecs import open
import sys

from setuptools import setup

REQUIRED = [
    'jinja2',
    'future',
    'humanfriendly',
    'six',
    'numpy',
    'psutil'
]

if sys.version_info < (3, 6):
    REQUIRED.append('pathlib2')

# find the location of this file
this_directory = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(this_directory, 'VERSION'), encoding='utf-8') as f:
    version = f.read()

setup(
    name='plus_slurm',
    version=version,
    packages=['plus_slurm'],
    url='https://gitlab.com/thht/plus-slurm',
    license='GPL3',
    author='Thomas Hartmann',
    author_email='thomas.hartmann@th-ht.de',
    description='Convenient Python Abstraction for the Slurm based cluster at the PLUS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=REQUIRED,
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    keywords='Slurm',
    python_requires='>=3.9'
)
