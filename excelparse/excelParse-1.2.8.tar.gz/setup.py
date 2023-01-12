#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name = "excelParse",
    version = "1.2.8",
    keywords= ["pip","excelParse"],
    description= "Used for KCmetadata.xls Parsing",
    license = "MIT License",
    
    url = "https://gitee.com/ganjun87/excel-parse.git",
    author = "ganjun",
    author_email= "ganjun@alumni.hust.edu.cn",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    python_requires = ">=3",
    install_requires = ["xlrd"],
)
