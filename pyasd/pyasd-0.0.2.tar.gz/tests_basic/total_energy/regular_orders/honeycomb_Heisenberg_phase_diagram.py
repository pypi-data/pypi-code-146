#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.family'] = 'DejaVu Sans'
rcParams['font.family'] = 'Times New Roman'
rcParams['text.usetex'] = True

confs=['FM','Neel-AFM','zigzag-AFM','stripy-AFM','super-Neel-AFM']
 

def calc_energy(J1,J2,J3,conf='FM'):
    E={
    'FM':           ( 12*J1 + 24*J2 + 12*J3) * S**2,
    'Neel-AFM':     (-12*J1 + 24*J2 - 12*J3) * S**2,
    'zigzag-AFM':   (  4*J1 -  8*J2 - 12*J3) * S**2,
    'stripy-AFM':   ( -4*J1 -  8*J2 + 12*J3) * S**2,
    'super-Neel-AFM':   (           - 12*J3) * S**2
    }
    return E[conf]


def calc_energy_numerical(J1,J2,J3,conf='FM'):
    from asd.core.spin_configurations import gen_regular_order_on_honeycomb_lattice
    from asd.core.geometry import build_latt
    from asd.core.shell_exchange import exchange_shell
    from asd.core.hamiltonian import spin_hamiltonian
    latt,sites,neigh_idx,rotvecs = build_latt('honeycomb',2,2,1)
    ones = np.ones(2)*S**2
    exch_1 = exchange_shell(neigh_idx[0],-J1*ones, shell_name='1NN')
    exch_2 = exchange_shell(neigh_idx[1],-J2*ones, shell_name='2NN')
    exch_3 = exchange_shell(neigh_idx[2],-J3*ones, shell_name='3NN')
    ham = spin_hamiltonian(S_values=np.ones(2)*S,
    BL_SIA=[],BL_exch=[exch_1,exch_2,exch_3],iso_only=True)
    magmom = gen_regular_order_on_honeycomb_lattice(conf)
    sp_lat = np.zeros((2,2,2,3))
    sp_lat[...,2] = magmom
    E = ham.calc_total_E(sp_lat)
    return E



def calculate_phase_diagram(J1,J2,J3):
    energies1 = np.array([calc_energy(J1,J2,J3,conf) for conf in confs])
    m,n = J1.shape
    energies2 = np.array([[[calc_energy_numerical(J1[i,j],J2[i,j],J3[i,j],conf) for j in range(n)] for i in range(m)] for conf in confs] )
    #for ii in range(5): np.testing.assert_allclose(energies1[ii],energies2[ii],atol=1e-6); print ('{} passed'.format(confs[ii]))

    energies = energies2
    # determine which config has the lowest energy
    # for each set of [J2,J3]
    min_conf = np.argmin(energies,axis=0)
    return min_conf


def map_phase_diagram(J1,J2,J3,show=True,scatters=None,labels=None,mark_phase=False):
    min_conf = calculate_phase_diagram(J1,J2,J3)
    J10 = J1/J3
    J20 = J2/J3
    colors=['lightgreen','khaki','lightyellow','royalblue','m']
    fig,ax=plt.subplots(1,1,figsize=(6,5))
    for i,conf in enumerate(confs):
        idx = np.where(min_conf==i)
        if scatters is None: ax.scatter(J10[idx],J20[idx],facecolor=colors[i],edgecolor='none',s=5,label=confs[i])
        else: ax.scatter(J10[idx],J20[idx],facecolor=colors[i],edgecolor='none',s=5)

    if mark_phase:
        ax.text(-1.5,-0.7,'FM',ha='center',fontsize=12)
        ax.text( 3.5,-0.7,'Neel',ha='center',fontsize=12)
        ax.text(-1.5,1.75,'Zigzag',ha='center',fontsize=12)
        ax.text( 3.5,1.75,'Stripy',ha='center',fontsize=12)
 
    if scatters is not None:
        markers = ['o','s','^']
        colors = ['g','r','royalblue']
        lab=None
        for ii,scatt in enumerate(scatters):
            if labels is not None: lab = labels[ii]
            ax.scatter(scatt[0]/scatt[2],scatt[1]/scatt[2],marker=markers[ii],s=40,c=colors[ii],label=lab)
    if scatters is None: ms=5
    else: ms=1
    lg = ax.legend(markerscale=ms,loc='center left')
    #for ii,tt in enumerate(lg.get_texts()): tt.set_color(colors[ii])
    lg.get_frame().set_alpha(1)
    ax.set_xlim(min_J1,max_J1)
    ax.set_ylim(min_J2,max_J2)
    ax.set_xlabel('$J_1/J_3$',fontsize=16)
    ax.set_ylabel('$J_2/J_3$',fontsize=16)
    ax.set_title('$J_3={}$'.format(J3[0,0]))
    ax.axvline(0,ls='--',c='gray',alpha=0.5)
    ax.axhline(0,ls='--',c='gray',alpha=0.5)
    fig.tight_layout()
    figname = 'Honeycomb_Heisenberg_phase_diagram'
    if np.max(J3)>0: figname += '_positive_J3'
    else: figname += '_negative_J3'
    fig.savefig(figname,dpi=250)
    if show: plt.show()
    return fig


def tenary_phase_diagram(J10,J20,J30,min_conf,scatters=None):
    import ternary

    J1_min=np.min(J10)
    J1_max=np.max(J10)
    J2_min=np.min(J20)
    J2_max=np.max(J20)
    J3_min=np.min(J30)
    J3_max=np.max(J30)
    assert J1_max-J1_min == J2_max-J2_min == J3_max-J3_min, 'scale for three axes should be equal!'

    confs=['FM','Neel','Zigzag','stripy']
    colors=['c','pink','g','m']

    # Simple example:
    ## Boundary and Gridlines
    scale = J1_max-J1_min
    fig, tax = ternary.figure(scale=scale)
    tax.ax.axis("off")
    fig.set_facecolor('w')

    origin = np.array([J1_min,J2_min,J3_min])
    if scatters is not None:
        scatters = np.array([[0,0,0]])
        points = scatters - origin
        points = [tuple(point) for point in points]
        print (points)
        tax.scatter(points ,facecolor='r',edgecolor='none',s=20,zorder=2)

    # Draw Boundary and Gridlines
    tax.boundary(linewidth=1.0)
    tax.gridlines(color="black", multiple=1, linewidth=0.5, ls='-')

    # Set Axis labels and Title
    fontsize = 16
    tax.left_axis_label(  "$J_3$", fontsize=fontsize, offset=0.13)
    tax.right_axis_label( "$J_2$", fontsize=fontsize, offset=0.12)
    tax.bottom_axis_label("$J_1$", fontsize=fontsize, offset=0.06)

    # Set custom axis limits by passing a dict into set_limits.
    # The keys are b, l and r for the three axes and the vals are a list
    # of the min and max in data coords for that axis. max-min for each
    # axis must be the same as the scale i.e. 9 in this case.
    #tax.set_axis_limits({'b': [67, 76], 'l': [24, 33], 'r': [0, 9]})
    tax.set_axis_limits({'b': [J1_min, J1_max], 'r': [J2_min, J2_max], 'l': [J3_min, J3_max]})
 
    # get and set the custom ticks:
    tax.get_ticks_from_axis_limits()
    tax.set_custom_ticks(fontsize=10, offset=0.02)

    tax.ax.set_aspect('equal', adjustable='box')
    tax._redraw_labels()
    fig.tight_layout()
    fig.savefig('tri_axis_plots',dpi=300)
    plt.show()
    return fig


S=7/2
 
nn=300


Js_Cl = np.array([0.116,0.047,0.185])
Js_Br = np.array([0.105,0.042,0.188])
Js_I  = np.array([0.062,0.036,0.182])

scatters = [Js_Cl,Js_Br,Js_I]
labels = ['$\mathrm{Gd_2C'+halogen+'_2}$' for halogen in ['Cl','Br','I']]

if __name__=='__main__':
    min_J1=-2
    max_J1=4
    min_J2=-3
    max_J2=4
    min_J3=-4
    max_J3=4
    J10,J20 = np.mgrid[min_J1:max_J1:1j*nn,min_J2:max_J2:1j*nn]

    # J3 = -1, FM
    J3 = -np.ones_like(J10)
    J1 = J10*J3
    J2 = J20*J3
    map_phase_diagram(J1,J2,J3,show=False)

    # J3 = 1, AFM
    min_J1=-2
    max_J1=4
    min_J2=-1
    max_J2=2
    min_J3=-4
    max_J3=4
    J10,J20 = np.mgrid[min_J1:max_J1:1j*nn,min_J2:max_J2:1j*nn]

    J3 = np.ones_like(J10)
    J1 = J10*J3
    J2 = J20*J3
    map_phase_diagram(J1,J2,J3,scatters=scatters,labels=labels,mark_phase=True)
    exit()

    nn = 50
    max_J = max(max_J1,max_J2,max_J3)
    min_J = min(min_J1,min_J2,min_J3)
    J10,J20,J30 = np.mgrid[min_J:max_J:1j*nn,min_J:max_J:1j*nn,min_J:max_J:1.j*nn]
    min_conf = calculate_phase_diagram(J10,J20,J30) 
    #tenary_phase_diagram(J10,J20,J30,min_conf,scatters)
