#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/7/31 12:36
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : minio.py
@Desc    : 
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/7/29 13:47
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : test-mlflow-minio.py
@Desc    : 
"""


import mlflow
# remote_server_uri = "..." # set to your server URI
# mlflow.set_tracking_uri(remote_server_uri)
# Note: on Databricks, the experiment name passed to mlflow_set_experiment must be a
# valid path in the workspace
import os
# experiment_id = mlflow.create_experiment(
#             "test", "%s%s" % ("s3://model/", "experiment_id"))
# mlflow.get_experiment(1)
experiment_id = "1"
# os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://192.168.2.88:9000'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://aioss.xiaobodata.com:8888'

os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''
# print(experiment_id)
mlflow.set_experiment(experiment_id)
# with mlflow.start_run(experiment_id=experiment_id):
#     print("进来了")
#     mlflow.log_artifact("README.md", "main3")


from sklearn.linear_model import LinearRegression
import mlflow.sklearn
lr = LinearRegression()
# mlflow.sklearn.log_model(sk_model=lr, artifact_path="model", conda_env="conda.yaml")

# mlflow.set_experiment("/my-experiment")
with mlflow.start_run(experiment_id=experiment_id):
    # mlflow.log_param("a", 1)
    # mlflow.log_metric("b", 2)
    mlflow.sklearn.log_model(sk_model=lr, artifact_path="model", conda_env="conda.yaml")