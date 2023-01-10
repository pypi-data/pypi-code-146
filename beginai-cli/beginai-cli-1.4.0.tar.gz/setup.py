# -*- coding: utf-8 -*-
"""
    Setup file for Begin AI CLI lib.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.2.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from importlib.metadata import entry_points
import sys
import os

from pkg_resources import VersionConflict, require
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_requirements(req_file):
    """Read requirements file and return packages and git repos separately"""
    requirements = []
    dependency_links = []
    lines = read(req_file).split("\n")
    for line in lines:
        if line.startswith("git+"):
            dependency_links.append(line)
        else:
            requirements.append(line)
    return requirements, dependency_links


try:
    require("setuptools>=38.3")
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

REQ_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pip-dep")
core_reqs, core_dependency_links = get_requirements(os.path.join(REQ_DIR, "requirements.txt"))


if __name__ == "__main__":
    setup(
        name="beginai-cli",
        version="1.4.0",
        author="Begin AI Research & Engineering",
        author_email="engineering@begin.ai",
        description="A CLI part of Begin AI ecosystesm that enables batch processing with minimum code.",
        long_description="""
        This is Begin AI CLI for both batch processing.
        It can be used to process historical data and generate signatures that are sent over to Begin AI servers

        You do not need machine learning experience to use this library, 
        check out our documentation for details. 

        https://docs.begin.ai/ddbb8c093f7a49e4b9c1d20a49317527

        Register at https://begin.ai to get started.
        """,
        long_description_content_type="text/markdown",
        url="https://docs.begin.ai",
        packages=find_packages(exclude=["dist", "tests", "pytest.ini"]),
        license="Proprietary",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=core_reqs,
        dependency_links=core_dependency_links,
        entry_points = {
            'console_scripts': ['beginai-cli=beginai_cli.main:app'],
        }
    )
