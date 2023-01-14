# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 18:46:11 2023

@author: Administrator
"""
import os,platform
def sudopy(*shell,password='',timeout=1800000):
    if platform.system()=='Windows':
        with open("temp.py",'a') as f:
            f.write(shell)
        os.system('sudo py temp.py')
    elif platform.system()=='Linux':
        with open("temp.py",'a') as f:
            f.write(shell)
        if not password:
            os.system('sudo python temp.py')
        else:
            os.system('sudo -S '+password+' python temp.py')
def sudo(shell,password='',timeout=1800000):
    if platform.system()=='Windows':
        os.system('sudo '+shell)
    elif platform.system()=='Linux':
        if not password:
            os.system('sudo python temp.py')
        else:
            os.system('sudo -S '+password+' python temp.py')