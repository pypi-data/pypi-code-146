import inspect
import typing

from uiautomator2 import UiObject
from uiautomator2.xpath import XPathSelector

from qrunner.core.android.driver import AndroidDriver
from qrunner.utils.exceptions import (
    ElementNameEmptyException,
    NoSuchElementException,
    DriverNotFound,
    LocMethodEmptyException)
from qrunner.utils.log import logger


class AdrElem(object):
    """
    安卓元素定义
    """

    def __init__(self,
                 driver: AndroidDriver = None,
                 res_id: str = None,
                 class_name: str = None,
                 text: str = None,
                 xpath: str = None,
                 index: int = 0,
                 desc: str = None):
        """
        @param driver: 安卓驱动，必填
        @param res_id: resourceId定位
        @param class_name: className定位
        @param text: text定位
        @param xpath: xpath定位
        @param index: 定位出多个元素时，指定索引
        @param desc: 元素描述，必填
        """
        if driver is None:
            raise DriverNotFound('该控件未传入安卓driver参数')
        else:
            self._driver = driver

        self._kwargs = {}
        if res_id is not None:
            pkg_name = self._driver.pkg_name
            if pkg_name is not None:
                if not res_id.startswith('com.'):
                    res_id = pkg_name + ':id/' + res_id
            self._kwargs["resourceId"] = res_id
        if class_name is not None:
            self._kwargs["className"] = class_name
        if text is not None:
            self._kwargs["text"] = text

        self._xpath = xpath
        self._index = index

        if desc is None:
            raise ElementNameEmptyException("请设置控件名称")
        else:
            self._desc = desc

        if self._xpath is None and not self._kwargs:
            raise LocMethodEmptyException("请至少指定一种定位方式")

    def find_element(self, retry=3, timeout=3):
        """
        为了留出异常处理的逻辑，所以加了一个find_element的方法，不然可以合并到get_element方法
        @param retry: 重试次数
        @param timeout: 每次查找时间
        @return:
        """
        if self._xpath is not None:
            logger.info(f'查找元素: xpath={self._xpath}')
        else:
            logger.info(f'查找元素: {self._kwargs}[{self._index}]')
        _element = self._driver.d.xpath(self._xpath) if \
            self._xpath is not None else self._driver.d(**self._kwargs)[self._index]
        while not _element.wait(timeout=timeout):
            if retry > 0:
                retry -= 1
                logger.warning(f'重试 查找元素： {self._kwargs},{self._index}')
            else:
                frame = inspect.currentframe().f_back
                caller = inspect.getframeinfo(frame)
                logger.warning(f'【{caller.function}:{caller.lineno}】未找到元素 {self._kwargs}')
                return None
        return _element

    def get_element(self, retry=3, timeout=3):
        """
        增加截图的方法
        @param retry: 重试次数
        @param timeout: 每次查找时间
        @return:
        """
        element = self.find_element(retry=retry, timeout=timeout)
        if element is None:
            self._driver.screenshot_with_time(f"[控件 {self._desc} 定位失败]")
            raise NoSuchElementException(f"[控件 {self._desc} 定位失败]")
        else:
            self._driver.screenshot_with_time(self._desc)
        return element

    @property
    def info(self):
        logger.info(f"获取元素信息")
        return self.get_element().info

    @property
    def text(self):
        logger.info(f"获取元素文本属性")
        return self.get_element().info.get("text")

    @property
    def bounds(self):
        logger.info(f"获取元素坐标")
        return self.get_element().info.get("bounds")

    def exists(self, timeout=3):
        logger.info(f"判断元素是否存在")
        element = self.find_element(retry=0, timeout=timeout)
        if element is None:
            # self._driver.screenshot(f'元素定位失败')
            return False
        return True

    @staticmethod
    def _adapt_center(e: typing.Union[UiObject, XPathSelector], offset=(0.5, 0.5)):
        if isinstance(e, UiObject):
            return e.center(offset=offset)
        else:
            return e.offset(offset[0], offset[1])

    def click(self, retry=3, timout=3):
        logger.info(f"点击元素")
        element = self.get_element(retry=retry, timeout=timout)
        # 这种方式经常点击不成功，感觉是页面刷新有影响
        # element.click()
        x, y = self._adapt_center(element)
        self._driver.d.click(x, y)

    def click_exists(self, timeout=3):
        logger.info(f"元素存在才点击")
        if self.exists(timeout=timeout):
            self.click()

    def set_text(self, text):
        logger.info(f"输入文本: {text}")
        self.get_element().set_text(text)

    def clear_text(self):
        logger.info("清除文本")
        self.get_element().clear_text()

    def drag_to(self, *args, **kwargs):
        logger.info(f"拖动至元素")
        self.get_element().drag_to(*args, **kwargs)

    def swipe_left(self):
        logger.info(f"左滑")
        self.get_element().swipe("left")

    def swipe_right(self):
        logger.info(f"右滑")
        self.get_element().swipe("right")

    def swipe_up(self):
        logger.info(f"上滑")
        self.get_element().swipe("up")

    def swipe_down(self):
        logger.info(f"下滑")
        self.get_element().swipe("down")


if __name__ == '__main__':
    driver = AndroidDriver()
    print(AdrElem(driver, text='企知道-测试版', desc='企知道app').exists())

