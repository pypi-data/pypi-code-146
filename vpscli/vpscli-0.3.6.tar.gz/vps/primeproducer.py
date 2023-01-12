import random
import time
import os

import codefast as cf
import requests
from dofast.client import parse_traffic

from enum import Enum, auto
import json, subprocess
from uuidentifier import snowflake

cf.logger.level = 'info'


class Action(Enum):
    MORE = auto()
    LESS = auto()
    NOTSURE = auto()


class TrafficMonitor:
    def __init__(self,
                 interface: str,
                 init_day: str,
                 total_volume: int,
                 traf_type: str = 'tx'):
        self.interface = interface
        self.init_day = init_day
        self.total_volume = total_volume
        self.traf_type = traf_type
        self.previous_volume = self.get_previous_consumed()
        self.counter = 0

    def get_previous_consumed(self) -> float:
        consumed = subprocess.check_output('vnstat --json d',
                                           shell=True).decode('utf-8').strip()
        consumed = json.loads(consumed)
        traffic = parse_traffic(consumed, self.interface, self.init_day)
        resp = traffic[self.traf_type]
        cf.info('previously all consumed volume is {}'.format(resp))
        return resp

    def need_consume_more(self) -> Action:
        '''To consumer more traffic or not
        return: Action
        More: consume more traffic
        Less: consume less traffic
        NotSure: not sure
        '''
        self.counter += 1
        if self.counter < 3600:
            return Action.NOTSURE
        self.counter = 0
        volume = self.get_previous_consumed()
        dummy, self.previous_volume = self.previous_volume, volume
        today = int(time.strftime("%d"))
        remain_hours = 24 - int(time.strftime(
            "%H")) + (int(self.init_day) + 30 - today - 1) % 30 * 24
        volume_diff = self.total_volume - volume - (volume -
                                                    dummy) * remain_hours
        cf.info('already consumed volume: {}, consumed in previous hour is {}'.
                format(volume, volume - dummy))
        cf.info('estimated volume diff in the end is {}'.format(volume_diff))
        return Action.MORE if volume_diff > 0 else Action.LESS


class Producer:
    THRESHOLD = 0.6  # keep consumer working at 60% time
    PUB_URL = 'http://localhost:4151'
    TOPIC = 'primes'
    CHANNEL = 'calculate_prime'
    busy_count = 1
    total_count = 1
    task_batch_size = 10  # change dynamically
    increase_step = 1
    descrase_step = 0.3
    min_size = 10
    tm = TrafficMonitor('eth0', '23', 500)
    redudant_size = 1 << 10

    def create_task(self):
        cf.info(
            'creating task: busy time count {}, total count {}, ratio {:.4f}, task generating speed {:.2f}/s, data redudant size {} bytes'
            .format(self.busy_count, self.total_count,
                    self.busy_count / self.total_count, self.task_batch_size,
                    self.redudant_size))

        for _ in range(int(self.task_batch_size)):
            n = random.randint(1 << 41, 1 << 53)
            redundant = ''.join(
                hex(c)[2:] for c in os.urandom(self.redudant_size))

            requests.post('{}/pub?topic={}'.format(self.PUB_URL, self.TOPIC),
                          json={
                              'number': n,
                              'rdd': redundant,
                              'uuid': snowflake.uuid()
                          })

    def is_too_busy(self) -> bool:
        '''busy ration exceeds threshold or not'''
        return (self.busy_count / self.total_count) > self.THRESHOLD

    def is_queue_empty(self) -> bool:
        '''whether queue is empty'''
        stats = requests.get('{}/stats?format=json'.format(
            self.PUB_URL)).json()
        topic = next(
            (e for e in stats['topics'] if e['topic_name'] == self.TOPIC),
            None)
        channel = next(
            (e
             for e in topic['channels'] if e['channel_name'] == self.CHANNEL),
            None)
        return int(channel['depth']) == 0

    def adjust_redudant_size(self):
        '''adjust redudant size'''
        xtion = self.tm.need_consume_more()
        if xtion == Action.MORE:
            self.redudant_size = max(self.redudant_size + 100, 20)
            cf.info('increase redudant size to {}'.format(self.redudant_size))
        elif xtion == Action.LESS:
            self.redudant_size = min(self.redudant_size - 20, 1 << 20)
            cf.info('decrease redudant size to {}'.format(self.redudant_size))

    def run(self):
        while True:
            time.sleep(1)
            self.adjust_redudant_size()
            if not self.is_queue_empty():
                self.busy_count += 1
            self.total_count += 1
            if not self.is_too_busy():
                self.create_task()
                self.task_batch_size += self.increase_step
            else:
                self.task_batch_size -= self.descrase_step
                self.task_batch_size = max(self.task_batch_size, self.min_size)

def entry():
    Producer().run()
