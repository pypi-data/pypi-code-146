#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/28 23:37
@File  : elementUtils.py
'''
from saf import WebDriver, By
from time import sleep

def find_element(driver: WebDriver = None,
                 by: str = By.XPATH,
                 value: str = '',
                 total_time: int = 30,
                 step_time: float = 0.5):
    '''
    通用定位元素方法
    :param driver       : 浏览器对象
    :param by           : 定位表达式
    :param value        : 定位表达式值
    :param total_time   : 定位超时时间（单位：秒）
    :param step_time    : 每次间隔定位时间（单位：秒）
    :return:
    '''
    while 1:
        if total_time > 0:
            if 0 == len(driver.find_elements(by=by, value=value)):
                sleep(step_time)
                total_time -= step_time
            else:
                return driver.find_element(by=by, value=value)
        else:
            break
    return None

def find_elements(driver: WebDriver = None, by: str = By.XPATH, value: str = ''):
    '''
    通用定位元素（复数）
    :param driver:
    :param by:
    :param value:
    :return:
    '''
    return driver.find_elements(by=by, value=value)