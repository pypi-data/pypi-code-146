#!/usr/bin/env python

# this function is still under development

import numpy as np
import matplotlib.pyplot as plt
from geometry import *


def gen_Rvecs(ncell=1,boundary_condition=[1,1,1]):
    Rvecs = np.mgrid[-ncell:ncell+1,-ncell:ncell+1,-ncell:ncell+1].reshape(3,-1).T
    for i in range(3):
        if boundary_condition[i]==0: Rvecs = Rvecs[Rvecs[:,i]==0]
    return Rvecs


# cutoff is in Angstrom, the same unit of latt
# sites are in shape of (nat,3), in fractional coord, within the unit cell
# sp_lat is in shape of (nx,ny,nz,nat,3), the spin configuration (normalized vector field)
# S_values are the spin quantum number for each spin site, in shape of nat
def calculate_dipolar_interaction_energy_real_space(latt,sites,sp_lat,S_values,
    cutoff=10,boundary_condition=[1,1,0]):

    sites_cart = np.dot(sites,latt)
    Rvecs = gen_Rvecs(ncell=1,boundary_condition=boundary_condition)
