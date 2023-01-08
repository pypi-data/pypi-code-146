#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

latt = np.array([[1,0],[-0.5,np.sqrt(3)/2]])
sites = np.array([[0,0]])

outdir = 'triangular'
four_site = np.loadtxt('{}/quadruplet'.format(outdir),skiprows=2)

polygons = []
for ii,pla in enumerate(four_site):
    polygon = [[0,0]]
    for jj in range(3):
        R = pla[np.array([2+4*jj,3+4*jj],int)]
        Rc = np.dot(sites[int(pla[1+4*jj])]+R, latt)
        polygon.append(Rc)
    polygons.append(polygon)
polygons = np.array(polygons)

fig,axes=plt.subplots(1,2,sharey=True,figsize=(6,3))
for ii in range(2):
    ax = axes[ii]
    for polygon in polygons[ii::2]:
        ax.fill(*tuple(polygon.T),alpha=0.5)
    ax.set_aspect('equal')
    ax.set_axis_off()
plt.show()
