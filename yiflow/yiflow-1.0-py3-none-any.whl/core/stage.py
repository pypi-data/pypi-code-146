#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File        : stage.py
@Description : 用于各工序的基类
@Date        : 2020/11/10 13:25:48
@Author      : merlinbao
@Version     : 1.0
"""


from abc import abstractmethod


class MetaStage(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        if not hasattr(cls, "registory"):
            # this is the base class
            cls.registory = {}
        else:
            # this is the subclass
            cls.registory[name] = cls


class Stage(object, metaclass=MetaStage):

    def __init__(self, params=None, **kwargs):
        self.serial = 1

        # parse params
        if params is not None:
            for k, v in params.items():
                setattr(self, k, v)

        # append other args
        for k, v in kwargs.items():
            setattr(self, k, v)

        # initialize
        self.setup()

    @abstractmethod
    def setup(self):
        raise NotImplementedError("`setup` method must be implemented!")

    @abstractmethod
    def run(self, feed_dict=None):
        raise NotImplementedError("`run` method must be implemented!")

    def __call__(self, feed_dict=None):
        return self.run(feed_dict)

    def __str__(self):
        return self.__class__.__name__
