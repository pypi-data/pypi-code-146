# _*_coding:utf-8_*_

class JDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    # 是否允许点操作符
    def allow_dotting(self, state=True):
        if state:
            self.__dict__ = self
        else:
            self.__dict__ = dict()

    # 当值不存在时返回None
    def __getattr__(self, *args):
        pass
