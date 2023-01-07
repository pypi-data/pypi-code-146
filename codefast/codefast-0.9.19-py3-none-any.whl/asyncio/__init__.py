#!/usr/bin/env python
import random
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from codefast.utils import shell

async def async_render(sync_func:Callable, *args, **kwargs):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, sync_func, *args, **kwargs)

def run_async_script(python_file:str):
    which_python = sys.executable
    return shell(f"{which_python} {python_file}")
