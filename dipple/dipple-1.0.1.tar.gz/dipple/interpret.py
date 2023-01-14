#!/usr/bin/env python
# coding: utf-8

# # Interpretation
# 
# - `plot_decision_boundary`
# - `predict_dec`

# In[1]:


#import import_ipynb


# In[4]:


from .utils.py_util import pd_to_np

# %% External module
import numpy as np
import matplotlib.pyplot as plt


# In[5]:


@pd_to_np                                     # Turn all pandas object argument into numpy.array object
def plot_decision_boundary_2D(model, X, y, threshold = 0.5):
    """
    Plot decision boundary for two features, show slicing map of response variable
    
    Argument:
    model : model object which have method predict 
    X : Features as numpy object with dimension (m*2)
    y : response as numpy object with dimension (m*1)
    
    """
    
    assert X.shape[1] == 2
    assert X.shape[0] == y.shape[0]
    
    X, y = X.T, y.T
    
    x1_min, x1_max = (X[0, :].min() - 1, X[0, :].max() + 1)  
    x2_min, x2_max = (X[1, :].min() - 1, X[1, :].max() + 1)
    
    h = 0.01 
    X1, X2 = np.meshgrid(np.arange(x1_min, x1_max, h), np.arange(x2_min, x2_max, h))   #Cartesian matching af set X1, X2 ; lower h, more smoother 
    

    Z = model.predict(np.c_[X1.ravel(), X2.ravel()], threshold, predict_proba = False) 
    Z = Z.reshape(X1.shape)

    plt.contourf(X1, X2, Z, cmap=plt.cm.Spectral)
    plt.xlabel('X1')
    plt.ylabel('X2')
    
    plt.scatter(X[0, :], X[1, :], c=y, cmap=plt.cm.Spectral)
    plt.show()

