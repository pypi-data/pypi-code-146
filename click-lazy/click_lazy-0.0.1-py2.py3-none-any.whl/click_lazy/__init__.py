from functools import lru_cache
from importlib import import_module

from click import Group, Context


class LazyGroup(Group):
    """
    A click Group that imports commands implementation only when needed.
    """

    def __init__(self, import_name: str, **kwargs):
        self._import_name = import_name
        super().__init__(**kwargs)

    @lru_cache
    def _get_group(self):
        module, name = self._import_name.split(':', 1)
        return getattr(import_module(module), name)

    @property
    def _group(self):
        return self._get_group()

    def get_command(self, ctx: Context, cmd_name: str):
        return self._group.get_command(ctx, cmd_name)

    def list_commands(self, ctx: Context):
        return self._group.list_commands(ctx)

    def invoke(self, ctx: Context):
        return self._group.invoke(ctx)

    def get_usage(self, ctx: Context):
        return self._group.get_usage(ctx)

    def get_params(self, ctx: Context):
        return self._group.get_params(ctx)
