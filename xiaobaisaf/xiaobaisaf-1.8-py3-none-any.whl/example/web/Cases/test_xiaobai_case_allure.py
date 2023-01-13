#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/24 22:05
@File  : test_xiaobai_allure_shop.py
'''
import pytest
import allure

@allure.feature('下单')
class Test_order():
    @allure.story('登录')
    def test_login(self):
        ''' 登录 '''
        with allure.step('输入账户'):
            assert True
        with allure.step('输入密码'):
            assert True
        with allure.step('点击登录'):
            assert True

    @allure.story('搜索商品')
    def test_search(self):
        ''' 搜索商品 '''
        with allure.step('搜索框输入：苹果'):
            assert True
        with allure.step('点击搜索按钮'):
            assert False


'''
# 执行脚本
pytest test_xiaobai_case_allure.py --alluredir=../data

# 打开报告
allure serve ../data
或者
allure generate -c -o ../report ../data
allure open ../report
'''