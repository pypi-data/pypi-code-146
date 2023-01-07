#! /usr/bin/env python
#
# Copyright (c) 2022-2023 Alberto Mardegan <mardy@users.sourceforge.net>
#
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

from setuptools import setup, find_packages

setup(
    name="obj2xgl",
    version="0.1",
    description="Convert Wavefront 3D models into C code (OpenGL, NDS, Wii)",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alberto Mardegan',
    author_email='info@mardy.it',
    url='https://gitlab.com/mardy/obj2xgl',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Software Development',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'obj2xgl=obj2xgl.__main__:main',
        ],
    },
)
