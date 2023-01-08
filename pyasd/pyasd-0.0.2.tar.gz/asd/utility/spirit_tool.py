#!/usr/bin/env python

#=============================================
#
# Analyze Spirit results
#
# Shunhong Zhang
# Last modified: Dec 21, 2020
#
#=============================================

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from .spin_visualize_tools import *


def verbose_quantities(p_state,conf_name,write_spin=False):
    from spirit import quantities, system, io
    mg=quantities.get_magnetization(p_state)
    sp = system.get_spin_directions(p_state)
    tc = quantities.get_topological_charge(p_state)
    en = system.get_energy(p_state,idx_image=0)
    fmt='{:30s}, Q = {:10.5f}, E_tot = {:10.5f} eV, M =['+' {:10.6f}'*3+' ]'
    print (fmt.format(conf_name,tc,en/1e3,*tuple(mg)))
    filename='spin_{0}.ovf'.format(conf_name)
    if write_spin: io.image_write(p_state, filename, fileformat=3)
    return mg,en,tc


def get_spin_sites_from_cfg(fil_cfg='input.cfg'):
    from spirit import state, geometry
    with state.State(fil_cfg,quiet=True) as p_state:
        pos = geometry.get_positions(p_state)
        ncell = geometry.get_n_cells(p_state)
        nat = geometry.get_n_cell_atoms(p_state)
    return pos.reshape(ncell[2],ncell[1],ncell[0],nat,3)
    

def trace_quantities(fils,fil_cfg='input.cfg'):
    from spirit import io, quantities, state, system, geometry, chain, configuration
    def conf_prop(p_state,conf_name):
        fmt='conf from fil: {:55s}, topo chg = {:8.4f}, en ={:12.6f} eV, M=[{:8.4f},{:8.4f},{:8.4f}]'
        system.update_data(p_state)
        tc=quantities.get_topological_charge(p_state)
        en = system.get_energy(p_state)
        mg = quantities.get_magnetization(p_state)
        print (fmt.format(conf_name,tc,en/1e3,*tuple(mg)))
    indice_int = np.array([fil.split('_')[-1].rstrip('.ovf') for fil in fils],int)
    fils = [fils[np.where(indice_int==i)[0][0]] for i in sorted(indice_int)]
    print ('\nTrace quantities')
    with state.State(fil_cfg,quiet=True) as p_state:
        chain.set_length(p_state,len(fils)+1)
        for i,fil in enumerate(fils):
            chain.jump_to_image(p_state,idx_image=i)
            io.image_read(p_state,fil)
            conf_prop(p_state,fil)
        chain.jump_to_image(p_state,idx_image=len(fils))
        configuration.plus_z(p_state)
        conf_prop(p_state,'ferromagnetic')


if __name__=='__main__':
    print ('post-processing of LLG simulation results produced by Spirit')
