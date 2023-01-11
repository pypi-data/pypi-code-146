import datetime

import yaml


def datetime_representer(dumper, dt):
    return dumper.represent_scalar("!time", dt.isoformat())


def datetime_constructor(loader, node):
    value = loader.construct_scalar(node)
    return datetime.datetime.fromisoformat(value).time()


def sym_init():
    yaml.add_representer(datetime.time, datetime_representer)
    yaml.add_constructor("!time", datetime_constructor)
