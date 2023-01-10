#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.generic.dot_dict import DotDict
from poppy.core.logger import logger

__all__ = ['get_raw_data']

def get_raw_data(pipeline):
    try:
        raw_data = {
             'packet_list': [{'binary': binary}
                             for binary in pipeline.args.binary],
             'idb_version': pipeline.args.idb_version[0],
             'idb_source': pipeline.args.idb_source[0],
         }
        return raw_data
    except:
        # If not defined as input argument, then assume that it is already
        # defined as target input
        pass
