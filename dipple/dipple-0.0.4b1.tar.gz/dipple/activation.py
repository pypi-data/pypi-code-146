#!/usr/bin/env python
# coding: utf-8

# # Activation function && Gradient of Activation function
# 
# Activation function is great for preventing the model to be linear model. Non-linear model often is able to learn complex problem
# 
# In Progress :
# 1. Perhap Turn this activation into an object involved both activation and its derivative

# In[1]:


# %% External module
import numpy as np


# In[7]:


__all__ = ['linear','dlinear',
          'sigmoid','dsigmoid',
          'tanh', 'dtanh',
          'relu','drelu',
          'leakyrelu','dleakyrelu',
          'softmax']


# # Linear
# 
# <fieldset>
#     
# - A.K.A. Identity function
# - often used at the output layer only
# - appropriate for regression task only
# 
# ![image.png](attachment:aea90a8a-6b56-4463-9c7d-d35bea9b81a1.png)

# In[8]:


def linear(z: np.ndarray) -> np.ndarray:
    assert isinstance(z,np.ndarray)
    return z

def dlinear():
    return 1


# # Sigmoid
# 
# <fieldset>
#     
# - Again, often used at output layer only, due to the mean is not zero, make it harder to compute for the next layer
# - Great for binary classification since its range is (0,1) 
#     
# ![image.png](attachment:a9d31856-eeaf-40db-9332-823675c6ce68.png)

# In[9]:


def sigmoid(z: np.ndarray) -> np.ndarray:
    assert isinstance(z,np.ndarray)      # temporary : in case z is not numpy array object
    return 1 / (1 + np.exp(-z))

def dsigmoid(z: np.ndarray) -> np.ndarray: 
    assert isinstance(z,np.ndarray)
    a = sigmoid(z)
    return a*(1 - a)


# # TanH
# 
# <fieldset>
#     
# - Shifted version of Sigmoid with mean zero 
# - Used to replace the idea that Sigmoid is not appropriate for hidden layer due to its mean is not zero, but tanh does
# 
# ![image.png](attachment:875cf651-a20c-4e4e-9fb4-228d9f2607e8.png)

# In[10]:


def tanh(z: np.ndarray) -> np.ndarray:
    assert isinstance(z,np.ndarray)
    return (np.exp(z) - np.exp(-z)) / (np.exp(z) + np.exp(-z))

def dtanh(z: np.ndarray) -> np.ndarray:
    assert isinstance(z,np.ndarray)
    a = tanh(z)
    return 1 - a ** 2


# # ReLU
# 
# <fieldset>
#     
# - stand for Rectified unit
# - A piesewise function one where turn those negative value to all zero, else z itself
# - Like Tanh, it's more appropriate in hidden layer (but faster than tanh due to punish those negative value to exactly zero)
# - May appropriate in regression task when your output cannot be negative value
# 
# ![image.png](attachment:fdfb0dd7-1aa6-4757-ae7e-0e129fb6facc.png)

# In[11]:


def relu(z: np.ndarray) -> np.ndarray:   # always return numpy array
    return np.where(z >= 0, z, 0)

def drelu(z: np.ndarray) -> np.ndarray:
    return np.where(z >= 0, 1, 0)


# # LeakyReLU
# 
# <fieldset>
#     
# - A variant of ReLU but 
# - used to solve vanish problem when the gradient at the early layer are negative for every iteration, so the parameter cannot update due to multiplication of zero, so leakyReLU do not punish them to be exactly zero but 0.01, so they can at least get updated
#     
# ![image.png](attachment:72d8b17f-62ad-437e-bfc9-7987921853e9.png)

# In[3]:


def leakyrelu(z: np.ndarray) -> np.ndarray: 
    return np.where(z >= 0, z, 0.01 * z)

def dleakyrelu(z: np.ndarray) -> np.ndarray:
    return np.where(z >= 0, 1, 0.01)


# In[2]:


def softmax(z: np.ndarray) -> np.ndarray: 
    a = np.exp(z)/np.exp(z).sum(axis=0)
    assert a.shape == z.shape ,'input and output of softmax dimension are mismatched '
    return a


# In[24]:





# In[26]:




