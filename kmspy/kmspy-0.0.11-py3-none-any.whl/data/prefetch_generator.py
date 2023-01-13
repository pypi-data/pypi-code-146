from __future__ import annotations

from collections import OrderedDict
from itertools import cycle, count
import logging
from multiprocessing import Process, Queue, SimpleQueue
import queue
import random
from threading import Thread
import time
import traceback as tb
from typing import Any, Callable, Dict, Iterable, Optional


from ..utils import make_partial


logger = logging.getLogger(__name__)
_counter = count(1)


class NoOutput(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PrefetchUnit(Process):
    def __init__(self, num_prefetch: int, gid: int, ignore_error: bool, processing_func: Optional[Callable[[Any], Any]] = None):
        """Prefetch Generator
        
        Args:
            num_prefetch (int): prefetch 개수
            gid (int): generator id
            processing_func (Callable): (Optional) 데이터 처리 함수
        """
        Process.__init__(self, name=f"PrefetchUnit-{gid}")
        self.data = SimpleQueue()
        self.queue = Queue(maxsize=num_prefetch)
        self.num_prefetch = num_prefetch
        self.gid = gid
        self.ignore_error = ignore_error
        self.processing_func = processing_func
        self.daemon = True
        self.start()

    def put(self, data):
        self.data.put(data)

    def run(self):
        idx = 0
        while True:
            item = self.data.get()
            if item is StopIteration:
                self.queue.put((StopIteration, self.gid, idx, True))
                self.data.close()
                self.queue.close()
                return
            else:
                try:
                    item = item if self.processing_func is None else self.processing_func(item)
                    self.queue.put((item, self.gid, idx, False))
                    idx += 1
                except Exception as e:
                    if self.ignore_error:
                        self.queue.put((tb.format_exc(), self.gid, idx, True))
                        idx += 1
                    else:
                        self.queue.put((tb.format_exc(), self.gid, idx, True))
                        self.data.close()
                        self.queue.close()
                        return


class PrefetchGenerator(Thread):
    """데이터를 병렬로 처리하는 generator

    Args:
        iterable (Iterable): iterable 데이터. (dict는 key만 사용되므로 주의. dict.items()와 같은 형태로 사용할 것)
        num_prefetch (int): prefetch 개수
        num_workers (int): 최대 Process 수. num_prefetch보다 작은 경우 num_prefetch와 같은 값으로 변경됨
        ordered (bool): 데이터 순서를 유지할 것인지(기본값=True)
        shuffle (bool): 데이터를 섞을 것인지(기본값=False). ordered = True 인 경우, shuffle은 항상 False
        processing_func (Callable): (Optional) 데이터 처리 함수
        func_args: processing_func의 인자
        func_kwargs: processing_func의 키워드 인자
    """
    def __init__(self, iterable: Iterable, num_prefetch: int = 1, num_workers: int = 1, ordered: bool = True, shuffle: bool = False, name: Optional[str] = None, ignore_error: bool = True, processing_func: Optional[Callable[[Any], Any]] = None, func_kwargs: Optional[Dict[str, Any]] = {}) -> None:
        if name is None:
            name = f"PrefetchGenerator-{_counter.__next__():d}"
        Thread.__init__(self, name=name)
        self._reset_states()
        self.iterable = iterable
        self.shuffle = shuffle
        if self.shuffle:
            self.ordered = False 
        else:
            self.ordered = ordered
        self.num_workers = min(num_prefetch, num_workers)
        self.num_prefetch = num_prefetch
        self._ignore_error = ignore_error
        self.processing_func = make_partial(processing_func, **func_kwargs)
        self._continue = True
        self._is_running = True
        self._units = self.make_units()
        self.daemon = True
        self.start()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        # TODO: 필요하지 않은 것 같아서 주석처리
        # 이상 없으면 다음 버전에서 삭제할 것
        # while self._continue and self.results:
        #     time.sleep(0.01)
        self.stop()

    def _reset_states(self):
        """iteration 상태를 초기화"""
        # self.results에 전처리가 끝난 데이터를 {index: item} 형태로 저장
        # ordered=True 이면 self._next_idx를 0부터 차례로 증가시키며 데이터를 꺼냄
        # ordered=False 이면 self._next_idx는 사용되지 않으며, 데이터 처리가 끝난 순서대로 데이터를 꺼냄

        # self._pendding=True이면 PrefetchUnit에서 데이터를 꺼내야하는 상태를 의미함

        # self._stoped_units는 데이터 처리가 끝난 PrefetchUnit의 개수를 의미하며,
        # self._stoped_units와 self.num_workers가 같아지면 모든 unit의 작업이 끝난 것을 의미함
        self.results = OrderedDict()
        self._next_idx = 0
        self._pendding = False
        self._stoped_units = 0

    def make_units(self) -> Dict[int, PrefetchUnit]:
        """self.num_workers만큼 PrefetchUnit 생성
        
        여러 유닛에 데이터를 순차적으로 할당
        iterable = [1, 2, 3, 4], num_workers = 2 인 경우,
        unit1에는 [1, 3], unit2에는 [2, 4]가 할당됨

        Returns:
            (Dict[int, PrefetchUnit]): gid(PrefetchUnit의 번호)를 key로 가지는 dictionary
        """

        def assign(iterable, units):
            if hasattr(iterable, "__len__") and self.shuffle:
                iterable = iterable[:]
                random.shuffle(iterable)
            num_units = len(units)

            for idx, item in enumerate(iterable):
                if self._is_running:
                    units[idx % num_units].put(item)
                else:
                    break
                
            # stop이 호출된 경우
            # unit에 있는 queue를 비우고 데이터 할당을 중단
            if not self._is_running:
                for unit_id, unit in units.items():
                    while unit.data.empty():
                        unit.data.get()

            # 데이터 할당이 끝났다는 것을 알려줌
            for unit in units.values():
                unit.put(StopIteration)

        num_prefetch_each_workers = max(self.num_prefetch//self.num_workers + (1 if self.num_prefetch%self.num_workers != 0 else 0) -1, 1)
        units = {gid: PrefetchUnit(num_prefetch_each_workers, gid, self._ignore_error, self.processing_func) for gid in range(self.num_workers)}
        _assign = Thread(target=assign, args=(self.iterable, units), name="Assign")
        _assign.daemon = True
        _assign.start()
        return units

    def run(self):
        """여러 PrefetchUnit에서 데이터를 꺼냄
        
        유닛에서 데이터를 꺼내서 self.results에 저장
        """
        def _run():
            # 한 번의 iteration을 처리하는 함수
            # 새로운 iteration을 의미하므로 self._reset_states()를 호출해서 상태 초기화

            # unit의 작업이 끝났다고해서 iteration이 종료되는 것은 아니며,
            # self.results에 저장해놓은 데이터까지 소진해야 완전히 종료됨

            # unit의 작업이 끝나고, self.results가 빈 경우 self._continue = False로 만듦
            # self._continue는 iteration을 종료하는 조건으로 사용됨

            while not self._continue:
                # 다음 iter가 시작될 때까지 대기
                if not self._is_running:
                    # stop이 호출된 경우에는 종료
                    self._continue = False
                    return
                else:
                    time.sleep(0.1)

            self._reset_states()
            _c = cycle(range(self.num_workers))  # 데이터를 꺼낼 PrefetchUnit의 index를 순차적으로 출력
            while self._stoped_units < self.num_workers and self._is_running:
                try:
                    if self._pendding:
                        # item: 데이터
                        # gid: unit의 번호
                        # idx: unit 내부의 몇 번째 데이터인지
                        # err: 오류 여부. 오류가 아니면 False
                        item, gid, idx, err = self._units[next(_c)].queue.get_nowait()

                        # 전체 데이터에서의 index 계산
                        total_idx = gid+idx*self.num_workers
                        if not err:
                            self.results[total_idx] = item
                        else:
                            if item is StopIteration:
                                # unit 하나가 종료됨
                                self._stoped_units += 1
                                self._units[gid].terminate()
                            else:
                                if self._ignore_error:
                                    self.results[total_idx] = NoOutput
                                    logger.warning(item)
                                else:
                                    logger.error(item)
                                    self._continue = False
                                    raise item
                    else:
                        # self._pendding=True가 될때까지, 즉 __next__가 수행될때까지 대기
                        # unit에서 데이터 처리는 정상적으로 수행되고 있음
                        time.sleep(0.01)
                except queue.Empty:
                    # unit에서 꺼낼 데이터가 없음
                    # 잠깐 대기
                    time.sleep(0.01)
                except Exception as e:
                    logger.debug(f"UnknownError {e.__class__.__name__}: {e.args[0] if e.args else None}", exc_info=True)
                    pass
            self._continue = False

        while self._is_running:
            _run()

    def stop_units(self):
        for gid, unit in self._units.items():
            self._stoped_units = min(self._stoped_units+1, len(self._units))
            unit.terminate()

    def stop(self):
        """PrefetchGenerator thread 종료"""
        self._is_running = False
        self._continue = False
        self.stop_units()

    def __next__(self):
        while True:
            if not self._is_running:
                # run이 완료되지 않은 상태에서 self.stop()이 호출된 경우
                # 작업중인 unit을 모두 종료하고 StopIteration을 일으킨다.
                [_unit.terminate() for _unit in self._units.values()]
                raise StopIteration
            if not self._continue and not self.results:
                # iteration이 정상적으로 한 번 끝난 경우
                # results에서 꺼낼 데이터도 없고, unit도 모두 종료된 상태
                raise StopIteration
            if (self._next_idx in self.results if self.ordered else self.results):
                # self.ordered=True 이면, self.results에서 next_idx를 꺼내고
                # self.ordered=False 이면, popitem(False)로 가장 오래된 데이터부터 꺼냄
                item = self.results.pop(self._next_idx) if self.ordered else self.results.popitem(False)[1]
                if item is NoOutput:
                    self._next_idx +=1
                    continue
                else:
                    self._pendding = False
                    self._next_idx +=1
                    return item
            else:
                # unit에서 데이터가 준비될때까지 대기하기 위해서 진입하는 조건문
                # sleep이 없는 경우 불필요하게 자원을 많이 사용할 수 있어서 제약을 둠
                self._pendding = True
                time.sleep(0.01) 
          
    def __iter__(self):
        # self._continue=False인 경우는, iter가 한 번 실행된 이후를 의미함
        # unit을 다시 만듦
        if self._is_running:
            if not self._continue:
                self._continue = True
                self._units = self.make_units() 
            return self
        else:
            raise ValueError("This is a terminated thread.")
