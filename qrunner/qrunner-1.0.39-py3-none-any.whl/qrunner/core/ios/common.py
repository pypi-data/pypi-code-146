import os
import socket

from qrunner.utils.exceptions import DeviceNotFoundException


def get_device_list():
    """获取当前连接的设备列表"""
    cmd = 'tidevice list'
    output = os.popen(cmd).read()
    device_list = [item.split(' ')[0] for item in output.split('\n') if item]
    if len(device_list) > 0:
        return device_list
    else:
        raise DeviceNotFoundException(msg=f"无已连接设备")


def get_current_device():
    """连接一个手机时，返回设备id"""
    device_list = get_device_list()
    return device_list[0]


def get_tcp_port(udid: str):
    """获取可用端口号"""
    # tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcp.bind(("", 0))
    # _, port = tcp.getsockname()
    # tcp.close()
    port = int(udid.split('-')[0])
    return port


def check_device(device_id):
    """检查设备是否已连接"""
    if device_id is None:
        device_id = get_current_device()
        return device_id
    else:
        if device_id in get_device_list():
            return device_id
        else:
            raise DeviceNotFoundException(msg=f"设备 {device_id} 未连接")


if __name__ == '__main__':
    print(get_device_list())

