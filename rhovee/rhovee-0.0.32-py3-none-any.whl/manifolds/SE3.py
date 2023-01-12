from . import SO3
from .utils import *

def manifold_dim():
    return (4,4)

def vector_dim():
    return (6,)

def to_Rt(se3_mat):
    assert se3_mat.shape == (4,4)
    R = se3_mat[0:3,0:3]
    t = se3_mat[0:3,3]
    return R, t

def inv(se3_mat):
    R,t = to_Rt(se3_mat)
    inv_T = np.identity(4)
    inv_T[:3,:3] = R.T
    inv_T[:3,3] = (-R.T@t).flatten()
    return inv_T

def from_Rt(R,t):
    t = t.flatten()
    assert R.shape == (3,3)
    assert t.shape == (3,)
    T = np.identity(4)
    T[:3,:3] = R
    T[:3,3] = t
    return T

def Rx(angle, t=[0,0,0], unit='rad'):
    t = np.array(t).flatten()
    assert t.shape == (3,)
    R = SO3.Rx(angle, unit)
    return from_Rt(R,t)

def Ry(angle, t=[0,0,0], unit='rad'):
    t = np.array(t).flatten()
    assert t.shape == (3,)
    R = SO3.Ry(angle, unit)
    return from_Rt(R,t)

def Rz(angle, t=[0,0,0], unit='rad'):
    t = np.array(t).flatten()
    assert t.shape == (3,)
    R = SO3.Rz(angle, unit)
    return from_Rt(R,t)


def identity():
    return np.identity(4)

def perturb_local(se3_mat, se3_vec):
    se3_vec = np.array(se3_vec).flatten()
    return se3_mat@Exp(se3_vec)

def perturb_global(se3_mat, se3_vec):
    se3_vec = np.array(se3_vec).flatten()
    return Exp(se3_vec)@se3_mat



def SVDO(se3_mat):
    R,t = to_Rt(se3_mat)
    R = SO3.SVDO(R)
    return from_Rt(R,t)


def wedge(vec):
    vec = np.array(vec)
    assert vec.shape == (6,)
    SE3_lie_alg = np.zeros((4,4))
    rho = vec[0:3]
    theta = vec[3:6]
    SO3_lie_alg = SO3.wedge(theta)
    SE3_lie_alg[0:3,0:3] = SO3_lie_alg
    SE3_lie_alg[0:3,3] = rho
    return SE3_lie_alg

def vee(lie_alg):
    assert lie_alg.shape == (4,4)
    SO3_lie_alg = lie_alg[0:3,0:3]
    rho = lie_alg[0:3,3]
    omega = SO3.vee(SO3_lie_alg)
    return np.concatenate((rho,omega))

def Exp(vec):
    vec = np.array(vec)
    assert vec.shape == (6,)
    transf_mat = np.identity(4)
    rho = vec[0:3]
    theta = vec[3:6]
    rot_mat = SO3.Exp(theta)
    transf_mat[0:3,0:3] = rot_mat
    transf_mat[0:3,3] = SO3.left_jacob(theta) @ rho
    return transf_mat

def exp(lie_alg):
    assert lie_alg.shape == (4,4)
    transf_mat = np.identity(4)
    u_skew = lie_alg[:3,:3]
    rho = lie_alg[:3, 3]
    R = SO3.exp(u_skew)
    transf_mat[0:3,0:3] = R
    transf_mat[0:3,3] = SO3.left_jacob(theta) @ rho
    return transf_mat

def Log(se3_mat):
    assert se3_mat.shape == (4,4)
    R,t = to_Rt(se3_mat)
    theta = SO3.Log(R)
    rho = SO3.inv_left_jacob(theta) @ t
    rho = np.squeeze(rho)
    return np.concatenate((rho,theta))

def log(se3_mat):
    return exp(Log(se3_mat))

def adjoint(se3_mat):
    ad = np.zeros((6,6))
    rot_mat, transl = to_Rt(se3_mat)
    skew_t = SO3.wedge(transl)
    ad[:3,:3] = rot_mat
    ad[:3, 3:6] = skew_t@rot_mat
    ad[3:6, 3:6] = rot_mat
    return ad



def jacob_q_term(vec):
    assert vec.shape == (6,)
    rho = vec[:3] # rho
    th = vec[3:] # theta
    an = np.linalg.norm(th) # angle
    skew_om = skew3(th)
    skew_rho = skew3(rho)
    cos_an = np.cos(an)
    sin_an = np.sin(an)

    term1 = 0.5*skew_rho
    term2 = (an - sin_an)/an**3
    term3 = skew_om @ skew_rho + skew_rho @ skew_om + skew_om @ skew_rho @ skew_om
    term4 = (1-an**2/2-np.cos(an))/an**4
    term5 = skew_om@skew_om@skew_rho+skew_rho@skew_om@skew_om-3*skew_om@skew_rho@skew_om
    term6 = 0.5*((1-an**2/2-cos_an)/(an**4)-3*(an-sin_an-an**3/6)/(an**5))
    term7 = skew_om@skew_rho@skew_om@skew_om+skew_om@skew_om@skew_rho@skew_om
    Q = term1 + term2*term3 - term4*term5 - term6*term7
    return Q


def left_jacobian(vec):
    vec = np.array(vec)
    assert vec.shape == (6,)
    if np.isclose(np.linalg.norm(vec), 0.):
        return np.identity(6) #+ 0.5 * wedge(vec)
    omega = vec[3:6]

    jacob = np.zeros((6,6))
    SO3_left_jacobian = SO3.left_jacob(omega)
    Q = jacob_q_term(vec)
    jacob[0:3,0:3] = SO3_left_jacobian
    jacob[0:3,3:] = Q
    jacob[3:,3:] = SO3_left_jacobian
    return jacob


def inv_left_jacobian(vec):
    vec = np.array(vec)
    assert vec.shape == (6,)
    if np.isclose(np.linalg.norm(vec), 0.):
        return np.identity(6) # todo: add first order taylor exp
    inv_jacob = np.zeros((6,6))
    theta_bold = vec[3:6]
    SO3_inv_left_jacobian = SO3.inv_left_jacob(theta_bold)
    Q = jacob_q_term(vec)
    inv_jacob[0:3,0:3] = SO3_inv_left_jacobian
    inv_jacob[0:3,3:] = -SO3_inv_left_jacobian@Q@SO3_inv_left_jacobian
    inv_jacob[3:,3:] = SO3_inv_left_jacobian
    return inv_jacob

def right_jacobian(vec):
    return left_jacobian(-vec)

def inv_right_jacobian(vec):
    vec = np.array(vec)
    assert vec.shape == (6,)
    return inv_left_jacobian(-vec)



def look_at(origin, target, up, approach_vec='z', up_vec='x'):
    assert approach_vec=='z' or approach_vec=='y' or approach_vec=='x'
    assert up_vec=='z' or up_vec=='y' or up_vec=='x'
    assert up_vec != approach_vec
    origin = np.array(origin)
    target = np.array(target)
    up = np.array(up)
    print("Origin", origin)
    print("Target", target)
    print("Up", up)
    assert origin.shape[0] == 3 and target.shape[0] == 3
    T = np.eye(4)
    T[:3,3] = origin
    approach_dir = (target-origin)
    approach_dir = approach_dir/np.linalg.norm(approach_dir)
    print("Approach dir", approach_dir)

    if approach_vec == 'x':
        T[:3,0] = approach_dir
        if up_vec == 'y':
            side_vec = np.cross(approach_dir, up)
            side_vec = side_vec/np.linalg.norm(side_vec)
            T[:3,2] = side_vec
            T[:3,1] = np.cross(side_vec, approach_dir)
        elif up_vec == 'z':
            pass
        else:
            assert False
    elif approach_vec == 'y':
        pass
    elif approach_vec == 'z':
        T[:3,2] = approach_dir
        if up_vec == 'y':
            side_vec = np.cross(approach_dir, up)
            side_vec = side_vec/np.linalg.norm(side_vec)
            T[:3,0] = side_vec
            T[:3,1] = np.cross(approach_dir, side_vec)
        elif up_vec == 'x':
            side_vec = np.cross(approach_dir, up)
            side_vec = side_vec/np.linalg.norm(side_vec)
            T[:3,1] = side_vec
            T[:3,0] = np.cross(side_vec, approach_dir)

    else: 
        assert False



    print(T)
    det = np.linalg.det(T[:3,:3])
    print("Determinant", det)
    assert np.isclose(det, 1.0)
    return T





       






if __name__ == '__main__':
    T = np.identity(4)
    inv(T)
