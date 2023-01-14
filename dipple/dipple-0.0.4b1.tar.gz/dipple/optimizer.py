#!/usr/bin/env python
# coding: utf-8

# # Optimizer
# 
# - Make parameter goes toward local minima quicker, and be able to escape saddle point by adjusting Gradient descent with the following views
# 
# 1. gradient into exponentially weighted average of gradient (to go toward minima quickly)
# 2. learning rate into scaled learning rate (to be able to escape the saddle & converge to minima when the gradient is)
# 
# - There are many optimizers from momentum to ndam
# 
# 1. Momentum (1)
# 2. Nesterov momentum (1)
# 3. AdaGrad (2)
# 4. RMSProp (2)
# 
# - Combination of these above optimizer
# 1. adam (1) (4)
# 2. nadam (2) (4)
# 

# In[ ]:


# %% External modules
import numpy as np


# In[ ]:


__all__ = ['initialize_v','initialize_s','bias_correction',
          'get_momentum_v','get_adagrad_s','get_rmsprop_s','get_scaled_lr_rms','get_adam_v_s']


# In[ ]:


def initialize_v(grad):
    """first iteration of gd with momentum? generate it 
    
    Arguments:
    1. grad : grad dict
    
    Returns :
    1. v : initiatized exponentially weighted average of gradient dict
    """    
    
    L = len(grad) // 2 # number of layers in the neural networks
    v = {}
    
    for l in range(1,L+1):
        v["dW" + str(l)] = np.zeros_like(grad["dW" + str(l)])
        v["db" + str(l)] = np.zeros_like(grad["db" + str(l)])
    
    return v


# In[ ]:


def initialize_s(grad):
    """first iteration of gd with adaptive learning rate? generate it 
    
    Arguments:
    1. grad : grad dict
    
    Returns :
    1. v : initiatized exponentially weighted average of squared gradient dict
    """    
    
    return initialize_v(grad) # same as initialize_v


# In[1]:


def bias_correction(exp_avg,iteration,beta):
    """bias correction of v or s due to the exp. weighted average side effect
    
    Arguments:    
    exp_avg --- exponentially weighted average of anything [v/s]
    iteration --- current iteration
    beta --- hyperparameter of that exp_avg
    
    Returns:
    exp_avg_ --- bias corrected exponentially weighted average of anything 
    """
    L = len(exp_avg) // 2 # number of layers in the neural networks
    exp_avg_ = {}
    
    for l in range(1,L+1):
        exp_avg_["dW" + str(l)] = (exp_avg["dW" + str(l)] / (1-beta**iteration))
        exp_avg_["db" + str(l)] = (exp_avg["db" + str(l)] / (1-beta**iteration))
    
    return exp_avg_


# # 1. Gradient to Exponentially weighted average of gradient

# In[ ]:


def get_momentum_v(v,grad,beta1,iteration):
    """grad in exp.grad out 
    
    
    Arguments:
    1. v
    2. grad
    3. beta1
    4. nesterov
    
    Returns :
    1. s_ : new exponentially weighted average of gradient 
    """
    
    L = len(grad) // 2 # number of layers in the neural networks
    v_ = {}
    
    for l in range(1,L+1):
        v_["dW" + str(l)] = beta1 * v["dW" + str(l)] + (1-beta1) * grad["dW" + str(l)]
        v_["db" + str(l)] = beta1 * v["db" + str(l)] + (1-beta1) * grad["db" + str(l)]
    
    if iteration <= 10:
        ### Bias correction ###
        v_ = bias_correction(v_,iteration,beta1)
        
    return v_


# In[2]:


def get_nesterov_momentum_v(v,param):
    """grad lookahead in exp of grad lookahead oiut
    
    """
    pass


# # 2. Learning rate to Scaled learning rate

# In[ ]:


def get_adagrad_s(s,grad):
    """grad in exp.grad^2 out 
    
    
    Arguments:
    1. s
    2. grad
    
    Returns :
    1. s_ : new exponentially weighted average of (gradient)^2
    """
    
    L = len(grad) // 2 # number of layers in the neural networks
    s_ = {}
    
    for l in range(1,L+1):
        s_["dW" + str(l)] += grad["dW" + str(l)]
        s_["db" + str(l)] += grad["db" + str(l)]
    
    return s_


# In[7]:


def get_rmsprop_s(s,grad,beta2,iteration):
    """grad in exp. grad^2 out 
    
    
    Arguments:
    1. s
    2. grad
    3. beta2
    4. iteration --- current iteration for bias correction
    
    Returns :
    1. s_ : new exponentially weighted average of (gradient)^2
    """
    
    L = len(grad) // 2 # number of layers in the neural networks
    s_ = {}
    
    for l in range(1,L+1):
        s_["dW" + str(l)] = beta2 * s["dW" + str(l)] + (1-beta2) * (grad["dW" + str(l)])**2
        s_["db" + str(l)] = beta2 * s["db" + str(l)] + (1-beta2) * (grad["db" + str(l)])**2
    
    if iteration <= 10:
        ### Bias correction ###
        s_ = bias_correction(s_,iteration,beta2)
    
    return s_


# In[ ]:


def get_scaled_lr_rms(s, lr, eps):
    
    L = len(s) // 2
    lr_dct = {}
    for l in range(1,L+1):
        lr_dct[ "dW" + str(l) ] = np.full_like( s["dW" + str(l)],lr )
        lr_dct[ "dW" + str(l) ] /= (np.sqrt(s["dW" + str(l)]) + eps)
        
        lr_dct[ "db" + str(l) ] = np.full_like( s["db" + str(l)],lr )
        lr_dct[ "db" + str(l) ] /= (np.sqrt(s["db" + str(l)]) + eps)
    
    return lr_dct  


# In[ ]:


def get_adam_v_s(v,beta1,s,beta2,iteration):
    """ Obtain v and s of Adam
    
    Arguments:
    1. v
    2. beta1
    3. s
    4. beta2
    5. iteration --- current iteration for bias correction
    
    Returns :
    1. v_ : new exponentially weighted average of gradient
    2. s_ : new exponentially weighted average of (gradient)^2
    """
    v_ = get_momentum_v(v,grad,beta1,iteration)
    s_ = get_rmsprop_s(s,grad,beta2,iteration)
    return v_ , s_


# In[1]:


def get_nadam_v_s(v,beta1,s,beta2,iteration):
    v_ = get_nesterov_momentum_v(v,grad,beta1,iteration)
    s_ = get_rmsprop_s(s,grad,beta2,iteration)
    return v_ , s_


# In[2]:


class Optimizer:
    pass


# In[4]:


class Momentum(Optimizer):
    #self.iter = 1?
    def __init__(self,beta1,temp_param): # retreive **kwargs_dict - lambd
        self.v = initialize_v(temp_param)
        self.iteration = 1
        
    def get_grad(self,grad,v) -> dict :   

        grad_ = get_momentum_v(self.v,
                               grad,
                               beta1,
                               self.iteration)
        
        self.iteration += 1
        return grad_
    
    def get_lr(self,grad,lr): 
        return lr

    


# In[12]:


class Rmsprop(Optimizer):
    
    def __init__(self,beta2,eps,temp_param):
        self.s = initialize_s(temp_param)
        self.iteration = 1
        
        self.beta2 = beta2
        self.eps = eps
    
    def get_grad(self,grad): 
        return grad

    def get_lr(self,grad,lr) -> dict :
        s = get_rmsprop_s(self.s, 
                          grad, 
                          self.beta2, 
                          self.eps, 
                          self.iteration)
        lr_ : dict = get_scaled_lr_rms(s,lr,eps)
        self.iteration += 1
        
        return lr_ 


# In[ ]:


class Adam(Optimizer):
    
    def __init__(self,beta1,beta2,eps,temp_param):
        self.v = initialize_v(temp_param)
        self.s = initialize_s(temp_param)
        self.iteration = 1
        
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
    
    def get_grad(self,grad) -> dict :   
        grad_ = get_momentum_v(self.v,
                           grad,
                           self.beta1,
                           self.iteration)
        return grad_
    
    def get_lr(self,grad,lr) -> dict :
        s = get_rmsprop_s(self.s, 
                          grad, 
                          self.beta2, 
                          self.eps, 
                          self.iteration)
        lr_ : dict = get_scaled_lr_rms(s,lr,eps)
        self.iteration += 1
        
        return lr_ 

