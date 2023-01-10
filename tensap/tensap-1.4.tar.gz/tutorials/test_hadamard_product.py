#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import tensap


def fun(I):
   return  I[:,0]*I[:,1] + I[:,2]*I[:,3] + I[:,4]
    
d=5
n=2
GRID = tensap.FullTensorGrid(np.arange(n), d)
I = GRID.array()

A = fun(I)
A = tensap.FullTensor(A, d, np.full(d, n))

TREE = tensap.DimensionTree.linear(d)
TR = tensap.Truncator()
TR.tolerance = 1e-8
Ar = TR.hsvd(A, TREE)

print('Error = %2.5e' % ((Ar.full()-A).norm()/A.norm()))
print('Storage = %d' % Ar.storage())
print('Ranks = %s\n' % Ar.ranks)


# %% 
A2=A*A
Ar2 = Ar*Ar

print('Error = %2.5e' % ((Ar2.full()-A2).norm()/A2.norm()))
