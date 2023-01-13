# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 08:03:52 2023

@author: user
"""

import time
import pickle as pkl
import os
from datetime import datetime
import numpy as np

this_dir, this_filename = os.path.split(__file__)  # Get path of data.pkl

data = pkl.load( open(  os.path.join(this_dir,"data.pkl"),"rb") )
time_process = np.array(data["time_process"]/5,dtype=int)
time_wait = np.array(data["wait"]/5,dtype=int)

paths = data["paths"]
paths[0] = paths[0]*0.2 +20
paths[1] = paths[1] *.1+.5
paths[2] = paths[2] *.1
paths[3] = paths[3] *.1


timestamp = 1673614800-5*3600*24

post = [0,0,0,0]

pos_process = 0
pos_wait = 0

count = 0
count_global = 0

inprocess = True

try:
    os.mkdir("donnees")
except:
    0

directories = [x[0] for x in os.walk("donnees")]

noserie = ["KOP_5943","KOP_1322","KOP_9974","KOP_3330"]



while(timestamp < time.time()):
    
    
    if(inprocess):
        
        # Process
        datetime_object = datetime.fromtimestamp(timestamp)
        timestr = str(datetime_object)
        
        # 4 temperatures
        t0 = paths[0][post[0]]
        t1 = t0 + paths[1][post[1]]
        t2 = t0 + paths[2][post[2]]
        t3 = t0 + paths[3][post[3]]
        at = [t0,t1,t2,t3]
        
        # 
        folder = "donnees\\" + str(count_global)
        
        if (folder not in directories): # If data does not exist, create folder
            
            try:
                # Make folder
                os.mkdir(folder)
            
                for i in range(4):
                    file = open(folder+"\\"+str(i)+".txt","w")
                    file.write(noserie[i]+"\n"+str(datetime_object)+\
                               "\n{:.2f}".format(at[i]))
                    file.close()
            
            except:
                0
        
        
        # For each path
        for i in range(4):
            post[i] += 1
            if(post[i] >= len(paths[i])):
                post[i] = 0
        
        count_global += 1
        
        count += 1
        if(count >= time_process[pos_process]):
            inprocess=False
            count = 0
            pos_process += 1
            if(pos_process >= len(time_process)):
                pos_process = 0
    
    
    else:
        
        count += 1
        if(count >= time_wait[pos_wait]):
            inprocess=True
            count = 0
            pos_wait += 1
            if(pos_wait >= len(time_wait)):
                pos_wait = 0
    
    timestamp = timestamp + 60*5



def nb_sous_dossiers():
    directories = [x[0] for x in os.walk("donnees")][1:]
    return( len(directories)-1 )