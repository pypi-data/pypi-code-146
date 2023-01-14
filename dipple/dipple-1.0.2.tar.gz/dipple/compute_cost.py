#!/usr/bin/env python
# coding: utf-8

# # Compute Cost Function of an iteration
# 
# - For reporting to user, to show that the cost function per iteration is consistency updated to its local minima
# 
# - Nothing to do with compute gradient of the cost function, since we compute gradient in `mlp.ipynb`
# 
# - plan to add with `compute_grad` (Specifically for get_nesterov_momentum_v)
# 
# # 2 cases
# - No regularization
# - Regularization 
# > L2 : (+ squared Frobenius norm of all layers of weight )

# In[1]:
#import import_ipynb

from .losses import *
from .regularization import get_L2_weight_penalty
# External modules
import numpy as np


# In[2]:


__all__ = ['compute_cost','get_L2_weight_penalty']


# In[1]:


# !Support only L2 regularization
def compute_cost(AL, Y , loss_function, regularization = None, **kwargs):
    """
    Compute the cost function with respect to AL
    cost function : Binary cross entropy
    
    Arguments:
    -----------------------------------------
    AL --- predicted value from L-Forward model
    y --- actual output
    loss_function --- first class function, loss function like Binary-Cross Entropy
    regularization --- regularization technique
    
    Keyword Arguments:
    -----------------------------------------
    lambd --- Regularization parameter for L2 Regularization 
    param --- Parameter for L2 Regularization (Especially weight)
    """
    
    #Setup
    allowed_kwargs = {'lambd','param'} 
    for kwarg in kwargs.keys():
        assert kwarg in allowed_kwargs, 'Invalid keyword argument: ' + kwarg
        
    m = Y.shape[1]

    _loss = loss_function(AL, Y)

    if _loss.shape[0] != 1:  # often is cross-entropy loss
        _loss = np.sum(_loss, axis = 0, keepdims=True)
    
    cost = (1/m) * np.sum(_loss, axis=1)
    
    if regularization:
        if regularization == 'L2':
            # -- Checking -- #
            assert {'lambd','param'} <= set(kwargs), 'L2 Regularization lacks of keyword argument lambd or param'
            lambd = kwargs['lambd']
            param = kwargs['param']
            # -- Validated -- #
            cost += get_L2_weight_penalty(lambd,param,m)
            
        elif regularization == 'L1':
            # ...
            print("Not supported L1 now")
            pass
        
        else:                                
            pass   # Dropout have same cost functton as None
    
    return cost

