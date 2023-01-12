# -*- coding: utf-8 -*-
import setuptools

with open("requirements.txt") as fp:
    requirements = fp.read().splitlines()


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="iacer",
    version="0.0.14",

    description="Iacer",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="qitan",
    packages=[
        "iacer",
        "iacer.cli_modules",
        "iacer.plugin",
        "iacer.report",
        "iacer.testing"
    ],

    install_requires=requirements,

    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X ",
    ],
    scripts=["bin/iacer"],
    include_package_data=True
)
