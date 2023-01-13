#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/1/13 23:47
@File  : run.py
'''

import os
import pytest
from loguru import logger
from saf.example.api.Config.config import report, log

logger.add(log.path() + 'info.log', level='INFO', rotation='1 days', retention='7 days', enqueue=True, encoding='UTF-8')

if __name__ == '__main__':
    ''' 执行用例之前清理上次输出的测试报告文件 '''
    if os.path.isfile(report.html_path()):
        os.remove(report.html_path())
        logger.info(f'已经移除{report.html_path()}')

    ''' 批量执行TestCases目录下的所有测试用例 '''
    pytest.main(['-s', f'--html={report.html_path()}', '--self-contained-html', 'TestCases'])

    ''' 如果测试脚本之间不存在数据关联，可以使用多进程并发运行:-n=4  4表示四个进程 '''
    # pytest.main(['-s', '-n=4', f'--html={report.html_path()}', '--self-contained-html', 'TestCases'])

    ''' 测试用例执行结束之后，发送邮件 '''
    if os.path.isfile(report.html_path()):
        # os.system('python send_email_script.py')
        logger.info('含测试报告文件的邮件已发送')