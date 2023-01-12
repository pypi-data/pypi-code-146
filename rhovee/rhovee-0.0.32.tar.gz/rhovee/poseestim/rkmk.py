import numpy as np
import math
import matplotlib.pyplot as plt
from rhovee import manifolds
    
def solve_RKMK_row(A_row, Fs):
    Theta = np.zeros(Fs[0].shape[0])
    for j in range(len(Fs)):
        Theta+=Fs[j]*A_row[j]
    return Theta

def sum_to_current_est(Fs, Bs):
    assert (len(Fs) == len(Bs))
    sum_vec = np.zeros(Fs[0].shape[0])
    for i in range(len(Fs)):
        sum_vec += Bs[i]*Fs[i]
    return sum_vec

class ButcherTableu():
    @property
    def heun(self):
        As = np.array([[0.0,0.0],[1.0,0.0]])
        Bs = np.array([0.5,0.5])
        Cs = np.array([0.0,1.0])
        heuns = (As,Bs,Cs)
        return heuns

    @property
    def euler(self):
        As = np.array([[0.0]])
        Bs = np.array([1.0])
        Cs = np.array([0.0])
        return (As,Bs,Cs)

    @property
    def rk4(self):
        As = np.zeros((4,4))
        As[1,0] = 0.5
        As[2,1] = 0.5
        As[3,2] = 1.0
        Bs = np.array([1.0/6.0, 1.0/3.0, 1.0/3.0, 1.0/6.0])
        Cs = np.array([0.0, 0.5,0.5,1.0])
        return (As,Bs,Cs)

butcher_tableu = ButcherTableu()



def RKMK(steps, kinematics, sim_duration, butcher_tableu, manifold):
    assert isinstance(butcher_tableu, tuple)
    mf = manifold
    mf_shape = mf.manifold_dim()
    mf_vec_shape = mf.vector_dim()
    As,Bs,Cs = butcher_tableu
    A_rows, A_cols = As.shape
    assert A_rows == len(Cs)
    assert A_cols == len(Bs)
    result = []

    stages = len(Cs)
    time = 0
    h = sim_duration/steps
    T0 = np.identity(mf_shape[0])

    T = T0
    result.append(T)
    for step in range(0,steps):
        Fs = []
        Theta0 = np.zeros(mf_vec_shape[0])
        F0 = h*kinematics(T0, time+Cs[0]*h)
        Fs.append(F0)
        for s in range(1,stages):
            A_row = As[s,:]
            Theta = solve_RKMK_row(A_row, Fs)
            theta = h*kinematics(T@mf.Exp(Theta), time+Cs[s]*h)
            inv_jac = mf.inv_right_jacobian(Theta)
            F = inv_jac@theta
            Fs.append(F)
        Theta = sum_to_current_est(Fs, Bs)
        T = T@mf.Exp(Theta)
        result.append(T)
        time += h
    return result
            
