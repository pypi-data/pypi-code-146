#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import RuanjianGongchengMianxiangDuixiangHechuantongdeFangfa
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('RuanjianGongchengMianxiangDuixiangHechuantongdeFangfa'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="ruanjian-gongcheng-mianxiang-duixiang-hechuantongde-fangfa",
    version=RuanjianGongchengMianxiangDuixiangHechuantongdeFangfa.__version__,
    url="https://github.com/apachecn/ruanjian-gongcheng-mianxiang-duixiang-hechuantongde-fangfa",
    author=RuanjianGongchengMianxiangDuixiangHechuantongdeFangfa.__author__,
    author_email=RuanjianGongchengMianxiangDuixiangHechuantongdeFangfa.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Documentation",
        "Topic :: Documentation",
    ],
    description="软件工程：面向对象和传统的方法原书第8版",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "ruanjian-gongcheng-mianxiang-duixiang-hechuantongde-fangfa=RuanjianGongchengMianxiangDuixiangHechuantongdeFangfa.__main__:main",
            "RuanjianGongchengMianxiangDuixiangHechuantongdeFangfa=RuanjianGongchengMianxiangDuixiangHechuantongdeFangfa.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
