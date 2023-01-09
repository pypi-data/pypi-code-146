#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/10 3:29 PM
# @Author  : cw
import os

from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return open(file_path, encoding='utf-8').read()


setup(
    name='pytest_ogsm_plugin',
    url='https://github.com/cw010/pytest_ogsm_plugin',
    version='3.2',
    author="cw",
    author_email='cwalk.t@gmail.com',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    description='针对特定项目定制化插件，优化了pytest报告展示方式,并添加了项目所需特定参数',
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python :: 3.9',
    ],
    license='proprietary',
    packages=find_packages(),
    package_data={
        "": ["*.html", '*.md'],
    },
    py_modules=['pytestOGSMplugin.pytest_ogsm'],
    keywords=[
        'pytest', 'py.test', 'pytest_ogsm_plugin',
    ],

    install_requires=[
        'pytest',
        'jinja2'
    ],
    entry_points={
        'pytest11': [
            'ogsm_plugin = pytestOGSMplugin.pytest_ogsm',
        ]
    }
)
