#!/usr/bin/env python


#=================================================
# Some functions for 3D plotting using matplotlib
# Shunhong Zhang
#=================================================

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt


def gen_grid_points_on_sphere(nphi,ntheta,conv=1):
    if conv==1: thetas,phis = np.mgrid[0:180:1.j*ntheta,0:360:1.j*nphi]
    if conv==2: thetas,phis = np.mgrid[-90:90:1.j*ntheta,-180:180:1.j*nphi]
    c1 = np.cos(np.deg2rad(thetas))
    s1 = np.sin(np.deg2rad(thetas))
    c2 = np.cos(np.deg2rad(phis))
    s2 = np.sin(np.deg2rad(phis))
    Rvec = np.array([s1*c2,s1*s2,c1])
    return thetas,phis,Rvec


def arrow3d(ax, length=1, width=0.05, head=0.2, headwidth=2,
                theta_x=0, theta_z=0, offset=(0,0,0), **kw):
    from scipy.spatial.transform import Rotation as RT
    w = width
    h = head
    hw = headwidth
    theta_x = np.deg2rad(theta_x)
    theta_z = np.deg2rad(theta_z)

    a = np.array([[0,0],[w,0],[w,(1-h)*length],[hw*w,(1-h)*length],[0,length]])
    r, theta = np.meshgrid(a[:,0], np.linspace(0,2*np.pi,30))
    z = np.tile(a[:,1],r.shape[0]).reshape(r.shape)
    x = r*np.sin(theta)
    y = r*np.cos(theta)

    rot_x = RT.from_rotvec(np.array([1,0,0])*theta_x).as_matrix()
    rot_z = RT.from_rotvec(np.array([0,0,1])*theta_z).as_matrix()

    b1 = np.dot(rot_x, np.c_[x.flatten(),y.flatten(),z.flatten()].T)
    b2 = np.dot(rot_z, b1)
    b2 = b2.T+np.array(offset)
    x = b2[:,0].reshape(r.shape);
    y = b2[:,1].reshape(r.shape);
    z = b2[:,2].reshape(r.shape);
    ax.plot_surface(x,y,z, **kw)



def ax_plot_parallelepiped(ax,latt,scale=1.,
    facecolor='cyan',face_alpha=0.25,
    frame_style='--',
    plot_verts=True,vert_size=10,orig=np.array([0.5,0.5,0.5])):

    points = np.array([[-1, -1, -1],
                      [1, -1, -1 ],
                      [1, 1, -1],
                      [-1, 1, -1],
                      [-1, -1, 1],
                      [1, -1, 1 ],
                      [1, 1, 1],
                      [-1, 1, 1]],float)/2
    points += orig

    Z = scale * np.dot(points,latt)
    if plot_verts: ax.scatter3D(*tuple(Z.T),s=vert_size)

    # list of sides' polygons of figure
    verts = [
     [Z[0],Z[1],Z[2],Z[3]],
     [Z[4],Z[5],Z[6],Z[7]], 
     [Z[0],Z[1],Z[5],Z[4]], 
     [Z[2],Z[3],Z[7],Z[6]], 
     [Z[1],Z[2],Z[6],Z[5]],
     [Z[4],Z[7],Z[3],Z[0]]]

    # plot sides
    ax.add_collection3d(Poly3DCollection(verts, linestyle=frame_style,
    facecolors=facecolor, linewidths=1, edgecolors='r', alpha=face_alpha))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


def plot_parallelepiped(latt,scale=1.,facecolor='cyan',face_alpha=0.25,frame_style='--',
    plot_verts=True,vert_size=10,show=True):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax_plot_parallelepiped(ax,latt,scale,facecolor,face_alpha,frame_style,plot_verts,vert_size)
    if show: plt.show()
    return fig


def map_3d_surface(mapping_prop,map_shape=False,show=False,alpha=0.5,cmap='viridis'):
    import matplotlib as mpl
    if int(mpl.__version__.split('.')[1])>=6: 
        print ('Warning from asd.utility.map_3d_surface')
        print ('matplotlib with version >=3.6 does not work well with Axes3D!')

    ntheta,nphi = mapping_prop.shape
    thetas,phis,Rvec = gen_grid_points_on_sphere(nphi,ntheta)
    if map_shape: 
        mm = abs(np.min(mapping_prop))
        for itheta,iphi in np.ndindex(ntheta,nphi):
            Rvec[:,itheta,iphi] *= mapping_prop[itheta,iphi] + mm

    minn, maxx = mapping_prop.min(), mapping_prop.max()
    norm = mpl.colors.Normalize(minn, maxx)
    m = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    m.set_array([])
    fcolors = m.to_rgba(mapping_prop)

    fig = plt.figure()
    ax = Axes3D(fig)
    surf = ax.plot_surface(*tuple(Rvec), facecolors=fcolors, 
    vmin=minn, vmax=maxx, alpha=alpha,
    shade=True,linewidth=0, antialiased=False, cmap=cmap)
    bb = np.max(abs(Rvec),axis=(1,2))*1.1
    ax.set_xlim(-bb[0],bb[0])
    ax.set_ylim(-bb[1],bb[1])
    ax.set_zlim(-bb[2],bb[2])
    ax.set_axis_off()
    fig.colorbar(surf,shrink=0.6)
    if show: plt.show()
    return fig


def map_sphere_on_2d(mapping_prop,polar=False,show_minima=True,show=False,phis=None,thetas=None,contour=True,cmap='viridis'):
    fig = plt.figure()
    if polar:
        figname+='_polar'
        ax=fig.add_subplot(1,1,1,projection='polar')
        cax=ax.pcolormesh(np.deg2rad(phis),np.deg2rad(thetas),mapping_prop)
        ax.set_ylim(0,np.pi)
        ax.set_yticks([0,np.pi/2,np.pi])
        ax.set_yticklabels(['0','$\pi/2$','$\pi$'],color='r',fontsize=12)
    else:
        min_idx = np.where(mapping_prop==np.min(mapping_prop))
        ax=fig.add_subplot(1,1,1)
        cax=ax.imshow(mapping_prop,extent=[0,360,0,180],origin='lower',cmap=cmap)
        if show_minima and phis is not None and thetas is not None: 
            ax.scatter(phis[min_idx],thetas[min_idx],facecolor='none',edgecolor='r',marker='*',s=50,zorder=1)
        ax.set_xticks(np.arange(0,370,60))
        ax.set_yticks(np.arange(0,190,45))
        ax.set_xlabel('$\\varphi$')
        ax.set_ylabel('$\\theta$')
        ax.set_xlim(0,360)
        ax.set_ylim(0,180)
        if contour: ax.contour(mapping_prop,extent=[0,360,0,180],colors='gray',alpha=0.8,linestyles='--')
    fig.colorbar(cax,shrink=0.6)
    fig.tight_layout()
    if show: plt.show()
    return fig


# contour plot for a irregular mesh
def contour_for_irr_mesh(ax,x0,y0,z0,ngridx=50,ngridy=50):
    import matplotlib.tri as tri
    xi = np.linspace(-np.pi, np.pi, ngridx)
    yi = np.linspace(-np.pi/2, np.pi/2, ngridy)

    x0 = x0.flatten()
    y0 = y0.flatten()
    z0 = z0.flatten()
    # Linearly interpolate the data (x, y) on a grid defined by (xi, yi).
    triang = tri.Triangulation(x0, y0)
    interpolator = tri.LinearTriInterpolator(triang, z0)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)
    ax.contour(xi, yi, zi, levels=14, linewidths=0.5, colors='k')
    return Xi,Yi,zi


def Cartesian_to_Kavaryskiy(x,y,z):
    norm = np.linalg.norm([x,y,z])
    theta = np.arccos(z/norm) - np.pi/2
    phi = - np.angle(x+1.j*y)
    return spherical_to_Kavaryskiy(theta,phi)

 
# theta is latitude  in [-pi/2,pi/2]
# phi   is longitude in [-pi  ,  pi]
def spherical_to_Kavaryskiy(theta,phi):
    x0 = 3*phi/2*np.sqrt(1/3. - (theta/np.pi)**2)
    y0 = theta
    return x0,y0 


def ax_map_sphere_on_2d_Kavrayskiy(ax,mapping_prop,cmap='viridis',scatter_size=8,title=None,contour=True):
    ntheta,nphi = mapping_prop.shape
    thetas,phis,Rvec = gen_grid_points_on_sphere(nphi,ntheta,conv=2)
    thetas = np.deg2rad(thetas)
    phis = np.deg2rad(phis)
    x0,y0 = spherical_to_Kavaryskiy(thetas,phis)
    if contour: 
        Xi,Yi,zi = contour_for_irr_mesh(ax,x0,y0,mapping_prop,ngridx=180,ngridy=60)
        cax = ax.scatter(Xi,Yi,c=zi,cmap=cmap)
    else:
        cax = ax.scatter(x0,y0,c=mapping_prop,cmap=cmap,s=scatter_size)
    ax.set_axis_off()
    ax.set_aspect('equal')
    if title is not None: ax.set_title(title)
    return x0,y0,cax
 

def map_sphere_on_2d_Kavrayskiy(mapping_prop,cmap='viridis',scatter_size=8,title=None,contour=True,show=True):
    fig = plt.figure()
    ax=fig.add_subplot(1,1,1)
    x0,y0,cax = ax_map_sphere_on_2d_Kavrayskiy(ax,mapping_prop,cmap,scatter_size,title,contour)
    fig.colorbar(cax,shrink=0.5)
    fig.tight_layout()
    if show: plt.show()
    return x0,y0,fig


if __name__ == '__main__':
    print ('plotting tools for 3D')
    mapping_prop = np.ones((30,60))
    map_3d_surface(mapping_prop,map_shape=False,show=True,alpha=0.5,cmap='viridis')

