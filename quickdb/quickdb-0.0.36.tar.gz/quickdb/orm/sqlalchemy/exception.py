"""
    错误定义
"""


# 后缀错误
class SuffixError(Exception):
    def __init__(self, msg: str):
        super(SuffixError, self).__init__(msg)
