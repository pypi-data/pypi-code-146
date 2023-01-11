#!/usr/bin/env python3
import asyncio
import time

import aiohttp


class ctx(object):

    @classmethod
    def to_str(cls):
        s = ''
        for k, v in cls.__dict__.items():
            if k.startswith('_') or k == 'to_str':
                continue
            s += f'{k}={v} '
        return s


start_time = time.time()
headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}


async def fetch_once(session, url):
    async with session.get(url, headers=headers) as resp:
        return await resp.text()


async def do_benchmark():

    async with aiohttp.ClientSession() as session:
        tasks = []
        while ctx.bound > 0:
            for i in range(ctx.step):
                tasks.append(
                    asyncio.ensure_future(fetch_once(session, ctx.url)))
            ctx.bound -= ctx.step
            ctx.sum += ctx.step
            await asyncio.gather(*tasks)
            print("{:<2.2f} seconds, progress {} / {}".format(
                time.time() - start_time, ctx.sum, ctx.bound))


def asyncbenchmark(url: str, bound: int = 1000, step: int = 100):
    ctx.url = url
    ctx.bound = bound
    ctx.step = step
    ctx.sum = 0
    print(ctx.to_str())
    asyncio.run(do_benchmark())
