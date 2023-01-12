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

    def test_get_app(self):
        from waveletai.app import App
        waveletai.set_app("b0a81f012780401391bc2ed0e6046c13")
        app: App = waveletai.get_app()
        print(app.name)
        print(app.desc)
        print(app.create_time)

    def test_create_app(self):
        from waveletai.app import App
        app: App = waveletai.create_app("sdk-add-app",tags=['1','2'],desc="sdk-add-app-desc")
        print(app.name)
        print(app.desc)
        print(app.id)

    def test_update_app(self):
        from waveletai.app import App
        waveletai.set_app("74aa92beb23d44a29556163a742551da")
        app: App = waveletai.get_app()
        app = app.update(name="sdk-add-app-1", desc="sdk-add-app-desc-1")
        print(app.name)
        print(app.desc)

    def test_del_app(self):
        from waveletai.app import App
        waveletai.set_app("74aa92beb23d44a29556163a742551da")
        app: App = waveletai.get_app()
        app.delete()


    # def test_register_model_version(self):
    #     mv: ModelVersion = waveletai.register_model_version("6de4a570f5f24ba68754ea18576625f6", "这是模型版本的备注",
    #                                                         "D:/artifacts/model", ModelRegisterMode.PYFUNC.value)
    #     print(mv.__repr__())
    def tearDown(self):
        waveletai.close()


if __name__ == '__main__':
    unittest.main()
