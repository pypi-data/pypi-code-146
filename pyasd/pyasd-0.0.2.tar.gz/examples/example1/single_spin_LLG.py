#!/usr/bin/env python

from __future__ import print_function
import numpy as np
from asd.core.hamiltonian import spin_hamiltonian
from asd.core.log_general import *
from asd.core.llg_simple import *
from asd.core.llg_advanced import *
from asd.core.geometry import build_latt
import os
import matplotlib.pyplot as plt

def analytic_solution(alpha,H,t):
    phi = gamma_e/(1+alpha**2)*np.linalg.norm(H)*t
    n_z = np.tanh(alpha*phi)
    n_x = np.cos(phi)*np.sqrt(1-n_z**2)
    return n_x,n_z


def plot_spin_evolve(alpha,llg_time,spin_evolve,H,show=True):
    import matplotlib.pyplot as plt
    llg_time_grid = np.linspace(0,llg_time[-1],5001)
    n_x,n_z=analytic_solution(alpha,H,llg_time_grid)
    fig,ax=plt.subplots(1,1)
    ax.plot(llg_time,spin_evolve[:,0],'o-',label='$n_x$',zorder=1)
    ax.plot(llg_time,spin_evolve[:,2],'o',label='$n_z$',zorder=1)
    ax.plot(llg_time_grid,n_x,'m-',lw=5,alpha=0.4,zorder=-1,label='$n_x^{analytic}$')
    ax.plot(llg_time_grid,n_z,'g-',lw=5,alpha=0.4,label='$n_z^{analytic}$')
    for yy in [0,1]: ax.axhline(yy,c='gray',ls='--',alpha=0.5,zorder=-1)
    ax.set_ylabel('spin component')
    ax.set_xlabel('Time (ps)')
    ax.set_xlim(llg_time[0],llg_time[-1])
    ax.set_yticks(np.arange(-1,1.1,0.5))
    ax.legend()
    fig.tight_layout()
    fig.savefig('Sinlge_Spin_field',dpi=500)
    if show: plt.show()
    return fig


nx=1
ny=1
nz=1
nat=1

Bfield=np.array([0,0,1])
S_values=np.array([0.5])
SIA=np.zeros(1)
lat_type='square'

ham = spin_hamiltonian(
Bfield=Bfield,
S_values=S_values,
BL_SIA=[SIA],
boundary_condition=[0,0,0])

latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,nz)


log_handle=log_general(
n_log_conf=10000,
n_log_magn=200,
log_force=True,
)

kws=dict(
S_values=S_values,
lat_type=lat_type,
alpha=0.1,
dt=1e-2,
nstep=30000,
log_handle=log_handle,
conv_ener=1e-11,
)

restart=False

if __name__=='__main__':
    LLG = llg_solver(**kws)
    LLG_adv = llg_solver_adv(**kws)

    sp_lat=np.zeros((nx,ny,nat,3),float)
    sp_lat[...,0]=1.

    # run one of the following functions for test
    if not restart:
        log_time,log_ener,log_conf = LLG.llg_simulation(ham,sp_lat)
        #log_time,log_ener,log_conf = LLG.mpi_llg_simulation(ham,sp_lat)
        #log_time,log_ener,log_conf = LLG.mpi_llg_simulation_shared_memory(ham,sp_lat)
        #log_time,log_ener,log_conf = LLG_adv.mpi_llg_simulation(ham,sp_lat)
        #log_time,log_ener,log_conf = LLG_adv.mpi_llg_simulation_advanced(ham,sp_lat)

    log_time = np.loadtxt('M.dat')[:,0]
    spin_evolve = np.loadtxt('M.dat')[:,-3:]
    fig = plot_spin_evolve(kws['alpha'],log_time,spin_evolve,Bfield)
