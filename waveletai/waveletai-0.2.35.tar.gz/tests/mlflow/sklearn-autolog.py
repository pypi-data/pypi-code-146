#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/30 14:11
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : sklearn-autolog.py
@Desc    : 
"""

import numpy as np
import mlflow
import waveletai
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LogisticRegression
import os

os.environ["WAVELETAI_API_URL"] = "http://fat.ai.xiaobodata.com/api"
waveletai.init("caokb", "lucky9921")

model = waveletai.get_model('032e2bec574e4c0fbe2e4f16c3f07565')

experiment = model.create_experiment(name='experiment-name', params={'pk1': 1, 'pk2': 2})
# mlflow.set_tracking_uri('waveletai-store://')
def print_auto_logged_info(r):
    tags = {k: v for k, v in r.data.tags.items() if not k.startswith("mlflow.")}
    artifacts = [f.path for f in MlflowClient().list_artifacts(r.info.run_id)]
    print("run_id: {}".format(r.info.run_id))
    print("artifacts: {}".format(artifacts))
    print("params: {}".format(r.data.params))
    print("metrics: {}".format(r.data.metrics))
    print("tags: {}".format(tags))

# prepare training data
X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
y = np.dot(X, np.array([1, 2])) + 3

# Auto log all the parameters, metrics, and artifacts
mlflow.sklearn.autolog()
# mlflow.autolog()
model = LogisticRegression(C=0.95)
with mlflow.start_run() as run:
    model.fit(X, y)
    model.score(X, y)
# mlflow.sklearn.log_model(model, "model")


# fetch the auto logged parameters and metrics for ended run
# print_auto_logged_info(mlflow.get_run(run_id=run.info.run_id))