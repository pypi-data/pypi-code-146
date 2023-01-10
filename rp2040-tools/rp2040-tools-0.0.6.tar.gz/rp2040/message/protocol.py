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

    def receive(self):
        """
        接收数据
        :return: 数据
        """
        header = self.uart.read(1)
        if header != b'\x55':
            return
        header = self.uart.read(1)
        if header != b'\xAA':
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
