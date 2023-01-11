#!/usr/bin/env python3
# pylint: skip-file


import os

from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mpitree",
    version="0.0.8",
    author="Jason Duong",
    licence="MIT",
    author_email="my.toe.ben@gmail.com",
    description="A Parallel Decision Tree Implementation using MPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["mpitree"],
    url="https://github.com/duong-jason/mpitree",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["matplotlib", "mpi4py", "numpy", "pandas", "scikit-learn"],
    python_requires=">=3.10",
    extras_require={"testing": ["black", "pytest", "pylint", "numpydoc"]},
    include_package_data=True,
)
