# -*- coding: utf-8 -*-
# @Time    : 2022/12/19 19:32
# @Author  : William
# @FileName: Question2.py
# @Software: PyCharm
# 请在超星学习平台“章节”的第 12 讲下找到两个文本文件："name_score.txt"这个文件包含了每个人的中文姓名和对应的成绩；"name_pinyin.txt"文件包含了每个人的中文姓名和对
# 应的拼音。请编写 Python 程序，读取这两个文件，然后生成一个名为 pinyin_score.txt 的文本文件，要求新的文本文件中第一列为每个人姓名所对应的拼音，第二列为这个人的成绩，
# 并且每个人的姓名和他对应的成绩是按照成绩从高到低排列的
# ------
# 著作权归黄家宝|AI悦创所有
# 原文链接：https://bornforthis.cn/1v1/15-Lantern_Fs/



with open("name_pinyin.txt", 'r', encoding = "gbk") as my_file_1:
    chinese_pinyin = my_file_1.readlines()
    index = 0
    name_pinyin_dict = {}
    a_tuple = ()
    a_list = []
    #print(chinese_pinyin)
    for pairs in chinese_pinyin:
        a_list.append(pairs.split(','))

    for lists in a_list:
        name_pinyin_dict[lists[0]] = lists[1]

    #print(name_pinyin_dict)

with open ("name_score.txt", 'r',  encoding="gbk") as my_file_2:
    name_scores_dict = {}
    chinese_score = my_file_2.readlines()
    b_list = []
    #print(chinese_score)
    for pairs in chinese_score:
        b_list.append(pairs.split(" "))
    #print(b_list)
    for lists in b_list:
        name_scores_dict[lists[0]] = lists[1]

print(name_pinyin_dict)
print(name_scores_dict)
pinyin_score_dict = {}
for key in name_pinyin_dict:
    if key in name_scores_dict:
        pinyin_score_dict[name_pinyin_dict[key]] = name_scores_dict[key]
print(pinyin_score_dict)






