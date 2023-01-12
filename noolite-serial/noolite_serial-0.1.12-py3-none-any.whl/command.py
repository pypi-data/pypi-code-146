import logging
from collections import defaultdict
from dataclasses import dataclass, astuple, field, asdict


APPROVAL_TIMEOUT = 0.3
MODE_SEND = 1
MODE_RECIEVE = 2

_toggles = defaultdict(lambda: 0)

lg = logging.getLogger('noolite')


@dataclass()
class NooliteCommand:
    """
    Контейнер для команды от адаптера или к адаптеру
    """
    st: int = 171
    mode: int = 0
    ctr: int = 0
    togl: int = field(hash=False, compare=False, default=0)
    ch: int = 0
    cmd: int = 0
    fmt: int = 0
    d0: int = 0
    d1: int = 0
    d2: int = 0
    d3: int = 0
    id0: int = 0
    id1: int = 0
    id2: int = 0
    id3: int = 0
    crc: int = field(hash=False, default=0, compare=False)
    sp: int = 172
    commit: bool = APPROVAL_TIMEOUT

    def __post_init__(self):
        tup = list(astuple(self))
        self.crc = NooliteCommand._calc_crc(tup)

    @staticmethod
    def _calc_crc(tup):
        crc = sum(tup[0:15])
        return crc % 256

    def as_tuple(self):
        """
        Возвращает байты в нужной последовательности
        :return:
        """
        tup = list(astuple(self))[:17]
        return tup

    def make_send(self):
        ret = asdict(self)
        ret.update(st=171, sp=172, mode=0)
        ret = NooliteCommand(**ret)
        return ret

    @classmethod
    def make_command(
            cls,
            *args,
            nrep=0,
            br=None,
            duration=None,
            **kwargs
    ):
        """
        Создает команду, добавляет кол-во повторов если нужно

        :param ch: канал
        :param duration: длительность (для временного включения)
        :param br: яркость (для регулирования яркости)
        :param nrep: кол-во дополнительных повторов (макс 3)
        :param args:
        :param kwargs: остальные данные передаваемые в исходный конструктор
        :return:
        """
        lg.debug(f'build command: {args}, nrep={nrep}, duration={duration}, {kwargs}')
        assert nrep <= 3
        if duration:
            # kwargs['cmd'] = const.TEMPORARY_ON
            kwargs['fmt'] = 2
            kwargs['d0'] = (duration // 5) & 0x00FF
            kwargs['d1'] = ((duration // 5) & 0xFF00) >> 8
        if br:
            kwargs['fmt'] = 1

            if br >= 100:
                kwargs['d0'] = 155
            elif br <= 0:
                kwargs['d0'] = 0
            else:
                kwargs['d0'] = 35 + int((120 * (br/100)) + 0.5)
        ret = cls(*args, **kwargs)
        if nrep == 0:
            return ret
        lg.debug(f'{ret}')
        ret = list(astuple(ret))
        ret[14] = NooliteCommand._calc_crc(ret)
        ctr = ret[2]
        ctr = int(f'{nrep:02b}' + f'{ctr:05b}', 2)
        ret[2] = ctr
        return cls(*ret)

    @property
    def battery_status(self):
        return int('{:08b}'.format(self.d1)[0])

    @property
    def sensor_type(self):
        """
        тип датчика
        :return:
        """
        # Тип датчика:
        #   000-зарезервировано
        #   001-датчик температуры (PT112)
        #   010-датчик температуры/влажности (PT111)
        return '{:08b}'.format(self.d1)[1:4]

    @property
    def temp(self):
        """
        температура
        :return:
        """
        temp_bits = '{:08b}'.format(self.command.d1)[4:] + '{:08b}'.format(self.command.d0)
        # Если первый бит 0 - температура считается выше нуля
        if temp_bits[0] == '0':
            return int(temp_bits, 2) / 10.
        # Если 1 - ниже нуля. В этом случае необходимо от 4096 отнять полученное значение
        elif temp_bits[0] == '1':
            return -((4096 - int(temp_bits, 2)) / 10.)

    @property
    def hum(self):
        """
        влажность
        :return:
        """
        # Если датчик PT111 (с влажностью), то получаем влажность из 3 байта данных
        if self.sensor_type == '010':
            return self.d2

    @property
    def analog_sens(self):
        # Значение, считываемое с аналогового входа датчика; 8 бит; (по умолчанию = 255)
        return self.d3

    @property
    def active_time(self):
        """
        Время на которое включается устройство
        :return:
        """
        return self.d0 * 5
