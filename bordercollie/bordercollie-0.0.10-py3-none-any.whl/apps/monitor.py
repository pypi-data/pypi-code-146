#!/usr/bin/env python3

import time

import codefast as cf
import pandas as pd

from bordercollie.utils import post_to_lark


def depthwatch(nsqd: str = 'http://localhost:4151', topics: str = 'test'):
    print('monitoring topic: ', topics)
    if not nsqd.startswith(('http', 'https')):
        nsqd = 'http://' + nsqd

    pres = [0] * len(topics)
    topics_map = {t: i for i, t in enumerate(topics)}
    pre_messages = {}

    while True:
        js = cf.net.get(f'{nsqd}/stats?format=json').json()
        for j in js['topics']:
            topicname = j['topic_name']
            if topicname not in topics: continue

            channel_list = j['channels']
            for chan in channel_list:
                depth = int(chan['depth'])
                name = chan['channel_name']
                predepth = pres[topics_map[topicname]]
                diff = depth - predepth
                pres[topics_map[topicname]] = depth
                if diff > 0:
                    diff = '+' + str(diff)
                msg = f'{name:<30} {depth:<10} ({diff})'
                if msg != pre_messages.get(name):
                    print(msg)
                pre_messages[name] = msg
        time.sleep(1)


def nsqtopic(webhook: str, max_depth: int = 100, nsqd:str='localhost:4151'):
    """nsq topic monitor"""
    url = 'http://{}/stats?format=json'.format(nsqd)
    print(url)

    js = cf.net.get(url).json()
    messages = []

    for j in js['topics']:
        channel_list = j['channels']
        for chan in channel_list:
            depth = int(chan['depth'])
            name = chan['channel_name']
            if depth > max_depth:
                messages.append('NSQ channel {} 当前队列长度为 {}，请留意系统状态。'.format(
                    name, depth))
    if messages:
        cur_time = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        messages = [cur_time] + messages
        msg = '\n'.join(messages)
        post_to_lark(webhook, msg)
