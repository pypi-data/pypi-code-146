#!/usr/bin/env python

from __future__ import print_function
import numpy as np
from spirit import chain,state,geometry,configuration,hamiltonian,system,quantities,io
from asd.utility.ovf_tools import parse_ovf,gen_params_for_ovf,write_ovf
from asd.utility.spin_visualize_tools import make_ani
from asd.core.hamiltonian import *
from asd.core.geometry import *
from asd.core.shell_exchange import get_exchange_xyz, exchange_shell, four_site_biquadratic_exchange_shell
import os


def get_Spirit_dataset(nx,ny,outdir,nimage=10,quiet=True,boundary_condition='periodic'):
    en_spirit=[]
    mgs=[]
    if boundary_condition == 'random':   bound_cond = np.random.randint(2,size=(nimage,2))
    if boundary_condition == 'periodic': bound_cond = np.ones((nimage,2),int)
    bounds = []
    with state.State('input.cfg',quiet) as p_state:
       chain.set_length(p_state,nimage)
       for idx in range(nimage):
            chain.jump_to_image(p_state,idx_image=idx)
            geometry.set_n_cells(p_state,[nx,ny,1])
            ix,iy = bound_cond[idx] 
            hamiltonian.set_boundary_conditions(p_state,[ix,iy,0])
            configuration.plus_z(p_state)
            if nx>=30 and ny>=30: 
                if idx<10: configuration.skyrmion(p_state,radius=idx*2)
                else:      configuration.random(p_state)
            else:
                if idx>=1: configuration.random(p_state)
            system.update_data(p_state)
            nos = system.get_nos(p_state)
            en0 = system.get_energy(p_state)
            mg0 = quantities.get_magnetization(p_state)
            en_spirit.append(en0)
            mgs.append(mg0)
            io.image_write(p_state,'confs/spin_{0}.ovf'.format(str(idx).zfill(2)))
            pos = geometry.get_positions(p_state)
            bon = hamiltonian.get_boundary_conditions(p_state)
            np.testing.assert_allclose( bon[:2],[ix,iy])
            bounds.append(bon)
    en_spirit = np.array(en_spirit)
    return en_spirit,mgs,bounds,pos



def test_one_lattice(outdir='honeycomb',nimage=30,nx=30,ny=30,boundary_condition='random'):
    lat_type=outdir
    latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,1,latt_choice=1)
    nat=sites.shape[-2]

    print ('\n\n'+'='*120)
    print ('Entering the following directory for testing:')
    print (outdir)
    print ('Use {} boundary condition'.format(boundary_condition))
    if boundary_condition!='periodic': print (open_bound_warning)
    print ('='*120+'\n\n')
    os.chdir(outdir)
    four_site = np.loadtxt('quadruplet',skiprows=2)

    S_values = np.ones(nat)*2
    SIA = [np.array([0.2]*nat),np.array([0.2]*nat),np.array([0.4]*nat)]
    SIA_axis = [np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])]

    BQ = four_site[:,-1]
    BQs = np.array([BQ]*nat)
    neigh_idx = [ [[item[2+jj*4],item[3+jj*4],item[1+jj*4]] for jj in range(3)] for item in four_site]
    neigh_idx = [np.array(neigh_idx, int), [] ]
    bq_four_site = four_site_biquadratic_exchange_shell(neigh_idx, BQs, 'four-site-BQ')
     
    ham = spin_hamiltonian(S_values=S_values,
    #BL_SIA=SIA,BL_SIA_axis=SIA_axis
    )
    ham.add_shell_exchange(bq_four_site,'general')

    if os.path.isdir('confs'): os.system('rm -rf confs')
    os.mkdir('confs')
    sp_lat = np.zeros((nx,ny,nat,3))
    ham.verbose_all_interactions(verbose_file='ham.dat')
    ham.verbose_reference_energy(sp_lat,file_handle=open('ham.dat','a'))

    nsites=nx*ny*nat
    fmt='{:9.5f}'*3
    en_spirit,mgs,bounds,pos =get_Spirit_dataset(nx,ny,outdir,nimage,True,boundary_condition)
    confs = np.array([parse_ovf('confs/spin_{0}.ovf'.format(str(i).zfill(2)))[1] for i in range(nimage)])
    confs = np.swapaxes(confs.reshape(-1,ny,nx,nat,3),1,2)
    sites_cart = np.swapaxes(pos.reshape(ny,nx,nat,3),0,1)

    kws = dict(superlatt=np.dot(np.diag([nx,ny]),latt),colorbar_shrink=0.3,
    colorbar_axes_position=[0.7,0.5,0.01,0.3],
    colorbar_orientation='vertical',scatter_size=30,
    titles=['config {}'.format(iconf) for iconf in range(nimage)])
    #make_ani(sites_cart,confs,**kws)

    fmt_head='\n'+'='*120+'\n' + 'idx |'+'{:>9s}'*3+' | '+'{:>14s} '*2+'{:>16s} {:>20s}' + '{:>15s}\n'+'-'*120
    print (fmt_head.format('Mx','My','Mz','E_spirit(meV)','my_E_tot(meV)','diff_E(meV)','diff_E(meV/site)',' |  boundary'))
    for i in range(nimage):
        mm=np.average(confs[i],axis=(0,1,2))
        ham.set_boundary_condition(bounds[i])
        en = ham.calc_total_E(confs[i],average_on_sites=False)
        #en = bq_four_site.calc_shell_exch_energy(confs[i],bounds[i])
        print (('{:3d} |'+fmt).format(i+1,*tuple(mm)),end=' | ')
        print (('{:14.7f} '*2+'{:16.7e} {:20.8e}').format(en_spirit[i],en,en-en_spirit[i],(en-en_spirit[i])/nsites),end = '    | ')
        print(('{:3d} '*3).format(*tuple(bounds[i])))
    print ('='*120)
    os.chdir('..')

 
open_bound_warning='''
For four-site quadruplet exchanges
We found some problems with Spirit for open boundary condition!
It always return energies under periodic boundary condition
The origin remains unclear'''
 
if __name__=='__main__':
    test_one_lattice('triangular',nx=20,ny=20,boundary_condition='periodic')
    test_one_lattice('honeycomb')
