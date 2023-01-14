#!/usr/bin/env python
# coding: utf-8

# # Multilayer Perceptron Components
# 
# - A.K.A. Components of Deep-L-Layer 
# > consists of 
# > 1. L_model_forward (Forward Propagation) to return output
# > 2. L_model_backward (Backward Propagation) to return error
# 
# Then use those errors of every parameter (known as gradient of cost function with respect to every parameter) to update parameters

# <img src="img_framework/mlp_architecture.jpg" alt="multilayer perceptron architecture" width="600" height="600"/>

# ---

# In[1]:


#import import_ipynb


# In[2]:


from .activation import *
from .regularization import dropout_unit

# %% External module
import numpy as np


# # Forward Propagation

# 0. Hyperparameter : Hidden Activation function , Output activation function
# 1. Input : A[0], parameter (dictionary of W[l], b[l])
# 2. Output : A[L]

# In[3]:


__all__ = ['linear_forward', 'linear_activation_forward', 'L_model_forward', 
           'linear_backward','linear_activation_backward', 'L_model_backward']


# In[4]:


def linear_forward(A_prev, W, b):
    """Linear Forward unit
    - Retrieve A_prev , W, b, and turn them into Z (with cache)
    
    Argument
    ----------    
    1. A_prev --- Activation node of the previous layer A[l-1]
    2. W --- Weight of layer l
    3. b --- Bias of layer l

    Return
    ----------
    1. Z --- Output Z of layer l 
    2. caches --- cache of Linear forward Unit
    """
    Z = np.dot(W, A_prev) + b
    
    assert(Z.shape == (W.shape[0], A_prev.shape[1]))
    cache = (A_prev,W,b)      # A :for dZ, W for dA & to get updating, b for updating , dA for dZ
    
    return Z, cache


# In[31]:


def linear_activation_forward(A_prev, W, b, activation_function):
    """Linear Forward unit
    - Dependencies of linear_forward and turn Z into A (with linear cache & activation cache)
    
    Argument
    ----------    
    1. A_prev --- Activation node of the previous layer A[l-1]
    2. W --- Weight of layer l
    3. b --- Bias of layer l

    Return
    ----------
    1. Z --- Output Z of layer l 
    2. caches --- cache of Linear forward Unit and Activation function
    """
    allowed_activation_function = {'sigmoid' : sigmoid,
                                  'tanh': tanh,
                                  'relu': relu,
                                  'leakyrelu' : leakyrelu,
                                  'linear' : linear,
                                  'softmax' : softmax}
    
    Z, linear_cache = linear_forward(A_prev, W, b)
    g = allowed_activation_function[activation_function]
    A = g(Z)
    
    activation_cache = Z
    
    assert (A.shape == (W.shape[0], A_prev.shape[1]))
    cache = (activation_cache, linear_cache)  # (Z, (A_prev,W,b))

    return A, cache


# In[6]:


def L_model_forward(X, param, hidden_activation_function, output_activation_function,**kwargs):   # Matter on Dropout
    """Forward propagation model from input to output layer
       Apply parameter to the input X to return the Activation Output 
    
    Argument
    ----------    
    1. X --- Input denoted as A[0]
    2. param --- Weight and Bias of every layer
                where its key must be {'W1','b1','W2','b2',...'WL','bL'}
                      its value must be numpy array with size n_l * n_l-1
                      
    3. hidden_activation_function --- the activation function for hidden layer 
    4. output_activation_function --- the activation function for output layer 
                                    Binary Classication : sigmoid
                                    Regression : linear
  
    Keyword Argument
    ----------   
    1. keep_prob_sequence --- When the regularization technique is dropout
    
    
    Return
    ----------
    1. AL --- Output A[L] from the propagation (Z[L] with sigmoid activation function)
    2. caches --- the cache of every layer l 
    """
   
    keep_prob_sequence = kwargs.get('keep_prob_sequence',None)

    A = X
    L = (len(param) // 2)  # param stores the weight and bias for L layer, hence len(param) = 2L

    caches = []

    # For Hidden Layer [1,2..,L-1]
    for l in range(1,L):  # l = 1,2,..,L-1
        A_prev = A
        W = param["W" + str(l)]
        b = param["b" + str(l)]
        A, cache = linear_activation_forward(A_prev, W, b, hidden_activation_function)
        
        if keep_prob_sequence is not None:                #For dropout
            A = dropout_unit(A,keep_prob_sequence[l])     
            
        caches.append(cache)  # append cache at layer l
    
    # For Output layer [L]
    
    A_prev = A
    W = param["W" + str(L)]
    b = param["b" + str(L)]
    AL, cache = linear_activation_forward(A_prev, W, b, output_activation_function)
    
    if keep_prob_sequence is not None:     #For dropout
        A = dropout_unit(A,keep_prob_sequence[l])
        
    caches.append(cache)

    #print(AL.shape)
    #assert(AL.shape == (1, X.shape[1]))  # deprecated
    return AL, caches


# In[39]:


w = np.array([[0.1,2,3,4],[7,8,9,10],[4,5,6,7]])
b = np.array([[1],[2],[3]])

A_prev = np.array([[1,2],[3,4],[5,6],[7,8]]) 


# In[50]:


w = np.random.randn(3,4)
b = np.zeros((3,1))

A_prev = np.array([[1,2],[3,4],[5,6],[7,8]]) 


# In[51]:


A_prev.shape


# In[57]:


output_activation_function = 'softmax'
A = linear_activation_forward(A_prev, w, b, output_activation_function )[0]


# In[58]:


A.shape


# In[60]:


A


# In[ ]:





# With Forward Propagation, we got 
# 
# 1. activation output at the last layer (AL) : 
# 
# <fieldset>
#     
# - data type : numpy array
# - size [1 * m]
# 
# </fieldset>
# 
# 2. cache (for every layer) : 
# 
# <fieldset> 
#     
# - data type : list
# - len : L 
# - each element : (activation_cache, linear_cache)
# - activation cache : Z_[l]
# - linear_cache : (A_[l-1], W[l], b[l]) 
#     
# </fieldset>

# ---

# # Backward Propagation

# 0. Hyperparameter : Hidden Activation function , Output activation function
# 1. Input : A[L], cache
# 2. Output : gradient of cost function of every parameter

# In[7]:


"""
Backward Propagation Unit
"""

def linear_backward(dZ, cache):
    """Retreive dZ from the layer l to obtain dW,dB,dA_prev
    Arguments
    ----------
      dZ -- Gradient of the cost with respect to the linear output (of current layer l)
      cache -- tuple of values (Z,(A_prev, W, b)) coming from the forward propagation in the current layer (We use only linear cache anyway)

    Returns
    ----------
      dA_prev --- Gradient of the cost with respect to the activation node at the previous layer
      dW --- Gradient of the cost with the weight in this layer
      db --- Gradient of the cost with the bias in this layer
    """
    _, linear_cache = cache  # We use only linear cache
    (A_prev, W, b) = linear_cache  # We do not use b to obtain those 3 gradients

    m = dZ.shape[1]  

    dW = (1 / m) * np.dot(dZ, A_prev.T)
    db = (1 / m) * np.sum(dZ, axis=1, keepdims=True)

    dA_prev = np.dot(W.T, dZ)
    
    assert (dA_prev.shape == A_prev.shape)
    assert (dW.shape == W.shape)
    assert (db.shape == b.shape)
    
    return dA_prev, dW, db


# In[8]:


def linear_activation_backward(dA, cache, activation_function):
    """Input dA to find dZ, then use dZ to obtain dW,dB,dA_prev
    Arguments
    ----------
      dZ -- Gradient of the cost with respect to the linear output (of current layer l)
      cache -- tuple of values (Z,(A_prev, W, b)) coming from the forward propagation in the current layer (We use only activation cache anyway)
    
    Returns
    ----------
      dA_prev --- Gradient of the cost with respect to the activation node at the previous layer
      dW --- Gradient of the cost with the weight in this layer
      db --- Gradient of the cost with the bias in this layer
    """
    
    allowed_activation_function = {'sigmoid' : dsigmoid,
                                  'tanh': dtanh,
                                  'relu':drelu,
                                  'leakyrelu' : dleakyrelu,
                                  'linear' : 1}
    
    activation_cache, _ = cache  # We use only activation cache
    Z = activation_cache
    
    g_ = allowed_activation_function[activation_function]   # dA/dZ
    dZ = dA * g_(Z)
    dA_prev, dW, db = linear_backward(dZ, cache)
    
    return dA_prev, dW, db


# In[1]:


def L_model_backward(AL, Y, cache, hidden_activation_function, output_activation_function, dZL_loss_function):
    """
    Backward propagation model from output AL to the parameter gradient of all layers
    Apply parameter to the input X to return the Activation Output 
    
    Arguments:
    A --- A at the layer L
    y --- an actual output
    cache --- cache from the forward propagation
    hidden_activation_function --- activation function for the hidden layer
    output_activation_function --- activation function for the output layer
    Return:
     grads  -- A dictionary with the gradients
               grads["dA" + str(l)] = ...
               grads["dW" + str(l)] = ...
               grads["db" + str(l)] = ...
    """
    L = len(cache)  # cache for each layer
    grads = {}
    allowed_dZL_function = {'BCE_dZL','CE_dZL','MSE_dZL'}
    assert dZL_loss_function.__name__ in allowed_dZL_function,  'Invalid dZL function: ' + dZL_loss_function.__name__
    
    # For Output layer
    
    dZL = dZL_loss_function(AL,Y)   # First chain of gradient is often be dZ[L] instead of dA[L] since it's easier to compute eg. AL-Y
    current_cache = cache[-1] 
    dA_prev, dW, db = linear_backward(dZL,current_cache)   # linear_backward often used for last layer
    grads["dW" + str(L)] = dW
    grads["db" + str(L)] = db
    
    dA = dA_prev
    
    # For Hidden layer [L-1, L-2...,1]
    for l in reversed(range(1,L)): 

        current_cache = cache[l-1] 
        (activation_cache, linear_cache) = current_cache
        
        Z = activation_cache
        a_prev, W, b = linear_cache  # Start with Z_[L] , A_[L-1], W_[L], b_[L]
        
        dA_prev, dW, db = linear_activation_backward(dA, current_cache, hidden_activation_function)

        grads["dW" + str(l)] = dW
        grads["db" + str(l)] = db
        
        dA = dA_prev

    return grads


# With Backward Propagation, we got 
# 
# 1. Gradient of cost function of all parameters : 
# 
# <fieldset>
#     
# - data type : dictionary
# - len : 2L (Each layer have weight and bias, so 2)
# 
# - len is the equivalent as `param`
# 
# </fieldset>

# ---

# In[ ]:




