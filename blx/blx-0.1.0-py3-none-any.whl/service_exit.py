from __future__ import annotations

import signal

__all__ = ["ServiceExit", "register_service_exit"]


class ServiceExit(Exception):
    pass


def register_service_exit():
    def raise_service_exit(signum, frame):
        del signum
        del frame
        raise ServiceExit

    signal.signal(signal.SIGTERM, raise_service_exit)
    signal.signal(signal.SIGINT, raise_service_exit)
