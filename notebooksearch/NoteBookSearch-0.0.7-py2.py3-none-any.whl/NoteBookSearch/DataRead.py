# -*- coding: utf-8 -*-
# @Time    : 28/09/2022 6:40 PM
# @Author  : William
# @FileName: DataManager.py
# @Software: PyCharm

class DataRead(object):
    def __init__(self, path):
        self.path = path

    def postfix(self, path: str):
        '''
        判断文件后缀
        '''
        suffix = path.split(".")[-1]
        return suffix

    def decide_suffix(self):
        '''
        判断文件后缀，使用对应函数打开文件
        :return:
        '''
        pass

    # def main(self):
    #     # abs_path = r"C:\Users\Willi\Documents\Note_Seach\README.md"
    #     d = DataRead(abs_path)
