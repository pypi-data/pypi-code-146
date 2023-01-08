#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from asd.core.geometry import build_latt,find_pbc_shell

nx=20
ny=20
nz=1
radius1=5

latt,sites,neigh_idx,rotvecs = build_latt('square',nx,ny,nz)
nat=sites.shape[-2]
sites_cart = np.dot(sites,latt)

shell_idx,rvec = find_pbc_shell(sites,latt,radius1,pos=np.array([-nx,-ny,0])/2)
sites_plot=np.array([sites_cart[ix,iy,iat] for (ix,iy,iat) in shell_idx])
dist=np.linalg.norm(rvec,axis=-1)
fig,ax=plt.subplots(1,1)
ax.scatter(sites_plot[...,0],sites_plot[...,1],s=80,edgecolor='k',facecolor='none')
cax=ax.scatter(sites_cart[...,0].flatten(),sites_cart[...,1].flatten(),c=dist.flatten(),cmap='rainbow',s=20)
fig.colorbar(cax)
ax.set_aspect('equal')
ax.set_axis_off()
fig.tight_layout()
plt.show()
