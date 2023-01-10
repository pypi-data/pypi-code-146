#!/usr/bin/env python3
import asyncio
import os

import codefast as cf
import fire


async def parse_config(config_file: str) -> dict:
    return cf.js(config_file)


async def _start(config_file: str = None):
    pwd = os.path.dirname(os.path.abspath(__file__))
    if not config_file:
        config_file = os.path.join(pwd, 'configs/default.json')
    config = await parse_config(config_file)
    cf.info(config)
    bin_cmd = os.path.join(pwd, 'bins/v2ray')
    cf.info(f'starting {bin_cmd}')
    file_handler = open('/tmp/v2ray.log', 'a')
    proc = await asyncio.create_subprocess_exec(bin_cmd, '-c', config_file,
                                                stdout=file_handler,
                                                stderr=file_handler)
    cf.info('process [v2ray ] started, pid is [ {} ]'.format(proc.pid))
    stdout, stderr = await proc.communicate()


class App(object):

    @staticmethod
    def start(config_file: str = None):
        """start both nsqlookupd and nsqd"""
        asyncio.run(_start(config_file))


def main():
    fire.Fire(App)


