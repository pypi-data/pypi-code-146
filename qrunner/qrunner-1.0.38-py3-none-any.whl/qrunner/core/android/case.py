import time
# import allure
from qrunner.utils.log import logger
from qrunner.utils.config import conf
from qrunner.core.android.driver import AndroidDriver
from qrunner.core.android.element import AndroidElement


class AndroidTestCase(object):
    """
    测试用例基类，所有测试用例需要继承该类
    """
    driver = None

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
        serial_no = conf.get_item('android', 'serial_no')
        cls.driver = AndroidDriver(serial_no)
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
        # 启动应用
        # self.driver.force_start_app()
        self.start()

    def teardown_method(self):
        self.end()
        # self.driver.screenshot('用例执行完成截图')
        # self.screenshot('用例执行完成截图')
        # 退出应用
        # self.driver.stop_app()
        logger.debug(f"[end_time]: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        take_time = time.time() - self.start_time
        logger.debug("[run_time]: {:.2f} s".format(take_time))

    @staticmethod
    def sleep(n: int):
        """休眠"""
        logger.debug(f'等待: {n}s')
        time.sleep(n)

    def install_app(self, url):
        """安装应用"""
        self.driver.install_app(apk_path=url)

    def new_install_app(self, url, pkg_name=None):
        """先卸载再安装应用"""
        self.driver.new_install_app(url, pkg_name)

    def uninstall_app(self, pkg=None):
        """卸载应用"""
        self.driver.uninstall_app(pkg_name=pkg)

    def start_app(self, pkg=None):
        """强制启动应用"""
        self.driver.force_start_app(pkg_name=pkg)

    def stop_app(self, pkg=None):
        """停止应用"""
        self.driver.stop_app(pkg_name=pkg)

    def screenshot(self, file_name):
        """截图"""
        self.driver.screenshot(file_name)

    # def element(self, **kwargs):
    #     """
    #     定位元素
    #     :param kwargs: 元素定位方式
    #     :return: 根据平台返回对应的元素
    #     """
    #     return AndroidElement(**kwargs)
    #
    # def screenshot(self, file_name):
    #     # 截图保存本地
    #     file_path = self.driver.screenshot(file_name)
    #     # 上传allure报告
    #     allure.attach.file(file_path, attachment_type=allure.attachment_type.PNG, name=f'{file_name}.png')
    #     logger.debug(f'[截图并上传报告] {file_path}')
    #
    # def click_alerts(self, alert_list: list):
    #     """处理弹窗"""
    #     self.driver.click_alert(alert_list)
    #
    # def click(self, **kwargs):
    #     """点击"""
    #     self.element(**kwargs).click()
    #
    # def click_exists(self, **kwargs):
    #     """存在才点击"""
    #     self.element(**kwargs).click_exists(**kwargs)
    #
    # def input(self, text, **kwargs):
    #     """输入"""
    #     self.element(**kwargs).set_text(text)
    #
    # def input_password(self, text):
    #     """输入密码，仅安卓使用"""
    #     self.driver.set_password(text)
    #
    # def input_clear(self, **kwargs):
    #     """清除输入框"""
    #     self.element(**kwargs).clear_text()
    #
    # def get_text(self, **kwargs):
    #     """获取文本属性"""
    #     return self.element(**kwargs).text

    def assertText(self, expect_value, timeout=5):
        """断言页面包含文本"""
        for _ in range(timeout + 1):
            try:
                page_source = self.driver.get_page_content()
                assert expect_value in page_source, f'页面内容不包含 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            page_source = self.driver.get_page_content()
            assert expect_value in page_source, f'页面内容不包含 {expect_value}'

    def assertNotText(self, expect_value, timeout=5):
        """断言页面不包含文本"""
        for _ in range(timeout + 1):
            try:
                page_source = self.driver.get_page_content()
                assert expect_value not in page_source, f'页面内容不包含 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            page_source = self.driver.get_page_content()
            assert expect_value not in page_source, f'页面内容仍然包含 {expect_value}'

    def assertElement(self, timeout=5, **kwargs):
        """断言元素存在"""
        for _ in range(timeout + 1):
            try:
                element = AndroidElement(**kwargs)
                assert element.exists(), f'元素 {kwargs} 不存在'
                break
            except AssertionError:
                time.sleep(1)
        else:
            assert AndroidElement(**kwargs).exists(), f'元素 {kwargs} 不存在'

    def assertNotElement(self, timeout=5, **kwargs):
        """断言元素不存在"""
        for _ in range(timeout + 1):
            try:
                assert not AndroidElement(**kwargs).exists(), f'元素 {kwargs} 仍然存在'
                break
            except AssertionError:
                time.sleep(1)
        else:
            assert not AndroidElement(**kwargs).exists(), f'元素 {kwargs} 仍然存在'
