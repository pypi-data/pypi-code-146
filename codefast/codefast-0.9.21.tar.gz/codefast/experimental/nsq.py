#!/usr/bin/env python3
from typing import List

import nsq


def create_reader(topic: str, channel: str, message_handler: callable,
                  lookupd_http_addresses: List[str],
                  nsqd_top_addresses: List[str]):
    return nsq.Reader(message_handler=message_handler,
                      lookupd_http_addresses=lookupd_http_addresses,
                      nsqd_tcp_addresses=nsqd_top_addresses,
                      topic=topic,
                      channel=channel,
                      lookupd_poll_interval=3,
                      max_in_flight=10)
