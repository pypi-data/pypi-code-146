#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

readme = open("README.rst").read()
# doclink = """
# Documentation
# -------------

# The full documentation is here: https://epfl-center-for-imaging.gitlab.io/orientationpy/index.html"""
history = open("HISTORY.rst").read().replace(".. :changelog:", "")


def readConf(fileName, comments=["#"]):
    """
    Reads a configuration files.
    Gives an array of strings where each item is a striped line that doesn't start by a character in `comments`
    """
    req = []
    with open(fileName) as f:
        for row in f.readlines():
            try:
                line = row.strip()
                if len(line):
                    if line[0] not in comments:
                        req.append(line)
            except BaseException as e:
                print("reading '{}': unable to read line: {}".format(fileName, line))
                print("{}".format(e))

    read = ", ".join(req) if len(req) else "nothing"
    print("reading '{}': add {}".format(fileName, read))
    return req


setup(
    name="orientationpy",
    version="0.2.0.0",
    description="Package for greyscale orientation analysis on 2D and 3D images",
    # long_description=readme + "\n\n" + doclink + "\n\n" + history,
    long_description=readme + "\n\n" + history,
    author="EPFL Center for Imaging",
    author_email="edward.ando@epfl.ch",
    # url="https://gitlab.com/epfl-center-for-imaging/orientationpy/",
    project_urls={
        # "Homepage":      "https://gitlab.com/epfl-center-for-imaging/orientationpy/",
        "Documentation": "https://epfl-center-for-imaging.gitlab.io/orientationpy/index.html",
        "Source Code": "https://gitlab.com/epfl-center-for-imaging/orientationpy",
        # "Bug Tracker":   "https://gricad-gitlab.univ-grenoble-alpes.fr/ttk/spam/-/issues",
    },
    packages=[
        "orientationpy",
    ],
    package_dir={"orientationpy": "orientationpy"},
    include_package_data=True,
    install_requires=readConf("requirements.txt"),
    license="GPLv3",
    zip_safe=False,
    keywords="orientationpy",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
