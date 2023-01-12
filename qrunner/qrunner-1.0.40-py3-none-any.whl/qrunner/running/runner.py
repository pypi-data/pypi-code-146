import inspect
import os

import pytest
from qrunner.running.config import Qrunner
from qrunner.utils.config import config
from qrunner.utils.log import logger
from qrunner.core.android.driver import AndroidDriver
from qrunner.core.ios.driver import IosDriver


class TestMain(object):
    """
    Support for app、web、http
    """
    def __init__(self,
                 platform: str = None,
                 device_id: str = None,
                 pkg_name: str = None,
                 pkg_url: str = None,
                 browser: str = 'chrome',
                 case_path: str = None,
                 rerun: int = 0,
                 concurrent: bool = False,
                 base_url: str = None,
                 headers: dict = None,
                 login_headers: dict = None,
                 timeout: int = 10,
                 env: str = None
                 ):
        """

        @param platform: 平台，android、ios、web、api
        @param device_id: 设备id，针对安卓和ios
        @param pkg_name: 应用包名，针对安卓和ios
        @param pkg_url: 应用安装包，针对安卓和ios
        @param browser: 浏览器类型，chrome、firefox、edge、safari
        @param case_path: 用例目录，默认代表当前文件、.代表当前目录
        @param rerun: 失败重试次数
        @param concurrent: 是否并发执行，针对接口
        @param base_url: 域名，针对接口和web
        @param headers: 登录和游客请求头，针对接口和web，格式: {
            "login": {},
            "visit": {}
        }
        @param login_headers: 登录请求头，针对接口和web，以字典形式传入需要的参数即可
        @param timeout: 超时时间，针对接口和web
        @param env: 测试数据所属环境
        """
        # 将数据写入全局变量
        config.set('common', 'platform', platform)
        if platform == 'android':
            Qrunner.driver = AndroidDriver(device_id)
            Qrunner.driver.pkg_name = pkg_name
            if pkg_url is not None:
                Qrunner.driver.install_app(pkg_url)
        elif platform == 'ios':
            Qrunner.driver = IosDriver(device_id)
            Qrunner.driver.pkg_name = pkg_name
            if pkg_url is not None:
                Qrunner.driver.install_app(pkg_url)
        # config.set('app', 'device_id', device_id)
        # config.set('app', 'pkg_name', pkg_name)
        # Qrunner.pkg_name = pkg_name
        # Qrunner.pkg_url = pkg_url
        config.set('web', 'browser', browser)
        config.set('common', 'base_url', base_url)
        if headers is not None:
            login_ = headers.pop('login', {})
            config.set('common', 'login', login_)
            visit_ = headers.pop('visit', {})
            config.set('common', 'visit', visit_)
        if login_headers is not None:
            config.set('common', 'login', login_headers)
        config.set('common', 'timeout', timeout)
        config.set('common', 'env', env)

        # 执行用例
        logger.info('执行用例')
        if case_path is None:
            stack_t = inspect.stack()
            ins = inspect.getframeinfo(stack_t[1][0])
            file_dir = os.path.dirname(os.path.abspath(ins.filename))
            file_path = ins.filename
            if "\\" in file_path:
                this_file = file_path.split("\\")[-1]
            elif "/" in file_path:
                this_file = file_path.split("/")[-1]
            else:
                this_file = file_path
            case_path = os.path.join(file_dir, this_file)
        logger.info(f'用例路径: {case_path}')
        cmd_list = [
            '-sv',
            '--reruns', str(rerun),
            '--alluredir', 'allure-results', '--clean-alluredir'
        ]
        if case_path:
            cmd_list.insert(0, case_path)
        if concurrent:
            """仅支持http接口测试和web测试，并发基于每个测试类，测试类内部还是串行执行"""
            cmd_list.insert(1, '-n')
            cmd_list.insert(2, 'auto')
            cmd_list.insert(3, '--dist=loadscope')
        logger.info(cmd_list)
        pytest.main(cmd_list)

        # 配置文件恢复默认
        config.set('common', 'platform', None)
        config.set('app', 'device_id', None)
        config.set('app', 'pkg_name', None)
        config.set('web', 'browser', None)
        config.set('common', 'base_url', None)
        config.set('common', 'login', {})
        config.set('common', 'visit', {})
        config.set('common', 'timeout', None)
        config.set('common', 'env', None)


main = TestMain


if __name__ == '__main__':
    main()

