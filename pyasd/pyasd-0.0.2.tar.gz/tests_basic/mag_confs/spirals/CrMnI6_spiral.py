#!/usr/bin/env python

import numpy as np
from asd.data_base.rectangular_cell_U4 import ham_rc,rectangular_honeycomb_cell
from asd.utility.spin_visualize_tools import plot_spin_2d


def test_spiral(ham_rec,nx_range,ny=6):
    from asd.core.spin_configurations import init_spin_spiral
    print ('testing spiral spin structures in rectangular cell')
    en=[]
    for nx in nx_range:
        latt,sites,neigh_idx[0],neigh_idx[1],neigh_idx[2] = rectangular_honeycomb_cell(nx,ny,1)
        nat = sites.shape[-2]

        q_vector = np.array([1./nx,0,0])*np.pi*2
        sp_lat=np.zeros((nx,ny,nat,3),float)
        sp_lat = init_spin_spiral(sp_lat,latt,sites,q_vector,20,0,axis=[0,1,1])
        sites_cart = np.dot(sites,latt)

        spins = np.swapaxes(sp_lat,0,1)
        sites_cart = np.swapaxes(sites_cart,0,1)

        tt = 'spiral, q=2*pi*[{:8.4f},{:8.4f},{:8.4f}]'.format(*tuple(q_vector/2/np.pi))
        quiver_kws = dict(units='x',pivot='mid',scale=1.5)
        fig,ax,scat,qv,tl = plot_spin_2d(sites_cart,spins,title=tt,
        show=False,scatter_size=10,save=True,latt=latt,quiver_kws=quiver_kws)

        en0 = ham_rec.calc_total_E_from_sym_mat(sp_lat)/(nx*ny*nat)
        print ('{:5d} {:12.5f}'.format(nx,en0))
        en.append(en0)

    import matplotlib.pyplot as plt

    fig,ax=plt.subplots(1,1)
    ax.plot(nx_range,en,'o-')
    ax.set_xlabel('nx')
    ax.set_ylabel('E (meV/site)')
    fig.tight_layout()
    plt.show()


if __name__=='__main__':
    test_spiral(ham_rc,range(20,24),ny=3)
