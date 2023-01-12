import argparse

from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager

from qrunner import __description__, __version__, logger
from qrunner.scaffold import create_scaffold
from qrunner.utils.webdriver_manager_extend import ChromeDriverManager


def main():
    """API test: parse command line options and run commands."""
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", help="版本号"
    )
    parser.add_argument(
        "-n", "--project_name", dest="project_name", help="项目名称，用于创建demo"
    )
    parser.add_argument(
        "-p", "--platform", dest="platform", help="所属平台，android、ios、web、api，用于创建demo"
    )
    parser.add_argument(
        "-i", "--install", dest="install", help="浏览器驱动名称，chrome、firefox、edge，用于安装浏览器驱动"
    )

    args = parser.parse_args()
    version = args.version
    project = args.project_name
    platform = args.platform
    install = args.install

    if version:
        print(__version__)
        return 0
    if project:
        if platform:
            create_scaffold(project, platform)
        else:
            print("请输入-p参数设置所属平台")
        return 0
    if install:
        install_driver(install)
        return 0


def install_driver(browser: str) -> None:
    """
    Download and install the browser driver
    :param browser: The Driver to download. Pass as `chrome/firefox/ie/edge`. Default Chrome.
    :return:
    """

    if browser == "chrome":
        driver_path = ChromeDriverManager().install()
        logger.info(f"Chrome Driver[==>] {driver_path}")
    elif browser == "firefox":
        driver_path = GeckoDriverManager().install()
        logger.info(f"Firefox Driver[==>] {driver_path}")
    elif browser == "ie":
        driver_path = IEDriverManager().install()
        logger.info(f"IE Driver[==>] {driver_path}")
    elif browser == "edge":
        driver_path = EdgeChromiumDriverManager().install()
        logger.info(f"Edge Driver[==>] {driver_path}")
    else:
        raise NameError(f"Not found '{browser}' browser driver.")
