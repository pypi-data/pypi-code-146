# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 16:52:17 2023

@author: Administrator
"""
__all__ = ['archive.py', 'file.py', 'sudo.py', 'pip.py','ntp.py','piptools.py']
import platform
import os
import sudo
import archive
import piptools
# logog=''''''
# logoe=''''''


def __runfst__():
    __fc = 'Python Version:'+' '+platform.python_version()
    __et = 'PKG Version:'+'0.3.2'
    print(__et)
    print(__fc)


# %%Gets the operating system type
if __name__ == '__main__':
    # %%Logo

    logo = '''
    ╔════╦═══╦═══╦╗  ╔╗╔═╦══╦════╗
    ║╔╗╔╗║╔═╗║╔═╗║║  ║║║╔╩╣╠╣╔╗╔╗║
    ╚╝║║╚╣║ ║║║ ║║║  ║╚╝║ ║║╚╝║║╚╝
      ║║ ║║ ║║║ ║║║ ╔╣╔╗║ ║║  ║║
      ║║ ║╚═╝║╚═╝║╚═╝║║║╚╦╣╠╗ ║║
      ╚╝ ╚═══╩═══╩═══╩╝╚═╩══╝ ╚╝'''

    # %%Logo Operate

    # Do not run.
    # Debugging~
    # def __debuging__setlogo__(logof):
    #     global logoe
    #     logoe=logof
    # if logoe=='':
    #     pass
    # else:
    #     logo==logoe
    # def _nologo():
    #     global logog
    #     logog=''''''
    # if not logog=='':
    #     pass
    # if logog=='':
    #     logo==logog
    print(logo)
    __runfst__()


def pshell(shell):
    os.system("powershell " + shell)


class clear:
    def __init__(self):
        os.system("cls")


sudo = sudo.sudo
unarchive = archive.unfile
make_archive = archive.addfile
pip_install = piptools.install
pip_uninstall = piptools.uninstall
pip_reinstall = piptools.reinstall
