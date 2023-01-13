from typing import TYPE_CHECKING, Optional

from . import plugin_manager

if TYPE_CHECKING:
    from .settings import Settings


def do(settings: "Settings", env: Optional[str] = None, header: str = "") -> None:
    pm = plugin_manager(settings)
    pm.hook.site_configure_install(settings=settings, pm=pm, header=header, env=env)


def undo(settings: "Settings") -> None:
    pm = plugin_manager(settings)
    pm.hook.site_configure_uninstall(settings=settings, pm=pm)
