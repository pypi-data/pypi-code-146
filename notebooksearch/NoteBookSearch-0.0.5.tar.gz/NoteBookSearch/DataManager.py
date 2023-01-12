# -*- coding: utf-8 -*-
# @Time    : 28/09/2022 6:40 PM
# @Author  : William
# @FileName: DataManager.py
# @Software: PyCharm
import pandas as pd
from uuid import uuid4
import json
import os
# 此库需要用到static variable
TEMPLATE_CONTENT = "FingerPrint={uuid};line:{index}>>>{content}"
TEMPLATE_CONTENT_WITH_PATH = "FilePath:{path}\n{content}"
DATA_FILE_PATH_DICT = {"DictPath": []} #Thsi is for the jason later
SEARCH_DATA_FILENAME = "SEARCH_DATA_NAME.txt"
PATH_JASON_FILENAME = "PATH_JSON.json"
class DataManager(object):
    def __init__(self, path):
        '''
        This path will be used to determine where (which folder)
        to search for notes
        :param path:
        '''
        self.path = path

    # ----------------------------------搜索器----------------------------------
    def postfix(self, path: str):  # 服务于搜索器
        '''
        判断文件后缀
        '''
        suffix = path.split(".")[-1]
        sum_suffix = ['py', 'xlsx', 'xls', 'html',
                      'md','css', 'js', 'txt', 'csv', 'json']
        if suffix in sum_suffix:
            return suffix.lower()
        else:
            return "There might be an error."

    def general_read(self, path):  # 服务于搜索器
        '''
        Read each line of the file and put it into a list as an individual element.
        :param path:
        :return:
        '''
        with open(path, 'r', encoding='utf-8') as f:
            return f.readlines()  # This allows us to read spacelines.

    def decide_suffix(self, path, suffix):  # 服务于搜索器
        '''
        判断文件后缀，使用对应函数打开文件
        :return:
        '''
        if suffix == 'py':
            return self.general_read(path)
        elif suffix == "txt":
            return self.general_read(path)
        elif suffix == "md":
            return self.general_read(path)

    # ----------------------------------搜索器----------------------------------

    # ----------------------------------检索器----------------------------------
    def parse(self, content, path):  # 服务于检索器
        """
        This part creates a form of data in order for us to search easier. The form is now
        a string.  This makes it easier for us to use the regx（正则表达式）.

        The path here is from the path list that we have generated from
        :param content:
        :return:
        """
        global DATA_FILE_PATH_DICT #全局字典，便于后期存储成jason文件
        uuid = str(uuid4())
        detail_dict_to_json_value = {uuid: path}#为所有的路径赋予一个uuid
        # print(detial_dict_to_json_value)
        DATA_FILE_PATH_DICT['DictPath'].append(detail_dict_to_json_value)#把每一个detail_dict_to_json_value丢进之前设计好的DATA_FILE_PATH_DICT
        line_content_str = ''
        for line_number, content in enumerate(content):
            if content != '\n':
                content = TEMPLATE_CONTENT.format(uuid = uuid, index=line_number + 1, content=content)
                line_content_str = line_content_str + content #上面的空字符

            else:
                pass

        return TEMPLATE_CONTENT_WITH_PATH.format(path = path, content = line_content_str)

    # ----------------------------------检索器----------------------------------
    def path_generator(self):
        '''
        Generate all the path that we want to search content for.
        下面就是在一个文件夹之下，把每一个文件的具体路径生成出来。
        :param path:
        :return:
        '''
        path_lst = []
        for dirpath,  dirname, filename in os.walk(self.path): #this takes out element from the tuples
            # print(dirpath,  dirname, filename)
            for element in filename:
                file_path = os.path.join(dirpath, element)
                path_lst.append(file_path)
        return path_lst




    # ----------------------------------总体调动----------------------------------
    def data_manager_engine(self, path):
        """
        1. 先是判断文件后缀
        2. 选用一种方式打开
        3. 以某种格式返还每文件里面的内容
        :param path:
        :return:
        """
        suffix = self.postfix(path=path)
        content = self.decide_suffix(path, suffix)  # 判断文件后缀，使用对应函数打开文件
        #print(content)
        if content: #如果有有内容我们就parse一下他
            return self.parse(content, path)
        else: #要是没有内容我们就说下面那句话
            return "这里有一个不支持的文件类型"

    def run(self): #This is the main function.
        path_lst = self.path_generator() # generate a list that contains all path.
        #print(path_lst)
        if os.path.exists(SEARCH_DATA_FILENAME):
            os.remove(SEARCH_DATA_FILENAME)
        if os.path.exists(PATH_JASON_FILENAME):
            os.remove(PATH_JASON_FILENAME)
        for path in path_lst:
            content = self.data_manager_engine(path)
            # print(content)
            # print("-"*100)
            self.save(SEARCH_DATA_FILENAME, content)
        self.save_jason(PATH_JASON_FILENAME, DATA_FILE_PATH_DICT)

    def save(self, filename, content):
        """
        每次都是换行再追加进文件里面
        :param filename:
        :param content:
        :return:
        """

        with open(filename, "a+", encoding="utf-8") as f:
            f.write(content + "\n")

    def save_jason(self, filename, content):
        with open(filename, "a+", encoding="utf-8") as f:
            json.dump(content, f)
    # ----------------------------------总体调动----------------------------------

