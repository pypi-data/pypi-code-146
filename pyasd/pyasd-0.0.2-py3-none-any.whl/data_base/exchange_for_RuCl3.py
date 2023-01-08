#!/usr/bin/env python

# There are two typical models for RuCl3
# one is J1-K1-Gamma1-J3 model
# the other is J1-K1-Gamma1-Gamma' model
# For detials See e.g.
# Nat Phys. 16, 837 (2020)
#
# In an earlier reference
# Nat. Commun. 8, 1152 (2017)
# There is a simplified model nnHK which only
# contains J1 and K1
#
# Shunhong Zhang
# Jun 08 2021
#

from asd.core.geometry import *
from asd.core.shell_exchange import *
from asd.core.spin_configurations import gen_regular_order_on_honeycomb_lattice
import numpy as np
r3h=np.sqrt(3)/2


def get_lowdin(s):
    e, evec = np.linalg.eigh(s)
    if min(abs(e))<1e-6: exit('Error in Lowdin orthogonalization: zero eigenvalues found!')
    lowdin_mat = np.dot(evec/np.sqrt(e), evec.T.conj())
    return lowdin_mat


def get_analytic_E(J1,K1,Gamma1,J3):
    # Analytical form of energy per site is taken from Supplementary Information
    # of Nat. Commun. 8, 1152 (2017), 
    # Note that each configuration has its own easy magnetization axis

    Asqrt = np.sqrt(9*Gamma1**2 - 4*Gamma1*K1 + 4*K1**2) 

    analytic_E = {
    'FM':  -(3*J1 + K1 -   Gamma1 +3*J3)/8,
    'Neel-AFM':  (3*J1 + K1 + 2*Gamma1 +3*J3)/8,
    'stripy-AFM': -(-2*J1 + Gamma1 + 6*J3 + Asqrt )/16,
    'zigzag-AFM': -( 2*J1 - Gamma1 - 6*J3 + Asqrt )/16,
    '120':  (K1 + 2*Gamma1)/8,
    'IC': -(K1 - Gamma1 - np.sqrt(8*Gamma1**2 + K1**2) )/2 }
    return analytic_E


def test_ham(ham,analytic_E,kwargs):
    latt,sites = build_latt(lat_type,2,2,1,return_neigh=False)
    sites_cart = np.dot(sites,latt)

    from asd.utility.spin_visualize_tools import plot_spin_2d
    from asd.utility.plot_tools_3d import gen_grid_points_on_sphere
    #ham.verbose_all_interactions()
    sp_lat = np.zeros((2,2,2,3))
    fmt = '\nTest easy axis for the {:>10s} configuration, E_analytic   = {:9.5f} meV/site'
    fmt0= 'min_theta = {:5.1f} deg, min_phi = {:5.1f} deg, min[E(theta,phi)] = {:9.5f} meV/site'

    thetas,phis,Rvec = gen_grid_points_on_sphere(kwargs['nphi'],kwargs['ntheta'])

    for conf_name in analytic_E.keys():
        if conf_name in ['120','IC']: continue
        print (fmt.format(conf_name,analytic_E[conf_name]))
        #magmom = gen_collinear_magmom(conf_name)
        magmom = gen_regular_order_on_honeycomb_lattice(conf_name)
    
        kwargs.update(
        collinear_magmom = magmom,
        figname = '{}'.format(conf_name),
        )

        ens_map,fig = ham.map_MAE_3d(sp_lat,**kwargs)

        min_en = np.min(ens_map)
        idx = np.where(ens_map==min_en)
        idx = np.array([item[0] for item in idx])
        saxis = Rvec[:,idx[0],idx[1]]
        saxis_Kitaev = np.dot(saxis,np.linalg.inv(Kitaev_XYZ))
        theta_Kitaev = np.rad2deg(np.arccos(saxis_Kitaev[2]))
        phi_Kitaev   = np.rad2deg(np.angle(saxis_Kitaev[0]+1.j*saxis_Kitaev[1]))
        if phi_Kitaev<0: phi_Kitaev += 360
        print (fmt0.format(thetas[tuple(idx)],phis[tuple(idx)],min_en)+'  <-- Cartesian coordinate')
        print (fmt0.format(theta_Kitaev,phi_Kitaev,min_en)+'  <-- Kitaev coordinate')
        print(('saxis = ['+'{:10.5f} '*3+' ]').format(*tuple(saxis))+' '*38+'  <-- Cartesian coordinate')
        print(('saxis = ['+'{:10.5f} '*3+' ]').format(*tuple(saxis_Kitaev))+' '*38+'  <-- Kitaev coordinate')
        

def get_exchange_params(data_source='NP20'):
    if data_source=='NP20':           # parameters from Nat. Phys. 16, 837 (2020), Fig. 3
        J1     =  1.5
        K1     =  10
        Gamma1 = -8.8
        J3     = -0.4

    elif data_source=='NC17':         # parameters from Nat. Commun. 8, 1152 (2017), Fig. 5
        J1     =  0.5
        K1     =  5.0
        Gamma1 = -2.5
        J3     = -0.5

    elif data_source=='NP20_S2c':     # parameters from Nat. Commun. 8, 1152 (2017), Fig. S2(c)
        J1     =  1.6
        K1     =  9.6
        Gamma1 = -9.0
        J3     = -0.4

    elif data_source=='NP20_S2d':     # parameters from Nat. Commun. 8, 1152 (2017), Fig. S2(2)
        J1     =  2.21
        K1     =  9.12
        Gamma1 = -9.12
        J3     = -0.57

    return J1,K1,Gamma1,J3


def gen_shell_exchange(J1,K1,Gamma1,J3):
    J1_sym = np.tile(np.eye(3),(2,3,1,1))*J1

    for ibond in range(3):
        gam = ibond
        alpha = (ibond+1)%3
        beta  = (ibond+2)%3
        J1_sym[:,ibond,gam,gam] += K1
        J1_sym[:,ibond,alpha,beta] += Gamma1
        J1_sym[:,ibond,beta,alpha] += Gamma1

    J1_sym_xyz = J1_sym*S_values[0]*S_values[1]

    J3_sym = np.diag([J3,J3,J3])*S_values[0]*S_values[1]
    J3_sym_xyz = np.tile(J3_sym,(2,3,1,1))

    exch_1 = exchange_shell(neigh_idx[0], None, J1_sym_xyz, shell_name='1NN')
    exch_3 = exchange_shell(neigh_idx[2], None, J3_sym_xyz, shell_name='3NN')
    return exch_1,exch_3


lat_type='honeycomb'
nx=1
ny=1
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,1)
nat = sites.shape[-2]

S_values = np.array([1/2,1/2])
SIA = np.array([0.0,0.0])
z=0.1
Kitaev_xyz_0 = np.array([[-0.5,r3h,z],[-0.5,-r3h,z],[1,0,z]])
s=np.dot(Kitaev_xyz_0,Kitaev_xyz_0.T)
lowdin_mat = get_lowdin(s)
Kitaev_XYZ = np.dot(lowdin_mat,Kitaev_xyz_0)

data_source='NC17'
J1,K1,Gamma1,J3 = get_exchange_params(data_source)
exch_1,exch_3 = gen_shell_exchange(J1,K1,Gamma1,J3)


def build_ham(Bfield=np.zeros(3)):
    from asd.core.hamiltonian import spin_hamiltonian
    ham = spin_hamiltonian(Bfield=np.zeros(3),
    S_values=S_values,
    BL_SIA=[SIA],
    BL_exch = [exch_1,exch_3],
    exchange_in_matrix=True,
    spin_coord=Kitaev_XYZ)
    return ham


kwargs=dict(
display_mode = '3d',
#display_mode = '2d_kav',
ntheta=30,
nphi=60,
show=True,
savefig=False,
#cmap='RdYlBu',
)
 


if __name__=='__main__':
    #data_source='NP20_S2c'
    J1,K1,Gamma1,J3 = get_exchange_params(data_source)
    print ('Kitaev_XYZ')
    print ((('{:10.5f} '*3+'\n')*3).format(*tuple(Kitaev_XYZ.flatten())))
    analytic_E = get_analytic_E(J1,K1,Gamma1,J3)
    ham = build_ham()
    test_ham(ham,analytic_E,kwargs)
