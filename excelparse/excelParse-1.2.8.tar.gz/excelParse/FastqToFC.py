#!/usr/bin/env python 

'''
:Name:	FastqToFC.py
:Author:	Zheng Yabiao
:Usage:	Extract the flowcell, lane and index information from fastq.
:Data:	2017.5.23
'''

import os

def flowcell_lane(file):
    """Get flowcell, lane and index from fastq
    
    :Args:
        file (file): input fastq file

    :Returns:
        * fc (str): flowcell_Lane, like KACAE34_L8
        * index (str): index sequence
    """
    if file.endswith("gz"):
        heads = os.popen('zcat %s|head -n 1' %(file)).readline().strip().split(":")
        length = len(os.popen('zcat %s|head -n 2|tail -n 1' %(file)).readline().strip())
    else:
        heads = os.popen('cat %s|head -n 1' %(file)).readline().strip().split(":")
        length = len(os.popen('cat %s|head -n 2|tail -n 1' %(file)).readline().strip())
    if len(heads) > 1:
        fc = heads[2] + "_L" + heads[3]
        index = heads[9]
    else:
        fc = heads[0][1:17]
        index = "AAAA"
    return fc, index, length

def diff_r1_r2(r1, r2):
    """Determine whether two fastq file have the same flowcell, lane and index
    
    :Args:
        * r1 (file): one input fastq file
        * r2 (file): two input fastq file

    :Returns:
        * `boolean`: whether the two files are same
    """
    f1, i1, l1 = flowcell_lane(r1)
    f2, i2, l2 = flowcell_lane(r2)
    if "_".join([f1, i1]) == "_".join([f2, i2]):
        return True
    else:
        return False
    
