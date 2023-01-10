"""Запуск процесса асинхронно."""

import asyncio
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


async def run_process_async(cmd: str) -> None:
    """Запуск процесса асинхронно."""
    proc = await asyncio.create_subprocess_shell(
        cmd=cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        log.debug("Команда выполнена: {0}".format(cmd))
    if stderr:
        msg: str = "Ошибка выполнения команды: {0}\n{1}".format(
            cmd,
            stderr.decode(),
        )
        log.error(msg)
