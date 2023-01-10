import os
import sys
import argparse
import platform
import time

import psutil
import subprocess

from uuid import UUID, getnode
from typing import Optional
from ..cls.utils import daemon_thread


# 检测PID是否在进程列表
def is_pid_exist(pid: int):
    return psutil.pid_exists(pid)


def kill_pid(pid: int):
    if is_pid_exist(pid) is True:
        os.kill(pid, 9)


def kill_process(name: str):
    os.popen(f"taskkill /im {name} -f")


# 显示全部进程
def get_all_pids():
    return psutil.pids()


# 获取当前进程ID
def get_current_pid():
    return os.getpid()


# 获取进程
def get_process(pid: int):
    return psutil.Process(pid)


# 获取进程信息
def get_process_info(pid: int) -> dict:
    info = {}
    p = get_process(pid)
    if p:
        with p.oneshot():
            info['memory'] = p.memory_info().rss/1024/1024
            info['threads'] = p.num_threads()
            info['connections'] = p.connections()
            info['cpu'] = p.cpu_percent()
            info['create'] = p.create_time()
    return info


def get_process_name(pid: int):
    return psutil.Process(pid).name()


def get_process_by_name(process_name: str, process_dir: Optional[str] = None):
    process_ext = os.path.splitext(process_name)[-1][1:]  # 进程后缀名
    for process in psutil.process_iter():
        if process_ext == 'exe':
            if process.name() == process_name:
                if process_dir is not None:
                    if process.cwd().replace('\\', '/') == process_dir:
                        return process.pid
                else:
                    return process.pid
        elif process_ext == 'py':
            if process.name() == 'python.exe':
                if process.cwd().replace('\\', '/') == process_dir:
                    return process.pid
    return -1


def get_process_by_path(path: str):
    process_dir = os.path.dirname(path).replace('\\', '/')
    process_name = os.path.basename(path)
    return get_process_by_name(process_name, process_dir)


def close_dump(child_id: int):
    # 检测崩溃弹框，关闭掉
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store_false', help='User name')
    parser.add_argument('-p', type=int, help='Process ID')
    parser.add_argument('-s', help='??')

    pids = get_all_pids()
    for pid in pids:
        if is_pid_exist(pid) is True:
            process = get_process(pid)
            if process is not None and 'WerFault.exe' in process.name():
                args, unknown_args = parser.parse_known_args(process.cmdline())
                if args.p == child_id:  # 如果进程子ID =
                    kill_pid(process.pid)


# 关闭进程
def close_process(pid: int, dump_close: bool = True):
    if dump_close is True:
        close_dump(pid)

    os.kill(pid, 9)  # 进行升级，退出此程序


# 启动进程
def open_process(process_path: str):
    if os.path.exists(process_path) is True:
        process_folder = os.path.dirname(process_path)
        process_ext = os.path.splitext(process_path)[-1][1:]  # 进程后缀名
        if process_ext == 'bat':
            return subprocess.Popen(f'cmd.exe /c {process_path}', creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=process_folder).pid  # 结束进程
        elif process_ext == 'exe':
            return subprocess.Popen(process_path, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=process_folder).pid  # 结束进程
        elif process_ext == 'py':
            return subprocess.Popen(f'python.exe {process_path}', creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=process_folder).pid  # 结束进程
    return -1


# 重启进程
def restart_process(process_path: str):
    pid = get_process_by_path(process_path)
    if pid > 0:
        close_process(pid)
    return open_process(process_path)


# 开机自启动
def auto_start(app_path: str):
    if platform.system().lower() == 'windows':
        import win32con
        from win32api import RegOpenKey, RegQueryValueEx, RegSetValueEx, RegCloseKey
        from win32con import KEY_ALL_ACCESS, HKEY_CURRENT_USER
        app_name = os.path.basename(app_path)
        app_ext = os.path.splitext(app_path)[1]
        reg_path = app_path
        reg_name = os.path.splitext(app_name)[0]
        if app_ext == '.py':
            reg_path = f"{os.path.dirname(app_path)}/{reg_name}.bat"
            base_dir = os.path.splitdrive(app_path)[0]  # 驱动器
            app_dir = os.path.dirname(app_path)  # 文件路径

            with open(reg_path, 'w') as f:
                f.write(f"@echo off\n")
                f.write(f"{base_dir}\n")
                f.write(f"cd {app_dir}\n")
                f.write(f"start {app_name}\n")
                f.write(f"exit")

        key = RegOpenKey(HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, KEY_ALL_ACCESS)
        try:
            reg_tuple = RegQueryValueEx(key, reg_name)
            if len(reg_tuple) > 0 and reg_tuple[0] != reg_path:
                RegSetValueEx(key, reg_name, 0, win32con.REG_SZ, reg_path)
                RegCloseKey(key)
            return True
        except Exception:
            RegSetValueEx(key, reg_name, 0, win32con.REG_SZ, reg_path)
            RegCloseKey(key)
    return False


# 重启自身
def restart():
    path = sys.executable
    if platform.system().lower() == 'windows':
        os.execv(path, [path, '"' + sys.argv[0] + '"'] + sys.argv[1:])
    else:
        os.execl(path, path, *sys.argv)


# 延迟重启
@daemon_thread
def restart_delay(delay: int):
    while delay > 0:
        time.sleep(1)
        delay = delay - 1
    return restart()


# 退出
def exit():
    return os._exit(0)


@daemon_thread
def exit_delay(delay: int):
    while delay > 0:
        time.sleep(1)
        delay = delay - 1
    return exit()


# 更新
def update(update_path: str):
    if os.path.exists(update_path) is True:
        bat_path = 'update.bat'
        current_path = os.path.realpath(sys.argv[0])
        with open(bat_path, 'w+') as f:
            f.write(f"@echo off\n")         # 关闭bat脚本的输出
            f.write(f"if not exist {update_path} exit \n")      # 新文件不存在,退出脚本执行
            f.write(f"choice /t 3 /d y /n >nul\n")      # 3秒后删除旧程序（3秒后程序已运行结束，不延时的话，会提示被占用，无法删除）
            f.write(f"if exist {current_path} del {current_path}\n")            # 删除当前文件
            f.write(f"copy /y {update_path} {current_path}\n")      # 拷贝新文件并重命名成旧名称
            f.write(f"start {current_path}")
        subprocess.Popen(bat_path)
        if current_path.endswith('exe') is True:
            close_process(get_current_pid())  # 进行升级，退出此程序
        else:
            sys.exit()      # 进行升级，退出此程序
    else:
        raise Exception(f"update path not exist")


# 重置控制台属性
def reset_console_property():
    if platform.system().lower() == 'windows':
        std_input_handle = -10
        enable_quick_edit_mode = 0x0040
        enable_insert_mode = 0x0010
        enable_mouse_input = 0x0020
        from ctypes import windll, c_int, byref
        handle = windll.kernel32.GetStdHandle(std_input_handle)
        if handle:
            in_mode = c_int(0)
            windll.kernel32.GetConsoleMode(c_int(handle), byref(in_mode))

            in_mode = c_int(in_mode.value & ~enable_quick_edit_mode)  # 移除快速编辑模式
            in_mode = c_int(in_mode.value & ~enable_insert_mode)  # 移除插入模式
            in_mode = c_int(in_mode.value & ~enable_mouse_input)  #
            windll.kernel32.SetConsoleMode(c_int(handle), in_mode)


# 获取MAC地址
def get_mac_address():
    mac = UUID(int=getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)]).upper()


# 进程唯一性检测
class SingleInstance:

    def __init__(self, name: str):
        self.mutexname = name
        self.mutex = None
        self.lasterror = 0
        self.create_mutex()

    def create_mutex(self):
        if platform.system().lower() == 'windows':
            from win32event import CreateMutex
            from win32api import GetLastError
            self.mutex = CreateMutex(None, False, self.mutexname)
            self.lasterror = GetLastError()

    def aleradyrunning(self) -> bool:
        return self.lasterror == 183

    def __del__(self):
        if self.mutex:
            from win32api import CloseHandle
            CloseHandle(self.mutex)
