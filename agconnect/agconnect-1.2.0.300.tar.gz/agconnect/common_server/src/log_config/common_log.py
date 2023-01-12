# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import os

from agconnect.common_server.src.log_config.logging_config import log_configuration

directory = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../logging_config.json'))
logger = log_configuration(directory)
