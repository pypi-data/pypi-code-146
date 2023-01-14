#!/usr/bin/env python
# coding: utf-8

# # Weight Initialization
# 
# - `mlp` updates their parameter from gradient (gradient descent), without initiated parameter, it would say "Gradient of what?"
# 
# - The problem of `initialization_zero` for mlp makes all units in every layer got updated by the same gradient, when all units got the same updated then it means it's simply a model with every layer by 1 unit
# 
# - `initialization_random` figures out that zero problem, so each unit is uniquely updated but stuck at vanishing/exploding gradient problem
# - `initialization_xavier` figures out that random problem, appropriate for TanH activation function
# - `initialization_he` figures out that random problem, appropriate for ReLU and its variant activation function
# 
# Both xavier and he does not specify the distribution of parameter, so we planned to get both normal and **uniform (not done)**

# In[6]:


# %% External module
import numpy as np


# In[ ]:


__all__ =   ['initiate_param', 
             'initialization_zero','initialization_random',
             'initialization_xavier','initialization_he']


# In[2]:


# PLAN TO REPLACE AS DECORATOR

def initiate_param(layer_dims:list ,initialization :str = 'random',seed:int = 42) -> list:
    """Initiate the paramaters W, B for each layer
    
    Arguments
    ----------
        layer_dims : list
            A sequence of number of units for every layer 
        initialization : str, optional
            A technique of weight initialization (default:random)
        seed : int, optional 
            A seed for randomize the initialization
        
    
    Returns
    ----------
        param : numpy.array
            Array of parameter of every layer 
    
    """
    if seed:
        np.random.seed(seed)
        
    allowed_initialization_method = {'zero': initialization_zero,
                                     'random' : initialization_random,
                                    'he' : initialization_he,
                                    'xavier' : initialization_xavier}
    
    initialization_method = allowed_initialization_method[initialization]
    param = initialization_method(layer_dims)

    return param


# In[3]:


def initialization_zero(layer_dims:list):
    """Initialize both weight and bias as zeros
    
    Arguments
    ----------
    layer_dims : int
        A sequence of number of units for every layer 
    
    Returns
    ----------
    param : 
        Array of parameter of every layer 
    """
    
    L = len(layer_dims) - 1  #Exclude input layer to calculating L
    param = {}
    
    for l in range(1,L+1):
        param["W" + str(l)] = np.zeros(shape=(layer_dims[l], layer_dims[l-1])) * 0.01 # Uniform(0,1] * 0.01
        param["b" + str(l)] = np.zeros(shape=(layer_dims[l], 1))
        
        assert(param['W' + str(l)].shape == (layer_dims[l], layer_dims[l - 1]))
        assert(param['b' + str(l)].shape == (layer_dims[l], 1))
        
    return param


# In[4]:


def initialization_random(layer_dims:list,scale:int=0.01):
    
    """Initialize weight randomly with Normal(mean=0,sigma=1)
    Initialize bias as uniform distributed ( min=0,max= <1 )
    
    Arguments
    ----------
    layer_dimss : int
        A sequence of number of units for every layer 
    scale : float, optional
        A constant to scale the weight initialization
    
    Returns
    ----------
    param : 
        Array of parameter of every layer 
    """
    L = len(layer_dims) - 1  #Exclude input layer to calculating L
    param = {}
    
    """
    scale : variance of the random variable
    y = scale * x
    var(y) = var(scale*x)
    var(y) = scale^2 * x
    """
    for l in range(1,L+1):
        param["W" + str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) * scale # Normal(0,1) * scale 
        param["b" + str(l)] = np.random.rand(layer_dims[l], 1)
        
        assert(param['W' + str(l)].shape == (layer_dims[l], layer_dims[l - 1]))
        assert(param['b' + str(l)].shape == (layer_dims[l], 1))
        
    return param


# In[5]:


def initialization_xavier(layer_dims:list):
    """
    Initialize weight randomly with Normal(mean=0,sigma=(1/fan_avg))
    Initialize bias as uniform distributed ( min=0,max= <1 )
    
    Arguments
    ----------
    layer_dimss : int
        A sequence of number of units for every layer 
    
    Returns
    ----------
    param : 
        Array of parameter of every layer 
    """
    
    L = len(layer_dims) - 1  #Exclude input layer to calculating L
    param = {}
    
    for l in range(1,L+1):
        fan_in , fan_out = layer_dims[l-1] , layer_dims[l]
        fan_avg = 1/2 * (fan_in + fan_out)
        
        param["W" + str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) * np.sqrt(1/fan_avg) 
        param["b" + str(l)] =  np.random.rand(layer_dims[l], 1)
        
        assert(param['W' + str(l)].shape == (layer_dims[l], layer_dims[l - 1]))
        assert(param['b' + str(l)].shape == (layer_dims[l], 1))
        
    return param


# In[ ]:


def initialization_he(layer_dims:list):
    """
    Initialize weight randomly with Normal(mean=0,sigma=(2/fan_in))
    Initialize bias as uniform distributed ( min=0,max= <1 )
    
    Arguments
    ----------
    layer_dimss : int
        A sequence of number of units for every layer 
    
    Returns
    ----------
    param : 
        Array of parameter of every layer 
    """
    
    L = len(layer_dims) - 1  #Exclude input layer to calculating L
    param = {}
    
    for l in range(1,L+1):
        fan_in = layer_dims[l-1]
        
        param["W" + str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) * np.sqrt(2/fan_in) 
        param["b" + str(l)] =  np.random.rand(layer_dims[l], 1)
        
        assert(param['W' + str(l)].shape == (layer_dims[l], layer_dims[l - 1]))
        assert(param['b' + str(l)].shape == (layer_dims[l], 1))
        
    return param

