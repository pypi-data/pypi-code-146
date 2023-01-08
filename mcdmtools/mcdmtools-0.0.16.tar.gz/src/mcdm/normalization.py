import pandas as pd
import numpy 
from numpy import log as ln

def vektorizeNormalization(dm, profitcost):
    squared = lambda x: x*x
    dm_norm = pd.DataFrame()
    for i in profitcost.columns:
        if profitcost.loc[0,i] == 'max':
            dm_norm[i] = dm[i] / squared(dm[i]).sum(axis=0)**0.5
        elif profitcost.loc[0,i]=='min':
             dm_norm[i] = 1- (dm[i] / squared(dm[i]).sum(axis=0)**0.5)
    return dm_norm

def compromiseNormalization(dm, profitcost):
    dm_norm = pd.DataFrame()
    for j in range(0,len(profitcost.columns)):
        col_name = "k" + str(j+1)
        maksimum = dm.iloc[:,j].max()
        minimum = dm.iloc[:,j].min()
        difference = maksimum - minimum
        if profitcost.iloc[0,j] == "max":
            dm_norm[col_name] = (dm.iloc[:,j]-minimum) / difference
        elif profitcost.iloc[0,j] == "min":
            dm_norm[col_name] = (maksimum - dm.iloc[:,j]) / difference
    return  dm_norm

def sumBasedLinearNormalization(dm, profitcost):
    dm_norm = pd.DataFrame()
    for i in profitcost.columns:
        if profitcost.loc[0,i] == 'max':
            dm_norm[i] = dm[i] / dm[i].sum(axis=0)
        elif profitcost.loc[0,i]=='min':
             dm_norm[i] = (1 / dm[i]) / ((1/dm[i]).sum(axis=0))
    return dm_norm

def logarithmicNormalization(dm, profitcost):
    dm_norm = pd.DataFrame()
    for i in profitcost.columns:
        if profitcost.loc[0,i] == 'max':
            dm_norm[i] = ln(dm[i]) / ln(dm.product())
        elif profitcost.loc[0,i]=='min':
            dm_norm[i] = (1-(ln(dm[i]) / ln(dm.product())))/(len(dm[i].index)-1)
    return dm_norm

def maximumLinearNormalization(dm,profitcost):
    dm_norm = pd.DataFrame()
    for i in profitcost.columns:
        if profitcost.loc[0,i] == 'max':
            dm_norm[i] = dm[i] / max(dm[i])
        elif profitcost.loc[0,i]=='min':
             dm_norm[i] = 1 - (dm[i] / max(dm[i]))
    return dm_norm

def minimumLinearNormalization(dm,profitcost):
    dm_norm = pd.DataFrame()
    for i in profitcost.columns:
        if profitcost.loc[0,i] == 'max':
            dm_norm[i] = 1-(min(dm[i]) / dm[i])
        elif profitcost.loc[0,i]=='min':
            dm_norm[i] = min(dm[i]) / dm[i]
    return dm_norm

def intervalNormalization(dm, profitcost):
    dm_norm = pd.DataFrame()
    for i in profitcost.columns:
        if profitcost.loc[0,i] == 'max':
            dm_norm[i] = dm[i] / max(dm[i])
        elif profitcost.loc[0,i]=='min':
            dm_norm[i] = min(dm[i]) / dm[i]
    return dm_norm

def juttlerKorthNormalization(dm, profitcost):
    dm_norm = pd.DataFrame()
    for i in profitcost.columns:
        if profitcost.loc[0,i] == 'max':
            dm_norm[i] = 1- abs((max(dm[i])-dm[i])/(max(dm[i])))
        elif profitcost.loc[0,i]=='min':
            dm_norm[i] = 1- abs((min(dm[i])-dm[i])/(max(dm[i])))
    return dm_norm