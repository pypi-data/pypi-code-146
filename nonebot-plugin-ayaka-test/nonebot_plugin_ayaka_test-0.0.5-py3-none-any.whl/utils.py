import re
import os
import json
import shlex
import base64
from pathlib import Path
from nonebot import get_driver, init, logger

init()
driver = get_driver()
port = driver.config.port


def base64_to_pic(base64_str):
    base64_str = re.sub("^.*?base64://", "", base64_str)
    base64_bs = base64.b64decode(base64_str)

    # 固定名称
    path, f = safe_open_file("data/ayaka_test/1.png", "wb+")
    with f:
        f.write(base64_bs)
    return str(path)


def safe_split(text: str,  n: int, sep: str = " "):
    '''安全分割字符串为n部分，不足部分使用空字符串补齐'''
    i = text.count(sep)
    if i < n - 1:
        text += sep * (n - i - 1)
    return text.split(sep, maxsplit=n-1)


def safe_open_file(path: str | Path, mode: str = "a+"):
    '''安全打开文件，如果文件父目录不存在，则自动新建

    参数：

        path：文件地址，str或Path类型

        mode：文件打开模式

    返回：

        path: 文件地址，Path类型

        f：打开后的文件IO
    '''
    if isinstance(path, str):
        path = Path(path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    return path, path.open(mode, encoding="utf8")


def load_data_from_file(path: str | Path):
    '''从指定文件加载数据

    参数:

        path: 文件路径

        若文件类型为json，按照json格式读取

        若文件类型为其他，则按行读取，并排除空行

    返回:

        json反序列化后的结果(对应.json文件) 或 字符串数组(对应.txt文件)
    '''
    if isinstance(path, str):
        path = Path(path)

    with safe_open_file(path, "r")[1] as f:
        if path.suffix == ".json":
            return json.load(f)
        else:
            # 排除空行
            return [line[:-1] for line in f if line[:-1]]


def run_in_startup(func):
    '''等效于driver.on_startup(func)'''
    driver.on_startup(func)
    return func


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
