# coding:utf-8
from tools_hjh.Tools import locattime, echo


class Log():
    """ 简单的日志类 """

    def __init__(self, filepath):
        self.filepath = filepath

    def info(self, *text):
        print(locattime(), 'info', str(text))
        echo((locattime(), 'info', str(text)), self.filepath)
        
    def warning(self, *text):
        print(locattime(), 'warning', str(text))
        echo((locattime(), 'warning', str(text)), self.filepath)
        
    def error(self, *text):
        print(locattime(), 'error', str(text))
        echo((locattime(), 'error', str(text)), self.filepath)
        
