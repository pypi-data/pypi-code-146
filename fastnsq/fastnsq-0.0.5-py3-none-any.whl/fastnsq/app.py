#!/usr/bin/env python3
import asyncio
import os

import codefast as cf
import fire


async def startall():
    t1 = asyncio.create_task(start_nsqlookupd())
    t2 = asyncio.create_task(start_nsqd())
    await asyncio.gather(t2, t1)


async def _start_bin(bin_name: str, *args):
    pwd = os.path.dirname(os.path.abspath(__file__))
    bin_cmd = os.path.join(pwd, 'bins', bin_name)
    cf.info(f'starting {bin_cmd}')
    file_handler = open('/tmp/%s.log' % bin_name, 'a')
    proc = await asyncio.create_subprocess_exec(bin_cmd,
                                                *args,
                                                stdout=file_handler,
                                                stderr=file_handler)
    cf.info('process [ {} ] started, pid is [ {} ]'.format(bin_name, proc.pid))
    stdout, stderr = await proc.communicate()


async def start_nsqd():
    await _start_bin(
        'nsqd',
        *['-data-path', '/tmp/', '-lookupd-tcp-address', '127.0.0.1:4160', '-max-msg-size', '20485760'])


async def start_nsqlookupd():
    await _start_bin('nsqlookupd')


class App(object):

    @staticmethod
    def start():
        """start both nsqlookupd and nsqd"""
        asyncio.run(startall())


def main():
    fire.Fire(App)
