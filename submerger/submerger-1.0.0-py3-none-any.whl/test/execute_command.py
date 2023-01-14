import asyncio
from pathlib import Path
from typing import Tuple


async def execute_command(
        command: str | Path,
        *args: str | Path,
) -> Tuple[int | None, str, str]:
    proc = await asyncio.create_subprocess_exec(
        command,
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout.decode(), stderr.decode()
