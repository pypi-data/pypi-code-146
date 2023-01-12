#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/6 6:10
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : _version.py
@Desc    : 
"""
import os

VERSION = os.environ.get('VERSION', "0.2.36")


def get_versions():
    file = os.path.join(os.path.split(os.path.realpath(__file__))[0], "_version")
    if os.path.exists(file):
        with open(file) as f:
            return f.readline()
    return VERSION


if __name__ == '__main__':
    print(get_versions())
