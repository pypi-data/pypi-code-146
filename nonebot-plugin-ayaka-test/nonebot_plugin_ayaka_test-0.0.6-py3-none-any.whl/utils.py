import re
import os
import json
import shlex
import base64
from pathlib import Path
from nonebot import get_driver, init, logger

try:
    driver = get_driver()
except:
    init()
    driver = get_driver()

port = driver.config.port


def base64_to_pic(base64_str):
    base64_str = re.sub("^.*?base64://", "", base64_str)
    base64_bs = base64.b64decode(base64_str)

    # 固定名称
    path = ensure_dir_exists("data/ayaka_test/1.png")
    path.write_bytes(base64_bs)
    return str(path)


def safe_split(text: str,  n: int, sep: str = " "):
    '''安全分割字符串为n部分，不足部分使用空字符串补齐'''
    i = text.count(sep)
    if i < n - 1:
        text += sep * (n - i - 1)
    return text.split(sep, maxsplit=n-1)


def ensure_dir_exists(path: str | Path):
    '''确保目录存在

    参数：

        path：文件路径或目录路径

            若为文件路径，该函数将确保该文件父目录存在

            若为目录路径，该函数将确保该目录存在

    返回：

        Path对象
    '''
    if not isinstance(path, Path):
        path = Path(path)
    # 文件
    if path.suffix:
        ensure_dir_exists(path.parent)
    # 目录
    elif not path.exists():
        path.mkdir(parents=True)
    return path


def load_data_from_file(path: str | Path):
    '''从指定文件加载数据

    参数:

        path: 文件路径

        若文件类型为json，按照json格式读取

        若文件类型为其他，则按行读取，并排除空行

    返回:

        json反序列化后的结果(对应.json文件) 或 字符串数组(对应.txt文件)
    '''
    path = ensure_dir_exists(path)

    with path.open("r", encoding="utf8") as f:
        if path.suffix == ".json":
            return json.load(f)
        else:
            # 排除空行
            return [line[:-1] for line in f if line[:-1]]


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
