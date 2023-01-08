from shutil import copyfile

from ..utils.config import AutostartConfig


class Autostart:

    def __init__(self, *args):

        self.config = AutostartConfig()

        for index, variable in enumerate(self.config.Variables):
            self.__dict__.update({variable: args[index]})

    def __create_copy(self):

        self.executor_name = self.executor_path.replace("\\", "/").split("/")[-1]
        copyfile(self.executor_path, rf"{self.config.ExecutorPath}\{self.executor_name}")

    def __add_to_autostart(self):

        with open(rf"{self.config.AutostartPath}\{self.config.AutostartName}.bat", "w+") as file:
            file.write(f'@echo off\nstart "{self.config.AutostartName}" "{self.config.ExecutorPath}\\{self.executor_name}"')

    def run(self):

        try:

            if self.statuses[0] is True:

                self.__create_copy()
                self.__add_to_autostart()

        except Exception as e:
            if self.errors is True: print(f"[AUTOSTART]: {repr(e)}")
