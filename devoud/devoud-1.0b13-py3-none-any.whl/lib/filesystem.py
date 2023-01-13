import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from sys import platform
from shutil import copytree, ignore_patterns
from pyshortcuts import make_shortcut


class FileSystem:
    os = platform
    path = Path(__file__).parents[1]
    local_path_config = Path(f'{path}/user/settings.json')
    default_settings = {"saveHistory": False,
                        "restoreTabs": False,
                        "easyprivacy": False,
                        "systemWindowFrame": False,
                        "theme": "night",
                        "homePage": "ya.ru",
                        "searchEngine": "Yandex",
                        "newPage": "Заставка с часами",
                        "TabBarPosition": "Снизу"}

    def __init__(self):
        """Сменит текущий каталог и проверит все необходимые файлы"""
        print('[Файлы]: Инициализация файловой системы')
        print(f'[Файлы]: Текущая операционная система {self.os}')
        os.chdir(FileSystem.path)  # сменить текущий каталог

        os_path_config = {'linux': Path(f'{Path.home()}/.config/devoud/user/settings.json'),
                          'darwin': Path(f'{Path.home()}/.config/devoud/user/settings.json'),
                          'win32': Path(f'{Path.home()}/AppData/Roaming/devoud/user/settings.json')}

        self.__os_config_path = os_path_config.get(self.os, self.local_path_config)
        self.user_settings = FileSystem.default_settings
        self.__path_config = FileSystem.local_path_config
        self.__files_exist()

    def path_config(self):
        return self.__path_config

    def config_dir(self):
        return self.__path_config.parent

    def config_exist(self):
        return Path.exists(self.__path_config)

    def os_config_dir(self):
        return self.__os_config_path.parent

    def os_config_path_exist(self):
        return Path.exists(self.os_path_config())

    def os_path_config(self):
        return self.__os_config_path

    def create_launch_shortcut(self):
        icon = {'win32': './ui/png/browser_icon.ico',
                'darwin': './ui/svg/browser_icon.svg',
                'linux': './ui/svg/browser_icon.svg'}
        make_shortcut('./Devoud.py', name='Devoud', icon=icon[self.os],
                      terminal=False, desktop=False)
        print(f'[Файлы]: Ярлык для запуска браузера был создан')

    def open_in_file_manager(self, path):
        command = {'win32': ["explorer", path],
                   'darwin': ["open", path],
                   'linux': ["xdg-open", path]}
        subprocess.Popen(command[self.os])

    @staticmethod
    def human_bytes(B):
        """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2)  # 1,048,576
        GB = float(KB ** 3)  # 1,073,741,824
        TB = float(KB ** 4)  # 1,099,511,627,776

        if B < KB:
            return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B / KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B / MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B / GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B / TB)

    def __files_exist(self):
        """Проверка необходимых файлов для работы браузера"""
        print(f'[Файлы]: Проверка необходимых файлов')
        if not self.os_config_path_exist():
            if not Path.exists(FileSystem.local_path_config):
                Path.mkdir(FileSystem.local_path_config.parent, parents=True, exist_ok=True)
                with FileSystem.local_path_config.open('w') as config_file:
                    json.dump(FileSystem.default_settings, config_file, indent=4, ensure_ascii=False)
                    print(
                        f'[Файлы]: Конфигурационного файла не существует, он создан в ({FileSystem.local_path_config})')
                    self.create_launch_shortcut()
        else:
            self.__path_config = self.os_path_config()

        for data_file in ('history', 'bookmarks', 'tabs', 'downloads.json'):
            if not Path.exists(Path(f'{self.config_dir()}/{data_file}')):
                Path(f'{self.config_dir()}/{data_file}').touch()

        with self.path_config().open('r+') as config_file:
            try:
                self.user_settings = json.load(config_file)
            except json.decoder.JSONDecodeError:
                json.dump(FileSystem.default_settings, config_file, indent=4, ensure_ascii=False)
                print('[Файлы]: Неверные параметры, файл перезаписан со стандартными значениями')
            print(f'[Файлы]: Конфигурационный файл находится в ({self.path_config()})')

        # создать каталог под сгенерированные иконки
        Path.mkdir(Path(FileSystem.path, './ui/custom/svg'), parents=True, exist_ok=True)

    def create_os_config_path(self):
        if not self.os_config_path_exist():
            print(f"[Файлы]: Начат этап копирования локальной конфигурации")
            copytree(self.config_dir(), self.os_config_dir(), dirs_exist_ok=True, ignore=ignore_patterns('Cache'))
            old_config_dir_name = f'{self.config_dir()} ({datetime.now().strftime("%d-%m-%Y %H-%M")}).old'
            Path.rename(self.config_dir(), old_config_dir_name)
            print(f"[Файлы]: Старая конфигурация была сохранена в каталоге программы с датой копирования")
            self.__files_exist()

    def restore_option(self, option):
        with self.path_config().open('w') as file:
            self.user_settings[option] = FileSystem.default_settings[option]
            json.dump(self.user_settings, file, indent=4, ensure_ascii=False)
            print('[Файлы]: Часть конфигурационного файла отсутствует, опция перезаписана со стандартными значениями')
            return self.user_settings[option]

    def get_option(self, option):
        try:
            return self.user_settings[option]
        except KeyError:
            self.restore_option(option)

    def save_option(self, option, arg='invert'):
        """Без параметров инвертирует значение (False->True)"""
        try:
            if arg == 'invert':
                self.user_settings[option] = not self.user_settings[option]
            else:
                self.user_settings[option] = arg
            with self.path_config().open('w') as file:
                json.dump(self.user_settings, file, indent=4, ensure_ascii=False)
        except KeyError:
            self.restore_option(option)
