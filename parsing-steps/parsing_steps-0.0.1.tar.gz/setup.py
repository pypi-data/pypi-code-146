#!/usr/bin/env python

from setuptools import find_packages, setup


def read_file(file_path):
    return open(file_path, "r", encoding="utf-8").read()


setup(
    name="parsing_steps",
    version="0.0.1",
    url="https://github.com/loievskyi/parsing_steps",
    license="BSD",
    description="Parsing steps",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="Viacheslav Loievskyi",
    author_email="loievskyi.slava@gmail.com",
    packages=find_packages(exclude=["tests*", "parsing_steps/future*"]),
    include_package_data=True,
    install_requires=["redis", "aioredis"],
    python_requires=">=3.8",
    zip_safe=False,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    project_urls={
        "Source": "https://github.com/loievskyi/parsing_steps",
    },
)
