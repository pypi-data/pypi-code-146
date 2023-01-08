#!/usr/bin/env python3

from timeit import default_timer as timer
import numpy as np
from asd.core.llg_simple import *
from asd.data_base.rectangular_cell_U4 import *
from asd.core.geometry import build_latt
from asd.core.spin_configurations import *
from asd.utility.spin_visualize_tools import *
from asd.core.shell_exchange import *

nx=100
ny=36

#nx=1
#ny=1
latt,sites,neigh_idx = rectangular_honeycomb_cell(nx,ny,1)
Bfield=np.array([0,0,0])

fmt_head='{:>12s} ' *2+'|'+'{:>12s} ' *2
fmt_log ='{:12.5f} '*2+'|'+'{:12.5f} '*2

if __name__=='__main__':
    sp_lat = np.zeros((nx,ny,nat,3))
    sp_lat = init_random(sp_lat)
    nsites = np.prod(sp_lat.shape[:-1])


    ham = spin_hamiltonian(Bfield=Bfield,S_values=S_values,BL_SIA=[SIA],
    BL_exch = [exch_1,exch_2],
    BQ_exch = [bq_exch_2],
    exchange_in_matrix = True)

    print ('\n'+'='*60)
    print ('Energy (mev/site)'.center(24), ' | ','Used time (s)'.center(24))
    print ('{}'.format('-'*60))
    print (fmt_head.format(*tuple(['method_1','method_2']*2)))
    print ('{}'.format('-'*60))

    for i in range(10):
        sp_lat = init_random(sp_lat,verbosity=0)

        stime = timer()
        en_p1 = ham.calc_total_E_from_Jmat(sp_lat)/nsites
        t1 = timer()-stime

        stime = timer() 
        en_p2 = ham.calc_total_E_from_Jmat(sp_lat,use_new_method=True)/nsites
        t2 = timer()-stime

        print (fmt_log.format(en_p1,en_p2,t1,t2))
        np.testing.assert_allclose(en_p1, en_p2)
            
    print ('='*60)
