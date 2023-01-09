#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/6 5:42
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : backend.py
@Desc    : 
"""

from abc import ABCMeta, abstractmethod

import six


@six.add_metaclass(ABCMeta)
class Backend:
    model_id = None
    app_id = None

    def set_model(self, model_id):
        self.model_id = model_id

    def set_app(self, app_id):
        self.app_id = app_id

    @abstractmethod
    def api_address(self):
        pass

    @abstractmethod
    def create_app(self, name, tags, desc):
        pass

    @abstractmethod
    def get_app(self):
        pass

    @abstractmethod
    def update_app(self, name, tags, desc):
        pass

    @abstractmethod
    def delete_app(self):
        pass

    @abstractmethod
    def create_dataset(self, name, data_type, visibility, json_data, desc):
        pass

    @abstractmethod
    def get_dataset(self, dataset_id):
        pass

    @abstractmethod
    def update_dataset(self, dataset_id, name, visibility, desc):
        pass

    @abstractmethod
    def delete_dataset(self, dataset_id):
        pass

    @abstractmethod
    def upload_dataset_artifacts(self, dataset_id, path):
        pass

    @abstractmethod
    def download_dataset_artifact(self, dataset_id, path, destination):
        pass

    @abstractmethod
    def download_dataset_artifacts(self, dataset_id, destination):
        pass

    @abstractmethod
    def download_data(self, dataset_id, path, destination_dir, datasource, fileext, query):
        pass

    @abstractmethod
    def create_model(self, app_id, name, desc):
        pass

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def update_model(self, model_id, app_id, name, desc):
        pass

    @abstractmethod
    def delete_model(self, model_id):
        pass

    @abstractmethod
    def get_model_version(self, model_id, version):
        pass

    @abstractmethod
    def list_model_versions(self, model_id, page=1, pagesize=10):
        pass

    @abstractmethod
    def abandon_model_version(self, model_id, version):
        pass

    @abstractmethod
    def update_model_version(self, model_id, version, desc):
        pass

    @abstractmethod
    def list_experiments(self, model_id):
        pass

    @abstractmethod
    def register_model_version(self, model_id, desc, artifacts, mode):
        pass

    @abstractmethod
    def download_model_artifact(self, model_id, path, destination):
        pass

    @abstractmethod
    def download_model_artifacts(self, model_id, destination):
        pass

    @abstractmethod
    def list_model_releases(self, model_id, version):
        pass

    @abstractmethod
    def get_mlflow_experiment(self, experiment_id):
        pass

    @abstractmethod
    def get_mlproject_file(self):
        pass

    @abstractmethod
    def get_experiment(self, experiment):
        pass

    @abstractmethod
    def create_experiment(self, name, model_id):
        pass

    @abstractmethod
    def create_mlflow_experiment(self, name, artifact_location):
        pass

    @abstractmethod
    def create_mlflow_run(self, name, artifact_uri, run_uuid, experiment_id, source_type,
                          source_name, entry_point_name, user_id, status, start_time, end_time,
                          source_version, lifecycle_stage):
        pass

    @abstractmethod
    def get_experiment_by_mlflow_experiment(self, experiment_id):
        pass

    @abstractmethod
    def get_experiment_by_mlflow_run(self, run_id):
        pass

    @abstractmethod
    def get_mlflow_run(self, run_id):
        pass

    @abstractmethod
    def log_params(self, run_id, params):
        pass

    @abstractmethod
    def log_metrics(self, run_id, metric, value, is_nan):
        pass

    @abstractmethod
    def set_tags(self, run_id, tags):
        pass

    @abstractmethod
    def update_run_info(self, run_id, run_status, end_time):
        pass

    @abstractmethod
    def upload_artifact(self, local_file, artifact_path, run_id):
        pass
