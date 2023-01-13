#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/9/2 1:21
@File  : test_xiaobai_case_submitBug.py
'''

'''
# filename = conftest.py 新增内容
from saf.utils.submitBugUtils import addZenTaoBUG
import pytest

TESTTYPE = 'sendMsg'

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """
    :param item     : 测试的单元对象
    :param call     : 测试的步骤：when（setup, call, teardown）三个步骤
    outcome         : 用例测试结果对象
    """
    outcome = yield                     # 获取每一条用例的执行结果
    report = outcome.get_result()
    if report.outcome == 'failed':
        if 'submitBug' == TESTTYPE:
            doc = item.function.__doc__
            doc = str(doc).replace('\n', '<br>')
            addZenTaoBUG(title=item.function.__name__,
                          steps=f'{doc}预期结果：passed<br>测试结果：{report.outcome}')
'''