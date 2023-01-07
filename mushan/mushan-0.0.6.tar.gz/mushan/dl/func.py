'''
Date: 2022-08-11 14:40:52
LastEditors: mushan wwd137669793@gmail.com
LastEditTime: 2022-12-30 21:47:56
FilePath: /mushan/mushan/dl/func.py
'''
import torch
import os
from varname import argname


def get_device():
    
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def disable_cuda(args=None):
    
    
    os.environ["CUDA_VISIBLE_DEVICES"]="-1"
    if torch.cuda.is_available():
        print("Disable CUDA fail!")
    else:
        print("Disable CUDA success!")
        
        
def set_cuda(gpus=None):
    """_summary_

    Args:
        gpus (int, list): _description_
    """
    
    if gpus == None or gpus == -1:
        disable_cuda()
    else:
        _gpus = []
        if isinstance(gpus, list):
            for g in gpus:
                _gpus.append(str(g))
        elif isinstance(gpus, int):
            _gpus.append(str(gpus))
        else:
            print("Unknow input types!")
            return
            
        os.environ["CUDA_VISIBLE_DEVICES"]=",".join(_gpus)
        
        print("Current CUDA Devices: {}".format(torch.cuda.current_device()))
        print("Total Visible CUDA Device Count: {}".format(torch.cuda.device_count()))
    
    
def printShape(*args):
    for i in range(len(args)):
        assert isinstance(args[i], torch.Tensor)
        print(f"{argname(f'args[{i}]')}.shape: {str(list(args[i].shape))}, {str(args[i].dtype)[6:]}")