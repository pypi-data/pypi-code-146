#!/usr/bin/env python
import time
from threading import Thread
from typing import Any, Callable, Dict, List, Tuple

from codefast import error, info


class CronDateTime(object):
    """ 定时任务时间解析
    """
    def __init__(
        self,
        year: str,
        month: str,
        day: str,
        hour: str,
        minute: str,
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def __str__(self):
        return '{}-{}-{} {}:{}'.format(self.year, self.month, self.day,
                                       self.hour, self.minute)

    def __repr__(self):
        return self.__str__()

    def is_time_to_run(self) -> bool:
        now = time.localtime()
        itmap = self.invoke_time_map
        return now.tm_year in itmap['year'] and \
            now.tm_mon in itmap['month'] and \
            now.tm_mday in itmap['day'] and \
            now.tm_hour in itmap['hour'] and \
            now.tm_min in itmap['minute']

    @property
    def invoke_time_map(self) -> Dict[str, List[int]]:
        ATTR_UPBOUND = {
            'year': 2999,
            'month': 12,
            'day': 31,
            'hour': 23,
            'minute': 59,
        }
        return dict((attr, self.get_runtime_list(getattr(self, attr), bound))
                    for attr, bound in ATTR_UPBOUND.items())

    def get_runtime_list(self, runtime: str, upbound: int) -> List[int]:
        if runtime == '*' or runtime == '':
            return list(range(1, upbound + 1))
        elif ',' in runtime:
            return [int(i) for i in runtime.split(',')]
        elif '-' in runtime:
            start, end = runtime.split('-')
            return list(range(int(start), int(end) + 1))
        elif '/' in runtime:
            start, step = runtime.split('/')
            return list(range(0, upbound + 1, int(step)))
        else:
            return [int(runtime)]


class BackgroundScheduler(Thread):
    def __init__(self,
                 interval: int = 10,
                 trigger: str = 'interval',
                 name: str = 'BackgroundScheduler',
                 hour: str = '',
                 minute: str = '',
                 day: str = '',
                 month: str = '',
                 year: str = ''):
        """ 定时任务调度器
        支持两种触发方式：interval 和 cron。
        interval: 按照固定的时间间隔执行任务
        cron: 按照 cron 表达式执行任务。
        支持格式：TODO
        """
        super(BackgroundScheduler, self).__init__()
        self.daemon = True
        self.interval = interval
        self.terminate = False
        self.jobs = []
        self.name = name
        self.trigger = trigger
        self.cdt = CronDateTime(year, month, day, hour, minute)

    def add_job(self, job: Callable, args: List[Any] = [], kwargs: dict = {})->'Self':
        self.jobs.append(job)
        return self

    def _is_interval_trigger(self) -> bool:
        return self.trigger == 'interval'

    def _run_jobs_once(self):
        for job in self.jobs:
            try:
                job()
            except Exception as e:
                error(e)

    def run(self):
        class_name = self.__class__.__name__
        while not self.terminate:
            if self._is_interval_trigger():
                self._run_jobs_once()
                msg = {
                    'class_name':
                    class_name,
                    'next run time':
                    time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(time.time() + self.interval))
                }
                info(msg)
                time.sleep(self.interval)
            else:
                if self.cdt.is_time_to_run():
                    msg = {
                        'class_name':
                        class_name,
                        'now':
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                    }
                    info(msg)
                    self._run_jobs_once()
                time.sleep(60)
        return self

    def join(self):
        info("{} join()".format(self.name))
        self.terminate = True
        super(BackgroundScheduler, self).join()
