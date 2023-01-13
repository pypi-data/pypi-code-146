"""Do nothing.

Useful when a list of plugins is constructed by a hyperparameter search task.
"""
from .plugin_base import PluginBase


class Plugin(PluginBase):
    pass
