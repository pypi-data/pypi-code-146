#!/usr/bin/env python

import numpy as np
import copy
from asd.core.shell_exchange import *
from asd.core.geometry import build_latt


MAE_dft=np.array([
  0.000000,
  0.076500,
  0.247000,
  0.503500,
  0.826000,
  1.183000,
  1.523500,
  1.805000,
  1.984000,
  2.046000,
])


def build_ham(S_values,SIA,BL_exch,BQ_exch,Bfield=np.zeros(3),nshell_bl=2,verbose=False,name='CrMnI6_ham'):
    from asd.core.hamiltonian import spin_hamiltonian
    ham = spin_hamiltonian(
    name = name,
    Bfield=Bfield,
    S_values=S_values,
    BL_SIA=[SIA],
    BL_exch = BL_exch[:nshell_bl],
    BQ_exch = BQ_exch,
    exchange_in_matrix=True)
    if verbose:
        print ('\n\n{0}\n{1}\n{0}'.format('='*30,ham._name))
        ham.verbose_all_interactions()
        ham.verbose_reference_energy(sp_lat)
        ham.map_MAE(sp_lat,show=True)
    return ham


# ham1 up to 2NN and ham2 up to 3NN 
def compare_hams_MAE(hams, labels, max_deg=90, deg_step=5, show=True, MAE_dft=None,
    figsize=(5,4)):
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    #rcParams['font.family']='Times New Roman'
    #rcParams['text.usetex']=True
    rcParams['axes.labelsize']='x-large'
    rcParams['xtick.labelsize']=14
    rcParams['ytick.labelsize']=14
    fig,ax=plt.subplots(1,1,figsize=figsize)
    for ii,ham in enumerate(hams):
        print ('\n\n{0}\n{1}\n{0}'.format('='*30,ham._name))
        sp_lat = np.zeros((1,1,ham._nat,3))
        en_ref = ham.verbose_reference_energy(sp_lat)
        angles_list,mae = ham.calculate_MAE(sp_lat,max_deg=max_deg,deg_step=deg_step,verbosity=0)
        ax.plot(angles_list,mae,label=labels[ii],lw=2.5)
    if MAE_dft is not None:
        angles = np.linspace(0,90.01,len(MAE_dft))
        ax.plot(angles,MAE_dft,label='DFT+U',lw=2)

    xlabel = '$\ \ \ \ \\theta (\degree) \ \ \ \ $'
    xl = '$\\mathrm{In-plane} \ \ \ \leftarrow$'
    xr = '$\\rightarrow \ \ \ \mathrm{Out-of-plane}$'
 
    # use this set when switching on 'usetex'
    #xlabel = '$\ \ \ \ \\theta\ (^\circ) \ \ \ \ $'
    #xl = '$\\textrm{In-plane} \ \ \ \leftarrow$'
    #xr = '$\\rightarrow \ \ \ \\textrm{Out-of-plane}$'

    xlabel = xl + xlabel + xr
    ax.set_xlabel(xlabel,fontsize=14)
    ax.set_ylabel('MAE (meV/site)',fontsize=14)
    ax.set_xticks(np.arange(0,100,30))
    ax.set_xlim(0,90)
    ax.set_ylim(-0.05,2.3)
    ax.legend(loc='upper left',framealpha=0,fontsize=14)
    fig.tight_layout()
    if show: plt.show()
    return fig



lat_type='honeycomb'
nx=1
ny=1
nz=1
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,nz)
nat=sites.shape[-2]

S1=3./2
S2=4./2
S_values=np.array([S1,S2])

Bfield=np.array([0,0,0])
SIA = np.array([0.280,0.322])*S_values**2


J1_sym = -np.array([
[   -0.3733 ,    0.0000  ,  -0.4017 ],
[    0.0000 ,   -1.1500  ,  -0.0004 ],
[   -0.4017 ,   -0.0004  ,  -0.5083 ]])

J1_sym = np.array([J1_sym,J1_sym])*S1*S2

DM1_rpz = np.array([0,0.208,0])*S1*S2 # symmetrized
DM1_rpz = np.array([DM1_rpz,-DM1_rpz])


J2a_sym = -np.array([
[   -0.4411 ,    0.0000  ,  -0.0578 ],
[    0.0000 ,   -0.4944  ,  -0.0006 ],
[   -0.0578 ,   -0.0006  ,  -0.4178 ]])
J2a_sym*=S1**2

J2b_sym = -np.array([
[   -0.9325  ,  -0.0003  ,   0.2766 ],
[   -0.0003  ,   0.1206  ,  -0.0006 ],
[    0.2766  ,  -0.0006  ,  -0.2350 ]])
J2b_sym*=S2**2

J2_sym = np.array([J2a_sym,J2b_sym])

DM2_rpz_1 = - np.array([ 0.0550  ,  -0.0000  ,  -0.1867]) * S1**2
DM2_rpz_2 = - np.array([-0.2712  ,  -0.0003  ,  -0.1009]) * S2**2
DM2_rpz=np.array([DM2_rpz_1,DM2_rpz_2])

J3_sym = -np.array([
[   -0.1433  ,   0.0000  ,  -0.0875 ],
[    0.0000  ,  -0.1925  ,   0.0000 ],
[   -0.0875  ,   0.0000  ,  -0.2158 ]])
J3_sym*=S1*S2
J3_sym = np.array([J3_sym,J3_sym])
DM3_rpz = -np.array([-0.0008  ,   0.0317  ,   0.0000]) *S1*S2
DM3_rpz = np.array([DM3_rpz,-DM3_rpz])

J1_iso = np.zeros(2)
J2_iso = np.zeros(2)
J3_iso = np.zeros(2)


J1_sym_xyz = get_exchange_xyz(J1_sym, rotvecs[0])
DM1_xyz = get_exchange_xyz(DM1_rpz,rotvecs[0])

J2_sym_xyz = get_exchange_xyz(J2_sym, rotvecs[1])
DM2_xyz = get_exchange_xyz(DM2_rpz,rotvecs[1])

J3_sym_xyz = get_exchange_xyz(J3_sym, rotvecs[2])
DM3_xyz = get_exchange_xyz(DM3_rpz,rotvecs[2])


exch_1 = exchange_shell( neigh_idx[0], J1_iso, J1_sym_xyz, DM1_xyz, shell_name = '1NN')
exch_2 = exchange_shell( neigh_idx[1], J2_iso, J2_sym_xyz, DM2_xyz, shell_name = '2NN')
exch_3 = exchange_shell( neigh_idx[2], J3_iso, J3_sym_xyz, DM3_xyz, shell_name = '3NN')


BQ1 = np.array([0, 0])

BQ2 = np.array([ 0.03276, -0.41128])
BQ2 = np.array([ 0.00000, -0.37015]) # modified Apr 22

bq_exch_1 = biquadratic_exchange_shell(neigh_idx[0],BQ1,'BQ_1NN')
bq_exch_2 = biquadratic_exchange_shell(neigh_idx[1],BQ2,'BQ_2NN')


BL_exch = [ exch_1, exch_2, exch_3]
BQ_exch = [bq_exch_2]


# ham0 and ham0_3NN are bilinear Hamiltonians, with exchange couplings up to the 2NN and 3NN respectively
ham0 = build_ham(S_values,SIA,BL_exch,[],nshell_bl=2,verbose=False,name='2NN_BL')
ham0_3NN = build_ham(S_values,SIA,BL_exch,[],nshell_bl=3,verbose=False,name='3NN_BL')


# ham1 and ham2 are built from ham0 and ham0_3NN, by adding a SCALAR biquadratic coupling between Mn-Mn NN pairs
ham1 = build_ham(S_values,SIA,BL_exch,BQ_exch,nshell_bl=2,verbose=False,name='2NN_BL+scalar_BQ')

BQ_exch_a = copy.deepcopy(BQ_exch)
BQ_exch_a[0]._BQ *= 1.5
ham2 = build_ham(S_values,SIA,BL_exch,BQ_exch_a,nshell_bl=3,verbose=False,name='3NN_BL+scalar_BQ')


# ham3 and ham4 are built from ham0 and ham0_3NN, by adding a TENSORIAL biquadratic coupling between Mn-Mn NN pairs
BQ_xyz = np.zeros((2,3,3))
BQ_xyz[1] = np.diag([0.9,0.9,0.6])
BQ_mat_1 = get_exchange_xyz(BQ_xyz,rotvecs[1])
bq_exch_2_generic = biquadratic_exchange_shell_general(neigh_idx[1],BQ_mat_1,shell_name='BQ_2NN')
ham3 = build_ham(S_values,SIA,BL_exch,[bq_exch_2_generic],nshell_bl=2,name='2NN_BL+tensorial_BQ')

BQ_xyz = np.zeros((2,3,3))
BQ_xyz[1] = np.diag([0.8,0.8,0.32])
BQ_mat_2 = get_exchange_xyz(BQ_xyz,rotvecs[1])
bq_exch_2_generic = biquadratic_exchange_shell_general(neigh_idx[1],BQ_mat_2,shell_name='BQ_2NN')
ham4 = build_ham(S_values,SIA,BL_exch,[bq_exch_2_generic],nshell_bl=3,name='3NN_BL+tensorial_BQ')


tensorial_BQ = '$[K_\parallel S_{iz}S_{jz}+K_\\perp (S_{ix}S_{jx}+S_{iy}S_{jy})]^2$'
scalar_BQ    = '$KS_{iz}^2S_{jz}^2$'
labels = [
'$H_{BL}^{3NN}+$'+tensorial_BQ,
'$H_{BL}^{2NN}+$'+tensorial_BQ,
'$H_{BL}^{3NN}+$'+scalar_BQ,
'$H_{BL}^{2NN}+$'+scalar_BQ,
'$H_{BL}^{2NN}$',
'$H_{BL}^{3NN}$']

hams = [ham4,ham3,ham2,ham1,ham0,ham0_3NN]
 

if __name__=='__main__':
    print ('exchange interactions for CrMnI6, U_eff(Cr)=2 eV, U_eff(Mn)=4 eV')
    sp_lat = np.zeros((1,1,2,3))
    #for ham in hams:
        #ham.verbose_all_interactions()
        #ham.verbose_reference_energy(sp_lat)
        #ham.map_MAE(sp_lat,show=True)
    
    idx = np.array([1,4])
    #hams = np.array(hams)[idx]
    #labels = np.array(labels)[idx]
    fig = compare_hams_MAE(hams,labels,MAE_dft=MAE_dft,figsize=(6,4))
    fig.savefig('MAE_model_DFT',dpi=800)
