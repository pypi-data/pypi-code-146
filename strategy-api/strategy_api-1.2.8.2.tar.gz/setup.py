#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Kevin
# @Time     : 2022/12/12

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='strategy_api',
    version='1.2.8.2',
    author='Kevin',
    author_email='1782552261@qq.com',
    description='bug 修改',
    long_description=long_description,
    url='https://gitee.com/Jason520deng/strategy_api',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

