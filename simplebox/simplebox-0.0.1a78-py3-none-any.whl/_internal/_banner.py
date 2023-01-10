#!/usr/bin/env python
# -*- coding:utf-8 -*-
import platform
import sys
from datetime import datetime
from enum import Enum
from locale import getpreferredencoding
from typing import Dict, List

from .. import config
from ..collection import ArrayList
from ..config import LogConfig
from ..converter import StorageUnit
from ..utils import Disk


def __build_system_banner_info() -> Dict:
    disk = Disk(str(LogConfig.dir))
    system_properties = {
        "Python Version": platform.python_version(),
        "Python Compiler": platform.python_compiler(),
        "System Encoding": sys.getdefaultencoding(),
        "Terminal Encoding": getpreferredencoding(False),
        "OS Version": platform.platform(),
        "CPU": platform.processor(),
        "Disk Free": f"{disk.get_free(StorageUnit.MB)} MB ({disk.get_free_percent()}%) ",
        "Date Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Weekend": f"{datetime.now().strftime('%A')}"
    }
    system_info = {"title": "System Configuration", "properties": system_properties}
    return system_info


def __build_frame_banner_infos() -> List:
    """
    Contains system properties
    """
    frame_config_infos = []
    frame_config_infos_append = frame_config_infos.append
    frame_config_infos_append(__build_system_banner_info())
    import importlib
    classes = ArrayList(iterable=dir(config))\
        .filter(lambda x: x.endswith("config"))\
        .map(lambda x: importlib.import_module(f".config.{x}", package="simplebox"))\
        .map(lambda x: x.__all__)\
        .flat()\
        .filter(lambda x: x.__class__.__name__.endswith("Config"))
    for class_ in classes:
        frame_config_info = {"title": class_.__doc__.strip()}
        frame_config_properties = {}
        frame_config_info["properties"] = frame_config_properties
        for k, v in class_.__dict__.items():
            if isinstance(v, Enum):
                value = v.name
            else:
                value = v
            frame_config_properties[k.split("__").pop().title().replace("_", " ")] = value
        frame_config_infos_append(frame_config_info)
    return frame_config_infos
