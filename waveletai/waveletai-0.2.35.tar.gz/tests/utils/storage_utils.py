import unittest#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/9 16:31
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : storage_utils.py
@Desc    : 
"""

import unittest
from waveletai.utils.storage_utils import UploadEntry, scan_upload_entries, split_upload_files

# import os
# files =scan_upload_entries({UploadEntry("C:\\Users\\janus\\Desktop\\test", "")})
# for file in files:
#     print(file.source_path)
#     print("prefix ", os.path.split(file.target_path)[0])
#     print("filename ", os.path.split(file.target_path)[1])
#     print(file.is_stream())

# upload_entry = UploadEntry("C:\\Users\\janus\\Desktop\\test\\大文件\\Car-Price-Prediction-Highly-Comprehensive-Linear-Regression-Project--master.zip", "")
# files =scan_upload_entries([UploadEntry("C:\\Users\\janus\\Desktop\\猫狗测试集", "")])
# for package in split_upload_files(files):
#     # 当文件很多时，每500个文件当作一个package上次一波
#     print(package.size)
#     for entry in package.items:
#         print(entry.source_path)

package = scan_upload_entries([UploadEntry("D:/artifacts/model/")])
for entry in package:
    print(entry.source_path,entry.target_path,entry.prefix)

package = scan_upload_entries([UploadEntry("D:/artifacts/model", "")])
for entry in package:
    print(entry.source_path,entry.target_path,entry.prefix)



