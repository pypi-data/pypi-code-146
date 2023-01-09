#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number,
# edit elasticgraph/__init__.py


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("README.rst") as readme_file:
    readme = readme_file.read()

setup(
    name="elasticgraph",
    # tests_require=["pytest", "pytest-cov"],
    # test_suite="tests",
    version=find_version("elasticgraph", "__init__.py"),
    description="Network Graph using D3js with grouping of nodes and elastic edges.",
    long_description=readme + "\n\n",
    author="RWS Datalab",
    author_email="datalab.codebase@rws.nl",
    url="https://gitlab.com/rwsdatalab/rwsdatalab/public/codebase/tools/elasticgraph",
    packages=["elasticgraph"],
    include_package_data=True,
    #package_data={"elasticgraph": ["py.typed"]},
    #zip_safe=False,
    keywords="elasticgraph",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
		"License :: OSI Approved",
    ],
    install_requires=['jinja2', 'd3graph'],
)
