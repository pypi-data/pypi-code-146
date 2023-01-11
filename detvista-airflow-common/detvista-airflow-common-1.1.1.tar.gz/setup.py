# -*- coding:UTF-8 -*-
#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages


setup(
    name="detvista-airflow-common",
    version="1.1.1",
    description="detvista airflow support",
    author="detvista",
    author_email="dennis.wang@detvista.com",
    license="Apache License",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "cx_Oracle <= 8.3.0 ",
        "apache-airflow >= 2.2.3"
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
)
