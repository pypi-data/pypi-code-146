import struct
from io import BufferedReader, BufferedWriter, BytesIO
from typing import Type, Union
from functools import reduce
from os import path


def get_tag(value: Union[dict, int, float, bytes, list]) -> int:
    """Return the tag value for a given type"""
    if isinstance(value, dict):
        return b"\x00"

    elif isinstance(value, int):
        return b"\x01"

    elif isinstance(value, float):
        return b"\x02"

    elif isinstance(value, bytes):
        return b"\x03"

    elif isinstance(value, list):
        return b"\x05"

    return None


def read_msg(
    file: Type[BufferedReader], tagged: bool = True, given_tag: int = 0x1
) -> Union[dict, int, float, bytes, list]:
    """Given a file, read the mesage from the hexxy data"""
    tag = 0x0

    if tagged:
        tag = struct.unpack("B", file.read(1))[0]
    else:
        tag = given_tag

    match tag:
        case 0x0:
            # object
            obj = {}
            obj_size = struct.unpack("Q", file.read(8))[0]
            while obj_size > 0:
                fieldnum = struct.unpack("Q", file.read(8))[0]
                msg = read_msg(file)
                obj[fieldnum] = msg

                obj_size -= 1

            return obj

        case 0x1:
            return struct.unpack("q", file.read(8))[0]

        case 0x2:
            return struct.unpack("d", file.read(8))[0]

        case 0x3:
            size = struct.unpack("Q", file.read(8))[0]
            return file.read(size)

        case 0x4:
            return struct.unpack("Q", file.read(8))[0]

        case 0x5:
            value = []
            size = struct.unpack("Q", file.read(8))[0]
            tag = struct.unpack("B", file.read(1))[0]
            while size > 0:
                value.append(read_msg(file, tagged=False, given_tag=tag))
                size -= 1

            return value


def safe_read_msg(filename: str) -> Union[dict, int, float, bytes, list, None]:
    """Return None if a file does not exist, failing quietly instead of throwing an exception"""
    if path.exists(filename):
        return read_msg(open(filename, "rb"))
    else:
        return None


def write_msg(
    file: Type[BufferedWriter],
    obj: Union[dict, int, float, bytes, list],
    tagged: bool = True,
):
    """given a BufferedWriter, will write an object to it. If tagged is set to false, then it won't add the tag to the type. This is so far only used for arrays"""
    buffer = BytesIO()

    if tagged:
        buffer.write(struct.pack("c", get_tag(obj)))
    if isinstance(obj, int):
        buffer.write(struct.pack("q", obj))

    elif isinstance(obj, float):
        buffer.write(struct.pack("d", obj))

    elif isinstance(obj, bytes):
        buffer.write(struct.pack("Q", len(obj)))
        buffer.write(obj)

    elif isinstance(obj, list):
        buffer.write(struct.pack("Qc", len(obj), get_tag(obj[0])))

        tag = get_tag(obj[0])
        for item in obj:
            if get_tag(item) != tag:
                return "All items in array must be the same, and a type representable by binformat"
            write_msg(buffer, item, tagged=False)

    elif isinstance(obj, dict):
        if not reduce(
            lambda x, y: x and y, map(lambda x: isinstance(x, int), list(obj.keys()))
        ):
            return "Fieldnumbers must be ints"

        buffer.write(struct.pack("Q", len(obj.keys())))

        for key, value in obj.items():
            buffer.write(struct.pack("Q", key))
            write_msg(buffer, value)

    file.write(buffer.getvalue())
    return None


def safe_write_msg(
    filename: str, obj: Union[dict, int, float, bytes, list]
) -> Union[None, str]:
    """Write a message to a file, only if it reads without error.
    Probably not the fastest, or best way to do this, but the only I can do without a major refactor. (which is due at some point)"""
    buffer = BytesIO()
    ret = write_msg(buffer, obj)

    if len(buffer.getvalue()) == 0:
        return "Error: " + str(ret)

    return None
