#!/usr/bin/env python

from setuptools import setup


def read(path):
    return open(path, 'r').read()


setup_options = dict(
    name='dox-cli',
    version='1.0.8',
    description='Cli to create project structure',
    long_description=read('README.md'),
    author='Bijay Das <imbijaydas@gmail.com>',
    entry_points='''
        [console_scripts]
        dox=cli:main
    ''',
    license='MIT License',
    extras_require={},
    python_requires='>=3.7',
    project_urls={
        'Source': 'https://github.com/bijaydas/dox-cli',
    },
)

setup(**setup_options)
