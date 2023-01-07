'''Generic observer/notifier super-class.'''

import asyncio
import logging
from typing import Any

VERBOSE_DEBUG = False


class Observer:
    '''Super class for an Observer class.

    The observer must use notifer.subscribe() and
    notifier.unsubscribe() messages to ensure that
    notify() messages will be received.'''

    def __init__(self):
        '''Initialise an Observer with a local queue.'''

        self._notifier_queue: asyncio.Queue = asyncio.Queue()

        super().__init__()

    async def notify(self, notifier):
        '''Receive a notification of a new message from
        notifier instance.  Pull the data off the notifier's
        queue and store in the local queue.'''

        message = await notifier.get(self)
        await self._notifier_queue.put(message)


class Notifier:
    '''Super class for a Notifier class.

    The notifier receives subscribe() and unsubscribe()
    messages to register interested observers.

    The notifier sends a notify() to observers when
    data exists and then receives a get() to pop the
    data from queue.'''

    def __init__(self):
        '''Initialise a Notifier with a local queue.'''

        self._logger = logging.getLogger('ac-ws.notifier')

        self._observer = {}
        self._observer_queues = {}

        super().__init__()

    async def get(self, observer: Any):
        '''
        Fetch an item from the queue.  Returns None if the queue is empty.
        Uses the observer value to index the correct queue.
        '''
        # pylint: disable=logging-fstring-interpolation

        try:
            response = self._observer_queues[id(observer)].get_nowait()
        except asyncio.QueueEmpty:
            response = None

        if VERBOSE_DEBUG:
            self._logger.debug(f'get({observer}) -> {response})')

        return response

    async def put(self, item, observer: Any = None):
        '''
        Put an item on a specific local queue and notify observer
        (if given) or all observers if None'''
        # pylint: disable=consider-using-dict-items, consider-iterating-dictionary, logging-fstring-interpolation

        if VERBOSE_DEBUG:
            self._logger.debug(f'put(self, {item}, {observer})')

        if observer:
            await self._observer_queues[id(observer)].put(item)
            await self._observer[id(observer)].notify(self)
        else:
            for key in self._observer_queues.keys():
                await self._observer_queues[key].put(item)
            for key in self._observer.keys():
                await self._observer[key].notify(self)

    def subscribe(self, observer):
        '''Subscribe an observer object for state changes.   Create a new queue per observer.
        Observer object must include an async notify(self, observable, *args, **kwargs) method.'''
        self._observer_queues[id(observer)] = asyncio.Queue()
        self._observer[id(observer)] = observer

    def unsubscribe(self, observer):
        '''Unsubscribe an observer object.'''
        try:
            del self._observer_queues[id(observer)]
            del self._observer[id(observer)]
        except ValueError:
            pass


class ObserverNotifier(Observer, Notifier):
    '''Super class that is both an Observer and Notifier.'''

    def __init__(self):
        # pylint: disable=useless-super-delegation
        super().__init__()
