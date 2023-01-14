#!/usr/bin/env python
# coding: utf-8

# # Regularization
# 
# - `dropout_unit` : Obtain filtered A[l] by shutting-off the nodes with binomial(N = n^[l] * m, p = 1-keep_prob) 
# - `get_L2_weight_penalty` : Obtain L2_weight_penalty by input lambd, param, and m

# In[ ]:


# %% External module
import numpy as np


# In[ ]:


def dropout_unit(A,keep_prob):
    """Implement dropout to activation node output
    
    Arguments
    -------------------
    A --- Activation node output
    keep_prob --- The proportion of non-shut-off units in the layer
    
    Returns
    -------------------
    A --- Filtered Activation node output by Dropout filter
    """
    
    D = np.random.rand(A.shape[0],A.shape[1]) < keep_prob   # Dropout filter
    A = np.multiply(A,D)
    
    A /= keep_prob #Inverted dropout
    
    return A


# In[ ]:


def get_L2_weight_penalty(lambd : float, param : list, m : int) -> float:
    """
    
    Arguments:
    -----------------------------------------
    lambd --- float
            regularization term 
    param --- list
            parameter W^[1], B^[1],... W^[L], B^[L]
    
    m --- int
           number of observation
        
    Return :
    -----------------------------------------
    L2_weight_penalty --- float
    
    """
    L:int = len(param) // 2
    L2_weight_penalty = 0
    
    for l in range(1,L+1): #summation of square of Frobenius weight norm for every layer
        W = param['W'+str(l)]
        L2_weight_penalty += np.sum(np.square(W))     
    
    L2_weight_penalty *= (lambd / (2*m) ) 
    
    return L2_weight_penalty


# In[ ]:


def get_L2_weight_decay(lambd : float, param : list, m : int) -> np.array:
    """
    Return L2 weight decay of a single layer
    
    Arguments:
    -----------------------------------------
    lambd --- float
            regularization term 
    param --- list
            parameter W^[1], B^[1],... W^[L], B^[L]
    
    m --- int
           number of observation
        
    Return :
    -----------------------------------------
    L2_weight_decay --- np.array
            How much parameter was decays
    
    """    
    pass
    
    

