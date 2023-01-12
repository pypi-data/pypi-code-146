import inspect
import time


from qrunner.utils.exceptions import ElementNameEmptyException, NoSuchElementException, DriverNotFound, \
    LocMethodEmptyException
from qrunner.utils.log import logger
from qrunner.core.ios.driver import IosDriver


class IosElem(object):
    """
    IOS原生元素定义
    """

    def __init__(self,
                 driver: IosDriver = None,
                 name: str = None,
                 label: str = None,
                 value: str = None,
                 text: str = None,
                 class_name: str = None,
                 xpath: str = None,
                 index: int = 0,
                 desc: str = None):
        """
        @param driver,
        @param name,
        param label,
        param value,
        param text,
        param class_name,
        param xpath,
        param index: 索引,
        param desc: 控件名称
        """
        if driver is None:
            raise DriverNotFound('该控件未传入IOS driver参数')
        else:
            self._driver = driver

        self._kwargs = {}
        if name is not None:
            self._kwargs["name"] = name
        if label is not None:
            self._kwargs["label"] = label
        if value is not None:
            self._kwargs["value"] = value
        if text is not None:
            self._kwargs["text"] = text
        if class_name is not None:
            self._kwargs["className"] = class_name

        self._xpath = xpath
        self._index = index

        if desc is None:
            raise ElementNameEmptyException("请设置控件名称")
        else:
            self._desc = desc

        if self._xpath is None and not self._kwargs:
            raise LocMethodEmptyException("请至少指定一种定位方式")

    def _find_element(self, retry=3, timeout=3):
        """
        循环查找元素，查找失败先处理弹窗后重试
        @param retry: 重试次数
        @param timeout: 单次查找超时时间
        @return:
        """
        if self._xpath is not None:
            logger.info(f'查找元素: xpath={self._xpath}')
        else:
            logger.info(f'查找元素: {self._kwargs}[{self._index}]')

        self._element = self._driver.d.xpath(self._xpath) if \
            self._xpath else self._driver.d(**self._kwargs)[self._index]
        self._element.wait(timeout=timeout)
        if retry > 0:
            for i in range(retry):
                logger.info(f'第{i + 1}次重试:')
                try:
                    if self._element.wait(timeout=timeout):
                        return self._element
                except ConnectionError:
                    logger.info('出现链接异常，重新连接IOS设备')
                    # 由于WDA会意外链接错误
                    self.driver = IosDriver(self.driver.device_id)
                    time.sleep(5)
            else:
                frame = inspect.currentframe().f_back
                caller = inspect.getframeinfo(frame)
                logger.warning(f'【{caller.function}:{caller.lineno}】未找到元素 {self._kwargs}')
                return None
        else:
            return self._element

    def get_element(self, retry=3, timeout=3):
        """
        针对元素定位失败的情况，抛出NoSuchElementException异常
        @param retry:
        @param timeout:
        @return:
        """
        element = self._find_element(retry=retry, timeout=timeout)
        if element is None:
            self._driver.screenshot_with_time(f"[控件 {self._desc} 定位失败]")
            raise NoSuchElementException(f"[控件 {self._desc} 定位失败]")
        else:
            self._driver.screenshot_with_time(self._desc)
        return element

    @property
    def info(self):
        """获取元素信息"""
        logger.info(f"获取元素属性")
        return self.get_element().info

    @property
    def text(self):
        """获取元素文本"""
        logger.info(f"获取元素text属性")
        return self.get_element().text

    @property
    def bounds(self):
        """获取元素bounds属性"""
        logger.info(f"获取元素的bounds属性")
        return self.get_element().bounds

    @property
    def rect(self):
        """获取元素左上角坐标和宽高"""
        logger.info(f"获取元素的左上角坐标和宽高")
        return [item * self._driver.d.scale for item in list(self.get_element().bounds)]

    def exists(self, timeout=3):
        """
        判断元素是否存在当前页面
        @param timeout:
        @return:
        """
        logger.info(f"判断元素是否存在:")
        element = self._find_element(retry=1, timeout=timeout)
        if element is None:
            return False
        return True

    def click(self, retry=3, timeout=3):
        """
        单击
        @param: retry，重试次数
        @param: timeout，每次重试超时时间
        """
        logger.info(f"点击元素")
        self.get_element(retry=retry, timeout=timeout).click()

    def click_exists(self, timeout=3):
        """元素存在时点击"""
        logger.info(f"存在才点击元素")
        if self.exists(timeout=timeout):
            self.click()

    def clear_text(self):
        """清除文本"""
        logger.info("清除文本")
        self.get_element().clear_text()

    def set_text(self, text):
        """输入内容"""
        logger.info(f"输入框文本 {text}")
        self.get_element().set_text(text)

    def scroll(self, direction=None):
        """
        滑动到元素可见的位置
        @param: direction，方向，"up", "down", "left", "right"
        @return:
        """
        if direction is not None:
            self.get_element().scroll(direction=direction)
        else:
            self.get_element().scroll()

    def swipe_left(self):
        """往左滑动"""
        self.get_element().swipe("left")

    def swipe_right(self):
        """往右滑动"""
        self.get_element().swipe("right")

    def swipe_up(self):
        """往上滑动"""
        self.get_element().swipe("up")

    def swipe_down(self):
        """往下滑动"""
        self.get_element().swipe("down")


if __name__ == '__main__':
    driver = IosDriver()
    IosElem(driver, value='1111', desc='手机桌面企知道app').set_text('2222')



