import os
import uuid

from django.conf import settings


def get_uuid4_hex():
    hh = uuid.uuid4().hex
    return hh


def get_setting_value(name):
    value = os.environ.get(name, getattr(settings, name, None))
    if value is None:
        raise NotImplementedError("没有配置这个参数%s" % name)
    return value


def get_env_value(name, default=None):
    value = os.environ.get(name, default)
    if value is None:
        raise NotImplementedError("没有配置这个参数%s" % name)
    return value
