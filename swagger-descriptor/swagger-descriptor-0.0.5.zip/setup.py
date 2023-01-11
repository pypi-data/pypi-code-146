#!/usr/bin/env python
# -*- coding: utf-8 -*-


import io
import os

from setuptools import setup, find_packages

import swagger_descriptor


cwd = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(cwd, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()


setup(
    name="swagger-descriptor",
    version=swagger_descriptor.__version__,
    packages=find_packages(exclude=["test*"]),
    description="这是一个swagger api解析模块，解析swagger api为apis（一个API接口一个对象）和definitions，便于后续的进一步使用",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rocky Peng",
    author_email="rockypengchina@outlook.com",
    url="https://github.com/meanstrong/swagger-descriptor",
    maintainer="Rocky Peng",
    maintainer_email="rockypengchina@outlook.com",
    platforms=["any"],
    include_package_data=True,
    license="Apache 2.0",
    classifiers=["Programming Language :: Python", "Programming Language :: Python :: 3"],
)
