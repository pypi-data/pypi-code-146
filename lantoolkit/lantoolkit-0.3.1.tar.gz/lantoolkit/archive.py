# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 17:28:15 2023

@author: Administrator
"""
import os


def unfile(file, filedir=''):
    if not not filedir:
        fd = '-o'+filedir
        mode = 'x'
    else:
        mode = 'e'
    # start
    os.system('7z '+mode+' '+file+' '+fd)


def hashfile(*file, methods=''):
    # Supported methods: CRC32, CRC64, SHA1, SHA256, BLAKE2sp. Default method is CRC32.
    if not not methods:
        for temp in methods:
            os.system('7z h '+'-scrc'+temp+''+file)
    else:
        os.system('7z h '+file)


def delfile(file1, df, rt=''):
    if '*' in df:
        rt = r'-r'
    os.system('7z d '+file1+' '+df+' ' + rt)


def addfile(file, files):
    os.system('7z a '+file+' '+files)
