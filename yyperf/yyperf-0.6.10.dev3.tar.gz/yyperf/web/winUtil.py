#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import sys

if sys.platform=="win32":
    import win32api
    import win32process
    import win32event
    import wmi
    w = wmi.WMI()
import signal
import psutil
import logging
from pynvml import *
import platform

def getComputerInfo():
    info = ""
    info += '操作系统:' + platform.platform() + ' ' + platform.architecture()[0]

    # for BIOSs in w.Win32_ComputerSystem():
    #     list.append('电脑名称: %s' %BIOSs.Caption)
    #     list.append('使 用 者: %s' %BIOSs.UserName)
    index = 0
    for processor in w.Win32_Processor():
        info += f' CPU[{index}]型号:{processor.Name.strip()} 核数：{processor.NumberOfCores}'
        index = index + 1

    index = 0
    for memModule in w.Win32_PhysicalMemory():
        totalMemSize = int(memModule.Capacity)
        # dict['内存厂商']= memModule.Manufacturer
        info +=' 内存[{}]型号'.format(index) + memModule.PartNumber
        info +=' 内存[{}]大小'.format(index) + '%.2fGB' % (totalMemSize / 1024 ** 3)
        index = index + 1
    index = 0
    for xk in w.Win32_VideoController():
        info +=' 显卡[{}]型号'.format(index) + xk.name
        index = index + 1

    return info

if sys.platform=="win32":
    pcinfo = getComputerInfo()

def get_pc_info():
    info = ""
    try:
        name = platform.node()
        cpu = w.Win32_Processor()[0].Name
        sysVer = platform.platform()
        #info = "%s|%s|%s"%(name,sysVer,cpu)
        info = "%s|%s|%s" % (name,cpu, sysVer)
    except Exception as e:
        logging.error(str(e))
    return info

def get_app_list(dev):
    appinfo_list = []
    all_pids = psutil.pids()
    for pid in all_pids:
        try:
            p = psutil.Process(pid)
            if p.name() not in appinfo_list:
                appinfo_list.append(f"{p.name()}")
        except:
            print('进程无法访问 pid=', pid)
    appinfo_list.sort()
    return appinfo_list

def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=True,
                   timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callabck function which is
    called as soon as a child terminates.
    """
    try:
        if psutil.pid_exists(pid) is False:
            return
        if pid == os.getpid():
            raise RuntimeError("I refuse to kill myself")
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        if include_parent:
            children.append(parent)
        for p in children:
            try:
                p.send_signal(sig)
            except:
                pass
        gone, alive = psutil.wait_procs(children, timeout=timeout,
                                        callback=on_terminate)
        return (gone, alive)
    except Exception as e:
        logging.error(str(e))
        return

def win_start_proc_wait(path, cmd, waitTime, workdir=None):
    '''
    启动进程，等待结束
    :param path: 程序exe所在的路径，如：'C:\\Program Files\\DAUM\\PotPlayer\\PotPlayerMini64.exe'
    :param cmd: 程序执行命名行，如：'C:\\Users\\duowan\\Desktop\\videos\\00010.m2ts /autoplay'
    :param waitTime: 等待时间，0-无限等待，超过等待时间，强制停止
    :param workdir: 工作目录，像obs要设置工作目录
    :return:
    '''
    prochandle = None
    current = 0
    if waitTime == 0:
        waitTime = win32event.INFINITE
    try:
        # 函数返回进程句柄、线程句柄、进程ID，以及线程ID
        handle = win32process.CreateProcess(
            path, cmd, None, None, 0, win32process.CREATE_NO_WINDOW, None, workdir, win32process.STARTUPINFO())
        prochandle = handle[0]
        threadhandle = handle[1]
        procid = handle[2]
        threadid = handle[3]
        running = True
        current = time.time()
        logging.info('启动成功，返回信息：进程句柄：%s 线程句柄：%s 进程ID：%d 线程ID：%d' % (str(prochandle), str(threadhandle), procid, threadid))
    except Exception as e:
        logging.error('启动失败：' + str(e))
        handle = None
        running = False
    while running:
        result = win32event.WaitForSingleObject(prochandle, waitTime)
        if result == win32event.WAIT_OBJECT_0:
            running = False
        if time.time() - current > waitTime:
            logging.info('超过等待时间，强制终止')
            win32process.TerminateProcess(prochandle, 0)
            running = False
            break
    if not running:
        logging.info('%s 进程终止' % path)


def win_start_proc_nowait(path, param, workdir=None):
    win32api.ShellExecute(0, 'open', path, param, workdir, 1)
    time.sleep(3)


def win_check_proc_running(procname):
    '''
    windows 检测进程名为procname是否运行中
    :param procname: 不支持正则表达式
    '''
    cmd = 'tasklist /FI "IMAGENAME eq %s"' % procname
    result = os.popen(cmd).read().count(procname)
    if result > 0:
        return True
    else:
        return False


def win_stop_proc_by_name(procname):
    '''
    windows 杀掉进程
    :param procname: 可以是正则表达式
    '''
    cmd = 'taskkill /F /IM %s' % procname
    # out = os.system(cmd)  #这个方法不能捕获输出，用下面的
    out = os.popen(cmd).read()
    logging.info(out)
    if 'PID' in out:
        return True
    else:
        return False


def win_stop_proc_by_handle(handle):
    win32process.TerminateProcess(handle, 0)

def screen_shot(device,file_name):
    from PIL import ImageGrab
    grab = ImageGrab.grab()
    grab.save(file_name)

if __name__ == "__main__":
    exe = 'C:\\Program Files (x86)\\obs-studio\\bin\\64bit\\obs64.exe'
    cu = 'C:\\Program Files (x86)\\obs-studio\\bin\\64bit'
    #win32process.CreateProcess(
     #   exe, None, None, None, 0, win32process.CREATE_NO_WINDOW, None, cu, win32process.STARTUPINFO())
    # win32api.ShellExecute(0, 'open', exe, None, cu, 1)
    print(get_pc_info())
