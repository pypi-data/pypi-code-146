#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File        : stage.py
@Description : 用于各工序的基类
@Date        : 2020/11/10 13:25:48
@Author      : merlinbao
@Version     : 1.0
"""

from time import time

from .stage import Stage
from .. import utils


class Flow:

    def __init__(self, *stages, **kwargs):
        self.timing = kwargs.get('timing', False)

        # 填充__stages列表和__named_stages字典
        self.__stages = []
        self.__named_stages = {}

        for stage in stages[0]:
            if isinstance(stage, Stage):
                self.__stages.append(stage)

                type_ = stage.__class__.__name__
                num_prev = sum([type_ in name for name in self.__named_stages])
                if num_prev == 0:       # 前面没有，则直接加入当前Stage
                    self.__named_stages[type_] = stage
                elif num_prev == 1:     # 前面只有一个，则前面的修改序号为1，当前的序号为2
                    self.__named_stages[type_ + '1'] = self.__named_stages.pop(type_)
                    self.__named_stages[type_ + '2'] = stage
                else:                   # 前面多余两个，则序号直接递增
                    self.__named_stages[f'{type_}{num_prev + 1}'] = stage

    @classmethod
    def from_config(cls, config, **kwargs):
        # check config
        if not config:
            raise ValueError("Flow config is empty.")

        # get gpu_id
        if "gpu_id" in kwargs:
            gpu_id = kwargs["gpu_id"]
        else:
            gpu_id = 0

        # instantiate stages
        stages = []
        for cf in config:
            # 按照配置实例化类
            type_ = cf['type']
            cls_ = Stage.registory[type_]
            stages.append(cls_(params=cf.get('params', {}), gpu_id=gpu_id))

        return cls(stages, **kwargs)

    @property
    def stages(self):
        return self.__stages
    
    @property
    def named_stages(self):
        return self.__named_stages

    def __call__(self, feed_dict):
        if self.timing:
            print(utils.wrap_title('Time Consuming:'))

        for name, stage in self.__named_stages.items():
            if self.timing: T = time()
            stage(feed_dict)
            if self.timing:
                T = time() - T
                print(name.rjust(25) + ' : ' + f'{T*1000:9.4f} (ms)')

    def __str__(self):
        # append head
        main_str = self.__class__.__name__ + "\n"
        main_str += "(\n"

        # append child name
        for stage in self.__stages:
            main_str += " " * 4 + str(stage) + ",\n"

        # append tail
        main_str += ")\n"

        return main_str
