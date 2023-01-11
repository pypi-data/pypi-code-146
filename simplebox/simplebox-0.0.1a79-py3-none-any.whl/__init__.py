#!/usr/bin/env python
# -*- coding:utf-8 -*-
__version__ = "0.0.1.alpha79"
banner = f"""
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |    _______   | || |     _____    | || | ____    ____ | || |   ______     | || |   _____      | || |  _________   | || |   ______     | || |     ____     | || |  ____  ____  | |
| |   /  ___  |  | || |    |_   _|   | || ||_   \  /   _|| || |  |_   __ \   | || |  |_   _|     | || | |_   ___  |  | || |  |_   _ \    | || |   .'    `.   | || | |_  _||_  _| | |
| |  |  (__ \_|  | || |      | |     | || |  |   \/   |  | || |    | |__) |  | || |    | |       | || |   | |_  \_|  | || |    | |_) |   | || |  /  .--.  \  | || |   \ \  / /   | |
| |   '.___`-.   | || |      | |     | || |  | |\  /| |  | || |    |  ___/   | || |    | |   _   | || |   |  _|  _   | || |    |  __'.   | || |  | |    | |  | || |    > `' <    | |
| |  |`\____) |  | || |     _| |_    | || | _| |_\/_| |_ | || |   _| |_      | || |   _| |__/ |  | || |  _| |___/ |  | || |   _| |__) |  | || |  \  `--'  /  | || |  _/ /'`\ \_  | |
| |  |_______.'  | || |    |_____|   | || ||_____||_____|| || |  |_____|     | || |  |________|  | || | |_________|  | || |  |_______/   | || |   `.____.'   | || | |____||____| | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 

Version::   {__version__}
\n"""

import sys
from threading import local

_local_var = local()

from ._internal import _argparser
from ._internal._argparser import _options_hook_func


def __print_help():
    msg = """
simplebox cli:
    set simplebox inbuilt configure.
    the option is to add the configuration of the setting parameter, the value is the configuration parameter, 
    the properties and values of each configuration, passed in in the form of key:value.
    If the key contains an underscore, you can also use a hyphen in the command, ex k-ey:value = k_ey:value
    multiple values use semicolons ';'Spaced.
    ex: python xxx.py --options=key1=value2;key2=value2
    --sb-help  show simplebox cli help information, then exit.so do not use with other commands.
    
    --sb-log   LogConfig set by cli, 
               ex: python xxx.py --sb-log=name:xxx_name;level:INFO
               See the LogConfig property for details
    --sb-rest  LogConfig set by cli, 
               ex: python xxx.py --sb-rest=only_body:True
               See the RestConfig property for details
    """
    print(msg)
    exit(0)


def __args_handler():
    args = sys.argv[1:]
    if "--sb-help" in args:
        __print_help()
    if not args:
        return
    for opt in _options_hook_func:
        for arg in args:
            identifier = f"{opt}=".replace("_", "-")
            if arg.startswith(identifier):
                getattr(_argparser, opt)(arg.split(identifier))
                sys.argv.remove(arg)


__all__ = []

__args_handler()
