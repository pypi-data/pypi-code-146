'''清理可能已经卡死的上一次的端口 win10使用'''
import os
import shlex
from .utils import get_driver

driver = get_driver()
port = driver.config.port


def clean_port():
    '''清理可能已经卡死的上一次的端口 win10使用'''
    print(port)
    result = os.popen(f'netstat -aon|findstr "{port}"')
    info = result.read()
    if not info:
        print("端口畅通")
    else:
        print(info)
        lines = info.strip().split("\n")
        pids = set(shlex.split(line)[-1] for line in lines)
        input(f"{pids} kill?")

        for pid in pids:
            result = os.popen(f"taskkill -pid {pid} -f")
            print(result.read())
