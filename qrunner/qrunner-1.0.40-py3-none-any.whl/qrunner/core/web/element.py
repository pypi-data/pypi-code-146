import inspect
import platform
from typing import Union

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from qrunner.utils.exceptions import ElementNameEmptyException, NoSuchElementException, DriverNotFound, \
    LocMethodEmptyException, LocMethodNotOne
from qrunner.utils.log import logger
from qrunner.core.web.driver import WebDriver
from qrunner.core.h5.driver import H5Driver

# 支持的定位方式
LOC_DICT = {
    "id_": By.ID,
    "name": By.NAME,
    "link_text": By.LINK_TEXT,
    "tag_name": By.TAG_NAME,
    "partial_link_text": By.PARTIAL_LINK_TEXT,
    "class_name": By.CLASS_NAME,
    "xpath": By.XPATH,
    "css": By.CSS_SELECTOR,
}


class WebElem:
    """
    根据定位方式定位元素并进行操作
    """

    def __init__(self,
                 driver: Union[WebDriver, H5Driver] = None,
                 id_: str = None,
                 name: str = None,
                 link_text: str = None,
                 partial_link_text: str = None,
                 tag_name: str = None,
                 class_name: str = None,
                 xpath: str = None,
                 css: str = None,
                 index: int = 0,
                 desc: str = None
                 ):
        """

        @param driver: 浏览器驱动
        @param id_: 根据标签id属性进行定位
        @param name: 根据标签name属性定位
        @param text: 根据标签内文本定位
        @param link_text: 根据超链接文本进行定位
        @param partial_link_text: 根据超链接文本的部分内容进行定位
        @param tag_name: 根据标签名进行定位
        @param class_name: 根据class属性进行定位
        @param xpath: 根据xpath进行定位
        @param css: 根据css selector进行定位
        @param index: 索引（因为可能定位到多个）
        @param desc: 元素描述，必填项
        """
        if driver is None:
            raise DriverNotFound('该控件未传入web driver参数')
        else:
            self._driver = driver

        self._kwargs = {}
        if id_ is not None:
            self._kwargs[LOC_DICT["id_"]] = id_
        if name is not None:
            self._kwargs[LOC_DICT["name"]] = name
        if link_text is not None:
            self._kwargs[LOC_DICT["link_text"]] = link_text
        if partial_link_text is not None:
            self._kwargs[LOC_DICT["partial_link_text"]] = partial_link_text
        if tag_name is not None:
            self._kwargs[LOC_DICT["tag_name"]] = tag_name
        if class_name is not None:
            self._kwargs[LOC_DICT["class_name"]] = class_name
        if xpath is not None:
            self._kwargs[LOC_DICT["xpath"]] = xpath
        if css is not None:
            self._kwargs[LOC_DICT["css"]] = css

        self._index = index

        if desc is None:
            raise ElementNameEmptyException("请设置控件名称")
        else:
            self._desc = desc

        if not self._kwargs:
            raise LocMethodEmptyException("请至少指定一种定位方式")
        if len(self._kwargs) > 1:
            raise LocMethodNotOne("定位方式只能有一种")
        self.k, self.v = next(iter(self._kwargs.items()))

    def _wait(self, timeout=3):
        try:
            WebDriverWait(self._driver.d, timeout=timeout).until(
                EC.visibility_of_element_located((self.k, self.v))
            )
            return True
        except Exception:
            return False

    def _find_element(self, retry=3, timeout=5):
        cur_retry = retry
        while not self._wait(timeout=timeout):
            if cur_retry > 0:
                logger.warning(f"第{retry-cur_retry+1}次重试，查找元素： {self._kwargs}")
                cur_retry -= 1
            else:
                frame = inspect.currentframe().f_back
                caller = inspect.getframeinfo(frame)
                logger.warning(
                    f"【{caller.function}:{caller.lineno}】Not found element {self._kwargs}"
                )
                return None
        elements = self._driver.d.find_elements(self.k, self.v)
        return elements

    def get_elements(self, retry=3, timeout=3):
        elements = self._find_element(retry=retry, timeout=timeout)
        if elements is None:
            self._driver.screenshot_with_time(f"[控件 {self._desc} 定位失败]")
            raise NoSuchElementException(f"[控件 {self._desc} 定位失败]")
        else:
            self._driver.screenshot_with_time(self._desc)
        return elements

    def get_element(self, retry=3, timeout=3):
        elements = self.get_elements(retry=retry, timeout=timeout)
        return elements[self._index]

    @property
    def rect(self):
        """获取的坐标位置不对，截图会偏"""
        logger.info(f"获取元素 {self._kwargs}的坐标")
        bounds = self.get_element().rect
        x = bounds["x"] * 2
        y = bounds["y"] * 2
        width = bounds["width"] * 2
        height = bounds["height"] * 2
        return [x, y, width, height]

    @property
    def display(self):
        logger.info(f"获取元素{self._kwargs}的display属性")
        displayed = self.get_element().is_displayed()
        return displayed

    @property
    def text(self):
        logger.info(f"获取元素 {self._kwargs} 文本")
        element = self.get_element()
        text = element.text
        return text

    def get_attr(self, attr_name):
        logger.info(f"获取属性{attr_name}的值")
        value = self.get_element().get_attribute(attr_name)
        return value

    def exists(self, timeout=3):
        logger.info(f"判断元素: {self._kwargs} 是否存在")
        element = self._find_element(retry=0, timeout=timeout)
        if element is None:
            return False
        return True

    def click(self, retry=3, timeout=5):
        logger.info(f"点击元素: {self._kwargs}")
        self.get_element(retry=retry, timeout=timeout).click()

    def click_exists(self, timeout=1):
        logger.info(f"存在才点击元素: {self._kwargs},{self._index}")
        if self.exists(timeout=timeout):
            self.click()

    def slow_click(self):
        logger.info(f"移动到元素{self._kwargs}，然后点击")
        elem = self.get_element()
        ActionChains(self._driver.d).move_to_element(elem).click(elem).perform()

    def right_click(self):
        logger.info(f"右键元素{self._kwargs}")
        elem = self.get_element()
        ActionChains(self._driver.d).context_click(elem).perform()

    def move_to_elem(self):
        logger.info(f"鼠标移动到元素{self._kwargs}上")
        elem = self.get_element()
        ActionChains(self._driver.d).move_to_element(elem).perform()

    def click_and_hold(self):
        logger.info(f"长按元素: {self._kwargs}")
        elem = self.get_element()
        ActionChains(self._driver.d).click_and_hold(elem).perform()

    def drag_and_drop(self, x, y):
        logger.info(f"拖动元素{self._kwargs}到坐标{x},{y}")
        elem = self.get_element()
        action = ActionChains(self._driver.d)
        action.drag_and_drop_by_offset(elem, x, y).perform()

    def double_click(self):
        logger.info(f"双击元素: {self._kwargs}")
        elem = self.get_element()
        ActionChains(self._driver.d).double_click(elem).perform()

    def set_text(self, text):
        logger.info(f"点击元素: {self._kwargs}，然后输入: {text}")
        self.get_element().send_keys(text)

    def clear_text(self):
        logger.info(f"清空文本")
        self.get_element().clear()

    def enter(self):
        logger.info(f"选中元素{self._kwargs}点击enter")
        self.get_element().send_keys(Keys.ENTER)

    def select_all(self) -> None:
        logger.info(f"选中元素{self._kwargs}, ctrl+a.")
        if platform.system().lower() == "darwin":
            self.get_element().send_keys(Keys.COMMAND, "a")
        else:
            self.get_element().send_keys(Keys.CONTROL, "a")

    def select_index(self, index):
        logger.info(f"选择第 {index} 个下拉列表")
        element = self.get_element()
        select = Select(element)
        select.select_by_index(index)

    def select_value(self, value):
        logger.info(f"选择id为 {value} 的下拉列表")
        element = self.get_element()
        select = Select(element)
        select.select_by_value(value)

    def select_text(self, text):
        logger.info(f"选择下拉列表 {text} 选项")
        element = self.get_element()
        select = Select(element)
        select.select_by_value(text)

    def submit(self):
        logger.info(f"提交表单: {self._kwargs}")
        elem = self.get_element()
        elem.submit()


if __name__ == '__main__':
    driver = WebDriver("chrome")
    driver.open_url('https://www.qizhidao.com')
    WebElem(driver, xpath='//*[@id="__layout"]/div/div[3]/div[1]/div[1]/div[2]/div[2]/a/div[3]/div/h2', desc='查专利入口').click()
    WebElem(driver, id_='driver-home-step1', desc='搜索框').set_text('无人机')
    WebElem(driver, id_='driver-home-step2', desc='搜索确认按钮').click()




