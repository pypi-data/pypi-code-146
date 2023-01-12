#!/usr/bin/env python3
"""BEMServer API client"""

from setuptools import setup, find_packages


# Get the long description from the README file
with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bemserver-api-client",
    version="0.9.0",
    description="BEMServer API client",
    long_description=long_description,
    url="https://github.com/BEMServer/bemserver-api-client",
    author="Nobatek/INEF4",
    author_email="dfrederique@nobatek.inef4.com",
    license="AGPLv3+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        (
            "License :: OSI Approved :: "
            "GNU Affero General Public License v3 or later (AGPLv3+)"
        ),
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.27.1",
        "packaging>=21.3",
    ],
    packages=find_packages(exclude=["tests*"]),
)
