#!/usr/bin/env python
import asyncio
import json
import ast
import aiohttp
import codefast as cf
import psutil
from codefast.asyncio import async_render
from vps.auth import Accounts

from vps.db import delete_old_than_hours, insert_once

loop = asyncio.get_event_loop()


async def get_cpu_usage() -> float:
    cpu_list = []
    for _ in range(1):
        cpu_list.append(psutil.cpu_percent())
        await asyncio.sleep(1)
    return sum(cpu_list) / len(cpu_list)


def memory_usage_to_json():
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'available': mem.available,
        'percent': mem.percent,
        'used': mem.used,
        'free': mem.free,
        'active': mem.active,
        'inactive': mem.inactive,
        'buffers': mem.buffers,
        'cached': mem.cached,
        'shared': mem.shared,
        'slab': mem.slab,
    }


async def get_mem_usage() -> float:
    return await loop.run_in_executor(None, memory_usage_to_json)


async def get_vnstat() -> float:
    resp = await async_render(
        cf.shell, 'vnstat --json |jq ".interfaces[0].traffic.day"')
    return json.loads(resp)


def disk_usage_to_json():
    disk = psutil.disk_usage('/')
    return {
        'total': disk.total,
        'used': disk.used,
        'free': disk.free,
        'percent': disk.percent,
    }


async def disk_usage():
    return await loop.run_in_executor(None, disk_usage_to_json)


async def uptime():
    return await async_render(cf.shell, 'uptime')


async def ipinfo() -> dict:
    local_cache = '/tmp/ipinfo.json'
    if cf.io.exists(local_cache):
        try:
            return cf.js(local_cache)
        except Exception:
            pass 

    async with aiohttp.ClientSession() as session:
        async with session.get('https://ipinfo.io/json?token={}'.format(
                Accounts.ipinfo_token)) as resp:
            resp = await resp.json()
            await async_render(cf.js.write, resp, local_cache)
            return resp


async def hostname():
    return await async_render(cf.shell, 'hostname')


async def post_summary(url: str, key: str, summary: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={
                'key': key,
                'value': str(summary)
        }) as resp:
            return await resp.json()


async def post_once():
    results = await asyncio.gather(
        get_cpu_usage(),
        get_mem_usage(),
        get_vnstat(),
        disk_usage(),
        uptime(),
        ipinfo(),
        hostname(),
    )
    summary = {
        'cpu': results[0],
        'mem': results[1],
        'vnstat': results[2],
        'disk': results[3],
        'uptime': results[4],
        'ipinfo': results[5],
        'hostname': results[6],
    }

    TIMEOUT = 60
    tasks = asyncio.gather(
        insert_once('vpsstatus', str(summary)),
        delete_old_than_hours(2)
    )
    return await asyncio.wait_for(tasks, timeout=TIMEOUT)

def status():
    loop.run_until_complete(post_once())
