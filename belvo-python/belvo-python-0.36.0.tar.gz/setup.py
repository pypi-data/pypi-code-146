#!/usr/bin/env python
import os

from setuptools import setup

from belvo import __version__

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(here, "requirements/base.txt")) as f:
    requirements = f.read().splitlines()


def get_packages():
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk("belvo")
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name="belvo-python",
    url="https://github.com/belvo-finance/belvo-python",
    version=__version__,
    description="Belvo Python SDK",
    python_requires=">=3.6, <4",
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=get_packages(),
)
