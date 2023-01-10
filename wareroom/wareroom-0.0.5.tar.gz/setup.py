"""Setup configuration for the package."""
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import versioneer


# pylint: disable=invalid-name
long_desc = """cloud object storage wrapper"""

requires = ["esdk-storage-python","wareroom"]

setup(
    name="wareroom",
    url="https://github.com/lipicoder/wareroom",
    author="lipi",
    author_email="lipicoder@qq.com",
    version = versioneer.get_version(),
    cmdclass = versioneer.get_cmdclass(),
    description= long_desc,
    long_description=long_desc,
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
)
