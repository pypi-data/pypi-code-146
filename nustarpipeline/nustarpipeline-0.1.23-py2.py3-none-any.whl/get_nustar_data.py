#!/usr/bin/env python
#

import sys,os

help="get_data.py OBSID\n"

if len(sys.argv) <2:
    
    print(help)
    sys.exit(1)

obsid=sys.argv[1]

from nustarpipeline import process

process.get_data(obsid)

