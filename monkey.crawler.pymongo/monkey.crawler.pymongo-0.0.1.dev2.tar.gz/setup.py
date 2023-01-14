#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

__name__ = 'monkey.crawler.pymongo'
__version__ = '0.0.1.dev2'
__author__ = 'Xavier ROY'
__author_email__ = 'xavier@regbuddy.eu'

project_dir = os.path.dirname(os.path.realpath(__file__))
requirement_file_path = project_dir + '/requirements.txt'
requirements = []
if os.path.isfile(requirement_file_path):
    with open(requirement_file_path) as f:
        requirements = f.read().splitlines()

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://bitbucket.org/monkey-python/monkey-crawler-pymongo/',
    description='Monkey crawler implementation for MongoDB data sources using PyMongo.',
    long_description=open('README.rst').read(),
    license="Apache License, Version 2.0",

    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,

    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers'
    ]
)
