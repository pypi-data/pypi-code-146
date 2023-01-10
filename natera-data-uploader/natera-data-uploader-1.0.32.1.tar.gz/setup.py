#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path
import soyuz
import soyuz.dx
import soyuz.data

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='natera-data-uploader',
    version=soyuz.__version__,
    description='Natera Uploader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nikita Berezin',
    author_email='nberezin@natera.com',
    packages=find_packages(exclude=["*.tests", "tests.*", "tests"]),
    entry_points={
        'console_scripts': [
            'uploader=soyuz.entrypoint:main',
        ],
    },
    install_requires=[
        'dxpy==0.318.1',
        'PyJWT==1.7.1',
        'zope.event==4.5.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 2'
    ],
    python_requires='>=2.7'
)
