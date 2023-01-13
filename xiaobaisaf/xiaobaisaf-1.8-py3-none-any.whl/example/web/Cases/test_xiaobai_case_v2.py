#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/21 0:25
@File  : test_xiaobai_shop_v2.py
'''
import pytest
from saf import full_load

''' 参数化 '''

data2 = {
    'test_login': {
        'keys': 'username, password, _assert',
        'values': [('xiaobai', '12345', 200), ('xiaohui', '1234567', 200)]
    }
}

data3 = full_load(open('..\\data\\testCase.yaml', 'r').read())

# 内部数据
@pytest.mark.parametrize('username, password, _assert', [('xiaobai', '12345', 200), ('xiaohui', '1234567', 200)])
def test_xiaobai_login1(username, password, _assert):
    # 业务实现代码
    assert _assert == 200

# 外部数据
@pytest.mark.parametrize(data2['test_login']['keys'], data2['test_login']['values'])
def test_xiaobai_login2(username, password, _assert):
    # 业务实现代码
    assert _assert == 200


# 外部文件数据
@pytest.mark.parametrize(data3['test_login']['keys'], [eval(v) for v in data3['test_login']['values']])
def test_xiaobai_login3(username, password, _assert):
    # 业务实现代码
    assert _assert == 200

if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_xiaobai_case_v2.py'])
