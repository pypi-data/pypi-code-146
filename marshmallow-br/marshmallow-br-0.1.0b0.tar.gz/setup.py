#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = [
    "marshmallow>=3.0.0b10",
]

test_requirements = [
    "pytest>=3",
]

setup(
    name="marshmallow-br",
    description="An unofficial extension to Marshmallow fields and validators for Brazilian documents",
    long_description=readme,
    author="Leandro César Cassimiro",
    author_email="ccleandroc@gmail.com",
    url="https://github.com/leandcesar/marshmallow-br",
    version="0.1.0b",
    license="Apache 2.0",
    python_requires=">=3.8",
    packages=find_packages(include=["marshmallow_br", "marshmallow_br.*"]),
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords=[
        "serialization",
        "br",
        "brazilian",
        "document",
        "marshal",
        "marshalling",
        "deserialization",
        "validation",
        "schema",
    ],
    zip_safe=False,
    install_requires=requirements,
    tests_require=test_requirements,
    test_suite="tests",
)
