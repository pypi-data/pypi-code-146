#!/usr/bin/env python

#=============================================
#
# visualize spin configurations
# of classic spin systems
# typically a vector field
# currently focus on 2D lattices
#
# For spin configurations loading
# interfaced to ovf files
# in OOMMF format (.ovf)
# commonly used in Spirit, OOMMF etc.
# Also the current package, pyasd
#
# Shunhong Zhang
# Last modified: Dec 21, 2020
#
#=============================================

from __future__ import print_function
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import gridspec
from asd.utility.ovf_tools import *
from asd.utility.auxiliary_colormaps import parula
import pickle
import os


def map_alpha(sites_cart,alpha,latt=None,scatter_size=15):
    import matplotlib.pyplot as plt
    xlen = np.max(sites_cart[:,0]) - np.min(sites_cart[:,0])
    ylen = np.max(sites_cart[:,1]) - np.max(sites_cart[:,1])
    if xlen>ylen: colorbar_orientation='horizontal'
    else: colorbar_orientation='vertical'
    fig,ax=plt.subplots(1,1)
    scat=ax.scatter(sites_cart[...,0],sites_cart[...,1],s=scatter_size,c=alpha,cmap='viridis')
    cbar=fig.colorbar(scat,shrink=0.5,orientation=colorbar_orientation)
    cbar.ax.set_title('$\\alpha$')
    ax.set_aspect('equal')
    ax.set_axis_off()
    ax.set_title('Map of damping parameter $\\alpha$')
    fig.tight_layout()
    fig.savefig('Alpha_map',dpi=300)
    plt.show()


def plot_mc():
    data=np.loadtxt(open('output/output_mc.txt'),skiprows=1)
    T,E,M,chi,c_v,cumulant=data.T
    fig,ax=plt.subplots(1,1)
    ax.plot(T,M/np.max(M),label='M')
    #ax.plot(T,E/np.max(abs(E)),label='E')
    ax.plot(T,chi/np.max(chi),label='$\chi$')
    #ax.plot(T,c_v/np.max(c_v),label='$C_v$')
    ax.set_xlabel('T (K)')
    ax.set_ylabel('normalized values')
    ax.legend(loc='upper right')
    ax.axhline(0,c='gray',ls='--',zorder=-1,alpha=0.7)
    return fig,ax


def get_energy_archive(fil_en):
    lines=open(fil_en).readlines()[3:]
    data=np.array([line.split('|') for line in lines])
    return np.array(data[:,np.array([0,2,4,5,6])],float)


def plot_energy_archive(iter_scale=1):
    import glob
    fil_en = glob.glob('output/*Image-00_Energy-archive.txt')[0]
    data=get_energy_archive(fil_en)
    iters,E_tot,E_ani,E_ex,E_DM = data.T
    iters //= iter_scale
    fig,ax=plt.subplots(1,1,figsize=(5,5))
    ax.plot(iters,E_tot,label='$E_{tot}$')
    ax.plot(iters,E_ani,label='$E_{ani}$')
    ax.plot(iters,E_ex,label='$E_{ex}$')
    ax.plot(iters,E_DM,label='$E_{DM}$')
    xl = 'Iterations'
    cc = np.log(iter_scale)/np.log(10)
    if cc>0: xl+='/10'
    if cc>1: xl+='$^{0:1.0f}$'.format(cc)
    ax.set_xlabel(xl)
    ax.set_ylabel('E (eV)')
    ax.set_ylim(-1.8,0.5)
    ax.legend(loc='upper center',ncol=2)
    fig.tight_layout()
    fig.savefig('Spirit_energy',dpi=500)
    return fig,ax


# in fractional coordinates
# sites should be in shape of (nx,ny,nat,ndim), ndim can be 2 or 3
def get_repeated_sites(sites,repeat_x=1,repeat_y=1):
    nx,ny=sites.shape[:2]
    sites_repeat = np.tile(sites,(repeat_x,repeat_y,1,1))
    for i,j in np.ndindex(repeat_x,repeat_y):
        sites_repeat[i*nx:(i+1)*nx,j*ny:(j+1)*ny,:,0] += i*nx
        sites_repeat[i*nx:(i+1)*nx,j*ny:(j+1)*ny,:,1] += j*ny
    return sites_repeat


# conf should be in shape of (nx,ny,nat,3) or (nx,ny,nz,nat,3)
def get_repeated_conf(conf,repeat_x=1,repeat_y=1,repeat_z=0):
    shape = conf.shape
    if len(shape)==4: conf_repeat = np.tile(conf,(repeat_x,repeat_y,1,1))
    if len(shape)==5: conf_repeat = np.tile(conf,(repeat_x,repeat_y,repeat_z,1,1))
    return conf_repeat


# shift the configuration along specific axes
def get_shifted_conf(conf,dx=1,dy=1,dz=0):
    shape = conf.shape
    if len(shape)==4: conf_shift = np.roll(confs_0,(-dy,-dx),axis=(1,0))
    if len(shape)==5: conf_shift = np.roll(confs_0,(-dz,-dy,-dx),axis=(2,1,0))
    return conf_shift


def ax_map_spin(ax,sites,spins,tri=None,Q_distri=None,color_mapping='Sz_full',
    scatter_size=30,colormap='rainbow',Q_colormap='bwr',Qmin=-0.2,Qmax=0.2):

    all_sites = sites.reshape(-1,sites.shape[-1])
    ndim = spins.shape[-1]
    all_spins = spins.reshape(-1,ndim)
 
    if colormap=='parula': colormap=parula
    if 'S' in color_mapping: 
        idx = {'Sx':0,'Sy':1,'Sz':2}[color_mapping.split('_')[0]]
        cc = all_spins[:,idx]
    if 'phi' in color_mapping: 
        phi = np.rad2deg(np.angle(spins[...,0] + 1.j*spins[...,1]))
        phi[phi<0] += 360
        if 'full' in color_mapping: norm = mpl.colors.Normalize(0,360)
        else: norm = mpl.colors.Normalize(np.min(phi),np.max(phi))

    Qmap_kwargs = dict(facecolors=Q_distri, edgecolors='none',cmap=Q_colormap,vmin=Qmin,vmax=Qmax,zorder=-2)
    if 'S' in color_mapping:
        Smap_kwargs = dict(c=cc,edgecolor='none',cmap=colormap,zorder=-1,vmin=-1,vmax=1,s=scatter_size)
        if color_mapping in ['Sx','Sy','Sz']:  Smap_kwargs.update(vmin=np.min(cc),vmax=np.max(cc))
        scat = ax.scatter(*tuple(all_sites[:,:2].T),**Smap_kwargs)
    elif 'phi' in color_mapping:
        Pmap_kwargs = dict(c=phi,cmap='hsv',zorder=-1,norm=norm,s=scatter_size)
        scat = ax.scatter(*tuple(all_sites[:,:2].T),**Pmap_kwargs)
    elif 'Q' in color_mapping:
        Q_mag = np.max(np.abs(Q_distri))
        if color_mapping=='Q' : Qmap_kwargs.update(vmin=-Q_mag,vmax=Q_mag)
        scat = ax.tripcolor(*tuple(all_sites[:,:2].T), tri, **Qmap_kwargs)
    else:
        print ('Currently valid color_mapping:')
        print ('Sx, Sy, Sz, phi (angle of in-plane S relative to x), Q (topological charge)')
        print ('Sx_full, Sy_full, Sz_full, phi_full, Q_full (colormap range [-1,1])')
        scat = None

    return scat


quiver_kws = dict(
units='x',
scale=1.2,
width=0.1,
headlength=5,
headwidth=3,
headaxislength=3,
pivot='mid',
cmap='rainbow')

def ax_plot_quiver(ax,sites,spins,quiver_kws=quiver_kws,colorful_quiver=False):
    if colorful_quiver: return ax.quiver(sites[:,0],sites[:,1],*tuple(spins.T),clim=(-1,1),**quiver_kws)
    else:               return ax.quiver(sites[:,0],sites[:,1],spins[:,0],spins[:,1],**quiver_kws)


def ax_plot_framework(ax,sites,latt=None,superlatt=None,framework=False):
    if not framework: ax.set_axis_off()
    if superlatt is not None:
        spoints = np.dot([[0,0],[1,0],[1,1],[0,1],[0,0]],superlatt)
        ax.plot(*tuple(spoints.T),'k--',alpha=0.5,zorder=-1)
    elif latt is not None:
        nx,ny,nat = sites.shape[:3]
        spoints = np.dot([[0,0],[1,0],[1,1],[0,1],[0,0]],latt)
        ax.plot(*tuple(spoints.T),'k--',alpha=0.5,zorder=-1)
    else:
        sites_f = sites.reshape(-1,sites.shape[-1])
        up_bound=np.max(sites_f,axis=0)
        dn_bound=np.min(sites_f,axis=0)
        margin = (up_bound-dn_bound)*0.05
        #margin[np.where(margin==0)]=1
        ax.set_xlim(dn_bound[0]-margin[0],up_bound[0]+margin[0])
        ax.set_ylim(dn_bound[1]-margin[1],up_bound[1]+margin[1])


def ax_plot_spin_2d(ax,sites,spins,xs=1,ys=1,x0=0,y0=0,
    site_plot_idx=-1,scatter_size=1,verbosity=1,
    title='spins',color_mapping='Sz_full',mapping_all_sites=True,
    tri=None,Q_distri=None,Qmin=-0.1,Qmax=0.1,
    framework=False,latt=None,superlatt=None,
    colormap='rainbow',Q_colormap='bwr',
    quiver_kws=quiver_kws,colorful_quiver=False):

    if colormap=='parula': colormap=parula
    quiver_kws['cmap']=colormap

    shape0=list(sites.shape)
    shape0[-1]=spins.shape[-1]
    spins = spins.reshape(shape0)
    if site_plot_idx == -1: 
        sites_to_plot = sites[x0::xs,y0::ys].reshape(-1,sites.shape[-1])
        spins_to_plot = spins[x0::xs,y0::ys].reshape(-1,shape0[-1])
    else:
        sites_to_plot = sites[x0::xs,y0::ys,np.array(site_plot_idx,int)].reshape(-1,sites.shape[-1])
        spins_to_plot = spins[x0::xs,y0::ys,np.array(site_plot_idx,int)].reshape(-1,shape0[-1])

    qv = ax_plot_quiver(ax,sites_to_plot,spins_to_plot,quiver_kws,colorful_quiver)

    if not colorful_quiver:
        if mapping_all_sites: scat = ax_map_spin(ax,sites,spins,tri,Q_distri,color_mapping,scatter_size,colormap,Q_colormap,Qmin=Qmin,Qmax=Qmax)
        else: scat = ax_map_spin(ax,sites_to_plot,spins_to_plot,tri,Q_distri,color_mapping,scatter_size,colormap,Q_colormap,Qmin=Qmin,Qmax=Qmax)
    else: scat = None

    tl = ax.set_title(title)
    ax_plot_framework(ax,sites,latt,superlatt,framework)
    ax.set_aspect('equal')
    return qv,scat,tl


def select_sites_in_box(sites_cart,region=[0,1,0,1]):
    left,right,bot,top = region
    hor = np.logical_and(sites_cart[...,0]>=left,sites_cart[...,0]<right)
    ver = np.logical_and(sites_cart[...,1]>=bot, sites_cart[...,1]<top)
    idx = np.array(np.where(np.logical_and(hor,ver))).T
    box = np.array([[left,bot],[right,bot],[right,top],[left,top],[left,bot]])
    return idx, box


inset_indicator_kws=dict(
edgecolor='k',
ls='-',
)

def add_zoomin_inset(ax,sites_cart,conf,zoomin_region,inset_pos,spin_plot_kws={},inset_indicator_kws={}):
    idx,box = select_sites_in_box(sites_cart,zoomin_region)
    assert len(idx)>0, 'No sites in the specified region! {}'.format(zoomin_region)
    sites_select = np.array([sites_cart[tuple(ii)] for ii in idx])
    spins_select = np.array([conf[tuple(ii)] for ii in idx])
    if 'color_mapping' in spin_plot_kws.keys():
        if 'Q' in spin_plot_kws['color_mapping']:
            from asd.core.topological_charge import calc_topo_chg
            tri_simplices,Q_distri,Q = calc_topo_chg(spins_select,sites_select,spatial_resolved=True)
            spin_plot_kws.update(tri=tri_simplices,Q_distri=Q_distri)
 
    axins = ax.inset_axes(inset_pos)
    ax_plot_spin_2d(axins, sites_select, spins_select,**spin_plot_kws)
    axins.set_axis_on()
    axins.set_xticklabels([])
    axins.set_yticklabels([])
    axins.set_xticks([])
    axins.set_yticks([])
    if 'edgecolor' in inset_indicator_kws:
        for pos in ['top','bottom','left','right']: axins.spines[pos].set_color(inset_indicator_kws['edgecolor'])
    ax.indicate_inset_zoom(axins, **inset_indicator_kws)



def set_colorbar(fig,cb_ax,mapping_obj,cb_kws={},color_mapping='Sz_full',Qmin=-0.1,Qmax=0.1):
    if color_mapping=='phi_full':
        xval = np.arange(-np.pi, np.pi, 0.01)
        norm = mpl.colors.Normalize(-np.pi, np.pi)
        for r in np.arange(0.5,1,0.05):
            yval = np.ones_like(xval)*r
            cb_ax.scatter(xval, yval, c=xval, s=10, cmap='hsv', norm=norm, linewidths=0)
        cb_ax.text(0,0,'$\phi$',va='center',ha='center')
        cb_ax.set_yticks([])
        cb_ax.set_ylim(0,1)
        cbar = None
    else:
        Q_map = mapping_obj.get_clim()
        Q_mag = np.max(np.abs(Q_map))
        Qmin = np.min(Q_map)
        Qmax = np.max(Q_map)
 
        cbar = fig.colorbar(mapping_obj, ax=cb_ax,  **cb_kws)
        if color_mapping == 'Sz_full':
            if cb_ax is None: cbar.set_ticks([-1,0,1])
            else: cb_ax.set_yticks([-1,0,1])
        if color_mapping=='Q_full': 
            if cb_ax is None: cbar.set_ticks([Qmin,Qmax])
            else: cb_ax.set_yticks([Qmin,Qmax]); cb_ax.set_ylim(Qmin,Qmax)
        if color_mapping=='Q':    cbar.set_ticks([-Q_mag,0,Q_mag])
        if 'Q' in color_mapping:    cbar.ax.set_title('$dQ\ (\mathbf{r})$')
        if 'S' in color_mapping:    cbar.ax.set_title('$n_{}$'.format(color_mapping[1]))
    return cbar
 


def plot_spin_2d(sites,spins,xs=1,ys=1,x0=0,y0=0,
    site_plot_idx=-1,scatter_size=1,verbosity=1,
    title='spins',show=False,save=False,figname='spin_conf',fig_dpi=500,
    color_mapping='Sz_full',mapping_all_sites=True,
    tri=None,Q_distri=None,Qmin=-0.1,Qmax=0.1,framework=False,latt=None,superlatt=None,
    colormap='rainbow',Q_colormap='bwr',quiver_kws=quiver_kws,colorful_quiver=False,
    colorbar=True,colorbar_shrink=0.6,colorbar_orientation='auto',colorbar_axes_position=None,
    width_ratios=(8,1),height_ratios=(8,1),figsize=None):

    if colorbar_orientation=='auto':
        xlen = np.max(sites[...,0]) - np.min(sites[...,0])
        ylen = np.max(sites[...,1]) - np.max(sites[...,1])
        if xlen>ylen: colorbar_orientation='horizontal'
        else: colorbar_orientation='vertical'

    fig = plt.figure(figsize=figsize)

    if colorbar_orientation=='vertical':   gs = gridspec.GridSpec(1,2,width_ratios=width_ratios)
    if colorbar_orientation=='horizontal': gs = gridspec.GridSpec(2,1,height_ratios=height_ratios)
    if colorbar:  ax = fig.add_subplot(gs[0])
    else:         ax = fig.add_subplot(1,1,1)

    qv,scat,tl = ax_plot_spin_2d(ax,sites,spins,xs,ys,x0,y0,site_plot_idx,
    scatter_size,verbosity,title,color_mapping,mapping_all_sites,
    tri,Q_distri,Qmin,Qmax,framework,latt,superlatt,
    colormap,Q_colormap,
    quiver_kws,colorful_quiver)

    if colorbar: 
        cb_kws = dict(shrink=colorbar_shrink,orientation=colorbar_orientation)
        cb_ax = None
        if color_mapping=='phi_full':
            cb_ax = fig.add_subplot(gs[1],polar=True)
        else:
            if colorbar_axes_position is not None:
                cb_ax = fig.add_axes(colorbar_axes_position)
                cb_kws.update(cax=cb_ax)

        if scat is not None:  mapping_obj = scat
        elif colorful_quiver: mapping_obj = qv
        cbar = set_colorbar(fig,cb_ax,mapping_obj,cb_kws,color_mapping,Qmin,Qmax) 

    fig.tight_layout()
    if save: fig.savefig(figname,dpi=fig_dpi)
    if show: plt.show()
    return fig,ax,scat,qv,tl


def plot_spin_2d_from_ovf(sites,fil_ovf,xs=1,ys=1,x0=0,y0=0,site_plot_idx=-1,quiver_kws={},
    scatter_size=1,verbosity=1,title=None):
    if verbosity: print ('plot spins from file {0}'.format(fil_ovf))
    params,spins = parse_ovf_1(fil_ovf)
    if title is None: tt=fil_ovf.split('_')[-1].rstrip('.ovf')
    else: tt=title
    fig,ax,scat,qv,tl = plot_spin_2d(sites,spins,xs,ys,x0,y0,site_plot_idx,scatter_size,verbosity,tt,quiver_kws=quiver_kws)
    return fig,ax,scat,qv,tl


def plot_spin_3d(sites,spins,xs=1,ys=1,x0=0,y0=0,site_plot_idx=-1,scatter_size=1,verbosity=1,
    title='spins',show=False,save=False,figname='spin_conf',color_mapping='Sz_full',mapping_all_sites=True,
    tri=None,Q_distri=None,Qmin=-0.1,Qmax=0.1,framework=False,latt=None,superlatt=None,colormap='rainbow',Q_colormap='bwr',quiver_kws={},colorful_quiver=False,
    colorbar=True,colorbar_shrink=0.6,colorbar_orientation='vertical',width_ratios=(8,1),height_ratios=(8,1)):

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.cm as cm
    from asd.utility.arrow_3d import arrow3d
    if colormap=='parula': colormap=parula

    shape0=list(sites.shape)
    shape0[-1]=3
    spins = spins.reshape(shape0)
    if site_plot_idx == -1:
        sites_to_plot = sites[x0::xs,y0::ys].reshape(-1,sites.shape[-1])
        spins_to_plot = spins[x0::xs,y0::ys].reshape(-1,shape0[-1])
    else:
        sites_to_plot = sites[x0::xs,y0::ys,np.array(site_plot_idx,int)].reshape(-1,sites.shape[-1])
        spins_to_plot = spins[x0::xs,y0::ys,np.array(site_plot_idx,int)].reshape(-1,shape0[-1])


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for idx in range(spins_to_plot.shape[0]):
        x,y=sites_to_plot[idx]
        theta_x = np.rad2deg(np.arccos(spins_to_plot[idx,2]))
        theta_z = np.rad2deg(np.angle(spins_to_plot[idx,1] + 1.j*spins_to_plot[idx,0]))
        arrow3d(ax, offset=[x,y,0],
        theta_x=theta_x, theta_z=theta_z, color=cm.rainbow(theta_x/180.), **quiver_kws)

    #ax.set_xlim(0,10)
    #ax.set_ylim(-1,1)
    #ax.set_zlim(-1,1)
    ax.set_axis_off()
    plt.show()


def make_ani(sites,all_spins,titles=None,
    xs=1,ys=1,x0=0,y0=0,
    site_plot_idx=-1,interval=1e3,
    scatter_size=1, verbosity=1,jump=1,
    savegif=False,gif_name='LLG.ani',gif_dpi=300,color_mapping='Sz_full',colormap='rainbow',quiver_kws=quiver_kws,colorful_quiver=False,
    framework=False,mapping_all_sites = True, latt=None,superlatt=None,
    colorbar=True,colorbar_shrink=0.6,colorbar_orientation='auto',
    colorbar_axes_position=None,
    figsize=None,
    width_ratios=(8,1),height_ratios=(8,1)):

    from matplotlib.animation import FuncAnimation, PillowWriter

    def update(i, qv, scat, all_spins_to_plot, titles, tl, all_spins_to_map):
        spins = all_spins_to_plot[i].reshape(-1,3)
        spins_map = all_spins_to_map[i].reshape(-1,3)
        if colorful_quiver: qv.set_UVC(spins[:,0],spins[:,1],spins[:,2])
        else: qv.set_UVC(spins[:,0],spins[:,1])
        if scat is not None: 
            if 'Sz' in color_mapping: 
                scat.set_array(spins_map[:,2])
            elif 'phi' in color_mapping:
                phi = np.rad2deg(np.angle(spins_map[...,0] + 1.j*spins_map[...,1]))
                scat.set_array(phi)
        if titles is not None: tl.set_text(titles[i])

    if jump!=1:
        idx = np.arange(0,len(all_spins),jump)
        if len(all_spins)-1 not in idx: idx = np.append(idx,[-1])
        all_spins = all_spins[idx]
        if titles is not None: titles = np.array(titles)[idx]

    nframe=all_spins.shape[0]
    shape0=list(sites.shape)
    shape0[-1]=3
    all_spins = all_spins.reshape([nframe]+shape0)
    if site_plot_idx == -1:
        sites_to_plot = sites[x0::xs,y0::ys]
        all_spins_to_plot = all_spins[:,x0::xs,y0::ys]
    else:
        sites_to_plot = sites[x0::xs,y0::ys,np.array(site_plot_idx,int)]
        all_spins_to_plot = all_spins[:,x0::xs,y0::ys,np.array(site_plot_idx,int)]

    print ('\nMake animation: {0} frames in total'.format(len(all_spins)))
    print ('Color mapping quantity: {0}'.format(color_mapping))

    if latt is not None: superlatt = np.dot([[sites.shape[0],0],[0,sites.shape[1]]],latt)
    if titles is not None: title = titles[0]
    else: title = None

    if 'phi' in color_mapping: colormap='hsv'

    spin_plot_kws=dict(
    scatter_size=scatter_size,verbosity=verbosity,title=title,
    color_mapping=color_mapping,mapping_all_sites=True,framework=framework,
    colormap=colormap,quiver_kws=quiver_kws,colorful_quiver=colorful_quiver,latt=latt,superlatt=superlatt,
    colorbar=colorbar,colorbar_shrink=colorbar_shrink,colorbar_orientation=colorbar_orientation,
    colorbar_axes_position=colorbar_axes_position,
    width_ratios=width_ratios,height_ratios=height_ratios,
    figsize=figsize)

    fig,ax,scat,qv,tl = plot_spin_2d(sites,all_spins[0],xs,ys,x0,y0,site_plot_idx,**spin_plot_kws)

    anim = FuncAnimation(fig, update, frames=range(nframe), interval=interval, repeat=False,
    fargs=[qv, scat, all_spins_to_plot, titles, tl, all_spins])
    if savegif:
        print ('save animation to {}.gif'.format(gif_name))
        anim.save('{}.gif'.format(gif_name), dpi=gif_dpi, writer='imagemagick')
    else: plt.show()


def make_ani_from_ovf(sites,fils,xs=1,ys=1,site_plot_idx=-1,interval=0.5e3,scatter_size=1,quiver_kws={},jump=1,
    gif_name='LLG_ani',verbosity=1,sort_fils=True,titles=None,savegif=False):
    if sort_fils:
        indice_int = np.array([fil.split('_')[-1].rstrip('.ovf') for fil in fils],int)
        fils = [fils[np.where(indice_int==i)[0][0]] for i in sorted(indice_int)]
    if titles is None: titles=[fil.split('_')[-1].rstrip('.ovf') for fil in fils]
    all_spins = np.array([parse_ovf_1(fil)[1].reshape(sites.shape) for fil in fils])
    make_ani(sites,all_spins,titles,xs,ys,site_plot_idx,interval,scatter_size,quiver_kws,gif_name,verbosity,jump,savegif)


    
if __name__=='__main__':
    print ('post-processing of llg simulation results')

