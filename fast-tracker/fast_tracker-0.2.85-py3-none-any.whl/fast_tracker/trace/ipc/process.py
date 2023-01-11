#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""

from multiprocessing import Process

from fast_tracker import config, agent


class FastProcess(Process):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *,
                 daemon=None):
        super(FastProcess, self).__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._fast_config = config.serialize()

    def run(self):
        if agent.started() is False:
            config.deserialize(self._fast_config)
            agent.start()
        super(FastProcess, self).run()
