#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/4 3:58
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : log.py
@Desc    : 
"""
import mlflow
import waveletai
from mlflow.tracking import MlflowClient



def log_figure(mlflow_experiment_id):
    import matplotlib.pyplot as plt
    client = MlflowClient()
    fig, ax = plt.subplots()
    ax.plot([0, 1], [2, 3])

    run = client.create_run(experiment_id=mlflow_experiment_id)
    client.log_figure(run.info.run_id, fig, "figure.png")



def waveletai_log_figure():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot([0, 1], [2, 3])
    mlflow.log_figure(fig, "figure.png")


def mlflow_log_batch():
    import time
    from mlflow.entities import Metric, Param, RunTag
    client = MlflowClient()
    metrics = []
    params = [Param("p", 'p')]
    tags = [RunTag("t", "t")]
    for i in range(100):
        time.sleep(0.05)
        metrics.append(Metric('m', 1+i, int(time.time() * 1000), i))
    client.log_batch(mlflow.active_run().info.run_uuid,metrics,params,tags)


if __name__ == '__main__':
    # log_figure()
    waveletai.init("xupx","lucky9921")
    from waveletai.experiment import Experiment
    waveletai.get_experiment("80808a94a6fe4d1b90b4d6363e676db2")
    mlflow.set_tracking_uri('waveletai-store://')
    # mlflow.start_run()
    # mlflow.tracking.fluent._get_or_start_run()
    # mlflow.log_param("test","test3")
    # # log_figure(e.mlflow_experiments_id)
    # waveletai_log_figure()
    mlflow_log_batch()
