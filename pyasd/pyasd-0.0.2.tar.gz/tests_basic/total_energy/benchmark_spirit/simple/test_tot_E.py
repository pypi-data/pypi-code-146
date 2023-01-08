#!/usr/bin/env python

from __future__ import print_function
import numpy as np
from spirit import chain,state,geometry,configuration,hamiltonian,system,quantities,io
from asd.utility.ovf_tools import parse_ovf
from asd.utility.spin_visualize_tools import make_ani
from asd.core.hamiltonian import *
from asd.core.geometry import *
from asd.core.shell_exchange import get_exchange_xyz, exchange_shell
import os


def get_Spirit_dataset(SIA,J1,J2,DM1,DM2,Bfield,nimage=10):
    en_spirit=[]
    mgs=[]
    bounds = []
    with state.State('input.cfg',True) as p_state:
        chain.set_length(p_state,nimage)
        for idx in range(nimage):
            chain.jump_to_image(p_state,idx_image=idx)
            geometry.set_n_cells(p_state,[nx,ny,1])
            ix,iy = np.random.randint(2,size=2)
            hamiltonian.set_boundary_conditions(p_state,[ix,iy,0])

            hamiltonian.set_anisotropy(p_state,SIA[0],[0,0,1])
            hamiltonian.set_field(p_state,np.linalg.norm(Bfield),Bfield)

            # NN + 2NN
            hamiltonian.set_exchange(p_state,2,[J1,J2])
            hamiltonian.set_dmi(p_state,2,[DM1,DM2])

            configuration.plus_z(p_state)
            if idx<10: configuration.skyrmion(p_state,radius=10*idx)
            else:      configuration.random(p_state)
            system.update_data(p_state)
            en_spirit.append(system.get_energy(p_state))
            mgs.append(quantities.get_magnetization(p_state))
            io.image_write(p_state,'confs/spin_{0}.ovf'.format(str(idx).zfill(2)))
            bounds.append( hamiltonian.get_boundary_conditions(p_state))
    en_spirit = np.array(en_spirit)
    return en_spirit,mgs,bounds


nimage=32

fmt_head='\n'+'='*120+'\n' + 'idx |'+'{:>7s}'*3+' | '+'{:>14s} '*2+'{:>16s} {:>20s}' + '{:>15s}\n'+'-'*120

nx=30
ny=30
lat_type='honeycomb'
latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,1,latt_choice=1)
sites_cart = np.dot(sites,latt)
nat=2

S_values = np.array([3./2,4./2])
Bfield=np.array([1.5,2,4])
SIA=np.array([0.5,0.5])

J1=1
J2=-0.23
J1_iso = np.ones(2)*J1
J2_iso = np.ones(2)*J2

DM1_rpz = np.array([[r3h,0.5,0],[-r3h,-0.5,0]])
DM1_xyz = get_exchange_xyz(DM1_rpz,rotvecs[0])
DM1 = np.linalg.norm(DM1_rpz[0])
DM2 = 0

exch_1 = exchange_shell( neigh_idx[0], J1_iso, DM_xyz = DM1_xyz, shell_name = '1NN')
exch_2 = exchange_shell( neigh_idx[1], J2_iso, shell_name = '2NN')

kws = dict(superlatt=np.dot(np.diag([nx,ny]),latt),colorbar_shrink=0.3,
colorbar_axes_position=[0.7,0.5,0.01,0.3],
colorbar_orientation='vertical',scatter_size=10,
titles=['config {}'.format(iconf) for iconf in range(nimage)])


if __name__=='__main__':
    if os.path.isdir('confs'): os.system('rm -rf confs')
    os.mkdir('confs')

    ham = spin_hamiltonian(Bfield=Bfield,S_values=S_values,
    BL_SIA=[SIA],
    BL_exch=[exch_1,exch_2],
    exchange_in_matrix=False)

    sp_lat = np.zeros((nx,ny,nat,3))
    ham.verbose_all_interactions(verbose_file='ham.dat')
    ham.verbose_reference_energy(sp_lat,file_handle=open('ham.dat','a'))

    nsites=nx*ny*nat
    fmt='{:7.3f}'*3
    en_spirit,mgs,bounds =get_Spirit_dataset(SIA,J1,J2,DM1,DM2,Bfield,nimage)

    confs = np.array([parse_ovf('confs/spin_{0}.ovf'.format(str(i).zfill(2)))[1] for i in range(nimage)])
    confs = np.swapaxes(confs.reshape(-1,ny,nx,nat,3),1,2)
    #make_ani(sites_cart,confs,**kws)

    print (fmt_head.format('Mx','My','Mz','E_spirit(meV)','my_E_tot(meV)','diff_E(meV)','diff_E(meV/site)',' |  boundary'))
    for i in range(nimage):
        mm=np.average(confs[i],axis=(0,1,2))
        ham._boundary_condition = bounds[i]
        en=ham.calc_total_E(confs[i],average_on_sites=False)
        print (('{:3d} |'+fmt).format(i+1,*tuple(mm)),end=' | ')
        print (('{:14.7f} '*2+'{:16.7e} {:20.8e}').format(en_spirit[i],en,en-en_spirit[i],(en-en_spirit[i])/nsites),end = '    | ')
        print(('{:3d} '*3).format(*tuple(bounds[i])))
    print ('='*120)
