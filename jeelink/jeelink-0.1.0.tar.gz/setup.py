#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="jeelink",
    version="0.1.0",
    author="Andre Basche",
    license="MIT",
    url="https://github.com/Andre0512/jeelink",
    platforms="any",
    py_modules=["jeelink"],
    packages=find_packages(),
    keywords="smart home automation",
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["pyserial", "pyserial-asyncio"],
)
