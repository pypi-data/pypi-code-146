import numpy as np

def manifold_dim():
    return (2,2)

def vector_dim():
    return (1,)

def SVDO(so2_mat):
    assert so2_mat.shape == (2,2)
    U,S,VT = np.linalg.svd(so2_mat)
    S_dash = np.identity(2)
    S_dash[1,1] = np.linalg.det(U@VT)
    return U@S_dash@VT

def identity():
    return np.identity(2)

def perturb_local(so2_mat, theta):
    theta = float(theta)
    return so2_mat@Exp(theta)

def perturb_global(so2_mat, theta):
    theta = float(theta)
    return Exp(theta)@so2_mat


    


def inv(so2_mat):
    assert se2_mat.shape == (2,2)
    return se2_mat.T

def Exp(theta):
    cosine = np.cos(theta)
    sine = np.sin(theta)
    so2_mat = np.array([[cosine, -sine],[sine, cosine]])
    return so2_mat

def Log(so2_mat):
    cosine = so2_mat[0,0]
    sine = so2_mat[1,0]
    theta = np.arctan2(sine,cosine)
    return theta

def adjoint(so2_mat):
    return 1.0

