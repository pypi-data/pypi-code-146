#!/usr/bin/env python

# build lattice for spin dynamics simulations
# last modified: Dec 19 2020
# Shunhong Zhang <szhang2@ustc.edu.cn>

import numpy as np
from scipy.spatial.transform import Rotation as RT

r3h=np.sqrt(3)/2

# in fractional coordinates
# sites should be in shape of (nx,ny,nat,ndim), ndim can be 2 or 3
def get_repeated_sites(sites,repeat_x=1,repeat_y=1):
    nx,ny=sites.shape[:2]
    sites_repeat = np.tile(sites,(repeat_x,repeat_y,1,1))
    for i,j in np.ndindex(repeat_x,repeat_y):
        sites_repeat[i*nx:(i+1)*nx,j*ny:(j+1)*ny,:,0] += i*nx
        sites_repeat[i*nx:(i+1)*nx,j*ny:(j+1)*ny,:,1] += j*ny
    return sites_repeat


# find sites in a shell with circular or elliptic shape
# periodic boundary condition is applied in the 2D lattice
# ellipticity defines the shape of ellipse (1 is circle)
def find_pbc_shell(sites,latt,radius,center_pos=np.zeros(3),ellipticity=1.,orig=None):
    nx,ny,nat = sites.shape[:3]
    if orig is None: orig = np.array([nx,ny])/2.
    rvec_pbc = []
    for ix,iy in np.ndindex(2,2):
        rvec_add = np.dot(sites - orig - center_pos[:2] + np.array([(ix-1)*nx,(iy-1)*ny]), latt)
        rvec_add[...,1] *= ellipticity
        rvec_pbc.append(rvec_add)

    rvec_pbc = np.array(rvec_pbc)
    dist_pbc = np.linalg.norm(rvec_pbc,axis=-1)
    rvec = np.zeros((nx,ny,nat,2),float)
    idx = np.argmin(dist_pbc,axis=0)
    for ix,iy,iat in np.ndindex(nx,ny,nat):
        rvec[ix,iy,iat] = rvec_pbc[idx[ix,iy,iat],ix,iy,iat]
    dist = np.min(dist_pbc,axis=0)
    shell_idx=np.array(np.where(dist<=radius)).T
    return shell_idx,rvec


def build_latt(lat_type,nx,ny,nz,latt_choice=2,return_neigh=True):
    lat_type_list = ['chain','square','triangular','kagome','honeycomb','simple cubic']
    lat_type = lat_type.lower()
    if lat_type=='simple cubic':
        nat=1
        latt=np.eye(3)
        sites=np.zeros((1,1,1,3),float)+0.5
        neigh1_cell_idx = np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]])
        neigh2_cell_idx = np.array([
        [0,1,1],[0,1,-1],[0,-1,1],[0,-1,-1],
        [1,0,1],[1,0,-1],[-1,0,1],[-1,0,-1],
        [1,1,0],[1,-1,0],[-1,1,0],[-1,-1,0]])
        neigh3_cell_idx = np.mgrid[-1:2:2,-1:2:2,-1:2:2].T.reshape(-1,3)
        neigh1_idx = np.zeros((nat, 6,4),int)
        neigh2_idx = np.zeros((nat,12,4),int)
        neigh3_idx = np.zeros((nat, 8,4),int)
        neigh1_idx[:,:,:3] = neigh1_cell_idx
        neigh2_idx[:,:,:3] = neigh2_cell_idx
        neigh3_idx[:,:,:3] = neigh3_cell_idx

        rotvec_neigh1 = np.array([[[0.,0.,i] for i in range(4)]+[[0.,1.,0.],[0.,-1.,0.]]])*np.pi/2
        rotvec_neigh2 = np.array([[[0.,0.,i] for i in range(4)]+[[0.,1.,0.],[0.,-1.,0.]]])*np.pi/2
        rotvec_neigh3 = np.array([[[0.,0.,i] for i in range(4)]+[[0.,1.,0.],[0.,-1.,0.]]])*np.pi/2

    elif lat_type=='bcc':
        nat=2
        latt=np.eye(3)
        sites=np.zeros((1,1,1,nat,3),float)
        sites[...,1,:] += 0.5

        neigh1_cell_idx = np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]])
        neigh2_cell_idx = np.array([
        [0,1,1],[0,1,-1],[0,-1,1],[0,-1,-1],
        [1,0,1],[1,0,-1],[-1,0,1],[-1,0,-1],
        [1,1,0],[1,-1,0],[-1,1,0],[-1,-1,0]])
        neigh3_cell_idx = np.mgrid[-1:2:2,-1:2:2,-1:2:2].T.reshape(-1,3)

    elif lat_type=='chain':    # 1D chain built in 2D form
        nat=1
        latt=np.eye(2)
        sites=np.array([[[0.5,0.5]]])
        neigh1_cell_idx = np.array([[[-1],[1]]])
        neigh2_cell_idx = neigh1_cell_idx*2
        neigh3_cell_idx = neigh1_cell_idx*3
        neigh1_idx = np.zeros((nat,2,3),int)
        neigh2_idx = np.zeros((nat,2,3),int)
        neigh3_idx = np.zeros((nat,2,3),int)
        neigh1_idx[:,:,:1] = neigh1_cell_idx
        neigh2_idx[:,:,:1] = neigh2_cell_idx
        neigh3_idx[:,:,:1] = neigh3_cell_idx
        rotvec_neigh1 = None
        rotvec_neigh2 = None
        rotvec_neigh3 = None

    elif lat_type=='square':
        nat=1
        latt=np.eye(2)
        sites=np.zeros((1,1,1,2),float)+0.5
        neigh1_cell_idx = np.array([[[1,0],[0,1],[-1,0],[0,-1]]])
        neigh2_cell_idx = np.array([[[1,1],[-1,1],[-1,-1],[1,-1]]])
        neigh3_cell_idx = neigh1_cell_idx * 2
        neigh1_idx = np.zeros((nat,4,3),int)
        neigh2_idx = np.zeros((nat,4,3),int)
        neigh3_idx = np.zeros((nat,4,3),int)
        neigh1_idx[:,:,:2] = neigh1_cell_idx
        neigh2_idx[:,:,:2] = neigh2_cell_idx
        neigh3_idx[:,:,:2] = neigh3_cell_idx

        rotvec_neigh1 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
        rotvec_neigh2 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])
        rotvec_neigh3 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(4)]])

    elif lat_type=='triangular':
        nat=1
        latt=np.array([[1,0],[-0.5,r3h]])
        sites=np.zeros((1,1,nat,2),float)+0.5
        neigh1_cell_idx = np.array([[[1,0],[1,1],[0,1],[-1,0],[-1,-1],[0,-1]]])
        neigh2_cell_idx = np.array([[[2,1],[1,2],[-1,1],[-2,-1],[-1,-2],[1,-1]]])
        neigh3_cell_idx = neigh1_cell_idx * 2
        neigh1_idx = np.zeros((nat,6,3),int)
        neigh2_idx = np.zeros((nat,6,3),int)
        neigh3_idx = np.zeros((nat,6,3),int)
        neigh1_idx[:,:,:2] = neigh1_cell_idx
        neigh2_idx[:,:,:2] = neigh2_cell_idx
        neigh3_idx[:,:,:2] = neigh3_cell_idx

        #rotvec_neigh1 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(6)]])
        rotvec_neigh1 = np.array([[[0,0,0],[r3h,0.5,0],[0,0,2./3],[0,1,0],[0,0,4./3],[r3h,-0.5,0]]])*np.pi
        rotvec_neigh2 = np.array([[[0,0,0],[0.5,r3h,0],[0,0,2./3],[-0.5,r3h,0],[0,0,4./3],[1,0,0]]])*np.pi
        rotvec_neigh3 = np.array([[[0,0,0],[r3h,0.5,0],[0,0,2./3],[0,1,0],[0,0,4./3],[r3h,-0.5,0]]])*np.pi


    elif lat_type=='triangular_r3':
        print ('sqrt(3)xsqrt(3) triangular lattice, still under test')
        nat=3
        latt=np.array([[1,0],[-0.5,r3h]])*np.sqrt(3)
        sites=np.zeros((1,1,nat,2),float)
        for i in range(3): 
            sites[:,:,i,0] += 5./6 - i/3.
            sites[:,:,i,1] += 1./6 + i/3.
        neigh1_cell_idx = np.array([[[1,0],[1,1],[0,1],[-1,0],[-1,-1],[0,-1]]])
        neigh2_cell_idx = np.array([[[2,1],[1,2],[-1,1],[-2,-1],[-1,-2],[1,-1]]])
        neigh3_cell_idx = neigh1_cell_idx * 2
        neigh1_idx = np.zeros((nat,6,3),int)
        neigh2_idx = np.zeros((nat,6,3),int)
        neigh3_idx = np.zeros((nat,6,3),int)
        neigh1_idx[:,:,:2] = neigh1_cell_idx
        neigh2_idx[:,:,:2] = neigh2_cell_idx
        neigh3_idx[:,:,:2] = neigh3_cell_idx

        rotvec_neigh1 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(6)]])
        rotvec_neigh2 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(6)]])
        rotvec_neigh3 = np.array([[np.array([0.,0.,i])*np.pi/2 for i in range(6)]])


    elif lat_type=='kagome':
        nat=3
        latt=np.array([[1,0],[-0.5,r3h]])
        sites=np.zeros((1,1,nat,2),float)
        for i in range(3):
            sites[:,:,i,0] = (i<2)
            sites[:,:,i,1] = (i>0)
        sites *= 0.5
        neigh1_idx = np.array([
        [  [0,-1,2],[0,-1,1],[1,0,2],[0,0,1]  ],
        [  [0, 0,0],[1, 0,2],[0,1,0],[0,0,2]  ],
        [  [-1,0,1],[-1,0,0],[0,0,1],[0,1,0]  ]  
        ])

        neigh2_idx = np.array([
        [  [0,-1,2],[0,-1,1],[1,0,2],[0,0,1]  ],
        [  [0, 0,0],[1, 0,2],[0,1,0],[0,0,2]  ],
        [  [-1,0,1],[-1,0,0],[0,0,1],[0,1,0]  ]
        ])
        neigh3_idx = np.array([
        [  [-1,0, 0],[ 1, 0,0]  ],
        [  [-1,-1,1],[ 1, 1,1]  ],
        [  [ 0,-1,2],[ 0, 1,2]  ]
        ])

        # to be developed
        rotvec_neigh1 = None
        rotvec_neigh2 = None
        rotvec_neigh3 = None


    elif lat_type=='honeycomb':
        sites=np.zeros((1,1,2,2),float)
        nat=2

        if latt_choice == 1:  # consistent with Spirit code
            latt = np.array([[0.5,-r3h],[0.5,r3h]])
            sites[0,0,0]=np.array([0,0])
            sites[0,0,1]=np.array([1./3,2./3])
            neigh1_cell_idx = np.array([[0,0],[-1,-1],[0,-1]])
            neigh2_cell_idx = np.array([[1,1],[0,1],[-1,0],[-1,-1],[0,-1],[1,0]])
            neigh3_cell_idx = np.array([[-1,0],[0,-2],[1,0]])
            rotvec_neigh1 = np.array([[0.,0.,i*2./3] for i in range(3)])*np.pi

        if latt_choice == 2:  # consistent with our DFT calculations
            latt = np.array([[1,0],[-0.5,r3h]])
            sites[0,0,0] = np.array([1./3,2./3])
            sites[0,0,1] = np.array([2./3,1./3])
            neigh1_cell_idx = np.array([[0,1],[-1,0],[0,0]])
            neigh2_cell_idx = np.array([[1,0],[1,1],[0,1],[-1,0],[-1,-1],[0,-1]])
            neigh3_cell_idx = np.array([[-1,-1],[1,1],[-1,1]])
            rotvec_neigh1 = np.array([[0.,0.,i*2./3] for i in range(3)])*np.pi

        neigh1_idx = np.zeros((nat,3,3),int)
        neigh1_idx[0,:,:2] =  neigh1_cell_idx
        neigh1_idx[1,:,:2] = -neigh1_cell_idx
        neigh1_idx[0,:,2] = 1
        neigh1_idx[1,:,2] = 0

        neigh2_idx = np.zeros((nat,6,3),int)
        for iat in range(nat): neigh2_idx[iat,:,:2] = neigh2_cell_idx
        neigh2_idx[1,:,2] = 1

        neigh3_idx = np.zeros((nat,3,3),int)
        neigh3_idx[0,:,:2] =  neigh3_cell_idx
        neigh3_idx[1,:,:2] = -neigh3_cell_idx
        neigh3_idx[0,:,2] = 1
        neigh3_idx[1,:,2] = 0

        rotvec_neigh1 = np.array([rotvec_neigh1,rotvec_neigh1])
        rotvec_neigh2 = np.array([[0,0,0],[r3h,0.5,0],[0,0,2./3],[0,1,0],[0,0,4./3],[r3h,-0.5,0]])*np.pi
        rotvec_neigh2 = np.array([rotvec_neigh2,rotvec_neigh2])
        rotvec_neigh3 = np.array([np.array([0,0,i*2./3])*np.pi for i in range(3)])
        rotvec_neigh3 = np.array([rotvec_neigh3,rotvec_neigh3])
    else:
        print ('Currently valid lat_type:')
        for item in lat_type_list: print (item)
        exit ('Your specified lattice type: {}'.format(lat_type))

    ndim=sites.shape[-1]
    if ndim==2:
        xx,yy=np.mgrid[0:nx,0:ny]
        sites_sc = np.zeros((nx,ny,nat,ndim),float)
        for iat in range(nat):
            sites_sc[...,iat,0] = sites[...,iat,0] + xx
            sites_sc[...,iat,1] = sites[...,iat,1] + yy
    elif ndim==3:
        xx,yy,zz = np.mgrid[0:nx,0:ny,0:nz]
        sites_sc = np.zeros((nx,ny,nz,nat,ndim),float)
        for iat in range(nat):
            sites_sc[...,iat,0] = sites[...,iat,0] + xx
            sites_sc[...,iat,1] = sites[...,iat,1] + yy
            sites_sc[...,iat,2] = sites[...,iat,2] + zz

    neigh_idx = [neigh1_idx, neigh2_idx, neigh3_idx]
    rotvecs = [rotvec_neigh1, rotvec_neigh2,rotvec_neigh3]
    if return_neigh: return latt,sites_sc,neigh_idx,rotvecs
    else: return latt,sites_sc


def rectangular_honeycomb_cell(nx,ny,nz,return_neigh=True):
    lat_type='honeycomb'
    prim_latt,prim_sites = build_latt(lat_type,nx,ny,nz,return_neigh=False)
    nat=4
    latt=np.dot([[1,0],[1,2]],prim_latt)
    xx,yy=np.mgrid[0:nx,0:ny]
    sites=np.zeros((nx,ny,nat,2),float)
    sites_home = np.array([[1./4,1./3],[3./4,5./6],[3./4,1./6],[1./4,2./3]])
    for iat in range(nat):
        sites[...,iat,0] = xx + sites_home[iat,0]
        sites[...,iat,1] = yy + sites_home[iat,1]

    neigh1_idx = np.array([[[0, 0,3],[-1,0,2],[ 0,0,2]],
                           [[0, 1,2],[ 0,0,3],[ 1,0,3]],
                           [[0,-1,1],[ 1,0,0],[ 0,0,0]],
                           [[0, 0,0],[ 0,0,1],[-1,0,1]]])

    neigh2_idx = np.array([[[1,0,0],[0,0,1],[-1,0,1],[-1,0,0],[-1,-1,1],[0,-1,1]],
                           [[1,0,1],[1,1,0],[ 0,1,0],[-1,0,1],[ 0, 0,0],[1, 0,0]],
                           [[1,0,2],[1,0,3],[ 0,0,3],[-1,0,2],[ 0,-1,3],[1,-1,3]],
                           [[1,0,3],[0,1,2],[-1,1,2],[-1,0,3],[-1, 0,2],[0, 0,2]]])

    neigh3_idx = np.array([[[0,-1,3],[ 1, 0,3],[-1, 0,3]],
                           [[0, 0,2],[ 1, 1,2],[-1, 1,2]],
                           [[0, 0,1],[-1,-1,1],[ 1,-1,1]],
                           [[0, 1,0],[-1, 0,0],[ 1,0,0]]])

    #check_neigh_idx(latt,sites_home,[neigh1_idx,neigh2_idx,neigh3_idx])
    neigh_idx = [neigh1_idx, neigh2_idx, neigh3_idx]
    if return_neigh: return latt,sites,neigh_idx
    else: return latt,sites


def show_neighbors(latt,sites_sc,neigh_idx):
    import matplotlib.pyplot as plt
    nx,ny,nat = sites_sc.shape[:3]
    sites_cart = np.dot(sites_sc,latt)
    cnx = nx//2
    cny = ny//2
    points = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]])+np.array([cnx,cny])
    spoints = np.dot(points,latt)

    fig,ax = plt.subplots(1,1)
    ax.plot(spoints[:,0],spoints[:,1],c='gray',ls='--',alpha=0.5,zorder=-1)
    #ax.scatter(*tuple(sites_cart.T),s=10)
    ax.scatter(*tuple(sites_cart[cnx,cny,0]),marker='*',c='r',s=80)
    colors = ['g','b','orange']
    for ish,neigh_shell in enumerate(neigh_idx):
        for inn,(dx,dy,jat) in enumerate(neigh_shell[0]):
            jx = cnx+dx
            jy = cny+dy
            ax.scatter(*tuple(sites_cart[jx,jy,jat].T),facecolor='none',edgecolor=colors[ish],s=150)
            ax.text(*tuple(sites_cart[jx,jy,jat].T),'{:1d}'.format(inn),c=colors[ish],ha='center',va='center')
    ax.set_aspect('equal')
    ax.set_axis_off()
    plt.show()


def display_latt(latt,sites):
    import matplotlib.pyplot as plt
    nx,ny,nat=sites.shape[:3]
    points = np.dot([[0,0],[1,0],[1,1],[0,1],[0,0]],latt)
    spoints = np.dot([[0,0],[nx,0],[nx,ny],[0,ny],[0,0]],latt)
    all_sites = np.dot(sites,latt).reshape(-1,2)
    fig,ax=plt.subplots(1,1)
    ax.plot(points[:,0],points[:,1],'g--')
    ax.plot(spoints[:,0],spoints[:,1])
    for iat in range(nat): ax.scatter(*tuple(all_sites[iat::nat].T),label=str(iat))
    ax.legend(bbox_to_anchor=[1.01,0.5])
    ax.set_aspect('equal')
    ax.set_axis_off()
    fig.savefig('cell_sites',dpi=500)
    plt.show()
    return fig,ax


def calc_space_disp(latt,sites,cutoff_x,cutoff_y,cutoff_z=0,ndim=2,verbosity=0):
    from asd.core.shell_exchange import get_latt_idx
    shape = sites.shape
    nx,ny,nz,nat,idx = get_latt_idx(shape)
    nnx = 2*cutoff_x+1
    nny = 2*cutoff_y+1
    sites_cart = np.dot(sites,latt)
    space_disp = np.zeros((nnx,nny,nat,nat,ndim),float)
    if verbosity: print ('Calculate displacements between lattice sites.')
    for ii,dx in enumerate(range(-cutoff_x,cutoff_x+1)):
        for jj,dy in enumerate(range(-cutoff_y,cutoff_y+1)):
            for iat,jat in np.ndindex(nat,nat):
                space_disp[ii,jj,iat,jat] = sites_cart[0,0,jat] - sites_cart[0,0,iat] + np.dot([dx,dy],latt)
    return space_disp


nx=5
ny=5
nz=1

if __name__=='__main__':
    for lat_type in ['square','triangular','kagome','honeycomb','simple cubic']:
        print ('lat_type={}'.format(lat_type))
        latt,sites,neigh_idx,rotvecs = build_latt(lat_type,nx,ny,nz)
        if latt.shape[0]==2: show_neighbors(latt,sites,neigh_idx)
    latt,sites,neigh_idx = rectangular_honeycomb_cell(nx,ny,nz)
    show_neighbors(latt,sites,neigh_idx)
    display_latt(latt,sites)
