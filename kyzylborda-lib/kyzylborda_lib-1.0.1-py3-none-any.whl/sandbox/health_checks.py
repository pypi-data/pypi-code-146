from __future__ import annotations

import abc
import asyncio
import os
from typing import TYPE_CHECKING

from .readiness import watch_file_creation
from ..server import tcp

if TYPE_CHECKING:
    from .box import Box


__all__ = ("HealthCheck", "ConnectHealthCheck", "ExistsHealthCheck", "parse_health_checks")


class HealthCheck(abc.ABC):
    @abc.abstractmethod
    async def wait(self, box: Box):
        ...


class ConnectHealthCheck(HealthCheck):
    def __init__(self, address: str):
        super().__init__()
        self.address = address


    async def wait(self, box: Box):
        address = box.get_external_socket_address(self.address)

        if address.startswith("unix:"):
            path = self.address[5:]
            if not os.path.exists(os.path.dirname(path)):
                raise RuntimeError("The directory containing the healthchecked file does not exist")
            await watch_file_creation(path)

        sleep_interval = 0.1
        while True:
            try:
                (await tcp.connect(address)).close()
                break
            except (ConnectionRefusedError, FileNotFoundError):
                await asyncio.sleep(sleep_interval)
                sleep_interval = min(sleep_interval * 2, 3)


class ExistsHealthCheck(HealthCheck):
    def __init__(self, path: str):
        super().__init__()
        self.path = path


    async def wait(self, box: Box):
        await watch_file_creation(box.get_external_file_path(self.path))


def parse_health_checks(data: dict[str, str]) -> list[HealthCheck]:
    result: list[HealthCheck] = []
    for kind, value in data.items():
        if kind == "connect":
            result.append(ConnectHealthCheck(value))
        elif kind == "exists":
            result.append(ExistsHealthCheck(value))
        else:
            raise ValueError(f"Unknown healthcheck {kind}")
    return result
