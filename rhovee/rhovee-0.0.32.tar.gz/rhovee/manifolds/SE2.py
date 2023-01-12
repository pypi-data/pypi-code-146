import numpy as np
from . import SO2
from .utils import *
from rhovee.plot import draw_arrowhead, draw_coord_sys_2d
import matplotlib.pyplot as plt

def plot(ax, se2_mat, size=1.0, label='', style='vec', color=None):
    R,t = to_Rt(se2_mat)
    x_axis = R[:2,0]
    y_axis = R[:2,1]
    #ax.plot(t[0],t[1], 'ro')
    if style == 'vec':
        draw_coord_sys_2d(ax, x_axis, y_axis, t, size, label, color=color)
    elif style == 'dir_x':
        draw_arrowhead(ax, x_axis, t, label=label, color=color)
    elif style == 'dir_y':
        draw_arrowhead(ax, y_axis, t, label=label, color=color)

def plot_trajectory(ax, se2_list, num_plot_poses=5, color='black', size=1):
    num_poses = len(se2_list)
    num_plot_poses = min(num_poses, num_plot_poses)
    idx_poses_to_plot = np.linspace(0,num_poses-1, num_plot_poses).astype(np.uint32)
    for idx in idx_poses_to_plot:
        plot(ax, se2_list[idx], size=size)
    se2_np_arr = np.array(se2_list)
    xs = se2_np_arr[:,0,2]
    ys = se2_np_arr[:,1,2]
    ax.plot(xs,ys)

def identity():
    return np.identity(3)

def tangent_delta(se2_mat, se2_defining_tangent):
    delta = Log(inv(se2_defining_tangent)@se2_mat)
    return delta

def tf_point(se2_mat, point):
    point = np.array(point).flatten()
    R,t = to_Rt(se2_mat)
    return R@point + t
    
def perturb_local(se2_mat, se2_vec):
    return se2_mat@Exp(se2_vec)

def perturb_global(se2_mat, se2_vec):
    return Exp(se2_vec)@se2_mat
    

def manifold_dim():
    return (3,3)

def vector_dim():
    return (3,)

def Rt(R,t):
    assert R.shape == (2,2)
    se2_mat = np.identity(3)
    se2_mat[:2,:2] = R
    se2_mat[:2,2] = t
    return se2_mat

def inv(se2_mat):
    R,t = to_Rt(se2_mat)
    inv_T = np.identity(3)
    inv_T[:2,:2] = R.T
    inv_T[:2,2] = -R.T@t
    return inv_T

def to_Rt(se2_mat):
    R = se2_mat[:2,:2]
    t = se2_mat[2,:2]
    return R,t

def SVDO(se2_mat):
    R,t = to_Rt(se2_mat)
    R = SO2.SVDO(R)
    return Rt(R,t)

def Rz(angle, t=[0,0], unit='rad'):
    t = np.array(t).flatten()
    assert t.shape == (2,)
    angle = angle_as_rad(angle, unit)
    R = SO2.Exp(angle)
    return Rt(R, t)

    


def to_Rt(SE2_mat):
    rot_mat = SE2_mat[:2,:2]
    t = SE2_mat[:2,2]
    return rot_mat, t


def V_helper(theta):
    if np.isclose(theta, 0):
        return np.identity(2)
    V = np.sin(theta)/theta * np.identity(2) + (1-np.cos(theta))/theta*skew2(1)
    return V

def V_inv_helper(theta):
    return np.linalg.inv(V_helper(theta))

def Exp(vec):
    assert vec.shape == (3,)
    SE2_mat = np.identity(3)
    theta = vec[2]
    rho = vec[:2]
    SO2_mat = SO2.Exp(theta)
    SE2_mat[:2,:2] = SO2_mat
    t = V_helper(theta)@rho
    SE2_mat[:2, 2] = t
    return SE2_mat

def Log(SE2_mat):
    assert SE2_mat.shape == (3,3)
    vec = np.zeros(3)
    R,t = to_Rt(SE2_mat)
    theta = SO2.Log(R)
    rho = V_inv_helper(theta)@t
    vec[:2] = rho
    vec[2] = theta
    return vec

def adjoint(SE2_mat):
    ad = np.identity(3)
    R,t = to_Rt(SE2_mat)
    ad[:2,:2] = R
    ad[:2, 2] = -skew2(1)@t
    return ad

def right_jacobian(vec):
    assert vec.shape == (3,)
    rho_1 = vec[0]
    rho_2 = vec[1]
    theta = vec[2]
    if np.allclose(theta, np.zeros(3)):
        return np.identity(3)
    right_jacob = np.zeros((3,3))
    sin_th = np.sin(theta)
    cos_th = np.cos(theta)
    right_jacob[0,0] = sin_th/theta
    right_jacob[1,0] = (cos_th - 1)/theta
    right_jacob[2,0] = 0.0
    right_jacob[0,1] = (1-cos_th)/theta
    right_jacob[1,1] = sin_th/theta
    right_jacob[2,1] = 0.0
    right_jacob[0,2] = (theta*rho_1 - rho_2 + rho_2*cos_th - rho_1*sin_th)/(theta**2)
    right_jacob[1,2] = (rho_1+theta*rho_2-rho_1*cos_th-rho_2*np.sin(theta))/theta**2
    right_jacob[2,2] = 1.0
    return right_jacob

def inv_right_jacobian(vec):
    assert vec.shape == (3,)
    return np.linalg.inv(right_jacobian(vec))

def left_jacobian(vec):
    assert vec.shape == (3,)
    return right_jacobian(-vec)



