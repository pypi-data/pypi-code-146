import re
import time
from typing import Union

import jmespath
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from qrunner.core.android.driver import AndroidDriver
from qrunner.core.android.element import AdrElem
from qrunner.core.api.request import HttpRequest, ResponseResult, formatting
from qrunner.core.h5.driver import H5Driver
from qrunner.core.ios.driver import IosDriver
from qrunner.core.ios.element import IosElem
from qrunner.core.web.driver import WebDriver
from qrunner.core.web.element import WebElem
from qrunner.core.ocr.element import OCRElem
from qrunner.core.image.element import ImageElem
from qrunner.utils.config import config
from qrunner.utils.log import logger
from qrunner.running.config import Qrunner
from qrunner.utils.exceptions import PlatformError, NoSuchDriverType


class TestCase(HttpRequest):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    driver: Union[AndroidDriver, IosDriver, WebDriver, H5Driver] = None

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
        # 初始化driver
        platform = config.get_platform()
        if platform == "web":
            browser = config.get_browser()
            cls.driver = WebDriver(browser)
        elif platform in ["android", "ios"]:
            cls.driver = Qrunner.driver
        elif platform == 'api':
            pass
        else:
            raise PlatformError(f"平台设置错误: {platform}，不是android、ios、web、api其中一个")
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        if isinstance(cls().driver, WebDriver):
            cls().driver.quit()
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
        if isinstance(self.driver, (AndroidDriver, IosDriver)):
            self.driver.start_app()
        self.start()

    def teardown_method(self):
        self.end()
        if self.driver is not None:
            self.driver.screenshot_with_time('用例执行完成截图')
        if isinstance(self.driver, (AndroidDriver, IosDriver)):
            self.driver.stop_app()
        take_time = time.time() - self.start_time
        logger.debug("[run_time]: {:.2f} s".format(take_time))

    # 公共方法
    @staticmethod
    def sleep(n: int):
        """休眠"""
        logger.debug(f"等待: {n}s")
        time.sleep(n)

    # UI自动化
    def elem(self, *args, **kwargs):
        """封装安卓、ios、web元素"""
        if isinstance(self.driver, AndroidDriver):
            return AdrElem(self.driver, *args, **kwargs)
        elif isinstance(self.driver, IosDriver):
            return IosElem(self.driver, *args, **kwargs)
        elif isinstance(self.driver, WebDriver):
            return WebElem(self.driver, *args, **kwargs)
        else:
            raise NoSuchDriverType('不支持的驱动类型')

    def adr_elem(self, *args, **kwargs):
        """安卓元素"""
        return AdrElem(self.driver, *args, **kwargs)

    def ios_elem(self, *args, **kwargs):
        """ios元素"""
        return IosElem(self.driver, *args, **kwargs)

    def web_elem(self, *args, **kwargs):
        """web元素"""
        return WebElem(self.driver, *args, **kwargs)

    def ocr_elem(self, *args, **kwargs):
        """ocr识别元素"""
        return OCRElem(self.driver, *args, **kwargs)

    def image_elem(self, *args, **kwargs):
        """图像识别元素"""
        return ImageElem(self.driver, *args, **kwargs)

    def assert_in_page(self, expect_value, timeout=5):
        """断言页面包含文本"""
        for _ in range(timeout + 1):
            try:
                page_source = self.driver.page_content
                logger.info(f"断言: {page_source}\n包含 {expect_value}")
                assert expect_value in page_source, f"页面内容不包含 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            page_source = self.driver.page_content
            logger.info(f"断言: {page_source}\n包含 {expect_value}")
            assert expect_value in page_source, f"页面内容不包含 {expect_value}"

    def assert_not_in_page(self, expect_value, timeout=5):
        """断言页面不包含文本"""
        for _ in range(timeout + 1):
            try:
                page_source = self.driver.page_content
                logger.info(f"断言: {page_source}\n不包含 {expect_value}")
                assert expect_value not in page_source, f"页面内容不包含 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            page_source = self.driver.page_content
            logger.info(f"断言: {page_source}\n不包含 {expect_value}")
            assert expect_value not in page_source, f"页面内容仍然包含 {expect_value}"

    def assert_title(self, expect_value=None, timeout=5):
        """断言页面标题等于"""
        for _ in range(timeout + 1):
            try:
                title = self.driver.title
                logger.info(f"断言: 页面标题 {title} 等于 {expect_value}")
                assert expect_value == title, f"页面标题 {title} 不等于 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            title = self.driver.title
            logger.info(f"断言: 页面标题 {title} 等于 {expect_value}")
            assert expect_value == title, f"页面标题 {title} 不等于 {expect_value}"

    def assert_in_title(self, expect_value=None, timeout=5):
        """断言页面标题包含"""
        for _ in range(timeout + 1):
            try:
                title = self.driver.title
                logger.info(f"断言: 页面标题 {title} 包含 {expect_value}")
                assert expect_value in title, f"页面标题 {title} 不包含 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            title = self.driver.title
            logger.info(f"断言: 页面标题 {title} 包含 {expect_value}")
            assert expect_value in title, f"页面标题 {title} 不包含 {expect_value}"

    def assert_url(self, expect_value=None, timeout=5):
        """断言页面url等于"""
        for _ in range(timeout + 1):
            try:
                url = self.driver.url
                logger.info(f"断言: 页面url {url} 等于 {expect_value}")
                assert expect_value == url, f"页面url {url} 不等于 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            url = self.driver.url
            logger.info(f"断言: 页面url {url} 等于 {expect_value}")
            assert expect_value == url, f"页面url {url} 不等于 {expect_value}"

    def assert_in_url(self, expect_value=None, timeout=5):
        """断言页面url包含"""
        for _ in range(timeout + 1):
            try:
                url = self.driver.url
                logger.info(f"断言: 页面url {url} 包含 {expect_value}")
                assert expect_value in url, f"页面url {url} 不包含 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            url = self.driver.url
            logger.info(f"断言: 页面url {url} 包含 {expect_value}")
            assert expect_value in url, f"页面url {url} 不包含 {expect_value}"

    def assert_alert_text(self, expect_value):
        """断言弹窗文本"""
        alert_text = self.driver.alert_text
        logger.info(f"断言: 弹窗文本 {alert_text} 等于 {expect_value}")
        assert expect_value == alert_text, f"弹窗文本 {alert_text} 等于 {expect_value}"

    # API专用方法
    @staticmethod
    def assert_status_code(status_code):
        """
        断言状态码
        """
        actual_code = ResponseResult.status_code
        logger.info(f"断言: {actual_code} 等于 {status_code}")
        assert (
                actual_code == status_code
        ), f"status_code {ResponseResult} != {status_code}"

    @staticmethod
    def assert_schema(schema, response=None) -> None:
        """
        Assert JSON Schema
        doc: https://json-schema.org/
        """
        logger.info(f"assertSchema -> {formatting(schema)}.")

        if response is None:
            response = ResponseResult.response

        try:
            validate(instance=response, schema=schema)
        except ValidationError as msg:
            assert "Response data" == "Schema data", msg

    @staticmethod
    def assert_eq(path, value):
        """
        功能同assertPath，用于兼容历史代码
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 等于 {value}")
        assert search_value == value, f"{search_value} != {value}"

    @staticmethod
    def assert_not_eq(path, value):
        """
        值不等于
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不等于 {value}")
        assert search_value != value, f"{search_value} 等于 {value}"

    @staticmethod
    def assert_len_eq(path, value):
        """
        断言列表长度等于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 等于 {value}")
        assert len(search_value) == value, f"{search_value} 的长度不等于 {value}"

    @staticmethod
    def assert_len_gt(path, value):
        """
        断言列表长度大于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 大于 {value}")
        assert len(search_value) > value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assert_len_gt_or_eq(path, value):
        """
        断言列表长度大于等于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 大于等于 {value}")
        assert len(search_value) >= value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assert_len_lt(path, value):
        """
        断言列表长度小于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 小于 {value}")
        assert len(search_value) < value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assert_len_lt_or_eq(path, value):
        """
        断言列表长度小于等于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 小于等于 {value}")
        assert len(search_value) <= value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assert_gt(path, value):
        """
        值大于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 大于 {value}")
        assert search_value > value, f"{search_value} 不大于 {value}"

    @staticmethod
    def assert_gt_or_eq(path, value):
        """
        值大于等于
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 大于等于 {value}")
        assert search_value >= value, f"{search_value} 小于 {value}"

    @staticmethod
    def assert_lt(path, value):
        """
        值小于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 小于 {value}")
        assert search_value < value, f"{search_value} 不大于 {value}"

    @staticmethod
    def assert_lt_or_eq(path, value):
        """
        值小于等于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 小于等于 {value}")
        assert search_value <= value, f"{search_value} 不大于 {value}"

    @staticmethod
    def assert_range(path, start, end):
        """值在(start, end)范围内
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 在 [{start}, {end}] 范围内")
        assert (search_value >= start) & (
                search_value <= end
        ), f"{search_value} 不在[{start}, {end}]范围内"

    @staticmethod
    def assert_in(path, value):
        """
        断言匹配结果被value_list包含
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 被 {value} 包含")
        assert search_value in value, f"{value} 不包含 {search_value}"

    @staticmethod
    def assert_not_in(path, value):
        """
        断言匹配结果不被value_list包含
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不被 {value} 包含")
        assert search_value not in value, f"{value} 包含 {search_value}"

    @staticmethod
    def assert_not_exists(path):
        """断言字段不存在"""
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {path} 不存在或值为None")
        assert search_value is None, f"仍然包含 {path} 为 {search_value}"

    @staticmethod
    def assert_contain(path, value):
        """
        断言匹配结果包含value
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 包含 {value}")
        assert value in search_value, f"{search_value} 不包含 {value}"

    @staticmethod
    def assert_not_contain(path, value):
        """
        断言匹配结果不包含value
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不包含 {value}")
        assert value not in search_value, f"{search_value} 包含 {value}"

    @staticmethod
    def assert_type_match(path, value_type):
        """
        类型匹配
        doc: https://jmespath.org/
        """
        if not isinstance(value_type, type):
            if value_type == "int":
                value_type = int
            elif value_type == "str":
                value_type = str
            elif value_type == "list":
                value_type = list
            elif value_type == "dict":
                value_type = dict
            else:
                value_type = str

        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 是 {value_type} 类型")
        assert isinstance(
            search_value, value_type
        ), f"{search_value} 不是 {value_type} 类型"

    @staticmethod
    def assert_starts_with(path, value):
        """
        以什么开头
        doc: https://jmespath.org/
        """
        search_value: str = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 以 {value} 开头")
        assert search_value.startswith(value), f"{search_value} 不以 {value} 开头"

    @staticmethod
    def assert_ends_with(path, value):
        """
        以什么结尾
        doc: https://jmespath.org/
        """
        search_value: str = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 以 {value} 结尾")
        assert search_value.endswith(value), f"{search_value} 不以 {value} 结尾"

    @staticmethod
    def assert_regex_match(path, value):
        """
        正则匹配
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        match_obj = re.match(r"" + value, search_value, flags=re.I)
        logger.info(f"断言: {search_value} 匹配正则表达式 {value} 成功")
        assert match_obj is not None, f"结果 {search_value} 匹配失败"
