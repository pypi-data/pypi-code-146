# -*- coding: utf-8 -*-
# @Time    : 2022/12/14 18:51
# @Author  : William
# @FileName: testing_os_walk.py
# @Software: PyCharm
import os
import uuid
from pprint import pprint #这个就是格式化输出， 就是让我们看得更舒服
path = "C:\\Users\\Willi\\Documents\\Note_Seach\\NoteBookSearch" #必须\\, 因为\U代表了Unicode，双斜杠就避免了电脑读成\u
n = list(os.walk(path))
#pprint(n)

"""
[('C:\\Users\\Willi\\Documents\\Note_Seach\\NoteBookSearch',['testing_folding', '__pycache__'], ['DataManager.py', 'NoteBookSearch.py', '__init__.py', '__version__.py']),
 ('C:\\Users\\Willi\\Documents\\Note_Seach\\NoteBookSearch\\testing_folding',[],['testing_file.py']),
 ('C:\\Users\\Willi\\Documents\\Note_Seach\\NoteBookSearch\\__pycache__',[],['DataManager.cpython-310.pyc','NoteBookSearch.cpython-310.pyc','__init__.cpython-310.pyc'])]
"""

for tuples in n:
    for files in tuples[2]:
        print(tuples[0] + "\\" +str(files))

#代替方案
path_list = []
for dirpath, dirnames, filenames in n:
    for filename in filenames:
        filepath = os.path.join(dirpath,filename)
        path_list.append(filepath)

#总结: 上面就是在一个文件夹之下，把每一个文件的具体路径生成出来。

from uuid import uuid4
uuid1 = uuid.uuid4()
uuid2 = uuid.uuid4()
uuid3 = uuid.uuid4()
uuid4 = uuid4()
print(uuid1, uuid2, uuid3)
print(uuid4)