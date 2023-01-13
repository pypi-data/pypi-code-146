from typing import TYPE_CHECKING, Literal, Optional

from .. import hookimpl
from . import disable, enable, start, stop

if TYPE_CHECKING:
    from ..ctx import Context
    from ..settings import Settings


def register_if(settings: "Settings") -> bool:
    return settings.scheduler == "systemd"


def unit(service: str, qualname: str) -> str:
    return f"pglift-{service}@{qualname}.timer"


@hookimpl
def schedule_service(ctx: "Context", service: str, name: str) -> Literal[True]:
    enable(ctx, unit(service, name))
    return True


@hookimpl
def unschedule_service(
    ctx: "Context", service: str, name: str, now: Optional[bool]
) -> Literal[True]:
    kwargs = {}
    if now is not None:
        kwargs["now"] = now
    disable(ctx, unit(service, name), **kwargs)
    return True


@hookimpl
def start_timer(ctx: "Context", service: str, name: str) -> Literal[True]:
    start(ctx, unit(service, name))
    return True


@hookimpl
def stop_timer(ctx: "Context", service: str, name: str) -> Literal[True]:
    stop(ctx, unit(service, name))
    return True
