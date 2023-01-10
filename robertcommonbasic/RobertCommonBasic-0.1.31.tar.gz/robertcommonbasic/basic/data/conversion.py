import pandas as pd

from struct import pack, unpack
from typing import Optional, Union, Any
from enum import Enum
from datetime import datetime, timedelta


class DataFormat(Enum):
    """应用于多字节数据的解析或是生成格式"""
    ABCD = 0
    BADC = 1
    CDAB = 2
    DCBA = 3


class TypeFormat(Enum):
    BOOL = 0
    BOOL_ARRAY = 1
    INT8 = 2
    INT8_ARRAY = 3
    UINT8 = 4
    UINT8_ARRAY = 5
    INT16 = 6
    INT16_ARRAY = 7
    UINT16 = 8
    UINT16_ARRAY = 9
    INT32 = 10
    INT32_ARRAY = 11
    UINT32 = 12
    UINT32_ARRAY = 13
    INT64 = 14
    INT64_ARRAY = 15
    UINT64 = 16
    UINT64_ARRAY = 17
    FLOAT = 18
    FLOAT_ARRAY = 19
    DOUBLE = 20
    DOUBLE_ARRAY = 21
    STRING = 22
    HEX_STRING = 23


def int_or_none(i: Union[None, int, str, float]) -> Optional[int]:
    return None if pd.isnull(i) else int(float(i))


def float_or_none(f: Union[None, int, str, float]) -> Optional[float]:
    return None if pd.isnull(f) else float(f)


def get_type_word_size(type: int, length: int = 0):
    if type in [TypeFormat.BOOL, TypeFormat.BOOL_ARRAY, TypeFormat.INT8, TypeFormat.UINT8, TypeFormat.INT16, TypeFormat.UINT16]:
        return 1
    elif type in [TypeFormat.INT32, TypeFormat.UINT32, TypeFormat.FLOAT]:
        return 2
    elif type in [TypeFormat.INT64, TypeFormat.UINT64, TypeFormat.DOUBLE]:
        return 4
    return length


# 将字节数组转换成十六进制的表示形式
def bytes_to_hex_string(datas: bytearray, segment: str = ' '):
    return segment.join(['{:02X}'.format(byte) for byte in datas])


# 从字节数组中提取bool数组变量信息
def bytes_to_bool_array(datas: bytearray, length: int = None):
    if datas is None:
        return None
    if length is None or length > len(datas) * 8:
        length = len(datas) * 8

    buffer = []
    for i in range(length):
        index = i // 8
        offect = i % 8
        temp_array = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
        temp = temp_array[offect]
        if (datas[index] & temp) == temp:
            buffer.append(True)
        else:
            buffer.append(False)
    return buffer


# 将buffer中的字节转化成byte数组对象
def trans_byte_array(datas: bytearray, index: int, length: int):
    data = bytearray(length)
    for i in range(length):
        data[i] = datas[i + index]
    return data


# 将buffer数组转化成bool数组对象，需要转入索引，长度
def trans_byte_bool_array(datas: bytearray, index: int, length: int):
    data = bytearray(length)
    for i in range(length):
        data[i] = datas[i + index]
    return bytes_to_bool_array(data)


# 将buffer中的字节转化成byte对象
def trans_byte(datas: bytearray, index: int):
    return datas[index]


# 反转多字节
def reverse_bytes(datas: bytearray, length: int, index: int = 0, format: DataFormat = DataFormat.ABCD):
    buffer = bytearray(length)
    if format == DataFormat.ABCD:
        for i in range(length):
            buffer[i] = datas[index + i]
    elif format == DataFormat.BADC:
        for i in range(int(length / 2)):
            buffer[2 * i] = datas[index + 2 * i + 1]
            buffer[2 * i + 1] = datas[index + 2 * i]
    elif format == DataFormat.CDAB:
        for i in range(int(length / 2)):
            buffer[2 * i] = datas[index + length - 2 * (i + 1)]
            buffer[2 * i + 1] = datas[index + length - 2 * (i + 1) + 1]
    elif format == DataFormat.DCBA:
        for i in range(length):
            buffer[i] = datas[index + length - i - 1]
    return buffer


def get_type_size_fmt(type: TypeFormat):
    type_size = 1
    type_fmt = '<h'
    if type in [TypeFormat.INT8, TypeFormat.INT8_ARRAY]:
        type_size = 1
        type_fmt = '<b'
    elif type in [TypeFormat.UINT8, TypeFormat.UINT8_ARRAY]:
        type_size = 1
        type_fmt = '<B'
    elif type in [TypeFormat.INT16, TypeFormat.INT16_ARRAY]:
        type_size = 2
        type_fmt = '<h'
    elif type in [TypeFormat.UINT16, TypeFormat.UINT16_ARRAY]:
        type_size = 2
        type_fmt = '<H'
    elif type in [TypeFormat.INT32, TypeFormat.INT32_ARRAY]:
        type_size = 4
        type_fmt = '<i'
    elif type in [TypeFormat.UINT32, TypeFormat.UINT32_ARRAY]:
        type_size = 4
        type_fmt = '<I'
    elif type in [TypeFormat.INT64, TypeFormat.INT64_ARRAY]:
        type_size = 8
        type_fmt = '<q'
    elif type in [TypeFormat.UINT64, TypeFormat.UINT64_ARRAY]:
        type_size = 8
        type_fmt = '<Q'
    elif type in [TypeFormat.FLOAT, TypeFormat.FLOAT_ARRAY]:
        type_size = 4
        type_fmt = '<f'
    elif type in [TypeFormat.DOUBLE, TypeFormat.DOUBLE_ARRAY]:
        type_size = 8
        type_fmt = '<d'
    return type_size, type_fmt


# 将bytes转换成各种值
def convert_bytes_to_values(datas: bytearray, type: TypeFormat, index: int, length: int = 1, encoding: str = '') -> list:
    if type == TypeFormat.STRING:
        return [trans_byte_array(datas, index, length).decode(encoding)]
    elif type == TypeFormat.HEX_STRING:
        return [bytes_to_hex_string(datas)]
    elif type in [TypeFormat.BOOL, TypeFormat.BOOL_ARRAY]:
        return trans_byte_bool_array(datas, index, len(datas))

    type_size, type_fmt = get_type_size_fmt(type)
    return [unpack(type_fmt, trans_byte_array(datas, index + type_size * i, type_size))[0] for i in range(length)]


# 从bool数组变量变成byte数组
def convert_bool_array_to_byte(values: list):
    if values is None:
        return None

    if len(values) % 8 == 0:
        length = int(len(values) / 8)
    else:
        length = int(len(values) / 8) + 1
    buffer = bytearray(length)
    for i in range(len(values)):
        index = i // 8
        offect = i % 8

        temp_array = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
        temp = temp_array[offect]

        if values[i]:
            buffer[index] += temp
    return buffer


# 将各种类型值转换为bytes
def convert_values_to_bytes(values: Any, type: TypeFormat, encoding: str = ''):
    if values is None:
        return None

    if type == TypeFormat.STRING:
        buffer = values.encode(encoding)
    elif type == TypeFormat.HEX_STRING:
        buffer = bytes.fromhex(values)
    else:
        if not isinstance(values, list):
            values = [values]
        if type in [TypeFormat.BOOL, TypeFormat.BOOL_ARRAY]:
            buffer = convert_bool_array_to_byte(values)
        else:
            type_size, type_fmt = get_type_size_fmt(type)
            buffer = bytearray(len(values) * type_size)
            for i in range(len(values)):
                buffer[(i * type_size): (i + 1) * type_size] = pack(type_fmt, values[i])
    return buffer


def format_bytes(data: bytes) -> str:
    return ''.join(["%02X" % x for x in data]).strip()


def convert_value(values: Any, src_type: TypeFormat, dst_type: TypeFormat, format: Optional[DataFormat] = DataFormat.ABCD, pos: int = -1):
    datas = convert_values_to_bytes(values, src_type)  # CDAB
    datas = reverse_bytes(datas, len(datas), 0, format)  # 转换为指定顺序
    type_size, type_fmt = get_type_size_fmt(dst_type)
    results = convert_bytes_to_values(datas, dst_type, 0, int(len(datas) / type_size))
    if 0 <= pos < len(results):
        return results[pos]
    return results


# 比较两个数组
def compare_bytes(bytes1: bytearray, bytes2: bytearray, length: int, start1: int = 0, start2: int = 0):
    if bytes1 is None or bytes2 is None:
        return False
    for i in range(length):
        if bytes1[i + start1] != bytes2[i + start2]:
            return False
    return True


# 补数
def fill_specified_time_data(time_datas: dict, freq: str = 'min', method: str = 'ffill') -> dict:
    """
     补数
    :param time_datas: {"2021-08-04 00:00:00": data_sturct}
    :param freq: ["min", "5min"]
    :param method: ["", ""]补齐方式
    :return:
    """

    times = sorted(list(time_datas.keys()))
    time_start = datetime.strptime(times[0], '%Y-%m-%d %H:%M:%S')
    time_end = datetime.strptime(times[-1], '%Y-%m-%d %H:%M:%S')

    # 获取指定格式时间段
    times_index_specified = []
    for date in pd.date_range(start=time_start, end=time_end + timedelta(days=1), freq=freq, normalize=True):  # 按分钟补齐
        time = date.to_pydatetime()
        if time_start <= date <= time_end:
            times_index_specified.append(time.strftime('%Y-%m-%d %H:%M:%S'))

    times_index_extra = []
    for time in times:
        if time not in times_index_specified:
            times_index_extra.append(time)

    times_index_specified.extend(times_index_extra)

    dict_value = pd.DataFrame(pd.DataFrame.from_dict(time_datas).T, index=sorted(times_index_specified)).fillna(method=method).drop(times_index_extra).T.to_dict()

    # 去除空值
    for time in dict_value.keys():
        for name in list(dict_value[time].keys()):
            if name in dict_value[time].keys():
                if pd.isnull(dict_value[time][name]):
                    del dict_value[time][name]

    return dict_value


def int_from_bytes(data: bytes, byteorder: str = 'little', signed: bool = False, mode: str = 'short', is_binary: bool = True):
    if is_binary is True:
        return int.from_bytes(data, byteorder, signed=signed)
    else:
        value = int(data.decode(), 16)
        if signed:
            if mode == "byte":
                bit = 8
            elif mode == "short":
                bit = 16
            elif mode == "long":
                bit = 32
            else:
                raise ValueError("cannnot calculate 2's complement")
            if (value & (1 << (bit - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
                value = value - (1 << bit)  # compute negative value
        return value


def int_to_bytes(data: int, byteorder: str = 'little', signed: bool = False, mode: str = 'short', is_binary: bool = True):
    if is_binary is True:
        if mode == "byte":
            return data.to_bytes(1, byteorder, signed=signed)
        elif mode == "short":
            return data.to_bytes(2, byteorder, signed=signed)
        elif mode == "long":
            return data.to_bytes(4, byteorder, signed=signed)
        else:
            raise ValueError(f"invalid mode({mode})")
    else:
        if mode == "byte":
            data.to_bytes(1, byteorder, signed=signed)
            data = data & 0xff
            return format(data, "x").rjust(2, "0").upper().encode()
        elif mode == "short":
            data.to_bytes(2, byteorder, signed=signed)
            data = data & 0xffff
            return format(data, "x").rjust(4, "0").upper().encode()
        elif mode == "long":
            data.to_bytes(4, byteorder, signed=signed)
            data = data & 0xffffffff
            return format(data, "x").rjust(8, "0").upper().encode()
        else:
            raise ValueError(f"invalid mode({mode})")


#
def get_bool(value: int, pos: int):
    if (1 << pos) & value == 0:
        return 0
    else:
        return 1


def set_bool(old_value: int, pos: int, bit_value: int):
    current_bit = get_bool(old_value, pos)
    if current_bit != bit_value:
        if bit_value == 1:
            old_value = old_value + (1 << pos)
        else:
            old_value = old_value - (1 << pos)
    return old_value


def unpack_bytes(value: bytes, type_fmt: str):
    return unpack(type_fmt, value)[0]


def pack_value(value, type_fmt: str):
    return pack(type_fmt, value)


# BCD
def bcd_to_float(value: bytes, precision: int = 0):
    v = ''
    for i in range(len(value)):
        v = f"{v}{(value[len(value) - i - 1]) >> 4 & 0xF}{(value[len(value) - i - 1]) & 0xF}"
        if len(value) - i - 1 == precision and precision > 0:
            v = f"{v}."
    return str(float(v))


def accumulate_sum(value: bytes):
    return sum(value) & 0xFF


# Align
def algin_content(content: str, algin: str, size: int, fill_char: Optional[str] = None) -> str:
    algins = {'left': '<', 'right': '>', 'center': '^'}
    _format = f"{{:{'' if fill_char is None else fill_char}{algins.get(algin, '<')}{size}}}"
    return _format.format(content)


# Decimal conversion
def value_to_decimal(value: Any, type: Optional[str] = None):
    if type is None:
        if isinstance(value, bytes):
            value = value.decode()
        type = str(value)[0:2]

    type = type.lower()
    if type == '0b':    # 2进制数（字符串）转10进制数
        return int(value, 2)
    elif type == '0o':  # 8进制数
        return int(value, 8)
    elif type == '0x':  # 16进制数
        return int(value, 16)
    else:
        return int(value)


def value_to_bin(value: Any, type: Optional[str] = None):
    return bin(value_to_decimal(value, type))   # 转2进制


def value_to_oct(value: Any, type: Optional[str] = None):
    return oct(value_to_decimal(value, type))   # 转8进制


def value_to_hex(value: Any, type: Optional[str] = None):
    return hex(value_to_decimal(value, type))   # 转16进制


def try_convert_value(value: Union[str, float, None]) -> Union[str, float, None]:
    try:
        return float(value)
    except (ValueError, TypeError):
        return value
