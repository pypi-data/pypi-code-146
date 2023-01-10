#!/usr/bin/env python3
'''

'''
from daskcheck.version import __version__
from fire import Fire
from daskcheck import config

import time
import os

import datetime as dt

from dask.distributed import Client, progress, as_completed
import platform
import time

import json
import datetime as dt

import glob

import sys

# ---------------------------------
import pandas as pd
import numpy as np

def get_dask_server():
    with open( os.path.expanduser("~/.dask_server") ) as f:
        return f.readlines()[0].strip()


#-----------------------------------

def get_cpu_info( order, param):
    """
    An example function to send to dask cluster cores
    """
    import subprocess as sp
    import platform
    import re
    import psutil

    start_time = time.perf_counter()  # Start the clock <-------------
    # -----start to collect info
    name, platf,   =  platform.node(), platform.machine()
    coremax = 0
    command = "cat /proc/cpuinfo"
    all_info = sp.check_output(command, shell=True).decode("utf8").strip()
    for line in all_info.split("\n"):
        if "model name" in line:
            proc = re.sub( ".*model name.*:", "", line,1)
            proc = proc.replace("     "," ")
            proc = proc.replace("    "," ")
            proc = proc.replace("   "," ")
            proc = proc.replace("  "," ")
        if "Model" in line:
            proc = re.sub( ".*Model.*:", "", line,1)
        if "processor" in line:
            coremax+=1
    corereal = psutil.cpu_count(logical = False)
    if corereal is None:  corereal = coremax
    while len(name)<10:name=name+" "  # One lenght for names
    time.sleep(3)

    spent_time = time.perf_counter() - start_time # read the clock <--------
    # RETURNS LIST composed of 2 elements: order number + LIST
    return order, [name,  f"{spent_time:.1f} s", f"{platf} {proc}"]
    return order, [name,  f"{spent_time:.1f} s", f"{platf} {proc}",f"pandas=={pd.__version__}",f"numpy=={np.__version__}"]



#-----------------------------------
def pislow(size):
    """
    calculate PI
    """
    pi = 0
    accuracy = size
    for i in range(0, accuracy):
        pi += ((4.0 * (-1)**i) / (2*i + 1))
    return pi





#************************************************************************* KING OF FUNCTIONS
#************************************************************************* KING OF FUNCTIONS
#************************************************************************* KING OF FUNCTIONS
def submit( xcore_function,   parameters):
    """
    general client submitter...  1/ function_to_calculate 2/LIST of parameters
    ... every parameter goes to one node ...
    RETURNS LIST with TWO elements:   [0]/ ORDER  [1]/  LIST of whatever results
    """
    nnodes = len(parameters)

    dask_server = get_dask_server()
    print( "i... dask server = /{dask_server}/")
    client = Client(f"{dask_server}:8786")
    print("i... client:",client)
    print("______________________________________")


    futures = []
    for i in range(nnodes):
        res = client.submit( xcore_function, i , parameters[i] )
        futures.append( res )

    print("*"*60)
    print(f"             {len(parameters)} jobs WERE SUBMITTED     ")
    print("*"*60)

    #print(futures)
    # #li = client.gather(futures)

    my_results = {} # DICT - the key is the order of submission
    for future in as_completed(futures):
        n = future.result()
        my_results[n[0]] = n[1] # ORDER IS 1st and the DICT KEY TOO
        print(f"i... {n[0]:5d}. has ended, totaly {len(my_results)} or {len(parameters)}        ", end="\r")

    #for k in  sorted(my_results.keys()):
    #    print(f"{k:5d}", my_results[k] )

    print("____________________________ Dataframe with results")
    df = pd.DataFrame( my_results ).transpose() # nodes are on rows
    print( df.sort_values( by=[0], ascending = True)  ) # sort by name ==1st member of the list)
    # SORT BY library version.... e.g
    #print( df.sort_values(0).groupby(4, group_keys=True).apply(lambda x:x)  )

    # Write LOG file.
    now = dt.datetime.now()
    stamp = now.strftime("%Y%m%d_%H%M%S")
    with open(f"dask_results_log_{stamp}.json", "w") as fp:
        json.dump( my_results , fp, sort_keys=True, indent='\t', separators=(',', ': '))
    return


def prepare_params(parlist):
    """
    commandline given parameter list TO LIST/STR
    """
    # ------  PREPARE PARAMETER LIST

    print(f"i...  parameter list= {parlist} of type {type(parlist)}")
    if type(parlist)==tuple:
        parameters = list(parlist)
    elif type(parlist) == str:
        if parlist.find("..")>0:
            rng = parlist.split("..")
            parameters = list( range( int(rng[0]),int(rng[1]) ) )
        else:
            parameters = parlist
    else:
        parameters = parlist
    print(f"i...  parameter list= {parameters} of type {type(parameters)}")
    return parameters


#------------------------------------------------------------------------ MAIN ***************
def main( importmodule, parlist):
    """
    give the directory with the module to import inside (same name as directory.py)
    1/ Create Param_LIST 2/ call "sumbit"
    Allowed parlist == run11  r1,r2,r3,r4,r5   1..5
    """

    # ------  PREPARE PARAMETER LIST

    print(f"i...  parameter list= {parlist} of type {type(parlist)}")
    if type(parlist)==tuple:
        parameters = list(parlist)
    elif type(parlist) == str:
        if parlist.find("..")>0:
            rng = parlist.split("..")
            parameters = list( range( int(rng[0]),int(rng[1]) ) )
        else:
            parameters = parlist
    else:
        parameters = parlist
    print(f"i...  parameter list= {parameters} of type {type(parameters)}")


    # -------- MODULE LOAD

    if not os.path.exists( importmodule ):
        print("X... module for import doesnt exist")
        sys.exit(1)
    import importlib
    xcorefunc = importlib.import_module(f'{importmodule}.{importmodule}')

    # --------- RUN IN DASK OR LOCALY

    if type(parameters)==list:
        print("i... viable for DASK ....")
        submit( xcorefunc.main  ,  parameters )
    else:

        my_results = xcorefunc.main( 1 , parameters )
        # Write LOG file.
        now = dt.datetime.now()
        stamp = now.strftime("%Y%m%d_%H%M%S")
        with open(f"dask_results_log_{stamp}.json", "w") as fp:
            json.dump( my_results , fp, sort_keys=True, indent='\t', separators=(',', ': '))
    return



def test():
    NTASKS = 40
    submit(  get_cpu_info, [ str(x) for x in range(1,NTASKS) ] )

def local():
    print(  get_cpu_info( 1, " ")  )

#==============================================================================================
if __name__=="__main__":
    print("i... in the __main__ of unitname of daskcheck")
    Fire({"dask":main,
          "test":test,
          "local":local
    } )
