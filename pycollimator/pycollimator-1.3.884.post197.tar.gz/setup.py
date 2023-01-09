#!/bin/env python3

"""Setup script for collimator notebook package."""

from setuptools import setup, find_packages  # type: ignore

deps = ["numpy", "pandas", "requests", "aiohttp", "control", "simpleeval", "ipywidgets==7.7.2"]

setup(
    name="pycollimator",
    setup_requires=["setuptools_scm"],
    use_scm_version={
        "root": "../../../",
        "relative_to": __file__,
        "local_scheme": "no-local-version",
        "version_scheme": "post-release",
    },
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=deps,
    long_description="Python package for Collimator.ai",
)
