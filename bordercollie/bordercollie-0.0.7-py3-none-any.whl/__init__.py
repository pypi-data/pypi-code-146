#!/usr/bin/env python3
import os
import sys
from typing import Dict, List, Optional, Set, Tuple

import codefast as cf
import fire

from bordercollie.apps.monitor import nsqtopic, depthwatch
from bordercollie.asrsummary import calculate_summary, save_record


def pip(cmd: str, douban: bool = False):
    """Python package installer"""
    pypi = "https://pypi.douban.com/simple" if douban else "https://pypi.org/simple"
    cmd = 'python3 -m pip install {} -i {}'.format(cmd, pypi)
    os.system(cmd)


def transfer(file):
    """transfer.sh script"""
    cmd = f"curl -s -o /tmp/transfer.pl https://host.ddot.cc/transfer.pl && perl /tmp/transfer.pl {file} && rm /tmp/transfer.pl"
    try:
        resp = os.system(cmd)
    except Exception as e:
        print(e)


def sync(file):
    """sync file to gofile"""
    try:
        # still file.ddot
        cmd = f"curl -s https://file.ddot.cc/gofil|bash -s '{file}'"
        resp = os.system(cmd)
        print(resp)
    except FileNotFoundError as e:
        print(e)


def esync(file: str):
    """sync file with encryption"""
    try:
        cmd = f"curl -s https://host.ddot.cc/gofile|bash -s '{file}'"
        resp = os.system(cmd)
        print(resp)
    except FileNotFoundError as e:
        print(e)


def oss(file: str):
    """sync file to oss"""
    try:
        cmd = f"curl -s https://host.ddot.cc/oss|bash -s {file}"
        resp = os.system(cmd)
        print(resp)
    except FileNotFoundError as e:
        print(e)


def grep(kw: str):
    """search from log"""
    print(cf.shell('grep {} /log/serving/serving.log'.format(kw)))


def main():
    fire.Fire()
