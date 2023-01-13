import os, sys, json
import ctypes
from epkernel import epcam, BASE
from epkernel.Action import Information

def show_layer(job:str, step:str, layer:str)->None:
    try:
        step_lst= Information.get_steps(job)
        if step!='':
            if step not in step_lst:
                print('step不存在')
                return 
            else:
                BASE.show_layer(job, step, layer)
        else:
            print('step不存在')
            return 
    except Exception as e:
        print(e)
    return 

def show_matrix(job:str):
    try:
        BASE.show_matrix(job)
    except Exception as e:
        print(e)
    return  

