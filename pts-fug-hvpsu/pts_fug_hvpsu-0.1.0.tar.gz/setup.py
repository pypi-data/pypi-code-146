from setuptools import find_packages, setup
import os

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pts_fug_hvpsu",
    version='0.1.0',
    author="Pass testing Solutions GmbH",
    description="FUG HV PSU Diagnostic Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="shuparna@pass-testing.de",
    url="https://gitlab.com/pass-testing-solutions/fug-power-supply",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    py_modules=["pts_fug_hvpsu"],
    packages=find_packages(include=['pts_fug_hvpsu']),
    include_package_data=True,
)
