from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from MyThread import decorator_thread


class ThreadPool(metaclass=ABCMeta):
    def __init__(self, produce=5, consume=7, qsize=0):

        self._qsize = qsize  # 队列大小
        self._produce = produce  # 生产者数量
        self._consume = consume  # 消费者数量

        self.timeout = 3  # 超时断开
        self.qsize_show = True  # 是否显示队列大小
        print(f'生产者:[{self._produce }] 消费者:[{self._consume}] 队列大小:[{self._qsize}] '
              f'是否显示队列[{self.qsize_show}] '
              f'超时断开:[{self.timeout}]秒')
        self.q = Queue(self._qsize)

        self.pool2 = ThreadPoolExecutor(self._consume)
        self.pool1 = ThreadPoolExecutor(self._produce)
        self.run()

    def run(self):
        self.t1()
        for _ in range(self._consume):
            self.t2()

    @decorator_thread
    def t1(self):
        for data in self.turn_pages():
            if isinstance(data, list):
                for i in data:
                    self.q.put(self.pool1.submit(self.get_data, i))
            else:
                self.q.put(self.pool1.submit(self.get_data, data))

    def t2(self):
        while True:
            if self.qsize_show:
                print(f'目前队列大小{self.q.qsize()}')
            try:
                data1 = self.q.get(timeout=self.timeout).result()
                for d in data1:
                    self.pool2.submit(self.save_data, d)
            except Exception as e:
                print(f'超时{self.timeout}s,程序结束:{e}')
                break

    @abstractmethod
    def turn_pages(self):
        pass

    @abstractmethod
    def get_data(self, args):
        pass

    @abstractmethod
    def save_data(self, args):
        pass
