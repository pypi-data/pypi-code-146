#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/11 15:43
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : constants.py
@Desc    : 
"""

"""{"api_url":"http://ai.xiaobodata.com","api_token":"","api_key":""}"""
from enum import Enum, unique

ANONYMOUS = 'ANONYMOUS'

ANONYMOUS_API_TOKEN = 'eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vdWkubmVwdHVuZS5haSIsImFwaV91cmwiOiJodHRwczovL3VpLm5lcHR1bmUuYW' \
                      'kiLCJhcGlfa2V5IjoiYjcwNmJjOGYtNzZmOS00YzJlLTkzOWQtNGJhMDM2ZjkzMmU0In0='


@unique
class DataSource(Enum):
    WTHINGS = 'timeseries'  # 小波物联
    MAMMUT = 'mammut'  # 网易猛犸


@unique
class FileExt(Enum):
    CSV = 'csv'
    Parquet = 'parquet'
    # Avro = 'avro'


@unique
class Visibility(Enum):
    # 可见性
    PUBLIC = 'public'  # 公开
    PRIVATE = 'private'  # 私有


@unique
class ModelRegisterMode(Enum):
    # 注册模型类型
    DOCKER = 'docker-container'  # 镜像方式注册
    FRAMEWORK = 'framework'  # 框架无代码部署
    PYFUNC = 'py-func'  # 自定义模型注册


@unique
class FeatureType(Enum):
    COCO = "coco"
    FILE = "zip"
    VOC = "pascal_voc"
    YOLOV5 = "yolov5"
    YOLOV3DARKNET = "yolov3darknet"
    YOLOV3KERAS = "yolov3keras"
    CLASSIFY = 'classify'

@unique
class DataType(Enum):
    # 文件类型 当前指csv
    TYPE_FILE = "file"
    # 图片类型
    TYPE_IMAGE = "image"
    # 视频类型
    TYPE_VIDEO = "video"
    # 视频帧类型 当前指rtsp视频流
    TYPE_VIDEO_FRAME = "video_frame"
    # 暂未用到
    TYPE_TF_RECORD = "tf_record"
    # 暂未用到
    TYPE_AUDIO = "audio"

@unique
class ModelSourceType(Enum):
    """
    model的来源类型
    flow 画布类型
    gitcode git类型
    """
    FLOW = 'flow'
    GITCODE = 'gitcode'

@unique
class DatasetImageType(Enum):
    """
    dataset的图片类型
    """
    CLASSIFY = 'classify'
    POLYGON = 'polygon'
    RECTANGLE = 'rectangle'