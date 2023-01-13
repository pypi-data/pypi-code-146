import logging
from typing import TYPE_CHECKING

from . import cmd

if TYPE_CHECKING:
    from .ctx import Context
    from .types import Runnable

logger = logging.getLogger(__name__)


def start(ctx: "Context", service: "Runnable", *, foreground: bool) -> None:
    """Start a service.

    This will use any service manager plugin, if enabled, and fall back to
    a direct subprocess otherwise.

    If foreground=True, the service is started directly through a subprocess.
    """
    if foreground:
        cmd.execute_program(service.args(), env=service.env())
        return
    if ctx.hook.start_service(
        ctx=ctx, service=service.__service_name__, name=service.name
    ):
        return
    pidfile = service.pidfile()
    if cmd.status_program(pidfile) == cmd.Status.running:
        logger.debug("service '%s' is already running", service)
        return
    cmd.Program(service.args(), pidfile, env=service.env())


def stop(ctx: "Context", service: "Runnable") -> None:
    """Stop a service.

    This will use any service manager plugin, if enabled, and fall back to
    a direct program termination (through service's pidfile) otherwise.
    """
    if ctx.hook.stop_service(
        ctx=ctx, service=service.__service_name__, name=service.name
    ):
        return
    pidfile = service.pidfile()
    if cmd.status_program(pidfile) == cmd.Status.not_running:
        logger.debug("service '%s' is already stopped", service)
        return
    cmd.terminate_program(pidfile)
