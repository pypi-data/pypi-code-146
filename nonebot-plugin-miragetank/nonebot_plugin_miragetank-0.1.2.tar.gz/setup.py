#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="nonebot_plugin_miragetank",
    version="0.1.2",
    keywords=["pip", "nonebot_plugin_miragetank"],
    description="Generate/Seperate miragetank picture",
    long_description="Generate miragetank picture",
    license="GPLv3 Licence",
    url="https://github.com/RafuiiChan/nonebot_plugin_miragetank",
    author="Yuyu1628", 
    author_email="a1628420979@163.com",
    packages=find_packages(include=["nonebot_plugin_miragetank", "nonebot_plugin_miragetank.*"]),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "pillow >= 8.4.0",
        "aiohttp",
        "numpy",
        "nonebot2 >= 2.0.0rc1",
        "nonebot-adapter-onebot >= 2.0.0b1",
    ],
)
