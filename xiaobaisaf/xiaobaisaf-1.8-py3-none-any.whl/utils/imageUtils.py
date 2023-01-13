#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/24 1:37
@File  : image_utils.py
'''
''' 将图片验证码转为字符串的样例 '''
from saf import WebDriver, By, DdddOcr
from saf.utils.elementUtils import find_element

def image2str(driver: WebDriver = None, by: str = By.XPATH,value: str = ''):
    '''
    验证码识别工具
    :param driver   : 浏览器驱动
    :param by       : 定位方法
    :param value    : 定位表达式
    :return         : 返回验证码图片中识别的字符串
    '''
    return DdddOcr(show_ad=False).classification(find_element(driver, by, value=value).screenshot_as_base64)