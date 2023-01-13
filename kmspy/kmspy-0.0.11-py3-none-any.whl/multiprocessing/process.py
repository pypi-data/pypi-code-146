import logging
from multiprocessing import Process as mp_Process
from multiprocessing import Queue
import queue
import time
from typing import Any, Callable


logger = logging.getLogger(__name__)


class Process(mp_Process):
    def __init__(self, target: Callable[[Any], Any], *args, **kwargs):
        mp_Process.__init__(self)
        start = kwargs.pop("start", True)
        # logger.debug(f"{args=}, {kwargs=}")
        self.target = target  # 실행할 함수
        self.args = args  # 인자
        self.kwargs = kwargs  # 인자
        self._queue = Queue()  # 데이터 전달용
        self._done = Queue()  # subprocess 종료 신호 전달용
        self.daemon = kwargs.pop("daemon", False)
        if start:
            self.start()

    def run(self):
        # subprocess에서 실행됨
        # 입력 받은 인자로 함수 실행하고 self._queue에 실행 결과 넣기
        self._queue.put(self.target(*self.args, **self.kwargs))

        # main process에서 self._queue의 데이터를 꺼내기 전까지 대기
        while True:
            try:
                # self._done에 데이터가 들어있지 않으면 queue.Empty 오류 발생해서 break는 실행되지 않음
                # while-try-except 사용하지 않고 self._done.get() 사용해도 될듯
                self._done.get_nowait()
                break
            except queue.Empty:
                # 잠시 대기
                time.sleep(0.1)

    def _get_result(self):
        result = self._queue.get_nowait()
        # self._queue에 데이터가 들어있지 않으면 queue.Empty 오류 발생해서 아래는 실행되지 않음
        self._done.put(True)  # subprocess에 프로세스 종료 신호 보내기
        # queue 닫기
        # subprocess에서 닫지 않는 이유는 여기서 put을 실행해서 그런지 main process 쪽에 QueueFeederThread가 생김
        # queue를 닫지 않으면 main process에 찌꺼기 thread가 남음
        # 여기서 self._done을 닫아도 subprocess에는 데이터만 전송되고 여전히 self._done이 살아있는 상태
        # Queue.close()는 이 프로세스에서는 더 이상 사용하지 않겠다는 의미라고 함
        self._done.close()
        return result

    def result(self, nowait=False):
        # main process에서 실행됨
        if nowait:
            return self.result_nowait()
        else:
            while not self._done._closed and self.is_alive():
                try:
                    return self._get_result()
                except queue.Empty:
                    # 잠시 대기
                    time.sleep(0.1)

    def result_nowait(self):
        # main process에서 실행됨
        try:
            return self._get_result()
        except queue.Empty:
            return None
