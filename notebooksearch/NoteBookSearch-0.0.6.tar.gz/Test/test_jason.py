# -*- coding: utf-8 -*-
# @Time    : 10/10/2022 6:33 pm
# @Author  : William
# @FileName: test_jason.py
# @Software: PyCharm
import json

f = open(r'C:\Users\Willi\Documents\Note_Seach\venv\Lib\site-packages\bleach\_vendor\html5lib\treewalkers\__pycache__etree.cpython-310.pyc', "r")
a = json.loads(f.read())
print(a)
# print(a['dict_path'][0]['uuid1'])
f.close()