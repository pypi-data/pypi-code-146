#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/9 13:19
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : model.py
@Desc    : 
"""

import logging
import yaml
import os
from waveletai.utils import set_mlflow_tracing_waveletai_store
from waveletai.constants import ModelRegisterMode
import mlflow

_logger = logging.getLogger(__name__)


class Model(object):

    def __init__(self, backend, id, name, desc, app_id, create_time, create_user_id, update_time, update_user_id, source):
        self._backend = backend
        self.id = id
        self.name = name
        self.desc = desc
        self.app_id = app_id
        self.create_time = create_time
        self.create_user_id = create_user_id
        self.update_time = update_time
        self.update_user_id = update_user_id
        self.source = source

    def update(self, name, desc):
        """
        更新模型信息
        :return: class: `Model` Object
        """
        return self._backend.update_model(name, desc)

    def delete(self):
        """
        删除模型
        :return:
        """
        return self._backend.delete_model()

    def register_model_version(self, desc, path, mode=ModelRegisterMode.PYFUNC.value):
        """
        注册模型库版本
        :param mode: 注册模式,默认为自定义
        :param path: 注册文件路径，可以是文件夹,当为docker模式时，此处为docker-image,可以用save命令导出  eg：deployment.tar
        :return: class: `ModelVersion` Object
        """
        self._backend.register_model_version(desc, path, mode)

    def get_model_version(self, version):
        """
        获取注册的指定版本的模型信息
        :param version: 模型版本号，如1,2,3
        :return: class: `ModelVersion` Object
        """
        return self._backend.get_model_version(version)

    def list_model_versions(self, page=1, pagesize=10):
        """
        获取注册的各版本模型信息列表
        fetch a list of all registered models in the registry with a simple method.
        :return: List of Class `ModelVersion` Object
        """
        return self._backend.list_model_versions(self.id, page, pagesize)

    def update_model_version(self, version, desc):
        """
        更新模型版本信息
        :param version: 模型版本号，如1,2,3
        :param desc: 模型版本信息
        :return:  List of Class `ModelVersion` Object
        """
        return self._backend.update_model_version(version, desc)

    def abandon_model_version(self, version):
        """
        根据版本号丢弃模型对比版本信息
        :param version: 模型版本号，如1,2,3
        :return:
        """
        return self._backend.abandon_model_version(version)

    def list_experiments(self):
        """
        返回当前模型的实验列表
        :return: List of Class `Experiment` Object
        """
        return self._backend.list_experiments()

    def list_release(self, version=None):
        """
        返回当前模型的发布列表，version为空时返回所有
        :return: List of Class `Release` Object
        """
        return self._backend.list_model_releases(version)

    def search_model_versions(self, desc, stage):
        """search for a specific stage or desc and list its version details"""
        pass

    def transition_model_version_stage(self, version, stage):
        pass

    def mlflow_project_file(self, mlproject_path=None):
        """
        获取模型的MLProject
        :param mlproject_path: 如果传入了路径, 将读取该路径指向的mlproject描述
        :return:
        """
        if mlproject_path:
            os.path.exists(mlproject_path)
            with open(mlproject_path, 'rb') as f:
                return yaml.load(f, Loader=yaml.FullLoader)

        return self._backend.get_mlproject_file()

    @set_mlflow_tracing_waveletai_store
    def create_experiment(self, name, params=None):
        """
        创建一个实验, 先创建mlflow的experiment, 再创建wai平台的experiment
        :param name:
        :param params: 训练参数字典 {key:value, key2:value2, ...}
        :return:
        """
        return self._backend.create_experiment(name=name, model_id=self.id,
                                               params=params,
                                               docker_args={},
                                               is_train=True
                                               )

    @set_mlflow_tracing_waveletai_store
    def get_experiment(self, experiment_id):
        """
        获取实验对象
        :param experiment_id:
        :return:
        """
        return self._backend.get_experiment(experiment_id)


class ModelVersion(object):
    def __init__(self, backend, id, version, desc, model_id, model_name, mode, create_user_name, create_time,
                 create_user_id):
        self._backend = backend
        self.id = id
        self.version = version
        self.desc = desc
        self.model_id = model_id
        self.mode = mode
        self.create_time = create_time
        self.create_user_id = create_user_id
        self.create_user_name = create_user_name
        self.model_name = model_name

    def download_artifact(self, path, destination_dir=None):
        """Download an artifact (file) from the model version.
        Download a file indicated by ``path`` from the experiment artifacts and save it in ``destination_dir``.
        Args:
            path (:obj:`str`): Path to the file to be downloaded.
            destination_dir (:obj:`str`):
                The directory where the file will be downloaded.
                If ``None`` is passed, the file will be downloaded to the current working directory.

        Raises:
            `NotADirectory`: When ``destination_dir`` is not a directory.
            `FileNotFound`: If a path in dataset artifacts does not exist.

        Examples:
            Assuming that `modelversion` is an instance of :class:`~waveletai.model.modelversion`.

            .. code:: python3

                dataset.download_asset('raw_data.csv', '/home/modelversion/files/')

        """
        return self._backend.download_model_version_asset(self.id, path, destination_dir)

    def download_artifacts(self, destination_dir=None):
        """Download all artifacts from the model version
        Download all artifacts and save it in ``destination_dir``

        Args:
            destination_dir (:obj:`str`): The directory where the archive will be downloaded.
                If ``None`` is passed, the archive will be downloaded to the current working directory.

        Raises:
            `NotADirectory`: When ``destination_dir`` is not a directory.
            `FileNotFound`: If a path in dataset artifacts does not exist.

        Examples:
            Assuming that that `modelversion` is an instance of :class:`~waveletai.model.modelversion`.

            .. code:: python3

                # Download all experiment artifacts to current working directory
                experiment.download_artifacts()

                # Download to user-defined directory
                experiment.download_artifacts('/home/modelversion/')

        """
        return self._backend.download_model_version_artifacts(self.id, destination_dir)

    def list_releases(self):
        """
        查询当前模型版本的发布服务列表
        :return:
        """
        return self._backend.list_model_releases_by_repo()
