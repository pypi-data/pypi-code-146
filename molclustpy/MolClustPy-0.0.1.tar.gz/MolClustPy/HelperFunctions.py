# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 14:41:07 2022

@author: Ani Chattaraj
"""
import sys 
from time import time 

def ProgressBar(jobName, progress, length=40):

    '''
    Parameters
    ----------
    jobName : string
        Name of the job given by user.

    progress : float
        progress of the job to be printed as percentage.

    length : interger
        prints the length of the progressbar. The default is 40.

    Returns
    -------
    None.
    '''
    completionIndex = round(progress*length)
    msg = "\r{} : [{}] {}%".format(jobName, "*"*completionIndex + "-"*(length-completionIndex), round(progress*100))
    if progress >= 1: msg += "\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()



def displayExecutionTime(func):
    """
    This decorator (function) will calculate the time needed to execute a task
    """
    def wrapper(*args, **kwrgs):
        t1 = time()
        func(*args, **kwrgs)
        t2 = time()
        delta = t2 - t1
        if delta < 60:
            print("Execution time : {:.4f} seconds".format(delta))
        else:
            t_min, t_sec = int(delta/60), round(delta%60)
            print(f"Execution time : {t_min} mins {t_sec} secs")

    return wrapper