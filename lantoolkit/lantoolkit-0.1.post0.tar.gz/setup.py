# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 10:40:59 2022

@author: Administrator
"""

from setuptools import setup, find_packages

setup(
    name="lantoolkit",  # 包名
    version="0.1r",  # 版本
    description="A python toolkit:fix",  # 包简介
    #long_description=open("README.md",mode='r'),  # 读取文件中介绍包的详细内容
    include_package_data=True,  # 是否允许上传资源文件
    author="lan",  # 作者
    author_email="soft-diyuge@outlook.com",  # 作者邮件
    maintainer="虚位以待",  # 维护者
    maintainer_email="none@none.none",  # 维护者邮件
    license="MuLan PSL License",  # 协议
    url="",  # github或者自己的网站地址
    #packages=['lanpy_toolkit'],  # 包的目录
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",  # 设置编写时的python版本
    ],
    #packages=find_packages(where="./src"), 
    python_requires=">=3.0",  # 设置python版本要求
    install_requires=[
        "cn2an","rich","ntplib","pyinstaller","numpy","sympy","cython"
    ],  # 安装所需要的库
    #entry_points={
    #    "console_scripts": [""],
    #},  # 设置命令行工具(可不使用就可以注释掉)
    
)
