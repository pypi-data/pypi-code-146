#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/6/29 15:52
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : __init__.py.py
@Product: WaveletAI
"""

import unittest
import waveletai
import os
from waveletai.dataset import Dataset
from waveletai.model import ModelVersion
from waveletai.constants import ModelRegisterMode


class TestInit(unittest.TestCase):
    def setUp(self):
        super(TestInit, self).setUp()
        waveletai.init(
            api_token="eyJhcGlfdXJsIjogImh0dHA6Ly9mYXQuYWkueGlhb2JvZGF0YS5jb20vYXBpIiwgInVzZXJfaWQiOiAiMTM1ZWJlNmRiY2JlNDYwOWJhMzg2MmRhOWQxMjBmZjEiLCAiYXBpX3Rva2VuIjogImJkYTlmM2Y2YzEzMDQ0NmM4OTBiMDUwZDg2NjZlZTdkZTY2OGQ2OTlkZjllY2UxMDIzYTcwNDI2ZDc1OWJhMDUifQ==")
        waveletai.get_experiment("4cb11a10b88449399a1ea8a7ae70e096")

    def test_get_app(self):
        from waveletai.app import App
        app: App = waveletai.get_app("27816f49bbac46858bc508793af86bb6")
        print(app.name)
        print(app.desc)
        print(app.create_time)

    def test_create_dataset(self):
        dataset: Dataset = waveletai.create_dataset(name="lalalal13", zone="test",
                                                    path="./test-data/")
        print(dataset.id)
        print(dataset.create_time)
        print(dataset.name)

    def test_get_dataset(self):
        dataset: Dataset = waveletai.get_dataset("4c477768cf244df8be0a332e451346f9")
        print(dataset.id)
        print(dataset.create_time)
        print(dataset.name)

    # def test_download_dataset_artifacts(self):
    #     dataset: Dataset = waveletai.get_dataset("4c477768cf244df8be0a332e451346f9")
    #     dataset.download_artifacts("./my_dataset2")

    def test_download_dataset_artifact(self):
        dataset: Dataset = waveletai.get_dataset("fce09c1d1b0241e6b3740db347afcb37")
        dataset.download_artifact("ZrbnrFS67tc6VypjfAGoDP.jpg", "./my_dataset3")

    # def test_register_model_version(self):
    #     mv: ModelVersion = waveletai.register_model_version("6de4a570f5f24ba68754ea18576625f6", "这是模型版本的备注",
    #                                                         "D:/artifacts/model", ModelRegisterMode.PYFUNC.value)
    #     print(mv.__repr__())
    def tearDown(self):
        waveletai.close()


if __name__ == '__main__':
    unittest.main()
