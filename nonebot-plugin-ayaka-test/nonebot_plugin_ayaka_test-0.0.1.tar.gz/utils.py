import json
from pathlib import Path
from nonebot import get_driver, init, logger

init()
driver = get_driver()


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
