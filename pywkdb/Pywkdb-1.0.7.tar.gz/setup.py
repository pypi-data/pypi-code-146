#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='Pywkdb',                                           # 打包起来的包的文件名
    version='1.0.7',                                            # 版本号,添加为打包文件的后缀名
    keywords='wangkai python db tools',
    description='wangkai python db tools',                         # 对项目简短的一个形容
    license='MIT License',                                      # 支持的开源协议
    author='wangkai',                                           # 作者
    author_email='1719456@qq.com',                           # 作者的邮箱
    url='http://blog.wangkaicn.cn',
    packages=find_packages(exclude=['venv', 'readme.md', 'test']),                              # 打包的python文件夹
    include_package_data=True,
    platforms='any',
    install_requires=[                                          #定义依赖哪些模块
        'pandas',
        'kombu',
        'pywkmisc'
    ],
 )

