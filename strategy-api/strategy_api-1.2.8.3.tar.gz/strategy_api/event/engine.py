# -*- coding:utf-8 -*-
# @Date: 2022-11-01
# @author: 邓大大
# @Desc: winTrader 框架的事件驱动框架。
# @Notice: 事件引擎开始后, 默认启动了一个 计时器
from collections import defaultdict
from queue import Empty, Queue
from threading import Thread
import time
from typing import Any, Callable, List

EVENT_TIMER = "eTimer"
EVENT_TICK = "eTick"
EVENT_BAR = "eBar"
EVENT_ORDER = "eOrder"


# 事件对象
# 由使用的类型字符串组成,通过事件引擎分发事件，以及一个数据
class Event:

    def __init__(self, type: str, data: Any = None) -> None:
        """"""
        self.type: str = type
        self.data: Any = data


# 定义要在事件引擎中使用的处理函数。
HandlerType: callable = Callable[[Event], None]


# 事件引擎
# 1、根据其类型分发事件对象给那些注册的处理程序。
# 2、它还按间隔秒生成计时器事件，可用于计时目的： 定时器事件默认每 1 秒生成一次，如果未指定间隔。
class EventEngine:

    def __init__(self, interval: int = 1) -> None:
        self._interval: int = interval
        self._queue_order: Queue = Queue()
        self._queue_tick: Queue = Queue()
        self._queue_bar: Queue = Queue()
        self._queue_time: Queue = Queue()
        self._active: bool = False
        self._timer: Thread = Thread(target=self._run_timer)

        self._timer_er: Thread = Thread(target=self._run_timer_er)
        self._barer: Thread = Thread(target=self._run_bar)
        self._ticker: Thread = Thread(target=self._run_tick)
        self._order_er: Thread = Thread(target=self._run_order)

        self._order_handlers: defaultdict = defaultdict(list)  # 特殊方法对应不同事件类型
        self._bar_handlers: defaultdict = defaultdict(list)  # 特殊方法对应不同事件类型
        self._tick_handlers: defaultdict = defaultdict(list)  # 特殊方法对应不同事件类型
        self._time_handlers: defaultdict = defaultdict(list)  # 特殊方法对应不同事件类型

    def _run_timer_er(self) -> None:
        while self._active:
            try:
                event: Event = self._queue_time.get(block=True, timeout=1)
                # 注册的每个方法都一次处理该对象
                [handler(event) for handler in self._time_handlers[event.type]]
            except Empty:
                pass

    def _run_order(self) -> None:
        while self._active:
            try:
                event: Event = self._queue_order.get(block=True, timeout=1)
                # 注册的每个方法都一次处理该对象
                [handler(event) for handler in self._order_handlers[event.type]]
            except Empty:
                pass

    def _run_bar(self) -> None:
        while self._active:
            try:
                event: Event = self._queue_bar.get(block=True, timeout=1)
                # 注册的每个方法都一次处理该对象
                [handler(event) for handler in self._bar_handlers[event.type]]
            except Empty:
                pass

    def _run_tick(self) -> None:
        while self._active:
            try:
                event: Event = self._queue_tick.get(block=True, timeout=1)
                # 注册的每个方法都一次处理该对象
                [handler(event) for handler in self._tick_handlers[event.type]]
            except Empty:
                pass

    # 定时事件put
    def _run_timer(self) -> None:
        while self._active:
            time.sleep(self._interval)
            event: Event = Event(EVENT_TIMER)
            self.put(event)

    # 开始事件引擎
    def start(self):
        self._active = True
        self._timer.start()

        self._ticker.start()
        self._barer.start()
        self._order_er.start()
        self._timer_er.start()

    # 停止事件引擎
    def stop(self):
        self._active = False
        self._timer.join()

        self._ticker.join()
        self._barer.join()
        self._order_er.join()
        self._timer_er.join()

    # 事件对象加入到事件队列中待处理
    def put(self, event: Event) -> None:
        if event.type == EVENT_TIMER:
            self._queue_time.put(event)
        elif event.type == EVENT_ORDER:
            self._queue_order.put(event)
        elif event.type == EVENT_TICK:
            self._queue_tick.put(event)
        elif event.type == EVENT_BAR:
            self._queue_bar.put(event)

    # 事件注册
    def register(self, type: str, handler: HandlerType) -> None:
        if type == EVENT_BAR:
            handler_list: list = self._bar_handlers[type]
        elif type == EVENT_TICK:
            handler_list: list = self._tick_handlers[type]
        elif type == EVENT_ORDER:
            handler_list: list = self._order_handlers[type]
        else:
            handler_list: list = self._time_handlers[type]
        if handler not in handler_list:
            handler_list.append(handler)

    # 事件注销
    def unregister(self, type: str, handler: HandlerType) -> None:
        if type == EVENT_BAR:
            handler_list: list = self._bar_handlers[type]
        elif type == EVENT_TICK:
            handler_list: list = self._tick_handlers[type]
        elif type == EVENT_ORDER:
            handler_list: list = self._order_handlers[type]
        else:
            handler_list: list = self._time_handlers[type]

        if handler in handler_list:
            handler_list.remove(handler)
