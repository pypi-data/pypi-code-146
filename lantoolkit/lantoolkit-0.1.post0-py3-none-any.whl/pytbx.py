# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 13:27:31 2022

@author: Administrator
"""
#%%Import and download modules
from __future__ import print_function
import os
import platform
import shutil
import subprocess
import pip
import ntplib#utc
import datetime
from rich.progress import track as tqdm #utc
import ctypes, sys



pip.main( ['install', 'cn2an', 'PyYAML>=5.3.1','-q','--use-pep517'])
import cn2an

#%%Set the variable
u = ''
f = False
pr=False
logog=''''''
logoe=''''''
#%%Gets the operating system type
pf=platform.system()
#%%Logo
logo='''114
\033[93m'''

#%%Logo Operate

#Do not run.
#Debugging~
def __debuging__setlogo__(logof):
    global logoe
    logoe=logof
if logoe=='':
    pass
else:
    logo==logoe
def _nologo():
    global logog
    logog=''''''
if not logog=='':
    pass
if logog=='':
    logo==logog
print(logo)
#%%Increase permissions
def sudo(*shell,password,timeout=1800000):
    if platform.system()=='Windows':
        def is_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
            
            if is_admin():
                shr=compile(shell)
                exec(shr)
            else:
                if sys.version_info[0] == 3:
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                    exec(shell)
                else:  # in python2.x
                    ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
    elif platform.system()=='Linux':
        with open("temp.py",'a') as f:
            f.write(shell)
        if not password:
            os.system('sudo python temp.py')
        else:
            os.system('sudo -S '+password+' python temp.py')
#%%File operations

def cpfiledata(a, b):
    try:
        file1 = open(a)
        file2 = open(b, "w")
        shutil.copyfileobj(file1, file2)
    except IOError as e:
        print("could not open file or no such file:", e)
        print("无法打开文件或无此文件：", e)


def cpflieper(src, dst):
    try:
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
            shutil.copyfile(src, dst)
            shutil.copymode(src, dst)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def cpfiletree(a, b):
    try:
        shutil.copytree(a, b)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件树或无该文件树：", e)


# noinspection PyUnboundLocalVariable
def mkarchive(tdir, ftype, rootdir):
    if tdir == "":
        tdir == "www"
    try:
        global out, f
        out = shutil.make_archive(tdir, ftype, root_dir=rootdir)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)
        f = True
    if not f:
        print(out)


# noinspection PyArgumentList,PyUnboundLocalVariable
def unarchive(tdir, ftype, rootdir):
    if tdir == "":
      tdir == "www"
    try:
        global out, f
        shutil.unpack_archive(tdir, ftype, root_dir=rootdir)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)
        f = True
    if not f:
        print(out)


def rmtree(fdir):
    try:
        shutil.rmtree(fdir)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def mvfile(src, dst):
    try:
        shutil.move(src, dst)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def rmfile(src):
    try:
        os.remove(src)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def renames(old, new):
    try:
        os.renames(old, new)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def path(file):
    # B  ct=25920000
    print("文件名：" + os.path.basename(file))
    # B  print( '最近访问时间：'+str(int(float(os.path.getatime(file))/ct))+'天前' )
    # B  print( '创建时间：'+str(float(os.path.getctime(file))/ct)+'天前' )
    # B  print( '最近修改时间：'+str(int(float(os.path.getmtime(file))/ct))+'天前' )

    if int(os.path.getsize(file)) >= 1024 * 1024 * 1024 * 1024 * 1024:
        print(
            "文件大小："
            + str(int(os.path.getsize(file)) / 1125899906842624)
            + "Pib"
        )
    elif int(os.path.getsize(file)) >= 1024 * 1024 * 1024 * 1024:
        print(
            "文件大小：" + str(int(os.path.getsize(file)) / 1099511627776) + "Tib"
        )
    elif int(os.path.getsize(file)) >= 1024 * 1024 * 1024:
        print("文件大小：" + str(int(os.path.getsize(file)) / 1073741824) + "Gib")
    elif int(os.path.getsize(file)) >= 1024 * 1024:
        print("文件大小：" + str(int(os.path.getsize(file)) / 1048576) + "Mib")
    elif int(os.path.getsize(file)) >= 1024:
        print("文件大小：" + str(int(os.path.getsize(file)) / 1024) + "Kib")
    else:
        print("文件大小：" + str(int(os.path.getsize(file))) + "B")
    print("文件路径：", os.path.abspath(file))  # 输出绝对路径
    print(os.path.normpath(file))  # 规范path字符串形式


def cpfile(a, b):
    try:
        shutil.copyfile(a, b)
    except IOError as e:
        print("could not open file or no such files:", e)
        print("无法打开文件或无该文件：", e)


def listfile(tdir):
    plat = platform.system().lower()
    if plat == "windows":
        if tdir == "":
            os.system("dir")
        else:
            os.system("cd %s" % tdir)
            os.system("dir")
    else:
        if tdir == "":
            os.system("ls")
        else:
            os.system("cd %s" % tdir)
            os.system("ls")

#%%Tools

def pshell(shell):
    os.system("powershell " + shell)

class clear:
    def __init__():
        os.system("cls")


# noinspection PyTypeChecker
def debug():
    pip.main(['config', 'debug'])


class piptools:
    def inst(pkg):
        for _ in tqdm(subprocess.call('pip install ' + pkg + ' --use-pep517', shell=True), description='install'):
            pass

    def rmpkg(pkg):
        pip.main(['uninstall', pkg])

    def downpkg(pkg):
        pip.main(['download', pkg])

    # noinspection PyTypeChecker
    class cfg:
        def set(*value):
            pip.main(['config', 'set', value])

        def edit(edor):
            if edor == '':
                pip.main(['config', 'edit'])
            else:
                pip.main(['config', '--editor=' + edor, 'edit'])

        def unset(cfg):
            pip.main(['config', 'unset', cfg])
#%%署名
class print_author_name:
    def __init__():
        lu=hex(ctypes.windll.kernel32.GetSystemDefaultUILanguage())
        if lu=='0xC04' or lu=='0x804' or lu=='0x404':
            print('作者：lan QQ:3288734411')
        if lu=='0x409':
            print('author:Lan QQ:3288734411')
        if lu=='0x40C':
            print('auteur:Lan QQ:3288734411')
        if lu=='0x419':
            print('автор:Lan QQ:3288734411')
#%%ntp_tools
def ct(url):
    c = ntplib.NTPClient()
    
    hosts = ['edu.ntp.org.cn', 'tw.ntp.org.cn', 'us.ntp.org.cn', 'cn.pool.ntp.org', 'jp.ntp.org.cn']
    # hosts=url
    for host in hosts:
    
        try:
    
            response = c.request(host)
    
            if response:
    
                break
    
        except Exception as e:
    
            print(e)
    
    current_time = response.tx_time
    
    _date, _time = str(datetime.datetime.fromtimestamp(current_time))[:22].split(' ')
    
    print("系统当前时间", str(datetime.datetime.now())[:22])
    
    print("北京标准时间", _date, _time)
    
    a, b, c = _time.split(':')
    
    c = float(c) + 0.5
    
    _time = "%s:%s:%s" % (a, b, c)
    
    eval(r"os.system('date %s && time %s' % (_date, _time))")
    print("同步后时间:", str(datetime.datetime.now())[:22])
def 对时(url):
    ct(url)
def Calibration_time(url):
    ct(url)
def cali_time(url):
    ct(url)