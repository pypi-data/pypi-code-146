#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygalaxy",
    version="0.3.8",
    author="patrickxu",
    author_email="xcpxcp198608@163.com",
    description="common package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patrickxu1986/pygalaxy",
    project_urls={
        "Bug Tracker": "https://github.com/patrickxu1986/pygalaxy/issues",
    },
    install_requires=[
        'pycryptodome>=3.15.0',
        'pymysql>=1.0.2',
        'PyJWT>=2.6.0',
        'requests>=2.28.1',
        'numpy>=1.23.4',
        'beautifulsoup4>=4.11.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",

)

# deploy.sh project to pypi
# pip3 install --upgrade build
# python3 -m build
# pip3 install --upgrade twine
# python3 -m twine upload --repository pypi dist/*
