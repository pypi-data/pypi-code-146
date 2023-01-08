print('-'*70)
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
import pkg_resources
import keras
from git.repo.base import Repo
import os

print('-'*70)
print('Depended packages imported successfully.')

initial_info = '''
                  -------------------------------------------------------
                  #--> import pkg:    import pycpep as pc
                  #--> load locally:  pc.pkg.load()
                  #--> get info:      pc.pkg.info()
                  #--> get help:      pc.pkg.help()
                  #--> prediction:    pc.pkg.prediction()
                  #--> use MWE.py to check minimum working example.

                  more details: https://github.com/nirmalparmarphd/PyCpep
                  -------------------------------------------------------
                  
                  '''
print(initial_info)

class pkg():
  def __init__(self):
    print('-'*70)    
    print('           PyCpep Loaded. You are Awesome!           ')
    print(initial_info)

  def load():
    print('-'*70)    
    url_pkg = 'https://github.com/nirmalparmarphd/PyCpep'
    cwd = os.getcwd()
    directory = 'dir_pycpep'
    path = os.path.join(cwd, directory)
    isExist = os.path.exists(path)
    if not isExist:    
      os.mkdir(path)
      print("Directory '% s' created" % directory)
      Repo.clone_from(url_pkg, 'dir_pycpep')
    else:
      print("Directory '% s' already exist!" % directory)
      exit()   
    path_rm_setup = os.path.join(path, 'setup.py')
    os.remove(path_rm_setup)
    path_rm_cfg = os.path.join(path, 'PyCpep/setup.cfg')
    os.remove(path_rm_cfg)
    path_rm_init = os.path.join(path, 'PyCpep/__init__.py')
    os.remove(path_rm_init)
    print('Downloaded PyCpep in current directory.')
    path_chwd = os.path.join(path, 'PyCpep')
    os.chdir(path_chwd)
    exit()

  def prediction(Ref,Sam):    
    if 0 < Ref <= 1 and 0 < Sam <= 1:
      # loading scaler
      with open('pycpep/mdl/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
      # loading ann model
      model = keras.models.load_model('pycpep/mdl/model.h5')
      # calculating vol-rel
      vol_rel = (Ref*Ref)/Sam
      data = [Ref, Sam, vol_rel]
      data = pd.DataFrame([data])
      # scaling data
      data_ = scaler.transform(data)
      # prediction from ann model
      pred = model.predict(data_)
      pred_ = np.round(((pred*100)-100).astype(np.float64),2)
      
      print('-'*70)
      print('Reference amount : ', Ref)
      print('Sample amount : ', Sam)
      
      if abs(pred_) <= 1.5:
        print('Heat capacity measurement deviation prediction (%): ', pred_)
        print('''COMMENT(s):
              You are Awesome!! The predicted deviation is below 1%!
              The combination of the sample and the reference amount is appropriate.
              NOTE:
              Consider 0.8~ml as standard amount to avoid any deviation in the measurement.''')
        print('-'*70)
      else:
        print('Heat capacity measurement deviation prediction (%): ', pred_)
        print('''COMMENT(s): 
              The combination of the sample and the reference amount is NOT appropriate.
              NOTE:
              Consider 0.8~ml as standard amount to avoid any deviation in the measurement.
              ''')
      print('-'*70)
    else:
      print(''' ERROR! --> Entered value of of the reference or/and the standard amount is NOT appropriate.

              # NOTE: enter the sample and reference material amount as mentioned below
                ## Full cell:               1.0     [0.80 to 1.00 ml]
                ## Two Third full cell:     0.66    [0.40 to 0.80 ml]
                ## One half full cell:      0.5     [0.26 to 0.40 ml]
                ## One third full cell:     0.33    [0.10 to 0.26 ml]
            ''')
      print('-'*70)

  def info():
      information ='''
        * This is a Deep learning (DL) ANN model to predict a deviation due to an inappropriate amount combination of the sample and a reference material in a batch cell of Tian-Calvet micro-DSC.

        * This ANN model predicts the possible deviation that may arise in the heat capacity measurement experiment due to in appropriate combination of the sample and the reference material amount!

        --> ANN Model accuracy on the test data is 99.82 [%] <--
        
        * more details: https://github.com/nirmalparmarphd/PyCpep
        
        '''
      print(information)
      print('-'*70)

  def help():
      help_info = '''
        # prediction of error/deviation in the heat capacity measurement
        # use: prediction = dsc_error_model(Reference amount, Sample amount)
        # NOTE: enter the sample and reference material amount as mentioned below
                ## Full cell:               1.0     [0.80 to 1.00 ml]
                ## Two Third full cell:     0.66    [0.40 to 0.80 ml]
                ## One half full cell:      0.5     [0.26 to 0.40 ml]
                ## One third full cell:     0.33    [0.10 to 0.26 ml]

        ### MINIMUM WORKING EXAMPLE ###

        # import module
        >>> import pycpep as pc

        # pkg check
        >>> pc.pkg()

        # download pkg locally with dependencies and minimum working example (MWE)
        >>> pc.pkg.load()

        # change to 'dir_pycpep' to access MWE.py

         * more details: https://github.com/nirmalparmarphd/PyCpep

            '''  
      print(help_info)
      print('-'*70)

