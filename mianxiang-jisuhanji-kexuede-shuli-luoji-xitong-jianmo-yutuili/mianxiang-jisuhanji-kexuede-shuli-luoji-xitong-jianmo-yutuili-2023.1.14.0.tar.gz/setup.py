#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import MianxiangJisuhanjiKexuedeShuliLuojiXitongJianmoYutuili
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('MianxiangJisuhanjiKexuedeShuliLuojiXitongJianmoYutuili'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="mianxiang-jisuhanji-kexuede-shuli-luoji-xitong-jianmo-yutuili",
    version=MianxiangJisuhanjiKexuedeShuliLuojiXitongJianmoYutuili.__version__,
    url="https://github.com/apachecn/mianxiang-jisuhanji-kexuede-shuli-luoji-xitong-jianmo-yutuili",
    author=MianxiangJisuhanjiKexuedeShuliLuojiXitongJianmoYutuili.__author__,
    author_email=MianxiangJisuhanjiKexuedeShuliLuojiXitongJianmoYutuili.__email__,
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
    description="面向计算机科学的数理逻辑系统建模与推理",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "mianxiang-jisuhanji-kexuede-shuli-luoji-xitong-jianmo-yutuili=MianxiangJisuhanjiKexuedeShuliLuojiXitongJianmoYutuili.__main__:main",
            "MianxiangJisuhanjiKexuedeShuliLuojiXitongJianmoYutuili=MianxiangJisuhanjiKexuedeShuliLuojiXitongJianmoYutuili.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
