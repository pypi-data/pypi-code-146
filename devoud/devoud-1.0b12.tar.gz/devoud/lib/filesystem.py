import json
import subprocess
from datetime import datetime
from pathlib import Path
from sys import platform
from shutil import copytree
import os


class FileSystem:
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
        os.chdir(FileSystem.path)  # сменить текущий каталог
        self.user_settings = FileSystem.default_settings
        self.__os_user_path_config = None
        self.__path_config = FileSystem.local_path_config
        self.__files_exist()

    def config_path(self):
        return self.__path_config

    def config_dir(self):
        return self.__path_config.parent

    def config_exist(self):
        return Path.exists(self.__path_config)

    def os_user_path(self):
        return self.__os_user_path_config

    def os_user_dir(self):
        return self.__os_user_path_config.parent

    def os_user_path_exist(self):
        return Path.exists(self.__os_user_path_config)

    def select_os_user_path(self):
        print('[OC]:', platform)
        if platform in ('linux', 'darwin'):
            self.__os_user_path_config = Path(f'{Path.home()}/.config/devoud/user/settings.json')
        elif platform == 'win32':
            self.__os_user_path_config = Path(f'{Path.home()}/AppData/Roaming/devoud/user/settings.json')
        else:
            print('[Файлы]: Программа пока не адаптирована под эту файловую систему, и все файлы будут храниться в '
                  'каталоге программы')

    def open_in_file_manager(self, path):
        if platform == 'win32':
            subprocess.check_call(["explorer", "/select", path])
        elif platform == 'darwin':
            subprocess.check_call(["open", path])
        else:
            subprocess.check_call(["xdg-open", path])

    def human_bytes(self, B):
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
        print(f'[Файлы]: Начат этап проверки файлов')
        self.select_os_user_path()
        if not Path.exists(self.__os_user_path_config):
            if not Path.exists(FileSystem.local_path_config):
                Path.mkdir(FileSystem.local_path_config.parent, parents=True, exist_ok=True)
                with FileSystem.local_path_config.open('w') as file1:
                    json.dump(FileSystem.default_settings, file1, indent=4, ensure_ascii=False)
                    print(f'[Файлы]: Конфигурационного файла не существует, он создался в ({FileSystem.local_path_config})')
        else:
            self.__path_config = self.__os_user_path_config

        for file2 in ('history', 'bookmarks', 'tabs', 'downloads.json'):
            if not Path.exists(Path(f'{self.config_dir()}/{file2}')):
                Path(f'{self.config_dir()}/{file2}').touch()

        with self.config_path().open() as file3:
            try:
                self.user_settings = json.load(file3)
            except json.decoder.JSONDecodeError:
                with self.config_path().open('w') as config_file:
                    json.dump(FileSystem.default_settings, config_file, indent=4, ensure_ascii=False)
                print('[Файлы]: Неверные параметры, файл перезаписан со стандартными значениями')
            print(f'[Файлы]: Конфигурационный файл находится в ({self.config_path()})')

        Path.mkdir(Path(FileSystem.path, './ui/custom/svg'), parents=True, exist_ok=True)

    def create_os_user_path(self):
        if not self.os_user_path_exist():
            try:
                print(f"[Файлы]: Начат этап копирования локальной конфигурации")
                copytree(self.config_dir(), self.os_user_dir())
                old_config_dir_name = f'{self.config_dir()} ({datetime.now().strftime("%d-%m-%Y %H-%M")}).old'
                Path.rename(self.config_dir(), old_config_dir_name)
                print(f"[Файлы]: Старая конфигурация была сохранена в каталоге программы с датой копирования")
                self.__files_exist()
            except Exception as error:
                print(f"[Файлы]: Ошибка операции создания пользовательского пути. {error}")
                return False
            else:
                print(f"[Файлы]: Копирование конфигурации завершено")
                return True

    def restore_option(self, option):
        with self.config_path().open('w') as file:
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
            with self.config_path().open('w') as file:
                json.dump(self.user_settings, file, indent=4, ensure_ascii=False)
        except KeyError:
            self.restore_option(option)
