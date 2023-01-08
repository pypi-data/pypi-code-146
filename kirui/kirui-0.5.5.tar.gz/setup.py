#!/usr/bin/env python
import os

from setuptools import find_packages, setup

try:
    with open('VERSION', 'r') as f:
        version = f.read().strip()
except FileNotFoundError:
    version = '0.5.5'

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kirui',
    version=version,
    description='UI framework with React / Preact and Django SSR backend',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Bence Lovas',
    author_email='me@lovasb.com',
    url='https://kirui.lovasb.com/',
    packages=find_packages(),
    include_package_data=True,
    project_urls={
        'Documentation': 'https://kirui.lovasb.com/',
        'Source': 'https://gitlab.com/lovasb/kirui',
        'Tracker': 'https://gitlab.com/lovasb/kirui/-/issues',
    },
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    scripts=['kirui_dev']
)
