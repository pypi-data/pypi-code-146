import asyncio
import logging
from collections import defaultdict
from datetime import datetime
import serial
from . import const
from .command import NooliteCommand
from typing import Callable
import typing

lg = logging.getLogger('noolite')
CbType = Callable[[NooliteCommand], typing.Any]


class NotApprovedError(Exception):
    pass


class Noolite:

    def __init__(
            self,
            tty_name: str,
            loop: typing.Optional[asyncio.AbstractEventLoop],
            anti_jitter: int = const.MOTION_JITTER,
    ):
        self.callbacks: typing.DefaultDict[int, typing.List[CbType]] = defaultdict(list)
        self._cmd_log: typing.Dict[int, datetime] = {}
        self._get_events = False
        self.event_que: asyncio.Queue[NooliteCommand] = asyncio.Queue()
        self.tty_name = tty_name
        self.tty = _get_tty(tty_name)
        # self.loop = asyncio.get_event_loop()
        self.loop.add_reader(self.tty.fd, self._handle_tty)
        self.wait_ftr: typing.Optional[asyncio.Future] = None
        self.wait_cmd: typing.Optional[NooliteCommand] = None
        self.send_lck = asyncio.Lock()
        self.anti_jitter = anti_jitter

    @property
    def loop(self):
        return asyncio.get_event_loop()

    def _handle_tty(self):
        """
        Хендлер входящих данных от адаптера
        :return:
        """
        try:
            while self.tty.in_waiting >= 17:
                in_bytes = self.tty.read_until(174, 17)
                if len(in_bytes) != 17:
                    lg.warning(f'received short message %f', list(in_bytes))
                resp = NooliteCommand(*(x for x in in_bytes))
                lg.debug(f'< %s', list(in_bytes))
                if self._cancel_waiting(resp):
                    return
                asyncio.create_task(self.handle_command(resp))
        except OSError:
            self.loop.remove_reader(self.tty.fd)
            self.loop.create_task(self.reconnect())

    async def reconnect(self):
        while True:
            lg.debug('reconnecting')
            try:
                self.tty = _get_tty(self.tty_name)
                self.loop.add_reader(self.tty.fd, self._handle_tty)
                return
            except Exception:
                lg.exception('while reconnecting')
            await asyncio.sleep(5)

    def _cancel_waiting(self, msg: NooliteCommand):
        """
        Отменяет ожидание подвтерждения, возвращает истину если ожидание было, ложь, если нет
        :return:
        """
        if isinstance(self.wait_ftr, asyncio.Future) \
                and msg.ch == self.wait_cmd.ch \
                and msg.mode == self.wait_cmd.mode:
            self.wait_ftr.set_result(True)
            lg.debug(f'{"Approved:".rjust(20, " ")} {self.wait_cmd}')
            return True
        else:
            return False

    async def _check_connection(self):
        while True:
            print(self.tty.readable())
            await asyncio.sleep(1)

    def callback(self, ch):
        """
        Декоратор, добавляет функцию в список колбэков канала
        :param ch:
        :return:
        """
        def deco(foo):
            self.callbacks[ch].append(foo)
            return foo
        return deco

    @property
    async def in_commands(self):
        """
        Возвращает пришедшие команды в бесконечном цикле
        :return:
        """
        self._get_events = True
        while True:
            yield await self.event_que.get()

    async def handle_command(self, resp: NooliteCommand):
        """
        При приеме входящего сообщения нужно вызвать этот метод

        :param resp:
        :return:
        """
        await asyncio.sleep(0.05)
        try:
            for cb in self.callbacks[resp.ch]:
                asyncio.create_task(cb(resp))
            if self._get_events:
                await self.event_que.put(resp)
        except Exception:
            lg.exception(f'handling {resp}')
            raise

    async def send_command(self, command: typing.Union[NooliteCommand, bytearray]):
        """
        Отправляет команды, асинхронно, ждет подтверждения уже отправленной команды
        :param command:
        :return:
        """
        # отправляем только одну команду до получения подтверждения
        async with self.send_lck:
            if isinstance(command, NooliteCommand):
                cmd = command.as_tuple()
            else:
                cmd = command
            lg.debug(f'> {cmd}')
            self.tty.write(bytearray(cmd))
            # отправляем команду и ждем секунду, если придет ответ, то ожидание будет отменено с ошибкой CancelledError
            # - значит от модуля пришел ответ о подтверждении команды, в противном случае поднимаем ошибку о том что
            # команда не подтверждена

            if command.commit is None:
                return True
            self.wait_ftr = self.loop.create_future()
            self.wait_cmd = command
            try:
                await asyncio.wait_for(self.wait_ftr, command.commit)
                await asyncio.sleep(0.05)
            except asyncio.CancelledError:
                return True
            except asyncio.TimeoutError:
                raise NotApprovedError(command)
            finally:
                self.wait_ftr = None
                self.wait_cmd = None


def _get_tty(tty_name) -> serial.Serial:
    """
    Подключение к последовательному порту
    :param tty_name: имя порта
    :return:
    """
    serial_port = serial.Serial(tty_name, 9600, timeout=2)
    if not serial_port.is_open:
        serial_port.open()
    serial_port.flushInput()
    serial_port.flushOutput()
    return serial_port
