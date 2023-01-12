#!/usr/bin/env python
import ast
import asyncio
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple, Union

import codefast as cf
import pandas as pd

from vps.db import load_data


class MemoryReader(object):

    def __init__(self, input_data: Dict[str, str]):
        self.data = input_data

    def humanize(self, unit: float) -> float:
        return unit / 1024 / 1024 / 1024

    def __repr__(self) -> str:
        # demo : {'total': 33815085056, 'used': 28684914688, 'free': 3395584000, 'percent': 89.4}
        total = self.humanize(self.data['total'])
        used = self.humanize(self.data['used'])
        return f'{self.data["percent"]}%({used:.2f}/{total:.2f}G)'


class Activity(object):

    def __init__(self, status_dict, datatime) -> None:
        self.status_dict = status_dict
        self.datatime = datatime

    def __repr__(self) -> str:
        return f'{self.datatime} {self.status_dict}'


class DataReader(object):

    def __init__(self, input_data: List[str]):
        self.activity_list = [
            Activity(ast.literal_eval(d[2]), d[3]) for d in input_data
        ]

    def process(self) -> dict:
        self.hosts = defaultdict(list)
        for a in self.activity_list:
            self.hosts[a.status_dict['hostname']].append(a)
        _ = [(k, v) for k, v in self.hosts.items()]
        _.sort(key=lambda x: x[0].lower(), reverse=True)
        return _


class DeviceStatus(object):

    def __init__(self, status_dict: Dict, alive_window: int = 20) -> None:
        self.status = status_dict
        self.bar = '❘'
        self.alert_threshold = 0.8
        self.alive_windown = alive_window

    def get_status(self) -> str:
        return cf.fp.green('RUNNING')

    def get_uptime(self) -> str:
        return self.status['uptime']

    def get_ip(self) -> str:
        return self.status['ipinfo'].get('ip', 'N/A')

    def get_location(self) -> str:
        ipinfo = self.status['ipinfo']
        return '{},{}'.format(ipinfo.get('city', 'N/A'),
                              ipinfo.get('country', 'N/A'))

    def get_cpu(self) -> str:
        cpu = self.status['cpu']
        return self._draw_bar(cpu) + '({:.1f}%)'.format(cpu * 100)

    def _draw_bar(self, ratio: float) -> str:
        import math
        ceiled = math.ceil(ratio * 10)
        if ratio > self.alert_threshold:
            return cf.fp.red(self.bar * ceiled) + self.bar * (10 - ceiled)
        return cf.fp.green(self.bar * ceiled) + self.bar * (10 - ceiled)

    def get_disk(self) -> str:
        usage = self.status['disk']
        ratio = usage['used'] / usage['total']
        bar_info = self._draw_bar(ratio)
        extra_info = '({}%,{:.1f})'.format(int(100 * ratio),
                                           usage['total'] / (1 << 30))
        return bar_info + extra_info

    def get_mem(self) -> str:
        usage = self.status['mem']
        ratio = usage['used'] / usage['total']
        bar_info = self._draw_bar(ratio)
        extra_info = '({}%,{:.1f})'.format(int(100 * ratio),
                                           usage['total'] / (1 << 30))
        return bar_info + extra_info

    def get_last_active(self) -> str:
        return self.status['datetime']

    def display(self):
        status = self.get_status()
        name = self.status['hostname']
        uptime = self.get_uptime()
        ip = self.get_ip()
        location = self.get_location()
        mem = self.get_mem()
        disk = self.get_disk()
        last_active = self.get_last_active()
        print('{:<17} {:<13} {:<10} {:<15} {:<16} {:<30} {:<30} {}'.format(
            status, name[:12], uptime, ip, location, disk, mem, last_active))


class DataReporter(object):

    def __init__(self, input_data: List[Activity]):
        self.data = input_data

    def report_by_host(self, hostname: str,
                       activities: List[Activity]) -> dict:
        activities.sort(key=lambda x: x.datatime, reverse=True)
        cpu_usage = round(activities[0].status_dict['cpu'], 2)
        uptime = activities[0].status_dict['uptime'].split(',')[0].split(
            'up')[1]
        ipinfo = activities[0].status_dict['ipinfo']
        memory = activities[0].status_dict['mem']
        disk = activities[0].status_dict['disk']
        last_update = activities[0].datatime
        diff_seconds = (pd.Timestamp('now') -
                        pd.to_datetime(last_update)).seconds - 3600 * 8
        last_update = (pd.to_datetime(last_update) +
                       pd.DateOffset(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        status_dict = {
            'cpu': cpu_usage,
            'uptime': uptime,
            'ipinfo': ipinfo,
            'mem': memory,
            'disk': disk,
            'datetime': "{}(+{})".format(last_update, diff_seconds),
            'hostname': hostname
        }
        return status_dict

    def process(self) -> dict:
        print('{:<8} {:<14} {:<9} {:<15} {:<16} {:<30} {:<30} {}'.format(
            'STATUS', 'NAME', 'UPTIME', 'IP', 'LOCATION', cf.fp.cyan('DISK'),
            cf.fp.cyan('MEM'), 'LAST_ACTIVE'))
        for hostname, activities in self.data:
            report = self.report_by_host(hostname, activities)
            device = DeviceStatus(report)
            device.display()


def client():
    loop = asyncio.get_event_loop()
    resp = loop.run_until_complete(load_data('vpsstatus'))
    print('')
    data = DataReader(resp).process()
    DataReporter(data).process()
    print('')
