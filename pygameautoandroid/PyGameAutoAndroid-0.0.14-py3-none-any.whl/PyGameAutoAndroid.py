# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : PyGameAutoAndroid.py
# Time       ：2022.8.30 23:53
# Author     ：小派精灵
# HomePage   : xiaopy.cn
# Email      : 3383716176@qq.com
# Description：
"""

import time


class Point:
    x = None
    y = None


class Rect:
    x = None
    y = None
    width = None
    height = None


class Text:
    text = None
    confidence = None


class Node:
    index = None
    id = None
    cls = None
    pkg = None
    text = None
    desc = None
    checkable = None
    checked = None
    clickable = None
    longClickable = None
    enabled = None
    focusable = None
    focused = None
    scrollable = None
    selected = None
    rect = Rect


class Path:
    def __init__(self, x: int, y: int):
        return self

    def moveTo(self, x: int, y: int, duration: float):
        return self


class Size:
    width = None
    height = None


def IdSelector(id: str):
    pass


def TextSelector(text: str):
    pass


def DescSelector(desc: str):
    pass


class xp:
    @classmethod
    def tap(cls, x1: float, y1: float, duration: float = 0.05):
        """
        点击
        :param x1: x坐标
        :param y1: y坐标
        :param duration: 持续时间
        :return:
        """
        pass

    @classmethod
    def swipe(cls, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, duration: float = 0.3):
        """
        滑动
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :param duration: 滑动时间
        :return:
        """
        pass

    @classmethod
    def gesture(cls, path: Path):
        pass

    @classmethod
    def matchColor(cls, colorDesc: str, x: int = 0, y: int = 0):
        """
        匹配颜色
        :param colorDesc: 颜色描述
        :param x: x 坐标
        :param y: y 坐标
        :return:
        """
        return

    @classmethod
    def findColor(cls, mainColorDesc: str, multiColorDesc: str, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        """
        多点找色
        :param mainColorDesc: 主点颜色描述
        :param multiColorDesc: 多点颜色描述
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :return:
        """
        return Point

    @classmethod
    def findImage(cls, imgName: str, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, sim: float = 0.9):
        """
        找图
        :param imgName: 图片名称, 包含后缀
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :param sim: 相似度
        :return:
        """
        return Rect

    @classmethod
    def findImageAll(cls, imgName: str, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, sim: float = 0.9):
        """
        找图
        :param imgName: 图片名称, 包含后缀
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :param sim: 相似度
        :return:
        """
        return [Rect]

    @classmethod
    def findText(cls, text: str, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, sim: float = 0.9):
        """
        文字查找
        :param text: 文本内容
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :param sim: 相似度
        :return:
        """
        return Rect

    @classmethod
    def findTextAll(cls, text: str, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, sim: float = 0.9):
        """
        查找范围内所有文字
        :param text:
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :param sim:
        :return:
        """
        return [Rect]

    @classmethod
    def getText(cls, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        """
        文字判断
        :param x1: 起点 x 坐标
        :param y1: 起点 y 坐标
        :param x2: 终点 x 坐标
        :param y2: 终点 y 坐标
        :return:
        """
        return Text

    @classmethod
    def getTextAll(cls, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0):
        """
        识别获取范围内所有文字
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        return [Text]

    @classmethod
    def findNode(cls, selector):
        """
        查找节点
        :param selector:
        :return:
        """
        return Node

    @classmethod
    def findNodeAll(cls, selector):
        """
        查找所有节点
        :param selector:
        :return:
        """
        return [Node]

    @classmethod
    def click(cls, node: Node) -> bool:
        """
        点击节点
        :param node:
        :return:
        """
        pass

    @classmethod
    def longClick(cls, node: Node) -> bool:
        """
        长点击节点
        :param node:
        :return:
        """
        pass

    @classmethod
    def log(cls, *msg: object):
        """
        日志框打印
        :param msg: 日志内容
        :return:
        """
        pass

    @classmethod
    def console(cls, *msg: object):
        """
        真机调试 开发日志打印
        :param msg: 日志内容
        :return:
        """
        pass

    @classmethod
    def toast(cls, *msg: object):
        """
        弹出 toast
        :param msg: 消息提示框内容
        :return:
        """
        pass

    @classmethod
    def home(cls):
        """
        手机Home键
        :return:
        """
        pass

    @classmethod
    def back(cls):
        """
        手机返回键
        :return:
        """
        pass

    @classmethod
    def launchApp(cls, packageName: str):
        """
        包名运行APP
        :param packageName:
        :return:
        """
        pass

    @classmethod
    def currentAppPackageName(cls):
        """
        获取当前APP包名
        :return:
        """
        pass

    @classmethod
    def screenSize(cls):
        """
        获取屏幕分辨率
        :return:
        """
        return Size

    @classmethod
    def inputText(cls, text: str):
        """
        输入文本
        :param text:
        :return:
        """
        pass

    @classmethod
    def clearText(cls):
        """
        清空文本
        :return:
        """
        pass
