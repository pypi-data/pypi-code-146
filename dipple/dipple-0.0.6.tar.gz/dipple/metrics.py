#!/usr/bin/env python
# coding: utf-8

# # Metrics
# 
# - `accuracy_score`

# In[ ]:


#import import_ipynb


# In[3]:


# %% External module
import numpy as np


# In[17]:


def accuracy_score(Y,Y_pred):
    """Evaluate accuracy for the classes
    
    Arguments
    -------------------
    Y --- np.array
          with dimension : (1 or 2)
            
    Y_pred --- np.array
               with dimension : 1
    
    Returns
    ------------------
    accuracy --- float
    """
    
    if Y.T.shape == Y_pred.shape:
        Y = Y.T
        
    if Y.ndim == 2:
        Y = np.squeeze(Y) # now Y ndim = 1
    elif Y_pred.ndim == 2:
        Y_pred = np.squeeze(Y_pred) # in case, the user swap the position of input between y_pred and y
    
    
    arr = Y == Y_pred
    arr_ = np.count_nonzero(arr) / len(arr)
    
    return arr_

