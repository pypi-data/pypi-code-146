#!/usr/bin/python3
from importlib.metadata import version
import sys
import os
import requests
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWidgets import QApplication


def main():
    from devoud import __version__
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            return print('Использование:       devoud [ссылка/опция]\n\n'
                         'Доступные опции:\n'
                         ' devoud              запуск браузера\n'
                         ' devoud \'ссылка\'     запустить браузер и открыть ссылку в новой вкладке\n'
                         ' devoud help         помощь по командам\n'
                         ' devoud update       проверить и установить обновления\n'
                         ' devoud version      показать текущую версию браузера')
        elif sys.argv[1] == 'version':
            return print(f'Devoud ({__version__}) by OneEyedDancer')
        elif sys.argv[1] == 'update':
            from .lib.filesystem import FileSystem
            with open(f'{FileSystem.path}/data/requirements.txt') as req_file:
                packages = ['devoud'] + req_file.read().splitlines()
            if input('Проверить доступные обновления? [Y/N]: ').lower() == 'y':
                for package in packages:
                    print('-'*10)
                    print('>', package)
                    current_version = version(package)
                    server_version = max(requests.get(f"https://pypi.org/pypi/{package}/json").json()["releases"].keys())
                    if current_version == server_version:
                        print(f'    У вас установлена последняя версия({current_version}), обновление не требуется')
                    else:
                        print('     Текущая версия:', current_version)
                        print('     Последняя версия на сервере:', server_version)
                print('-' * 10)
                if input('Обновить пакеты до актуальных версий с сервера? [Y/N]: ').lower() == 'y':
                    for package in packages:
                        os.system(f'pip3 install {package} --upgrade')
                    return print('Операция завершена!')
            return print('Операция отменена')

    from devoud.lib.browser_window import BrowserWindow
    from devoud.lib.browser_page_wrapper import BrowserPageWrapper
    from devoud.lib.browser_ad_blocker import AdBlocker, WebEngineUrlRequestInterceptor

    print(f'''---------------------------------------------
  Добро пожаловать в
  _____  ________      ______  _    _ _____  
 |  __ \|  ____\ \    / / __ \| |  | |  __ \ 
 | |  | | |__   \ \  / / |  | | |  | | |  | |
 | |  | |  __|   \ \/ /| |  | | |  | | |  | |
 | |__| | |____   \  / | |__| | |__| | |__| |
 |_____/|______|   \/   \____/ \____/|_____/ 
    ({__version__}) by OneEyedDancer            
---------------------------------------------''')
    os.environ["QT_FONT_DPI"] = "96"
    args = []
    app = QApplication(sys.argv + args)

    window = BrowserWindow()

    if len(sys.argv) > 1:
        if BrowserPageWrapper.is_url(sys.argv[1]):
            # открытие ссылки в новой вкладке
            window.tab_widget.create_tab(sys.argv[1])

    size = window.screen().availableGeometry()
    window.resize(size.width() * 2 / 3, size.height() * 2 / 3)
    window.show()

    window.change_style()

    ad = AdBlocker()
    if ad.load_file():
        interceptor = WebEngineUrlRequestInterceptor(ad.rules)
        QWebEngineProfile.defaultProfile().setUrlRequestInterceptor(interceptor)

    app.exec()


if __name__ == '__main__':
    main()
