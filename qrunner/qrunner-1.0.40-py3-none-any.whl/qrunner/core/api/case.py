import re
import time
import jmespath
from qrunner.utils.decorate import step
from qrunner.utils.log import logger
from qrunner.core.api.request import HttpRequest, ResponseResult


class TestCase(HttpRequest):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    # ---------------------初始化-------------------------------
    def start_class(self):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    def end_class(self):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        cls().end_class()

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    def setup_method(self):
        self.start_time = time.time()
        logger.debug(f"[start_time]: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.start()

    def teardown_method(self):
        self.end()
        logger.debug(f"[end_time]: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        take_time = time.time() - self.start_time
        logger.debug("[run_time]: {:.2f} s".format(take_time))

    @staticmethod
    def sleep(n: int):
        logger.debug(f'等待: {n}s')
        time.sleep(n)

    @staticmethod
    def assertStatusCode(status_code):
        """
        断言状态码
        """
        with step(f'断言响应状态码 == {status_code}'):
            actual_code = ResponseResult.status_code
            logger.info(f'断言 {actual_code} 等于 {status_code}')
            assert actual_code == status_code, \
                f'status_code {ResponseResult} != {status_code}'

    @staticmethod
    def assertPath(path, value):
        """
        功能同assertEq，用于兼容历史代码
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} == {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 等于 {value}')
            assert search_value == value, f'{search_value} != {value}'

    @staticmethod
    def assertNotEq(path, value):
        """
        值不等于
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} != {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 不等于 {value}')
            assert search_value != value, f"{search_value} 等于 {value}"

    @staticmethod
    def assertLenEq(path, value):
        """
        断言列表长度等于多少
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 的长度 == {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 的长度等于 {value}')
            assert len(search_value) == value, f"{search_value} 的长度不等于 {value}"

    @staticmethod
    def assertLenGt(path, value):
        """
        断言列表长度大于多少
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 的长度 > {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 的长度大于 {value}')
            assert len(search_value) > value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assertLenGtOrEq(path, value):
        """
        断言列表长度大于等于多少
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 的长度 >= {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 的长度大于等于 {value}')
            assert len(search_value) >= value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assertLenLt(path, value):
        """
        断言列表长度小于多少
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 的长度 < {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 的长度小于 {value}')
            assert len(search_value) < value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assertLenLtOrEq(path, value):
        """
        断言列表长度小于等于多少
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 的长度 <= {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 的长度小于等于 {value}')
            assert len(search_value) <= value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assertGt(path, value):
        """
        值大于多少
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} > {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 大于 {value}')
            assert int(search_value) > int(value), f"{search_value} 不大于 {value}"

    @staticmethod
    def assertGtOrEq(path, value):
        """
        值大于等于
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} >= {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            if isinstance(search_value, str):
                search_value = int(search_value)
            logger.info(f'断言 {search_value} 大于等于 {value}')
            assert search_value >= value, f"{search_value} 小于 {value}"

    @staticmethod
    def assertLt(path, value):
        """
        值小于多少
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} < {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 小于 {value}')
            assert int(search_value) < int(value), f"{search_value} 不大于 {value}"

    @staticmethod
    def assertLtOrEq(path, value):
        """
        值小于等于多少
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} <= {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 小于等于 {value}')
            assert int(search_value) <= int(value), f"{search_value} 不大于 {value}"

    @staticmethod
    def assertRange(path, start: int, end: int):
        """值在(start, end)范围内
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 在({start}, {end})范围内'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 在 ({start}, {end}) 范围内')
            assert (int(search_value) > start) & (int(search_value) < end), f'{search_value} 不在({start}, {end})范围内'

    @staticmethod
    def assertIn(path, value):
        """
        断言匹配结果被value_list包含
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 被 {value} 包含'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 被 {value} 包含')
            assert search_value in value, f"{value} 不包含 {search_value}"

    @staticmethod
    def assertNotIn(path, value):
        """
        断言匹配结果不被value_list包含
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 不被 {value} 包含'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 不被 {value} 包含')
            assert search_value not in value, f"{value} 包含 {search_value}"

    @staticmethod
    def assertNotExists(path):
        """断言字段不存在"""
        with step(f'断言响应中 {path} 值为None或字段不存在'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 为None')
            assert search_value is None, f'仍然包含 {path} 为 {search_value}'

    @staticmethod
    def assertContains(path, value):
        """
        断言匹配结果包含value
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 包含 {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 包含 {value}')
            assert value in search_value, f"{search_value} 不包含 {value}"

    @staticmethod
    def assertNotContains(path, value):
        """
        断言匹配结果不包含value
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 不包含 {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 不包含 {value}')
            assert value not in search_value, f"{search_value} 包含 {value}"

    @staticmethod
    def assertTypeMatch(path, value_type):
        """
        类型匹配
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 的数据类型等于 {value_type}'):
            if not isinstance(value_type, type):
                if value_type == 'int':
                    value_type = int
                elif value_type == 'str':
                    value_type = str
                elif value_type == 'list':
                    value_type = list
                elif value_type == 'dict':
                    value_type = dict
                else:
                    value_type = str

            search_value = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 的数据类型等于 {value_type}')
            assert isinstance(search_value, value_type), f'{search_value} 不是 {value_type} 类型'

    @staticmethod
    def assertStartsWith(path, value):
        """
        以什么开头
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 以 {value} 开头'):
            search_value: str = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 以 {value} 开头')
            assert search_value.startswith(value), f'{search_value} 不以 {value} 开头'

    @staticmethod
    def assertEndsWith(path, value):
        """
        以什么结尾
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 以 {value} 结尾'):
            search_value: str = jmespath.search(path, ResponseResult.response)
            logger.info(f'断言 {search_value} 以 {value} 结尾')
            assert search_value.endswith(value), f'{search_value} 不以 {value} 结尾'

    @staticmethod
    def assertRegexMatch(path, value):
        """
        正则匹配
        doc: https://jmespath.org/
        """
        with step(f'断言响应中 {path} 正则匹配表达式 {value}'):
            search_value = jmespath.search(path, ResponseResult.response)
            match_obj = re.match(r'' + value, search_value, flags=re.I)
            logger.info(f'断言 {search_value} 匹配正则表达式 {value}')
            assert match_obj is not None, f'结果 {search_value} 匹配失败'
