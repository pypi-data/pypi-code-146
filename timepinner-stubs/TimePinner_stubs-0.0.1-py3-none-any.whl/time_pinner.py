# -*- coding:utf-8 -*-
from time import perf_counter
from typing import Union


class Pinner(object):
    """用于记录时间间隔的工具"""

    def __init__(self, pin: bool = False, show_everytime: bool = True) -> None:
        """初始化                                       \n
        :param pin: 初始化时是否记录一个时间点
        :param show_everytime: 是否每次记录时打印时间差
        """
        self.times = []
        self.show_everytime = show_everytime
        if pin:
            self.pin('起始点')

    @property
    def records(self) -> list:
        """返回所有时间差组成的列表"""
        return [(self.times[k][1] or f't{k}', self.times[k][0] - self.times[k - 1][0])
                for k in range(1, len(self.times)) if self.times[k][1] is not False]

    @property
    def winner(self) -> Union[tuple, None]:
        """返回最短的时间差"""
        ts = sorted(self.records, key=lambda x: x[1])
        return ts[0] if ts else None

    def pin(self, text: str = '', show: bool = None) -> tuple:
        """记录一个时间点                             \n
        :param show: 是否打印与上一个时间点的差
        :param text: 记录点说明文本
        :return: 返回与上个时间点的间隔
        """
        now = perf_counter()
        prev = self.times[-1][0] if self.times else now
        self.times.append((now, text))
        gap = now - prev

        if show is True or (self.show_everytime and show is None):
            p_text = f'{text}：' if text else ''
            print(f'{p_text}{gap}')

        return text, gap

    def skip(self) -> None:
        """跳过从上一个时间点到当前的时间"""
        self.times.append((perf_counter(), False))

    def show(self) -> None:
        """打印所有时间差"""
        for k in self.records:
            print(f'{k[0]}：{k[1]}')

    def clear(self) -> None:
        """清空已保存的时间点"""
        self.times = []
