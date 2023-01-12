#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/9/29 14:36
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : main.py.py
@Desc    : 
"""
import os
import neptune

os.environ[
    'NEPTUNE_API_TOKEN'] = "eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vdWkubmVwdHVuZS5haSIsImFwaV91cmwiOiJodHRwczovL3VpLm5lcHR1bmUuYWkiLCJhcGlfa2V5IjoiMWUxY2FkNDAtNzYwNS00YTY0LWJkNzQtMTUxMjI2ZGRjNTNhIn0="

# The init() function called this way assumes that
# NEPTUNE_API_TOKEN environment variable is defined.

neptune.init('janus-xu/sandbox')
neptune.create_experiment(name='minimal_example')

# log some metrics

for i in range(100):
    neptune.log_metric('loss', 0.95 ** i)

neptune.log_metric('AUC', 0.96)


#<class 'dict'>:
# {'exp': 1615456176,
# 'iat': 1615454376,
# 'jti': '2ef3d45d-7857-4494-b622-4f3c15033417',
# 'iss': 'https://ui.neptune.ai/auth/realms/neptune',
# 'aud': ['broker', 'account'],
# 'sub': '20279e4b-7e99-4011-bd81-88de95938d80',
# 'typ': 'Bearer',
# 'azp': 'neptune-cli',
# 'session_state': '85f0eb6d-5156-4bca-a5da-e1f7d6d26acd',
# 'acr': '0',
# 'allowed-origins': ['http://localhost*', 'http://localhost:*', 'https://alpha.neptune.ai', '/*', '/', 'https://alpha.neptune.ai/*'],
# 'realm_access': {'roles': ['neptune_write', 'offline_access', 'neptune_read', 'uma_authorization']},
# 'resource_access': {'broker': {'roles': ['read-token']},
# 'account': {'roles': ['manage-account', 'manage-account-links', 'view-profile']}},
# 'scope': 'offline_access',
# 'preferred_username': 'janus-xu',
# 'neptuneHost': 'https://app.neptune.ml',
# 'email': 'janus.xu@outlook.com'}#