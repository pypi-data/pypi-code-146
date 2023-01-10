#!/usr/bin/env python
import random
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from codefast.utils import shell
from codefast.decorators import cachedclassproperty

class _objs(object):
    @cachedclassproperty
    def pool(cls):
        return ThreadPoolExecutor(max_workers=100)

    @classmethod
    def loop(cls):
        return asyncio.get_event_loop()

async def async_render(sync_func:Callable, *args, **kwargs):
        return await _objs.loop.run_in_executor(_objs.pool, sync_func, *args, **kwargs)

def run_async_script(python_file:str):
    which_python = sys.executable
    return shell(f"{which_python} {python_file}")
