#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/6 7:33
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : hosted_backend.py
@Desc    :
"""

from waveletai.backends.hosted_backend import HostedBackend
from waveletai.sessions import Session
import waveletai
from waveletai.utils.storage_utils import UploadEntry
import unittest
from waveletai.dataset import Dataset
from waveletai.model import ModelVersion
from waveletai.constants import ModelRegisterMode


class TestHostedBackend(unittest.TestCase):
    def setUp(self):
        super(TestHostedBackend, self).setUp()
        import os
        os.environ["WAVELETAI_API_URL"] = ""
        os.environ["WAVELETAI_USERNAME"] = ""
        os.environ["WAVELETAI_PASSWORD"] = ""
        self.host_backend = HostedBackend()
        # self.session: Session = waveletai.init(name="", pwd="")

    # def test_init(self):
    #     self.host_backend = HostedBackend()
    #
    # def test_create_dataset(self):
    #     dataset: Dataset = self.host_backend.create_dataset(name="big file6", zone="test",
    #                                                         path="C:\\Users\\janus\\Desktop\\test")
    #     print(dataset.id)
    #     print(dataset.create_time)
    #     print(dataset.name)
    #
    # def test_upload_dataset(self):
    #     self.host_backend.upload_dataset(dataset_id="3c2a4776e4fc4747a47ba1928b84b00a",
    #                                      path="C:\\Users\\janus\\Desktop\\test\\万翠台北苑16-1-102.csv")
    #
    # def test_download_dataset_artifacts(self):
    #     self.host_backend.download_dataset_artifacts(dataset_id="3c2a4776e4fc4747a47ba1928b84b00a",
    #                                                  destination=".\\")
    #
    # def test_model_upload(self):
    #     self.host_backend._model_upload(UploadEntry("D:/accurate.png"), model_repo_id = 'e69eeca80a2649ed833fba9c1b1a5ca5')
    #
    # def test_model_chunk_upload_loop(self):
    #     self.host_backend._model_chunk_upload_loop(UploadEntry("E:/face_mask_data.rar"), model_repo_id = 'e69eeca80a2649ed833fba9c1b1a5ca5')

    def test_register_model_version(self):
        mv: ModelVersion = self.host_backend.register_model_version("032e2bec574e4c0fbe2e4f16c3f07565", "lav3",
                                                                    "C:/Users/admin/Desktop/图片文件夹/1/",
                                                                    ModelRegisterMode.PYFUNC.value)
        print(mv.__repr__())

    def test_download_csv(self):
        result = self.host_backend.download_dataset_artifact('66d975aee3764db6b289cbcd0896fe76', 'DB.csv',
                                                             'C:/Users/admin/Desktop/图片文件夹/')

    def test_all_file(self):
        result = self.host_backend.download_dataset_artifacts('e9bb7d45aebd4d2d8bc31e16630cc5c4',
                                                              'C:/Users/admin/Desktop/图片文件夹/',
                                                              "coco",False)

    def test_upload_dataset(self):
        result = self.host_backend.upload_dataset_artifacts('66d4cc1be4a442a0a02c971146ea749d', 'D:/VISIO/压测')

    def test_create_app(self):
        result = self.host_backend.create_app(name='122223',tags=['111'],desc='123')

    def test_get_app_obj(self):
        result = self.host_backend.create_model('bb4dedc03ae94d02881d867336483105', 'tes001')
        print(result.keys())
    def test_get_path(self):
        result = self.host_backend._download_feature_zip('07530c929d3b454c8f8139973b3fb876', r'C:\Users\admin\Desktop\图片文件夹', True)

    def test_get_fea(self):
        result = self.host_backend.get_feature('12314214')

if __name__ == '__main__':
    unittest.main()
