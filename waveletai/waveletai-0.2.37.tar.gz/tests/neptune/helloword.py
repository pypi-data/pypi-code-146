#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/7 23:39
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : helloword.py
@Desc    :
"""

import os
os.environ[
    'NEPTUNE_API_TOKEN'] = "eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vdWkubmVwdHVuZS5haSIsImFwaV91cmwiOiJodHRwczovL3VpLm5lcHR1bmUuYWkiLCJhcGlfa2V5IjoiMWUxY2FkNDAtNzYwNS00YTY0LWJkNzQtMTUxMjI2ZGRjNTNhIn0="



import neptune.new as neptune

run = neptune.init('janus-xu/sandbox') # your credentials

# Track metadata and hyperparameters of your Run
run["JIRA"] = "NPT-952"
run["algorithm"] = "ConvNet"

params = {
    "batch_size": 64,
    "dropout": 0.2,
    "learning_rate": 0.001,
    "optimizer": "Adam"
}
run["parameters"] = params


# Track the training process by logging your training metrics
for epoch in range(100):
    run["train/accuracy"].log(epoch * 0.6)
    run["train/loss"].log(epoch * 0.4)

# Log the final results
run["f1_score"] = 0.66

# Stop logging to your Run
# run.stop()