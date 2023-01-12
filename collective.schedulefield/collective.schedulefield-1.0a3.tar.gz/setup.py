# -*- coding: utf-8 -*-

version = "1.0a3"

from setuptools import setup, find_packages

long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n"
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.rst").read()
    + "\n"
)

setup(
    name="collective.schedulefield",
    version=version,
    description="Schedule behaviors for Plone content types",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="",
    author="IMIO",
    author_email="support@imio.be",
    url="https://github.com/IMIO/collective.schedulefield/",
    license="GPL version 2",
    packages=find_packages("src"),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "Plone",
        # -*- Extra requirements: -*-
    ],
    extras_require={"test": []},
    entry_points={},
)
