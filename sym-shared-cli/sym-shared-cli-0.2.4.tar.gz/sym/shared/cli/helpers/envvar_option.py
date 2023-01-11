import os
from typing import ClassVar

from click import Option
from click_option_group import GroupedOption

from ..helpers.util import wrap


class Used:
    data: ClassVar[dict] = {}


def get_used():
    return Used.data


def reset_used():
    Used.data = {}


def _value_from_envvar(self, value):
    if value:
        for envvar in wrap(self.envvar):
            if os.getenv(envvar) == value:
                get_used()[envvar] = (self.name, value)
                break
    return value


class EnvvarOption(Option):
    def value_from_envvar(self, ctx):
        value = super().value_from_envvar(ctx)
        return _value_from_envvar(self, value)


class EnvvarGroupedOption(GroupedOption):
    def value_from_envvar(self, ctx):
        value = super().value_from_envvar(ctx)
        return _value_from_envvar(self, value)
