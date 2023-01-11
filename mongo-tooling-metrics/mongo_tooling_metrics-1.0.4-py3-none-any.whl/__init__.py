from importlib.metadata import version
from typing import Type
from mongo_tooling_metrics.base_hook import BaseHook
from mongo_tooling_metrics.registry import _HookRegistry

VERSION = version('mongo-tooling-metrics')
HOOK_REGISTRY = _HookRegistry()


def register_hook(hook_instance: BaseHook) -> BaseHook:
    """Add the hook to the registry if it doesn't exist & return the singleton hook instance."""
    return HOOK_REGISTRY._safe_set_hook(hook_instance)


def get_hook(hook_class: Type[BaseHook]) -> BaseHook:
    """Get the hook if it exists -- else fail."""
    return HOOK_REGISTRY._safe_get_hook(hook_class)


__all__ = ["base_models", "client", "errors", "hooks"]
