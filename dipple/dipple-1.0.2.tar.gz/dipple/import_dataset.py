#!/usr/bin/env python
# coding: utf-8

# # Import_dataset
# 
# sample dataset to test and check our model dipple

# In[2]:


# %% External module
import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.datasets
from sklearn.model_selection import train_test_split


# In[48]:


def load_2D_dataset_football():
    """ Receive data file and partition into train test set"""
    data = scipy.io.loadmat('Dataset/data_football.mat')
        
    train_X = data['X'].T
    train_Y = data['y'].T
    test_X = data['Xval'].T
    test_Y = data['yval'].T
    
    return train_X, train_Y, test_X, test_Y


def load_2D_dataset_crescent() -> np.array:
    """ 
    Generated dataset make_moon from package sklearn.datasets
    and partition those into train test set
    
    Argument:
    None
    
    Return :
    train_X --- np.array of training X
    train_Y --- np.array of training Y
    test_X --- np.array of testing X
    test_Y --- np.array of testing Y
    """
    
    np.random.seed(3)
    train_X, train_Y = sklearn.datasets.make_moons(n_samples=300, noise=.2) 
    test_X, test_Y = sklearn.datasets.make_moons(n_samples=60, noise=.2) 
    
    train_X = train_X.T
    train_Y = train_Y.reshape((1, train_Y.shape[0]))
    test_X = test_X.T
    test_Y = test_Y.reshape((1, test_Y.shape[0]))   
    
    return train_X, train_Y, test_X, test_Y


# In[22]:


def merge_split_train_test_into_df(train_X, train_Y,test_X, test_Y):
    """
    Compact (train_X, train_Y,test_X, test_Y) into train_test dataset
    """
    df_train = pd.DataFrame(np.column_stack([train_X.T, train_Y.T]), 
                               columns=['x1', 'x2', 'y'])
    
    df_test = pd.DataFrame(np.column_stack([test_X.T, test_Y.T]), 
                           columns=['x1', 'x2', 'y'])
    
    df_train = df_train.astype({"y":'category'})
    df_test = df_test.astype({"y":'category'})
    
    sns.set()
    fig, axes = plt.subplots(1, 2)

    p = sns.scatterplot(data=df_train,x='x1',y='x2',hue='y',ax=axes[0])
    p.set_title('Training set')
    
    g = sns.scatterplot(data=df_test,x='x1',y='x2',hue='y',ax=axes[1])
    g.set_title('Test set')

    fig.tight_layout()
    
    return df_train, df_test


# In[49]:


class Dataset_Library:
    
    """
    A Dataset Library where contains all essential datasets to test on model
    """
    
    avai_load_func =    {'football' : load_2D_dataset_football ,
                         'crescent' : load_2D_dataset_crescent}
    
    def __init__(self,data_name):
        load_f = self.avai_load_func.get(data_name,None)
        
        if load_f:
            self.load_f = load_f
        else :
            raise ValueError(f'{data_name} is not in Dataset_Library.avai_load_func')
     
        self.train_X, self.train_Y, self.test_X, self.test_Y = self.load_f()
        self.df_train, self.df_test = merge_split_train_test_into_df(self.train_X, self.train_Y, self.test_X, self.test_Y)
        
    def get_4split(self):
        return self.train_X, self.train_Y, self.test_X, self.test_Y
    
    def get_2df(self):
        return self.df_train, self.df_test
        

