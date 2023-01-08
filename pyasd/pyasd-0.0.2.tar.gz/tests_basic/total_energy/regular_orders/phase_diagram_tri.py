#!/usr/bin/env python

# See the reference
# Phys. Rev. B 83, 184401 (2011)
# for defination of the tetrahedra order
# on a triangular spin lattice
# This order is the ground state of
# the J1-J2-J3 classical spin model
# in certain region of the phase diagram
# which can be obtained by our LLG simulations
#
# run llg.py to check this assertion
# Shunhong Zhang
# Aug 31, 2021


import numpy as np
from asd.core.geometry import *
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.core.shell_exchange import *
from asd.core.hamiltonian import *
import matplotlib.pyplot as plt
import asd.mpi.mpi_tools as mt

'''
lat_type = 'triangular_r3'
data = build_latt(lat_type,2,2,1)
latt,sites,neigh_idx,rotvecs = data
sites_cart = np.dot(sites,latt)
plt.scatter(sites_cart[...,0],sites_cart[...,1])
plt.show()
exit()
'''

lat_type='triangular'
data = build_latt(lat_type,2,2,1,latt_choice=1)
latt,sites,neigh_idx,rotvecs = data
nat=2

sp_lat = regular_order(lat_type,'tetrahedra')

def show_conf(sites,latt,sp_lat,xx=3,yy=3):
    sites1 = get_repeated_sites(sites,xx,yy)
    sp_lat1 = get_repeated_conf(sp_lat,xx,yy)
    sites_cart = np.dot(sites1,latt)
    plot_spin_2d(sites_cart,sp_lat1,latt=latt,scatter_size=50,show=True)


J1 = 1.
n2 = 101
n3 = 101
bb = 3
J2_values,J3_values = np.mgrid[-bb:bb:1.j*n2,-bb:bb:1.j*n3]
exch_1 = exchange_shell(neigh_idx[0], J1*np.ones(1), shell_name='J1')

comm,size,rank,node = mt.get_mpi_handles()
J2_values = J2_values.flatten()
J3_values = J3_values.flatten()

sp_lat_FM = np.zeros((1,1,1,3))
sp_lat_FM[...,2] = 1.

nn = len(J2_values)
start,last = mt.assign_task(nn,size,rank)
ens = np.zeros((last-start,2))
for i in range(start,last):
    J2 = J2_values[i]*np.ones(1)
    J3 = J3_values[i]*np.ones(1)
    exch_2 = exchange_shell(neigh_idx[1], J2, shell_name='J2')
    exch_3 = exchange_shell(neigh_idx[2], J3, shell_name='J3')
    ham = spin_hamiltonian(S_values = np.ones(1), 
    BL_SIA = [np.zeros(1)],
    BL_exch = [exch_1,exch_2,exch_3], iso_only=True)

    ens[i-start,1] = ham.calc_total_E(sp_lat)/np.prod(sp_lat.shape[:-1])
    ens[i-start,0] = ham.calc_total_E(sp_lat_FM)

ens = comm.gather(ens,root=0)

if rank==0:
    ens = np.concatenate(ens,axis=0)
    ediff = ens[...,1] - ens[...,0]
    vv = np.max(abs(ediff))
    idx = np.where(abs(ediff)<1e-1)
    fig,ax=plt.subplots(1,1)
    ax.scatter(-J2_values[idx],-J3_values[idx],c='k',s=2,zorder=2)
    cax = ax.scatter(-J2_values,-J3_values,c=ediff,cmap='bwr',vmin=-vv,vmax=vv)
    ax.set_xlim(-bb,bb)
    ax.set_ylim(-bb,bb)
    fig.colorbar(cax)
    ax.set_xlabel('$J_2$')
    ax.set_ylabel('$J_3$')
    fig.tight_layout()
    plt.show()
