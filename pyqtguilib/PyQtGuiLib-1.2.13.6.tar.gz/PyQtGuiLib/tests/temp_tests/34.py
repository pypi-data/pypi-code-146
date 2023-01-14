# -*- coding:utf-8 -*-
# @time:2023/1/1016:01
# @author:LX
# @file:34.py
# @software:PyCharm

import queue

def test(a,b,c):
    print(a,b,c)

def callback(fun,*args,**kwargs):
    fun(*args,**kwargs)

# 创建队列
que = queue.Queue()
# 进队列
que.put({
    "fun":test,
    "agrc":("aaa",'bbb','''555'''),
    "kwargs":dict()
})
# 出队列
out = que.get()

callback(out["fun"],*out["agrc"],**out["kwargs"])