#!/usr/bin/env python

from asd.core.llg_simple import *
from asd.core.spin_configurations import *
from asd.utility.ovf_tools import *
from spirit import io,state,geometry,configuration,chain,hamiltonian,system,quantities
import matplotlib.pyplot as plt


def get_Spirit_dataset(nx,ny,outdir,nimage=10,quiet=True,boundary_condition='periodic',fil_ovf='all_confs.ovf'):
    import os
    os.system('rm {} 2>/dev/null'.format(fil_ovf))
    en_spirit=[]
    mgs=[]
    if boundary_condition == 'random':   bound_cond = np.random.randint(2,size=(nimage,2))
    if boundary_condition == 'periodic': bound_cond = np.ones((nimage,2),int)
    bounds = []
    with state.State('',quiet) as p_state:
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
            #io.image_write(p_state,'confs/spin_{0}.ovf'.format(str(idx).zfill(2)))
            io.image_append(p_state,fil_ovf)
            pos = geometry.get_positions(p_state)
            bon = hamiltonian.get_boundary_conditions(p_state)
            np.testing.assert_allclose( bon[:2],[ix,iy])
            bounds.append(bon)
    en_spirit = np.array(en_spirit)
    return en_spirit,mgs,bounds,pos


def check_Spirit_ovfs(nx,ny,nat,fil_ovf='all_confs.ovf'):
    conf = np.zeros((ny,nx,nat,3))
    with ovf.ovf_file(fil_ovf) as ovf_file:
        print ('{} segments found'.format(ovf_file.n_segments))
        for iseg in range(ovf_file.n_segments):
            print ('\n{0}\nReading segment {1}\n{0}\n'.format('-'*30,iseg))
            segment = ovf.ovf_segment()
            ovf_file.read_segment_header(iseg,segment)
            ovf_file.read_segment_data(iseg,segment,conf)
            msg = ovf_file.get_latest_message()
            print (msg)
            with state.State(quiet=True) as p_state:
                io.image_read(p_state, fil_ovf)
 


nx=5
ny=4
nat=2
nsegment = 4

#get_Spirit_dataset(nx,ny,'.',nsegment)
#check_Spirit_ovfs(nx,ny,nat)

sp_lat = np.zeros((nx,ny,nat,3))
confs = []
for ic in range(nsegment):
    conf = init_random(sp_lat,verbosity=0)
    confs.append(conf)

confs = np.array(confs)
confs = confs.reshape(nsegment,-1,3)

fil_ovf = 'my_confs.ovf'
params = gen_params_for_ovf(nx,ny,nat,nsegment=nsegment)
write_ovf(params,confs,fil_ovf)

with ovf.ovf_file(fil_ovf) as ovf_file:
    print ('{} segments found'.format(ovf_file.n_segments))
    for iseg in range(ovf_file.n_segments):
        print ('\n{0}\nReading segment {1}\n{0}\n'.format('-'*30,iseg))
        segment = ovf.ovf_segment()
        ovf_file.read_segment_header(iseg,segment)
        conf_read = np.zeros((segment.N,segment.valuedim))
        ovf_file.read_segment_data(iseg,segment,conf_read)
        msg = ovf_file.get_latest_message()

        c1 = confs[iseg]
        c2 = conf_read
        np.testing.assert_allclose(c1,c2)
