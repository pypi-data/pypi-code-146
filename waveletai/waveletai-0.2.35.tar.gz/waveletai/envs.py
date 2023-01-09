#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/11 16:01
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : envs.py
@Desc    : 
"""

BACKEND = 'WAVELETAI_BACKEND'

API_URL = 'WAVELETAI_API_URL'

API_KEY = ''

API_TOKEN = 'WAVELETAI_TOKEN'

API_MODEL= 'WAVELETAI_MODEL'

API_PROJ = 'WAVELETAI_PROJ'

"""单次请求最大值 1kb"""
CHUNK_SIZE = 1024

"""超过1M的内容显示进度"""
WARN_SIZE = 1024 * 1024 * 1
