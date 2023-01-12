#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/15 11:17
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : __init__.py.py
@Desc    : 
"""

from pprint import pprint
from river import compose
from river import linear_model
from river import metrics
from river import preprocessing
from river import datasets
import time
import os
import waveletai
from waveletai.app import App
from waveletai.model import Model
from waveletai.run import Metric, Param, RunTag
from waveletai.experiment import Experiment

# os.environ["WAVELETAI_API_URL"] = "http://fat.ai.xiaobodata.com/api"
# waveletai.init("caokb", "lucky9921")
waveletai.init(
    api_token="eyJhcGlfdXJsIjogImh0dHA6Ly9mYXQuYWkueGlhb2JvZGF0YS5jb20vYXBpIiwgInVzZXJfaWQiOiAiMTM1ZWJlNmRiY2JlNDYwOWJhMzg2MmRhOWQxMjBmZjEiLCAiYXBpX3Rva2VuIjogImJkYTlmM2Y2YzEzMDQ0NmM4OTBiMDUwZDg2NjZlZTdkZTY2OGQ2OTlkZjllY2UxMDIzYTcwNDI2ZDc1OWJhMDUifQ==")
# app: App = waveletai.create_app("test_app")
# model: Model = app.create_model("test_name")
# model.create_experiment("test_exp")
dataset = datasets.Phishing()

model = waveletai.get_model('e7af09d768a94cdc956e859958da14e7')

experiment = model.create_experiment(name='experiment-name', params={'pk1': 1, 'pk2': 2})

for x, y in dataset:
    pprint(x)
    print(y)
    break

model = compose.Pipeline(
    # preprocessing.AdaptiveStandardScaler(),
    preprocessing.StandardScaler(),
    linear_model.LogisticRegression()
    # linear_model.SoftmaxRegression()
)

metric = metrics.Accuracy()

metrics_ = []
params = []
tags = []

params.append(Param("1", "2"))
params.append(Param("test", "2123"))
params.append(Param("test2", "3.221321903"))

tags.append(RunTag("1", "2"))
tags.append(RunTag("test", "2123"))
tags.append(RunTag("test2", "3.221321903"))

for x, y in dataset:
    y_pred = model.predict_one(x)  # make a prediction
    metric = metric.update(y, y_pred)  # update the metric
    metrics_.append(Metric("m", metric.get(), time.time(), 0))
    if len(metrics_) == 950:
        waveletai.log_batch(metrics_, params, tags)
        metrics_.clear()
    model = model.learn_one(x, y)  # make the model learn
    print(metric)
waveletai.log_batch(metrics_, params, tags)
