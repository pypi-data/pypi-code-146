def calculate_crc(data):
    """
    计算数据校验码
    :param data: 2进制数据
    :return: 16位数据校验码
    """
    crc = 0xFFFF
    for i in data:
        crc ^= i
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 0x01 else crc >> 1
    return crc.to_bytes(2, 'big')


class UartProtocol1:
    """
    串口协议1
    2字节帧头 1字节数据长度 1~250字节数据 2字节校验码
    """

    def __init__(self, uart):
        """
        初始化
        :param uart: 串口对象
        """
        self.uart = uart

    def any(self):
        """
        判断是否有数据
        :return: True/False
        """
        return self.uart.any()

    def send(self, data):
        """
        发送数据
        :param data: 数据
        :return: None
        """
        header = b'\x55\xAA'
        data = data.encode('utf-8')
        length = len(data).to_bytes(1, 'big')
        crc = sum(data).to_bytes(2, 'big')
        self.uart.write(header + length + data + crc)

    def receive(self, block=True):
        """
        接收数据
        :return: 数据
        """
        header = self.uart.read(1)
        if block:
            while header not in [b'\x55', b'\xAA']:
                header = self.uart.read(1)
        elif header not in [b'\x55', b'\xAA']:
            return
        if header == b'\x55' and self.uart.read(1) != b'\xAA':
            return
        length = self.uart.read(1)
        if length is None:
            return None
        length = int.from_bytes(length, 'big')
        data = self.uart.read(length)
        if data is None:
            return None
        crc = self.uart.read(2)
        if crc is None:
            return None
        return None if crc != sum(data).to_bytes(2, 'big') else data.decode('utf-8')


class UartProtocolForSmallData:

    def __init__(self, uart, number_of_bytes=1):
        """
        初始化
        :param uart: 串口对象
        """
        self.uart = uart
        self.number_of_bytes = number_of_bytes
        self.length = number_of_bytes // 8 + bool(number_of_bytes % 8)
        self.byte_length = 8 * self.length

    def any(self):
        """
        判断是否有数据
        :return: True/False
        """
        return self.uart.any()

    def send(self, list_of_data):
        """
        发送数据
        :param list_of_data: 数据
        :return: None
        """
        data = 0x0
        for dat in list_of_data:
            data <<= 1
            data |= dat
        self.uart.write(b'\x55\xAA' + data.to_bytes(self.length, 'big'))

    def receive(self, block=True):
        """
        接收数据
        :return: 数据
        """
        header = self.uart.read(1)
        if block:
            while header not in [b'\x55', b'\xAA']:
                header = self.uart.read(1)
        elif header not in [b'\x55', b'\xAA']:
            return
        if header == b'\x55' and self.uart.read(1) != b'\xAA':
            return
        data = self.uart.read(self.length)
        if data is None:
            return None
        data = int.from_bytes(data, 'big')
        return [data >> (self.number_of_bytes - 1 - i) & 0x01 for i in range(self.number_of_bytes)]
