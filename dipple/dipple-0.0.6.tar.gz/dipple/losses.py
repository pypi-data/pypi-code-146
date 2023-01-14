#!/usr/bin/env python
# coding: utf-8

# # Loss function
# - Used to evaluate how good the model is fit to the data 
# - technically, (dJ/dA[L]) without sum for every observation
# - Q: Why matter ? without them, 
# - A: we do not know what to fill in blank <br>
# Gradient of ____ with respect to this parameter
# - This module only used to report the loss
# 
# ### Available loss function : 
# - Binary Cross Entropy function (BCE) (**was planning to remove to make it general for both binary and multi-**)
# - Cross Entropy function (CE)
# - Mean Squared error (MSE) 
# - These dZ[L] based on J (first chain for the gradient is dZ[L] not dA[L], how ever for l!=L : we firstly use dAl 
# 
# The following cost function is being used since it's atleast a convex function for Logistic regression (No hidden layer)

# In[1]:


import numpy as np


# In[2]:


__all__ = ['binary_cross_entropy_loss','cross_entropy_loss','MSE',
           'BCE_dZL','CE_dZL','MSE_dZL']


# In[3]:


def binary_cross_entropy_loss(AL: np.ndarray, Y: np.ndarray) -> np.ndarray :  #plan to merge into cross entropy loss
    return -((Y * np.log(AL)) + ((1 - Y) * np.log(1 - AL)))  # For 1 output unit

def cross_entropy_loss(AL: np.ndarray, Y: np.ndarray) -> np.ndarray :
    return -(Y * np.log(AL))

def MSE(AL: np.ndarray, Y: np.ndarray) -> np.ndarray : # Often used for regression (output : linear)
    return np.power(AL - Y , 2)


# In[4]:


#dZL_loss_function

def BCE_dZL(AL: np.ndarray, Y: np.ndarray) -> np.ndarray :  #plan to merge into cross entropy loss
    return AL - Y   # For 1 output unit

def CE_dZL(AL: np.ndarray, Y: np.ndarray) -> np.ndarray :
    return  AL - Y

def MSE_dZL(AL: np.ndarray, Y: np.ndarray) -> np.ndarray :
    return 2 * (AL - Y)


# In[12]:


#binary_cross_entropy_loss test

y_test = np.array([[0.],[1.]])
A_test = np.array([[0.1],[0.6]])


# In[13]:


binary_cross_entropy_loss(A_test,y_test)


# In[14]:


BCE_dZL(A_test,y_test)


# In[7]:


#cross_entropy_loss test

y_test = np.array([[0,1,0,0],
                   [1,0,0,0]])
A_test = np.array([[0.02,0.9,0.03,0.05],
                   [0.4,0.05,0.15,0.6]])


# In[8]:


cross_entropy_loss(A_test,y_test)


# In[10]:


CE_dZL(A_test,y_test)

