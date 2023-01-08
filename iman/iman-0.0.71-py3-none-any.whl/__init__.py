import matplotlib.pyplot as plt
import time
from glob import glob as gf
import os
import numpy as np
from joblib import load,dump

def help():
    from iman import web
    x=web.dl(r'https://pypi.org/project/iman/')
    idx = x.index('class="project-description"')
    idy = x.index('</div>' , idx+1)
    y= (x[idx+29:idy].strip().replace('<span class="docutils literal">','<').replace('</span>','>').replace('</section>','').replace('<h2>','').replace('</h2>','').replace('<p>','').replace('</p>','').replace('<section id=from-iman-import>',''))
    

    while(True):
       try:
        idx=0
        idx = y.index('<section',idx+1)

        idy = y.index('>' , idx+1)

        y = y.replace(y[idx:idy+1] , '')
       except:
         break       
    print(y)
   
def clear():
    if os.name == 'nt':
        _ = os.system('cls')  
    else:
        _ = os.system('clear')
        
def now():
   return time.time()
     
def F(float_number , float_number_count = 2):
   _str=("{:." + str(float_number_count) +"f}").format(float_number)
   return(_str) 

def D(int_number , int_number_count = 3):
   _str=("{:0>" + str(int_number_count) +"d}").format(int(int_number))
   return(_str) 
   
def Write(_str,Filename):
   with open(Filename , 'w' , encoding='utf-8') as fid:
              fid.write(_str)    

def Write_List(MyList,Filename):
   with open(Filename , 'w' , encoding='utf-8') as fid:
        for x in MyList:
              fid.write(str(x) + '\n')    

def Write_Dic(MyDic,Filename):
   with open(Filename , 'w' , encoding='utf-8') as fid:
        for x,y in MyDic.items():
              fid.write(str(x) + '\t' + str(y) + '\n')                 
              
def Read(Filename):
    with open(Filename , 'r' , encoding='utf-8') as fid:
         return(fid.read())

def Read_Lines(Filename):
    with open(Filename , 'r' , encoding='utf-8') as fid:
         return([x.strip() for x in fid if (x.strip()!="")])    

def gfa(directory , ext="*.*"):
 fols = gf(directory)
 a=[]
 for _fol in fols: 
   [a.append(x) for x in gf(os.path.join(_fol , ext))]
   for root, dirs, files in os.walk(_fol):
      for dirname in dirs:
         _dir =os.path.join(root, dirname)         
         [a.append(x) for x in gf(os.path.join(_dir , ext))]           
 return a         

def ReadE(Filename):
    import pandas as pd
    pp = pd.read_excel(Filename , engine='openpyxl')
    return pp
    
def PB(filename):
   return os.path.basename(filename)    
         
def PD(filename):
   return os.path.dirname(filename)  
   
def PM(folname):
   return os.makedirs(folname , exist_ok=True)
       
def PN(filename):
   return os.path.basename(os.path.splitext(filename)[0])  

def PE(filename):
   return os.path.splitext(filename)[1]   

def PX(filename):
   return os.path.exists(filename)    
   
def PJ(*_segments):
   x=""
   for p in _segments:
      x = os.path.join(x,p)
   return x   
   
def PS(filename):
   return os.path.getsize(filename)  
   
def RI(start_int , end_int , count=1):
   return np.random.randint(low=int(start_int), high=int(end_int), size=(count,))
   
def RF(start_float , end_float , count=1):
  return np.random.uniform(start_float, end_float , count)
  
def RS(Arr):
  np.random.shuffle(Arr)
  return Arr
  
def RC(Arr , _size=1):
   return np.random.choice(Arr , _size)


def LJ(job_file_name):
   return load(job_file_name)
   
def SJ(value , job_file_name):
   dump(value , job_file_name)   
   
def LN(np_file_name):
   return np.load(np_file_name) 
   
def SN(arr , np_file_name):
   return np.save(np_file_name , arr)   
   
def cmd(command , redirect=True):
  if (redirect):
   return os.popen(command).read()   
  else:
    os.system(command)  
    
    
def onehot(data, nb_classes):
    """Convert an iterable of indices to one-hot encoded labels."""
    targets = np.array(data).reshape(-1)
    return np.eye(nb_classes)[targets]
    
    
def exe(fname):
    cmd('pyinstaller --onefile ' + fname , False)    