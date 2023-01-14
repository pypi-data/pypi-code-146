#!/usr/bin/env python
# coding: utf-8

# # Update parameter over iterations

# - Gradient descent is used to find the optimal parameter which atleast could make local minimum of cost function

# In[10]:


#import import_ipynb  # Import modules from Jupyter notebook


# In[11]:


from .mlp_component import * #linear_forward ,.... linear_backward_model
from .optimizer import *

# %% External modules
import numpy as np


# In[12]:


# I need param , grad, lr
# Optimizer method (so generate v & s)
# Regularization (add weight decay then)


# In[1]:


__all__ =   ['update_params', 
             'initialize_v','initialize_s',
             'bias_correction',
             'get_momentum_v','get_rmsprop_s','get_adagrad_s','get_adam_v_s']


# In[1]:


# TEST OPTIMIZER

def update_params(param,grads,lr, regularization=None, optimizer = None, **kwargs):
    """param in param_ out, updated by gradient descent technique
    
    Arguments:
    1. param
    2. grads -- d_theta 
    3. lr
    4. optimizer
    5. regularization

    Keyword Argument
    ----------   
    1. lambd 
    2. beta1
    3. beta2
    4. epsilon?
    
    Returns :
    param_ : updated parameter
    """
    

    
    """dict for dev
    grads_ : v
    lr_ : scaled lr
    param_ : updated param
    cache : list of v,s
    """
    L = len(param) // 2

    if optimizer: (param, optmz_caches) = _update_params_opt(param,grads,lr,optimizer,**kwargs) #.. special case for optimizer
    
    else:
        for l in range(1,L+1):                                                   #.. No optimizer case 
            param["W" + str(l)] -= lr * grads["dW" + str(l)]
            param["b" + str(l)] -= lr * grads["db" + str(l)]
            optmz_caches = None                                                  # ..
        
    # Add weight decay if regularization

    if regularization == "L2":
        assert {'lambd','m'} <= set(kwargs)
        lambd = kwargs.get("lambd")
        m = kwargs.get("m")
        for l in range(1,L+1):
            param["W" + str(l)] -= (lambd/m)*param["W" + str(l)]  

    return param, optmz_caches


# In[3]:


def _update_params_opt(param,grads,lr,optimizer,**kwargs):
    L = len(param) // 2
    t = kwargs.get('t')
    v = kwargs.get('v')
    s = kwargs.get('s')
    eps = kwargs.get('eps')

    if optimizer == 'momentum':
        beta1 = kwargs.get('beta1')
        grads_ = get_momentum_v(v,grads,beta1,t)   #..known as v
        lr_ : float = lr
        
        s = None

    elif optimizer == 'rmsprop':
        beta2 = kwargs.get('beta2')
        grads_ = grads
        s = get_rmsprop_s(s,grads,beta2,t)
        lr_ : dict = get_scaled_lr_rms(s,lr,eps)
        
    elif optimizer == 'adam':
        beta1 = kwargs.get('beta1')
        beta2 = kwargs.get('beta2')
        grads_ = get_momentum_v(v,grads,beta1,t)
        s = get_rmsprop_s(s,grads,beta2,t)
        lr_ : dict = get_scaled_lr_rms(s,lr,eps)

    for l in range(1,L+1):
        if not isinstance(lr_,dict) : lr_W, lr_b = np.full_like(grads["dW" + str(l)],lr_), np.full_like(grads["db" + str(l)],lr_)
        else: lr_W,lr_b = lr_[ "dW" + str(l) ], lr_[ "db" + str(l) ]

        param["W" + str(l)] -= np.multiply(lr_W, grads_["dW" + str(l)])   #.. element-wise mult
        param["b" + str(l)] -= np.multiply(lr_b, grads_["db" + str(l)])
    
    optmz_caches = [grads_,s]
    
    return param, optmz_caches

