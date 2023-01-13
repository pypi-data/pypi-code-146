# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 17:01:55 2023

@author: Himanshu
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))


VERSION = '0.0.1'
DESCRIPTION = 'qibb commons'
LONG_DESCRIPTION = 'qibb common long'

# Setting up
setup(
    name="qibb-common",
    version=VERSION,
    author="Himanshu",
    author_email="<himanshu.gju@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['boto3'],
    keywords=['qibb'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
