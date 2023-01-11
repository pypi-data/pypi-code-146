#!/usr/bin/env python3
import sys
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import fire

from .fund import fund
from .roundcorner import rc
from .app import asyncbenchmark

def download(url: str, filename: str = None):
    import codefast as cf 
    cf.net.download(url, filename)

def main():
    fire.Fire()
