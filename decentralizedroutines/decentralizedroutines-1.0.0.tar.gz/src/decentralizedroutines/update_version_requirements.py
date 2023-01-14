import os
import boto3
from datetime import datetime
import time
import pandas as pd
import numpy as np
from pathlib import Path


from decentralizedroutines.worker_lib import send_command
import decentralizedroutines.defaults as defaults 
from SharedData.Logger import Logger
logger = Logger(__file__)


shareddata_version='shareddata==0.60.0'
decentralizedroutines_version='decentralizedroutines==0.60.0'
source_folder = os.environ['SOURCE_FOLDER']
for path in Path(source_folder).iterdir():
    if path.is_dir():        
        req_path = path/'requirements.txt'
        if (req_path).is_file():            
            print(req_path)
            with open(req_path) as f:
                s = f.read()
            
            with open(req_path, 'w') as f:                
                
                if 'shareddata==' in s:
                    lines = np.array(s.split('\n'))
                    lidx = np.array(['shareddata==' in line for line in lines])
                    lines[lidx] = shareddata_version
                    hasdecentralizedroutines = False
                    lidx = np.array(['decentralizedroutines==' in line for line in lines])
                    if lidx.any():
                        lines[lidx] = decentralizedroutines_version
                        hasdecentralizedroutines=True


                    _s = '\n'.join(lines)                    
                    f.write(_s)
                    f.flush()
            
                    send_command('git -C '+str(path)+' commit -a -m "'+shareddata_version+'"')
                    send_command('git -C '+str(path)+' push')
                    send_command(str(path/'venv\Scripts\python.exe')+' -m pip install '+shareddata_version)
                    if hasdecentralizedroutines:
                        send_command(str(path/'venv\Scripts\python.exe')+' -m pip install '+decentralizedroutines_version)

                


            