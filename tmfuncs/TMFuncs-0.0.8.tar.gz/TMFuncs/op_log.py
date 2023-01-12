# -*- coding:utf-8 -*-

import logging
import os
import sys
import traceback
import datetime
from logging.handlers import TimedRotatingFileHandler


def check_path(file_path):
    """检查输出目录是否存在，如果不存在则新建目录
    如果path_type=='file'或'dir'

    注意：使用os.path.isdir 或 os.path.isfile 时，如果路径不存在，则返回False
    所以：必须使用绝对路径
    """
    split_info = os.path.splitext(os.path.abspath(file_path))
    if split_info[1] == '':  # 如果是路径，没有文件扩展名
        path = file_path
    else:  # 先拆分出路径，再判断
        path, _ = os.path.split(os.path.abspath(file_path))
    if not os.path.exists(path):
        os.makedirs(path)  # 注意使用多级目录方法


class LOG:
    """
    输出log日志到指定目录

    参数
    ----
    log_path: log日志所在的完整路径，包含log文件

    示例
    ----

    >>> from utils.op_log import LOG
    >>> file_path = '../log/20190306164611.log'
    >>> log_ins = LOG(file_path)
    >>> log_ins.info('this is a info 1')
    >>> log_ins.error('this is a info 1')
    >>> log_ins.warning('this is a info 1')
    >>> log_ins.close()

    备注
    ---
    file_path必须是包含log文件名的路径，可以是绝对路径，也可以是相对路径。

    不同的信息，调用不同的方法，例如：一般常用的是info方法，在Exception是调用error，
    在警告时调用warning方法。

    实例化对象的最后，务必调用close方法关闭对象。否则会导致不同的信息，写入相同的log
    文件中。

    """

    def __init__(self, log_path, if_print_in_console=True):
        file_path, _ = os.path.split(log_path)
        check_path(file_path)  # 检查目录是否存在
        # 获取logger实例
        self.logger = logging.getLogger()
        # 设置日志级别
        self.logger.setLevel(logging.INFO)
        # 文件日志
        self.file_handler = logging.FileHandler(log_path)
        # 消息记录格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(formatter)
        # 控制台日志
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.formatter = formatter  # 也可以直接给formatter赋值
        # 为logger添加的日志处理器
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        # 控制是否在控制台打印输出
        self.if_print_in_console = if_print_in_console

    def info(self, info):
        self.logger.info(info)
        if not self.if_print_in_console:
            self.logger.removeHandler(self.console_handler)

    def error(self, info):
        self.logger.error(f'Error: {info}, here are details: {traceback.format_exc()} .\n')
        if not self.if_print_in_console:
            self.logger.removeHandler(self.console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)

    def remove(self):
        self.logger.removeHandler(self.file_handler)
        self.logger.removeHandler(self.console_handler)

    def close(self):
        self.file_handler.close()
        self.console_handler.close()


# 适用于API等长期在线的日志
def get_logger(log_path):
    check_path(log_path)  # 检查目录是否存在
    # 获取logger实例
    log = logging.getLogger()
    # 设置日志级别
    log.setLevel(logging.INFO)
    # 消息记录格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # 各种日志处理器
    file_handler = logging.FileHandler(log_path)  # 文件日志
    console_handler = logging.StreamHandler(sys.stdout)  # 控制台日志
    split_handler = TimedRotatingFileHandler(log_path, when='midnight', interval=1,
                                             backupCount=7, encoding='utf-8',
                                             atTime=datetime.time(0, 0, 0, 0))  # 日期分割
    # 添加格式
    handles = [file_handler, console_handler, split_handler]
    for i in handles:
        i.setFormatter(formatter)
        log.addHandler(i)
    return log
