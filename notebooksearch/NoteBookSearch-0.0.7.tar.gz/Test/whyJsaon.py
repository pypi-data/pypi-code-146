# -*- coding: utf-8 -*-
# @Time    : 2022/12/17 19:02
# @Author  : William
# @FileName: whyJsaon.py
# @Software: PyCharm
"""给予了一个uuid，  要求返data.txy对应的文件路径"""

# with open("data.txt", "r") as f:
#     # content = f.readlines()
#     content = f.read()
# # print(len(content))
#
# lst = []
# for i in content.split(","):
#     n1 = i.find("[")
#     n2 = i.find("]")
#     # print(i.find("["))
#     if (n1 == -1) and (n2 == -1):
#         # print(i)
#         lst.append(i)
#     else:
#         if not (n1 == -1):
#             new_i = i[i.find("[") + 1:]
#             # print(new_i)
#             lst.append(new_i)
#         else:
#             r = i[:n2]
#             # print(r)
#             lst.append(r)
# u = input(":>>>")
# for i in lst:
#     i = i.replace("{", "")
#     i = i.replace("}", "")
#     i = i.replace('"', "")
#     i = i.replace(' ', "")
#     # i = i.strip(" ")
#     if u in i:
#         print(i.split(":")[1])

'----------------------------------------------------------'
import json
with open("data.txt") as my_file:
    content = json.load(my_file) #读取的时候已经是dictionary了
    print(content)

