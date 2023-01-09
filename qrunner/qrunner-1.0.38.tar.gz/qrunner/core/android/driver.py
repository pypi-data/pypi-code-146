import os
import re
import time

import allure
import requests
import six
import uiautomator2 as u2

from qrunner.core.android.common import check_device
from qrunner.utils.exceptions import ScreenFailException
from qrunner.utils.log import logger
from qrunner.running.config import Qrunner


class AndroidDriver(object):

    def __init__(self, device_id=None):
        self.device_id = check_device(device_id)
        logger.info(f'初始化安卓驱动: {self.device_id}')
        self.pkg_name = None
        self.d = u2.connect(self.device_id)
        # 配置点击前延时0.5s，点击后延时1s
        self.d.settings['operation_delay'] = (.5, .5)

    @property
    def info(self):
        """连接信息"""
        logger.info(f"获取连接信息")
        return self.d.info

    @property
    def app_info(self, pkg_name=None):
        """获取指定应用信息"""
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"获取指定应用信息: {pkg_name}")
        info = self.d.app_info(pkg_name)
        return info

    @property
    def device_info(self):
        """获取设备信息"""
        logger.info(f"获取设备信息")
        info = self.d.device_info
        return info

    @property
    def page_content(self):
        """获取页面xml内容"""
        return self.d.dump_hierarchy()

    def uninstall_app(self, pkg_name=None):
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"卸载应用: {pkg_name}")
        self.d.app_uninstall(pkg_name)

    @staticmethod
    def download_apk(src):
        """下载安装包"""
        if isinstance(src, six.string_types):
            if re.match(r"^https?://", src):
                logger.info(f'下载中: {src}')
                file_path = os.path.join(os.getcwd(), src.split('/')[-1])
                r = requests.get(src, stream=True)
                if r.status_code != 200:
                    raise IOError(
                        "Request URL {!r} status_code {}".format(src, r.status_code))
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                logger.info(f'下载成功: {file_path}')
                return file_path
            elif os.path.isfile(src):
                return src
            else:
                raise IOError("file {!r} not found".format(src))

    def install_app(self, apk_path, auth=True, new=True, pkg_name=None):
        import subprocess

        """
        安装应用，push改成adb命令之后暂时无法支持远程手机调用
        @param pkg_name: 应用包名
        @param apk_path: 安装包链接，支持本地路径以及http路径
        @param auth: 是否进行授权
        @param new: 是否先卸载再安装
        """
        logger.info(f"安装应用: {apk_path}")
        # 卸载
        if new is True:
            if pkg_name is None:
                pkg_name = self.pkg_name
            self.uninstall_app(pkg_name)

        # 下载
        source = self.download_apk(apk_path)

        # 把安装包push到手机上
        target = "/data/local/tmp/_tmp.apk"
        subprocess.check_call(f'adb -s {self.device_id} push {source} {target}', shell=True)

        # 安装
        cmd_list = ['pm', 'install', "-r", "-t", target]
        if auth is True:
            cmd_list.insert(4, '-g')
        logger.debug(f"{' '.join(cmd_list)}")
        cmd_str = f'adb -s {self.device_id} shell {" ".join(cmd_list)}'
        subprocess.check_call(cmd_str, shell=True)

        logger.info('安装成功')

        # 删除下载的安装包
        if 'http' in apk_path:
            os.remove(source)

    def start_app(self, pkg_name=None, stop=True):
        """启动应用
        @param pkg_name: 应用包名
        @param stop: 是否先关闭应用再启动
        """
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"启动应用: {pkg_name}")
        self.d.app_start(pkg_name, stop=stop, use_monkey=True)

    def stop_app(self, pkg_name=None):
        """停止指定应用"""
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"退出应用: {pkg_name}")
        self.d.app_stop(pkg_name)

    def clear_app(self, pkg_name=None):
        """清除应用缓存"""
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"清除应用缓存: {pkg_name}")
        self.d.app_clear(pkg_name)

    def wait_app_running(self, pkg_name=None, front=True, timeout=20):
        """
        等待应用运行
        @param pkg_name: 应用包名
        @param front: 是否前台运行
        @param timeout: 等待时间
        @return: 应用pid
        """
        if not pkg_name:
            pkg_name = self.pkg_name
        pid = self.d.app_wait(pkg_name, front=front, timeout=timeout)
        if not pid:
            logger.info(f"{pkg_name} is not running")
        else:
            logger.info(f"{pkg_name} pid is {pid}")
        return pid

    def health_check(self):
        """检查设备连接状态"""
        logger.info("检查并维持设备端守护进程处于运行状态")
        self.d.healthcheck()

    def open_url(self, url):
        """
        通过url打开web页面或者app schema
        @param url: 页面url，https://www.baidu.com，taobao://taobao.com
        @return:
        """
        logger.info(f"打开链接: {url}")
        self.d.open_url(url)

    def shell(self, cmd, timeout=60):
        """
        执行adb shell命令
        @param cmd: shell字符串或list，pwd，["ls", "-l"]
        @param timeout: 超时时间
        @return:
        """
        logger.info(f"执行shell命令: {cmd}")
        output, exit_code = self.d.shell(cmd, timeout=timeout)
        return output, exit_code

    def screenshot(self, file_name):
        """截图并保存至images目录"""
        if "." in file_name:
            file_name = file_name.split(r".")[0]
        # 截图并保存到当前目录的images文件夹中
        img_dir = os.path.join(os.getcwd(), "images")
        if os.path.exists(img_dir) is False:
            os.mkdir(img_dir)
        file_path = os.path.join(img_dir, f'{file_name}.png')
        logger.info(f'截图保存至: {file_path}')
        self.d.screenshot(file_path)
        return file_path

    def screenshot_with_time(self, file_name):
        """
        同screenshot方法，只是命名加上时间戳
        @param file_name: foo.png or fool
        @return:
        """
        logger.info(f'截图: {file_name}')
        # 把文件名处理成test.png的样式
        try:
            if "." in file_name:
                file_name = file_name.split(r".")[0]
            # 截图并保存到当前目录的images文件夹中
            img_dir = os.path.join(os.getcwd(), "images")
            if os.path.exists(img_dir) is False:
                os.mkdir(img_dir)
            time_str = time.strftime("%Y-%m-%d %H:%M:%S")
            file_path = os.path.join(img_dir, f"{time_str}-{file_name}.png")
            self.d.screenshot(file_path)
            logger.info(f"截图并保存至: {file_path}")
            # 上传allure报告
            allure.attach.file(
                file_path,
                attachment_type=allure.attachment_type.PNG,
                name=f"{file_name}.png",
            )
            return file_path
        except Exception as e:
            raise ScreenFailException(f"{file_name} 截图失败\n{str(e)}")

    def back(self):
        logger.info(f'返回上一页')
        self.d.press('back')

    def click(self, x, y):
        """点击坐标"""
        logger.info(f"单击坐标: {x},{y}")
        self.d.click(x, y)

    def click_alerts(self, alert_list: list):
        """点击弹窗"""
        logger.info(f"批量点击弹窗: {alert_list}")
        with self.d.watch_context() as ctx:
            for alert in alert_list:
                ctx.when(alert).click()
            ctx.wait_stable()

    def swipe(self, sx, sy, ex, ey):
        """滑动"""
        logger.info(f"从坐标{sx},{sy} 滑到 {ex},{ey}")
        self.d.swipe(sx, sy, ex, ey)

    def swipe_left(self, scale=0.9):
        """往左滑动"""
        logger.info("往左滑动")
        self.d.swipe_ext("left", scale=scale)

    def swipe_right(self, scale=0.9):
        """往右滑动"""
        logger.info("往右滑动")
        self.d.swipe_ext("right", scale=scale)

    def swipe_up(self, scale=0.8):
        """往上滑动"""
        logger.info("往上滑动")
        self.d.swipe_ext("up", scale=scale)

    def swipe_down(self, scale=0.8):
        """往下滑动"""
        logger.info("往下滑动")
        self.d.swipe_ext("down", scale=scale)

    def drag(self, sx, sy, ex, ey):
        """拖动"""
        logger.info(f"从坐标{sx},{sy} 拖动到坐标{ex},{ey}")
        self.d.drag(sx, sy, ex, ey)

    def set_text(self, text: str):
        """输入框内容"""
        logger.info(f'输入: {text}')
        self.d.send_keys(text)


if __name__ == '__main__':
    driver = AndroidDriver('UQG5T20414005787')
    driver.pkg_name = 'com.qizhidao.clientapp'
    print(driver.info)
    print(driver.device_info)
    print(driver.app_info)















