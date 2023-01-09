import time
from typing import Union

from qrunner.core.h5.driver import H5Driver
from qrunner.core.web.driver import WebDriver
from qrunner.core.ios.driver import IosDriver
from qrunner.core.android.driver import AndroidDriver
from qrunner.utils.log import logger
from qrunner.core.android.element import AdrElem
from qrunner.core.ios.element import IosElem
from qrunner.core.web.element import WebElem
from qrunner.core.ocr.element import OCRElem
from qrunner.core.image.element import ImageElem
from qrunner.utils.exceptions import ElementNameEmptyException, NoSuchDriverType


def Elem(
        res_id: str = None,
        class_name: str = None,
        text: str = None,
        name: str = None,
        label: str = None,
        value: str = None,
        id_: str = None,
        link_text: str = None,
        partial_link_text: str = None,
        tag_name: str = None,
        css: str = None,
        image: str = None,
        xpath: str = None,
        index: int = None,
        desc: str = None
):
    _kwargs = {}
    if res_id is not None:
        _kwargs["res_id"] = res_id
    if class_name is not None:
        _kwargs["class_name"] = class_name
    if text is not None:
        _kwargs["text"] = text
    if name is not None:
        _kwargs["name"] = name
    if label is not None:
        _kwargs["label"] = label
    if value is not None:
        _kwargs["value"] = value
    if id_ is not None:
        _kwargs["id_"] = id_
    if link_text is not None:
        _kwargs["link_text"] = link_text
    if partial_link_text is not None:
        _kwargs["partial_link_text"] = partial_link_text
    if tag_name is not None:
        _kwargs["tag_name"] = tag_name
    if css is not None:
        _kwargs["css"] = css
    if image is not None:
        _kwargs["image"] = image
    if xpath is not None:
        _kwargs["xpath"] = xpath
    if index is not None:
        _kwargs["index"] = index
    if desc is None:
        raise ElementNameEmptyException("请设置控件名称")
    else:
        _kwargs["desc"] = desc
    return _kwargs


class Page(object):
    """页面基类，用于pom模式封装"""

    def __init__(self, driver: Union[AndroidDriver, IosDriver, WebDriver, H5Driver]):
        self.driver = driver

    @staticmethod
    def sleep(n):
        """休眠"""
        logger.info(f"休眠 {n} 秒")
        time.sleep(n)

    def elem(self, kwargs):
        """封装安卓、ios、web元素"""
        if isinstance(self.driver, AndroidDriver):
            return AdrElem(self.driver, **kwargs)
        elif isinstance(self.driver, IosDriver):
            return IosElem(self.driver, **kwargs)
        elif isinstance(self.driver, WebDriver):
            return WebElem(self.driver, **kwargs)
        else:
            raise NoSuchDriverType('不支持的驱动类型')

    def adr_elem(self, kwargs):
        return AdrElem(self.driver, **kwargs)

    def ios_elem(self, kwargs):
        return IosElem(self.driver, **kwargs)

    def web_elem(self, kwargs):
        return WebElem(self.driver, **kwargs)

    def ocr_elem(self, kwargs):
        return OCRElem(self.driver, **kwargs)

    def image_elem(self, kwargs):
        return ImageElem(self.driver, **kwargs)

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



