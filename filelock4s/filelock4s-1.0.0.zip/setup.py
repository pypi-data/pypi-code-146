#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

import filelock4s


with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="filelock4s",
    version=filelock4s.__version__,
    packages=find_packages(exclude=["test*"]),
    zip_safe=False,
    install_requires=["filelock"],
    url="https://github.com/meanstrong/filelock4s",
    description="single shared lock pool manage by filelock",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="pengmingqiang",
    author_email="rockypengchina@outlook.com",
    maintainer="pengmingqiang",
    maintainer_email="rockypengchina@outlook.com",
    platforms=['any'],
    license="Apache 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
