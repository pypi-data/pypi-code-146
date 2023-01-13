# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airtel",  # This is the name of the package
    version="0.0.1",  # The initial release version
    author="rivo2302",  # Full name of the author
    author_email="rivo2302@gmail.com",  # Email address of the author
    description="airtel is a light open source module for your Airtel API.",
    long_description=long_description,  # Long description read from the readme
    long_description_content_type="text/markdown",
    project_urls={
        "Homepage": "https://github.com/rivo2302/airtel_money_api",
    },
    packages=["airtel"],  # List of all modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    python_requires=">=3.7",
    py_modules=["airtel"],  # Name of the python package
    install_requires=["requests"],  # depandance
    include_package_data=True,  # Include all data file with the package
)
