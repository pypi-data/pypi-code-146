#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Jake Cui
# Mail: cqp@cau.edu.cn
# Created Time:  2022-09-18 22:04:41
#############################################

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


requirements = [
    'pandas', 'setuptools'
]


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'metadownload', '__init__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)


# Get the long description from the relevant file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="metadownload",
    version=about['__version__'],
    keywords=["wgs", "pubmlst", "mlst"],
    description="python mlst analysis tool",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT Licence",
    url="https://github.com/hbucqp/metadownload",
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=find_packages(),
    include_package_data=True,
    # package_data={'': ['*']},
    platforms="any",
    install_requires=requirements,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'metadownload=metadownload.metadownload:main',
        ],
    },
)
